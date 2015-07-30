# encoding=utf8
'''
Created on 2015年7月29日

@author: admin
'''
import pika
import sys
import time


def publish():
    conParam= pika.ConnectionParameters(host="localhost")
    connection = pika.BlockingConnection(parameters=conParam)
    channel = connection.channel()
    channel.queue_declare(queue="task_queue",durable=True) #持久化队列
    message = "".join(sys.argv[1:]) or "hello world"
    properties = pika.BasicProperties(delivery_mode=2)  # 持久化消息
    channel.basic_publish(exchange="",routing_key="task_queue",body=message,properties=properties)
    print " [X] sent %r " % (message,)
    connection.close()

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    time.sleep( body.count('.') )
    print " [x] Done"
    ch.basic_ack(delivery_tag = method.delivery_tag)
    
def receive():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)  #持久化队列
    print ' [*] Waiting for messages. To exit press CTRL+C'
    '''
    basic_qos设置prefetch_count=1，使得rabbitmq不会在同一时间给工作者分配多个任务，即只有工作者完成任务之后，才会再次接收到任务。
    '''
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback,queue='task_queue',no_ack=False)
    channel.start_consuming()
    
if __name__ == '__main__':
    publish()
#     receive()