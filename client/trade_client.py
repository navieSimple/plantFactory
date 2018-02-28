#!/usr/bin/env python
#coding=utf-8

import threading
import time
import global_list
import logging
import json_client
import sensors
import LEDandWaterpump 
import water_level
import water_cycle
import config_parse
import light_control
import camera_capture
import sensors_new
#import os

heart_jump_sent = {'fun_ID':'00','collector_ID':'AABBBCCCC'}
get_shelfID_layerNUM_sent = {'fun_ID':'01','collector_ID':'AABBBCCCC'}

indoor_envir_sent = {'fun_ID':'05','collector_ID':'230000001','indoor_temp':'27','indoor_humi':'45.2','co2':'23.4'}
shelf_data_sent = {'fun_ID':'06', 'collector_ID':'230000001','shelf_ID':'0001','layer_ID':'0001','water_level':'12','water_temp':'20','illumination':'200.1'}

def send_message(msg):
    if global_list.socket_state == True:
        json_data = json_client.json_encode(msg)
        global_list.g_queue_send.put(json_data)

#send the message {‘fun_ID’:’010’， ’collector_ID’:’xx’}
def get_layernum():
    msg_data = {"fun_ID":"010"}
    msg_data["collector_ID"] = global_list.collector_ID
    send_message(msg_data)

#process responsive data of getting layer number 
#{‘fun_ID’:’010’， ’collector_ID’:’xx’， 'layer_num':'x }
def get_layernum_process(layer_num):
    global_list.layer_counts = int(layer_num)
    config_parse.update_layer_counts(layer_num)

#send the message {‘fun_ID’:’011’， ’collector_ID’:’xx’， 'layer_ID':'x'，'light_mode':'x'(1:auto;0:non-auto)，'light_on_off_state':'x' }
def update_lighttime_scheme():
    msg_data = {'fun_ID':'011'}
    msg_data["collector_ID"] = global_list.collector_ID
    for i in range(0, global_list.layer_counts):
        msg_data['layer_ID'] = str(i+1)
        #msg_data['start_time'] = global_list.light_attr[i]['scheme']['openTime']
        #msg_data['end_time'] = global_list.light_attr[i]['scheme']['closeTime']
        msg_data['light_mode'] = str(global_list.light_attr[i]['mode'])
        msg_data['light_on_off_state'] = str(global_list.light_attr[i]['state'])
        send_message(msg_data)

#process responsive data of updating light time scheme 
#{‘fun_ID’:’011’， 'layer_ID':'x'，'start_time':' xxxx'， ' end_time ':' xxxx'}
def update_lighttime_scheme_process(layer, start_time, end_time):
    global_list.light_attr[layer-1]['scheme']['openTime'] = start_time
    global_list.light_attr[layer-1]['scheme']['closeTime'] = end_time
    config_parse.update_light_scheme(layer, start_time, end_time)

#send the message {‘fun_ID’:’012’， ’collector_ID’:’xx’， 'layer_ID':'x'，'cycle_mode':' xxxx', 'cycle_state':' xxxx' }
def update_watercycle_scheme_growthzone():
    msg_data = {'fun_ID':'012'}
    msg_data["collector_ID"] = global_list.collector_ID
    for i in range(0, global_list.layer_counts):
        msg_data['layer_ID'] = str(i+1)
        #msg_data['cycle_time'] = str(global_list.water_cycle_attr[i]['scheme']['cycleTime'])
        #msg_data['waiting_time'] = str(global_list.wait_time)
        msg_data['cycle_mode'] = str(global_list.water_cycle_attr[i]['mode'])
        msg_data['cycle_state'] = str(global_list.water_cycle_attr[i]['runState'])
        send_message(msg_data)

#process responsive data of updating water cycle scheme in the growth zone
#{‘fun_ID’:’012’ ， 'layer_ID':'x'，'cycle_time':' xxxx'， 'waiting_time':' xxxx'}
def update_watercycle_scheme_growthzone_process(layer, cycle_time, wait_time):
    global_list.wait_time = int(wait_time)
    global_list.water_cycle_attr[layer - 1]['scheme']['cycleTime'] = int(cycle_time)
    config_parse.update_water_scheme_growth(layer, cycle_time, wait_time)

