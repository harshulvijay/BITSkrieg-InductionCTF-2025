from Crypto.Util.number import getPrime, bytes_to_long
from sympy import nextprime

bitlen = 512
p = getPrime(bitlen)
q = p
while abs(p-q) < 696969:
    q = nextprime(q)

N = p * q
e = 65537
pt = b"XXXXXXXXXXXXXXXXXXXX"

pt_long = bytes_to_long(pt)
ct = pow(pt_long, e, N)

print(N)
print(e)
print(ct)
