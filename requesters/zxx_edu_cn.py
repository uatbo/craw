import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver as sdriver
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import webdriver as swdriver # 导入 selenium-wire

class zxx_edu_cn_request():
    def __init__(self, driverfile_path):
        self.url = "https://www.zxx.edu.cn/syncClassroom"
        self.driverfile_path = driverfile_path
        pass

    # 获取m3u8文件的下载链接
    def get_m3u8_url(self):
        options = swdriver.EdgeOptions()
        options.add_argument('--proxy-server=127.0.0.1:8080')  # 设置代理服务器
        driver = swdriver.Edge(executable_path=self.driverfile_path)

    # 获取每个视频页面的url
    def get_video_url(self):
        driver = sdriver.Edge()
        driver.get(self.url)
        print(driver.current_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[3]/div[4]/div[2]/div[1]/div/div[2]/div/div[5]/div[2]/label[2]')))
        # button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-search')))
        option_area = driver.find_element(By.XPATH, "/html/body/div/div/div/div[3]/div[4]/div[2]/div[1]/div/div[2]/div")
        option_elements = option_area.find_elements(By.CLASS_NAME, "tagSelect-module_tag-level-wrap_yPDhC")
        for i in range(len(option_elements)):
            # 查找学校区域
            school_area = option_elements[i].find_element(By.CLASS_NAME, "fish-radio-group fish-radio-group-outline tagSelect-module_level-tag_XZcnH")
            # 查找所有学校元素
            school_elements = school_area.find_elements(By.TAG_NAME, "lable")
            # 查找并点击小学标签
            for school in school_elements:
                if school.text == "高中":
                    school.click()
                    break

            print("done")

if __name__ == "__main__":
    driverfile_path = "D:/Files/Projects/msedgedriver.exe"
    request = zxx_edu_cn_request(driverfile_path=driverfile_path)
    request.get_video_url()
