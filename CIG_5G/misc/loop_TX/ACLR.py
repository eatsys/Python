#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import socket
import datetime
import time
import telnetlib
import csv
#import result
import re
# ACLR
def ACPtest(ip,sn,type,targpwr,channel,mode,BD,BW,path):
    #"Measuer ACLR"
    Host = ip
    Port = "5023"
    tn = telnetlib.Telnet(Host,Port)
    tn.set_debuglevel(0);
    time.sleep(1)
    tn.read_until(b"SCPI>")
    n = tn.write(b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"INIT:CONT ON" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":CONF:ACP" + b"\r\n")
    n = tn.write(b":CCAR:REF " + channel + "MHz" + b"\r\n")
    tn.read_until(b"SCPI>")
    if BW == "50M" or BW == "100M" :
        n = tn.write(b"RAD:STAN:PRES B"+BW+ b"\r\n")
        tn.read_until(b"SCPI>")
    else:
        print ("****** BW Error")
    n = tn.write(b":POW:RANG:OPT IMM" + b"\r\n") #输入执行的命令
    tn.read_until(b"SCPI>")
    time.sleep(5)
    n = tn.write(b"INIT:CONT OFF"+b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"INIT:REST"+b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":CALCulate:DATA1?" + b"\r\n")
    time.sleep(10)
    result = tn.read_very_eager()
    num = re.sub(r'\s+',"", result)
    num = re.sub(r'>', "", num)
    num = re.sub(r'SCPI', "", num)
    num = num.split(",")
    pwr = num[1]
    LoA = num[4]
    LoB = num[8]
    UpA = num[6]
    UpB = num[10]
    pwr = float(pwr)
    pwr = round(pwr,3)
    print "::::::::ACLR TEST::::::::::::::"
    print "Channel Power:",pwr
    LoA = float(LoA)
    LoA = round(LoA,3)
    LoA = abs(LoA)
    print "LoA",LoA
    LoB = float(LoB)
    LoB = round(LoB,3)
    LoB = abs(LoB)
    print "LoB",LoB
    UpA = float(UpA)
    UpA = round(UpA,3)
    UpA = abs(UpA)
    print "UpA",UpA
    UpB = float(UpB)
    UpB = round(UpB,3)
    UpB = abs(UpB)
    print "UpB",UpB
    #pwr = int(pwr)
    n = tn.write(b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":CALCulate:CLIMits:FAIL?" + b"\r\n")
    time.sleep(1)
    result = tn.read_very_eager()
    #print result
    result = re.sub(r'\s+',"", result)
    result = re.sub(r'>', "", result)
    result = re.sub(r'SCPI', "", result)
    #print result
    if result == str(0):
        res = "Pass"
    else:
        res = "Fail"
    print res
    print "::::::::::::::::::::::"
    #sn = str(sn)
    #type = str(type)
    #mode = str(mode)
    #BD = str(BD)
    targpwr = str(targpwr)
    pwr = str(pwr)
    LoA = str(LoA)
    LoB = str(LoB)
    UpA = str(UpA)
    UpB = str(UpB)
    res = str(res)
    mds = re.sub(r'\.', "_", mode)
    scrname = "ACLR"+"_"+sn+'_'+type+"_"+mds+"_"+BD+"_"+BW+"_"+channel+"_"+path+"_"+res+".png"
    print scrname
    n = tn.write(b':MMEM:STOR:SCR "'+scrname+ b'"\n')
    filename = "log_all.txt"
    with open("../Log/"+filename,'a') as f:
        f.writelines([sn+" ",type+" ",mode+" ",BD+" ",BW+" ",channel+" ",path+" ",targpwr+" ",pwr+" ",LoA+" ",UpA+" ",LoB+" ",UpB+" ",res+"\n"])
    filename = sn+'_'+"ACLR_log.txt"
    with open("../Log/"+filename,'a') as f:
        f.writelines([type+" ",mode+" ",BD+" ",BW+" ",channel+" ",path+" ",targpwr+" ",pwr+" ",LoA+" ",UpA+" ",LoB+" ",UpB+" ",res+"\n"])
    filename = sn+'_'+"ACLR_result.csv"
    with open("../Result/"+filename,'ab+') as f:
        writer = csv.writer(f)
        writer.writerow([type,mode,BD,BW,channel,path,targpwr,pwr,"Adj Lower",LoA])
        writer.writerow([type,mode,BD,BW,channel,path,targpwr,pwr,"Adj Higher",UpA])
        writer.writerow([type,mode,BD,BW,channel,path,targpwr,pwr,"Alt Lower",LoB])
        writer.writerow([type,mode,BD,BW,channel,path,targpwr,pwr,"Alt Higher",UpB])
    tn.close()
    return