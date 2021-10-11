1. use `file <file>` command to see the file, it's a ELF file.
2. use `xxd <file> | grep easy` to take a look and fortunatly we find the flag.

```
00001030: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00001040: 6561 7379 6374 667b 6562 3034 6661 6466  easyctf{eb04fadf
00001050: 7d00 4743 433a 2028 5562 756e 7475 2034  }.GCC: (Ubuntu 4
00001060: 2e38 2e34 2d32 7562 756e 7475 317e 3134  .8.4-2ubuntu1~14
```

flag:easyctf{eb04fadf}
