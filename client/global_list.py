#!/usr/bin/env python
#coding=utf-8
import Queue
import threading

SERVER_IP = "182.61.18.112"
SERVER_PORT = 50013
server_addr = (SERVER_IP, SERVER_PORT)

socket_tcp = None


socket_threads = []
deal_threads = []

TCP_link_is_OK = 1 #1:link is OK; 0: link is broken

RcvData_MAX_len = 1024

g_queue_recv = Queue.Queue()
g_queue_send = Queue.Queue()

zone = 0 # 0: growth zone; 1: nursery zone
collector_zone_parameters = 0 # 1: collector get just zone parameters; 0: collector will get the parameters of the shelf.  

collector_ID = ""
shelf_ID = {} #key is shelf_ID; value is the number of layer corresponding to shelf_ID
shelfID_to_collector_shelfID= {}#shelfID is corresponding to shelfID of collector
list_all_startandend_time_for_light = []#it is a two dimension.
                        #[[shelf_ID layer_ID light_type start_time end_time],...] 
list_all_light_status = [] ##it is a two dimension.
                        #[[shelf_ID layer_ID light_status ultraviolet_status],...] 
ini_start_time =730
ini_end_time =1930

waterlevel_low = 0
shelf_to_waterlevel = {1:1,2:1,3:1,4:1} # the waterlevel of each shelf is low or not.
#{shelf_num:0/1/2} 0: waterlevel is low; 1: waterlevel is ok; 2: waterlevel is high

trade_dict_data = {}

timer = None
heart_jump_time = 10

heart_jump_num = 0

waterdump_timer = None
waterdump_work_duration = 150
waterdump_NOwork_duration = 600
waterdump_flag = 0

'''
新增
'''
socket_state = False
config_file = "/home/pi/plant_factory/conf/plant_factory.conf"
log_file    = "/home/pi/plant_factory/logs/plant_factory.log"
layer_counts = 0 #层数
water_cycle_attr = []   #水循环属性列表
water_mutex = threading.Lock()
current_water_run_layer = 0 #当前正在运行的层. 0--没有运行的层. 层从1开始
wait_time = 0.0 # 栽培区架子大循环间隔时间，秒数
wait_time_default = 30    #大循环间隔时间默认值
over_time_default = 300 #育苗区水循环超时时间默认值
light_attr = [] #灯控列表
collect_env_interval = 30    #30s环境采集间隔时间
zone_collect_env = {}        #区域环境参数字典
shelf_collect_env = {}       #架子环境参数字典
layer_collect_env = []       #层环境参数列表
camera_capture_interval = 1800 #摄像头拍照间隔时间, 从配置文件读取，默认为30min
camera_counts = 4   #摄像头默认最大数. usb口个数
capture_width = 1920
capture_height = 1080
capture_expose_interval = 10