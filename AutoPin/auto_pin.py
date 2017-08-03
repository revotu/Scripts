import logging
import os
import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from pyvirtualdisplay import Display

logging.basicConfig()
selenium_logger = logging.getLogger(
        'selenium.webdriver.remote.remote_connection')
selenium_logger.setLevel(logging.WARNING)
logger = logging.getLogger('AutoPin')
logger.setLevel(logging.INFO)

class AutoPin(object):
    def __init__(self, lang='en', headless=False):
        # Linux use headless mode
        self.display = None
        if os.name == 'posix' and headless:
            self.display = Display(visible=0, size=(800, 600))
            self.display.start()

        self.WAIT_TIME = 5
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.driver.implicitly_wait(self.WAIT_TIME)
        logger.info('Starting AutoPin...')

    def close(self):
        if self.display != None:
            self.display.stop()
        self.driver.quit()
        logger.info('Goodbye, AutoPin.')

    def AutoPin(self, username, password, pinurl, board):
        try:
            self.driver.get('https://www.pinterest.com/login/?referrer=home_page')
            self.driver.find_element_by_xpath('//form//input[@type="email"]').send_keys(username)
            self.driver.find_element_by_xpath('//form//input[@type="password"]').send_keys(password)
            self.driver.find_element_by_xpath('//form//button').click()

            logger.info('Successfully log in pinterest!')
            time.sleep(3)
        except Exception:
            logger.error('Failed log in pinterest!')
            return

        try:
            self.driver.get(pinurl)
            wait = WebDriverWait(self.driver, self.WAIT_TIME)
            results = wait.until(EC.presence_of_all_elements_located(
                    (By.XPATH, '//dd[@class="prodName"]/a')))
            urlList = [result.get_attribute('href') for result in results]

            if urlList:
                for url in urlList:
                    logger.info('Auto pin url : %s' % url)
                    self.driver.get(url)
                    pinnedImages = []
                    while True:
                        try:
                            currentImage = self.driver.find_element_by_xpath('//div[@id="w-featurePics"]/a').get_attribute('href')
                            if currentImage in pinnedImages:
                                break
                            else:
                                pinnedImages.append(currentImage)
                                logger.info('Auto pin Image : %s' % currentImage)
                            self.driver.find_element_by_xpath('//div[@id="w-featurePics"]/div').click()
                            if len(self.driver.window_handles) > 1:
                                self.driver.switch_to.window(self.driver.window_handles[-1])
                                self.driver.find_element_by_xpath('//div[@role="button"]//p[contains(text(), "%s")]' % board).click()
                                time.sleep(2)
                                self.driver.close()
                                self.driver.switch_to.window(self.driver.window_handles[0])
                            self.driver.find_element_by_xpath('//div[@id="prodthumbnails"]/div/a[1]').click()
                            time.sleep(2)
                        except Exception:
                            logger.error('Failed auto pin!')
                            break
        except Exception:
            logger.error('Failed auto pin!')
            return

def main():
    username = 'support@junebridals.com'
    password = 'mingDA@1509'
    pinurl = 'https://www.junebridals.com/plus-size-wedding-dresses.html'
    board = 'Plus Size Wedding Dresses'

    pin = AutoPin()
    pin.AutoPin(username, password, pinurl, board)
    pin.close()

if __name__ == '__main__':
    main()