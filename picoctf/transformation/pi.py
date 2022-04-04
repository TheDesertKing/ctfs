nums = []
with open('enc') as f:
    #''.join([chr((ord(flag[i]) << 8) + ord(flag[i+1])) for i in range(0, len(flag),2)])
    line = f.readline()
    for letter in line:
        nums.append(str(ord(letter)) + ' ')
    letters = ''
    for i in nums:
        i = int(i)
        letters += chr(i >> 8)
        letters += chr(i - ((i >> 8) << 8))


    

print(letters)
