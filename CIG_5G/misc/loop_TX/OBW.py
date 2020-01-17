#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import socket
import datetime
import time
import telnetlib
import csv
import re


def obwtest(ip,sn,type,targpwr,channel,mode,BD,BW,path):
########"Measuer obwtest"###########
    Host = ip
    Port = "5023"
    tn = telnetlib.Telnet(Host,Port)
    tn.set_debuglevel(0);
    time.sleep(1)
    tn.read_until(b"SCPI>")
    n = tn.write(b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"INIT:CONT ON"+b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":CONF:OBW" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":INIT:OBW" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":CCAR:REF " + channel + "MHz" + b"\r\n")
    tn.read_until(b"SCPI>")
    if BW == "50M" or BW == "100M" :
        n = tn.write(b"RAD:STAN:PRES B"+BW+ b"\r\n")
        tn.read_until(b"SCPI>")
    else:
        print ("******** BW Error")
    n = tn.write(b":POW:RANG:OPT IMM" + b"\r\n") #输入执行的命令
    tn.read_until(b"SCPI>")
    time.sleep(5)
    n = tn.write(b"INIT:CONT OFF"+b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"INIT:REST"+b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":CALCulate:DATA1?" + b"\r\n")
    time.sleep(13)
    result = tn.read_very_eager() 
    num = re.sub(r'\s+',"", result)
    num = re.sub(r'>', "", num)
    num = re.sub(r'SCPI', "", num)
    num = num.split(",")
    obw = float(num[0])
    obw = obw/1000000
    obw = round(obw,3)
    pwr = float(num[1])
    pwr = round(pwr,3) 
    print "::::::::OBW TEST::::::::::::::"
    print "OBW:",obw
    print "Power:",pwr
    if BW > obw:
        res = "Pass"
    else:
        res = "Fail"
    print res
    print "::::::::::::::::::::::"
    targpwr =str(targpwr)
    obw =str(obw)
    pwr = str(pwr)
    res = str(res)
    mds = re.sub(r'\.', "_", mode)
    scrname = "OBW"+"_"+sn+'_'+type+"_"+mds+"_"+BD+"_"+BW+"_"+channel+"MHz_"+path+"_"+res+".png"
    print scrname
    n = tn.write(b':MMEM:STOR:SCR "'+scrname+ b'"\n')
    filename = "log_all.txt"
    with open("../Log/"+filename,'a') as f1:
        f1.writelines([sn+" ",type+" ",mode+" ",BD+" ",BW+" ",channel+" ",path+" ",targpwr+" ",pwr+" ",obw+" ",res+"\n"])
    f1.close()
    filename = sn+'_'+"OBW_log.txt"
    with open("../Log/"+filename,'a') as f2:
        f2.writelines([type+" ",mode+" ",BD+" ",BW+" ",channel+" ",path+" ",targpwr+" ",pwr+" ",obw+" ",res+"\n"])
    f2.close()
    filename = sn+'_'+"OBW_result.csv"
    with open("../Result/"+filename,'ab+') as f3:
        writer = csv.writer(f3)
        writer.writerow([type,mode,BD,BW,channel,path,targpwr,pwr,obw])
    f3.close()
    tn.close()
    time.sleep(1)
    return

