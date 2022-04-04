#import json

with open('text.txt', 'r') as file:
    lines = file.readlines()
#with open('out1.txt', 'w') as out:
#    for line in lines:
#        counter = {'a':0,'m':0,'1':0,'2':0,'3':0,'sum':0}
#        for letter in line:
#            if letter == '\n':
#                continue
#            counter[letter] += 1
#            if letter in ['1','2','3']:
#                counter['sum'] += int(letter)
#        out.write(json.dumps(counter)+'\n')
        
with open('out2.txt', 'w') as out:
    for line in lines:
        counter = {'a':0,'m':0,'1':0,'2':0,'3':0,'sum':0}
        for letter in line:
            if letter == '\n':
                continue
            counter[letter] += 1
            if letter in ['1','2','3']:
                counter['sum'] += int(letter)
        out.write(str(counter['sum'])+str(counter['a'])+str(counter['m'])+'\n')
