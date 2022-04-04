#!/use/bin/env python3
with open('message.txt','r') as f:
    data = f.read()

out = ''
numbers = data.split(" ")[:-1]
for n in numbers:
    modded = int(n) % 37
    if modded < 26:
        orded = modded + 65
    elif modded < 36:
        orded = modded + 22
    else:
        orded = 95
    chrded = chr(orded)
    out += chrded
print('picoCTF{'+out+'}')
        
