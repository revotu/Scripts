#-*- coding: UTF-8 -*-
import os
import MySQLdb
import sys
import shutil

def getSiteImages(site,id):
    conn = MySQLdb.connect('127.0.0.1','root','hacker@die1m','similar_images',charset="utf8")
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    
    if site == "trade":
        cursor.execute('select * from %s where face_classification = %s' % (site,id))
    else:
        cursor.execute('select * from %s where `id` = %s' % (site,id))
    conn.commit()
    
    result = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return result

def main():
    inputFile = '/root/compare.dat'
    destPath = '/root/similarFaces'
    
    similarImages = {}
    
    with open(inputFile) as f:
        for line in f:
            id,classId = line.strip().split(' ')
            if classId not in similarImages:
                similarImages[classId] = []
            similarImages[classId].append(id)
    
    index = 1        
    for classId in similarImages:
        
        trade = getSiteImages("trade",classId)
        
        for image in trade:
            similarPath = os.path.join(destPath,str(index),'trade')
            if not os.path.exists(similarPath):
                os.makedirs(similarPath)
            shutil.copy(image['path'], similarPath)
            shutil.move(os.path.join(similarPath,image['name']), os.path.join(similarPath,image['origin_name']))
        
        for v in similarImages[classId]:
            counterfeit = getSiteImages("counterfeit",v)
            
            for image in counterfeit:
                similarPath = os.path.join(destPath,str(index),'counterfeit')
                if not os.path.exists(similarPath):
                    os.makedirs(similarPath)
                shutil.copy(image['path'], similarPath)
                shutil.move(os.path.join(similarPath,image['name']), os.path.join(similarPath,image['owner']+'-'+image['name']))
        index += 1
    print 'OK'
    

if __name__ == "__main__":
    main()