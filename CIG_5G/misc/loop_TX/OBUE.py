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

def OBUEtest(ip,sn,type,targpwr,channel,mode,BD,BW,path):
    #"Measuer ACLR"
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
    n = tn.write(b":CONF:SEM" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":CCAR:REF " + channel + "MHz" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SEM:AVER ON " + b"\r\n")
    tn.read_until(b"SCPI>")
    if BW == "50M" or BW == "100M":
        n = tn.write(b"RAD:STAN:PRES B"+BW+ b"\r\n")
        tn.read_until(b"SCPI>")
    else:
        print ("********** BW Error")
    n = tn.write(b":POW:RANG:OPT IMM" + b"\r\n") #输入执行的命令
    tn.read_until(b"SCPI>")
    n = tn.write(b"INIT:CONT OFF"+b"\r\n")
    #tn.read_until(b"SCPI>")
    #n = tn.write(b"SEM:OFFS1:LIST:SIDE NEG,NEG,NEG" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"INIT:REST"+b"\r\n")
    time.sleep(10)
    mds = re.sub(r'\.', "_", mode)
    scrname = "OBUE_"+sn+'_'+type+"_"+mds+"_"+BD+"_"+BW+"_"+channel+"_"+path+".png"
    print scrname
    n = tn.write(b':MMEM:STOR:SCR "'+scrname+ b'"\n')
    n = tn.write(b":CALCulate:DATA1?" + b"\r\n")
    time.sleep(10)
    result = tn.read_very_eager()
    num = re.sub(r'\s+',"", result)
    num = re.sub(r'>', "", num)
    num = re.sub(r'SCPI', "", num)
    num = num.split(",")
    pwr = num[0]
    LoA = num[13]
    LoB = num[23]
    LoC = num[33]
    LoD = num[43]
    UpA = num[18]
    UpB = num[28]
    UpC = num[38]
    UpD = num[48]
    pwr = float(pwr)
    pwr = round(pwr,3)
    print "::::::::OBUE TEST::::::::::::::"
    print "Channel Power:",pwr
    LoA = float(LoA)
    LoA = round(LoA,3)
    print "LoA",LoA
    LoB = float(LoB)
    LoB = round(LoB,3)
    print "LoB",LoB
    LoC = float(LoC)
    LoC = round(LoC,3)
    print "LoC",LoC
    LoD = float(LoD)
    LoD = round(LoD,3)
    print "LoD",LoD
    UpA = float(UpA)
    UpA = round(UpA,3)
    print "UpA",UpA
    UpB = float(UpB)
    UpB = round(UpB,3)
    print "UpB",UpB
    UpC = float(UpC)
    UpC = round(UpC,3)
    print "UpC",UpC
    UpD = float(UpD)
    UpD = round(UpD,3)
    print "UpD",UpD
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
    targpwr = str(targpwr)
    pwr = str(pwr)
    LoA = str(LoA)
    LoB = str(LoB)
    LoC = str(LoC)
    LoD = str(LoD)
    UpA = str(UpA)
    UpB = str(UpB)
    UpC = str(UpC)
    UpD = str(UpD)
    res = str(res)
    filename = "log_all.txt"
    with open("../Log/"+filename,'a') as f:
        f.writelines([sn+" ",type+" ",mode+" ",BD+" ",BW+" ",channel+" ",path+" ",targpwr+" ",pwr+" ",LoA+" ",LoB+" ",LoC+" ",LoD+" ",UpA+" ",UpB+" ",UpC+" ",UpD+" ",res+"\n"])
    filename = sn+'_'+"OBUE_log.txt"
    with open("../Log/"+filename,'a') as f:
        f.writelines([type+" ",mode+" ",BD+" ",BW+" ",channel+" ",path+" ",targpwr+" ",pwr+" ",LoA+" ",LoB+" ",LoC+" ",LoD+" ",UpA+" ",UpB+" ",UpC+" ",UpD+" ",res+"\n"])
    filename = sn+'_'+"OBUE_result.csv"
    with open("../Result/"+filename,'ab+') as f:
        writer = csv.writer(f)
        writer.writerow([type,mode,BD,BW,channel,path,targpwr,pwr,"Range 1 Lower Side Margin",LoA])
        writer.writerow([type,mode,BD,BW,channel,path,targpwr,pwr,"Range 1 Higher Side Margin",UpA])
        writer.writerow([type,mode,BD,BW,channel,path,targpwr,pwr,"Range 2 Lower Side Margin",LoB])
        writer.writerow([type,mode,BD,BW,channel,path,targpwr,pwr,"Range 2 Higher Side Margin",UpB])
        writer.writerow([type,mode,BD,BW,channel,path,targpwr,pwr,"Range 3 Lower Side Margin",LoC])
        writer.writerow([type,mode,BD,BW,channel,path,targpwr,pwr,"Range 3 Higher Side Margin",UpC])
        writer.writerow([type,mode,BD,BW,channel,path,targpwr,pwr,"Range 4 Lower Side Margin",LoD])
        writer.writerow([type,mode,BD,BW,channel,path,targpwr,pwr,"Range 4 Higher Side Margin",UpD])
    tn.close()
    return