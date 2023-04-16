import pandas
import pika
import json
import time


# 发送好课件的资料
def good_ke_jian():
    # 文件路径
    path = "../results/final_good_ke_jian.csv"

    # 连接到RabbitMQ服务器
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('114.132.249.3', 5672, "/", pika.PlainCredentials("admin", "rabbitmlgbz0729")))
    channel = connection.channel()
    # 创建消息队列，如果队列已存在则不会重复创建
    channel.queue_declare(queue='courseware_queue')
    # 读取文件
    data = pandas.read_csv(path)
    # 发送到消息队列
    for i in range(2172, len(data)):
        body = json.dumps(
            {
                "content": data["content"][i],
                "grade": int(data["grade"][i]),
                "name": data["name"][i],
                "semester": int(data["semester"][i]),
                "category": int(data["category"][i]),
                "version": data["version"][i],
                "executor": data["executor"][i],
                "needUncompress": int(data["needUncompress"][i])
            }
        ).encode("utf-8")
        print(body)
        # 向消息队列发送消息
        channel.basic_publish(exchange='courseware_exchange', routing_key='hello', body=body)
        print("Sent!")
        time.sleep(0.5)

    # 关闭连接
    channel.close()


# 发送zxx.edu.cn的课例视频
def zxx_edu_cn():
    # 文件路径
    path = "../results/zxx_edu_cn.csv"

    # 连接到RabbitMQ服务器
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('114.132.249.3', 5672, "/", pika.PlainCredentials("admin", "rabbitmlgbz0729")))
    channel = connection.channel()
    # 创建消息队列，如果队列已存在则不会重复创建
    channel.queue_declare(queue='courseware_queue')
    # 读取文件
    data = pandas.read_csv(path)
    # 发送到消息队列
    for i in range(len(data)):
        if data["grade"][i] == "三年级":
            grade = 3
        else:
            grade = 4
        if data["semester"][i] == "上册":
            semester = 0
        else:
            semester = 1
        body = json.dumps(
            {
                "grade": grade,
                "semester": semester,
                "category": int(data["category"][i]),
                "version": data["version"][i],
                "executor": data["executor"][i],
                "chapter": int(data["chapter"][i]),
                "section": int(data["section"][i]),
                "name": data["name"][i],
                "content": data["content"][i],
            }
        ).encode("utf-8")
        print(body)
        # 向消息队列发送消息
        channel.basic_publish(exchange='courseware_exchange', routing_key='hello', body=body)
        print("Sent!")
        time.sleep(0.5)

    # 关闭连接
    channel.close()


if __name__ == "__main__":
    # good_ke_jian()
    zxx_edu_cn()
