from hashlib import sha256, md5


flag = "InductionCTF{u_shall_hash_and_you_shall_pass}"

print("--------round 1--------")
password = input("enter your password : ")
if sha256(password.encode()).hexdigest() != '1c8bfe8f801d79745c4631d09fff36c82aa37fc4cce4fc946683d7b336b63032':
    print("you shall not pass")
    exit(0)


print("--------round 2--------")
secret = input("enter the secret phrase : ")
if not secret.startswith("My name is ") or not secret.endswith(" and I am the admin") or len(secret) != 35:
    print("you shall not pass")
    exit(0)

if sha256(secret.encode()).hexdigest() != "b095977d3b88a6a905b8048a4b1147e545602f44402f2eb9652c42f315f585a9":
    print("you shall not pass")
    exit(0)

print("--------round 3--------")
key_1 = input("enter your first key (in hex) : ")
key_2 = input("enter your second key (in hex) : ")

try:
    key_1 = bytes.fromhex(key_1)
    key_2 = bytes.fromhex(key_2)
except ValueError as e:
    print("Invalid hex input")
    exit(0)


if key_1 == key_2:                      
    print("you shall not pass")
    exit(0)

hash1 = md5(key_1).hexdigest()
hash2 = md5(key_2).hexdigest()

if hash1 == hash2:
    print(f"Well done! Here is your reward : {flag}")
else:
    print("you shall not pass")
    exit(0)