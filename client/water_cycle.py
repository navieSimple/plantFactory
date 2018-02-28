#!/usr/bin/env python
#coding=utf-8

import global_list
import config_parse
import logging
import time
import trade_client
import RPi.GPIO as GPIO

layer_1_solenoid_valve = 4
layer_2_solenoid_valve = 17
layer_3_solenoid_valve = 27
layer_4_solenoid_valve = 22
layer_5_solenoid_valve = 5
layer_6_solenoid_valve = 6
shelf_water_pump = 21
shelf_water_high = 19
shelf_water_low = 26

def init_and_reset_water_gpio():
    #初始化电池阀、水泵的开关信号输出及水位信号输入
    GPIO.setmode(GPIO.BCM)
    '''
    初始化gpio口
    '''
    GPIO.setup(layer_1_solenoid_valve, GPIO.OUT)
    GPIO.setup(layer_2_solenoid_valve, GPIO.OUT)
    GPIO.setup(layer_3_solenoid_valve, GPIO.OUT)
    GPIO.setup(layer_4_solenoid_valve, GPIO.OUT)
    GPIO.setup(layer_5_solenoid_valve, GPIO.OUT)
    GPIO.setup(layer_6_solenoid_valve, GPIO.OUT)
    GPIO.setup(shelf_water_pump, GPIO.OUT)
    GPIO.setup(shelf_water_high, GPIO.IN)
    GPIO.setup(shelf_water_low, GPIO.IN)
    GPIO.setup(shelf_water_high, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(shelf_water_low, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    '''
    根据配置文件重置gpio
    '''
    GPIO.output(layer_1_solenoid_valve, False)
    GPIO.output(layer_2_solenoid_valve, False)
    GPIO.output(layer_3_solenoid_valve, False)
    GPIO.output(layer_4_solenoid_valve, False)
    GPIO.output(layer_5_solenoid_valve, False)
    GPIO.output(layer_6_solenoid_valve, False)
    GPIO.output(shelf_water_pump, False)

    b_run = False
    for i in range(0, len(global_list.water_cycle_attr)):
        if global_list.water_cycle_attr[i]['runState'] == 0: #关闭
            close_layer_solenoid_valve(i+1)
        else:
            open_layer_solenoid_valve(i+1)
            global_list.current_water_run_layer = i+1
            b_run = True
    if b_run == True:
        open_water_pump()

def check_water_level():
    ret = True
    '''
    检测水箱水位是否正常  True--正常  False--异常
   
    ret1= GPIO.input(shelf_water_low)  #低水位
    ret2 = GPIO.input(shelf_water_high) #高水位
    if ret1 == True and ret2 == False:
        logging.info("水箱水位正常")
    else:
        if ret1 == False:
            logging.error("水箱水位过低")
        if ret2 == True:
            logging.error("水箱水位过高")
        ret = False
    '''
    #level = int(global_list.shelf_collect_env['water_level'])
    #if level != 0:
        #ret = False
    #目前硬件不提供水位信息.
    return ret

def open_layer_solenoid_valve(layer):
    ret = True
    logging.info("打开第[%d]层电池阀", layer)
    if layer == 1:
        GPIO.output(layer_1_solenoid_valve, True)
    elif layer == 2:
        GPIO.output(layer_2_solenoid_valve, True)
    elif layer == 3:
        GPIO.output(layer_3_solenoid_valve, True)
    elif layer == 4:
        GPIO.output(layer_4_solenoid_valve, True)
    elif layer == 5:
        GPIO.output(layer_5_solenoid_valve, True)
    elif layer == 6:
        GPIO.output(layer_6_solenoid_valve, True)
    return ret

def close_layer_solenoid_valve(layer):
    ret = True
    logging.info("关闭第%d层电池阀", layer)
    if layer == 1:
        GPIO.output(layer_1_solenoid_valve, False)
    elif layer == 2:
        GPIO.output(layer_2_solenoid_valve, False)
    elif layer == 3:
        GPIO.output(layer_3_solenoid_valve, False)
    elif layer == 4:
        GPIO.output(layer_4_solenoid_valve, False)
    elif layer == 5:
        GPIO.output(layer_5_solenoid_valve, False)
    elif layer == 6:
        GPIO.output(layer_6_solenoid_valve, False)
    return  ret

def open_water_pump():
    ret = True
    logging.info("打开水泵")
    GPIO.output(shelf_water_pump, True)
    return  ret

def close_water_pump():
    ret = True
    logging.info("关闭水泵")
    GPIO.output(shelf_water_pump, False)
    return  ret

def collect_layer_humi(layer):
    humi = 0.0
    '''
    采集土壤湿度值
    是由此处进行采集还是由心跳时进行采集??
    '''
    humi = float(global_list.layer_collect_env[layer-1]['ave_humidity'])
    logging.info("第%d层土壤湿度值: %.2f", layer, humi)
    return humi

def update_state(layer, state):
    config_parse.update_state(layer, state)
    global_list.water_cycle_attr[layer - 1]['runState'] = state

def update_state_and_time(layer, state):
    if state == 0: #关闭
        config_parse.update_state_and_time(layer, 0, 0)
        global_list.water_cycle_attr[layer - 1]['beginTime'] = 0
    else:   #开启
        now = time.time()
        config_parse.update_state_and_time(layer, 1, now)
        global_list.water_cycle_attr[layer - 1]['beginTime'] = now
    global_list.water_cycle_attr[layer - 1]['runState'] = state

def any_layer_shoud_run(now = 0):     #当前是否有需要运行的层
    layer = 0
    for i in range(now, global_list.layer_counts + now):
        k = i % global_list.layer_counts
        if (k+1) == now or  global_list.water_cycle_attr[k]['mode'] == 0:    #排除正在运行的层和手动模式的层
            continue
        humi = collect_layer_humi(k+1)  #编号从1开始
        if  humi <= global_list.water_cycle_attr[k]['scheme']['lowerLimit']:
            layer =  k+1
            break
    logging.info("当前需要运行的层为：%d", layer)
    return  layer

def nursery_auto_cycle(): #育苗区水循环
    send_state_data = {"fun_ID": "14", "collector_ID": "", "layer_ID": "", "cycle_state": ""}
    while True:
        run_layer = global_list.current_water_run_layer
        if run_layer == 0:  #没有层正在运行
            logging.info("当前没有正在运行的层")
            #查看是否有层需要运行
            needLayer = any_layer_shoud_run()
            if needLayer > 0:
                if  check_water_level() == True:
                    logging.info("准备开启水泵及第%d层电池阀", needLayer)
                    global_list.water_mutex.acquire()
                    open_layer_solenoid_valve(needLayer)
                    open_water_pump()
                    update_state_and_time(needLayer, 1)
                    global_list.current_water_run_layer = needLayer
                    global_list.water_mutex.release()
                    '''
                  向服务端发送数据库更新请求：needLayer层运行状态为开启 
                  '''
                    send_state_data["collector_ID"] = global_list.collector_ID
                    send_state_data["layer_ID"] = str(needLayer)
                    send_state_data["cycle_state"] = "1"
                    trade_client.send_message(send_state_data)
                    continue
                else:   #水位异常
                    logging.error("水箱水位异常")
                    time.sleep(5)
                    continue
            else:
                logging.info("没有层需要运行")
                time.sleep(5)
                continue
        else:
            tmp = 0
            logging.info("当前正在运行的层: %d", run_layer)
            now = time.time()
            '''
            TODO:
            当overTime没有设置值时，添加默认最短超时时间， 
             如 max( global_list.water_cycle_attr[run_layer -1]['scheme']['overTime'], 10 )
             设置10s为最短超时时间
            '''
            if  abs(now - global_list.water_cycle_attr[run_layer -1]['beginTime']) <= \
                                        global_list.water_cycle_attr[run_layer -1]['scheme']['overTime']: #未超时
                if global_list.water_cycle_attr[run_layer - 1]['mode'] == 1:  # 自动模式
                    humi = collect_layer_humi(run_layer)
                    if humi <= global_list.water_cycle_attr[run_layer - 1]['scheme']['upperLimit']:  #未超过阈值
                        time.sleep(5)
                        continue
                else:  #手动模式
                    time.sleep(5)
                    continue
            #超时或者超过阈值. 停止注水
            needLayer = any_layer_shoud_run(run_layer)
            global_list.water_mutex.acquire()
            if needLayer > 0:    #有其它层需要运行
                logging.info("第%d层需要运行", needLayer)
                if check_water_level() == True:
                    logging.info("水位正常，打开第%d层电池阀", needLayer)
                    open_layer_solenoid_valve(needLayer)
                    update_state_and_time(needLayer, 1)
                    global_list.current_water_run_layer = needLayer
                else:
                    logging.error("水箱水位异常,关闭水泵")
                    close_water_pump()
                    global_list.current_water_run_layer = 0
                    tmp = 1
            else:   #没有其它层需要运行
                logging.info("没有其它层需要运行,关闭水泵")
                close_water_pump()
                global_list.current_water_run_layer = 0
                tmp = 1
            logging.info("关闭第%d层电池阀", run_layer)
            close_layer_solenoid_valve(run_layer)
            update_state_and_time(run_layer, 0)
            global_list.water_mutex.release()
            '''
            向服务端发送数据库更新请求: run_layer状态为关闭
           '''
            send_state_data["collector_ID"] = global_list.collector_ID
            send_state_data["layer_ID"] =  str(run_layer)
            send_state_data["cycle_state"] = "0"
            trade_client.send_message(send_state_data)
            if tmp == 0:
                '''
                向服务端发送数据库更新请求: needLayer状态为开启
                '''
                send_state_data["layer_ID"] = str(needLayer)
                send_state_data["cycle_state"] = "1"
                trade_client.send_message(send_state_data)

def growth_auto_cycle():  #栽培区水循环
    send_state_data = {"fun_ID": "14", "collector_ID": "", "layer_ID": "", "cycle_state": ""}
    while True:
        run_layer = global_list.current_water_run_layer
        flag = 0
        for i in range(run_layer, global_list.layer_counts):
            if global_list.water_cycle_attr[i]['mode'] == 0: #手动模式/非自动模式
                continue
            if check_water_level() == False:
                break
            open_layer_solenoid_valve(i + 1)
            if run_layer > 0:   #有层正在运行
                close_layer_solenoid_valve(run_layer)
                update_state(run_layer, 0)
                flag = 1
            else:
                open_water_pump()
            update_state(i+1, 1)
            '''
            向服务端发送数据库更新请求: i+1层运行
            '''
            send_state_data["collector_ID"] = global_list.collector_ID
            send_state_data["layer_ID"] = str(i+1)
            send_state_data["cycle_state"] = "1"
            trade_client.send_message(send_state_data)
            if flag == 1:
                update_state(run_layer, 0)
                '''
                向服务端发送数据库更新请求: run_layer层关闭
              '''
                send_state_data["layer_ID"] = str(run_layer)
                send_state_data["cycle_state"] = "0"
                trade_client.send_message(send_state_data)
            global_list.current_water_run_layer = i + 1
            run_layer = i + 1
            '''
                TODO:
                    当cycleTime没有设置值时，添加默认最短运行时间， 
                    如 max( global_list.water_cycle_attr[i]['scheme']['cycleTime'], 10 )
                    设置10s为最短运行时间
            '''
            time.sleep(global_list.water_cycle_attr[i]['scheme']['cycleTime'])
        if run_layer == 0:
            logging.info("当前没有正在运行的层")
            time.sleep(5)
        else:
            logging.info("当前正在运行的层：%d, 关闭水泵及其电池阀", run_layer)
            close_water_pump()
            close_layer_solenoid_valve(run_layer)
            global_list.current_water_run_layer = 0
            update_state(run_layer, 0)
            '''
            向服务端发送数据库更新请求: run_layer状态为关闭
           '''
            send_state_data["collector_ID"] = global_list.collector_ID
            send_state_data["layer_ID"] = str(run_layer)
            send_state_data["cycle_state"] = "0"
            trade_client.send_message(send_state_data)
            '''
              TODO:
               当wait_time没有设置值时，添加默认最短等待时间， 
                如 max( global_list.wait_time, 30 )
                设置30s为最短等待时间
            '''
            time.sleep(global_list.wait_time)

def manual_on_nursery_water_cycle(layer, client_identify):
    logging.info("育苗区手动开启水循环")
    flag = 0
    send_state_data = {"fun_ID": "14", "collector_ID": global_list.collector_ID, "layer_ID": "", "cycle_state": ""}
    send_state_reply = {"client_identify": client_identify, "fun_ID": "09", "collector_ID": global_list.collector_ID,
                        "layer_ID": "", "cycle_state": "", "cycle_mode": ""}
    if global_list.water_cycle_attr[layer-1]['runState'] == 1:
        logging.info("该层已经处于运行状态")
    else:
        if check_water_level() == False:
            '''
            不发送响应消息
            '''
            logging.error("水箱水位异常")
            return
        run_layer = global_list.current_water_run_layer
        global_list.water_mutex.acquire()
        open_layer_solenoid_valve(layer)
        update_state_and_time(layer, 1)
        global_list.current_water_run_layer = layer
        if  run_layer > 0:
            logging.info("需关闭第%d层电池阀，打开第%d层电池阀", run_layer, layer)
            close_layer_solenoid_valve(run_layer)
            update_state_and_time(run_layer, 0)
            flag = 1
        else:
            logging.info("打开第%d层电池阀及水泵", layer)
            open_water_pump()
        global_list.water_mutex.release()
        if flag == 1:
            send_state_data["layer_ID"] = str(run_layer)
            send_state_data["cycle_state"] = "0"
            trade_client.send_message(send_state_data)
    #发送响应消息
    global_list.water_cycle_attr[layer - 1]['mode'] = 0
    config_parse.update_water_mode(layer, "0")
    send_state_reply["layer_ID"] = str(layer)
    send_state_reply["cycle_state"] = "1"
    send_state_reply["cycle_mode"] = "0"
    trade_client.send_message(send_state_reply)

def manual_off_nursery_water_cycle(layer, client_identify):
    logging.info("育苗区手动关闭水循环")
    send_state_reply = {"client_identify": client_identify, "fun_ID": "09", "collector_ID": global_list.collector_ID,
                        "layer_ID": "", "cycle_state": "", "cycle_mode": ""}
    send_state_data = {"fun_ID": "14", "collector_ID": global_list.collector_ID, "layer_ID": "", "cycle_state": ""}
    flag = 0
    if global_list.water_cycle_attr[layer-1]['runState'] == 0:
        logging.info("该层已经处于关闭状态")
    else:
        needLayer = any_layer_shoud_run(layer)
        global_list.water_mutex.acquire()
        if needLayer > 0:
            logging.info("第%d层需要运行，打开%d层电池阀，关闭第%d电池阀", needLayer, needLayer, layer)
            open_layer_solenoid_valve(needLayer)
            update_state_and_time(needLayer, 1)
            global_list.current_water_run_layer = needLayer
            flag = 1
        else:
            logging.info("没有其它层需要运行，关闭第%d层电池阀，关闭水泵", layer)
            close_water_pump()
            global_list.current_water_run_layer = 0
        close_layer_solenoid_valve(layer)
        update_state_and_time(layer, 0)
        global_list.water_mutex.release()
        if flag == 1:
            send_state_data["layer_ID"] = str(needLayer)
            send_state_data["cycle_state"] = "1"
            trade_client.send_message(send_state_data)
    global_list.water_cycle_attr[layer - 1]['mode'] = 0
    config_parse.update_water_mode(layer, "0")
    send_state_reply["layer_ID"] = str(layer)
    send_state_reply["cycle_state"] = "0"
    send_state_reply["cycle_mode"] = "0"
    trade_client.send_message(send_state_reply)