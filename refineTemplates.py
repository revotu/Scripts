# -*- coding:utf-8 -*-
import os
import re
import shutil
import random
import fnmatch
from bs4 import BeautifulSoup

def replaceMainCSS(templates):
    cssNames = ['main.css','style.css','styles.css','base.css','style.min.css','styles.min.css','base.min.css']
    for template in os.listdir(templates):
        replaceName = 'main.css'
        for css in os.listdir(os.path.join(templates, template, 'css')):
            if css == 'main.css':
                while True:
                    replaceName = random.choice(cssNames)
                    if replaceName == 'main.css' or not os.path.exists(os.path.join(templates, template, 'css', replaceName)):
                        break;
        try:
            if replaceName != 'main.css':
                shutil.move(os.path.join(templates, template, 'css', 'main.css'), os.path.join(templates, template, 'css', replaceName))
                for root, dirnames, filenames in os.walk(os.path.join(templates, template)):
                    for filename in fnmatch.filter(filenames,'*.html'):
                        with open(os.path.join(root, filename)) as f:
                            content = f.read()

                        content = content.replace('main.css', replaceName)

                        with open(os.path.join(root, filename), 'w') as f:
                            f.write(content)

        except NameError:
            pass

        print 'CSS RENAME : ',replaceName

def extractClsssAndId(template):
    classValues = []
    idValues = []

    for css in os.listdir(os.path.join(template, 'css')):
        with open(os.path.join(template, 'css', css)) as f:
            content = f.read()

        classValues.extend(re.findall(r'\.([\w_-]+)',content))
        idValues.extend(re.findall(r'#([\w_-]+)',content))

    return idValues,classValues

def removeClassAndId(templates):
    for template in os.listdir(os.path.join(templates)):
        idValues,classValues = extractClsssAndId(os.path.join(templates, template))
        for root, dirnames, filenames in os.walk(os.path.join(templates, template)):
            for filename in fnmatch.filter(filenames, '*.html'):
                with open(os.path.join(root, filename)) as f:
                    content =  f.read().replace('<%','#####').replace('%>','%%%%%')
                    soup = BeautifulSoup(content, 'lxml')

                    for tag in soup.find_all():
                        idv = tag.get('id')
                        if idv is not None and idv not in idValues:
                            del tag['id']

                        classv = tag.get('class')
                        cv = []
                        if classv is not None:
                            for v in classv:
                               if v and v in classValues:
                                   cv.append(v)

                            if not cv:
                                del tag['class']
                            else:
                                tag['class'] = cv


                content = soup.prettify().encode('utf8').replace('#####','<%').replace('%%%%%','%>')

                with open(os.path.join(root, filename) ,'w') as f:
                    f.write(content)
        print 'COMPLETE : ',template

def refineTemplates(templates):
    replaceMainCSS(templates)
    removeClassAndId(templates)


def main():
    templates = r'D:\work\seo_server\templates'
    print templates
    return
    refineTemplates(templates)

if __name__ == "__main__":
    main()