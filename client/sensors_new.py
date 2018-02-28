#!/usr/bin/env python
#coding=utf-8
import serial
import binascii
from time import sleep
import logging
import RPi.GPIO as GPIO

def zone_CO2_Temp_Hum(): #Co2、温度、湿度
    ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=0.5)
    CO2 = 0.0
    Temp = 0.0
    Humi = 0.0
    try:
        ser.write("\x02\x03\x00\x00\x00\x03\x05\xf8")
        sleep(0.2)
        count = ser.inWaiting()
        recv = ser.read(count)
        sleep(0.2)
        ser.flushInput()
        while len(recv) == 11 and recv[:1] == '\x02':
            num = binascii.hexlify(recv)
            co2_temp = num[6:10]
            CO2 = int(co2_temp, 16)
            # print(CO2)
            tem_temp = num[10:14]
            tem = int(tem_temp, 16)
            Temp = float(tem) / 100
            # print(Temp)
            hum_temp = num[14:18]
            hum = int(hum_temp, 16)
            Humi = float(hum) / 100
            # print(Humi)
            break
    except UnboundLocalError:
        logging.info("It's the problem of CO2_Temp_Hum sensor")
        CO2 = 0.0
        Temp = 0.0
        Humi = 0.0
    ser.close()
    return CO2, Temp, Humi

def shelf_Water_Tem(): #水温
    ser = serial.Serial('/dev/ttyAMA0',9600,timeout =0.5)
    Water_Temp = 0.0
    try:
        ser.write("\x00\x03\x00\x00\x00\x01\x85\xdb")
        sleep(0.2)
        count = ser.inWaiting()
        rec = ser.read(count)
        sleep(0.2)
        ser.flushInput()
        while len(rec) == 7 and rec[:1] == '\x01':
            num = binascii.hexlify(rec)
            water_temn = num[6:10]
            water_te = int(water_temn, 16)
            if water_te > 2000:
                Water_Temp = -(65535 - water_te) / float(10)
            else:
                Water_Temp = float(water_te) / 10
           # print(Water_Temp)
            break
    except UnboundLocalError:
        logging.info("It's the problem of Water_Temp sensor")
        Water_Temp = 0
    ser.close()
    return Water_Temp

def shelf_PH(): #PH值
    ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=0.5)
    PH_val = 0.0
    try:
        ser.write("\x10\x03\x00\x00\x00\x01\x87\x4b")
        sleep(0.2)
        count = ser.inWaiting()
        recv = ser.read(count)
        sleep(0.2)
        ser.flushInput()
        while len(recv) == 7 and recv[:1] == '\x10':
            num = binascii.hexlify(recv)
            PH_value = num[6:10]
            PH_valu = int(PH_value, 16)
            PH_val = float(PH_valu) / 100
            # print( PH_val)
            break
    except UnboundLocalError:
        logging.info("It's the problem of PH sensor")
        PH_val = 0
    ser.close()
    return PH_val

def shelf_EC():
    ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=0.5)
    EC_val = 0
    try:
        ser.write("\x03\x03\x00\x00\x00\x01\x85\xe8")
        sleep(0.2)
        count = ser.inWaiting()
        recv = ser.read(count)
        sleep(0.2)
        ser.flushInput()
        while len(recv) == 7 and recv[:1] == '\x03':
            num = binascii.hexlify(recv)
            EC_value = num[6:10]
            EC_val = int(EC_value, 16)
            # print( EC_val)
            break
    except UnboundLocalError:
        logging.info("It's the problem of PH sensor")
        EC_val = 0
    ser.close()
    return EC_val


