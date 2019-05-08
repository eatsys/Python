#!/user/bin/env python
# encoding: utf-8
#@time      : 2019/4/26 11:16

__author__ = 'Ethan'

#import os
#import re
#import time
#import xlsxwriter
#from config import conf
#import data.write_datas
#from data.parameters import RADIO, CHANNEL, ANGLE, ATTENUATE_LIST
#os.chdir(r'..')
#retval = os.getcwd()
#print(retval)
##os.chdir(r'..')
#file_d = retval + '\\Result\\IxChariotOD\\ WF-1931'
#file = file_d + '\\ 2.4g_ 1_ 10_ 0_Tx.txt'
##' 2.4g_ 1_ 10_ 0_Tx.txt'
#f = open(file, "r")
#print(f)
#result = f.read()
#print(f.read())
#txthrought = (re.findall(r'Totals:\s+\d.+', result)[0].split()[1].encode("ascii")).decode("ascii")
#print("tx_throught is    : {0} ".format(txthrought))

#try:
#    #file_path = 'D:\\work\\Reamon\\Python\\rvr\\Result\\IxChariotOD\\ WF-1931\\ 2.4g_ 1_ 10_ 0_Tx.txt'
#    #D:\work\Reamon\Python\rvr/Result/IxChariotOD/ WF-1931/ 2.4g_ 1_ 10_ 0_Tx.txt
#    #D:\work\Reamon\Python/Result/IxChariotOD/ WF-1931/ 2.4g_ 1 _10_ 0_Tx.txt
#    retval = os.getcwd()
#    print(retval)
#    test_ap = conf.Ap_type_get()
#    file = retval + '/Result/IxChariotOD/ ' + test_ap + '/ 2.4g_ 1_ 10_ 0_Tx.txt'
#    file = 'D:\\work\\Reamon\\Python\\rvr/Result/IxChariotOD/ WF-1931/ 2.4g_ 1_ 10_ 0_Tx.txt'
#    #file = 'D:/work/Reamon/Python/rvr/Result/IxChariotOD/ WF-1931/ 2.4g_ 1_ 10_ 0_Tx.txt'
#    #file = 'D:\\work\\Reamon\\Python\\rvr\\Result\\IxChariotOD\\ WF-1931\\ 2.4g_ 1_ 10_ 0_Tx.txt'
#    #file = 'D:\work\Reamon\Python\rvr/Result/IxChariotOD/ WF-1931/ 2.4g_ 1 _10_ 0_Tx.txt'
#    file = 'D:\\work\\Reamon\\Python\\rvr/Result/IxChariotOD/ WF-1931/ 2.4g_ 1 #_10_ 0_Tx.txt'
#    file_path = file
#    print('33', file_path)
#    f = open(file_path, "r")
#    print('88', f)
#    result = f.read()
#    print(f.read())
#    txthrought = (re.findall(r'Totals:\s+\d.+', result)[0].split()[1].encode("ascii")).decode("ascii")
#    print("tx_throught is    : {0} ".format(txthrought))
#except:
#    print("fail to open tx test result")
#
#try:
#    result = f.read()
#    print(f.read())
#    txthrought = (re.findall(r'Totals:\s+\d.+', result)[0].split()[1].encode("ascii")).decode("ascii")
#    data.write_datas.tx_tp_wirte(txthrought)
#    print("tx_throught is    : {0} ".format(txthrought))
#except:
#    pass
#finally:
#    f.close()


#result_file = 'D:\\work\\Reamon\\Python\\rvr/Result/Data/ WF-1931/'
##result_file = 'D:\\work\\Reamon\\Python\\rvr\\Result\\Data'
#os.makedirs(result_file)
#print(result_file + "tx_tp.txt")
#with open(result_file + "tx_tp.txt", "a") as tx_tp:
#    print(tx_tp)
#    tx_tp.write('999')
#    tx_tp.write("\n")


#now_time = time.strftime("%Y-%m-%d", time.localtime())
#test_ap = conf.Ap_type_get()
#test_radio = conf.Radio_get()
#
#filename = "Rate Over Range OTA test result_" + test_ap + '_' + test_radio + "_8angles_" + now_time + '.xlsx'
#print(filename)
## filename="Rate Over Range OTA test result_"
#workbook = xlsxwriter.Workbook(filename)
#print(workbook)
#worksheet = workbook.add_worksheet("Rate over Range")
#print(worksheet)
#workbook.close()
#

#with open('result.txt', 'r') as f:
#    rssi= f.readlines()
#    print(rssi)
#    print(rssi[0])
#    print(rssi[1])
#    print(rssi[2])


#import win32api, win32con
#win32api.MessageBox(0, "五一太阳大，晒爆了!!!", "Warning", win32con.MB_OK)
#
#import numpy
#n = 7
#print(numpy.sqrt(n))
#for x in range(2, numpy.sqrt(n)):
#    r = n/x
#    print(type(r))
#    if r:
#        print(n, '是质数')
#    else:
#        print(n, '不是质数')#

#Geometric series
while 1:
    a = input('Input a Integer:')
    if a.isdigit() is False:
        print('Please input a Integer')
        break
    r = input('Input a Constant:')
    try:
        r = float(r)
    except Exception as err:
        print('Please input a number')
        break
    n = input('Input the power:')
    try:
        n = float(n)
    except Exception as err:
        print('Please input a number')
        break
    gs_sum = int(a)*(float(r)**float(n)-1)/(float(r)-1)
    print('The Sum is', gs_sum)