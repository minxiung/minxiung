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

3. `r2 split`, `aa`, `afl`, I notice the special function **pwnme**, **usefulFunction**. Ichoose ti see the main function first. It seems do nothing but print some strings.

![Image](https://i.imgur.com/6wijIYI.png)

4. go to see another function pwnme. we have a input which store at **var_20h(rbp-0x20)**. 

![Image](https://i.imgur.com/nvN8Qsf.png)

5. and the usefulfunction is below.

![Image](https://i.imgur.com/NmfH83V.png)