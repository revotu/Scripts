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


def RemovePunctuation(str_txt):
    new_str = ""
    for ch in str_txt:
        if string.punctuation.find(ch) == -1:
            new_str += ch
    return new_str

def SnippetSeenQuery(raw_snippet, raw_query):
    raw_snippet = raw_snippet.lower()
    raw_snippet = raw_snippet.replace("\n", "")
    raw_snippet = RemovePunctuation(raw_snippet)
    raw_query = raw_query.lower()
    raw_query = RemovePunctuation(raw_query)
    query_words = raw_query.split(" ")
    for i in range(len(query_words) - 1):
        sub_query = "%s %s" % (query_words[i], query_words[i + 1])
        if raw_snippet.find(sub_query) == -1:
            return False
    return True

def IsNotSeenInSearchAPI(raw_query):
    query = urllib.urlencode({'q': raw_query})
    url = 'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    search_results = response.read()
    results = json.loads(search_results)
    data = results['responseData']
    if data is None:
        return "NOTSURE"
    hits = data['results']
    if len(hits) == 0:
        return "NOTSURE"

    for h in hits:
        raw_snippet = utils.StripHtmlTag(h['content'])
        if SnippetSeenQuery(raw_snippet, raw_query):
            return False
    return True

class checkUrlRanking(object):
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

    def is_rank_in_top_100(self, checkUrl):
        raw_query = checkUrl.split('/')[-1].lower().replace('.html','').replace('.htm','').replace('-',' ')
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
            if checkUrl in urlList:
                return urlList.index(checkUrl) + 1
        except:
            logger.error('Exception in check url ranking.')
            with open('google.html', 'w') as fp:
                fp.write(page_source)

        return False

def main():
    rank = checkUrlRanking()
    
    print rank.is_rank_in_top_100("http://www.davidsbridal.com/wedding-dresses/sheath-wedding-dresses")
    print rank.is_rank_in_top_100("http://www.ucenterdress.com/bestcollections/u/unique-sheath-wedding-dresses.html")
    print rank.is_rank_in_top_100("http://www.ucenterdress.com/bestcollections/w/where-to-find-plus-size-prom-dresses.html")

 
    rank.close()


if __name__ == '__main__':
    main()

