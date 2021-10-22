1. use `file <file>` command to take a look.

```
$ file BabyAssembly.exe
BabyAssembly.exe: PE32 executable (console) Intel 80386, for MS Windows
```

2. use `strings <file>` to take a look. there's something like flag.

```
$ strings BabyAssembly.exe
!This program cannot be run in DOS mode.
Rich/
TJO[
.textbss
.text
`.rdata
@.data
.idata
@.00cfg
@.rsrc
@.reloc
Brea
kAll
CTF{
Y35_
1_m3
an_7
h1s_
0n3}
```

flag: BreakAllCTF{Y35_1_m3an_7h1s_0n3}

p.s. If you use `strings <file> | grep CTF` to search, you may find a fake flag like bellow.
```
$ strings BabyAssembly.exe | grep CTF
CTF{
./config/CGCTF{is_this_the_flag}.txt
```
