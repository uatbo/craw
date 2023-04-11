# craw

craw 项目的一些说明

---

## 目录结构

```shell

├─parsers
│      good_ke_jian.py    # 好课件的解析器
│      __init__.py
│          
├─requests
│      good_ke_jian.py    # 好课件的请求器
│      __init__.py
│          
├─results
│      good_ke_jian.csv   # 好课件爬取的信息
│      
├─utils
│      rabbitmq.py  # 暂未实现，不要使用
│      __init__.py
│      
├─good_ke_jian.py  # 好课件的程序入口
├─main.py  # 暂无用处
├─README.md
└─test.py  # 暂无用处，可以用来写一些模块测试代码
```

## 环境配置

```shell
# Python版本：3.8
# 使用Anaconda包管理器
conda install --yes --file requirements.txt
```

## 使用到的库

解析：
beautifulsoup

请求：
urllib

消息队列：
pika

数据存储：
pandas