#send the message {‘fun_ID’:’013’， ’collector_ID’:’xx’， 'layer_ID':'x'，'cycle_mode':' xxxx',  'cycle_state':' xxxx' }
def update_watercycle_scheme_nurseryzone():
    msg_data = {'fun_ID':'013'}
    msg_data['collector_ID'] = global_list.collector_ID
    for i in range(0, global_list.layer_counts):
        msg_data['layer_ID'] = str(i+1)
        #msg_data['timeout'] = str(global_list.water_cycle_attr[i]['scheme']['overTime'])
        #msg_data['humi_min'] = str(global_list.water_cycle_attr[i]['scheme']['lowerLimit'])
        #msg_data['humi_max'] = str(global_list.water_cycle_attr[i]['scheme']['upperLimit'])
        msg_data['cycle_mode'] = str(global_list.water_cycle_attr[i]['mode'])
        msg_data['cycle_state'] = str(global_list.water_cycle_attr[i]['runState'])
        send_message(msg_data)

#process responsive data of updating water cycle scheme in the nursery zone
#{‘fun_ID’:’013’ ， 'layer_ID':'x'，'timeout':' xxxx'，'humi_min':'xx', 'humi_max':'xx'}
def update_watercycle_scheme_nurseryzone_process(layer, timeout, humi_min, humi_max):
    global_list.water_cycle_attr[layer - 1]['scheme']['overTime'] = int(timeout)
    global_list.water_cycle_attr[layer - 1]['scheme']['lowerLimit'] = float(humi_min)
    global_list.water_cycle_attr[layer - 1]['scheme']['upperLimit'] = float(humi_max)
    config_parse.update_water_scheme_nursery(layer, humi_min, humi_max, timeout)

#send the message {‘fun_ID’:’02’， ’collector_ID’:’xx’, 'zone_humi':'xx', 'zone_temp':'xx', 'co2':'xx'}
def send_zone_envir_para():
    msg_data = {'fun_ID':'02'}
    msg_data['collector_ID'] = global_list.collector_ID
    msg_data['zone_humi'] = global_list.zone_collect_env['zone_humi']
    msg_data['zone_temp'] = global_list.zone_collect_env['zone_temp']
    msg_data['co2']  = global_list.zone_collect_env['co2']
    send_message(msg_data)

#process responsive data of sending zone enviroment parameters
#{‘fun_ID’:’02’ }
def send_zone_envir_para_process():
    pass

#send the message {‘fun_ID’:’10’， ’collector_ID’:’xx’，'water_level':'x'，'PH':'xx', 'EC':'xx', 'water_temp':'xx'}
def send_shelf_data():
    msg_data = {'fun_ID': '10'}
    msg_data['collector_ID'] = global_list.collector_ID
    msg_data['water_level'] = global_list.shelf_collect_env['water_level']
    msg_data['PH'] = global_list.shelf_collect_env['PH']
    msg_data['EC'] = global_list.shelf_collect_env['EC']

    msg_data['water_temp'] = global_list.shelf_collect_env['water_temp']
    send_message(msg_data)

#process responsive data of sending shelf data
#{‘fun_ID’:’10’ }
def send_shelf_data_process():
    pass

#send the message {‘fun_ID’:’11’， ’collector_ID’:’xx’， 'layer_ID':'x'， 'illumination':'xx', 'ave_humidity':'xx'}
def send_layer_data():
    for i in range(0, global_list.layer_counts):
        msg_data = {'fun_ID': '11'}
        msg_data['collector_ID'] = global_list.collector_ID
        msg_data['layer_ID'] = str(i+1)
        msg_data['illumination'] = global_list.layer_collect_env[i]['illumination']
        msg_data['ave_humidity'] = global_list.layer_collect_env[i]['ave_humidity']
        send_message(msg_data)

#process responsive data of sending layer data
#{‘fun_ID’:’11’ }
def send_layer_data_process():
    pass

