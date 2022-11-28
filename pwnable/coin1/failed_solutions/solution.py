from pwn import *

def get_coin_indexes(start,end):
    """returns formated line of coin indexes
    IE: b'0 1 2 3...'"""
    return ' '.join([str(x) for x in range(start,end)]).encode()


def find_fake_coin(c,coin_count,tries):
    """weighing coins via bianry search"""
    offset = 0
    i = 2
    coin_indexes = get_coin_indexes(offset,offset+coin_count//i)
    while coin_indexes.count(b' ') != 0:
        if coin_indexes.count(b' ') == 2:
            for index in coin_indexes.split(b' '):
                print('sent:',index)
                c.sendline(index)
                if c.recvS() == '9':
                    offset = index
                    break
        print('sent:',coin_indexes)
        c.sendline(coin_indexes)
        weight = c.recvS()
        print('recv:',weight)
        if int(weight.split('\n')[0]) % 10 == 0:
            offset += coin_count//i
        i *= 2
        tries -= 1
        coin_indexes = get_coin_indexes(offset,offset+coin_count//i)
    while tries > 0:
        print('fake coin:', offset)
        c.sendline(str(offset).encode())
        tries -= 1
    return offset


def parse_coin_count_and_tries(raw):
    """parsing N and C; coin_count and tries"""
    coin_count = int(raw.split('N=')[1].split(' ')[0])
    tries = int(raw.split('C=')[1])
    return coin_count,tries



def main():
    c = remote('pwnable.kr',9007)
    #c.interactive()
    c.recv() #the instructions & tutorial
    cc,t = parse_coin_count_and_tries(c.recvS())
    print("coin_count:",cc,"\ntries:",t)
    find_fake_coin(c,cc,t)
    print(c.recv())
    c.interactive()

if __name__ == "__main__":
    main()
