from pwn import *


fifth = 0x6c5cec8
last = 0x6c5cec8 + 4

payload = p32(fifth)*4+p32(last)

s = ssh('col','pwnable.kr',2222,'guest')
p = s.process(['col',payload],'./col')
print("flag:\t"+p.recv().decode())
