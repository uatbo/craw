import pandas as pd
from parsers.zxx_edu_cn import zxx_edu_cn_parser


def run():
    driverfile_path = "D:/Files/Projects/msedgedriver.exe"
    request = zxx_edu_cn_parser(driverfile_path=driverfile_path)
    request.get_video_url()

    # 存储爬取的信息
    df = pd.DataFrame(request.data)
    path = "../results/zxx_edu_cn.csv"
    df.to_csv(path, index=False)


if __name__ == "__main__":
    run()