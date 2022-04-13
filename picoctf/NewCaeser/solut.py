import string

LOWERCASE_OFFSET = ord('a')
ALPHABET = string.ascii_lowercase[:16]
FLAG = 'mlnklfnknljflfmhjimkmhjhmljhjomhmmjkjpmmjmjkjpjojgjmjpjojojnjojmmkmlmijimhjmmj'

def b16_decode(enc):
    """reverse b16_encode
    """
    decod = ''
    i = 0
    while i < len(enc):
        a,b = enc[i:i+2]
        aBinary = "{0:04b}".format((ALPHABET.index(a)))
        bBinary = "{0:04b}".format((ALPHABET.index(b)))
        decod += chr(int(aBinary + bBinary,2))
        i += 2
    return decod

def unshift(char,key):
    """reverse shift() by turning + to -
    causing a reverse shift"""
    t1 = ord(char) - LOWERCASE_OFFSET
    t2 = ord(key) - LOWERCASE_OFFSET
    return ALPHABET[(t1 + t2) % len(ALPHABET)]

def main():

    unshifted = ['' for i in range(16)]
    for l in ALPHABET:
        for c in FLAG:
            unshifted[ALPHABET.index(l)]  += unshift(c,l)

    for u in unshifted:
        print(b16_decode(u))

if __name__ == '__main__':
    main()
