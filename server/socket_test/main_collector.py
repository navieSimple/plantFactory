#!/usr/bin/env python
#coding=utf-8

#import threading
#import time
import sys
#from threading import Timer

import socket_client
import logging
import my_log
import global_list
import json_client
#import trade_client
#import LEDandWaterpump 
#import test_log # for test log
#old_time = time.clock()
#i = 0
data_sent = {}
def send_data(data_sent):
    #data_sent['collector_ID'] = global_list.collector_ID
    sent = json_client.json_encode(data_sent)
    global_list.g_queue_send.put(sent)

'''
threads = []
t1 = threading.Thread(target=socket_client.thread_recv)
threads.append(t1)
t2 = threading.Thread(target=socket_client.thread_send)
threads.append(t2)
t3 = threading.Thread(target=trade_client.thread_trade)
threads.append(t3)
'''
if __name__=='__main__':
    try:
        
        # test the log codes
        #logging.info('this is test')
        #test_log.test_log();
        
        #socket_client.thread_recv(queue_rvc)
        
        #time.sleep(30)
        my_log.log_conf() 
        logging.info("client program start.........")
        #socket_client.read_configure_file()
        socket_client.connect_server()
        socket_client.open_threads()
        #socket_client.recv_send()
        #global_list.TCP_link_is_OK = 1 #1:link is OK; 0: link is broken      
        send_data(data_sent)
        '''
        #open all threads
        for t in threads:
            t.setDaemon(True)
            t.start()
        print '  threads is started   '
        '''    
        #if global_list.collector_zone_parameters == 0:
            #trade_client.update_data_sent()            
        #
        #logging.info('start ini_LED_waterdump')
        #LEDandWaterpump.ini_LED_waterdump()
        #logging.info('end ini_LED_waterdump')        
        #print '  LED AND waterpump is inilialiratin....   '
        #
        
        #get collectID AND shelf_ID AND the number of layer
        #logging.info('start get_shelfID_send')
        #trade_client.get_shelfID_send()  
        #time.sleep(3)        
        #logging.info('end get_shelfID_send')
        
        #update lamp status data
        #logging.info('start update_data_send')
        #trade_client.update_data_send()        
        #logging.info('end update_data_send')
        
        #start heart jump(include: send growth/nursery zone shelf/layer parameters)
        #logging.info('start heart_jump')
        #trade_client.heart_jump_sent()
        #logging.info('end heart_jump')
        #end start heart jump
        
        #open water dump for work
        #global_list.waterdump_timer = threading.Timer(global_list.waterdump_work_duration,trade_client.waterdump)
        #global_list.waterdump_timer.start()
        #logging.info('start waterdump')
        #trade_client.waterdump()
        #logging.info('end waterdump')
        #end water dump
        
        while True:
            '''
            if  global_list.TCP_link_is_OK == 0:                
                time.sleep(3)
                #logging.info(global_list.TCP_link_is_OK)
                if  global_list.TCP_link_is_OK == 0:
                    logging.info(global_list.TCP_link_is_OK)
                    #for t in global_list.threads:
                        #t.terminate()
                        #t.join()
                    global_list.socket_tcp.close()
                    #time.sleep(1)
                    socket_client.connect_server()
                    #global_list.TCP_link_is_OK = 1
                    time.sleep(1)
                    #update data
                    if global_list.collector_zone_parameters == 0:
                        trade_client.update_data_sent()
            '''       
            #trade_client.check_start_end_time()
        # end test queue codes
    except Exception,e:
        logging.error('exited the system')
        logging.error(e.message)
        global_list.socket_tcp.close()
        sys.exit(1)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    