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
#from openpyxl import load_workbook
import csv
import re


#pathloss_file = csv.reader(open('./pathloss.csv'))
#next(pathloss_file)
#for rows in pathloss_file:
#    print (rows[0])
#
#
#
#
#    ###################################################################
#    dut_file = load_workbook('./test_config.xlsx')
#    #print(dut_file.sheetnames)
#    sheet = dut_file['Sheet1']
#    #print(sheet['A'])
#    #print(sheet['1'])
#    #print(sheet['A1'].value)
#    #print(sheet.max_row)
#    #print(sheet.max_column)
#    for i in sheet['1']:
#        print(i.value)
#        for j in sheet['2']:
#            print(j.value)


#now_time = datetime.datetime.now()
#print(now_time)
#now_time = str(now_time)
#now_time = now_time.split()
#print(now_time)
#day_time = re.sub('-','',now_time[0])
#now_time = now_time[1].split('.')
#print(day_time)
#print(now_time)
#now_time = re.sub(':','',now_time[0])
#now_time = day_time + now_time
#print(now_time)
##result_name = '_' + 'TX_Result'+'_'+now_time+'.csv'




#spec_file = load_workbook('./spec.xlsx')
#print(spec_file.sheetnames)
#sheet = spec_file['Sheet1']
#rows = []
#rate = '6M'
#ratelist = ['1L', '2L', '5_5S', '11S','6M','9M','12M','18M','24M','36M','48M','54M','HT20_MCS0','HT20_MCS1',
#            'HT20_MCS2','HT20_MCS3','HT20_MCS4','HT20_MCS5','HT20_MCS6','HT20_MCS7','HT40_MCS0','HT40_MCS1',
#            'HT40_MCS2','HT40_MCS3','HT40_MCS4','HT40_MCS5','HT40_MCS6','HT40_MCS7']
#target_pwr_1L, target_pwr_2L,  target_pwr_5_5S, target_pwr_11S, target_pwr_6M, target_pwr_9M, target_pwr_12M,\
#    target_pwr_18M, target_pwr_24M, target_pwr_36M, target_pwr_48M, target_pwr_54M, target_pwr_HT20_MCS0,\
#    target_pwr_HT20_MCS1, target_pwr_HT20_MCS2, target_pwr_HT20_MCS3, target_pwr_HT20_MCS4, target_pwr_HT20_MCS5,\
#    target_pwr_HT20_MCS6, target_pwr_HT20_MCS7, target_pwr_HT40_MCS0, target_pwr_HT40_MCS1, target_pwr_HT40_MCS2,\
#    target_pwr_HT40_MCS3, target_pwr_HT40_MCS4, target_pwr_HT40_MCS5, target_pwr_HT40_MCS6, target_pwr_HT40_MCS7\
#    = [None] * 28
#for row in sheet:
#    rows.append(row)
#    # print(rows)
#for r in range(sheet.max_row):
#    for c in range(sheet.max_column):
#        # print(rows[r][c].value)
#        rows[r][c].valu#e = str(rows[r][c].value).strip()
#        rs = r + 1
#        for x in ratelist:
#            print('rate', x)
#            if x+'_target' == rows[r][c].value:
#                print('rs', rs)
#                print('power', rows[rs][c].value)
#                exec('target_pwr_%s=%d' % (x, rows[rs][c].value))
#                break
#print(target_pwr_6M)
#targetpower = eval('target_pwr_%s'% rate)
##targetpower = 'target_pwr_'+rate
#print(targetpower)
#
##
##names = locals(#)
##for i in range(5):
##    print(names.get('var' + str(i)), end=' ')

default_value = '13'
print(default_value)
default_value = int(default_value, 16)
print(default_value)
default_value = default_value + 2
print(default_value)
default_value = hex(default_value)
print(default_value)
default_value = re.sub('0x', '', default_value)
print(default_value)
print(type(default_value))