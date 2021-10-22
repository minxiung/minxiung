1. use `file <file>` to take a look.

```
$ file run-asm.asm
run-asm.asm: ASCII text
```

2. use `cat <file>' to see the context. It look like just put something into the stack.
```
$ cat run-asm.asm
global _start

section .text
_start:
  mov rax, 1
  mov rdi, 1
  push 0x7d214e75
  push 0x525f646e
  push 0x345f6d53
  push 0x615f6531
  push 0x69706d30
  push 0x437b4654
  push 0x43747372
  push 0x6946794d
  mov rsi, rsp
  mov rdx, 0x40
  syscall

  mov rax, 60
  mov rdi, 0
  syscall
```
3. transfer the hex to string, I write a python script to do that.
```
hex_string = "7d214e75525f646e345f6d53615f653169706d30437b4654437473726946794d"

byte_array = bytearray.fromhex(hex_string)
byte_array.decode()
reverse_string=''.join(reversed(byte_array.decode()))
print(reverse_string)
```

4. run the python script and get the flag.
```
$ python3 strings.py
MyFirstCTF{C0mpi1e_aSm_4nd_RuN!}
```
