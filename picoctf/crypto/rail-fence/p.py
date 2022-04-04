with open('message.txt','r') as f:
    content = f.read()

t = 'WECRUO ERDSOEERNTNE AIVDAC'
print(content)
r =[list(reversed(list(rail))) for rail in content.split(' ')]
print(r)
i = 0
j = 0
dir = 'up'
out = []
while j < 100:
    if r[i]:
        out.append(r[i].pop())
    if i == 3 and dir == 'up': dir = 'down'
    if i == 0 and dir == 'down': dir = 'up'
    if dir == 'up': i += 1
    if dir == 'down': i -= 1
    j += 1
#out.reverse()
print(''.join(out))
