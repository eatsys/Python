#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import socket
import datetime
import time
import telnetlib
import csv
import re

def spurtest(ip,sn,type,targpwr,channel,mode,BD,BW,path):
########"Measuer Powertest"###########
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
    n = tn.write(b":CONF:CHP" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":INIT:CHP" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":CCAR:REF " + channel + "MHz" + b"\r\n")
    tn.read_until(b"SCPI>")
    if BW == "50M" or BW == "100M" :
        n = tn.write(b"RAD:STAN:PRES B"+BW+ b"\r\n")
        tn.read_until(b"SCPI>")
    else:
        print ("********* BW Error")
    n = tn.write(b":CHP:AVER:COUNt 10" + b"\r\n")
    tn.read_until(b"SCPI>")
    time.sleep(3)
    n = tn.write(b"INIT:CONT OFF"+b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"INIT:REST"+b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":POW:RANG:OPT IMM" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":CALCulate:DATA1?" + b"\r\n")
    time.sleep(2)
    result = tn.read_very_eager() 
    num = re.sub(r'\s+',"", result)
    num = re.sub(r'>', "", num)
    num = re.sub(r'SCPI', "", num)
    num = num.split(",")
    pwr = float(num[0])
    pwr = round(pwr,3)
    print "Power:",pwr
    time.sleep(3)
