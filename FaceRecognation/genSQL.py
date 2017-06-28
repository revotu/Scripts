import os

def genSQL(filepath):
    with open(filepath) as f:
        for line in f:
            id, face_number = line.strip().split(' ')
            print 'UPDATE trade SET face_number = {} WHERE id = {};'.format(face_number, id)


def main():
    filepath = 'C:/Users/Administrator/Desktop/trade.face_numbers'
    genSQL(filepath)

if __name__ == '__main__':
    main()