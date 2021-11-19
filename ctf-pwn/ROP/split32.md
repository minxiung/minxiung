1. `file split`

```bash
$ file split32
split32: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), 
dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 3.2.0, 
BuildID[sha1]=76cb700a2ac0484fb4fa83171a17689b37b9ee8d, not stripped
```

2. gdb-peda, checksec

```bash
$ gdb-peda split32                                                                                                1 ⨯
Reading symbols from split32...
(No debugging symbols found in split32)
gdb-peda$ checksec
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : Partial
gdb-peda$
```

3. `r2 split32`, `aa`, `afl`. pay attention to three function **pwnme**, **usefulFunction**,  **main**.

```bash
[0x08048546]> afl
0x08048430    1 50           entry0
0x08048463    1 4            fcn.08048463
0x080483f0    1 6            sym.imp.__libc_start_main
0x08048490    4 50   -> 41   sym.deregister_tm_clones
0x080484d0    4 58   -> 54   sym.register_tm_clones
0x08048510    3 34   -> 31   sym.__do_global_dtors_aux
0x08048540    1 6            entry.init0
0x080485ad    1 95           sym.pwnme                  ===> this one
0x08048410    1 6            sym.imp.memset
0x080483d0    1 6            sym.imp.puts
0x080483c0    1 6            sym.imp.printf
0x080483b0    1 6            sym.imp.read
0x0804860c    1 25           sym.usefulFunction         ===> this one
0x080483e0    1 6            sym.imp.system
0x08048690    1 2            sym.__libc_csu_fini
0x08048480    1 4            sym.__x86.get_pc_thunk.bx
0x08048694    1 20           sym._fini
0x08048630    4 93           sym.__libc_csu_init
0x08048470    1 2            sym._dl_relocate_static_pie
0x08048546    1 103          main                       ===> this one
0x08048400    1 6            sym.imp.setvbuf
0x08048374    3 35           sym._init
0x08048420    1 6            sym..plt.got
[0x08048546]>
```

4. `s main`, `VV`. there is 
![Image](https://i.imgur.com/REFe4H5.png)


5. `s sym.pwnme`, `VV`
![Image](https://i.imgur.com/Hpm9vGe.png)

6. `s sym.usefulfunction`, `VV`

## TBC