# process on/off light
#{‘fun_ID’:’03’ ，’collector_ID’:’xx’， 'layer_ID':'x'，'light_on_off':'x'(1:on;0:off)}
def lihgt_on_off_process(layer,state):
    if state == 1:
        light_control.light_munual_open(layer)
    else:
        light_control.light_munual_close(layer)

#process light scheme
#{‘fun_ID’:’04’， ’collector_ID’:’xx’， 'layer_ID':'x'， 'start_time':' xxxx'， ' end_time ':' xxxx' }
def light_scheme_process(layer, start_time, end_time):
    global_list.light_attr[layer-1]['scheme']['openTime'] = start_time
    global_list.light_attr[layer - 1]['scheme']['closeTime'] = end_time
    config_parse.update_light_scheme(layer, start_time, end_time)

#process light start/quit auto mode
#{‘fun_ID’:’12’ ，’collector_ID’:’xx’， 'layer_ID':'x'，'light_mode':'x'(1:auto;0: non-auto)}
def light_s_q_automode_process(layer, mode):
    global_list.light_attr[layer-1]['mode'] = int(mode)
    config_parse.update_light_mode(layer, mode)

#process water cycle scheme in the growth zone
#{‘fun_ID’:’05’， ’collector_ID’:’xx’， 'layer_ID':'x'， 'cycle_time':' xxxx'， ' waiting_time ':' xxxx' }
def watercycle_scheme_growthzone_process(layer, cycle_time, wait_time):
    global_list.wait_time = int(wait_time)
    global_list.water_cycle_attr[layer-1]['scheme']['cycleTime'] = int(cycle_time)
    config_parse.update_water_scheme_growth(layer, cycle_time ,wait_time)

# process certain layer of water cycle  start/quit  auto mode in the growth zone
#{‘fun_ID’:’06’ ，’collector_ID’:’xx’， 'layer_ID':'x'，'cycle_mode':'x'(1:auto;0:non-auto)}
def watercycle_s_q_automode_growthzone_process(layer, cycle_mode):
    global_list.water_cycle_attr[layer-1]['mode'] = int(cycle_mode)
    config_parse.update_water_mode(layer, cycle_mode)

#process water cycle scheme in the nursery zone
#{‘fun_ID’:’07’， ’collector_ID’:’xx’， 'layer_ID':'x'， 'timeout':' xxxx'， ' humi_min ':' xxxx' ，' humi_max ':' xxxx' }
def watercycle_scheme_nurseryzone_process(layer, timeout, humi_min, humi_max):
    global_list.water_cycle_attr[layer - 1]['scheme']['overTime'] = int(timeout)
    global_list.water_cycle_attr[layer - 1]['scheme']['lowerLimit'] = float(humi_min)
    global_list.water_cycle_attr[layer - 1]['scheme']['upperLimit'] = float(humi_max)
    config_parse.update_water_scheme_nursery(layer, humi_min, humi_max, timeout)

# process certain layer of water cycle  start/quit  auto mode in the nursery zone
#{‘fun_ID’:’08’ ，’collector_ID’:’xx’， 'layer_ID':'x'，'cycle_mode':'x'(1:auto;0:non-auto)}
def watercycle_s_q_automode_nurseryzone_process(layer, cycle_mode):
    global_list.water_cycle_attr[layer - 1]['mode'] = int(cycle_mode)
    config_parse.update_water_mode(layer, cycle_mode)

#process manual on/off water cycle in the nursery zone
#{‘fun_ID’:’09’ ，’collector_ID’:’xx’， 'layer_ID':'x'，'cycle_on_off':'x'(1:on;0:off)}
def waterclyel_on_off_nurseryzone_process(layer, state, client_identify):
    if state == 1:
        water_cycle.manual_on_nursery_water_cycle(layer, client_identify)
    else:
        water_cycle.manual_off_nursery_water_cycle(layer, client_identify)

# when the system start or restart,update all data.
def update_data_send():
    get_layernum()
    update_lighttime_scheme()
    if global_list.zone == 0:#(global_list.zone# 0: growth zone; 1: nursery zone)
        update_watercycle_scheme_growthzone()
    else:
        update_watercycle_scheme_nurseryzone()

