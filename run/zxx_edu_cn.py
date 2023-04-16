import yaml
import pandas as pd
from parsers.zxx_edu_cn import zxx_edu_cn_parser


def run():
    driverfile_path = "C:/Users/uatbo/Desktop/msedgedriver.exe"
    request = zxx_edu_cn_parser(driverfile_path=driverfile_path)
    try:
        request.get_video_url()
    except Exception:
        # 将列表保存为 YAML 文件
        with open('../configs/zxx_edu_cn.yml', 'w', encoding='utf-8') as file:
            yaml.dump(request.sinfo, file, allow_unicode=True)
        # 清除不完整的数据
        while (True):
            if request.data["grade"][-1] == request.sinfo[0][0] and request.data["version"][-1] == request.sinfo[0][1] and request.data["semester"][-1] == request.sinfo[0][2]:
                request.data["grade"].pop()
                request.data["semester"].pop()
                request.data["category"].pop()
                request.data["version"].pop()
                request.data["executor"].pop()
                request.data["chapter"].pop()
                request.data["section"].pop()
                request.data["name"].pop()
                request.data["content"].pop()
                # 如果为空了要跳出循环
                if len(request.data["grade"]) == 0:
                    break
            # 如果不为空，但是当前记录已经清空则跳出循环
            else:
                break
        print(Exception)


    # 存储爬取的信息
    df = pd.DataFrame(request.data)
    path = "../results/zxx_edu_cn.csv"
    df.to_csv(path, mode='a', index=False)


if __name__ == "__main__":
    run()
