from itertools import product
from hashlib import sha256

#round 1 can be done easily by using https://crackstation.net/

#round 2
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
prexif = "My name is "
suffix = " and I am the admin"
hash = "b095977d3b88a6a905b8048a4b1147e545602f44402f2eb9652c42f315f585a9"

#name doesnt start with caps btw
#brute should be sub 2 hours
for name in product(charset, repeat=5):
    test_name = ''.join(name)
    test_string = prexif + test_name + suffix

    if sha256(test_string.encode()).hexdigest() == hash:
        print(test_string)
        break

#round 3, either use hashclash or just surf the web
#https://crypto.stackexchange.com/questions/1434/are-there-two-known-strings-which-have-the-same-md5-hash-value