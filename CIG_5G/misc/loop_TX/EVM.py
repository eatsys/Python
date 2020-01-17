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

def evmtest(ip,sn,type,targpwr,channel,mode,BD,BW,path):
    #"Measuer EVM"
    Host = ip
    Port = 5023
    tn = telnetlib.Telnet(Host,Port)
    tn.set_debuglevel(0);
    time.sleep(1)
    tn.read_until(b"SCPI>")
    n = tn.write(b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"INIT:CONT ON"+b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":CONF:EVM" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":CCAR:REF " + channel + "MHz" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SERV:EVM:PHA:COMP 0"+b"\r\n")
    tbl = 0
    mcs = 0
    if mode == "NR-TM2":#64QAM
        tbl = 1
        mcs = 27
    elif mode == "NR-TM2a":#256 QAM
        tbl = 2
        mcs = 27
    elif mode == "NR-TM3.1":#64QAM
        tbl = 1
        mcs = 27
    elif mode == "NR-TM3.1a":#256 QAM
        tbl = 2
        mcs = 27
    elif mode == "NR-TM3.2":#16QAM
        tbl = 1
        mcs = 10
    elif mode == "NR-TM3.3":#QPSK
        tbl = 1
        mcs = 0
    print mode,tbl,mcs
    tbl = str(tbl)
    mcs = str(mcs)
    tn.read_until(b"SCPI>")
    n = tn.write(b"EVM:CCAR0:NUMB:PDSC 1"+b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"EVM:CCAR0:PDSC1:MCS:TABL TABL"+ tbl +b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"EVM:CCAR0:PDSC1:MCS "+ mcs +b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"EVM:CCAR0:DC:PUNC 1"+b"\r\n")
    time.sleep(15)
    tn.read_until(b"SCPI>")
    #n = tn.write(b"EVM:CCAR0:DLIN:SYNC:CID:AUTO 1"+b"\r\n")
    #tn.read_until(b"SCPI>")
    #n = tn.write(b":POW:RANG:OPT IMM" + b"\r\n") #输入执行的命令
    #tn.read_until(b"SCPI>")
    print ":::::::::EVM Test:::::::::::::"
    n = tn.write(b"INIT:CONT OFF"+b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"INIT:REST"+b"\r\n")
    time.sleep(5)
    tn.read_until(b"SCPI>")
    n = tn.write(b":POW:EATT:STAT ON" + b"\r\n") #输入执行的命令
    tn.read_until(b"SCPI>")
    n = tn.write(b":POW:RANG:OPT IMM" + b"\r\n") #输入执行的命令
    n = tn.write(b"POW:ATT 32" + b"\n") #输入执行的命令
    time.sleep(20)
    tn.read_until(b"SCPI>")
    n = tn.write(b":CALCulate:DATA1?" + b"\r\n")
    time.sleep(45)
    result = tn.read_very_eager()
    #print result
    num = re.sub(r'\s+>SCPI',"", result)
    num = re.sub(r'>', "", num)
    num = re.sub(r'SCPI', "", num)
    num = num.split(",")
    #print num
    pwr = num[0]
    evm = num[1]
    ppm = num[4]
    pwr = float(pwr)
    pwr = round(pwr,3)
    print "::::::::::::::::::::::"
    print "Channel Power:",pwr
    evm = float(evm)
    evm = round(evm,3)
    print "EVM",evm
    targpwr = float(targpwr)
    ppm = float(ppm)
    ppm = round(ppm,5)
    print "SymClk Err:",ppm
    n = tn.write(b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":CALCulate:CLIMits:FAIL?" + b"\r")
    time.sleep(1)
    result = tn.read_very_eager()
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
    pwr = str(pwr)
    evm = str(evm)
    ppm = str(ppm)
    res = str(res)
    targpwr = str(targpwr)
    mds = re.sub(r'\.', "_", mode)
    scrname = "EVM"+"_"+sn+'_'+type+"_"+mds+"_"+BD+"_"+BW+"_"+channel+"_"+path+"_"+res+".png"
    print scrname
    n = tn.write(b':MMEM:STOR:SCR "'+scrname+ b'"\n')
    filename = "log_all.txt"
    with open("../Log/"+filename,'a') as f:
        f.writelines([sn+" ",type+" ",mode+" ",BD+" ",BW+" ",channel+" ",path+" ",targpwr+" ",pwr+" ",evm+" ",ppm+" ",res+"\n"])
    filename = sn+'_'+"EVM_log.txt"
    with open("../Log/"+filename,'a') as f:
        f.writelines([type+" ",mode+" ",BD+" ",BW+" ",channel+" ",path+" ",targpwr+" ",pwr+" ",evm+" ",ppm+" ",res+"\n"])
    filename = sn+'_'+"EVM_result.csv"
    with open("../Result/"+filename,'ab+') as f:
        writer = csv.writer(f)
        writer.writerow([type,mode,BD,BW,channel,path,targpwr,pwr,evm])
    tn.close()
    return