#!/usr/bin/env python
#coding=utf-8

import socket
import time
import global_list
import threading
#import sys
#import Queue
import logging
import trade_client
import struct
import os
# create the send and recieve queues
#queue_recv = Queue.Queue()
#queue_send = Queue.Queue()

def open_deal_threads():
    if global_list.collector_zone_parameters ==0: #架子嵌入式
        t1 = threading.Thread(target=trade_client.thread_light)
        global_list.deal_threads.append(t1)
        if global_list.zone == 0:   #栽培区
            t2 = threading.Thread(target=trade_client.thread_watercycle_growthzone)
            global_list.deal_threads.append(t2)
        else:   #育苗区
            t2 = threading.Thread(target=trade_client.thread_watercycle_nurseryzone)
            global_list.deal_threads.append(t2)
        t3 = threading.Thread(target=trade_client.shelf_collect_env) #架子及层环境采集
        global_list.deal_threads.append(t3)
        t4 = threading.Thread(target=trade_client.camera_cature) #摄像头拍照
        global_list.deal_threads.append(t4)
    else: #区域嵌入式
        t1 = threading.Thread(target=trade_client.zone_collect_env)
        global_list.deal_threads.append(t1)

    t5 = threading.Thread(target=trade_client.thread_trade)
    global_list.deal_threads.append(t5)

    for t in global_list.deal_threads:
        t.setDaemon(True)
        t.start()
            
# open threads
def open_socket_threads():
    global_list.socket_threads = []
    t1 = threading.Thread(target=thread_recv)
    global_list.socket_threads.append(t1)
    t2 = threading.Thread(target=thread_send)
    global_list.socket_threads.append(t2)
    for t in global_list.socket_threads:
        t.setDaemon(True)
        t.start()

# connect the server    
def connect_server():
    #print("Starting socket: TCP...")
    logging.info('Starting socket: TCP...')
    global_list.socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:  
        try:
            #print("Connecting to server @ %s:%d..." %(global_list.SERVER_IP, global_list.SERVER_PORT))           
            #logging.info("Connecting to server @ %s:%d...",global_list.SERVER_IP, global_list.SERVER_PORT)
            ret = global_list.socket_tcp.connect(global_list.server_addr)
            logging.info(ret)
            if ret ==None:
                global_list.TCP_link_is_OK = 1
                logging.info(global_list.TCP_link_is_OK)
                global_list.socket_state = True
                break
            time.sleep(1)
        except Exception as e:
            global_list.TCP_link_is_OK = 0
            global_list.socket_state = False
            logging.info(e.message)
            logging.info("Can't connect to server, try it latter!")
            #print("Can't connect to server, try it latter!")
            time.sleep(1)
            continue
        
    logging.info('Connect to server @ %s:%d...',global_list.SERVER_IP, global_list.SERVER_PORT)    
    #print("Connection success...")
    logging.info('Connection success...')

def thread_recv():
    while global_list.socket_state == True:
        try:
            head_struct = global_list.socket_tcp.recv(4)
            if not head_struct:
                #logging.error("Received head error!")
                time.sleep(0.1)
                continue
            head_len = struct.unpack('i', head_struct)[0]
            tmp = 0
            recv_data = ""
            while (tmp < head_len):
                recv_data = recv_data + global_list.socket_tcp.recv(head_len - tmp)
                tmp = tmp + len(recv_data)
            logging.info('Received data: %s',recv_data)
            global_list.g_queue_recv.put(recv_data)
        except Exception as e:
            #print(e)
            logging.error("Recv thread: Socket error!")
            time.sleep(0.1)
    logging.error("thread_recv exit... pid[%d]", os.getpid())

def thread_send():
    while global_list.socket_state == True:
        try:
            if global_list.g_queue_send.empty() == True:
                time.sleep(0.1)
                continue
            data = global_list.g_queue_send.get()
            data_len = len(data)
            struct1 = struct.pack('i', data_len)
            send_data = struct1 + data
            global_list.socket_tcp.sendall(send_data)
            #logging.info('Sent data_len: %d  data: %s', data_len, data)
            logging.info('Sent data_len: %d  ', data_len)
        except  Exception as e:
            #print(e)
            logging.error("Send thread: Socket error!")
            time.sleep(0.1)
    logging.error("thread_send exit...pid[%d]", os.getpid())