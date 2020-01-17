#!/user/bin/env python
# encoding: utf-8
# @time      : 2019/9/27 11:06

__author__ = 'Ethan'

import sys
import os
# import re
#
# import serial
#
#
# def sn():
#     com = 'COM7'
#     ser = serial.Serial(com, 9600)
#     len = ser.inWaiting()
#     print(ser)
#     ss = ser.write(b'shell iwpriv vap0 get_rx_info' + b'\r\n')
#     command_result = ser.read_until(b'success')
#     print(command_result)
#     command_result = re.search(b'RX OK:\w+', command_result)
#     print(command_result)
#     print(command_result.group())
#     rx_good = re.sub('RX OK:', '', command_result.group().decode('ascii'))
#     print(rx_good)
#     #data = ser.read_until(b'success')
#     # while True:
#     #     data = ser.read()
#     #     if data < 0:
#     #         break
#
#     ser.close()
#
#
# if __name__ == '__main__':
#     sn()

#
# ss = 5.123
# sss = int(ss)
# print(ss, sss)
# cali_2g = '0'
# cali_5g = '1'
#
#
# if cali_2g == '1' and cali_5g == '1':
#     cali_list = [1,1]
#     band_list = [1,2]
# elif cali_2g == '1':
#     cali_list = [1,0]
#     band_list = [1,0]
# elif cali_5g == '1':
#     cali_list = [0,1]
#     band_list = [0,2]
# else:
#     band_list = []
#     cali_list = []
# print(cali_list,band_list)
# cali_para = [[0 for cali in cali_list] for band in band_list]
# cali_para[0][0] = cali_list[0]
# cali_para[0][1] = band_list[0]
# cali_para[1][0] = cali_list[1]
# cali_para[1][1] = band_list[1]
# print(cali_para)
# for cali,band in cali_para:
# #     print(cali,band)
# a = 18.91
# b = int(a*10)
# print(b)
#
#
# import serial
# import re
# sn = serial.Serial('COM11', 9600)
# sn.timeout = 0.5
# sn.write(b'\r\n')
# sn.write(b'shell WifiTxPowerInit.sh 1 11b 20 3 11 0001')
# # command_result = sn.readlines()
# # print('666', command_result)
# sn.write(b'shell WifiTxRxSwitch.sh 1 tx off\r\n')
# # command_result = sn.readlines()
# # print('777', command_result)
# sn.write(b'shell iwpriv Hisilicon0 cali_power "1 2 204 164 125"\r\n')
# command_result = sn.readlines()
# print('888', command_result)
# for result in command_result:
#     print(result)
# sn.write(b'shell iwpriv Hisilicon0 get_power_param\r\n')
# command_result = sn.readlines()
# print('999', command_result)
# for result in command_result:
#     print(result)
# pwrcali_para = re.findall(b'get_power_param:(.+)\r+\n', command_result)[2].decode('utf-8')
# print('666',pwrcali_para)
# sn.write(b'wifi calibrate test parameter write wifichip 1 type power len 77 value %s\r\n' % pwrcali_para.encode('ascii'))
# #print(f'wifi calibrate test parameter write wifichip 1 type power len 77 value {pwrcali_para}')
# sn.write(b'wifi calibrate test parameter read wifichip 1 type power len 77\r\n')
# #print(f'wifi calibrate test parameter read wifichip 1 type power len 77')
# pwrcali_result = sn.read_until(b'success!')
# print(pwrcali_result)
# # for result in pwrcali_result:
# #     print(result)

import re

str = 'xx4rf5'
result = re.match('xx', str)
print(result)
print(result.group())
