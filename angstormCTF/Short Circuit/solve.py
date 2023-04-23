import requests


def reverseSwap(chunk_list):
    """ The site uses a function `swap` to re-order
    30 char chunks around, this funciton does the
    reverse swaping."""

    temp = chunk_list[0]
    chunk_list[0] = chunk_list[1]
    chunk_list[1] = chunk_list[3]
    chunk_list[3] = temp

    return ''.join(chunk_list)

def get_scrambled_password():
    URL = "https://shortcircuit.web.actf.co/"
    r = requests.get(URL)
    html_lines = r.text.split("\n")

    # Use some parsing to find the scrambled password
    scrambled_password = [line.split('"')[3] for line in html_lines if "swap(chunk(document.forms[0].password.value, 30)" in line][0]

    return scrambled_password


def chunk_password(password):
    ret = []
    i = 0
    while i < len(password):
        ret.append(password[i:i+30])
        i+=30

    return ret


def main():
    print(reverseSwap(chunk_password(get_scrambled_password())))




if __name__ == "__main__":
    main()
