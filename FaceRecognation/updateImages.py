#-*- coding: UTF-8 -*-
import os
import MySQLdb

def getSiteImages(site,owner = None):
    conn = MySQLdb.connect('127.0.0.1','root','hacker@die1m','similar_images',charset="utf8")
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    
    if owner:
        cursor.execute('select * from %s where owner = "%s"' % (site,owner))
    else:
        cursor.execute('select * from %s where 1' % (site))
    conn.commit()
    
    result = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return result

def updateSiteImages(owner,diffImages):
    conn = MySQLdb.connect('127.0.0.1','root','hacker@die1m','similar_images',charset="utf8")
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    
    for image in diffImages:
        path = '/data/dev-crawler/avarsha/images/' + owner + '/' + image + '.jpg'
        if os.path.isfile(path) == True:
            cursor.execute('INSERT INTO counterfeit(owner,name,path,date) VALUES ("%s","%s","%s","%s") ' % (owner,image + '.jpg', path,'2017-05-26'))
            conn.commit()
    
    cursor.close()
    conn.close()

def getLocalImages(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path,file)) == True:
            dbImages = []
            localImages = []
            result = getSiteImages('counterfeit',file)
            for image in result:
                dbImages.append(image['name'].split('.')[0])
            with open(os.path.join(path,file)) as f:
                localImages = [line.strip() for line in f]
                
            diffImages = list(set(localImages) - set(dbImages))
            if diffImages:
                print file,diffImages
                updateSiteImages(file,diffImages)

def main():
    path = '/data/dev-crawler/database'
    getLocalImages(path)

if __name__ == "__main__":
    main()
