#encoding: Utf-8
import sys
import socket
import datetime
import time
import telnetlib
#import commands
#import serial
from datetime import date




def SA(ip,samode):
    Host = ip     #频谱仪连接配置
    #print Host
    #print samode
    Port = "5023"
    tn = telnetlib.Telnet(Host,Port) #频谱仪IP地址和端口设置
    tn.set_debuglevel(0);
    print("Signal Analyzer Connecting...");
    time.sleep(5)
    n = tn.write(b"\r\n") #输入执行的命令
    tn.read_until(b"SCPI>")    #返回提示符格式
    print("Connected")
    #tn.read_until(b"SCPI>")    #返回提示符格式
    n = tn.write(b":SYST:PRES" + b"\n") #输入执行的命令
    print("Reset System...")
    #tn.read_until(b"SCPI>")    #返回提示符格式
    n = tn.write(b"POW:ATT 32" + b"\n") #输入执行的命令
    time.sleep(5)
    #tn.read_until(b"SCPI>")
    print("Reset System Done")
    if samode == "5G":
        samode = "5G"
        n = tn.write(b":INST NR5G" + b"\n") #输入执行的命令
        print("Test Mmode:5G NR")
    elif samode == "TDD":
        samode = "LTEATDD"
        n = tn.write(b"INST:SEL LTEATDD" + b"\n") #输入执行的命令
        print("Test Mmode:TDD")
    else:
        print ("Mode error")
    #tn.read_until(b"SCPI>")
    time.sleep(3)
    return

