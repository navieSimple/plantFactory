import pika
import json

def callback(ch, method, properties, body):
    dic = {}
    dic=json.loads(body)
    print dic
    
connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost',5672,'/'))
channel = connection.channel()
channel.queue_declare(queue='pf_up')
channel.basic_consume(callback, queue='pf_up', no_ack=True)
channel.start_consuming()