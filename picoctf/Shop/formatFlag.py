rawFlag = '112 105 99 111 67 84 70 123 98 52 100 95 98 114 111 103 114 97 109 109 101 114 95 98 97 54 98 56 99 100 102 125'
ret = ''
for n in rawFlag.split(' '):
    ret += chr(int(n))
print(ret)
