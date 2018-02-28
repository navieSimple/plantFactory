#!/usr/bin/env python
#coding=utf-8
import cv2
import numpy
import logging
import subprocess
import trade_client
import global_list
import os
import base64
import time

def file_exist(file_name):
    return os.path.exists(file_name)

def parse_dev(dev_name):
    cmd = "readlink -f " + dev_name
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    out = process.communicate()[0]
    nums = [int(x) for x in out if x.isdigit()]
    return nums[0]

def position_capture_longExpos1(position):
    dev_name = "/dev/camera" + str(position)
    if file_exist(dev_name) == False:
        logging.info("第%d位置没有连接摄像头", position)
        return
    dev_num = parse_dev(dev_name)
    print (dev_num)
    cap = cv2.VideoCapture(dev_num)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, global_list.capture_width)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, global_list.capture_height)
    if cap.isOpened() == False:
        logging.error("第%d位置摄像头不可用", position)
        return
    # 摄像头增加长曝光处理.
    (rAvg, gAvg, bAvg) = (None, None, None)
    try:
        total = 0
        while total <= 10:
            #ret, frame = cap.read()
            (grabbed, frame) = cap.read()
            if not grabbed:
                break
            (B, G, R) = cv2.split(frame.astype("float"))
            if rAvg is None:
                rAvg = R
                gAvg = G
                bAvg = B
            else:
                rAvg = ((total * rAvg) + (1 * R)) / (total + 1.0)
                gAvg = ((total * gAvg) + (1 * G)) / (total + 1.0)
                bAvg = ((total * bAvg) + (1 * B)) / (total + 1.0)
            total += 1
        avg = cv2.merge([bAvg, gAvg, rAvg]).astype("uint8")
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]
        result, imgencode = cv2.imencode('.jpg', avg, encode_param)
        #data = numpy.array(imgencode)
        #string_data = data.tostring()  #json dump error!!!
        string_data = base64.b64encode(imgencode)
        msg_data = {"fun_ID":"15"}
        msg_data["collector_ID"] = global_list.collector_ID
        msg_data["position_ID"] = str(position)
        msg_data["image"] = string_data
        trade_client.send_message(msg_data)
    except Exception as e:
        logging.error("第%d位置摄像头采集图像数据出错", position)
    cap.release()

def position_capture_longExpos2(position):
    dev_name = "/dev/camera" + str(position)
    if file_exist(dev_name) == False:
        logging.info("第%d位置没有连接摄像头", position)
        return
    dev_num = parse_dev(dev_name)
    print (dev_num)
    cap = cv2.VideoCapture(dev_num)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, global_list.capture_width)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, global_list.capture_height)
    if cap.isOpened() == False:
        logging.error("第%d位置摄像头不可用", position)
        return
    # 摄像头增加长曝光处理.
    try:
        begin_time = time.time()
        ret = False
        frame = None
        while True:
            ret, frame = cap.read()
            now = time.time()
            if (now - begin_time) >= global_list.capture_expose_interval:
                break
        if ret == True:
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]
            result, imgencode = cv2.imencode('.jpg', frame, encode_param)
            #data = numpy.array(imgencode)
            #string_data = data.tostring()  #json dump error!!!
            string_data = base64.b64encode(imgencode)
            msg_data = {"fun_ID":"15"}
            msg_data["collector_ID"] = global_list.collector_ID
            msg_data["position_ID"] = str(position)
            msg_data["image"] = string_data
            trade_client.send_message(msg_data)
    except Exception as e:
        logging.error("第%d位置摄像头采集图像数据出错", position)
    cap.release()

def camera_capture():
    for i in range(0, global_list.camera_counts):
        position_capture_longExpos2(i+1)
