import urllib.request


url = 'http://image.mingdabeta.com/upload/34/12/4d277833fbdef9167bf43b993c4c890d.jpg'
file_name = '4d277833fbdef9167bf43b993c4c890d.jpg'
urllib.request.urlretrieve(url, file_name)

print(urllib.request.urlretrieve(url))
