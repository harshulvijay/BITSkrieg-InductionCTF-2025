from itertools import cycle

#example ct
ct = b'j\xcc\xa0]\x80\x97.L\xcc\x87|\xa5\x98$\x13\xcc\xa3Z\xd7\x972O\xc3\xb0\x19\x8c\x8dr|\xdb\xf4]\xbc\x82pF\xfd\xbc\x18\x91\xbc7Q\x92\xb9'

prefix = b'InductionCTF{'

for i in range(6, 14):
    test_key = bytes([x ^ y for x, y in zip(prefix[:i], ct[:i])])

    test_flag = bytes([x ^ y for x, y in zip(ct , cycle(test_key))])
    print(test_flag)
