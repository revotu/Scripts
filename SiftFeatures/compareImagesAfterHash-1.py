#-*- coding: UTF-8 -*-
import cv2
import os
import sys
import datetime
import json
import shutil
import MySQLdb
import numpy as np
import cPickle as pickle

def compareImages(image1Desc,image2Desc):
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    matches = bf.match(image1Desc, image2Desc)
    matches = sorted(matches, key = lambda x:x.distance)
    if matches[0].distance <= 20.0 and matches[int(len(matches)*0.20)].distance <= 100.0:
        return True
    return False

def getSiteImages(site,sn = [],owner = None):
    conn = MySQLdb.connect('127.0.0.1','root','hacker@die1m','similar_images',charset="utf8")
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    if sn:
        cursor.execute('SELECT * FROM %s WHERE sn IN ("%s")' % (site,'","'.join(sn)))
    elif owner:
        cursor.execute('SELECT * FROM %s WHERE owner = "%s"' % (site,owner))
    else:
        cursor.execute('select * from %s where 1' % (site))
    conn.commit()
    
    result = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return result

def main():
    similarImagesPath = '/data2/fingerprint/similar-images/2017-03-13-doriswedding'
    sitePath = '/data2/fingerprint/phash-doriswedding'
    resultFile = '/data2/fingerprint/similarID/doriswedding-job1'
    jobPath = '/data/dev-crawler/scripts/phash-doriswedding-sn-job/job1'
    site = 'doriswedding'
    result1 = getSiteImages('counterfeit')
    result2 = getSiteImages(site)
    counterfeit = {}
    tradesite = {}
    jobSN = []
    
    for v in result1:
        counterfeit[str(v['id'])] = '/data2/fingerprint/counterfeit/%s/%s/%s' % (v['owner'],v['date'],v['name'].split('.')[0])
    for s in result2:
        tradesite[str(s['id'])] = '/data2/fingerprint/%s/%s/%s' % (site,s['date'],s['origin_name'].split('.')[0])
    
    with open(jobPath) as f:
        for line in f:
           jobSN.append(line.strip())
    
    for file in os.listdir(sitePath):
        if os.path.isfile(os.path.join(sitePath,file)) == True and file in jobSN:
            if file in tradesite:
                if os.path.isfile(tradesite[file]):
                    image1Desc = pickle.load(open(tradesite[file],"rb"))
                else:
                    continue
                image2DescList = {}
                with open(os.path.join(sitePath,file)) as f:
                    for line in f:
                        if os.path.isfile(counterfeit[line.strip()]):
                            image2DescList[line.strip()] = pickle.load(open(counterfeit[line.strip()],"rb"))
            else:
                continue
    
    
            for image2DescID in image2DescList:
                image2Desc = image2DescList[image2DescID]
                if image1Desc is not None and image2Desc is not None:
                    status= compareImages(image1Desc,image2Desc)
                    if status:
                        with open(resultFile,'a') as f:
                            f.write(file + ';' + image2DescID +'\n')
            print file
            sys.stdout.flush()

if __name__ == "__main__":
    main()
