# coding: utf-8

import codecs

# errors file empty
def test_encoding(path):
    with open(path) as input, open(path, 'w') as output:
        content = input.read()
        content = content.replace('<title>','<test title>')
        output.write(content)

def test_encoding_2(path):
    with open(path) as f:
        content = f.read()

    content = content.replace('<title>','<test title>')

    with open(path, 'w') as f:
        f.write(content)

def test_codecs_encoding(path):
    with codecs.open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    content = content.replace('<title>', '<title 無料出会い,出会い無料,出会い系サイト>'.decode('utf-8', errors='replace'))

    with codecs.open(path, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(content)

def main():
    path = r'C:\Users\Administrator\Desktop\index.html'
    test_codecs_encoding(path)


if __name__ == "__main__":
    main()
