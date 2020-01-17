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
#while 1:
#    a = input('Input a Integer:')
#    if a.isdigit() is False:
#        print('Please input a Integer')
#        break
#    r = input('Input a Constant:')
#    try:
#        r = float(r)
#    except Exception as err:
#        print('Please input a number')
#        break
#    n = input('Input the power:')
#    try:
#        n = float(n)
#    except Exception as err:
#        print('Please input a number')
#        break
#    gs_sum = int(a)*(float(r)**float(n)-1)/(float(r)-1)
#    print('The Sum is', gs_sum)

# import re
#
# f = open('D:/rvr/Result/IxChariotOD/ WF-1931/ 2.4g_ 1_ 10_ 0_Tx.txt', "r")
# result = f.read()
# txthrought = re.sub(',', '', (re.findall(r'Totals:\s+\d.+', result)[0].split()[1].encode("ascii")).decode("ascii"))
# print(txthrought)

# from config import conf
# test_ap = str(conf.Ap_type_get())
# test_radio = conf.Radio_get()
# channel = conf.Channel_get()
#
# print('0'+channel)
#
# print('0'+test_ap)
# print('0'+test_radio)
#
# ap = test_ap.strip()
# test_radio = test_radio.strip()
# print('0'+ap)
# print('0'+test_radio)
#
# from chariot import chariot
# import threading
# import time
# import logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
#
#
# def ff(s, t):
#     logger.info(s+' in...')
#     time.sleep(t)
#     logger.info(s+' out...')
#
# t1 = threading.Thread(target=chariot(), args=('t1', 2))
# t1.start()
#
# t2 = threading.Thread(target=ff, args=('t2', 3))
# t2.start()
#
# a = 1
# b = 1
# while a == 1:
#     print('x')
#     b += 1
#     if b > 5:
#         exit()
# else:
#     print('xx')
#
# print('xxx')

import threading
import time