#############################频谱仪设置########################
    n = tn.write(b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"CONFigure:SPURious" + b"\r\n") #输入执行的命令
    tn.read_until(b"SCPI>")
    n = tn.write(b"INIT:CONT OFF"+b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"INPut:COUPling DC"+b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPURious:AVERage:COUNt 1" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"POW:RF:RANGE:OPT:ATT COMB" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"POW:RANGE:OPTimize IMMediate" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"TRIG:SPUR:SOUR FRAM" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"TRIG:FRAM:PER 10 ms" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"TRIG:RFB:LEV:ABS -24.7 dBm" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:DET AVER" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:PEAK:EXC 6" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:PEAK:THReshold -130" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:STATE ON,OFF,OFF,OFF,OFF,OFF,OFF,OFF" + b"\r\n")
#############################SPUR:9KHz-150KHZ########################
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:BAND:RES 1KHZ" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPURious:BANDwidth:VIDeo:AUTO ON" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:FREQ:START 9KHz" + b"\r\n")#测试起始频率
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:FREQ:STOP 150KHz" + b"\r\n")#测试结束频率
    tn.read_until(b"SCPI>")
    n = tn.write(b"CALC:SPUR:LIM:ABS:DATA -36dBm" + b"\r\n")#判定条件Limit
    tn.read_until(b"SCPI>")
    n = tn.write(b"CALC:SPUR:LIM:ABS:DATA:STOP -36dBm" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:ATT:AUTO 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:ATT 0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"POW:ATT 0" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":INIT:CONT ON" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":INITiate:RESTart" + b"\r\n")
    tn.read_until(b"SCPI>")
    time.sleep(5)
    n = tn.write(b":INIT:CONT OFF" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":FETCh:SPURious1?" + b"\r\n")
    time.sleep(3)
    result = tn.read_very_eager() 
    num = re.sub(r'\s+',"", result)
    num = re.sub(r'>', "", num)
    num = re.sub(r'SCPI', "", num)
    num = num.split(",")
    amp = [float(i) for i in num[4::6]]
    amp = [round(i,2) for i in amp]
    #print amp
    spur = max(amp)
    print ":::::::::Spur CB:::::::::::::"
    print "SPUR:",spur,"dBm"
    j = amp.index(spur)
    #print j
    freq = [float(i) for i in num[3::6]]
    freq = [i/1000000 for i in freq]
    freq = [round(i,3) for i in freq]
    freq = freq[j]
    print "Freq:",freq,"MHz"
    limit = [float(i) for i in num[5::6]]
    limit = [round(i,2) for i in limit]
    limit = limit[j]
    print "limit:",limit,"dBm"
    if spur < limit:
        res = "Pass"
    else:
        res = "Fail"
    print "Result:",res
    print "::::::::::::::::::::::"
    targpwr = str(targpwr)
    spur = str(spur)
    freq = str(freq)
    limit = str(limit)
    mds = re.sub(r'\.', "_", mode)
    scrname = "SPUR"+"_"+sn+'_'+type+"_"+mds+"_"+BD+"_"+BW+"_"+channel+"MHz_"+path+"_9KHz-150KHz_"+res+".png"
    print scrname
    n = tn.write(b':MMEM:STOR:SCR "'+scrname+ b'"\n')
    filename = "log_all.txt"
    with open("../Log/"+filename,'a') as f1:
        f1.writelines([sn+" ",type+" ",mode+" ",BD+" ",BW+" ",channel+" ",path+" ",targpwr+" ","9KHz-150KHz ",spur+" ",freq+"MHz ",res+"\n"])
    f1.close()
    filename = sn+'_'+"SPUR_log.txt"
    with open("../Log/"+filename,'a') as f2:
        f2.writelines([sn+" ",type+" ",mode+" ",BD+" ",BW+" ",channel+" ",path+" ",targpwr+" ","9KHz-150KHz ",spur+" ",freq+"MHz ",res+"\n"])
    f2.close()
    filename = sn+'_'+"SPUR_result.csv"
    with open("../Result/"+filename,'ab+') as f3:
        writer = csv.writer(f3)
        writer.writerow([type,mode,BD,BW,channel,path,targpwr,"9KHz-150KHz",spur,freq,res])
    f3.close()
#############################SPUR:150kHz-30MHz########################
    n = tn.write(b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:BAND:RES 10KHZ" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPURious:BANDwidth:VIDeo:AUTO ON" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:FREQ:START 150KHz" + b"\r\n")#测试起始频率
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:FREQ:STOP 30MHz" + b"\r\n")#测试结束频率
    tn.read_until(b"SCPI>")
    n = tn.write(b"CALC:SPUR:LIM:ABS:DATA -36dBm" + b"\r\n")#判定条件Limit
    tn.read_until(b"SCPI>")
    n = tn.write(b"CALC:SPUR:LIM:ABS:DATA:STOP -36dBm" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:ATT:AUTO 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:ATT 0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"POW:ATT 0" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":INIT:CONT ON" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":INITiate:RESTart" + b"\r\n")
    tn.read_until(b"SCPI>")
    time.sleep(5)
    n = tn.write(b":INIT:CONT OFF" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":FETCh:SPURious1?" + b"\r\n")
    time.sleep(3)
    result = tn.read_very_eager() 
    num = re.sub(r'\s+',"", result)
    num = re.sub(r'>', "", num)
    num = re.sub(r'SCPI', "", num)
    num = num.split(",")
    amp = [float(i) for i in num[4::6]]
    amp = [round(i,2) for i in amp]
    #print amp
    spur = max(amp)
    print "::::::::::::::::::::::"
    print "SPUR:",spur,"dBm"
    j = amp.index(spur)
    #print j
    freq = [float(i) for i in num[3::6]]
    freq = [i/1000000 for i in freq]
    freq = [round(i,3) for i in freq]
    freq = freq[j]
    print "Freq:",freq,"MHz"
    limit = [float(i) for i in num[5::6]]
    limit = [round(i,2) for i in limit]
    limit = limit[j]
    print "limit:",limit,"dBm"
    if spur < limit:
        res = "Pass"
    else:
        res = "Fail"
    print "Result:",res
    print "::::::::::::::::::::::"
    spur = str(spur)
    freq = str(freq)
    limit = str(limit)
    mds = re.sub(r'\.', "_", mode)
    scrname = "SPUR"+"_"+sn+'_'+type+"_"+mds+"_"+BD+"_"+BW+"_"+channel+"MHz_"+path+"_150KHz-30MHz_"+res+".png"
    print scrname
    n = tn.write(b':MMEM:STOR:SCR "'+scrname+ b'"\n')
    filename = "log_all.txt"
    with open("../Log/"+filename,'a') as f1:
        f1.writelines([sn+" ",type+" ",mode+" ",BD+" ",BW+" ",channel+" ",path+" ",targpwr+" ","150KHz-30MHz ",spur+" ",freq+"MHz ",res+"\n"])
    f1.close()
    filename = sn+'_'+"SPUR_log.txt"
    with open("../Log/"+filename,'a') as f2:
        f2.writelines([sn+" ",type+" ",mode+" ",BD+" ",BW+" ",channel+" ",path+" ",targpwr+" ","150KHz-30MHz ",spur+" ",freq+"MHz ",res+"\n"])
    f2.close()
    filename = sn+'_'+"SPUR_result.csv"
    with open("../Result/"+filename,'ab+') as f3:
        writer = csv.writer(f3)
        writer.writerow([type,mode,BD,BW,channel,path,targpwr,"150KHz-30MHz",spur,freq,res])
    f3.close()
#############################SPUR:30MHz-1GHz########################
    n = tn.write(b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:BAND:RES 100KHZ" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPURious:BANDwidth:VIDeo:AUTO ON" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:FREQ:START 30MHz" + b"\r\n")#测试起始频率
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:FREQ:STOP 1000MHz" + b"\r\n")#测试结束频率
    tn.read_until(b"SCPI>")
    n = tn.write(b"CALC:SPUR:LIM:ABS:DATA -36dBm" + b"\r\n")#判定条件Limit
    tn.read_until(b"SCPI>")
    n = tn.write(b"CALC:SPUR:LIM:ABS:DATA:STOP -36dBm" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:ATT:AUTO 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:ATT 0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"POW:ATT 0" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":INIT:CONT ON" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":INITiate:RESTart" + b"\r\n")
    tn.read_until(b"SCPI>")
    time.sleep(5)
    n = tn.write(b":INIT:CONT OFF" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":FETCh:SPURious1?" + b"\r\n")
    time.sleep(3)
    result = tn.read_very_eager() 
    num = re.sub(r'\s+',"", result)
    num = re.sub(r'>', "", num)
    num = re.sub(r'SCPI', "", num)
    num = num.split(",")
    amp = [float(i) for i in num[4::6]]
    amp = [round(i,2) for i in amp]
    #print amp
    spur = max(amp)
    print "::::::::::::::::::::::"
    print "SPUR:",spur,"dBm"
    j = amp.index(spur)
    #print j
    freq = [float(i) for i in num[3::6]]
    freq = [i/1000000 for i in freq]
    freq = [round(i,2) for i in freq]
    freq = freq[j]
    print "Freq:",freq,"MHz"
    limit = [float(i) for i in num[5::6]]
    limit = [round(i,2) for i in limit]
    limit = limit[j]
    print "limit:",limit,"dBm"
    if spur < limit:
        res = "Pass"
    else:
        res = "Fail"
    print "Result:",res
    print "::::::::::::::::::::::"
    spur = str(spur)
    freq = str(freq)
    limit = str(limit)
    mds = re.sub(r'\.', "_", mode)
    scrname = "SPUR"+"_"+sn+'_'+type+"_"+mds+"_"+BD+"_"+BW+"_"+channel+"MHz_"+path+"_30MHz-1GHz_"+res+".png"
    print scrname
    n = tn.write(b':MMEM:STOR:SCR "'+scrname+ b'"\n')
    filename = "log_all.txt"
    with open("../Log/"+filename,'a') as f1:
        f1.writelines([sn+" ",type+" ",mode+" ",BD+" ",BW+" ",channel+" ",path+" ",targpwr+" ","30MHz-1GHz ",spur+" ",freq+"MHz ",res+"\n"])
    f1.close()
    filename = sn+'_'+"SPUR_log.txt"
    with open("../Log/"+filename,'a') as f2:
        f2.writelines([sn+" ",type+" ",mode+" ",BD+" ",BW+" ",channel+" ",path+" ",targpwr+" ","30MHz-1GHz ",spur+" ",freq+"MHz ",res+"\n"])
    f2.close()
    filename = sn+'_'+"SPUR_result.csv"
    with open("../Result/"+filename,'ab+') as f3:
        writer = csv.writer(f3)
        writer.writerow([type,mode,BD,BW,channel,path,targpwr,"30MHz-1GHz",spur,freq,res])
    f3.close()
#############################SPUR:1GHz-12.75GHz:Left Side########################
    if channel >2110 and channel <2170 and BD == "n1":  ############n1:2110MHz-2170MHz
        BD = n1
        starf = "2180MHz"
        stopf = "2100MHz"
    elif channel > 1930 and channel < 1990 and BD == "n2":############n2:1930MHz-1990MHz
        starf = "2000MHz"
        stopf = "1920MHz"
    elif channel > 1805 and channel < 1880 and BD == "n3":
        BD = n3
        starf = "1890MHz"
        stopf = "1795MHz"
    elif channel > 2620 and channel < 2690 and BD == "n7":
        BD = n7
        starf = "2700MHz"
        stopf = "2610MHz"
    elif channel > 1930 and channel < 1995 and BD == "n25":
        starf = "2005MHz"
        stopf = "1920MHz"
    elif channel > 2010 and channel < 2025 and BD == "n34":
        BD = n34
        starf = "2035MHz"
        stopf = "2000MHz"
    elif channel > 2570 and channel < 2620 and BD == "n38":
        BD = n38
        starf = "2630MHz"
        stopf = "2560MHz"
    elif channel > 1880 and channel < 1920 and BD == "n39":
        BD = n39
        starf = "1930MHz"
        stopf = "1870MHz"
    elif channel > 2300 and channel < 2400 and BD == "n40":
        BD = n40
        starf = "2410MHz"
        stopf = "2290MHz"
    elif channel > 2496 and channel < 2690:
        BD = n41
        starf = "2700MHz"
        stopf = "2486MHz"
    elif channel > 1432 and channel < 1517 and BD == "n50":
        BD = n50
        starf = "1527MHz"
        stopf = "1422MHz"
    elif channel > 1427 and channel < 1432 and BD == "n51":
        BD = n51
        starf = "1442MHz"
        stopf = "1417MHz"
    elif channel > 2110 and channel < 2200 and BD == "n66":
        BD = n66
        starf = "2210MHz"
        stopf = "2100MHz"
    elif channel > 1995 and channel < 2020 and BD == "n70":
        BD = n70
        starf = "2030MHz"
        stopf = "1985MHz"
    elif channel > 1475 and channel < 1518 and BD == "n74":
        BD = n74
        starf = "1528MHz"
        stopf = "1465MHz"
    elif channel > 1432 and channel < 1517 and BD == "n75":
        BD = n75
        starf = "1527MHz"
        stopf = "1422MHz"
    elif channel > 1427 and channel < 1432 and BD == "n76":
        BD = n76
        starf = "1442MHz"
        stopf = "1417MHz"
    elif channel > 3300 and channel < 4200:
        starf = "4210MHz"
        stopf = "3290MHz"
    elif channel > 3300 and channel < 3800 and BD == "n78":
        BD = n78
        starf = "3810MHz"
        stopf = "3290MHz"
    elif channel > 4400 and channel < 5000:
        BD = n79
        starf = "5010MHz"
        stopf = "4390MHz"
    n = tn.write(b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:PEAK:EXC 6,6" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:PEAK:THReshold -130,-130" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:STATE ON,ON,OFF,OFF,OFF,OFF,OFF,OFF" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:BAND:RES 1MHZ,1MHZ" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPURious:BANDwidth:VIDeo:AUTO ON" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:FREQ:START 1000MHz,"+starf + b"\r\n")#测试起始频率
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:FREQ:STOP "+stopf+",12750MHz" + b"\r\n")#测试结束频率
    tn.read_until(b"SCPI>")
    n = tn.write(b"CALC:SPUR:LIM:ABS:DATA -30dBm" + b"\r\n")#判定条件Limit
    tn.read_until(b"SCPI>")
    n = tn.write(b"CALC:SPUR:LIM:ABS:DATA:STOP -30dBm" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:ATT:AUTO 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"SPUR:ATT 0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b"POW:ATT 0" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":SPUR:STAT ON,OFF,OFF,OFF,OFF,OFF,OFF,OFF"+ b"\r\n")#只打开range1
    tn.read_until(b"SCPI>")
    n = tn.write(b":INIT:CONT ON" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":INITiate:RESTart" + b"\r\n")
    tn.read_until(b"SCPI>")
    time.sleep(5)
    n = tn.write(b":INIT:CONT OFF" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":FETCh:SPURious1?" + b"\r\n")
    time.sleep(3)
    result = tn.read_very_eager() 
    num = re.sub(r'\s+',"", result)
    num = re.sub(r'>', "", num)
    num = re.sub(r'SCPI', "", num)
    num = num.split(",")
    amp = [float(i) for i in num[4::6]]
    amp = [round(i,2) for i in amp]
    #print amp
    spur = max(amp)
    print "::::::::::::::::::::::"
    print "SPUR:",spur,"dBm"
    j = amp.index(spur)
    #print j
    freq = [float(i) for i in num[3::6]]
    freq = [i/1000000 for i in freq]
    freq = [round(i,2) for i in freq]
    freq = freq[j]
    print "Freq:",freq,"MHz"
    limit = [float(i) for i in num[5::6]]
    limit = [round(i,2) for i in limit]
    limit = limit[j]
    print "limit:",limit,"dBm"
    if spur < limit:
        res = "Pass"
    else:
        res = "Fail"
    print "Result:",res
    print "::::::::::::::::::::::"
    spur = str(spur)
    freq = str(freq)
    limit = str(limit)
    mds = re.sub(r'\.', "_", mode)
    scrname = "SPUR"+"_"+sn+'_'+type+"_"+mds+"_"+BD+"_"+BW+"_"+channel+"MHz_"+path+"_1000MHz-"+stopf+"_"+res+".png"
    print scrname
    n = tn.write(b':MMEM:STOR:SCR "'+scrname+ b'"\n')
    filename = "log_all.txt"
    with open("../Log/"+filename,'a') as f1:
        f1.writelines([sn+" ",type+" ",mode+" ",BD+" ",BW+" ",channel+" ",path+" ",targpwr+" ","1000MHz-"+stopf+" ",spur+" ",freq+"MHz ",res+"\n"])
    f1.close()
    filename = sn+'_'+"SPUR_log.txt"
    with open("../Log/"+filename,'a') as f2:
        f2.writelines([sn+" ",type+" ",mode+" ",BD+" ",BW+" ",channel+" ",path+" ",targpwr+" ","1000MHz-"+stopf+" ",spur+" ",freq+"MHz ",res+"\n"])
    f2.close()
    filename = sn+'_'+"SPUR_result.csv"
    with open("../Result/"+filename,'ab+') as f3:
        writer = csv.writer(f3)
        writer.writerow([type,mode,BD,BW,channel,path,targpwr,"1000MHz-"+stopf,spur,freq,res])
    f3.close()
#############################SPUR:1GHz-12.75GHz:Right Side########################
    n = tn.write(b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":SPUR:STAT OFF,ON,OFF,OFF,OFF,OFF,OFF,OFF"+ b"\r\n")#只打开range2
    tn.read_until(b"SCPI>")
    n = tn.write(b":INIT:CONT ON" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":INITiate:RESTart" + b"\r\n")
    tn.read_until(b"SCPI>")
    time.sleep(5)
    n = tn.write(b":INIT:CONT OFF" + b"\r\n")
    tn.read_until(b"SCPI>")
    n = tn.write(b":FETCh:SPURious1?" + b"\r\n")
    time.sleep(3)
    result = tn.read_very_eager() 
    num = re.sub(r'\s+',"", result)
    num = re.sub(r'>', "", num)
    num = re.sub(r'SCPI', "", num)
    num = num.split(",")
    amp = [float(i) for i in num[4::6]]
    amp = [round(i,2) for i in amp]
    #print amp
    spur = max(amp)
    print "::::::::::::::::::::::"
    print "SPUR:",spur,"dBm"
    j = amp.index(spur)
    #print j
    freq = [float(i) for i in num[3::6]]
    freq = [i/1000000 for i in freq]
    freq = [round(i,2) for i in freq]
    freq = freq[j]
    print "Freq:",freq,"MHz"
    limit = [float(i) for i in num[5::6]]
    limit = [round(i,2) for i in limit]
    limit = limit[j]
    print "limit:",limit,"dBm"
    if spur < limit:
        res = "Pass"
    else:
        res = "Fail"
    print "Result:",res
    print "::::::::::::::::::::::"
    spur = str(spur)
    freq = str(freq)
    limit = str(limit)
    mds = re.sub(r'\.', "_", mode)
    scrname = "SPUR"+"_"+sn+'_'+type+"_"+mds+"_"+BD+"_"+BW+"_"+channel+"MHz_"+path+"_"+starf+"-12.75GHz_"+res+".png"
    print scrname
    n = tn.write(b':MMEM:STOR:SCR "'+scrname+ b'"\n')
    filename = "log_all.txt"
    with open("../Log/"+filename,'a') as f1:
        f1.writelines([sn+" ",type+" ",mode+" ",BD+" ",BW+" ",channel+" ",path+" ",targpwr+" ",starf+"-12.75GHz"+" ",spur+" ",freq+"MHz ",res+"\n"])
    f1.close()
    filename = sn+'_'+"SPUR_log.txt"
    with open("../Log/"+filename,'a') as f2:
        f2.writelines([sn+" ",type+" ",mode+" ",BD+" ",BW+" ",channel+" ",path+" ",targpwr+" ",starf+"-12.75GHz"+" ",spur+" ",freq+"MHz ",res+"\n"])
    f2.close()
    filename = sn+'_'+"SPUR_result.csv"
    with open("../Result/"+filename,'ab+') as f3:
        writer = csv.writer(f3)
        writer.writerow([type,mode,BD,BW,channel,path,targpwr,starf+"-12.75GHz",spur,freq,res])
    f3.close()
    tn.close()
    time.sleep(1)
    return