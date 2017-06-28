#-*- coding: UTF-8 -*-
import os
import MySQLdb
try:
   import cPickle as pickle
except:
   import pickle
import face_recognition
import sys

def getFaceEncodings(site,result):
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
    return result

def getSiteImages(site):
    conn = MySQLdb.connect('127.0.0.1','root','hacker@die1m','similar_images',charset="utf8")
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    if site == 'trade':
        cursor.execute('select * from %s where face_number > 0 and `date` = "2017-06-26"' % (site))
        #cursor.execute('select * from %s where face_classification > 0 GROUP BY `face_classification`' % (site))
    else:
        cursor.execute('select * from %s where face_number > 0' % (site))
    conn.commit()
    
    result = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return result

def main():
    trade = getSiteImages('trade')
    counterfeit = getSiteImages('counterfeit')

    trade = getFaceEncodings('trade',trade)
    counterfeit = getFaceEncodings('counterfeit',counterfeit)

    index = 1
    for image in trade:
        sys.stdout.flush()
        results = face_recognition.compare_faces([v['face_encoding'] for v in counterfeit], image['face_encoding'],0.3)
        for k,v in enumerate(results):
            if v:
                #print(counterfeit[k]['id'],image['face_classification'])
                print(counterfeit[k]['id'],image['id'])
        
        index += 1     
    

if __name__ == "__main__":
    main()