def Light_intensity(layer):
    ser = serial.Serial('/dev/ttyAMA0',9600,timeout =0.5)
    Light = 0
    try:
        if layer==1:
            ser.write("\x04\x03\x00\x06\x00\x01\x64\x5e")
            sleep(0.2)
            count=ser.inWaiting()
            rec=ser.read(count)
            sleep(0.2)
            ser.flushInput()
            while len(rec)==7 and rec[:1]=='\x04':
                num=binascii.hexlify(rec)
                light_temp=num[6:10]
                Light=int(light_temp,16)
               #print(Light)
                break
        elif layer==2:
            ser.write("\x05\x03\x00\x06\x00\x01\x65\x8f")
            sleep(0.2)
            count=ser.inWaiting()
            rec=ser.read(count)
            sleep(0.2)
            ser.flushInput()
            while len(rec)==7 and rec[:1]=='\x05':
                num=binascii.hexlify(rec)
                light_temp=num[6:10]
                Light=int(light_temp,16)
               #print(Light)
                break
        elif layer==3:
            ser.write("\x06\x03\x00\x06\x00\x01\x65\xbc")
            sleep(0.2)
            count=ser.inWaiting()
            rec=ser.read(count)
            sleep(0.2)
            ser.flushInput()
            while len(rec)==7 and rec[:1]=='\x06':
                num=binascii.hexlify(rec)
                light_temp=num[6:10]
                Light=int(light_temp,16)
               #print(Light)
                break
        elif layer==4:
            ser.write("\x07\x03\x00\x06\x00\x01\x64\x6d")
            sleep(0.2)
            count=ser.inWaiting()
            rec=ser.read(count)
            sleep(0.2)
            ser.flushInput()
            while len(rec)==7 and rec[:1]=='\x07':
                num=binascii.hexlify(rec)
                light_temp=num[6:10]
                Light=int(light_temp,16)
               #print(Light)
                break
        elif layer == 5:
            ser.write("\x08\x03\x00\x06\x00\x01\x64\x92")
            sleep(0.2)
            count = ser.inWaiting()
            rec = ser.read(count)
            sleep(0.2)
            ser.flushInput()
            while len(rec) == 7 and rec[:1] == '\x08':
                num = binascii.hexlify(rec)
                light_temp = num[6:10]
                Light = int(light_temp, 16)
                # print(Light)
                break
        elif layer == 6:
            ser.write("\x09\x03\x00\x06\x00\x01\x65\x43")
            sleep(0.2)
            count = ser.inWaiting()
            rec = ser.read(count)
            sleep(0.2)
            ser.flushInput()
            while len(rec) == 7 and rec[:1] == '\x09':
                num = binascii.hexlify(rec)
                light_temp = num[6:10]
                Light = int(light_temp, 16)
                # print(Light)
                break
        else:
            Light=0
            logging.info('No this layer')
    except UnboundLocalError:
        logging.info("It's the problem of Light_intensity sensor")
        Light = 0
    ser.close()
    return Light


