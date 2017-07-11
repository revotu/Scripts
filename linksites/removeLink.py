# coding:utf-8
import os
import urllib2

def removeLink(sites):
    remove_links = []
    for site in os.listdir(sites):
        if os.path.isdir(os.path.join(sites, site)):
            if os.path.isfile(os.path.join(sites, site, 'sitemap.txt')):
                with open(os.path.join(sites, site, 'sitemap.txt')) as f:
                    saveURL = []
                    for line in f:
                        URL = line.strip()
                        try:
                            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
                            req = urllib2.Request(URL, headers=headers)
                            response = urllib2.urlopen(req)
                            content = response.read()
                            if 'Wayback Machine' in content:
                                remove_links.append(URL)
                                print 'Remove URL : ', URL, 'Wayback Machine'
                            else:
                                saveURL.append(URL)
                                print 'Save URL : ', URL
                        except Exception, e:
                            #remove_links.append(URL)
                            print 'Exception URL : ', URL, e

                with open(os.path.join(sites, site, 'sitemap.txt'), 'w') as f:
                    f.write('\n'.join(saveURL))

    with open(os.path.join(sites, 'removeLinks.txt'), 'w') as f:
        f.write('\n'.join(remove_links))

def main():
    sites = r'/home/zhangpeng/history'
    removeLink(sites)

if __name__ == "__main__":
    main()