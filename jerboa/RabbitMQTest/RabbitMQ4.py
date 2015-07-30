# encoding=utf8
'''
Created on 2015年7月29日

@author: admin
'''
import pika
import sys
import time


def publish():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    # virtual_host 必须和用户密码一起使用
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',virtual_host="%2fonline"))
    channel = connection.channel()
    # 定义交换机，设置类型为direct
#     channel.exchange_delete("messages")
    channel.exchange_declare(exchange='messages', type='direct')
    result = channel.queue_declare(exclusive=True)
#     channel.queue_declare(queue='message_info', durable=True)  #持久化队列
    channel.queue_delete(queue='message_info')
    channel.queue_bind(exchange='messages',
                           queue=result.method.queue,
                           routing_key="info")
    
    # 定义三个路由键
    routings = ['info', 'warning', 'error']
     
    # 将消息依次发送到交换机，并设置路由键
    for routing in routings:
        message = '%s message.' % routing
        channel.basic_publish(exchange='messages',
                              routing_key=routing,
                              body=message)
        print message
    time.sleep(500)
    connection.close()

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)

def receive():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
     
    # 定义交换机，设置类型为direct
    channel.exchange_declare(exchange='messages', type='direct')
     
    # 从命令行获取路由键参数，如果没有，则设置为info
    routings = sys.argv[1:]
    if not routings:
        routings = ['info']
     
    # 生成临时队列，并绑定到交换机上，设置路由键
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    for routing in routings:
        channel.queue_bind(exchange='messages',
                           queue=queue_name,
                           routing_key=routing)
     
     
    channel.basic_consume(callback, queue=queue_name, no_ack=True)
     
    print ' [*] Waiting for messages. To exit press CTRL+C'
    channel.start_consuming()

if __name__ == '__main__':
    publish()
#     receive()
