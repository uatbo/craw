from bs4 import BeautifulSoup as bs
from requests.good_ke_jian import good_ke_jian_request as gkjrq

import re


class good_ke_jian:
    def __init__(self, base_url="http://www.goodkejian.com/", url="mulu/sxrj.htm"):
        self.base_url = base_url
        self.url = base_url + url
        self.url_list = self.good_ke_jian_parser(self.url)

        '''
        url0: 课件url
        url1: 教案url
        url1: 试题或试卷url
        '''
        self.download_url = [
            {
                "grade": 3,
                "semester": 0,
                "url": [[], [], []],
                "name": [[], [], []]
            },
            {
                "grade": 3,
                "semester": 1,
                "url": [[], [], []],
                "name": [[], [], []]
            },
            {
                "grade": 4,
                "semester": 0,
                "url": [[], [], []],
                "name": [[], [], []]
            },
            {
                "grade": 4,
                "semester": 1,
                "url": [[], [], []],
                "name": [[], [], []]
            }
        ]

    def find_download_url(self, url):
        html = gkjrq(self.base_url + url)
        soup = bs(html, "html.parser")
        a_list = soup.find_all('a')

        for k in a_list:
            k_string = str(k.string).encode('unicode-escape').decode()
            if re.search(r"\\u4e3b\\u529b\\u4e0b\\u8f7d\\u4e00", k_string) is not None:
                return self.base_url + k["href"][3:]

        return

    def specific_parser(self, url):
        html = gkjrq(url)
        soup = bs(html, "html.parser")
        a_list = soup.find_all('a')

        # 0代表课件，1代表教案，2代表试题
        urlList0 = []
        urlList1 = []
        urlList2 = []

        name0 = []
        name1 = []
        name2 = []

        for k in a_list:
            k_string = str(k.string).encode('unicode-escape').decode()
            if re.search(r"\\u5e74\\u7ea7.+?\\u8bfe\\u4ef6", k_string):  # 匹配“年级”...“课件”
                download_url = self.find_download_url(k["href"])
                if download_url is None:
                    continue
                name0.append(k.string)
                urlList0.append(download_url)
            elif re.search(r"\\u5e74\\u7ea7.+?(\\u6559\\u6848|\\u6559\\u5b66\\u8bbe\\u8ba1)",
                           k_string):  # 匹配“年级”...“教案”|“教学设计”
                download_url = self.find_download_url(k["href"])
                if download_url is None:
                    continue
                name1.append(k.string)
                urlList1.append(download_url)
            elif re.search(r"\\u5e74\\u7ea7.+?(\\u8bd5\\u9898|\\u8bd5\\u5377|\\u6d4b\\u8bd5)",
                           k_string):  # 匹配“年级”...“试题”|“试卷”|“测试”
                download_url = self.find_download_url(k["href"])
                if download_url is None:
                    continue
                name2.append(k.string)
                urlList2.append(download_url)
            else:
                pass

        return urlList0, urlList1, urlList2, name0, name1, name2

    def good_ke_jian_parser(self, url):
        html = gkjrq(url)
        soup = bs(html, "html.parser")
        a_list = soup.find_all('a')

        url_list = []
        for k in a_list:
            k_string = str(k.string).encode('unicode-escape').decode()

            if re.search(r"(\\u4e09\\u5e74\\u7ea7|\\u56db\\u5e74\\u7ea7)", k_string):
                info_dict = {
                    "grade": 3,
                    "semester": 0,
                    "category": 0,
                    "url": ""
                }

                '''
                grade: 3代表三年级，4代表四年级
                semester: 0代表上册，1代表下册
                category: 0代表课件，1代表教案，2代表试题
                '''
                grade = 3
                category = 0
                semester = 0
                url = ""

                if re.search(r"\\u4e09\\u5e74\\u7ea7", k_string) is not None:
                    grade = 3
                    # 判断上下册
                    if re.search(r"\\u4e0a\\u518c", k_string) is not None:
                        semester = 0
                    elif re.search(r"\\u4e0b\\u518c", k_string) is not None:
                        semester = 1
                    else:
                        pass
                    # 判断资源类型
                    if re.search(r"\\u8bfe\\u4ef6", k_string) is not None:
                        category = 0
                    elif re.search(r"\\u6559\\u6848", k_string) is not None:
                        category = 1
                    elif re.search(r"\\u8bd5\\u9898", k_string) is not None:
                        category = 2
                    else:
                        pass
                    url = k['href']

                elif re.search(r"\\u56db\\u5e74\\u7ea7", k_string) is not None:
                    grade = 4
                    # 判断上下册
                    if re.search(r"\\u4e0a\\u518c", k_string) is not None:
                        semester = 0
                    elif re.search(r"\\u4e0b\\u518c", k_string) is not None:
                        semester = 1
                    else:
                        pass
                    # 判断资源类型
                    if re.search(r"\\u8bfe\\u4ef6", k_string) is not None:
                        category = 0
                    elif re.search(r"\\u6559\\u6848", k_string) is not None:
                        category = 1
                    elif re.search(r"\\u8bd5\\u9898", k_string) is not None:
                        category = 2
                    else:
                        pass
                    url = k['href']

                else:
                    pass

                info_dict["grade"] = grade
                info_dict["semester"] = semester
                info_dict["category"] = category
                info_dict["url"] = url

                url_list.append(info_dict)

        return url_list

    def run(self):
        # 分别爬取每个年级的每个学期的每个资源
        for i in self.url_list:
            print(len(self.url_list))
            print("grade: " + str(i["grade"]) + ", " + "semester: " + str(i["semester"]) + ", " + "category: " + str(i["category"]))

            # 查看有多少页，读取第一页的页脚的总页数
            html = gkjrq(i["url"])
            soup = bs(html, "html.parser")
            font_list = soup.find_all('font')
            numOfPages = 1  # 页面数
            for f in font_list:
                if f["color"] == "#FF0000":
                    try:
                        numOfPages = int(f.string)
                    except:
                        continue
            print("总共有"+str(numOfPages)+"页")

            # 一页一页的爬取
            for num in range(1, numOfPages + 1):
                print("第"+str(num)+"页:")
                url = i["url"] + "&page=" + str(num)
                print("页面url: "+url)

                url0, url1, url2, name0, name1, name2 = self.specific_parser(url)
                print(url0)
                print(url1)
                print(url2)
                for j in self.download_url:
                    if j["grade"] == i["grade"] and j["semester"] == i["semester"]:
                        j["url"][0].extend(url0)
                        j["url"][1].extend(url1)
                        j["url"][2].extend(url2)
                        j["name"][0].extend(name0)
                        j["name"][1].extend(name1)
                        j["name"][2].extend(name2)

        # 打印爬取到的信息
        for i in self.download_url:
            print("grade: " + str(i["grade"]) + ", " + "semester: " + str(i["semester"]))
            print(i["url"])
            print(i["name"])

        return self.download_url



