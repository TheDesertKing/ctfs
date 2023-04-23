import requests
import concurrent.futures

def main():

    find_flag()


def get_res_text(subdir):
    URL = "https://directory.web.actf.co/"
    resp = requests.get(url=URL+str(subdir)+".html")
    return resp.text,subdir


def find_flag():
    subdir = 1
    with concurrent.futures.ThreadPoolExecutor() as executor:

        futures = []

        for subdir in range(1,200):
            futures.append(executor.submit(get_res_text,subdir))

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if "your flag is in another file" not in result[0]:
                print("FLAG: ",result)
            print(result[1])


if __name__ == "__main__":
    main()

    #slow solution:
#    URL = "https://directory.web.actf.co/"
#    subdir = 0
#    while subdir < 5000:
#        res = requests.get(URL+str(subdir)+".html").text
#        print(res)
#        if "your flag is in another file" not in res:
#            print(res)
#            break
#        subdir += 1
