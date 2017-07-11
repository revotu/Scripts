import time
from selenium import webdriver

PROXY = '219.153.76.77:8080'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server={0}'.format(PROXY))
driver = webdriver.Chrome(executable_path='../resources/chromedriver.exe', chrome_options=chrome_options)
driver.get('http://httpbin.org/ip')
print(driver.page_source)

time.sleep(15)
driver.quit()