import logging
import os
import re
import time
import random
import urllib2

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from pyvirtualdisplay import Display

import MySQLdb

logging.basicConfig()
selenium_logger = logging.getLogger(
    'selenium.webdriver.remote.remote_connection')
selenium_logger.setLevel(logging.WARNING)
logger = logging.getLogger('checkDomainIndexes')
logger.setLevel(logging.INFO)


def searchIndexes():
    indexes = [
        'http://www.ladyfashions.net/introduce.html',
        'http://www.marriagemode.com/guide.html',
        'http://www.promdresscodes.com/customized.html'
    ]
    searchLinks = {}
    for index in indexes:
        content = urllib2.urlopen(index).read()
        links = re.findall(r'<a href=["\'](.+?)["\']', content)
        for link in links:
            url = index[:index.rfind('/')] + '/' + link
            html = urllib2.urlopen(url).read()
            seo_link = re.findall(r'<a href=["\'](.+?)["\']', html)
            if seo_link:
                searchLinks[seo_link[0]] = url
    return searchLinks

def domainIndexesFromDB():
    conn = MySQLdb.connect('45.79.71.23','mdtrade','trade@mingDA123','servers',charset="utf8")
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute('SELECT CONCAT("http://",prefix, site_name,"/",new_index,".html") as link FROM linksite WHERE `indexable` = 1 AND `status` = 1 AND `type` = "TRADE";')
    conn.commit()
    links = [result['link'] for result in cursor.fetchall()]

    cursor.close()
    conn.close()
    
    return links


class checkDomainIndexes(object):
    def __init__(self, lang='en', headless=False):
        # Linux use headless mode
        self.display = None
        if os.name == 'posix' and headless:
            self.display = Display(visible=0, size=(800, 600))
            self.display.start()

        self.WAIT_TIME = 5
        self.driver = webdriver.Chrome('./resources/chromedriver.exe')
        self.driver.implicitly_wait(self.WAIT_TIME)
        logger.info('Log in to google successfully.')

    def close(self):
        if self.display != None:
            self.display.stop()
        self.driver.quit()
        logger.info('Goodbye, Google.')

    def domainIndexStatus(self, indexLink):
        url = 'https://www.google.com/'

        try:
            self.driver.get(url)
            self.driver.find_element(By.NAME, 'q').send_keys(indexLink)
            self.driver.find_element(By.NAME, 'q').submit()

            time.sleep(random.randint(1,3))
            wait = WebDriverWait(self.driver, self.WAIT_TIME)
            results = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'h3.r > a')))
            urlList = [result.get_attribute('href') for result in results]

            if urlList and indexLink in urlList:
                return True
        except TimeoutException:
            if 'google.com/sorry/index' in self.driver.current_url:
                raise Exception('Sorry, Recaptcha Appears!')
            return False

        return False

def main():
    indexInstance = checkDomainIndexes()
    searchLinks = searchIndexes()

    indexLinks = domainIndexesFromDB()
    for indexLink in indexLinks:
        status = indexInstance.domainIndexStatus(indexLink)
        with open('index-status.txt', 'a') as f:
            if indexLink in searchLinks:
                f.write('{}\t{}\t{}\t{}\n'.format(indexLink.split('/')[-2], status, True, searchLinks[indexLink]))
            else:
                f.write('{}\t{}\t{}\n'.format(indexLink.split('/')[-2], status, False))

    indexInstance.close()


if __name__ == '__main__':
    main()