def heart_jump_send():
    global_list.heart_jump_num = global_list.heart_jump_num + 1
    global_list.TCP_link_is_OK = 0
    #sending heart jump
    heart_jump_sent['collector_ID'] = global_list.collector_ID
    send_message(heart_jump_sent)
    logging.info(global_list.TCP_link_is_OK)
    
    #sending zone environment data
    if global_list.heart_jump_num % 4 == 0:
        if global_list.collector_zone_parameters == 1:
            send_zone_envir_para()
        else:
            send_shelf_data()
    
    if global_list.heart_jump_num % 5 == 0 and global_list.collector_zone_parameters == 0:
        send_layer_data()
    
    global_list.timer = threading.Timer(global_list.heart_jump_time,heart_jump_send)
    global_list.timer.start()
    
#process responsive data of heart jump sent  {‘fun_ID’:’00’， ’collector_ID’:’xx’}  
def heart_jump_process():
    global_list.TCP_link_is_OK = 1
    logging.info("recieved the heart jump!")    


#light on or off automatically
def thread_light():
   light_control.light_auto_control()

# automatical water cycle in the growth zone
def thread_watercycle_growthzone():
    water_cycle.growth_auto_cycle()

# automatical water cycle in the nursery zone
def thread_watercycle_nurseryzone():
    water_cycle.nursery_auto_cycle()

def zone_collect_env():
    #global_list.zone_collect_env = {'zone_humi':'', 'zone_temp':'', 'co2':''}
    while True:
        #time.sleep(global_list.collect_env_interval)
        '''
        采集区域环境参数   
        '''
        co2, temp, hum = sensors_new.zone_CO2_Temp_Hum()
        global_list.zone_collect_env['zone_humi'] = str(hum)
        global_list.zone_collect_env['zone_temp'] = str(temp)
        global_list.zone_collect_env['co2'] = str(co2)
        time.sleep(global_list.collect_env_interval)

def shelf_collect_env():
    #global_list.shelf_collect_env = {'water_level':''，'PH':'', 'EC':'', 'water_temp':''}
    #global_list.layer_collect_env = [{'illumination':'', 'ave_humidity':''},{'illumination':'', 'ave_humidity':''}...]
    while True:
        #time.sleep(global_list.collect_env_interval)
        '''
         采集架子环境参数 及 层环境参数 
        '''
        water_temp = sensors_new.shelf_Water_Tem()
        ph = sensors_new.shelf_PH()
        ec = sensors_new.shelf_EC()
        level= sensors_new.water_level()
        global_list.shelf_collect_env['PH'] = str(ph)
        global_list.shelf_collect_env['EC'] = str(ec)
        global_list.shelf_collect_env['water_temp'] = str(water_temp)
        global_list.shelf_collect_env['water_level'] = str(level)
        for i in range(0, global_list.layer_counts):
            illum = sensors_new.Light_intensity(i+1)
            ave_humidity = sensors_new.layer_humi(i+1)
            global_list.layer_collect_env[i]['illumination'] = str(illum)
            global_list.layer_collect_env[i]['ave_humidity'] = str(ave_humidity)
        time.sleep(global_list.collect_env_interval)

