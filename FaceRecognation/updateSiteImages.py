#-*- coding: UTF-8 -*-
import os
from datetime import datetime
import MySQLdb

def getSiteSN(site):
    conn = MySQLdb.connect('45.79.71.23','mdtrade','trade@mingDA123',site,charset="utf8")
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute('SELECT sn FROM products WHERE status = 1')
    conn.commit()
    
    sn = []
    for res in cursor.fetchall():
        sn.append(res['sn'])

    cursor.close()
    conn.close()
    
    return sn

def getLocalSN():
    conn = MySQLdb.connect('127.0.0.1','root','hacker@die1m','similar_images',charset="utf8")
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute('SELECT DISTINCT sn FROM trade WHERE 1')
    conn.commit()
    
    sn = []
    for res in cursor.fetchall():
        sn.append(res['sn'])

    cursor.close()
    conn.close()
    
    return sn

def getSiteImages(sn):
    conn = MySQLdb.connect('127.0.0.1','root','hacker@die1m','image',charset="utf8")
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    
    cursor.execute('SELECT * FROM image WHERE sn IN ("%s")' % ('","'.join(sn)))
    conn.commit()
    
    result = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return result

def updateSiteImages(result):
    conn = MySQLdb.connect('127.0.0.1','root','hacker@die1m','similar_images',charset="utf8")
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    
    for image in result: 
        cursor.execute('INSERT INTO trade (sn,origin_name,name,path,date) VALUES ("%s","%s","%s","%s","%s")' % (image['sn'],image['origin_name'],image['name'],image['path']+'/'+image['name'],datetime.now().date()))
        conn.commit()
    
    cursor.close()
    conn.close()

def diffSiteImages(site):
    sn_total = getSiteSN(site)
    sn_exist = getLocalSN()
    return list(set(sn_total) - set(sn_exist))


def main():
    list = ['junebridals','dorriswedding','ucenterdress']
    for site in list:
        sn = diffSiteImages(site)
#         path = '/data/dev-crawler/scripts/june-sn.txt'
#         sn = []
#         with open(path) as f:
#             sn = [line.strip() for line in f]
        print sn
        result = getSiteImages(sn)
        updateSiteImages(result)

if __name__ == "__main__":
    main()
