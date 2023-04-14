from hashlib import sha256
hash = sha256(b"PRITCHARD").hexdigest()
hashIndex = [4,5,3,6,2,7,1,8]
ret = ''

for num in hashIndex:
    ret += hash[num]

key = "picoCTF{1n_7h3_|<3y_of_" + ret + "}"

print(f"the solution is {key}")
