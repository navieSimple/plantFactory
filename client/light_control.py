#!/usr/bin/env python
#coding=utf-8

import global_list
import config_parse
import logging
import time
import trade_client
import RPi.GPIO as GPIO


layer_1_light_valve = 18
layer_2_light_valve = 23
layer_3_light_valve = 25
layer_4_light_valve = 12
layer_5_light_valve = 16
layer_6_light_valve = 20

send_state_data = {"fun_ID": "13", "collector_ID": "", "layer_ID": "", "light_on_off_state": ""}
#send_m_state_data = {"fun_ID": "03", "collector_ID": "", "layer_ID": "", "light_on_off_state": ""}

'''
def light_auto_control(): #自动控灯
    while True:
        currenttime = time.localtime()
        hour_str = "%02d"%(currenttime[3])
        min_str = "%02d"%(currenttime[4])
        time_str = hour_str +  min_str
        collector_id = global_list.collector_ID
        for i in range(0, global_list.layer_counts):
            layer_light_mode = global_list.light_attr[i]["mode"]
            if layer_light_mode == 1:
                logging.info('第%d层为自动模式!', i+1)
                layer_light_status = global_list.light_attr[i]["state"]  # 当前架子层灯的状态--0-off，1-on
                if layer_light_status == 0:  # 判断灯的状态
                    logging.info("第%d层灯状态为关闭", i+1)
                    if time_str >= global_list.light_attr[i]["scheme"]["openTime"] and \
                                    time_str < global_list.light_attr[i]["scheme"]["closeTime"]:
                        open_light(i + 1)  # 开灯
                        update_light_state(i + 1, 1)  # 设置状态为开
                        send_state_data["collector_ID"] = collector_id
                        send_state_data["layer_ID"] = str(i + 1)
                        send_state_data["light_on_off_state"] = "1"
                        json_data = json_client.json_encode(send_state_data)
                        global_list.g_queue_send.put(json_data)
                    else:
                        logging.info("开灯时间未到，等待...")
                        #time.sleep(1)
                        continue
                else:
                    logging.info("第%d层灯状态为开启", i+1)
                    if time_str < global_list.light_attr[i]["scheme"]["openTime"] or time_str >= global_list.light_attr[i]["scheme"]["closeTime"]:
                        close_light(i + 1)  # 关灯
                        update_light_state(i + 1, 0)  # 设置状态为关
                        send_state_data["collector_ID"] = collector_id
                        send_state_data["layer_ID"] = str(i + 1)
                        send_state_data["light_on_off_state"] = "0"
                        json_data = json_client.json_encode(send_state_data)
                        global_list.g_queue_send.put(json_data)
                    else:
                        logging.info("关灯时间未到，等待...")
                        #time.sleep(1)
                        continue
            else:
                logging.info("第%d层为手动模式", i+1)
        time.sleep(1)
'''


def light_auto_control(): #自动控灯
    flag_list = []
    for i in range(0, global_list.layer_counts):
        flag_list.append(-1)
    while True:
        currenttime = time.localtime()
        hour_str = "%02d"%(currenttime[3])
        min_str = "%02d"%(currenttime[4])
        time_str = hour_str +  min_str
        collector_id = global_list.collector_ID
        for i in range(0, global_list.layer_counts):
            layer_light_mode = global_list.light_attr[i]["mode"]
            if layer_light_mode == 1:
                logging.info('第%d层为自动模式!', i+1)
                if time_str >= global_list.light_attr[i]["scheme"]["openTime"] and \
                                time_str < global_list.light_attr[i]["scheme"]["closeTime"]:
                    if flag_list[i] != 0:
                        logging.info("第%d层应开灯，开灯", i+1)
                        open_light(i + 1)  # 开灯
                        update_light_state(i + 1, 1)  # 设置状态为开
                        send_state_data["collector_ID"] = collector_id
                        send_state_data["layer_ID"] = str(i + 1)
                        send_state_data["light_on_off_state"] = "1"
                        trade_client.send_message(send_state_data)
                        flag_list[i] = 0
                else:
                    if flag_list[i] != 1:
                        logging.info("第%d层应关灯，关灯", i + 1)
                        close_light(i + 1)  # 关灯
                        update_light_state(i + 1, 0)  # 设置状态为关
                        send_state_data["collector_ID"] = collector_id
                        send_state_data["layer_ID"] = str(i + 1)
                        send_state_data["light_on_off_state"] = "0"
                        trade_client.send_message(send_state_data)
                        flag_list[i] = 1
            else:
                logging.info("第%d层为手动模式", i+1)
        time.sleep(10)