# from bs4 import BeautifulSoup as bs
# from requests.good_ke_jian import good_ke_jian_request as gkjrq
# import pika
# import re
# import json
# import time
# import pandas
#
# class good_ke_jian:
#     def __init__(self, base_url="http://www.goodkejian.com/", url="http://goodkejian.com/mulu/sxrj.htm", version="人教版"):
#         self.base_url = base_url
#         self.url = url
#         self.version = version
#         self.urlList = self.good_ke_jian_parser(self.url)
#
#         '''
#         url0: 课件url
#         url1: 教案url
#         url1: 试题或试卷url
#         '''
#         self.download_url = [
#             {
#                 "grade": 3,
#                 "semester": 0,
#                 "version": self.version,
#                 "url0": [],
#                 "url1": [],
#                 "url2": []
#             },
#             {
#                 "grade": 3,
#                 "semester": 1,
#                 "version": self.version,
#                 "url0": [],
#                 "url1": [],
#                 "url2": []
#             },
#             {
#                 "grade": 4,
#                 "semester": 0,
#                 "version": self.version,
#                 "url0": [],
#                 "url1": [],
#                 "url2": []
#             },
#             {
#                 "grade": 4,
#                 "semester": 1,
#                 "version": self.version,
#                 "url0": [],
#                 "url1": [],
#                 "url2": []
#             }
#         ]
#
#     def findDownloadUrl(self, base_url, url):
#         html = gkjrq(base_url + url)
#
#         soup = bs(html, "html.parser")
#         aList = soup.find_all('a')
#
#         for k in aList:
#             k_string = str(k.string).encode('unicode-escape').decode()
#             if re.search(r"\\u4e3b\\u529b\\u4e0b\\u8f7d\\u4e00", k_string) is not None:
#                 return base_url + k["href"][3:]
#
#         return
#
#     def specific_parser(self, base_url, url):
#         html = gkjrq(url)
#         soup = bs(html, "html.parser")
#         aList = soup.find_all('a')
#
#         # 0代表课件，1代表教案，2代表试题
#         urlList0 = []
#         urlList1 = []
#         urlList2 = []
#
#         name0 = []
#         name1 = []
#         name2 = []
#
#         for k in aList:
#             k_string = str(k.string).encode('unicode-escape').decode()
#             if re.search(r"\\u5e74\\u7ea7.+?\\u8bfe\\u4ef6", k_string):  # 匹配“年级”...“课件”
#                 downloadUrl = self.findDownloadUrl(base_url, k["href"])
#                 if downloadUrl is None:
#                     continue
#                 name0.append(k.string)
#                 urlList0.append(downloadUrl)
#             elif re.search(r"\\u5e74\\u7ea7.+?(\\u6559\\u6848|\\u6559\\u5b66\\u8bbe\\u8ba1)",
#                            k_string):  # 匹配“年级”...“教案”|“教学设计”
#                 downloadUrl = self.findDownloadUrl(base_url, k["href"])
#                 if downloadUrl is None:
#                     continue
#                 name1.append(k.string)
#                 urlList1.append(downloadUrl)
#             elif re.search(r"\\u5e74\\u7ea7.+?(\\u8bd5\\u9898|\\u8bd5\\u5377|\\u6d4b\\u8bd5)",
#                            k_string):  # 匹配“年级”...“试题”|“试卷”|“测试”
#                 downloadUrl = self.findDownloadUrl(base_url, k["href"])
#                 if downloadUrl is None:
#                     continue
#                 name2.append(k.string)
#                 urlList2.append(downloadUrl)
#             else:
#                 pass
#
#         return urlList0, urlList1, urlList2, name0, name1, name2
#
#     def good_ke_jian_parser(self, url):
#         html = gkjrq(url)
#         soup = bs(html, "html.parser")
#         aList = soup.find_all('a')
#
#         urlList = []
#         for k in aList:
#             k_string = str(k.string).encode('unicode-escape').decode()
#
#             if re.search(r"(\\u4e09\\u5e74\\u7ea7|\\u56db\\u5e74\\u7ea7)", k_string):
#                 infoDict = {
#                     "grade": 3,
#                     "sourceType": 0,
#                     "semester": 0,
#                     "version": "",
#                     "url": ""
#                 }
#                 '''
#                 grade: 3代表三年级，4代表四年级
#                 sourceType: 0代表课件，1代表教案，2代表试题
#                 semester: 0代表上册，1代表下册
#                 version: 教材版本
#                 '''
#                 grade = 3
#                 sourceType = 0
#                 semester = 0
#                 version = self.version
#                 url = ""
#
#                 if re.search(r"\\u4e09\\u5e74\\u7ea7", k_string) is not None:
#                     grade = 3
#                     # 判断资源类型
#                     if re.search(r"\\u8bfe\\u4ef6", k_string) is not None:
#                         sourceType = 0
#                     elif re.search(r"\\u6559\\u6848", k_string) is not None:
#                         sourceType = 1
#                     elif re.search(r"\\u8bd5\\u9898", k_string) is not None:
#                         sourceType = 2
#                     else:
#                         pass
#                     # 判断上下册
#                     if re.search(r"\\u4e0a\\u518c", k_string) is not None:
#                         semester = 0
#                     elif re.search(r"\\u4e0b\\u518c", k_string) is not None:
#                         semester = 1
#                     else:
#                         pass
#
#                     version = self.version
#                     url = k['href']
#
#                 elif re.search(r"\\u56db\\u5e74\\u7ea7", k_string) is not None:
#                     grade = 4
#                     # 判断资源类型
#                     if re.search(r"\\u8bfe\\u4ef6", k_string) is not None:
#                         sourceType = 0
#                     elif re.search(r"\\u6559\\u6848", k_string) is not None:
#                         sourceType = 1
#                     elif re.search(r"\\u8bd5\\u9898", k_string) is not None:
#                         sourceType = 2
#                     else:
#                         pass
#                     # 判断上下册
#                     if re.search(r"\\u4e0a\\u518c", k_string) is not None:
#                         semester = 0
#                     elif re.search(r"\\u4e0b\\u518c", k_string) is not None:
#                         semester = 1
#                     else:
#                         pass
#
#                     version = self.version
#                     url = k['href']
#
#                 else:
#                     pass
#
#                 infoDict["grade"] = grade
#                 infoDict["sourceType"] = sourceType
#                 infoDict["semester"] = semester
#                 infoDict["version"] = version
#                 infoDict["url"] = url
#
#                 urlList.append(infoDict)
#
#         return urlList
#
#     def run(self):
#         # 分别爬取每个年级的每个学期的每个资源
#         for i in self.urlList:
#             print("grade: " + str(i["grade"]) + ", " + "semester: " + str(i["semester"]))
#
#             # 查看有多少页，读取第一页的页脚的总页数
#             html = gkjrq(i["url"])
#             soup = bs(html, "html.parser")
#             fontList = soup.find_all('font')
#             numOfPages = 1  # 页面数
#             for f in fontList:
#                 if f["color"] == "#FF0000":
#                     try:
#                         numOfPages = int(f.string)
#                     except:
#                         continue
#             print("总共有"+str(numOfPages)+"页")
#             # 一页一页的爬取
#             for num in range(1, numOfPages + 1):
#                 print("第"+str(num)+"页:")
#                 url = i["url"] + "&page=" + str(num)
#                 # page = gkjrq(i["url"] + "&page=" + str(num))
#                 print("页面url: "+url)
#
#                 url0, url1, url2, name0, name1, name2 = self.specific_parser(self.base_url, url)
#                 print(url0)
#                 print(url1)
#                 print(url2)
#                 for j in self.download_url:
#                     if j["grade"] == i["grade"] and j["semester"] == i["semester"]:
#                         j["url0"].extend(url0)
#                         j["url1"].extend(url1)
#                         j["url2"].extend(url2)
#
#                         # # 发送到消息队列
#                         # # 连接到RabbitMQ服务器
#                         # connection = pika.BlockingConnection(
#                         #     pika.ConnectionParameters('114.132.249.3', 5672, "/",
#                         #                               pika.PlainCredentials("admin", "rabbitmlgbz0729")))
#                         # channel = connection.channel()
#                         # # 创建消息队列，如果队列已存在则不会重复创建
#                         # channel.queue_declare(queue='courseware_queue')
#                         # # 发送课件
#                         # for url, name in zip(url0, name0):
#                         #     body = json.dumps(
#                         #         {
#                         #             "content": url,
#                         #             "grade": j["grade"],
#                         #             "name": name,
#                         #             "semester": j["semester"],
#                         #             "category": 0,
#                         #             "version": self.version,
#                         #             "executor": "段斌",
#                         #             "needUncompress": 1
#                         #         }
#                         #     ).encode("utf-8")
#                         #     # 向消息队列发送消息
#                         #     channel.basic_publish(exchange='courseware_exchange', routing_key='hello', body=body)
#                         #     print("Sent!")
#                         #     time.sleep(0.5)
#                         # # 发送教案
#                         # for url, name in zip(url1, name1):
#                         #     body = json.dumps(
#                         #         {
#                         #             "content": url,
#                         #             "grade": j["grade"],
#                         #             "name": name,
#                         #             "semester": j["semester"],
#                         #             "category": 1,
#                         #             "version": self.version,
#                         #             "executor": "段斌",
#                         #             "needUncompress": 1
#                         #         }
#                         #     ).encode("utf-8")
#                         #     # 向消息队列发送消息
#                         #     channel.basic_publish(exchange='courseware_exchange', routing_key='hello', body=body)
#                         #     print("Sent!")
#                         #     time.sleep(0.5)
#                         # # 发送试题
#                         # for url, name in zip(url2, name2):
#                         #     body = json.dumps(
#                         #         {
#                         #             "content": url,
#                         #             "grade": j["grade"],
#                         #             "name": name,
#                         #             "semester": j["semester"],
#                         #             "category": 2,
#                         #             "version": self.version,
#                         #             "executor": "段斌",
#                         #             "needUncompress": 1
#                         #         }
#                         #     ).encode("utf-8")
#                         #     # 向消息队列发送消息
#                         #     channel.basic_publish(exchange='courseware_exchange', routing_key='hello', body=body)
#                         #     print("Sent!")
#                         #     time.sleep(0.5)
#                         #
#                         # channel.close()
#
#         # 打印爬取到的信息
#         for i in self.download_url:
#             print("grade: " + str(i["grade"]) + ", " + "semester: " + str(i["semester"]))
#             print(i["url0"])
#             print(i["url1"])
#             print(i["url2"])



