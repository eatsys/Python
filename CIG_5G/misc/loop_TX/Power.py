#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import socket
import datetime
import time
import telnetlib
import csv
import re


def powertest(ip,sn,type,targpwr,channel,mode,BD,BW,path):
########"Measuer Power"###########
    Host = ip
    Port = "5023"
    tn = telnetlib.Telnet(Host,Port)
    tn.set_debuglevel(0);
    time.sleep(1)
    n = tn.write(b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":INST NR5G" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"INIT:CONT ON" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":CONF:CHP" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":INIT:CHP" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":CHP:AVER:COUN 15" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":CCAR:REF " + channel + "MHz" + b"\r\n")
    tn.read_until(b"SCPI>")
    if BW == "50M" or BW == "100M":
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
    time.sleep(15)
    result = tn.read_very_eager() 
    num = re.sub(r'\s+',"", result)
    num = re.sub(r'>', "", num)
    num = re.sub(r'SCPI', "", num)
    num = num.split(",")
    pwr = float(num[0])
    pwr = round(pwr,3)
    print ":::::::::Power Test:::::::::::::"
    print "Power:",pwr
    targpwr = int(targpwr)
    delta =  pwr - targpwr
    if delta >=-2 and delta <=2:
        res = "Pass"
    else:
        res = "Fail"
    print res
    print "::::::::::::::::::::::::::::::::"
    print "Output Files"
    pwr = str(pwr)
    res = str(res)
    targpwr = str(targpwr)
    mds = re.sub(r'\.', "_", mode)
    scrname = "Power"+"_"+sn+'_'+type+"_"+mds+"_"+BD+"_"+BW+"_"+channel+"_"+path+"_"+res+".png"
    print scrname
    n = tn.write(b':MMEM:STOR:SCR "'+scrname+ b'"\n')
    filename = "log_all.txt"
    with open("../Log/"+filename,'a') as f1:
        f1.writelines([sn+" ",type+" ",mode+" ",BD+" ",BW+" ",channel+" ",path+" ",targpwr+" ",pwr+" ",res+"\n"])
    f1.close()
    filename = sn+'_'+"Power_log.txt"
    with open("../Log/"+filename,'a') as f2:
        f2.writelines([type+" ",mode+" ",BD+" ",BW+" ",channel+" ",path+" ",targpwr+" ",pwr+" ",res+"\n"])
    f2.close()
    filename = sn+'_'+"Power_result.csv"
    with open("../Result/"+filename,'ab+') as f3:
        writer = csv.writer(f3)
        writer.writerow([type,mode,BD,BW,channel,path,targpwr,pwr,delta])
    f3.close()
    print filename
    tn.close()
    time.sleep(1)
    return

