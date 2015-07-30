# encoding=utf8
'''
Created on 2015年7月29日

@author: admin
'''
import pika

    
def publish() :
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
     
    #定义交换机  广播
    channel.exchange_declare(exchange='messages', type='fanout')
     
    #将消息发送到交换机
    # basic_publish方法的参数exchange被设定为相应交换机，因为是要广播出去，发送到所有队列，所以routing_key就不需要设定了。
    channel.basic_publish(exchange='messages', routing_key='', body='Hello World!')
    print " [x] Sent 'Hello World!'"
    connection.close()
    
    
def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    
def receive():    
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    #定义交换机  fanout：转发消息到所有绑定队列  
    channel.exchange_declare(exchange='messages', type='fanout')
    '''
    #随机生成队列，并绑定到交换机上
    #queue_declare的参数exclusive=True表示当接收端退出时，销毁临时产生的队列，这样就不会占用资源
    '''
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='messages', queue=queue_name)
    channel.basic_consume(callback, queue=queue_name, no_ack=True)
    print ' [*] Waiting for messages. To exit press CTRL+C'
    channel.start_consuming() 

if __name__=="__main__":
    publish()
#     receive()