# def findDownloadUrl(base_url, url):
#     html = gkjrq(base_url + url)
#
#     soup = bs(html, "html.parser")
#     aList = soup.find_all('a')
#
#     for k in aList:
#         k_string = str(k.string).encode('unicode-escape').decode()
#         if re.search(r"\\u4e3b\\u529b\\u4e0b\\u8f7d\\u4e00", k_string) is not None:
#             return base_url + k["href"][3:]
#
#     return
#
#
# def specific_grade_parser(base_url, html):
#     soup = bs(html, "html.parser")
#     aList = soup.find_all('a')
#
#     # 0代表课件，1代表教案，2代表试题
#     urlList0 = []
#     urlList1 = []
#     urlList2 = []
#
#     for k in aList:
#         k_string = str(k.string).encode('unicode-escape').decode()
#         if re.search(r"\\u5e74\\u7ea7.+?\\u8bfe\\u4ef6", k_string):  # 匹配“年级”...“课件”
#             downloadUrl = findDownloadUrl(base_url, k["href"])
#             if downloadUrl is None:
#                 continue
#             urlList0.append(downloadUrl)
#         elif re.search(r"\\u5e74\\u7ea7.+?(\\u6559\\u6848|\\u6559\\u5b66\\u8bbe\\u8ba1)", k_string):  # 匹配“年级”...“教案”|“教学设计”
#             downloadUrl = findDownloadUrl(base_url, k["href"])
#             if downloadUrl is None:
#                 continue
#             urlList1.append(downloadUrl)
#         elif re.search(r"\\u5e74\\u7ea7.+?(\\u8bd5\\u9898|\\u8bd5\\u5377|\\u6d4b\\u8bd5)", k_string):  # 匹配“年级”...“试题”|“试卷”|“测试”
#             downloadUrl = findDownloadUrl(base_url, k["href"])
#             if downloadUrl is None:
#                 continue
#             urlList2.append(downloadUrl)
#         else:
#             pass
#
#     return urlList0, urlList1, urlList2
#
#
# def good_ke_jian_parser(html):
#     soup = bs(html, "html.parser")
#
#     aList = soup.find_all('a')
#
#     urlList = []
#     for k in aList:
#         k_string = str(k.string).encode('unicode-escape').decode()
#
#         if re.search(r"(\\u4e09\\u5e74\\u7ea7|\\u56db\\u5e74\\u7ea7)", k_string):
#             infoDict = {
#                 "grade": 3,
#                 "sourceType": 0,
#                 "semester": 0,
#                 "version": "人教版",
#                 "url": ""
#             }
#             '''
#             grade: 3代表三年级，4代表四年级
#             sourceType: 0代表课件，1代表教案，2代表试题
#             semester: 0代表上册，1代表下册
#             version: 教材版本
#             '''
#             grade = 3
#             sourceType = 0
#             semester = 0
#             version = "人教版"
#             url = ""
#
#             if re.search(r"\\u4e09\\u5e74\\u7ea7", k_string) is not None:
#                 grade = 3
#                 # 判断资源类型
#                 if re.search(r"\\u8bfe\\u4ef6", k_string) is not None:
#                     sourceType = 0
#                 elif re.search(r"\\u6559\\u6848", k_string) is not None:
#                     sourceType = 1
#                 elif re.search(r"\\u8bd5\\u9898", k_string) is not None:
#                     sourceType = 2
#                 else:
#                     pass
#                 # 判断上下册
#                 if re.search(r"\\u4e0a\\u518c", k_string) is not None:
#                     semester = 0
#                 elif re.search(r"\\u4e0b\\u518c", k_string) is not None:
#                     semester = 1
#                 else:
#                     pass
#
#                 version = "人教版"
#                 url = k['href']
#
#             elif re.search(r"\\u56db\\u5e74\\u7ea7", k_string) is not None:
#                 grade = 4
#                 # 判断资源类型
#                 if re.search(r"\\u8bfe\\u4ef6", k_string) is not None:
#                     sourceType = 0
#                 elif re.search(r"\\u6559\\u6848", k_string) is not None:
#                     sourceType = 1
#                 elif re.search(r"\\u8bd5\\u9898", k_string) is not None:
#                     sourceType = 2
#                 else:
#                     pass
#                 # 判断上下册
#                 if re.search(r"\\u4e0a\\u518c", k_string) is not None:
#                     semester = 0
#                 elif re.search(r"\\u4e0b\\u518c", k_string) is not None:
#                     semester = 1
#                 else:
#                     pass
#
#                 version = "人教版"
#                 url = k['href']
#
#             else:
#                 pass
#
#             infoDict["grade"] = grade
#             infoDict["sourceType"] = sourceType
#             infoDict["semester"] = semester
#             infoDict["version"] = version
#             infoDict["url"] = url
#
#             urlList.append(infoDict)
#
#     return urlList
#
#
# if __name__ == "__main__":
#     html_doc = """
#     <html><head><title>The Dormouse's story</title></head>
#     <body>
#     <p class="title"><b>The Dormouse's story</b></p>
#
#     <p class="story">Once upon a time there were three little sisters; and their names were
#     <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
#     <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
#     <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
#     and they lived at the bottom of a well.</p>
#
#     <p class="story">...</p>
#     """
#
#     base_url = "http://www.goodkejian.com/"
#     url = "http://goodkejian.com/mulu/sxrj.htm"
#
#     info = []
#     html = gkjrq(url)
#
#     urlList = good_ke_jian_parser(html)
#     download_url = [
#         {
#             "grade": 3,
#             "semester": 0,
#             "version": "人教版",
#             "url0": [],
#             "url1": [],
#             "url2": []
#         },
#         {
#             "grade": 3,
#             "semester": 1,
#             "version": "人教版",
#             "url0": [],
#             "url1": [],
#             "url2": []
#         },
#         {
#             "grade": 4,
#             "semester": 0,
#             "version": "人教版",
#             "url0": [],
#             "url1": [],
#             "url2": []
#         },
#         {
#             "grade": 4,
#             "semester": 1,
#             "version": "人教版",
#             "url0": [],
#             "url1": [],
#             "url2": []
#         }
#     ]
#     for i in urlList:
#
#         # 查看有多少页
#         html = gkjrq(i["url"])
#         soup = bs(html, "html.parser")
#         fontList = soup.find_all('font')
#         numOfPages = 1
#         for f in fontList:
#             if f["color"] == "#FF0000":
#                 try:
#                     numOfPages = int(f.string)
#                 except:
#                     continue
#
#         for num in range(1, numOfPages+1):
#             html = gkjrq(i["url"] + "&page=" + str(num))
#             print(i["url"] + "&page=" + str(num))
#
#             url0, url1, url2 = specific_grade_parser(base_url, html)
#             for j in download_url:
#                 if j["grade"] == i["grade"] and j["semester"] == i["semester"]:
#                     j["url0"].extend(url0)
#                     j["url1"].extend(url1)
#                     j["url2"].extend(url2)
#
#                     # import pika
#                     #
#                     # # 连接到RabbitMQ服务器
#                     # connection = pika.BlockingConnection(
#                     #     pika.ConnectionParameters('114.132.249.3', 5672, "/",
#                     #                               pika.PlainCredentials("admin", "rabbitmlgbz0729")))
#                     # channel = connection.channel()
#                     #
#                     # # 创建消息队列，如果队列已存在则不会重复创建
#                     # channel.queue_declare(queue='courseware_queue')
#                     #
#                     # for url in j["url0"]:
#                     #     body = json.dumps(
#                     #         {
#                     #             "content": url,
#                     #             "grade": j["grade"],
#                     #             "name": "kejian",
#                     #             "semester": j["semester"],
#                     #             "version": "人教版",
#                     #             "executor": "段斌"
#                     #         }
#                     #     ).encode("utf-8")
#                     #     # 向消息队列发送消息
#                     #     channel.basic_publish(exchange='courseware_exchange', routing_key='hello', body=body)
#                     #     print(" [x] Sent 'Hello World!'")
#                     #     import time
#                     #
#                     #     time.sleep(5)
#
#
#     for i in download_url:
#         print("grade: " + str(i["grade"]) + ", " + "semester: " + str(i["semester"]))
#         print(i["url0"])
#         print(i["url1"])
#         print(i["url2"])
#
#     # import pika
#     #
#     # # 连接到RabbitMQ服务器
#     # connection = pika.BlockingConnection(
#     #     pika.ConnectionParameters('114.132.249.3', 5672, "/", pika.PlainCredentials("admin", "rabbitmlgbz0729")))
#     # channel = connection.channel()
#     #
#     # # 创建消息队列，如果队列已存在则不会重复创建
#     # channel.queue_declare(queue='courseware_queue')
#     #
#     #
#     # for i in download_url:
#     #     for url in i["url0"]:
#     #         body = json.dumps(
#     #             {
#     #                 "content": url,
#     #                 "grade": i["grade"],
#     #                 "name": "kejian",
#     #                 "semester": i["semester"],
#     #                 "version": "人教版",
#     #                 "executor": "段斌"
#     #             }
#     #         ).encode("utf-8")
#     #         # 向消息队列发送消息
#     #         channel.basic_publish(exchange='courseware_exchange', routing_key='hello', body=body)
#     #         print(" [x] Sent 'Hello World!'")
#     #         import time
#     #
#     #         time.sleep(5)
#     #
#     #
#     #
#     # connection.close()


