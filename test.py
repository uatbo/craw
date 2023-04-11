import pandas


path = "./results/good_ke_jian.csv"
data = pandas.read_csv(path, index_col=0)
print(data)
df = data.drop_duplicates()
df.to_csv("./results/abc.csv", index=False)
