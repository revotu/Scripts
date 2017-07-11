import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

browser = webdriver.Chrome('../resources/chromedriver.exe')
browser.get('https://www.google.com/preferences?hl=en&fg=1')
browser.find_element_by_xpath('//div[@id="form-buttons"]/div[contains(@class,"jfk-button-action")]').click()

try:
    WebDriverWait(browser, 3).until(EC.alert_is_present(),
                                    'Timed out waiting for popup to appear.')

    alert = browser.switch_to.alert()
    time.sleep(3)
    alert.accept()
    time.sleep(3)
    print 'alert accepted'
except TimeoutException:
    print 'no alert'

browser.quit()