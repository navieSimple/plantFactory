#!/usr/bin/env python
#coding=utf-8
import ConfigParser
import global_list
import string
import sys
import logging

my_config = ConfigParser.ConfigParser()

'''
程序运行前必须有配置文件，并且配置文件中需有[global]标签
[global]下的zone、collector_zone_parameters、collector_id需进行配置
'''

def read_camera_capture_interval():
    global_list.camera_capture_interval = int(my_config.get("camera", "camera_capture_interval"))

def init_camera_capture_interval():
    global_list.camera_capture_interval = 1800 #30min
    my_config.set("camera", "camera_capture_interval", "1800")

def read_water_cycle():
    if global_list.zone == 0:  # 栽培区超时时间
        global_list.wait_time = int(my_config.get("waterCycle", "wait_time"))
    for i in range(0, global_list.layer_counts):  # 读取配置初始化水循环属性结构体
        global_list.water_cycle_attr.append({})
        mode_str = "layer[%d]_mode" % (i + 1)
        state_str = "layer[%d]_state" % (i + 1)
        global_list.water_cycle_attr[i]["mode"] = int(my_config.get("waterCycle", mode_str))
        global_list.water_cycle_attr[i]["runState"] = int(my_config.get("waterCycle", state_str))
        if global_list.zone == 1:  # 育苗区本次水循环初始运行时间，用于超时机制
            begin_time_str = "layer[%d]_begin_time" % (i + 1)
            global_list.water_cycle_attr[i]["beginTime"] = \
                float(my_config.get("waterCycle", begin_time_str))
        global_list.water_cycle_attr[i]["scheme"] = {}
        if global_list.zone == 0:  # 栽培区水循环策略
            cycle_time_str = "layer[%d]_cycle_time" % (i + 1)
            global_list.water_cycle_attr[i]["scheme"]["cycleTime"] = \
                int(my_config.get("waterCycle", cycle_time_str))
        else:  # 育苗区水循环策略
            lower_limit_str = "layer[%d]_lower_limit" % (i + 1)
            upper_limit_str = "layer[%d]_upper_limit" % (i + 1)
            over_time_str = "layer[%d]_over_time" % (i + 1)
            global_list.water_cycle_attr[i]["scheme"]["lowerLimit"] = \
                float(my_config.get("waterCycle", lower_limit_str))
            global_list.water_cycle_attr[i]["scheme"]["upperLimit"] = \
                float(my_config.get("waterCycle", upper_limit_str))
            global_list.water_cycle_attr[i]["scheme"]["overTime"] = \
                int(my_config.get("waterCycle", over_time_str))

def init_water_cycle():
    if global_list.zone == 0:  # 栽培区超时时间
        global_list.wait_time = 0
        my_config.set("waterCycle", "wait_time", "0")
    for i in range(0, global_list.layer_counts):  # 读取配置初始化水循环属性结构体
        global_list.water_cycle_attr.append({})
        mode_str = "layer[%d]_mode" % (i + 1)
        state_str = "layer[%d]_state" % (i + 1)
        global_list.water_cycle_attr[i]["mode"] = 0
        my_config.set("waterCycle", mode_str, "0")
        global_list.water_cycle_attr[i]["runState"] = 0
        my_config.set("waterCycle", state_str, "0")
        if global_list.zone == 1:  # 育苗区本次水循环初始运行时间，用于超时机制
            begin_time_str = "layer[%d]_begin_time" % (i + 1)
            global_list.water_cycle_attr[i]["beginTime"] = 0
            my_config.set("waterCycle", begin_time_str, "0")
        global_list.water_cycle_attr[i]["scheme"] = {}
        if global_list.zone == 0:  # 栽培区水循环策略
            cycle_time_str = "layer[%d]_cycle_time" % (i + 1)
            global_list.water_cycle_attr[i]["scheme"]["cycleTime"] = 0
            my_config.set("waterCycle", cycle_time_str, "0")
        else:  # 育苗区水循环策略
            lower_limit_str = "layer[%d]_lower_limit" % (i + 1)
            upper_limit_str = "layer[%d]_upper_limit" % (i + 1)
            over_time_str = "layer[%d]_over_time" % (i + 1)
            global_list.water_cycle_attr[i]["scheme"]["lowerLimit"] = 0.0
            my_config.set("waterCycle", lower_limit_str, "0.0")
            global_list.water_cycle_attr[i]["scheme"]["upperLimit"] = 0.0
            my_config.set("waterCycle", upper_limit_str, "0.0")
            global_list.water_cycle_attr[i]["scheme"]["overTime"] = 0
            my_config.set("waterCycle", over_time_str, "0")

def read_light_ctl():
    for i in range(0, global_list.layer_counts):
        global_list.light_attr.append({})
        mode_str = "layer[%d]_mode"%(i+1)
        state_str = "layer[%d]_state"%(i+1)
        open_time_str = "layer[%d]_open_time"%(i+1)
        close_time_str = "layer[%d]_close_time"%(i+1)
        global_list.light_attr[i]["mode"] = int(my_config.get("lightCtl", mode_str))
        global_list.light_attr[i]["state"] = int(my_config.get("lightCtl", state_str))
        global_list.light_attr[i]["scheme"] = {}
        global_list.light_attr[i]["scheme"]["openTime"] = my_config.get("lightCtl", open_time_str)  #字符串格式
        global_list.light_attr[i]["scheme"]["closeTime"] = my_config.get("lightCtl", close_time_str)
