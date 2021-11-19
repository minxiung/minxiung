1. `file callme`

```bash
$ file callme
callme: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=e8e49880bdcaeb9012c6de5f8002c72d8827ea4c, not stripped
```

2. `gdb-peda callme`, `checksec`

```bash
$ gdb-peda callme
Reading symbols from callme...
(No debugging symbols found in callme)
gdb-peda$ checksec
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : Partial
gdb-peda$
```

3. `r2 callme`, `aa`, `afl`, several function needs to be checkout.

```bash
$ r2 callme
[0x00400760]> aa
[x] Analyze all flags starting with sym. and entry0 (aa)
[0x00400760]> afl
0x00400760    1 42           entry0
0x004006a8    3 23           sym._init
0x004009b4    1 9            sym._fini
0x004007a0    4 42   -> 37   sym.deregister_tm_clones
0x004007d0    4 58   -> 55   sym.register_tm_clones
0x00400810    3 34   -> 29   sym.__do_global_dtors_aux
0x00400840    1 7            entry.init0
0x00400898    1 90           sym.pwnme                  ====>
0x00400700    1 6            sym.imp.memset
0x004006d0    1 6            sym.imp.puts
0x004006e0    1 6            sym.imp.printf
0x00400710    1 6            sym.imp.read
0x004008f2    1 74           sym.usefulFunction         ====>
0x004006f0    1 6            sym.imp.callme_three       ====>
0x00400740    1 6            sym.imp.callme_two         ====>
0x00400720    1 6            sym.imp.callme_one         ====>
0x00400750    1 6            sym.imp.exit
0x004009b0    1 2            sym.__libc_csu_fini
0x00400940    4 101          sym.__libc_csu_init
0x00400790    1 2            sym._dl_relocate_static_pie
0x00400847    1 81           main                       ====>
0x00400730    1 6            sym.imp.setvbuf
[0x00400760]>
```

