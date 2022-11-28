from pwn import *

def get_coin_indexes(start,end):
    """returns formated line of coin indexes
    IE: b'0 1 2 3...'"""
    return ' '.join([str(x) for x in range(start,end)]).encode()

def check_for_fake_coin(weight):
    """returns true if fake coin in weight"""
    return weight[-2] == '9' #weight[-1] is newline

def find_fake_coin(c,coin_count,tries):
    """weighing coins via bianry search"""
    low, high = 0,coin_count-1
    res = b''
    while high-low > 1:
        mid = (low+high)//2
        indexes = get_coin_indexes(low,mid)
        #print('send: ',indexes)
        c.sendline(indexes)
        res = c.recvS()
        #print('response:',res)
        if check_for_fake_coin(res):
            high = mid
        else:
            low = mid
        tries -= 1
        #print('low:',low,'high:',high,'tries:',tries)

    #print('sending fake coin: ',indexes,tries)
    while tries >= 0:
        c.sendline(str(low).encode())
        tries -= 1
    print(c.recvuntil(b')\n'))




def parse_coin_count_and_tries(raw):
    """parsing N and C; coin_count and tries"""
    coin_count = int(raw.split('N=')[1].split(' ')[0])
    tries = int(raw.split('C=')[1])
    return coin_count,tries



def main():
    c = remote('pwnable.kr',9007)
    #c.interactive()
    c.recv() #the instructions & tutorial
    for i in range(100):
        cc,t = parse_coin_count_and_tries(c.recvS())
        find_fake_coin(c,cc,t)
    c.interactive()

if __name__ == "__main__":
    main()
