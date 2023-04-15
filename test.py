# import yaml
#
# sinfo = {
#     "grade": ["三年级", "四年级"],
#     "semester": ["上册", "下册"],
#     "version": ["北京版", "北师大版", "苏教版", "人教版"],
# }
#
#
# # 将字典写入 UTF-8 编码的 YAML 文件
# with open('./configs/zxx_edu_cn.yml', 'w', encoding='utf-8') as file:
#     yaml.dump(sinfo, file, allow_unicode=True)
#
# # 从 YAML 文件中读取数据
# with open('./configs/zxx_edu_cn.yml', 'r', encoding='utf-8') as file:
#     info = yaml.safe_load(file)
#
# # 打印读取的数据
# print(type(info))

# import yaml
#
# sinfo = [
#     ["三年级", "北京版", "上册"],
#     ["三年级", "北京版", "下册"],
#     ["三年级", "北师大版", "下册"],
#     ["三年级", "苏教版", "上册"],
#     ["三年级", "苏教版", "下册"],
#     ["三年级", "人教版", "上册"],
#     ["三年级", "人教版", "下册"],
#     ["四年级", "北京版", "上册"],
#     ["四年级", "北京版", "下册"],
#     ["四年级", "北师大版", "下册"],
#     ["四年级", "苏教版", "上册"],
#     ["四年级", "苏教版", "下册"],
#     ["四年级", "人教版", "上册"],
#     ["四年级", "人教版", "下册"]
# ]
#
# # 将列表保存为 YAML 文件
# with open('./configs/zxx_edu_cn.yml', 'w', encoding='utf-8') as file:
#     yaml.dump(sinfo, file, allow_unicode=True)
#
#
#
#
# # 从 YAML 文件中读取数据
# with open('./configs/zxx_edu_cn.yml', 'r', encoding='utf-8') as file:
#     info = yaml.safe_load(file)
#
# # 打印读取的数据
# print(info)

# sinfo = [
#     ["三年级", "北京版", "上册"],
#     ["三年级", "北京版", "下册"],
#     ["三年级", "北师大版", "下册"],
#     ["三年级", "苏教版", "上册"],
#     ["三年级", "苏教版", "下册"],
#     ["三年级", "人教版", "上册"],
#     ["三年级", "人教版", "下册"],
#     ["四年级", "北京版", "上册"],
#     ["四年级", "北京版", "下册"],
#     ["四年级", "北师大版", "下册"],
#     ["四年级", "苏教版", "上册"],
#     ["四年级", "苏教版", "下册"],
#     ["四年级", "人教版", "上册"],
#     ["四年级", "人教版", "下册"]
# ]
# info = {
#     "grade": None,
#     "semester": None,
#     "version": None
# }
#
# while(len(sinfo) != 0):
#     info["grade"] = sinfo[0][0]
#     info["version"] = sinfo[0][1]
#     info["semester"] = sinfo[0][2]
#
#     print(sinfo[0])
#     sinfo.pop(0)
#
# my_list = [1, 2, 3, 4, 5]
#
# # 从尾部开始遍历列表
# for i in range(len(my_list)-1, -1, -1):
#     print(my_list[i])
my_list = [1, 2, 3, 4, 5]

# 删除列表尾部的元素
my_list.pop()

# 打印删除后的列表
print(my_list)
