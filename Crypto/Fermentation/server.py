#!/usr/bin/env python3

import random
from Crypto.Util.number import getPrime, bytes_to_long, isPrime

def generate_weak_rsa_keys():
    p = getPrime(2048)
    
    offset = random.randint(100, 50000)
    q_candidate = p + offset
    
    if q_candidate % 2 == 0:
        q_candidate += 1
    
    while not isPrime(q_candidate):
        q_candidate += 2
    
    q = q_candidate
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 0x1000001 
    d = pow(e, -1, phi)
    
    return n, e, d, p, q

def encrypt_flag():
    try:
        with open('/Users/aurora/krieg/InductionCTF/Fermentation/flag.txt', 'r') as f:
            flag = f.read().strip()
    except FileNotFoundError:
        flag = "InductionCTF{why_w0uld_7h3_4dm1n_l34v3_7h3_fl4g_h3r3_dumb455}"
    
    n, e, d, p, q = generate_weak_rsa_keys()
    
    flag_bytes = flag.encode()
    m = bytes_to_long(flag_bytes)
    c = pow(m, e, n)
    
    with open('values.txt', 'w') as f:
        f.write(f"n = {n}\n")
        f.write(f"e = {e}\n")
        f.write(f"c = {c}\n")
    
    print(f"Public key (n, e): ({n}, {e})")
    print(f"Ciphertext: {c}")
        
if __name__ == "__main__":
    encrypt_flag()