#!/usr/bin/env python
#coding=utf-8

import socket
import time
import global_list
import threading
#import sys
#import Queue
import logging
#import trade_client
# create the send and recieve queues
#queue_recv = Queue.Queue()
#queue_send = Queue.Queue()

# read configure file to initialize global variables
def read_configure_file():
    pass    

# open threads
def open_threads():
    global_list.threads = []
    t1 = threading.Thread(target=thread_recv)
    global_list.threads.append(t1)
    t2 = threading.Thread(target=thread_send)
    global_list.threads.append(t2)
    '''
    t3 = threading.Thread(target=trade_client.thread_trade)
    global_list.threads.append(t3)
    if global_list.collector_zone_parameters ==0:
        t4 = threading.Thread(target=trade_client.thread_light)
        global_list.threads.append(t4)
        if global_list.zone == 0:
            t5 = threading.Thread(target=trade_client.thread_watercycle_growthzone)
            global_list.threads.append(t5)
        else:
            t5 = threading.Thread(target=trade_client.thread_watercycle_nurseryzone)
            global_list.threads.append(t5)
    '''        
        #open all threads
    for t in global_list.threads:
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
                
            break  
        except Exception,e:
            global_list.TCP_link_is_OK = 0
            logging.info(e.message)
            logging.info("Can't connect to server, try it latter!")
            #print("Can't connect to server, try it latter!")
            time.sleep(1)
            continue
        
    logging.info('Connect to server @ %s:%d...',global_list.SERVER_IP, global_list.SERVER_PORT)    
    #print("Connection success...")
    logging.info('Connection success...')

def thread_recv():
    while True:
        data = global_list.socket_tcp.recv(global_list.RcvData_MAX_len)
        if len(data)>0:
            logging.info('Received data: %s',data)
            global_list.g_queue_recv.put(data)
        
def thread_send():
    while True:
        while not global_list.g_queue_send.empty():
            data = global_list.g_queue_send.get()
            global_list.socket_tcp.sendall(data)
            logging.info('Sent data: %s',data)
  