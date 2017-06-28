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

    cursor.execute('select * from %s where face_number > 0' % (site))
    conn.commit()
    
    result = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return result

def main():
    site = 'trade'
    result = getSiteImages(site)
    all = []
    classifications = []
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
            if image['date'] and sn and image['face_number']:
                FacePathDir = FacePathDir + '/' + sn
                if os.path.isfile(FacePathDir) == True:
                    image['face_encoding'] = pickle.load(open(FacePathDir, "rb"))[0]
                    all.append(image)
    
    while len(all) > 1:
        tmp = all.pop()
        tmpClass = [tmp['id']]
        results = face_recognition.compare_faces([v['face_encoding'] for v in all], tmp['face_encoding'],0.5)
        for k,v in reversed(list(enumerate(results))):
            if v:
                tmpClass.append(all[k]['id'])
                del all[k]
        classifications.append(tmpClass)
        print(len(tmpClass),len(all))
    if len(all) == 1:
        classifications.append([all[0]['id']])
    print(len(classifications))
    with open('trade.dat','w') as f:
        for k,v in enumerate(classifications):
            for d in v:
                f.write('%s\t%s\n' %(d,k+1))
            
    


if __name__ == "__main__":
    main()
