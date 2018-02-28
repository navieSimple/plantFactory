#coding=utf-8
import Queue

#HOST_IP = ""
#HOST_PORT = 50011

#server_addr = (SERVER_IP, SERVER_PORT)

socket_tcp = None
socket_con = None
message_queue_map = {}   # socket到消息队列的映射
ioloop = None
cur = None #it is cursor for mysql
conn = None
conn_leadingend = None
channel_leadingend =None
consume_queue_name = 'pf_down'
publish_queue_name = 'pf_up'

RcvData_MAX_len = 512

g_queue_recv = Queue.Queue()
g_queue_send = Queue.Queue()

g_default_starttime_to_alllight ='0730'
g_default_endtime_to_alllight ='1830'
g_image_dir = "/var/www/P11/plant_image/"
g_database_img_dir = "http://182.61.18.112:8081/plant_image/"
g_msg_len_max = 5 * 1024 * 1024
g_log_file = "/mnt/plant_factory/logs/plant_factory.log"