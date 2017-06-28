#-*- coding: UTF-8 -*-
import os
import MySQLdb
try:
   import cPickle as pickle
except:
   import pickle
import face_recognition
import sys

def FaceEncoding(image):
    image = face_recognition.load_image_file(image)
    face_encoding = face_recognition.face_encodings(image)
    return len(face_encoding),face_encoding


def getSiteImages(site):
    conn = MySQLdb.connect('127.0.0.1','root','hacker@die1m','similar_images',charset="utf8")
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    #cursor.execute('select * from %s where 1' % (site))
    cursor.execute('select * from %s where `date` = "2017-06-26"' % (site))
    conn.commit()
    
    result = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return result

def main():
    site = 'trade'
    result = getSiteImages(site)
    for image in result:
        if image['path']:
            if 'owner' in image:
                FacePathDir = '/data/dev-crawler/FaceEncodings/%s/%s/%s' % (site,image['owner'],image['date'])
            else:
                FacePathDir = '/data/dev-crawler/FaceEncodings/%s/%s' % (site,image['date'])
            if 'origin_name' in image:
                sn = image['origin_name'].split('.')[0]
            else:
                sn = image['name'].split('.')[0]
            if image['date'] and sn:
                if not os.path.exists(FacePathDir):
                    os.makedirs(FacePathDir)
                FacePathDir = FacePathDir + '/' + sn
                if os.path.isfile(FacePathDir) == True:
                    continue
                face_number,face_encoding = FaceEncoding(image['path'])
                if face_number > 0  and face_encoding is not None:
                    pickle.dump(face_encoding, open(FacePathDir, "wb"))
                print (image['id'],face_number)
                sys.stdout.flush()

if __name__ == "__main__":
    main()
