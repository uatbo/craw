from parsers.good_ke_jian import good_ke_jian
from utils.drop_duplicates import drop_duplicates

import pandas as pd


base_url = "http://www.goodkejian.com/"
urls = [
    ["mulu/sxrj.htm", "人教版"],
    ["mulu/sxsj.htm", "苏教版"],
    ["mulu/sxbsd.htm", "北师大版"],
    ["mulu/sxxsd.htm", "西师大版"],
    ["mulu/sxjj.htm", "冀教版"],
    ["mulu/sxzj.htm", "浙教版"],
    ["mulu/sxqd.htm", "青岛版"],
    ["mulu/sxbj.htm", "北京版"],
    ["mulu/sxhj.htm", "沪教版"]
]


executor = "段斌"
needUncompress = 1
data = {
    "grade": [],
    "semester": [],
    "category": [],
    "version": [],
    "executor": [],
    "needUncompress": [],
    "name": [],
    "content": []
}

for item in urls:
    version = item[1]
    print("爬取教材版本：" + version)
    parser = good_ke_jian(base_url, item[0])
    results = parser.run()
    for i in results:
        for j in range(3):
            for url, name in zip(i["url"][j], i["name"][j]):
                data["grade"].append(i["grade"])
                data["name"].append(name)
                data["content"].append(url)
                data["semester"].append(i["semester"])
                data["category"].append(j)
                data["version"].append(version)
                data["executor"].append(executor)
                data["needUncompress"].append(needUncompress)

# 存储爬取的信息
df = pd.DataFrame(data)
path = "./results/good_ke_jian.csv"
df.to_csv(path)
# 去除重复行
df = drop_duplicates(path)
df.to_csv("../results/final_good_ke_jian.csv", index=False)  # 保存取出重复行的文件
