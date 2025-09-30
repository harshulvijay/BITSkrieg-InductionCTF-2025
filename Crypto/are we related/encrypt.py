from Crypto.Util.number import getPrime, bytes_to_long
import random

p = getPrime(1024)
q = getPrime(1024)

N = p*q
e1 = getPrime(6)
e2 = getPrime(9)
a = random.randint(1, 1000)
b = random.randint(1000, 2000)

pt = b"XXXXXXXXXXXXXXXXXXXXXX"
m1 = bytes_to_long(pt)
m2 = (a*m1 + b)%N

c1 = pow(m1, e1, N)
c2 = pow(m2, e2, N)

print("N =", N)
print("e1 =", e1)
print("e2 =", e2)
print("a =", a)
print("b =", b)
print("c1 =", c1)
print("c2 =", c2)

