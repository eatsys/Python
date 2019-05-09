# -*- coding: utf-8 -*-
# @Time    : 2019/2/12 13:33
# @Author  : Ethan
# @FileName: report.py for HW

import csv
from openpyxl import Workbook

def gen_report(sn):
    # 生成测试log
    sn = str(sn)
    filename = sn + '_' + "TX_result.csv"
    with open("../Result/" + filename, 'ab+') as f:
        writer = csv.writer(f)
        writer.writerow(["Case", "Chain", "Channel", "Rate", "Result", "Output Power(dBm)", "Gain(dB)"])
    f.close()

    # 生成测试报告数据文件
    sn = str(sn)
    filename = sn + '_' + "TX_result.csv"
    with open("../Result/" + filename, 'ab+') as f:
        writer = csv.writer(f)
        writer.writerow(["Case", "Chain", "Channel", "Rate", "Result", "Output Power(dBm)", "Gain(dB)"])
    f.close()