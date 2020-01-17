#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import socket
import datetime
import time
import telnetlib
import csv
import re


def ccdftest(ip,sn,type,targpwr,channel,mode,BD,BW,path):
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
    n = tn.write(b":CONF:PST" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"PST:COUN 2000000" + b"\r\n")
    #tn.read_until(b"SCPI>")
    #n = tn.write(b":INIT:OBW" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":CCAR:REF " + channel + "MHz" + b"\r\n")
    #tn.read_until(b"SCPI>")
    #if BW == "50M" or BW == "100M" :
    #    n = tn.write(b"RAD:STAN:PRES B"+BW+ b"\r\n")
    #    tn.read_until(b"SCPI>")
    #else:
    #    print ("******** BW Error")
    n = tn.write(b":POW:RANG:OPT IMM" + b"\r\n") #输入执行的命令
    tn.read_until(b"SCPI>")
    time.sleep(5)
    n = tn.write(b"INIT:CONT OFF"+b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"INIT:REST"+b"\r\n")
    time.sleep(20)
    tn.read_until(b"SCPI>")
    n = tn.write(b":CALCulate:DATA1?" + b"\r\n")
    time.sleep(5)
    result = tn.read_very_eager() 
    num = re.sub(r'\s+',"", result)
    num = re.sub(r'>', "", num)
    num = re.sub(r'SCPI', "", num)
    num = num.split(",")
    print num
    pwr = float(num[0])
    pwr = round(pwr,2) 
    dB0 = float(num[1])
    dB0 = round(dB0,2)
    P10 = float(num[2])
    P10 = round(P10,2)
    P1 = float(num[3])
    P1 = round(P1,2)
    P0_1 = float(num[4])
    P0_1 = round(P0_1,2)
    P0_01 = float(num[5])
    P0_01 = round(P0_01,2)
    P0_001 = float(num[6])
    P0_001 = round(P0_001,2)
    P0_0001 = float(num[7])
    P0_0001 = round(P0_0001,2)
    PK = float(num[8])
    PK = round(PK,2)
    print "::::::::CCDF TEST::::::::::::::"
    print "Power:",pwr
    print "at 0 dB:",dB0
    print "10.0%:",P10
    print "1.0%:",P1
    print "0.1%:",P0_1
    print "0.01%:",P0_01
    print "0.001%:",P0_001
    print "0.0001%",P0_0001
    print "Peak",PK
    print "::::::::::::::::::::::"
    pwr =str(pwr)
    targpwr = str(targpwr)
    channel = str(channel)
    dB0 = str(dB0)
    P10 = str(P10)
    P1 = str(P1)
    P0_1 = str(P0_1)
    P0_01 = str(P0_01)
    P0_001= str(P0_001)
    P0_0001 = str(P0_0001)
    PK = str(PK)
    mds = re.sub(r'\.', "_", mode)
    scrname = "CCDF"+"_"+sn+'_'+type+"_"+mds+"_"+BD+"_"+BW+"_"+channel+"MHz_"+path+".png"
    print scrname
    n = tn.write(b':MMEM:STOR:SCR "'+scrname+ b'"\n')
    filename = "log_all.txt"
    with open("../Log/"+filename,'a') as f1:
        f1.writelines([sn+" ",type+" ",mode+" ",BD+" ",BW+" ",channel+" ",path+" ",targpwr+" ",pwr+"\n"])
    f1.close()
    filename = sn+'_'+"CCDF_log.txt"
    with open("../Log/"+filename,'a') as f2:
        f2.writelines([type+" ",mode+" ",BD+" ",BW+" ",channel+" ",path+" ",targpwr+" ",pwr+"\n"])
    f2.close()
    filename = sn+'_'+"CCDF_result.csv"
    with open("../Result/"+filename,'ab+') as f3:
        writer = csv.writer(f3)
        #writer.writerow([type,mode,BD,BW,channel,path,targpwr,pwr,dB0])
        #writer.writerow([type,mode,BD,BW,channel,path,targpwr,pwr,P10])
        #writer.writerow([type,mode,BD,BW,channel,path,targpwr,pwr,P1])
        #writer.writerow([type,mode,BD,BW,channel,path,targpwr,pwr,P0_1])
        writer.writerow([type,mode,BD,BW,channel,path,targpwr,pwr,P0_01])
        #writer.writerow([type,mode,BD,BW,channel,path,targpwr,pwr,P0_001])
        #writer.writerow([type,mode,BD,BW,channel,path,targpwr,pwr,P0_0001])
        #writer.writerow([type,mode,BD,BW,channel,path,targpwr,pwr,PK])
    f3.close()
    tn.close()
    time.sleep(1)
    return

