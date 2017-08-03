#-*- coding: UTF-8 -*-
import os
import glob
try:
    import cPickle as pickle
except:
    import pickle
import face_recognition
import sys

def FaceEncoding(image):
    image = face_recognition.load_image_file(image)
    face_encoding = face_recognition.face_encodings(image)
    return face_encoding

def main():
    trade = []
    for FacePathDir in glob.iglob('/data/dev-crawler/FaceEncodings/trade/*/*'):
        trade.append(pickle.load(open(FacePathDir, "rb"))[0])

    for image in glob.iglob('/data/dev-crawler/etsy/images/etsy/*/*'):
        name = os.path.basename(image)
        brand = os.path.basename(os.path.dirname(image))
        sn = name.split('_')[0]
        print(name)
        image_face_encoding = FaceEncoding(image)
        if image_face_encoding:
            image_face_encoding = image_face_encoding[0]

            results = face_recognition.compare_faces(trade, image_face_encoding,0.3)
            for k,v in enumerate(results):
                if v:
                    with open('remove.txt', 'a') as f:
                        f.write(brand + '\t'+ sn + '\n')
            sys.stdout.flush()

if __name__ == "__main__":
    main()
