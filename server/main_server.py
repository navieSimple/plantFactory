#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   cold
#   E-mail  :   wh_linux@126.com
#   Date    :   13/04/15 15:08:51
#   Desc    :   Tornado Echo Server
#   HOME    :   http://www.linuxzen.com
#
import Queue
import socket
import pika
import threading
import json
import trade_server
import global_list
import logging
import my_log
import struct

from functools import partial

from tornado.ioloop import IOLoop

my_log.log_conf()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setblocking(0)  # 将socket设置为非阻塞

server_address = ("", 50013)

sock.bind(server_address)
sock.listen(20)

fd_map = {}  # 文件描述符fd到socket的映射(fd is key;socket is value)

uid_fd = {}  # uid(collector_ID)到文件描述符fd的映射(collector_ID is key; fd is value)

fd = sock.fileno()
fd_map[fd] = sock

trade_server.mysql_conn()  # connect database mysql

global_list.ioloop = IOLoop.instance()


# 'body' is from the queue of rabbitmq,and then send the 'body' to client
def callback(ch, method, properties, body):
    try:
        dic = {}
        dic = json.loads(body)
        uid = dic['collector_ID']
        logging.info(uid_fd)
        logging.info(uid)
        if uid_fd:
            if uid_fd[uid]:
                fd = uid_fd[uid]
                s = fd_map[fd]
                logging.info(dic)
                # send the data of function ID= '03','04','05','06','07','08','09','12';
                # '03': on or off the light
                # '04':set light time scheme about on or off
                # '05':set water cycle scheme abot on or off in the growth zone
                # '06':the water cycle of certain layer start or quit auto mode in the growth zone
                # '07':set water cycle scheme abot on or off in the nursery zone
                # '08':the water cycle of certain layer start or quit auto mode in the nursery zone
                # '09':the water cycle of certain layer on or off by manual mode in the nursery zone
                # '12': the light of the layer start or quit auto mode
                global_list.ioloop.update_handler(fd, IOLoop.WRITE)
                global_list.message_queue_map[s].put(body)
            else:
                pass
        else:
            logging.error('collecotr ID got is error!')
    except Exception as e:
        logging.error('collecotr ID got is error!')


connection = pika.BlockingConnection(pika.ConnectionParameters(
    'localhost', 5672, '/'))
channel = connection.channel()
channel.queue_declare(queue=global_list.consume_queue_name)
channel.basic_consume(callback, queue=global_list.consume_queue_name, no_ack=True)
# channel.start_consuming()

# send data to leading end
# global_list.conn_leadingend = pika.BlockingConnection(pika.ConnectionParameters(
#               'localhost',5672,'/'))
global_list.channel_leadingend = connection.channel()
global_list.channel_leadingend.queue_declare(queue=global_list.publish_queue_name)


# global_list.channel_leadingend.basic_publish(exchange='', routing_key='hello', body='Hello World!')


def rabbit_consuming():
    print ' [*] Waiting for messages. To exit press CTRL+C'
    channel.start_consuming()


t = threading.Thread(target=rabbit_consuming)
t.start()

read_head = 0  # 0--head 1--body
read_len = 0  # 用于非阻塞socket处理半包问题
data = ""

def clean_action(fd):
    s = fd_map[fd]
    s.close()
    del fd_map[fd]
    for k in uid_fd.keys():
        if uid_fd[k] == fd:
            del uid_fd[k]
    del global_list.message_queue_map[s]

