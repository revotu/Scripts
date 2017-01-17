#-*- coding: UTF-8 -*-
import os
from PIL import Image
import imagehash

def _binary_array_to_hex(arr):
    """
    internal function to make a hex string out of a binary array
    """
    h = 0
    s = []
    for i, v in enumerate(arr.flatten()):
        if v: 
            h += 2**(i % 8)
        if (i % 8) == 7:
            s.append(hex(h)[2:].rjust(2, '0'))
            h = 0
    return "".join(s)

def wHashImages(image):
    w = imagehash.whash(Image.open(image))
    return (_binary_array_to_hex(w.hash),len(w.hash))

def main():
    HashDataPath = '/data/dev-crawler/hashdata'
    allImagesPath = '/data/dev-crawler/database'
    ownerList = [owner for owner in os.listdir(allImagesPath) if os.path.isdir(os.path.join(allImagesPath, owner))]
    for owner in ownerList:
        HashDataOwner = os.path.join(HashDataPath,owner)
        with open(HashDataOwner,'w') as f:
            ownerPath = os.path.join(allImagesPath,owner)
            for file in os.listdir(ownerPath):
                imagePath = os.path.join(ownerPath,file)
                if os.path.isfile(imagePath) == True:
                    (wHash,wHashLength) = wHashImages(imagePath)
                    print '%s\t%s\t%s\t%s\t%s\n' % (owner,file,imagePath,wHash,wHashLength)
                    f.write('%s\t%s\t%s\t%s\t%s\n' % (owner,file,imagePath,wHash,wHashLength))


if __name__ == "__main__":
    main()