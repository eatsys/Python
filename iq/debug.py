# coding: utf-8
#@time      : 2019/11/15 10:00
import struct

__author__ = 'Ethan'

# import csv
#
# path_loss_list = []
# with open('./pathloss.csv', newline='') as f:
#     pathloss = csv.reader(f)
#     for p in pathloss:
#         print('read', p)
#         path_loss_list.append(p)
#     for loss in path_loss_list:
#          print('create', loss)
#     # rows = [row for row in pathloss]
#     # for row in pathloss:
#     #     rows = [row for row in pathloss]
#     #     print(rows[0])
#     #     print(len(rows[0]))
#     rows = [row for row in path_loss_list]
#     print(rows[0])
#     print(len(rows[0]))
#     path = len(rows[0]) - 1
#     print('path num', path)
#     for p in range(path):
#         print('path', p)
#         for path_loss in path_loss_list:
#             print(p, path_loss)
#             channel = path_loss[0]
#             pathloss = path_loss[p+1]
#             print('pathloss', pathloss)

# PER_LIST = [0,0,0,12,43,100]
# SEN_LIST = [-90,-91,-92,-93,-94,-95]
# print(PER_LIST[-2])
# print(SEN_LIST[-2],type(SEN_LIST[-2]))
#
# import urllib2

#
# class yv_root(object):
#
#
#     def __init__(self, interim):
#         self.interim = interim
#         print(self.interim)
#
#     def html_wei_read(self):
#         n = self.interim + 'wyh'
#         print(n)
#
#
#
# n0 = yv_root('http://www.*****.com')
# n1 = yv_root('http://www.*****.cn:6001')


#
# root = (n0, n1)
#
# i = 0
# while i < 5:
#     root[i].html_wei_read()
#     print(root[i].inspect())
#     i = i + 1
#

#  -*- coding:utf-8 -*-
#
# from ctypes import *
# import os
# os.environ['path'] += ';D:\work\Reamon\Python\iq'
# dll = cdll.LoadLibrary('D:\work\Reamon\Python\iq\IQmeasure.dll')
# dir = dll.__dir__()
# print(dll)
# a = dll.version()
# print(type(a))
# print(a)
# import visa
# ip = '192.168.100.253'
# address = 'TCPIP0::%s::hislip0::INSTR' % ip
# resourceManager = visa.ResourceManager()
# instance = resourceManager.open_resource(address)
#
# idn = instance.query('*IDN?')
# print(idn)
# instance.write('CHAN1')
# instance.write('VSA1 ;init')
# instance.write('WIFI')
# result=instance.query('calc:txq 0, 1;*wai;*opc?')
# print(result,type(result))
# data_pwr = instance.query_ascii_values('WIFI;FETC:SEGM:TXQ:OFDM:AVER?')
# print(data_pwr[0], type(data_pwr[0]))
# # data_pwr = instance.query('WIFI;FETC:SEGM:POW:AVER?')
# for data in data_pwr:
#     print(data)

# result = instance.write('calc:txq 0, 2')
# print(result)
# result=instance.write('calc:ccdf 0, 2')
# print(result)
# result =instance.write('calc:ramp 0, 2')
# print(result)
# result= instance.write('calc:spec 0, 2')
# print(result)

# print(type(result))
# print(str(result))
# result1 = []
# for r in result:
#     print(r)
#     print(chr(r))
#     result1.append(chr(r))
# print(result1)
# print('*****************************')
# s = b'\xaa\xb8\x08\xc2\x07\xc2\n'
# s = s.encode()
# print(s.decode('utf-8'))
# for ss in s:
#     print(ss)
# sss = s.hex()
# print(sss)
# import telnetlib
# import time
# tn = telnetlib.Telnet()
# tn.set_debuglevel(1)
# tn.open('192.168.100.1', port=23)
# tn.read_until(b'Login: ', timeout=1)
# tn.write(b'root\n')
# tn.read_until(b'Password:', timeout=1)
# tn.write(b'admin\n')
# tn.write(b'su\r\n')
# tn.read_until(b'>', timeout=1)
# tn.write(b'shell\r\n')
# tn.read_until(b'#', timeout=1)
# tn.write(b'iw wlan1_0 e2p get freq_offset\r\n')
# time.sleep(0.5)
# command_result = tn.read_very_eager()
# print(command_result)
# print(command_result.decode('utf-8'))
# print(command_result.decode('utf-8').split())
# print(command_result.decode('utf-8').split()[-4])
# result_list = []
# for result in command_result.split():
#     print(result.decode('utf-8'))
#     result_list.append(result.decode('utf-8'))
# pwr_word = result_list[-4]
# print(pwr_word)

# a = b'\xaa\x3d\n'
# print(a.decode('utf-8','strict'))
# print(a.decode('utf-8'))
# import csv
# s = 'Pass'
# a = 2
# b = 3
# c = 4
# list = []
# list.append([a,b,c])
# print(list)
#
# s = 'Pass'
# a = 5
# b = 6
# c = 7
# list.append([a,b,c])
# print(list)
# if s == 'Pass':
#     list.append([7,8,9])
#     print(list)
# else:
#     result_final = list[-1]
#     with open('./Result/' + 'test.csv', 'a+', newline='') as write_txmax_result:
#         writer_file = csv.writer(write_txmax_result)
#         writer_file.writerow(result_final)

str = (26, '<StatusCode.success: 0>')
print(str)
print(str[0])
print(str[1])