def init_light_ctl():
    for i in range(0, global_list.layer_counts):
        global_list.light_attr.append({})
        mode_str = "layer[%d]_mode"%(i+1)
        state_str = "layer[%d]_state"%(i+1)
        open_time_str = "layer[%d]_open_time"%(i+1)
        close_time_str = "layer[%d]_close_time"%(i+1)
        global_list.light_attr[i]["mode"] = 0
        my_config.set("lightCtl", mode_str, "0")
        global_list.light_attr[i]["state"] = 0
        my_config.set("lightCtl", state_str, "0")
        global_list.light_attr[i]["scheme"] = {}
        global_list.light_attr[i]["scheme"]["openTime"] = "0000"
        my_config.set("lightCtl", open_time_str, "0000")  #字符串格式
        global_list.light_attr[i]["scheme"]["closeTime"] = "0000"
        my_config.set("lightCtl", close_time_str, "0000")

def init_configure():
    try:
        ret = my_config.read(global_list.config_file)
        if len(ret) == 0:
            logging.error('no config file!')
            sys.exit(1)
        else:
            global_list.collector_ID = my_config.get("global", "collector_id")
            global_list.zone = int(my_config.get("global", "zone"))
            global_list.collector_zone_parameters = int(my_config.get("global", "collector_zone_parameters"))
            if global_list.collector_zone_parameters == 1:  #区域环境采集集中器
                global_list.zone_collect_env = {"zone_humi":"0.0", "zone_temp":"0.0", "co2":"0.0"}
            else:   #架子集中器
                global_list.shelf_collect_env = {"water_level":"1", "PH":"0.0", "EC":"0", "water_temp":"0.0"}
            if my_config.has_option("global", "layer_counts") == True:
                global_list.layer_counts = int(my_config.get("global", "layer_counts"))
            elif global_list.collector_zone_parameters == 0:  # 架子集中器
                global_list.layer_counts = 0
                my_config.set("global", "layer_counts", "0")
            if global_list.collector_zone_parameters == 0:  #架子集中器
                for i in range(0, global_list.
                        layer_counts):
                    tmp_dict = {"illumination":"0.0", "ave_humidity":"0.0"}
                    global_list.layer_collect_env.append(tmp_dict)
            if my_config.has_section("waterCycle") == True:
                read_water_cycle()
            elif global_list.collector_zone_parameters == 0:
                my_config.add_section("waterCycle")
                init_water_cycle()
            if  my_config.has_section("lightCtl") == True:
                read_light_ctl()
            elif global_list.collector_zone_parameters == 0:
                my_config.add_section("lightCtl")
                init_light_ctl()
            if my_config.has_section("camera") == True:
                read_camera_capture_interval()
            elif global_list.collector_zone_parameters == 0:
                my_config.add_section("camera")
                init_camera_capture_interval()
            my_config.write(open(global_list.config_file, "w"))
    except Exception as e:
        logging.error(e.message)
        sys.exit(1)

def update_state(layer, state):
    lay_state_str = "layer[%d]_state" % (layer)
    my_config.set("waterCycle", lay_state_str, str(state))
    my_config.write(open(global_list.config_file, "w"))

def update_state_and_time(layer, state, time):
    #my_config.read(global_list.config_file)
    lay_state_str = "layer[%d]_state" % (layer)
    lay_time_str = "layer[%d]_begin_time"%(layer)
    my_config.set("waterCycle", lay_state_str, str(state))
    my_config.set("waterCycle", lay_time_str, str(time))
    my_config.write(open(global_list.config_file, "w"))

def update_light_state(layer, state):
    lay_state_str = "layer[%d]_state" % (layer)
    my_config.set("lightCtl", lay_state_str, str(state))
    my_config.write(open(global_list.config_file, "w"))

def update_layer_counts(counts):
    my_config.set('global', 'layer_counts', counts)
    my_config.write(open(global_list.config_file, "w"))

def update_water_scheme_nursery(layer, lowerLimit, upperLimit, overTime):
    lower_limit_str = "layer[%d]_lower_limit" %(layer)
    upper_limit_str = "layer[%d]_upper_limit" %(layer)
    over_time_str = "layer[%d]_over_time" %(layer)
    my_config.set("waterCycle", lower_limit_str, lowerLimit)
    my_config.set("waterCycle", upper_limit_str, upperLimit)
    my_config.set("waterCycle", over_time_str, overTime)
    my_config.write(open(global_list.config_file, "w"))

def update_water_scheme_growth(layer, cycle_time, wait_time):
    cycle_time_str = "layer[%d]_cycle_time" %(layer)
    my_config.set("waterCycle", cycle_time_str, cycle_time)
    my_config.set("waterCycle", "wait_time", wait_time)
    my_config.write(open(global_list.config_file, "w"))

def update_light_scheme(layer, open_time, close_time):
    open_time_str = "layer[%d]_open_time" %(layer)
    close_time_str = "layer[%d]_close_time" %(layer)
    my_config.set("lightCtl", open_time_str, open_time)
    my_config.set("lightCtl", close_time_str, close_time)
    my_config.write(open(global_list.config_file, "w"))

def update_light_mode(layer, mode):
    mode_str = "layer[%d]_mode" %(layer)
    my_config.set("lightCtl", mode_str, mode)
    my_config.write(open(global_list.config_file, "w"))

def update_water_mode(layer, mode):
    mode_str = "layer[%d]_mode" %(layer)
    my_config.set("waterCycle", mode_str, mode)
    my_config.write(open(global_list.config_file, "w"))