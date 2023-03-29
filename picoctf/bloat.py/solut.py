with open("./bloat.flag.py",'rb') as f:
  content = f.read()
print(content.replace(b'kkk',0x0a.to_bytes(2,'big')))

