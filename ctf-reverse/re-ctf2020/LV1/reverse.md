1. use `file <file>` to take a look.
```
$ file reverse
reverse: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, 
for GNU/Linux 2.6.32, BuildID[sha1]=0eae3e9fd6d9a63980d737561cba79a68e655c9f, not stripped
```

2. use `strings <file>` to take a look. Find the flag.

```
$ strings reverse
/lib/ld-linux.so.2
libc.so.6
_IO_stdin_used
gets
puts
__libc_start_main
__gmon_start__
GLIBC_2.0
PTRh
QVh;
UWVS
t$,U
[^_]
BreakALLCTF{4U49uY7OJCrJL0vtbXjd}
Try again?
;*2$"(
GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.4) 5.4.0 20160609
crtstuff.c
__JCR_LIST__
deregister_tm_clones
__do_global_dtors_aux
completed.7200
__do_global_dtors_aux_fini_array_entry
frame_dummy
__frame_dummy_init_array_entry
re-1.c
__FRAME_END__
__JCR_END__
__init_array_end
_DYNAMIC
__init_array_start
__GNU_EH_FRAME_HDR
_GLOBAL_OFFSET_TABLE_
__libc_csu_fini
_ITM_deregisterTMCloneTable
__x86.get_pc_thunk.bx
gets@@GLIBC_2.0
_edata
__data_start
puts@@GLIBC_2.0
__gmon_start__
__dso_handle
_IO_stdin_used
__libc_start_main@@GLIBC_2.0
__libc_csu_init
_fp_hw
__bss_start
main
_Jv_RegisterClasses
__TMC_END__
_ITM_registerTMCloneTable
.symtab
.strtab
.shstrtab
.interp
.note.ABI-tag
.note.gnu.build-id
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rel.dyn
.rel.plt
.init
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
.got.plt
.data
.bss
.comment
```

flag: BreakALLCTF{4U49uY7OJCrJL0vtbXjd}