def light_munual_open(layer): #单层手动控开灯
    collector_id = global_list.collector_ID
    layer_light_status = global_list.light_attr[layer-1]["state"]  # 当前架子层灯的状态--0-off，1-on
    if layer_light_status == 0:  # 判断灯的状态
        logging.info("当前灯是处于灭的状态")
        open_light(layer)  # 开灯
        update_light_state(layer, 1)  # 设置状态为开
        '''
     向服务端发送数据库更新请求：层运行状态为开启 
        send_m_state_data["collector_ID"] = collector_id
        send_m_state_data["layer_ID"] = str(layer)
        send_m_state_data["light_on_off"] = "1"
        json_data = json_client.json_encode(send_m_state_data)
        global_list.g_queue_send.put(json_data)
        '''
    else:
        logging.info("当前灯是处于开的状态")
        #open_light(layer)  # 开灯

def light_munual_close(layer): #单层手动关灯
    collector_id = global_list.collector_ID
    layer_light_status = global_list.light_attr[layer-1]["state"]  # 当前架子层灯的状态--0-off，1-on
    if layer_light_status == 0:  # 判断灯的状态
        logging.info("当前灯是处于灭的状态")
        #close_light(layer)  # 关灯
    else:
        logging.info("当前灯是处于开的状态")
        close_light(layer)  # 关灯
        update_light_state(layer, 0)
        '''
     向服务端发送数据库更新请求：层运行状态为关闭 
        send_m_state_data["collector_ID"] = collector_id
        send_m_state_data["layer_ID"] = str(layer)
        send_m_state_data["light_on_off"] = "0"
        json_data = json_client.json_encode(send_m_state_data)
        global_list.g_queue_send.put(json_data)
        '''

def ini_light():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(layer_1_light_valve, GPIO.OUT)
    GPIO.setup(layer_2_light_valve, GPIO.OUT)
    GPIO.setup(layer_3_light_valve, GPIO.OUT)
    GPIO.setup(layer_4_light_valve, GPIO.OUT)
    GPIO.setup(layer_5_light_valve, GPIO.OUT)
    GPIO.setup(layer_6_light_valve, GPIO.OUT)

    GPIO.output(layer_1_light_valve, False)
    GPIO.output(layer_2_light_valve, False)
    GPIO.output(layer_3_light_valve, False)
    GPIO.output(layer_4_light_valve, False)
    GPIO.output(layer_5_light_valve, False)
    GPIO.output(layer_6_light_valve, False)

    for i in range(0, global_list.layer_counts):
        layer_light_status = global_list.light_attr[i]["state"]
        if layer_light_status== 0:  # 判断灯的状态
            logging.info("当前灯是处于灭的状态")
            close_light(i+1)  # 关灯
        else:
            logging.info("当前灯是处于灭的状态")
            open_light(i+1)  # 开灯




def open_light(layer):
    logging.info("开第[%d]层灯", layer)
    if layer == 1:
        GPIO.output(layer_1_light_valve, True)
    elif layer == 2 :
        GPIO.output(layer_2_light_valve, True)
    elif layer == 3 :
        GPIO.output(layer_3_light_valve, True)
    elif layer == 4 :
        GPIO.output(layer_4_light_valve, True)
    elif layer == 5 :
        GPIO.output(layer_5_light_valve, True)
    elif layer == 6 :
        GPIO.output(layer_6_light_valve, True)
    else:
        logging.info('layer is error!')


def close_light(layer):
    logging.info("关第[%d]层灯", layer)
    if layer == 1 :
        GPIO.output(layer_1_light_valve, False)
    elif layer == 2 :
        GPIO.output(layer_2_light_valve, False)
    elif layer == 3 :
        GPIO.output(layer_3_light_valve, False)
    elif layer == 4 :
        GPIO.output(layer_4_light_valve, False)
    elif layer == 5 :
        GPIO.output(layer_5_light_valve, False)
    elif layer == 6 :
        GPIO.output(layer_6_light_valve, False)
    else:
        logging.info('layer is error!')
'''
def light_control_mode():
    collector_id = global_list.collector_ID
    layer_light_mode = global_list.light_attr[i]["mode"]
    if layer_light_mode == 1:
        logging.info('进入自动模式!')
        light_auto_control()

    else:
        logging.info('进入手动模式!')
        light_munual_control()
'''


def update_light_state(layer, state):
    config_parse.update_light_state(layer, state)
    global_list.light_attr[layer - 1]['state'] = state
