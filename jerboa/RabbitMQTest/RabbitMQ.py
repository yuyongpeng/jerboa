# encoding=utf8
'''
Created on 2015年7月29日

@author: admin
'''
import pika

def publish():
    '''
    发布消息
    @param param: 
    '''
    conParam = pika.ConnectionParameters(host="localhost")
    connection = pika.BlockingConnection(conParam)
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
    print " [x] Sent 'Hello World!'"
    connection.close()
    
def callback(ch, method, properties, body):
    '''
    消费者 处理函数
    '''
    print " [x] receive %r " % body
    
def receive():
    '''
    接收消息
    '''
    conParam = pika.ConnectionParameters(host="localhost")
    connection = pika.BlockingConnection(conParam)
    channel = connection.channel()
    channel.queue_declare(queue="hello")
    print ' [*] Waiting for messages. To exit press CTRL+C'
    channel.basic_consume(callback,queue="hello",no_ack=True)
    channel.start_consuming()

    
if __name__ == '__main__':
    publish()
#     receive()
    
    
    
    