#encoding: Utf-8
import sys
import os
import socket
import datetime
import time
import telnetlib
#import commands
import serial
from datetime import date

def ant_start(type):
    ser = serial.Serial("COM12",115200)
    n = ser.write(b"\n") #输入执行的命令
    ser.read_until(b"Squatch1> ")#返回提示符格式
    print("Open ANT Serial: "+ser.portstr )
    time.sleep(1)
    with open("./Channel_set/ANT_Cfg_Catalina_RF0_and_RF1_and_RF2_TX.txt","r") as f:
        print "Load ANT_cfg:"+f.name
        cmd = f.readlines()
        for line in cmd:
            ser.write(line + b"\r\n")
            print line
    ser.read_until(b"Squatch1>")
    print("Send ANT all_cmd done")
    n = ser.write(b"\n") #输入执行的命令
    ser.read_until(b"Squatch1> ")#返回提示符格式
    with open("./Channel_set/ANT_Cfg_4AXC_TO_RF0+RF1+RF2.txt","r") as f:
        print "Load ANT_cfg:"+f.name
        cmd = f.readlines()
        for line in cmd:
            ser.write(line + b"\r\n")          
            print line
    ser.read_until(b"Squatch1>")
    print("Send ANT all_cmd done")
    ser.close()
    time.sleep(3)