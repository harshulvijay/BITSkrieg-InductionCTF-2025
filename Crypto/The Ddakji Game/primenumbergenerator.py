from Crypto.Util import number
import secrets

# generate a random 1536-bit prime
p = number.getPrime(1536, randfunc=secrets.token_bytes)
q = number.getPrime(1536, randfunc=secrets.token_bytes)
n = p*q
print("p = ", p )
print("q = ", q )
print("n = ", n )