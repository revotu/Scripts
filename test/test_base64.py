import base64

with open('4d277833fbdef9167bf43b993c4c890d.jpg', 'rb') as fr, open('test_base64.jpg', 'wb') as fw:
    data = base64.b64encode(fr.read())
    print(type(data))
    fw.write(base64.b64decode(data))