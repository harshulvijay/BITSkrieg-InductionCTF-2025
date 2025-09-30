import os
import random
from itertools import cycle

flag = b'InductionCTF{c0ngr4tulat1on5_y0u_a7e_x0r_pr0}'

def main():
    print("------welcome to varxor------")
    key_length = random.randint(6, 13)
    key = os.urandom(key_length)
    ciphertext = bytes([x ^ y for x, y in zip(flag, cycle(key))])
    print(f"here is your ciphertext : {ciphertext}")
    print("-------------bye-------------")
    exit(0)

if __name__ == "__main__":
    main()