def layer_humi(layer):
    ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=0.5)
    Humi_val = 0.0
    try:
        if layer == 1:
            ser.write("\x0a\x03\x00\x00\x00\x02\xc5\x70")
            sleep(0.2)
            count = ser.inWaiting()
            recv = ser.read(count)
            sleep(0.2)
            ser.flushInput()
            if recv == '':
                ser.write("\x0a\x03\x00\x00\x00\x02\xc5\x70")
                count = ser.inWaiting()
                recv = ser.read(count)
                ser.flushInput()
                while len(recv) == 9 and recv[:1] == '\x0a':
                    num = binascii.hexlify(recv)
                    humid_value = num[6:10]
                    Humid_val = int(humid_value, 16)
                    Humi_val = float(Humid_val) / 10
                    break
            else:
                while len(recv) == 9 and recv[:1] == '\x0a':
                    num = binascii.hexlify(recv)
                    humid_value = num[6:10]
                    Humid_val = int(humid_value, 16)
                    Humi_val = float(Humid_val) / 10
                    break
        elif layer==2:
            ser.write("\x0b\x03\x00\x00\x00\x02\xc4\xa1")
            sleep(0.2)
            count = ser.inWaiting()
            recv = ser.read(count)
            sleep(0.2)
            ser.flushInput()
            if recv == '':
                ser.write("\x0b\x03\x00\x00\x00\x02\xc4\xa1")
                count = ser.inWaiting()
                recv = ser.read(count)
                ser.flushInput()
                while len(recv) == 9 and recv[:1] == '\x0b':
                    num = binascii.hexlify(recv)
                    humid_value = num[6:10]
                    Humid_val = int(humid_value, 16)
                    Humi_val = float(Humid_val) / 10
                    break
            else:
                while len(recv) == 9 and recv[:1] == '\x0b':
                    num = binascii.hexlify(recv)
                    humid_value = num[6:10]
                    Humid_val = int(humid_value, 16)
                    Humi_val = float(Humid_val) / 10
                    break
        elif layer==3:
            ser.write("\x0c\x03\x00\x00\x00\x02\xc5\x16")
            sleep(0.2)
            count = ser.inWaiting()
            recv = ser.read(count)
            sleep(0.2)
            ser.flushInput()
            if recv == '':
                ser.write("\x0c\x03\x00\x00\x00\x02\xc5\x16")
                count = ser.inWaiting()
                recv = ser.read(count)
                ser.flushInput()
                while len(recv) == 9 and recv[:1] == '\x0c':
                    num = binascii.hexlify(recv)
                    humid_value = num[6:10]
                    Humid_val = int(humid_value, 16)
                    Humi_val = float(Humid_val) / 10
                    break
            else:
                while len(recv) == 9 and recv[:1] == '\x0c':
                    num = binascii.hexlify(recv)
                    humid_value = num[6:10]
                    Humid_val = int(humid_value, 16)
                    Humi_val = float(Humid_val) / 10
                    break
        elif layer==4:
            ser.write("\x0d\x03\x00\x00\x00\x02\xc4\xc7")
            sleep(0.2)
            count = ser.inWaiting()
            recv = ser.read(count)
            sleep(0.2)
            ser.flushInput()
            if recv == '':
                ser.write("\x0d\x03\x00\x00\x00\x02\xc4\xc7")
                count = ser.inWaiting()
                recv = ser.read(count)
                ser.flushInput()
                while len(recv) == 9 and recv[:1] == '\x0d':
                    num = binascii.hexlify(recv)
                    humid_value = num[6:10]
                    Humid_val = int(humid_value, 16)
                    Humi_val = float(Humid_val) / 10
                    break
            else:
                while len(recv) == 9 and recv[:1] == '\x0d':
                    num = binascii.hexlify(recv)
                    humid_value = num[6:10]
                    Humid_val = int(humid_value, 16)
                    Humi_val = float(Humid_val) / 10
                    break
        elif layer == 5:
            ser.write("\x0e\x03\x00\x00\x00\x02\xc4\xf4")
            sleep(0.2)
            count = ser.inWaiting()
            recv = ser.read(count)
            sleep(0.2)
            ser.flushInput()
            if recv == '':
                ser.write("\x0e\x03\x00\x00\x00\x02\xc4\xf4")
                count = ser.inWaiting()
                recv = ser.read(count)
                ser.flushInput()
                while len(recv) == 9 and recv[:1] == '\x0e':
                    num = binascii.hexlify(recv)
                    humid_value = num[6:10]
                    Humid_val = int(humid_value, 16)
                    Humi_val = float(Humid_val) / 10
                    break
            else:
                while len(recv) == 9 and recv[:1] == '\x0e':
                    num = binascii.hexlify(recv)
                    humid_value = num[6:10]
                    Humid_val = int(humid_value, 16)
                    Humi_val = float(Humid_val) / 10
                    break
        elif layer == 6:
            ser.write("\x0f\x03\x00\x00\x00\x02\xc5\x25")
            sleep(0.2)
            count = ser.inWaiting()
            recv = ser.read(count)
            sleep(0.2)
            ser.flushInput()
            if recv == '':
                ser.write("\x0f\x03\x00\x00\x00\x02\xc5\x25")
                count = ser.inWaiting()
                recv = ser.read(count)
                ser.flushInput()
                while len(recv) == 9 and recv[:1] == '\x0f':
                    num = binascii.hexlify(recv)
                    humid_value = num[6:10]
                    Humid_val = int(humid_value, 16)
                    Humi_val = float(Humid_val) / 10
                    break
            else:
                while len(recv) == 9 and recv[:1] == '\x0f':
                    num = binascii.hexlify(recv)
                    humid_value = num[6:10]
                    Humid_val = int(humid_value, 16)
                    Humi_val = float(Humid_val) / 10
                    break
        else:
            Humi_val=0.0
            logging.info('No this layer')
    except UnboundLocalError:
        logging.info("It's the problem of Humid sensor")
        Humi_val = 0.0
    ser.close()
    return  Humi_val


def water_level():
    # 0--正常  1--过低 2--过高
    shelf_water_high = 19
    shelf_water_low = 26
    water_low = GPIO.input(shelf_water_low)  # 低水位
    water_high = GPIO.input(shelf_water_high)  # 高水位
    if water_low == True and water_high == False:
        logging.info("水箱水位正常")
        ret = 0
    else:
        if water_low == False:
            logging.error("水箱水位过低")
            ret = 1
        if water_high == True:
            logging.error("水箱水位过高")
            ret = 2
    return ret