#trade process function   
def thread_trade():
    while True:
        try:
            if global_list.g_queue_recv.empty() == True:
                time.sleep(0.1)
                continue
            else:
                data = global_list.g_queue_recv.get()
                global_list.trade_dict_data = {}
                global_list.trade_dict_data = json_client.json_decode(data)
                logging.info('Recieve data in the thread_trade: %s',global_list.trade_dict_data)
                #print("Recieve data in the thread_trade: %s" %global_list.trade_dict_data)
                '''
                if (global_list.trade_dict_data['collector_ID'] != global_list.collector_ID):
                    logging.error("collector_ID error!")
                    continue
                '''
                if global_list.trade_dict_data['fun_ID'] =='00': #process heart jump
                    heart_jump_process()

                elif global_list.trade_dict_data['fun_ID'] =='010': #process responsive data of getting layer number
                    get_layernum_process(global_list.trade_dict_data['layer_num'])

                elif global_list.trade_dict_data['fun_ID'] =='011': #process responsive data of updatign light time scheme
                    update_lighttime_scheme_process(int(global_list.trade_dict_data['layer_ID']),
                                                    global_list.trade_dict_data['start_time'],global_list.trade_dict_data['end_time'])

                elif global_list.trade_dict_data['fun_ID'] =='012': #process responsive data of updatign water cycle scheme in the growth zone
                    remote_cycle = int(global_list.trade_dict_data['cycle_time'])
                    cycle_time = (remote_cycle / 100) * 60 + remote_cycle % 100
                    remote_wait = int(global_list.trade_dict_data['waiting_time'])
                    wait_time = (remote_wait / 100) * 60 + remote_wait % 100
                    update_watercycle_scheme_growthzone_process(int(global_list.trade_dict_data['layer_ID']), str(cycle_time),
                                                         str(wait_time))

                elif global_list.trade_dict_data['fun_ID'] =='013': #process responsive data of updatign water cycle scheme in the nursery zone
                    remote_out = int(global_list.trade_dict_data['timeout'])
                    time_out = (remote_out / 100) * 60 + remote_out % 100
                    update_watercycle_scheme_nurseryzone_process(int(global_list.trade_dict_data['layer_ID']), str(time_out),
                                                          global_list.trade_dict_data['humi_min'], global_list.trade_dict_data['humi_max'])

                elif global_list.trade_dict_data['fun_ID'] =='02': #process responsive data of sending zone enviroment parameters
                    send_zone_envir_para_process()

                elif global_list.trade_dict_data['fun_ID'] =='03': #process on/off light
                    layer = int(global_list.trade_dict_data['layer_ID'])
                    state = int(global_list.trade_dict_data['light_on_off'])
                    lihgt_on_off_process(layer, state)
                    msg_data = {'client_identify':global_list.trade_dict_data['client_identify'],\
                                'fun_ID': '03', 'collector_ID':global_list.trade_dict_data['collector_ID'],\
                                'layer_ID':global_list.trade_dict_data['layer_ID'] ,\
                                'light_on_off':global_list.trade_dict_data['light_on_off']}
                    send_message(msg_data)

                elif global_list.trade_dict_data['fun_ID'] =='04': #process light scheme
                    light_scheme_process(int(global_list.trade_dict_data['layer_ID']),
                                         str(global_list.trade_dict_data['start_time']), str(global_list.trade_dict_data['end_time']))
                    msg_data = { 'client_identify': global_list.trade_dict_data['client_identify'], \
                                'fun_ID': '04', 'collector_ID': global_list.trade_dict_data['collector_ID'], \
                                'layer_ID': global_list.trade_dict_data['layer_ID'], \
                                'start_time': global_list.trade_dict_data['start_time'],\
                                'end_time': global_list.trade_dict_data['end_time'] }
                    send_message(msg_data)

                elif global_list.trade_dict_data['fun_ID'] =='05': #process water cycle scheme in the growth zone
                    remote_cycle = int( global_list.trade_dict_data['cycle_time'] )
                    cycle_time = ( remote_cycle / 100 ) * 60 +  remote_cycle % 100
                    remote_wait = int( global_list.trade_dict_data['waiting_time'] )
                    wait_time = ( remote_wait / 100 ) * 60 + remote_wait % 100
                    #logging.info("remote_cycle:%d cycle_time:%d remote_wait:%d wait_time:%d", remote_cycle, cycle_time, remote_wait, wait_time)
                    watercycle_scheme_growthzone_process(int(global_list.trade_dict_data['layer_ID']), str(cycle_time),
                                                         str(wait_time))
                    msg_data = {'client_identify': global_list.trade_dict_data['client_identify'], \
                                'fun_ID': '05', 'collector_ID': global_list.trade_dict_data['collector_ID'], \
                                'layer_ID': global_list.trade_dict_data['layer_ID'], \
                                'cycle_time': global_list.trade_dict_data['cycle_time'], \
                                'waiting_time': global_list.trade_dict_data['waiting_time']}
                    send_message(msg_data)

                elif global_list.trade_dict_data['fun_ID'] =='06': #process certain layer of water cycle  start/quit  auto mode in the growth zone
                    watercycle_s_q_automode_growthzone_process(int(global_list.trade_dict_data['layer_ID']), str(global_list.trade_dict_data['cycle_mode']))
                    msg_data = {'client_identify': global_list.trade_dict_data['client_identify'], \
                                'fun_ID': '06', 'collector_ID': global_list.collector_ID, \
                                'layer_ID': global_list.trade_dict_data['layer_ID'],\
                                'cycle_mode': global_list.trade_dict_data['cycle_mode']}
                    send_message(msg_data)

                elif global_list.trade_dict_data['fun_ID'] =='07': #process water cycle scheme in the nursery zone
                    remote_out = int(global_list.trade_dict_data['timeout'])
                    time_out = ( remote_out / 100) * 60 + remote_out % 100
                    watercycle_scheme_nurseryzone_process(int(global_list.trade_dict_data['layer_ID']), str(time_out),
                                                          str(global_list.trade_dict_data['humi_min']), str(global_list.trade_dict_data['humi_max']))
                    msg_data = {'client_identify': global_list.trade_dict_data['client_identify'],\
                                'fun_ID': '07', 'collector_ID': global_list.collector_ID, \
                                'layer_ID': global_list.trade_dict_data['layer_ID'], \
                                'timeout': global_list.trade_dict_data['timeout'], \
                                'humi_min': global_list.trade_dict_data['humi_min'], \
                                'humi_max': global_list.trade_dict_data['humi_max']}
                    send_message(msg_data)

                elif global_list.trade_dict_data['fun_ID'] =='08': #process certain layer of water cycle  start/quit  auto mode in the nursery zone
                    watercycle_s_q_automode_nurseryzone_process(int(global_list.trade_dict_data['layer_ID']), str(global_list.trade_dict_data['cycle_mode']))
                    msg_data = {'client_identify': global_list.trade_dict_data['client_identify'],\
                                'fun_ID': '08', 'collector_ID': global_list.collector_ID,
                                'layer_ID': global_list.trade_dict_data['layer_ID'],
                                'cycle_mode': global_list.trade_dict_data['cycle_mode']}
                    send_message(msg_data)

                elif global_list.trade_dict_data['fun_ID'] =='09': #process manual on/off water cycle in the nursery zone
                    layer = int(global_list.trade_dict_data['layer_ID'])
                    state = int(global_list.trade_dict_data['cycle_state'])
                    client_identify = global_list.trade_dict_data['client_identify']
                    waterclyel_on_off_nurseryzone_process(layer, state, client_identify)

                elif global_list.trade_dict_data['fun_ID'] =='10': #process responsive data of sending shelf data
                    send_shelf_data_process()

                elif global_list.trade_dict_data['fun_ID'] =='11': #process responsive data of sending layer data
                    send_layer_data_process()

                elif global_list.trade_dict_data['fun_ID'] =='12': #process light start/quit auto mode
                    light_s_q_automode_process(int(global_list.trade_dict_data['layer_ID']), str(global_list.trade_dict_data['light_mode']))
                    msg_data = {'client_identify': global_list.trade_dict_data['client_identify'], \
                                'fun_ID': '12', 'collector_ID': global_list.trade_dict_data['collector_ID'], \
                                'layer_ID': global_list.trade_dict_data['layer_ID'], \
                                'light_mode': global_list.trade_dict_data['light_mode']}
                    send_message(msg_data)

                elif global_list.trade_dict_data['fun_ID'] == '13': #process responsive data of updatign light state
                    pass

                elif global_list.trade_dict_data['fun_ID'] == '14': #process responsive data of updatign water cycle state
                    pass

                elif global_list.trade_dict_data['fun_ID'] == '15': #process responsive data of layer camera capture
                    pass

                else:
                   logging.error("function ID error!")
        except:
            logging.error("thread_trade error!")


def camera_cature():
    time.sleep(60)
    while True:
        camera_capture.camera_capture()
        time.sleep(global_list.camera_capture_interval)