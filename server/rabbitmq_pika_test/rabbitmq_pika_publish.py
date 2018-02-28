#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pika
import json

#on_off ={'fun_ID':'03','collector_ID':'231110001','shelf_ID':'10','layer_ID':'2','light_type':'0','light_on_off':'1'}
#time_set = {'fun_ID':'04','collector_ID':'231110001','shelf_ID':'10','layer_ID':'2', 'light_type':'0','start_time':'0820', 'end_time':'1768'}

#data_sent ={'fun_ID':'04','collector_ID':'231110012','layer_ID':'3','start_time':'0600', 'end_time':'1600'}
#data_sent ={'fun_ID':'03','collector_ID':'231110013','layer_ID':'3','light_on_off':'0'}
#data_sent ={'fun_ID':'12','collector_ID':'231110013','layer_ID':'3','light_mode':'0'}
#data_sent ={'fun_ID':'05','collector_ID':'231110017','layer_ID':'3','cycle_time':'125','waiting_time':'125'}
#data_sent ={'fun_ID':'06','collector_ID':'231110017','layer_ID':'3','cycle_mode':'0'}
data_sent ={'fun_ID':'07','collector_ID':'231110023','layer_ID':'1','timeout':'127','humi_min':'12','humi_max':'129'}
#data_sent ={'fun_ID':'08','collector_ID':'231110022','layer_ID':'2','cycle_mode':'0'}
#data_sent ={'fun_ID':'09','collector_ID':'231110022','layer_ID':'2','cycle_state':'0'}




connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost',5672,'/'))
channel = connection.channel()
channel.queue_declare(queue='pf_down')
 
channel.basic_publish(exchange='', routing_key='pf_down', body=json.dumps(data_sent))
