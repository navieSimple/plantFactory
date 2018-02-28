#!/usr/bin/env python
#coding=utf-8
import serial
import binascii
from time import sleep
import logging 

def CO2_Temp_Hum(): 
    
    ser = serial.Serial('/dev/ttyAMA0',9600,timeout =0.5)
    try:
        ser.write("\x02\x03\x00\x00\x00\x03\x05\xf8")
        sleep(0.2)
        count=ser.inWaiting()
        recv=ser.read(count)
        sleep(0.2)
        ser.flushInput()
        while len(recv)==11 and recv[:1]=='\x02':
            num=binascii.hexlify(recv)
            co2_temp=num[6:10]
            CO2=int(co2_temp,16)
           #print(CO2)
            tem_temp=num[10:14]
            tem=int(tem_temp,16)
            Temp=float(tem)/100
           #print(Temp)
            hum_temp=num[14:18]
            hum=int(hum_temp,16)
            Humi=float(hum)/100
           #print(Humi)
            break
        return CO2, Temp, Humi
    except UnboundLocalError:
        logging.info("It's the problem of CO2_Temp_Hum sensor")
    ser.close()

def Water_Tem(a):  
    ser = serial.Serial('/dev/ttyAMA0',9600,timeout =0.5)
    try:
        if a==1:
            ser.write("\x0a\x03\x00\x00\x00\x02\xc5\x70")
            sleep(0.2)
            count=ser.inWaiting()
            rec=ser.read(count)
            sleep(0.2)
            ser.flushInput()
            while len(rec)==9 and rec[:1]=='\x0a':
                num=binascii.hexlify(rec)
                water_temn=num[6:10]
                water_te=int(water_temn,16)
                if water_te>2000:
                    Water_Temp=-(65535-water_te)/float(10)
                else:
                    Water_Temp=float(water_te)/10
                print(Water_Temp)
                break
        elif a==2:
            ser.write("\x0e\x03\x00\x00\x00\x02\xc4\xf4")
            sleep(0.2)
            count=ser.inWaiting()
            rec=ser.read(count)
            sleep(0.2)
            ser.flushInput()
            while len(rec)==9 and rec[:1]=='\x0e':
                num=binascii.hexlify(rec)
                water_temn=num[6:10]
                water_te=int(water_temn,16)
                if water_te>2000:
                    Water_Temp=-(65535-water_te)/float(10)
                else:
                    Water_Temp=float(water_te)/10
                print(Water_Temp)
                break
        elif a==3:
            ser.write("\x0c\x03\x00\x00\x00\x02\xc5\x16")
            sleep(0.2)
            count=ser.inWaiting()
            rec=ser.read(count)
            sleep(0.2)
            ser.flushInput()
            while len(rec)==9 and rec[:1]=='\x0c':
                num=binascii.hexlify(rec)
                water_temn=num[6:10]
                water_te=int(water_temn,16)
                if water_te>2000:
                    Water_Temp=-(65535-water_te)/float(10)
                else:
                    Water_Temp=float(water_te)/10
                print(Water_Temp)
                break
        elif a==4:
            ser.write("\x0d\x03\x00\x00\x00\x02\xc4\xc7")
            sleep(0.2)
            count=ser.inWaiting()
            rec=ser.read(count)
            sleep(0.2)
            ser.flushInput()
            while len(rec)==9 and rec[:1]=='\x0d':
                num=binascii.hexlify(rec)
                water_temn=num[6:10]
                water_te=int(water_temn,16)
                if water_te>2000:
                    Water_Temp=-(65535-water_te)/float(10)
                else:
                    Water_Temp=float(water_te)/10
                print(Water_Temp)
                break
        else:
            Water_Temp=0
            print('No this shelf')
        return Water_Temp
    except UnboundLocalError:
        logging.info("It's the problem of Water_Tem sensor")
    ser.close()

def Light_intensity(b):    
    ser = serial.Serial('/dev/ttyAMA0',9600,timeout =0.5)
    try:
        if b==1:
            ser.write("\x03\x03\x00\x06\x00\x01\x65\xe9")
            sleep(0.2)
            count=ser.inWaiting()
            rec=ser.read(count)
            sleep(0.2)
            ser.flushInput()
            while len(rec)==7 and rec[:1]=='\x03':
                num=binascii.hexlify(rec)
                light_temp=num[6:10]
                Light=int(light_temp,16)
               #print(Light)
                break
        elif b==2:
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
        elif b==3:
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
        elif b==4:
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
        else:
            Light=0
            print('No this shelf')
        return Light
    except UnboundLocalError:
        logging.info("It's the problem of Light_intensity sensor")
    ser.close()

def Water_lev(c):    
    ser = serial.Serial('/dev/ttyAMA0',9600,timeout =0.5)
    try:
        if c==1:
            ser.write("\x01\x03\x00\x00\x00\x01\x84\x0a")
            sleep(0.2)
            count=ser.inWaiting()
            rec=ser.read(count)
            sleep(0.2)
            ser.flushInput()
            while len(rec)==7 and rec[:1]=='\x01':
                num=binascii.hexlify(rec)
                water_temp=num[6:10]
                water_le=int(water_temp,16)
                Water_le=float(water_le)*3/2000
               #print(Water_lec)
                break
        elif c==2:
            ser.write("\x01\x03\x00\x00\x00\x01\x84\x0a")
            sleep(0.2)
            count=ser.inWaiting()
            rec=ser.read(count)
            sleep(0.2)
            ser.flushInput()
            while len(rec)==7 and rec[:1]=='\x01':
                num=binascii.hexlify(rec)
                water_temp=num[6:10]
                water_le=int(water_temp,16)
                Water_le=float(water_le)*3/2000
               #print(Water_lec)
                break
        elif c==3:
            ser.write("\x01\x03\x00\x00\x00\x01\x84\x0a")
            sleep(0.2)
            count=ser.inWaiting()
            rec=ser.read(count)
            sleep(0.2)
            ser.flushInput()
            while len(rec)==7 and rec[:1]=='\x01':
                num=binascii.hexlify(rec)
                water_temp=num[6:10]
                water_le=int(water_temp,16)
                Water_le=float(water_le)*3/2000
               #print(Water_lec)
                break
        elif c==4:
            ser.write("\x01\x03\x00\x00\x00\x01\x84\x0a")
            sleep(0.2)
            count=ser.inWaiting()
            rec=ser.read(count)
            sleep(0.2)
            ser.flushInput()
            while len(rec)==7 and rec[:1]=='\x01':
                num=binascii.hexlify(rec)
                water_temp=num[6:10]
                water_le=int(water_temp,16)
                Water_le=float(water_le)*3/2000
               #print(Water_le)
                break
        else:
            Water_le=0
            print('No this shelf')
        return Water_le
    except UnboundLocalError:
        logging.info("It's the problem of Water_lev sensor")
    ser.close()



#CO2,Temp,Humi=CO2_Temp_Hum()              
#a=input("Enter value from 1 to 4:")   
#Water_T=Water_Tem(a)                  
#b=input("Enter value from 1 to 4:")
#Light=Light_intensity(b) 
#print(Light)             
#c=input("Enter value from 1 to 4:")
#Water_L=Water_lev(a)                 