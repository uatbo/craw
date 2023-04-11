import pandas
import pika
import json
import time


# 文件路径
path = "../results/final_good_ke_jian.csv"

# 连接到RabbitMQ服务器
connection = pika.BlockingConnection(pika.ConnectionParameters('114.132.249.3', 5672, "/", pika.PlainCredentials("admin", "rabbitmlgbz0729")))
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

# # 发送课件
# for url, name in zip(url0, name0):
#     body = json.dumps(
#         {
#             "content": url,
#             "grade": j["grade"],
#             "name": name,
#             "semester": j["semester"],
#             "category": 0,
#             "version": self.version,
#             "executor": "段斌",
#             "needUncompress": 1
#         }
#     ).encode("utf-8")
#     # 向消息队列发送消息
#     channel.basic_publish(exchange='courseware_exchange', routing_key='hello', body=body)
#     print("Sent!")
#     time.sleep(0.5)
# # 发送教案
# for url, name in zip(url1, name1):
#     body = json.dumps(
#         {
#             "content": url,
#             "grade": j["grade"],
#             "name": name,
#             "semester": j["semester"],
#             "category": 1,
#             "version": self.version,
#             "executor": "段斌",
#             "needUncompress": 1
#         }
#     ).encode("utf-8")
#     # 向消息队列发送消息
#     channel.basic_publish(exchange='courseware_exchange', routing_key='hello', body=body)
#     print("Sent!")
#     time.sleep(0.5)
# # 发送试题
# for url, name in zip(url2, name2):
#     body = json.dumps(
#         {
#             "content": url,
#             "grade": j["grade"],
#             "name": name,
#             "semester": j["semester"],
#             "category": 2,
#             "version": self.version,
#             "executor": "段斌",
#             "needUncompress": 1
#         }
#     ).encode("utf-8")
#     # 向消息队列发送消息
#     channel.basic_publish(exchange='courseware_exchange', routing_key='hello', body=body)
#     print("Sent!")
#     time.sleep(0.5)




# class Q:
#     USERNAME = 'admin'
#     PASSWORD = 'rabbitmlgbz0729'
#     VIRTUAL_HOST = "/"
#     HOST = '114.132.249.3'
#     PORT = 5672
#
#
# class rabbitmq:
#
#     def __init__(self, connection_info=Q):
#         # 连接到RabbitMQ服务器
#         credentials = pika.PlainCredentials(connection_info.USERNAME, connection_info.PASSWORD)
#         parameters = pika.ConnectionParameters(connection_info.HOST, connection_info.PORT, connection_info.VIRTUAL_HOST,
#                                                credentials)
#         self.connection = pika.BlockingConnection(parameters)
#         self.channel = self.connection.channel()
#
#     def create_queue_exchange(self, queue, exchange):
#         # 创建消息队列，如果队列已存在则不会重复创建
#         self.channel.queue_declare(queue=queue)
#         self.channel.exchange_declare(exchange=exchange , exchange_type='fanout', durable=True, auto_delete=True)#
#
#     def publish(self, body):
#         # 向消息队列发送消息
#         self.channel.basic_publish(exchange='courseware_exchange', routing_key='', body=body)
#         print("Sent!")
#
#     def close(self):
#         self.connection.close()
#
#
# if __name__ == "__main__":
#     MyRabbitmq = rabbitmq()
#     MyRabbitmq.create_queue_exchange("courseware_queue", "courseware_exchange")
#
#     MyRabbitmq.publish(json.dumps(
#         {
#             "content": "hello",
#             "grade": 1,
#             "name": "课件test1",
#             "semester": 0,
#             "version": "北大版",
#             "executor": "段斌"
#         }
#     ))
#
#     MyRabbitmq.close()
