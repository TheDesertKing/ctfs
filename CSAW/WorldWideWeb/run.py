# coding: utf-8
def run(count):
    link = 'stuff'
    for i in range(count):
        res = s.get(url+link)
        try:
            link = res.text.split('"')[-2][1:]
        except:
            print(i)
            print(res.text)
            break
    print(s.cookies)
    
