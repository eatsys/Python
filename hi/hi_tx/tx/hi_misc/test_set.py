# -*- coding: utf-8 -*-
# @Time    : 2019/1/18 13:23
# @Author  : Ethan
# @FileName: test_set.py
import sys
import os
import socket
import datetime
import time
import telnetlib
import serial
from openpyxl import Workbook
import csv

try:
    ###################################################################
    print '############ WELCOME #############'
    Number = raw_input("SN:")
    sn = "SN_"+ Number
    ###################################################################
    dut_file = load_workbook('./dut_config.xlsx')
    for rows in dut_file:
        if rows[0] == 'ip':
           ip = rows[1]
           print 'DUT IP: ',ip
        elif rows[0] == 'username':
           user = rows[1]
           print 'DUT Username: ',user
        elif rows[0] == 'password':
           pwd = rows[1]
           print 'DUT Password: ',pwd
        elif rows[0] == 'addition1':
           add1 = rows[1]
           print 'Addition Parameters: ',add1
        elif rows[0] == 'addition2':
           add2 = rows[1]
           print 'Addition Parameters: ',add2
        elif rows[0] == 'addition3':
           add3 = rows[1]
           print 'Addition Parameters: ',add3
    ###################################################################
    ###################################################################
    pathloss_file = csv.reader(open('./pathloss.csv'))
    next(pathloss_file)
    for rows in pathloss_file:


        #################################################################
        #################################################################
        print 'INIT SG...'
        Host = sg_ip
        Port = 5023
        tn = telnetlib.Telnet(Host,Port,timeout=3)
        tn.set_debuglevel(0);
        tn.read_until(b"SCPI>")
        n = tn.write(b"\r\n")
        tn.read_until(b"SCPI>")
        n = tn.write(b":SYST:PRES" + b"\r\n")
        #tn.read_until(b"SCPI>")
        #n = tn.write(b":RAD:ARB:TRIG:TYPE:CONT TRIG" + b"\r\n") #设置Trigger Type
        #tn.read_until(b"SCPI>")
        #n = tn.write(b":RAD:ARB:TRIG:EXT:SLOP POS" + b"\r\n") #设置EXT Polarity
        #tn.read_until(b"SCPI>")
        #n = tn.write(b":RAD:ARB:TRIG:EXT:DEL:STAT ON" + b"\r\n") #打开时延
        #tn.read_until(b"SCPI>")
        #n = tn.write(b":RAD:ARB:TRIG:EXT:DEL 11usec" + b"\r\n") #设置时延时间
        ######################################################################
        Keysight_Set.SA(ip,type)
        ##################信号源设置########################################################
        print "**************** Starting Test ********************"
        n = tn.write(b"\r\n")
        tn.read_until(b"SCPI>")
        n = tn.write(b":RAD:ARB:WAV "+ wavef +b"\r\n") #加载波形文件
        tn.read_until(b"SCPI>")
        n = tn.write(b":RAD:ARB ON"+ b"\r\n") #打开ARB开关
        tn.read_until(b"SCPI>")
        n = tn.write(b":FREQ:FIX "+ channel + "MHz" + b"\r\n") #配置信道
        tn.read_until(b"SCPI>")
        n = tn.write(b":OUTP:MOD ON" + b"\r\n") #打开mode开关
        tn.read_until(b"SCPI>")
        n = tn.write(b":OUTP ON" + b"\r\n") #打开RF 开关
        tn.read_until(b"SCPI>")
        #####################################################################################
        #生成测试报告数据文件
        sn = str(sn)
        filename = sn+'_'+"Power_result.csv"
        with open("../Result/"+filename,'ab+') as f:
             writer = csv.writer(f)
             writer.writerow(["Type","Test Mode","Band","BandWith","Frequence(MHZ)","Path","Input Power(dBm)","Output Power(dBm)","Gain(dB)"])
        f.close()
        filename = sn+'_'+"EVM_result.csv"
        with open("../Result/"+filename,'ab+') as f:
             writer = csv.writer(f)
             writer.writerow(["Type","Test Mode","Band","BandWith","Frequence(MHZ)","Path","Input Power(dBm)","Output Power(dBm)","Result (dB)"])
        f.close()
        filename = sn+'_'+"ACLR_result.csv"
        with open("../Result/"+filename,'ab+') as f:
             writer = csv.writer(f)
             writer.writerow(["Type","Test Mode","Band","BandWith","Frequence(MHZ)","Path","Input Power(dBm)","Output Power(dBm)","Range","Result(dBc)"])
        f.close()
        filename = sn+'_'+"OBUE_result.csv"
        with open("../Result/"+filename,'ab+') as f:
             writer = csv.writer(f)
             writer.writerow(["Type","Test Mode","Band","BandWith","Frequence(MHZ)","Path","Input Power(dBm)","Output Power(dBm)","Position","Result"])
        f.close()
        filename = sn+'_'+"OBW_result.csv"
        with open("../Result/"+filename,'ab+') as f:
             writer = csv.writer(f)
             writer.writerow(["Type","Test Mode","Band","BandWith","Frequence(MHZ)","Path","Input Power(dBm)","Output Power(dBm)","Result(MHz)"])
        f.close()
        filename = sn+'_'+"SPUR_result.csv"
        with open("../Result/"+filename,'ab+') as f:
             writer = csv.writer(f)
             writer.writerow(["Type","Test Mode","Band","BandWith","Frequence(MHZ)","Path","Input Power(dBm)","Range","Result(dBm)","Pre(MHz)"])
        f.close()
        filename = sn+'_'+"CCDF_result.csv"
        with open("../Result/"+filename,'ab+') as f:
             writer = csv.writer(f)
             writer.writerow(["Type","Test Mode","Band","BandWith","Frequence(MHZ)","Path","Input Power(dBm)","Output Power(dBm)","Result (dB)"])
        f.close()
        ######################################################
        #amp = float(starf) + abs(float(pathloss))
        n = tn.write(b":POW:OFFS "+ pathloss +"dBm"+ b"\r\n")
        tn.read_until(b"SCPI>")
        x = 0
        while ( starf <= stopf):
            rsamp = float(starf)                     ####################设置测试初始信号强度
            n = tn.write(b":POW "+ str(rsamp) +"dBm"+ b"\r\n")
            tn.read_until(b"SCPI>")
            time.sleep(3)
           #########################################################################################
            Power.powertest(ip,sn,type,rsamp,channel,mode,BD,BW,path)
            print ""
            print "@@@ Power Test Done @@@"
            time.sleep(3)
            EVM.evmtest(ip,sn,type,rsamp,channel,mode,BD,BW,path)
            print ""
            print "@@@ EVM Test Done @@@"
            time.sleep(3)
            ACLR.ACPtest(ip,sn,type,rsamp,channel,mode,BD,BW,path)
            print ""
            print "@@@ ACLR Test Done @@@"
            time.sleep(3)
            OBUE.OBUEtest(ip,sn,type,rsamp,channel,mode,BD,BW,path)
            print ""
            print "@@@ OBUE Test Done @@@"
            time.sleep(3)
            OBW.obwtest(ip,sn,type,rsamp,channel,mode,BD,BW,path)
            print ""
            print "@@@ OBW Test Done @@@"
            SpurCB.spurtest(ip,sn,type,rsamp,channel,mode,BD,BW,path)
            print ""
            print "@@@ Spur Test Done @@@"
            CCDF.ccdftest(ip,sn,type,rsamp,channel,mode,BD,BW,path)
            print ""
            print "@@@ CCDF Test Done @@@"
            starf = float(starf)
            starf = starf + step
            x = x + 1
            print x
        starf = starf - x*float(step)
        print starf
finally:
    time.sleep(1)