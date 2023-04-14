with open('level3.hash.bin', 'rb') as rf:
    content = rf.read().decode('latin-1')
with open('formattedHash','w') as wf:
    wf.write(content)