# http://www.goodkejian.com/search.asp?keyword=%C8%CB%BD%CC%20%CA%FD%D1%A7%20%C8%FD%C4%EA%BC%B6%20%C9%CF%20%BF%CE&page=1



# def findDownloadUrl(base_url, url):
#     html = gkjrq(base_url + url)
#
#     soup = bs(html, "html.parser")
#     aList = soup.find_all('a')
#
#     for k in aList:
#         k_string = str(k.string).encode('unicode-escape').decode()
#         if re.search(r"\\u4e3b\\u529b\\u4e0b\\u8f7d\\u4e00", k_string) is not None:
#             return base_url + k["href"][3:]
#
#     return
#
#
# def specific_grade_parser(base_url, html):
#     soup = bs(html, "html.parser")
#     aList = soup.find_all('a')
#
#     # 0代表课件，1代表教案，2代表试题
#     urlList0 = []
#     urlList1 = []
#     urlList2 = []
#
#     for k in aList:
#         k_string = str(k.string).encode('unicode-escape').decode()
#         if re.search(r"\\u5e74\\u7ea7.+?\\u8bfe\\u4ef6", k_string):  # 匹配“年级”...“课件”
#             downloadUrl = findDownloadUrl(base_url, k["href"])
#             if downloadUrl is None:
#                 continue
#             urlList0.append(downloadUrl)
#         elif re.search(r"\\u5e74\\u7ea7.+?(\\u6559\\u6848|\\u6559\\u5b66\\u8bbe\\u8ba1)", k_string):  # 匹配“年级”...“教案”|“教学设计”
#             downloadUrl = findDownloadUrl(base_url, k["href"])
#             if downloadUrl is None:
#                 continue
#             urlList1.append(downloadUrl)
#         elif re.search(r"\\u5e74\\u7ea7.+?(\\u8bd5\\u9898|\\u8bd5\\u5377|\\u6d4b\\u8bd5)", k_string):  # 匹配“年级”...“试题”|“试卷”|“测试”
#             downloadUrl = findDownloadUrl(base_url, k["href"])
#             if downloadUrl is None:
#                 continue
#             urlList2.append(downloadUrl)
#         else:
#             pass
#
#     return urlList0, urlList1, urlList2
#
#
# def good_ke_jian_parser(html):
#     soup = bs(html, "html.parser")
#
#     aList = soup.find_all('a')
#
#     urlList = []
#     for k in aList:
#         k_string = str(k.string).encode('unicode-escape').decode()
#
#         if re.search(r"(\\u4e09\\u5e74\\u7ea7|\\u56db\\u5e74\\u7ea7)", k_string):
#             infoDict = {
#                 "grade": 3,
#                 "sourceType": 0,
#                 "semester": 0,
#                 "version": "人教版",
#                 "url": ""
#             }
#             '''
#             grade: 3代表三年级，4代表四年级
#             sourceType: 0代表课件，1代表教案，2代表试题
#             semester: 0代表上册，1代表下册
#             version: 教材版本
#             '''
#             grade = 3
#             sourceType = 0
#             semester = 0
#             version = "人教版"
#             url = ""
#
#             if re.search(r"\\u4e09\\u5e74\\u7ea7", k_string) is not None:
#                 grade = 3
#                 # 判断资源类型
#                 if re.search(r"\\u8bfe\\u4ef6", k_string) is not None:
#                     sourceType = 0
#                 elif re.search(r"\\u6559\\u6848", k_string) is not None:
#                     sourceType = 1
#                 elif re.search(r"\\u8bd5\\u9898", k_string) is not None:
#                     sourceType = 2
#                 else:
#                     pass
#                 # 判断上下册
#                 if re.search(r"\\u4e0a\\u518c", k_string) is not None:
#                     semester = 0
#                 elif re.search(r"\\u4e0b\\u518c", k_string) is not None:
#                     semester = 1
#                 else:
#                     pass
#
#                 version = "人教版"
#                 url = k['href']
#
#             elif re.search(r"\\u56db\\u5e74\\u7ea7", k_string) is not None:
#                 grade = 4
#                 # 判断资源类型
#                 if re.search(r"\\u8bfe\\u4ef6", k_string) is not None:
#                     sourceType = 0
#                 elif re.search(r"\\u6559\\u6848", k_string) is not None:
#                     sourceType = 1
#                 elif re.search(r"\\u8bd5\\u9898", k_string) is not None:
#                     sourceType = 2
#                 else:
#                     pass
#                 # 判断上下册
#                 if re.search(r"\\u4e0a\\u518c", k_string) is not None:
#                     semester = 0
#                 elif re.search(r"\\u4e0b\\u518c", k_string) is not None:
#                     semester = 1
#                 else:
#                     pass
#
#                 version = "人教版"
#                 url = k['href']
#
#             else:
#                 pass
#
#             infoDict["grade"] = grade
#             infoDict["sourceType"] = sourceType
#             infoDict["semester"] = semester
#             infoDict["version"] = version
#             infoDict["url"] = url
#
#             urlList.append(infoDict)
#
#     return urlList
#
#
# if __name__ == "__main__":
#     html_doc = """
#     <html><head><title>The Dormouse's story</title></head>
#     <body>
#     <p class="title"><b>The Dormouse's story</b></p>
#
#     <p class="story">Once upon a time there were three little sisters; and their names were
#     <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
#     <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
#     <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
#     and they lived at the bottom of a well.</p>
#
#     <p class="story">...</p>
#     """
#
#     base_url = "http://www.goodkejian.com/"
#     url = "http://goodkejian.com/mulu/sxrj.htm"
#
#     info = []
#     html = gkjrq(url)
#
#     urlList = good_ke_jian_parser(html)
#     download_url = [
#         {
#             "grade": 3,
#             "semester": 0,
#             "version": "人教版",
#             "url0": [],
#             "url1": [],
#             "url2": []
#         },
#         {
#             "grade": 3,
#             "semester": 1,
#             "version": "人教版",
#             "url0": [],
#             "url1": [],
#             "url2": []
#         },
#         {
#             "grade": 4,
#             "semester": 0,
#             "version": "人教版",
#             "url0": [],
#             "url1": [],
#             "url2": []
#         },
#         {
#             "grade": 4,
#             "semester": 1,
#             "version": "人教版",
#             "url0": [],
#             "url1": [],
#             "url2": []
#         }
#     ]
#     for i in urlList:
#
#         # 查看有多少页
#         html = gkjrq(i["url"])
#         soup = bs(html, "html.parser")
#         fontList = soup.find_all('font')
#         numOfPages = 1
#         for f in fontList:
#             if f["color"] == "#FF0000":
#                 try:
#                     numOfPages = int(f.string)
#                 except:
#                     continue
#
#         for num in range(1, numOfPages+1):
#             html = gkjrq(i["url"] + "&page=" + str(num))
#             print(i["url"] + "&page=" + str(num))
#
#             url0, url1, url2 = specific_grade_parser(base_url, html)
#             for j in download_url:
#                 if j["grade"] == i["grade"] and j["semester"] == i["semester"]:
#                     j["url0"].extend(url0)
#                     j["url1"].extend(url1)
#                     j["url2"].extend(url2)
#
#                     # import pika
#                     #
#                     # # 连接到RabbitMQ服务器
#                     # connection = pika.BlockingConnection(
#                     #     pika.ConnectionParameters('114.132.249.3', 5672, "/",
#                     #                               pika.PlainCredentials("admin", "rabbitmlgbz0729")))
#                     # channel = connection.channel()
#                     #
#                     # # 创建消息队列，如果队列已存在则不会重复创建
#                     # channel.queue_declare(queue='courseware_queue')
#                     #
#                     # for url in j["url0"]:
#                     #     body = json.dumps(
#                     #         {
#                     #             "content": url,
#                     #             "grade": j["grade"],
#                     #             "name": "kejian",
#                     #             "semester": j["semester"],
#                     #             "version": "人教版",
#                     #             "executor": "段斌"
#                     #         }
#                     #     ).encode("utf-8")
#                     #     # 向消息队列发送消息
#                     #     channel.basic_publish(exchange='courseware_exchange', routing_key='hello', body=body)
#                     #     print(" [x] Sent 'Hello World!'")
#                     #     import time
#                     #
#                     #     time.sleep(5)
#
#
#     for i in download_url:
#         print("grade: " + str(i["grade"]) + ", " + "semester: " + str(i["semester"]))
#         print(i["url0"])
#         print(i["url1"])
#         print(i["url2"])
#
#     # import pika
#     #
#     # # 连接到RabbitMQ服务器
#     # connection = pika.BlockingConnection(
#     #     pika.ConnectionParameters('114.132.249.3', 5672, "/", pika.PlainCredentials("admin", "rabbitmlgbz0729")))
#     # channel = connection.channel()
#     #
#     # # 创建消息队列，如果队列已存在则不会重复创建
#     # channel.queue_declare(queue='courseware_queue')
#     #
#     #
#     # for i in download_url:
#     #     for url in i["url0"]:
#     #         body = json.dumps(
#     #             {
#     #                 "content": url,
#     #                 "grade": i["grade"],
#     #                 "name": "kejian",
#     #                 "semester": i["semester"],
#     #                 "version": "人教版",
#     #                 "executor": "段斌"
#     #             }
#     #         ).encode("utf-8")
#     #         # 向消息队列发送消息
#     #         channel.basic_publish(exchange='courseware_exchange', routing_key='hello', body=body)
#     #         print(" [x] Sent 'Hello World!'")
#     #         import time
#     #
#     #         time.sleep(5)
#     #
#     #
#     #
#     # connection.close()


# http://www.goodkejian.com/search.asp?keyword=%C8%CB%BD%CC%20%CA%FD%D1%A7%20%C8%FD%C4%EA%BC%B6%20%C9%CF%20%BF%CE&page=1