def handle_client(cli_addr, fd, event):
    s = fd_map[fd]
    if event & IOLoop.READ:
        # data = s.recv(2048)
        # logging.info(data)
        global read_head
        global read_len
        global data
        if read_head == 0:  # read head
            head_struct = s.recv(4)
            if not head_struct:
                logging.info("closing %s", cli_addr)
                # print "     closing %s" % cli_addr
                global_list.ioloop.remove_handler(fd)
                clean_action(fd)
                return
            read_head = 1
            read_len = struct.unpack('i', head_struct)[0]
            logging.info('Received head data. body_len: %d', read_len)
            if read_len > global_list.g_msg_len_max:
                logging.error("msg too long!")
                global_list.ioloop.remove_handler(fd)
                clean_action(fd)
                read_head = 0
                return
            data = ""
        if read_head == 1:  # read body
            recv_data = s.recv(read_len)
            if len(recv_data) < read_len:
                read_len = read_len - len(recv_data)
            else:
                read_head = 0
            data = data + recv_data
        #logging.info('Received data: %s', data)
        if read_head == 1: #body
            return
        logging.info('Received data. len: %d', len(data))
        if data:
            try:
                # print "     received '%s' from %s" % (data, cli_addr)
                dic = {}
                # dic=json.loads(data)
                dic = json.loads(data)
                uid = dic['collector_ID']
                uid_fd[uid] = fd
            except:
                logging.info("closing %s", cli_addr)
                # print "     closing %s" % cli_addr
                global_list.ioloop.remove_handler(fd)
                clean_action(fd)
                read_head = 0
            #print "     received '%s' from %s,%s" % (data, uid, cli_addr)
            print "     received data_len %d from %s,%s" % (len(data), uid, cli_addr)
            # 接收到消息更改事件为写, 用于发送数据到对端
            # ioloop.update_handler(fd, IOLoop.WRITE)
            # message_queue_map[s].put(data)
            print dic['fun_ID']
            if dic['fun_ID'] == '00':  # heart jump process
                # json_data = json.dumps(dic)
                global_list.ioloop.update_handler(fd, IOLoop.WRITE)
                global_list.message_queue_map[s].put(json.dumps(dic))
                # message_queue_map[s].put(json_data)
                # s.send(json_data)

            elif dic['fun_ID'] == '010':  # get the number of layer
                logging.info('processing fun_ID = 010')
                dic_1 = {}
                dic_1 = trade_server.get_layernum(dic)
                global_list.ioloop.update_handler(fd, IOLoop.WRITE)
                global_list.message_queue_map[s].put(json.dumps(dic_1))
                logging.info('fun_ID = 010 has been finished')

            elif dic['fun_ID'] == '011':  # update the scheme about on or off light time
                logging.info('processing fun_ID = 011')
                dic_1 = {}
                dic_1 = trade_server.update_lighttime_scheme(dic)
                global_list.ioloop.update_handler(fd, IOLoop.WRITE)
                global_list.message_queue_map[s].put(json.dumps(dic_1))
                logging.info('fun_ID = 011 has been finished')

            elif dic['fun_ID'] == '012':  # update the scheme about on or off water cycle in the growth zone
                logging.info('processing fun_ID = 012')
                dic_1 = {}
                dic_1 = trade_server.update_watercycle_scheme_growthzone(dic)
                global_list.ioloop.update_handler(fd, IOLoop.WRITE)
                global_list.message_queue_map[s].put(json.dumps(dic_1))
                logging.info('fun_ID = 012 has been finished')

            elif dic['fun_ID'] == '013':  # update the scheme about on or off water cycle in the nursery zone
                logging.info('processing fun_ID = 013')
                dic_1 = {}
                dic_1 = trade_server.update_watercycle_scheme_nurseryzone(dic)
                global_list.ioloop.update_handler(fd, IOLoop.WRITE)
                global_list.message_queue_map[s].put(json.dumps(dic_1))
                logging.info('fun_ID = 013 has been finished')

            elif dic['fun_ID'] == '02':  # environment parameters of the zone
                logging.info('processing fun_ID = 02')
                dic_1 = {}
                dic_1 = trade_server.zone_environment_parameters(dic)
                global_list.ioloop.update_handler(fd, IOLoop.WRITE)
                global_list.message_queue_map[s].put(json.dumps(dic_1))
                logging.info('fun_ID = 02 has been finished')

            elif dic['fun_ID'] == '10':  # shelf parameters
                logging.info('processing fun_ID = 10')
                dic_1 = {}
                dic_1 = trade_server.shelf_parameters(dic)
                global_list.ioloop.update_handler(fd, IOLoop.WRITE)
                global_list.message_queue_map[s].put(json.dumps(dic_1))
                logging.info('fun_ID = 10 has been finished')

            elif dic['fun_ID'] == '11':  # layer parameters
                logging.info('processing fun_ID = 11')
                dic_1 = {}
                dic_1 = trade_server.layer_parameters(dic)
                global_list.ioloop.update_handler(fd, IOLoop.WRITE)
                global_list.message_queue_map[s].put(json.dumps(dic_1))
                logging.info('fun_ID = 11 has been finished')

            elif dic['fun_ID'] == '12':  # the light of the layer start or quit auto mode
                logging.info('processing fun_ID = 12')
                trade_server.light_mode(dic)
                global_list.channel_leadingend.basic_publish(exchange='', routing_key=global_list.publish_queue_name,
                                                             body=json.dumps(dic))
                logging.info('fun_ID = 12 has been finished')

            elif dic['fun_ID'] == '13':  # update light state when it is time out
                logging.info('processing fun_ID = 13')
                dic_1 = {}
                dic_1 = trade_server.update_light_state(dic)
                global_list.ioloop.update_handler(fd, IOLoop.WRITE)
                global_list.message_queue_map[s].put(json.dumps(dic_1))
                logging.info('fun_ID = 13 has been finished')

            elif dic['fun_ID'] == '03':  # process the light on or off
                logging.info('processing fun_ID = 03')
                trade_server.light_on_off_process(dic)
                global_list.channel_leadingend.basic_publish(exchange='', routing_key=global_list.publish_queue_name,
                                                             body=json.dumps(dic))
                logging.info('fun_ID = 03 has been finished')
                # global_list.channel_leadingend.basic_publish(exchange='', routing_key='up', body=json.dumps(dic))


            elif dic['fun_ID']=='04': #set light time scheme about on or off
                logging.info('processing fun_ID = 04')
                global_list.channel_leadingend.basic_publish(exchange='', routing_key=global_list.publish_queue_name,
                                                             body=json.dumps(dic))
                logging.info('fun_ID = 04 has been finished')

            elif dic['fun_ID']=='05':
                logging.info('processing fun_ID = 05')
                global_list.channel_leadingend.basic_publish(exchange='', routing_key=global_list.publish_queue_name,
                                                             body=json.dumps(dic))
                logging.info('fun_ID = 05 has been finished')

            elif dic['fun_ID'] == '06':  # the water cycle of certain layer start or quit auto mode in the growth zone
                logging.info('processing fun_ID = 06')
                trade_server.layer_watercyle_mode_growthzone(dic)
                global_list.channel_leadingend.basic_publish(exchange='', routing_key=global_list.publish_queue_name,
                                                             body=json.dumps(dic))
                logging.info('fun_ID = 06 has been finished')

            elif dic['fun_ID']=='07':
                logging.info('processing fun_ID = 07')
                global_list.channel_leadingend.basic_publish(exchange='', routing_key=global_list.publish_queue_name,
                                                             body=json.dumps(dic))
                logging.info('fun_ID = 07 has been finished')

            elif dic['fun_ID'] == '08':  # the water cycle of certain layer start or quit auto mode in the nursery zone
                logging.info('processing fun_ID = 08')
                trade_server.layer_watercyle_mode_nurseryzone(dic)
                global_list.channel_leadingend.basic_publish(exchange='', routing_key=global_list.publish_queue_name,
                                                             body=json.dumps(dic))
                logging.info('fun_ID = 08 has been finished')

            elif dic['fun_ID'] == '09':  # the water cycle of certain layer on or off by manual mode in the nursery zone
                logging.info('processing fun_ID = 09')
                trade_server.layer_watercyle_onoff_manual_nurseryzone(dic)
                global_list.channel_leadingend.basic_publish(exchange='', routing_key=global_list.publish_queue_name,
                                                             body=json.dumps(dic))
                logging.info('fun_ID = 09 has been finished')

            elif dic['fun_ID'] == '14':  # update water cycle state when it is doing
                logging.info('processing fun_ID = 14')
                dic_1 = {}
                dic_1 = trade_server.update_watercycle_state(dic)
                global_list.ioloop.update_handler(fd, IOLoop.WRITE)
                global_list.message_queue_map[s].put(json.dumps(dic_1))
                logging.info('fun_ID = 14 has been finished')
            elif dic['fun_ID'] == '15':  # position camera cature
                logging.info('processing fun_ID = 15')
                trade_server.process_position_camera_capture(dic)
                dic_1 = {'fun_ID': '15', 'position_ID': dic['position_ID']}
                global_list.ioloop.update_handler(fd, IOLoop.WRITE)
                global_list.message_queue_map[s].put(json.dumps(dic_1))
                logging.info('fun_ID = 15 has been finished')
            else:
                # ioloop.update_handler(fd, IOLoop.WRITE)
                # message_queue_map[s].put(data)
                logging.error('trade process error happened......')

        else:
            logging.info("closing %s", cli_addr)
            # print "     closing %s" % cli_addr
            global_list.ioloop.remove_handler(fd)
            clean_action(fd)
            read_head = 0

    if event & IOLoop.WRITE:
        try:
            next_msg = global_list.message_queue_map[s].get_nowait()
        except Queue.Empty:
            print "%s queue empty" % cli_addr
            global_list.ioloop.update_handler(fd, IOLoop.READ)
        else:
            print 'sending "%s" to %s' % (next_msg, cli_addr)
            data_len = len(next_msg)
            struct1 = struct.pack('i', data_len)
            send_data = struct1 + next_msg
            logging.info('Sent data_len: %d  data: %s', data_len, next_msg)
            s.send(send_data)

    if event & IOLoop.ERROR:
        # print " exception on %s" % cli_addr
        logging.error(" exception on %s", cli_addr)
        global_list.ioloop.remove_handler(fd)
        clean_action(fd)
        read_head = 0


def handle_server(fd, event):
    s = fd_map[fd]
    if event & IOLoop.READ:
        conn, cli_addr = s.accept()
        logging.info("     connection %s", cli_addr[0])
        # print "     connection %s" % cli_addr[0]
        conn.setblocking(0)
        conn_fd = conn.fileno()
        fd_map[conn_fd] = conn
        handle = partial(handle_client, cli_addr[0])  # 将cli_addr作为第一个参数
        # 将连接和handle注册为读事件加入到 tornado ioloop
        global_list.ioloop.add_handler(conn_fd, handle, IOLoop.READ)
        global_list.message_queue_map[conn] = Queue.Queue()  # 创建对应的消息队列


def startIoLoop():
    print "start IoLoop"
    global_list.ioloop.add_handler(fd, handle_server, IOLoop.READ)
    global_list.ioloop.start()


t2 = threading.Thread(target=startIoLoop)
t2.start()
