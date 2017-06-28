import os
import shutil

def replace_images(imagesPath, rulesPath):
    rules = {}
    with open(rulesPath) as f:
        for line in f:
            old, new = line.strip().split(',')
            rules[old] = new

    for image in os.listdir(imagesPath):
        sn, index, suffix = image.split('.')
        if sn in rules:
            new_name = '{sn}_({index}).{suffix}'.format(sn=rules[sn], index=index, suffix='jpg')
            shutil.move(os.path.join(imagesPath, image), os.path.join(imagesPath, new_name))
        else:
            print 'ERROR: {}'.format(sn)

def main():
    imagesPath = 'E:/task/replace-images-name'
    rulesPath = 'E:/task/rules/rules.csv'
    replace_images(imagesPath, rulesPath)

if __name__ == "__main__":
    main()