with open('message.txt','r') as f:
    content = f.read()

numbers = [int(i) for i in content.split(' ')[:-1]]
#print(numbers)

out = ''
for n in numbers:
    inverse = pow(n,-1,41)
    if inverse < 27:
        orded = inverse + 64
    elif inverse < 37:
        orded = inverse + 21
    else:
        orded = 95
    chrded = chr(orded)
    out += chrded
print('picoCTF{'+out+'}')
