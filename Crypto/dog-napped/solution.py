#!/usr/bin/env python3

# Affine cipher parameters
A = 5
B = 8
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
A2I = {c: i for i, c in enumerate(ALPHA)}
I2A = {i: c for i, c in enumerate(ALPHA)}

# Modular inverse of A (5) mod 26 is 21
A_INV = 21  

def affine_decrypt(ciphertext: str, a: int = A, b: int = B) -> str:
    plaintext = []
    for ch in ciphertext.upper():
        if ch.isalpha():
            y = A2I[ch]
            x = (A_INV * (y - b)) % 26
            plaintext.append(I2A[x])
        else:
            plaintext.append(ch)  # keep spaces/punctuation
    return "".join(plaintext)

if __name__ == "__main__":
    enc = input("Enter encrypted name: ").strip()
    dec = affine_decrypt(enc)
    print("Decrypted:", dec)
