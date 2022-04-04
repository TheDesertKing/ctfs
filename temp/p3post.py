import requests as r
usr = 'alert(0)'
pas = ''
payload = { 'username':usr, 'password':pas}
req = r.post("https://elfmail.hackyholidays.h1ctf.com/login-store", data=payload)
print(req.text)


