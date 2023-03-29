from pwn import *
import time
###
# Find the flag length
# Decrypt the flag
###
SERVER = ("localhost", 10101)

GREETS = [
        "Herzlich willkommen! Der Schlüssel ist {0}, und die Flagge lautet {1}.",
        "Bienvenue! Le clé est {0}, et le drapeau est {1}.",
        "Hartelĳk welkom! De sleutel is {0}, en de vlag luidt {1}.",
        "ようこそ！鍵は{0}、旗は{1}です。",
        "歡迎！鑰匙是{0}，旗幟是{1}。",
        "Witamy! Niestety nie mówię po polsku...",
        ]


def getData():
        R = remote(*SERVER)
        data = R.recv()
        R.close()
        return data


def getEmptyGreetsLengths():
        return [len(x)-6 for x in GREETS[:-1]].append(len(GREETS[-1]))
        # Minus 6 cause I want the length of the greet 
        # without the "{n}" which appears twice.
        # The last greet doesn't have the flag and key in it.


def getGreetsPartsLength():
        """ Returns the amount of chars in between
        the key and the flag parts of the formatted string:
        [[4,5,2]...]
        [`abc {0} abcd {1} e`,...]
        """
        lengths = []
        for g in GREETS[:-1]:
                formatted = g.format("AAAA","BBBB").encode()
                start = formatted.split(b"AAAA")[0]
                middle = formatted.split(b"AAAA")[1].split(b"BBBB")[0]
                end = formatted.split(b"BBBB")[1]
                lengths.append([start,middle,end])
                #print(f"whole:{len(formatted)}\n \
                #      start:{len(start)}\n \
                #      middle:{len(middle)}\n \
                #      end:{len(end)}\n ")


def getFlagLength():
        dataList = []
        for i in range(100):
                dataList.append(getData())
                time.sleep(1)
        dataList.sort(len)
        lengthsSet = set([len(x) for x in dataList].sort())
        print(lengthsSet)


def main():
        getFlagLength()


if __name__ == "__main__":
        main()
