import string

LOWERCASE_OFFSET = ord("a")
ALPHABET = string.ascii_lowercase[:16]

def b16_encode(plain):
        enc = ""
        for c in plain:
                binary = "{0:08b}".format(ord(c))
                print(binary)
                enc += ALPHABET[int(binary[:4], 2)]
                print('1',c, enc)
                enc += ALPHABET[int(binary[4:], 2)]
                print('2',c, enc)
        return enc

def shift(c, k):
        t1 = ord(c) - LOWERCASE_OFFSET
        t2 = ord(k) - LOWERCASE_OFFSET
        return ALPHABET[(t1 + t2) % len(ALPHABET)]

flag = "abcdefghijklmnopabccba"
key = "a"
print([k in ALPHABET for k in key])
print([k for k in key])
#assert all([k in ALPHABET for k in key])
#assert len(key) == 1

b16 = b16_encode(flag)
print('aha',b16)
enc = ""
for i, c in enumerate(b16):
        enc += shift(c, key[i % len(key)])
print(enc)
