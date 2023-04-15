import time

from selenium import  webdriver as driver


driver = driver.Edge()
url = "https://www.zxx.edu.cn/syncClassroom"


driver.get(url)
time.sleep(5)
driver.execute_script("window.scrollBy(0, -500);")
time.sleep(1000)
