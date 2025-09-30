#!/usr/bin/env python3

import math
from Crypto.Util.number import long_to_bytes

def fermat_factorization(n):
    a = math.isqrt(n)
    if a * a == n:
        return a, a
    
    a += 1
    while True:
        b_squared = a * a - n
        b = math.isqrt(b_squared)
        
        if b * b == b_squared:
            p = a - b
            q = a + b
            return p, q
        
        a += 1
        if a > n:
            return None, None

def mod_inverse(a, m):
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        return None
    return (x % m + m) % m

def solve_rsa_challenge():    
    values = {}
    with open('values.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            key, value = line.split(' = ')
            values[key] = int(value)
    
    n = values['n']
    e = values['e']
    c = values['c']
    
    p, q = fermat_factorization(n)
    
    if p and q:
        print(f"p = {p}")
        print(f"q = {q}")
        
        phi = (p - 1) * (q - 1)
        d = mod_inverse(e, phi)
        
        if d:            
            m = pow(c, d, n)
            flag = long_to_bytes(m).decode()
            print(f"\nJhanda: {flag}")
            return flag

if __name__ == "__main__":
    solve_rsa_challenge()