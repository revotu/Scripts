import requests

url = 'https://lumendatabase.org/notices/14858169'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
r = requests.get(url, headers=headers)
print r