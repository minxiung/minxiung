1. use `file <file>` to take a look.

```
$ file base64
base64: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter 
/lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=c38c6095d7833d84847ad96ad407feb9df8aa1db, stripped
```

2. use `strings <file>` to take a look, there's some special string out there after the regular ABCDEF...strings.

```
$ strings base64
/lib64/ld-linux-x86-64.so.2
libc.so.6
__isoc99_scanf
puts
__stack_chk_fail
realloc
strlen
malloc
__ctype_b_loc
__cxa_finalize
__libc_start_main
_ITM_deregisterTMCloneTable
__gmon_start__
_Jv_RegisterClasses
_ITM_registerTMCloneTable
GLIBC_2.3
GLIBC_2.7
GLIBC_2.4
GLIBC_2.2.5
dH34%(
dH34%(
AWAVA
AUATL
[]A\A]A^A_
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/I can decode base64
%399s
The output is
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/
;*3$"
cHVzaCAweDdkMjEyMTIxCnB1c2ggMHg0NzZlNjk1MgpwdXNoIDB4NzQ1MzVmNjMKcHVzaCAweDMxNDczNDZkCnB1c2ggMHg1ZjQ0NmU2YwpwdXNoIDB4NDY1ZjU1MzAKcHVzaCAweDU5N2I0NjU0CnB1c2ggMHg0Mzc0NzM3MgpwdXNoIDB4Njk0Njc5NGQK
GCC: (Ubuntu 6.3.0-12ubuntu2) 6.3.0 20170406
.shstrtab
.interp
.note.ABI-tag
.note.gnu.build-id
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rela.dyn
.init
.plt
.plt.got
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.init_array
.fini_array
.jcr
.dynamic
.data
.bss
.comment
```

3. run the program, it says it is a base64 decoder, so i put the interesting strings we found in stap 2 into this program, and get the stack push asm coed.

```
$ ./base64
I can decode base64
cHVzaCAweDdkMjEyMTIxCnB1c2ggMHg0NzZlNjk1MgpwdXNoIDB4NzQ1MzVmNjMKcHVzaCAweDMxNDczNDZkCnB1c2ggMHg1ZjQ0N
mU2YwpwdXNoIDB4NDY1ZjU1MzAKcHVzaCAweDU5N2I0NjU0CnB1c2ggMHg0Mzc0NzM3MgpwdXNoIDB4Njk0Njc5NGQK
The output is
push 0x7d212121
push 0x476e6952
push 0x74535f63
push 0x3147346d
push 0x5f446e6c
push 0x465f5530
push 0x597b4654
push 0x43747372
push 0x6946794d
```
4. use the python script below to tranfer the hex to strings, and we get the flag.

```
hex_string = input("input the data: ")

byte_array = bytearray.fromhex(hex_string)
byte_array.decode()
reverse_string=''.join(reversed(byte_array.decode()))
print(reverse_string)
```

```
$ python3 push_stack_decode.py
input the data: 7d212121476e695274535f633147346d5f446e6c465f5530597b4654437473726946794d
MyFirstCTF{Y0U_FlnD_m4G1c_StRinG!!!}
```

flag: MyFirstCTF{Y0U_FlnD_m4G1c_StRinG!!!}
