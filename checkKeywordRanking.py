import urllib
import urllib2
import logging
import md5
import os
import json
import string
import time
import traceback
import utils
from lxml import html
from lxml.html import clean

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pyvirtualdisplay import Display

from openpyxl import load_workbook

logging.basicConfig()
selenium_logger = logging.getLogger(
    'selenium.webdriver.remote.remote_connection')
selenium_logger.setLevel(logging.WARNING)
logger = logging.getLogger('checkUrlRanking')
logger.setLevel(logging.INFO)

class checkKeywordRanking(object):
    def __init__(self, lang='en', headless=False):
        # Linux use headless mode
        self.display = None
        if os.name == 'posix' and headless:
            self.display = Display(visible=0, size=(800, 600))
            self.display.start()

        self.WAIT_TIME = 12
        options = webdriver.ChromeOptions()
        options.add_argument('--lang=%s' % lang)
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.implicitly_wait(self.WAIT_TIME)
        logger.info('Log in to google successfully.')
        
        
        self.driver.get('https://www.google.com/')
        self.driver.implicitly_wait(self.WAIT_TIME)
        self.driver.find_element_by_link_text('Settings').click()
        self.driver.find_element_by_link_text('Search settings').click()
        self.driver.implicitly_wait(self.WAIT_TIME)
        self.driver.find_element_by_css_selector('#instant-radio div[data-value="2"]').click()
        self.driver.find_element_by_id('result_slider').click()
        self.driver.find_element_by_id('result_slider').click()
        self.driver.find_element_by_id('result_slider').click()
        self.driver.find_element_by_id('result_slider').click()
        self.driver.find_element_by_id('result_slider').click()

        self.driver.find_element_by_css_selector('#form-buttons > :first-child').click()
        self.driver.implicitly_wait(self.WAIT_TIME)
        alert = self.driver.switch_to_alert()
        alert.accept()
        

    def close(self):
        if self.display != None:
            self.display.stop()
        self.driver.quit()
        logger.info('Goodbye, Google.')

    def siteKeywordRank(self, keyword, site):
        raw_query = keyword
        query = urllib.urlencode({'q': raw_query})
        url = 'https://www.google.com/?gws_rd=ssl#%s' % (query)

        try:
            self.driver.get(url)
            time.sleep(15)
            wait = WebDriverWait(self.driver, self.WAIT_TIME)
            hrefs = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'h3.r > a')))
            urlList = [href.get_attribute('href') for href in hrefs]
        except:
            logger.error('Wait timeout, google again.')
            return False

        page_source = self.driver.page_source.encode('utf-8')

        try:
            for index,url in enumerate(urlList):
                if site in url:
                    return index + 1
        except:
            logger.error('Exception in check url ranking.')
            with open('google.html', 'w') as fp:
                fp.write(page_source)

        return False

def main():
    rank = checkKeywordRanking(headless=True)
    keywordList = ['cheap wedding dresses','cheap prom dresses','cheap bridesmaid dresses']
    siteList = ['www.junebridals.com','www.doriswedding.com','www.ucenterdress.com']
    
    for keyword in keywordList:
        for site in siteList:
            result =  rank.siteKeywordRank(keyword, site)
            if result == False:
                result = '100+'
            with open('keywordRank','a') as f:
                f.write('%s\t%s\t%s\t%s\n' % (time.strftime("%Y-%m-%d"),keyword,site,result))
                

 
    rank.close()


if __name__ == '__main__':
    main()

