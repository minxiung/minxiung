1. in IDA pro, 首先看到有stack cookies的防護機制。

```
; int __cdecl main(int argc, const char **argv, const char **envp)
_main proc near

; __unwind { // __except_handler4
push    ebp
mov     ebp, esp
push    0FFFFFFFEh
push    offset stru_403688
push    offset __except_handler4
mov     eax, large fs:0
push    eax
add     esp, 0FFFFFF40h
mov     eax, ___security_cookie   ======>有stack cookies
xor     [ebp+ms_exc.registration.ScopeTable], eax
xor     eax, ebp
mov     [ebp+var_1C], eax
push    ebx
push    esi
push    edi
push    eax
lea     eax, [ebp+ms_exc.registration]
mov     large fs:0, eax
mov     [ebp+ms_exc.old_esp], esp
mov     dword ptr [ebp+var_B8], 0
mov     [ebp+var_CC], 1
mov     [ebp+var_D0], 1
```

再來大概看一下，發現有疑似可以走後門的地方。
![Image](https://i.imgur.com/s0MwAF4.png)


接下來F5查看反組譯結果。
```c
int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
  FILE *v3; // eax
  FILE *v4; // eax
  int v5; // [esp+20h] [ebp-C0h]
  int v6; // [esp+24h] [ebp-BCh]
  char v7; // [esp+28h] [ebp-B8h]
  int i; // [esp+2Ch] [ebp-B4h]
  char v9[128]; // [esp+44h] [ebp-9Ch] BYREF
  CPPEH_RECORD ms_exc; // [esp+C8h] [ebp-18h]

  ms_exc.registration.TryLevel = 0;
  v3 = _acrt_iob_func(1u);
  setvbuf(v3, 0, 4, 0);
  v4 = _acrt_iob_func(0);
  setvbuf(v4, 0, 4, 0);
  puts("ouch! Do not kill me , I will tell you everything");
  sub_401420("stack address = 0x%x\n", (char)v9);
  sub_401420("main address = 0x%x\n", (char)main);
  for ( i = 0; i < 10; ++i )
  {
    puts("Do you want to know more?");
    sub_401000(v9, 10);
    v6 = strcmp(v9, "yes");
    if ( v6 )
      v6 = v6 < 0 ? -1 : 1;
    if ( v6 )
    {
      v5 = strcmp(v9, "no");
      if ( v5 )
        v5 = v5 < 0 ? -1 : 1;
      if ( !v5 )
        break;
      sub_401000(v9, 256);   ======> BOF
    }
    else
    {
      puts("Where do you want to know");
      v7 = sub_401060();
      sub_401420("Address 0x%x value is 0x%x\n", v7);
    }
  }
  ms_exc.registration.TryLevel = -2;
  puts("I can tell you everything, but I never believe 1+1=2");
  puts("AAAA, you kill me just because I don't think 1+1=2??");
  exit(0);
}
```

首先查看sub_401420()函式，猜測應該是print類函式。

```c
sub_401420("stack address = 0x%x\n", (char)v9);
sub_401420("main address = 0x%x\n", (char)main);
```
在程式的一開始就會print出stack address和main address，因此也不怕stack address改變和ASLR了。

接著查看sub_401000函式，是一個get使用者輸入的函式。    
可以看到v9長度只有128，但是卻可以输入256，導致BOF，但是程式出口全部都由exit堵上了。
```c
int __cdecl sub_401000(int a1, int a2)
{
  int i; // [esp+0h] [ebp-8h]
  char v4; // [esp+7h] [ebp-1h]

  for ( i = 0; ; ++i )
  {
    v4 = getchar();
    if ( i == a2 )
      break;
    if ( v4 == 10 )
    {
      *(_BYTE *)(i + a1) = 0;
      return i;
    }
    *(_BYTE *)(i + a1) = v4;
  }
  return i;
}
```

接下來分析這段:
```c
v6 = strcmp(v9, "yes");
    if ( v6 )
      v6 = v6 < 0 ? -1 : 1;
    if ( v6 )
    {
      v5 = strcmp(v9, "no");
      if ( v5 )
        v5 = v5 < 0 ? -1 : 1;
      if ( !v5 )
        break;
      sub_401000(v9, 256);
    }
    else
    {
      puts("Where do you want to know");
      v7 = sub_401060();
      sub_401420("Address 0x%x value is 0x%x\n", v7);
    }
```
當我們的輸入no時，會退出，輸入非no非yes時會stack overflow，輸入yes時，v6==0，會進入else分支，查看sub_401060()。
```c
int sub_401060()
{
  char String; // [esp+0h] [ebp-14h] BYREF
  int v2; // [esp+1h] [ebp-13h]
  int v3; // [esp+5h] [ebp-Fh]
  int v4; // [esp+9h] [ebp-Bh]
  __int16 v5; // [esp+Dh] [ebp-7h]
  char v6; // [esp+Fh] [ebp-5h]

  String = 0;
  v2 = 0;
  v3 = 0;
  v4 = 0;
  v5 = 0;
  v6 = 0;
  sub_401000((int)&String, 15);
  return atoi(&String);
}
```
該函式會吃我們輸入並將字符串轉為int。    
所以這裡如果想得知地址的值的话，需要将目標地址的十六進制轉換成十進制输入，同時，這裡如果atoi轉換的是一个非數字型數字，那麼轉換會失敗，程式會進入異常處理seh。

之前我們曾經發現疑似後門的system("cmd")，如果能夠控制eip，通過之前我们洩漏出的function address，算出偏移，直接跳轉到system（"cmd"），就可以直接完成攻擊了。

### SEH
Structured Exception Handling, 結構化例外狀況處理。
是Windows作業系統上，Microsoft對C/C++程序語言做的語法擴展，用於處理異常事件的程序控制結構。

異常事件是打斷程序正常執行流程的不在期望之中的硬體、軟體事件。硬體異常是CPU拋出的如「除0」、數值溢出等；軟體異常是作業系統與程序通過RaiseException語句拋出的異常。

Microsoft擴展了C語言的語法，用 try-except與try-finally語句來處理異常。[1]異常處理程序可以釋放已經獲取的資源、顯示出錯信息與程序內部狀態供調試、從錯誤中恢復、嘗試重新執行出錯的代碼或者關閉程序等等。

一個__try語句不能既有__except，又有__finally。但try-except與try-finally語句可以嵌套使用。

SEH stack frame:
![Image](https://i.imgur.com/tMuXGKi.png)


### SafeSEH


    




