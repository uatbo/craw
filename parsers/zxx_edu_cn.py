import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver as sdriver
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import webdriver as swdriver # 导入 selenium-wire

class zxx_edu_cn_parser():
    def __init__(self, driverfile_path):
        self.url = "https://www.zxx.edu.cn/syncClassroom"
        self.driverfile_path = driverfile_path
        self.data = {
            "grade": [],
            "semester": [],
            "category": [],
            "version": [],
            "executor": [],
            "chapter": [],
            "section": [],
            "name": [],
            "content": []
        }
        self.category = 5
        self.executor = "段斌"


    # 获取m3u8文件的下载链接
    def get_m3u8_url(self, url):
        options = swdriver.EdgeOptions()
        options.add_argument('--proxy-server=127.0.0.1:8080')  # 设置代理服务器
        wire_driver = swdriver.Edge(executable_path=self.driverfile_path)

        m3u8_url = ""
        while(len(m3u8_url) == 0):
            wire_driver.get(url)
            WebDriverWait(wire_driver, 100).until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div/div/div/div[3]/div[4]/div/div[2]/div[1]/div[2]/div[1]/div/div[2]/div/div/button')))

            # 查看网络请求
            for request in wire_driver.requests:
                if re.search("m3u8$", request.url):
                    m3u8_url = request.url

        # 关闭浏览器
        wire_driver.quit()

        return m3u8_url


    # 解析视频列表
    def parse_video_list_1(self, info):
        time.sleep(1)
        # 解析目录区域
        contents_area = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div/div/div/div/div[3]/div[2]/div[3]/div/div/div")))

        # 预处理，将所有的标签全部关闭
        contents = contents_area.find_elements(By.XPATH, "./*")
        contents[1].click()
        time.sleep(0.5)
        contents = contents_area.find_elements(By.XPATH, "./*")
        contents[0].click()
        time.sleep(0.5)

        # 逐层打开
        contents = contents_area.find_elements(By.XPATH, "./*")
        chapter_num = len(contents)
        num = [[] for i in range(chapter_num)]
        for chapter in range(chapter_num):
            contents[chapter].click()
            time.sleep(0.5)

            contents = contents_area.find_elements(By.XPATH, "./*")
            section_num = len(contents) - chapter_num
            [num[chapter].append([]) for i in range(section_num)]
            for section in range(section_num):
                contents[chapter+section+1].click()
                time.sleep(0.5)

                contents = contents_area.find_elements(By.XPATH, "./*")
                video_num = len(contents) - chapter_num - section_num
                [num[chapter][section].append([]) for i in range(video_num)]
                contents[chapter+section+1].click()
                time.sleep(0.5)
                contents = contents_area.find_elements(By.XPATH, "./*")

            contents[chapter].click()
            time.sleep(0.5)
            contents = contents_area.find_elements(By.XPATH, "./*")

        # 将页面向上滚动，不然第一个章节点击不了
        self.driver.execute_script("window.scrollBy(0, -500);")

        for i in range(len(num)):
            print("第" + str(i+1) + "章有" + str(len(num[i])) + "个小节")
            for j in range(len(num[i])):
                print("第" + str(j + 1) + "小节有" + str(len(num[i][j])) + "个视频")
                for k in range(len(num[i][j])):
                    contents[i].click()
                    time.sleep(0.5)
                    contents = contents_area.find_elements(By.XPATH, "./*")
                    contents[i+j+1].click()
                    time.sleep(0.5)
                    contents = contents_area.find_elements(By.XPATH, "./*")
                    name = contents[i + j + k + 2].text
                    contents[i + j + k + 2].click()
                    time.sleep(0.5)
                    video_page_url = self.driver.current_url
                    m3u8_url = self.get_m3u8_url(video_page_url)
                    print(m3u8_url)
                    self.driver.back()

                    self.data["grade"].append(info["grade"])
                    self.data["semester"].append(info["semester"])
                    self.data["category"].append(self.category)
                    self.data["version"].append(info["version"])
                    self.data["executor"].append(self.executor)
                    self.data["chapter"].append(i)
                    self.data["section"].append(j)
                    self.data["name"].append(name)
                    self.data["content"].append(m3u8_url)

                    time.sleep(1)
                    # 解析目录区域
                    contents_area = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div/div/div/div/div[3]/div[2]/div[3]/div/div/div")))
                    # 预处理，将所有的标签全部关闭
                    contents = contents_area.find_elements(By.XPATH, "./*")
                    contents[1].click()
                    time.sleep(0.5)
                    contents = contents_area.find_elements(By.XPATH, "./*")
                    contents[0].click()
                    time.sleep(0.5)
                    contents = contents_area.find_elements(By.XPATH, "./*")


        print("ok")


    def parse_video_list_2(self, info):
        time.sleep(1)
        # 解析目录区域
        contents_area = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH,"/html/body/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div/div/div/div/div[3]/div[2]/div[3]/div/div/div")))

        # 预处理，将所有的标签全部关闭
        contents = contents_area.find_elements(By.XPATH, "./*")
        contents[0].click()
        time.sleep(0.5)

        # 逐层打开
        contents = contents_area.find_elements(By.XPATH, "./*")
        chapter_num = len(contents)
        num = [[] for i in range(chapter_num)]
        for chapter in range(chapter_num):
            contents[chapter].click()
            time.sleep(0.5)

            contents = contents_area.find_elements(By.XPATH, "./*")
            video_num = len(contents) - chapter_num
            [num[chapter].append([]) for i in range(video_num)]
            contents[chapter].click()
            time.sleep(0.5)
            contents = contents_area.find_elements(By.XPATH, "./*")

        # 将页面向上滚动一定像素，不然第一个章节点击不了
        self.driver.execute_script("window.scrollBy(0, -500);")

        for i in range(len(num)):
            print("第" + str(i + 1) + "章有" + str(len(num[i])) + "个视频")
            for j in range(len(num[i])):
                contents[i].click()
                time.sleep(0.5)
                contents = contents_area.find_elements(By.XPATH, "./*")
                name = contents[i + j + 1].text
                contents[i+j+1].click()
                time.sleep(0.5)
                video_page_url = self.driver.current_url
                m3u8_url = self.get_m3u8_url(video_page_url)
                print(m3u8_url)
                self.driver.back()

                self.data["grade"].append(info["grade"])
                self.data["semester"].append(info["semester"])
                self.data["category"].append(self.category)
                self.data["version"].append(info["version"])
                self.data["executor"].append(self.executor)
                self.data["chapter"].append(i)
                self.data["section"].append(-1)  # 没有小节，赋值为-1
                self.data["name"].append(name)
                self.data["content"].append(m3u8_url)

                time.sleep(1)
                # 解析目录区域
                contents_area = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div/div/div/div[3]/div[4]/div[2]/div[2]/div/div/div/div/div/div/div[3]/div[2]/div[3]/div/div/div")))

                # 预处理，将所有的标签全部关闭
                contents = contents_area.find_elements(By.XPATH, "./*")
                contents[0].click()
                time.sleep(0.5)
                contents = contents_area.find_elements(By.XPATH, "./*")


        print("ok")


    def click_option(self, info):
        # 查找并点击小学标签
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[3]/div[4]/div[2]/div[1]/div/div[2]/div')))
        time.sleep(1)
        # 等待小学标签可点击
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div/div/div/div[3]/div[4]/div[2]/div[1]/div/div[2]/div/div[1]/div[2]/label[1]')))
        school = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div/div/div/div[3]/div[4]/div[2]/div[1]/div/div[2]/div/div[1]/div[2]/label[1]')))
        self.driver.execute_script('arguments[0].click();', school)

        time.sleep(1)
        # 解析年级区域
        # 等待六年级标签可点击
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div/div/div/div[3]/div[4]/div[2]/div[1]/div/div[2]/div/div[2]/div[2]/label[6]")))
        # 查找年级区域
        grade_area = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div/div/div/div[3]/div[4]/div[2]/div[1]/div/div[2]/div/div[2]/div[2]')))
        # 查找所有年级元素
        grade_elements = grade_area.find_elements(By.TAG_NAME, "label")
        grade = None
        for g in grade_elements:
            if g.text == info["grade"]:
                grade = g
        if grade is None:
            return False
        self.driver.execute_script('arguments[0].click();', grade)

        time.sleep(1)
        # 点击数学
        subject = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div/div/div/div[3]/div[4]/div[2]/div[1]/div/div[2]/div/div[3]/div[2]/label[2]')))
        self.driver.execute_script('arguments[0].click();', subject)

        time.sleep(1)
        # 解析版本区域
        # 等待人教版标签可以点击
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div/div/div/div[3]/div[4]/div[2]/div[1]/div/div[2]/div/div[4]/div[2]/label[4]")))
        # 查找版本区域
        version_area = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div/div/div/div[3]/div[4]/div[2]/div[1]/div/div[2]/div/div[4]/div[2]')))
        # 查找所有版本元素
        versions = version_area.find_elements(By.TAG_NAME, "label")
        version = None
        for v in versions:
            if v.text == info["version"]:
                version = v
        if version is None:
            return False
        self.driver.execute_script('arguments[0].click();', version)

        time.sleep(1)
        # 解析册次区域
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div/div/div/div[3]/div[4]/div[2]/div[1]/div/div[2]/div/div[5]/div[2]/label[1]")))
        semester_area = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div/div/div/div[3]/div[4]/div[2]/div[1]/div/div[2]/div/div[5]/div[2]')))
        # 查找所有的册次元素
        semesters = semester_area.find_elements(By.TAG_NAME, "label")
        semester = None
        for s in semesters:
            if s.text == info["semester"]:
                semester = s
        if semester is None:
            return False
        self.driver.execute_script('arguments[0].click();', semester)

        return True


    # 获取每个视频页面的url
    def get_video_url(self):
        self.driver = sdriver.Edge()
        self.driver.get(self.url)
        print(self.driver.current_url)

        sinfo = {
            "grade": ["三年级", "四年级"],
            "semester": ["上册", "下册"],
            "version": ["北京版", "北师大版", "苏教版", "人教版"],
        }
        info = {
            "grade": None,
            "semester": None,
            "version": None
        }
        for grade in sinfo["grade"]:
            for version in sinfo["version"]:
                for semester in sinfo["semester"]:
                    info["grade"] = grade
                    info["version"] = version
                    info["semester"] = semester
                    if self.click_option(info) is True:
                        print("爬取信息 " + "grade: " + grade + ", " + "version: " + version + ", " + "semester: " + semester)
                        time.sleep(5)  # 等待视频列表加载完成
                        if version == "北京版":
                            self.parse_video_list_1(info)
                        else:
                            self.parse_video_list_2(info)
                    else:
                        continue


if __name__ == "__main__":
    driverfile_path = "D:/Files/Projects/msedgedriver.exe"
    request = zxx_edu_cn_parser(driverfile_path=driverfile_path)
    request.get_video_url()