# def run_a():
#     for i in range(10):
#         time.sleep(1)
#         print('1')
#
# def run_b():
#     for i in range(10):
#         time.sleep(1)
#         print('2')
#
# threads_tx = []
# threads_tx.append(threading.Thread(target=run_a))
# threads_tx.append(threading.Thread(target=run_b))
# for tx in threads_tx:
#     tx.start()
#     #tx.join()
# for tx in threads_tx:
#     tx.join()
#
#
# import paramiko
# from io import StringIO
# key_str = """-----BEGIN RSA PRIVATE KEY-----
# MIIEowIBAAKCAQEAuab4BqHVwkS/EISamu2VBapaIeqX4Df+6CQ0Ek1d6Cj9FsM5
# ozHgsvlbsABFgA00JcEiqc+TMYpdOw3DUrhqPczkvclMq/zQyuyv/Hzhv/jGISwy
# RO01AJEkdnYa9SWL25BGFPby3Ec41yecRZibbrOIOEZtoFXSNt5Td3pAMZ2BmuGm
# t4Hgetms9nLh/ZiqY98q11lY36xTXMv8ECBRvtgbIRL+e36bRboKe9fSPLJwtUFx
# JQa5+P70MUTdWnjFuBWC4bTa1uGz7pC0JjpGNYAoe26xI7VcYVuFBm6yW223/hvh
# sSUDn4ncC4TdrT3RFPzbH+zO5d7UbtcPzWmo/QIDAQABAoIBAQCJzbwxABNxHiJM
# moFAGrYQ/H/myQFu92GI4sacBz17RGGIceTok+9cKee63pi4EhTxKUkXjvKNRU0q
# tm6TijuiH+JyVWdKCmDZH5MJ8ZCINJqsqOevbft3rkTIgaZE7VfA5HiAu0VN6Lfy
# TH6c0kgdhbnJO83Hw6xD+gcumlnn+ORBDyrKgJAQ1hxZCG3h2ha3UFvMl8bx0Guv
# OaEGpRludxVtiIBCrkACSUMhKWA2sizV+XHnpNB5ktk4NhR8baPRD9JthfwtWFLR
# 6yWP+DNaF7KjdzJiammzfTqi4gnawxiyNHJSu/tZ/OCSZtJE6bd2iUWvs4isvES8
# S672ZjcBAoGBANvw0ti+oJpIKfJsArnCx2ymLWEYf6A4XzyfXVWHuIYhWOKl51hF
# xTPHAENAHCYzWfOllU07DfNCsbyzdEf4SAyW+kM+IH3ZCDic+q+kUk0xpuFa8sUh
# F2Z+yJecQZJOlJl17KvBvkPU3hcqy3fCXTvC9d2otImJYYKj9szGB58dAoGBANgX
# BA8v2wT04fKkxIKmEUMJyOJ2uYnJqyyyb+w3sD0ZJxWuo2IIeXjA057IkNFDW4Wu
# MDATPJE2HvnnbS59AeVk04ini5j0xjsH1l7LssMFKKoI7hEHXBAPsJYT22ezRnS8
# TFy5YqeNf5UDi043b7NTbwy+Lv8VlopMX6Zn1qthAoGAFXOPnQQ6tdGEBdjzCxss
# SDSNCINTL1VQNKF2gPkTzkFCYhi8T6e+bCZkqCqAlFk91L25qiawXaGLpFP8a2iT
# 3mZ7UkOk96FLY/ormSX1wQGuvRwZwZBQr/Z9qgvbeWGgrLcLtlTXMdZ5MtlBrxSN
# 8144jL3/ncqAcDV9xMsrwyECgYAX+jXRGZZL7oBD1FSZyqOPtL49or7jsyTzSLly
# lJtRrEDR/xbSAe64n2zb6ZVoIvk81B80tm26Dy9Qu4U561UShyWRvEWZK0/zrOL0
# kdW8Hg5tD6Ca8x4cCiGmBX4K+7GNsncmsstnnCPT/RiwDSav10ozN8cvNs4FeoQC
# ivMfAQKBgGWZoI4eUqPxZY3tCeQYa6E9cc54HwXo7zroQvq9i2jehybRTnK6qb3h
# mDaHLrCxKCGe3hpjm9H4Oox07rt1vHj/CG4pjJM61hiIJLZilrkmHiZj/SIXQ8vq
# PxaN0gEF4ibH237vfwrHxGUyFSJRh2B77zW4t79sUw6t89DdpR4Z
# -----END RSA PRIVATE KEY-----
# """
# # 创建SSH对象
# private_key = paramiko.RSAKey(file_obj=StringIO(key_str))
#
# transport = paramiko.Transport(('192.168.1.10', 22))
# transport.connect(username='root', pkey=private_key)
#
# ssh = paramiko.SSHClient()
# #ssh._transport() = transport
# # 允许连接不在know_hosts文件中的主机
#
# transport.auth_none('root')
#
# #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# # 连接服务器
# #ssh.connect(hostname='192.168.1.50', port=22, username='root', pkey=private_key)
# # 执行命令
#
# # 执行命令
# stdin, stdout, stderr = ssh.exec_command('df')
# result, err = stdout.read(), stderr.read()
# print(result.decode())
# # stdin, stdout2, stderr = ssh.exec_command('ifconfig')
#
# print(err.decode())
#
# # 关闭连接
# ssh.close()


# import paramiko
# paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)
# transport = paramiko.Transport(('192.168.1.10', 22))
# ssh = paramiko.SSHClient()
# ssh._transport = transport
# transport.auth_none('root')
#
#
#
# #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# # 连接服务器
# #ssh.connect(hostname='192.168.1.50', port=22, username='root', pkey=private_key)
# # 执行命令
#
# # 执行命令
# stdin, stdout, stderr = ssh.exec_command('df')
# result, err = stdout.read(), stderr.read()
# print(result.decode())
# # stdin, stdout2, stderr = ssh.exec_command('ifconfig')
#
# print(err.decode())
#
# # 关闭连接
# ssh.close()

import paramiko
paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname="192.168.1.10", port=22, username="root", password='')



#ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 连接服务器
#ssh.connect(hostname='192.168.1.50', port=22, username='root', pkey=private_key)
# 执行命令

# 执行命令
stdin, stdout, stderr = ssh.exec_command('df')
result, err = stdout.read(), stderr.read()
print(result.decode())
print(err.decode())


stdin, stdout, stderr = ssh.exec_command(b'iwpriv wdev1sta0 getrssi;dmesg -c\r\n')
rssi_ant_result = stdout.read().decode('utf-8')
# 关闭连接
ssh.close()