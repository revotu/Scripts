import os
import re
import requests

def get_status_code(url):
    try:
        r = requests.head(url)
        return r.status_code
    except StandardError:
        return None

def test_re():
    print re.findall(r'\.([\w-]+)(?![;)])','-webkit-box-shadow: 0 0 2px 0 rgba(31, 31, 31, 0.07);')

def main():
    # print(id(a))
    # print(id(b))
    # print a ** 3
    #test_re()

    nums = [1, 2, 3]
    print nums




if __name__ == "__main__":
    main()