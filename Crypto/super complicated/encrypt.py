from Crypto.Util.number import getPrime, bytes_to_long

p = getPrime(1024)
q = getPrime(1024)

N = p*q
e = 65537

pt = b"InductionCTF{571ck_70_7h3_b451c5}"
pt_long = bytes_to_long(pt)

ct = pow(pt_long, e, N)

print(p)
print(e)
print(ct)

