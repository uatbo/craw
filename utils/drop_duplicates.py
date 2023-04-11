import pandas


def drop_duplicates(path):
    data = pandas.read_csv(path, index_col=0)
    data = data.drop_duplicates()  # 去除重复行，因为爬取的到的数据可能会有相同的
    return data
