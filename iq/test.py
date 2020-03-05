# -*- coding: utf-8 -*-
# @Time    : 2019/1/18 13:23
# @Author  : Ethan
# @FileName: tx_test.py
"""add 5g and RX
   add calibration"""

# from __future__ import division
# from openpyxl import load_workbook
# import iq
# import dut
# from parameters import IQ_IP, RX_PACKETS, IQ_IP_INTERFERE, DUT_COM, DUT_BAUDRATE, LOG_ENABLE, RX_DYNAMIC, \
#     CALI_2G, CALI_5G
# import os
# import time
# from colorama import init, Fore, Style
# import csv
# import re
# import logging
# logger = logging.getLogger()
#
#
#
# def __isset__(v: object) -> object:
#     try:
#         type(eval(v))
#     except Exception as error:
#         return 0
#     else:
#         return 1
#
#
# def calibration():
#     # calibration
#     if CALI_2G == '1' and CALI_5G == '1':
#         cali_list = [1, 1]
#         band_list = [1, 2]
#     elif CALI_2G == '1':
#         cali_list = [1, 0]
#         band_list = [1, 0]
#     elif CALI_5G == '1':
#         cali_list = [0, 1]
#         band_list = [0, 2]
#     else:
#         band_list = []
#         cali_list = []
#     if band_list and cali_list is not None:
#         cali_para = [[0 for cali in cali_list] for band in band_list]
#         cali_para[0][0] = cali_list[0]
#         cali_para[0][1] = band_list[0]
#         cali_para[1][0] = cali_list[1]
#         cali_para[1][1] = band_list[1]
#         logger.debug(cali_para)
#         for cali, band in cali_para:
#             cali = str(cali)
#             band = str(band)
#             logger.info('Band' + band)
#             if cali == '1':
#                 if band == '1':
#                     channel = 2412
#                     cali_channel_list = [3, 8, 12]
#                     cali_mode = '11b'
#                     cali_rate = '11'
#                     radio_adress = '77'
#                 else:
#                     channel = 5180
#                     cali_channel_list = [40, 56, 104, 120, 136, 157]
#                     cali_mode = '11a'
#                     cali_rate = '6'
#                     radio_adress = '155'
#                 # dt.init_cali()
#                 logger.debug(band)
#                 logger.info('Calibration...')
#                 # ppm cali
#                 logger.info('PPM Calibration...')
#                 chain = '0'
#                 mode = '11g/a'
#                 bw = '20'
#                 dt.init_ppm()
#                 iq.set_port(20)
#                 iq.analysis()
#                 pwr_len, txq_len, data_pwr, data_txq = iq.get_status()
#                 symbol_clock_error = iq.adjust_ppm()
#                 init_ppm = int(float(symbol_clock_error))
#                 logger.debug('Default ppm: ' + str(init_ppm))
#                 dt.adjust_ppm(init_ppm)
#                 time.sleep(3)
#                 iq.analysis()
#                 pwr_len, txq_len, data_pwr, data_txq = iq.get_status()
#                 symbol_clock_error = iq.adjust_ppm()
#                 cali_ppm = int(float(symbol_clock_error))
#                 logger.debug('Cali ppm: ' + str(cali_ppm))
#                 if cali_ppm > 5 or cali_ppm < -5:
#                     logger.info(Fore.RED + 'PPM CALIBRATION FAIL' + Style.RESET_ALL)
#                 else:
#                     logger.info(Fore.GREEN + 'PPM CALIBRATION SUCCESS' + Style.RESET_ALL)
#                 # power cali
#                 logger.info('Power Calibration...')
#                 cali_chain_list = ['0', '1']
#                 cali_power_list = [200, 160, 120]
#                 for cali_chain in cali_chain_list:
#                     if cali_chain == '0':
#                         chain = '01'
#                     else:
#                         chain = '10'
#                     for cali_channel in cali_channel_list:
#                         adjust_power_list = []
#                         dt.cali_pwr(cali_channel, chain)
#                         if cali_channel < 30:
#                             channel = 2407 + cali_channel * 5
#                         else:
#                             channel = 5000 + cali_channel * 5
#                         for cali_power in cali_power_list:
#                             dt.adjust_pwr(cali_power)
#                             iq.set_port(int(cali_power / 10))
#                             target_power = int(cali_power / 10)
#                             mode = cali_mode
#                             rates = cali_rate
#                             iq.analysis()
#                             pwr_len, txq_len, data_pwr, data_txq = iq.get_status()
#                             avg_power = iq_wanted.get_power()
#                             adjust_power = int(float(avg_power) * 10.0)
#                             adjust_power_list.append(adjust_power)
#                         dt.adjust_pwr(300)
#                         dt.tx_off()
#                         logger.debug(adjust_power_list)
#                         dt.cali_pwr_write(adjust_power_list)
#                 dt.cali_para_write()
#                 dt.crc()
#                 logger.info(Fore.GREEN + 'POWER CALIBRATION SUCCESS' + Style.RESET_ALL)
#             else:
#                 logger.info(Fore.YELLOW + 'Calibration skip' + Style.RESET_ALL)
#     else:
#         logger.info(Fore.YELLOW + 'Calibration skip' + Style.RESET_ALL)
#
#
# def tx_test():
#     pass
#
#
# def rx_test():
#     pass
#
#
# def aj_test():
#     pass
#
#
# def naj_test():
#     pass
#
#
# if __name__ == '__main__':
#     init(autoreset=True)
#
#     # generate result and log
#     directory_r = os.path.exists(r'./Result')
#     if directory_r is False:
#         os.makedirs('Result')
#
#     directory_l = os.path.exists(r'./log')
#     if directory_l is False:
#         os.makedirs('log')
#
#     # GEN TIME
#     now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
#     # logger.debug(now_time)
#     logger.setLevel(logging.DEBUG)  # logger的总开关，只有大于Debug的日志才能被logger对象处理
#
#     # 第二步，创建一个handler，用于写入日志文件
#     file_handler = logging.FileHandler('./log/log_' + now_time + '.txt', mode='w')
#     file_handler.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
#     # 创建该handler的formatter
#     file_handler.setFormatter(
#         logging.Formatter(
#             fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
#             datefmt='%Y-%m-%d %H:%M:%S')
#     )
#     # 添加handler到logger中
#     logger.addHandler(file_handler)
#
#     # 第三步，创建一个handler，用于输出到控制台
#     console_handler = logging.StreamHandler()
#     if LOG_ENABLE == 1:
#         console_handler.setLevel(logging.DEBUG)  # 输出到控制台的log等级的开关
#     else:
#         console_handler.setLevel(logging.INFO)  # 输出到控制台的log等级的开关
#     # 创建该handler的formatter
#     console_handler.setFormatter(
#         logging.Formatter(
#             fmt='%(asctime)s - %(levelname)s: %(message)s',
#             datefmt='%Y-%m-%d %H:%M:%S')
#     )
#     logger.addHandler(console_handler)
#
#     # input sn
#     Number = input("SN:")
#     sn = "SN_" + Number
#
#     # test define
#     target_pwr_1M, target_pwr_2M, target_pwr_5_5M, target_pwr_11M, target_pwr_6M, target_pwr_9M, \
#     target_pwr_12M, target_pwr_18M, target_pwr_24M, target_pwr_36M, target_pwr_48M, target_pwr_54M, \
#     target_pwr_HT20_MCS0, target_pwr_HT20_MCS1, target_pwr_HT20_MCS2, \
#     target_pwr_HT20_MCS3, target_pwr_HT20_MCS4, target_pwr_HT20_MCS5, target_pwr_HT20_MCS6, \
#     target_pwr_HT20_MCS7, target_pwr_HT40_MCS0, target_pwr_HT40_MCS1, target_pwr_HT40_MCS2, \
#     target_pwr_HT40_MCS3, target_pwr_HT40_MCS4, target_pwr_HT40_MCS5, target_pwr_HT40_MCS6, \
#     target_pwr_HT40_MCS7, target_pwr_VHT20_MCS0, target_pwr_VHT20_MCS1, target_pwr_VHT20_MCS2, \
#     target_pwr_VHT20_MCS3, target_pwr_VHT20_MCS4, target_pwr_VHT20_MCS5, target_pwr_VHT20_MCS6, \
#     target_pwr_VHT20_MCS7, target_pwr_VHT20_MCS8, target_pwr_VHT40_MCS0, target_pwr_VHT40_MCS1, \
#     target_pwr_VHT40_MCS2, target_pwr_VHT40_MCS3, target_pwr_VHT40_MCS4, target_pwr_VHT40_MCS5, \
#     target_pwr_VHT40_MCS6, target_pwr_VHT40_MCS7, target_pwr_VHT40_MCS8, target_pwr_VHT40_MCS9, \
#     target_pwr_VHT80_MCS0, target_pwr_VHT80_MCS1, target_pwr_VHT80_MCS2, target_pwr_VHT80_MCS3, \
#     target_pwr_VHT80_MCS4, target_pwr_VHT80_MCS5, target_pwr_VHT80_MCS6, target_pwr_VHT80_MCS7, \
#     target_pwr_VHT80_MCS8, target_pwr_VHT80_MCS9, \
#     target_pwr_VHT160_MCS0, target_pwr_VHT160_MCS1, target_pwr_VHT160_MCS2, target_pwr_VHT160_MCS3, \
#     target_pwr_VHT160_MCS4, target_pwr_VHT160_MCS5, target_pwr_VHT160_MCS6, target_pwr_VHT160_MCS7, \
#     target_pwr_VHT160_MCS8, target_pwr_VHT160_MCS9, target_pwr_HE20_HE0, target_pwr_HE20_HE1, target_pwr_HE20_HE2, \
#     target_pwr_HE20_HE3, target_pwr_HE20_HE4, target_pwr_HE20_HE5, \
#     target_pwr_HE20_HE6, target_pwr_HE20_HE7, target_pwr_HE20_HE8, target_pwr_HE20_HE9, target_pwr_HE20_HE10, \
#     target_pwr_HE20_HE11, target_pwr_HE40_HE0, target_pwr_HE40_HE1, target_pwr_HE40_HE2, target_pwr_HE40_HE3, \
#     target_pwr_HE40_HE4, target_pwr_HE40_HE5, target_pwr_HE40_HE6, target_pwr_HE40_HE7, target_pwr_HE40_HE8, \
#     target_pwr_HE40_HE9, target_pwr_HE40_HE10, target_pwr_HE40_HE11, target_pwr_HE80_HE0, target_pwr_HE80_HE1, \
#     target_pwr_HE80_HE2, target_pwr_HE80_HE3, target_pwr_HE80_HE4, target_pwr_HE80_HE5, target_pwr_HE80_HE6, \
#     target_pwr_HE80_HE7, target_pwr_HE80_HE8, target_pwr_HE80_HE9, target_pwr_HE80_HE10, target_pwr_HE80_HE11, \
#     target_pwr_HE160_HE0, target_pwr_HE160_HE1, target_pwr_HE160_HE2, target_pwr_HE160_HE3, target_pwr_HE160_HE4, \
#     target_pwr_HE160_HE5, target_pwr_HE160_HE6, target_pwr_HE160_HE7, target_pwr_HE160_HE8, target_pwr_HE160_HE9, \
#     target_pwr_HE160_HE10, target_pwr_HE160_HE11 = [None] * 115
#
#     target_EVM_1M, target_EVM_2M, target_EVM_5_5M, target_EVM_11M, target_EVM_6M, target_EVM_9M, target_EVM_12M, \
#     target_EVM_18M, target_EVM_24M, target_EVM_36M, target_EVM_48M, target_EVM_54M, target_EVM_HT20_MCS0, \
#     target_EVM_HT20_MCS1, target_EVM_HT20_MCS2, target_EVM_HT20_MCS3, target_EVM_HT20_MCS4, target_EVM_HT20_MCS5, \
#     target_EVM_HT20_MCS6, target_EVM_HT20_MCS7, target_EVM_HT40_MCS0, target_EVM_HT40_MCS1, target_EVM_HT40_MCS2, \
#     target_EVM_HT40_MCS3, target_EVM_HT40_MCS4, target_EVM_HT40_MCS5, target_EVM_HT40_MCS6, target_EVM_HT40_MCS7, \
#     target_EVM_VHT20_MCS0, target_EVM_VHT20_MCS1, target_EVM_VHT20_MCS2, target_EVM_VHT20_MCS3, target_EVM_VHT20_MCS4, \
#     target_EVM_VHT20_MCS5, target_EVM_VHT20_MCS6, target_EVM_VHT20_MCS7, target_EVM_VHT20_MCS8, target_EVM_VHT40_MCS0, \
#     target_EVM_VHT40_MCS1, target_EVM_VHT40_MCS2, target_EVM_VHT40_MCS3, target_EVM_VHT40_MCS4, target_EVM_VHT40_MCS5, \
#     target_EVM_VHT40_MCS6, target_EVM_VHT40_MCS7, target_EVM_VHT40_MCS8, target_EVM_VHT40_MCS9, target_EVM_VHT80_MCS0, \
#     target_EVM_VHT80_MCS1, target_EVM_VHT80_MCS2, target_EVM_VHT80_MCS3, target_EVM_VHT80_MCS4, target_EVM_VHT80_MCS5, \
#     target_EVM_VHT80_MCS6, target_EVM_VHT80_MCS7, target_EVM_VHT80_MCS8, target_EVM_VHT80_MCS9, \
#     target_EVM_VHT160_MCS0, target_EVM_VHT160_MCS1, target_EVM_VHT160_MCS2, target_EVM_VHT160_MCS3, \
#     target_EVM_VHT160_MCS4, target_EVM_VHT160_MCS5, target_EVM_VHT160_MCS6, target_EVM_VHT160_MCS7, \
#     target_EVM_VHT160_MCS8, target_EVM_VHT160_MCS9, target_EVM_HE20_HE0, target_EVM_HE20_HE1, target_EVM_HE20_HE2, \
#     target_EVM_HE20_HE3, target_EVM_HE20_HE4, target_EVM_HE20_HE5, \
#     target_EVM_HE20_HE6, target_EVM_HE20_HE7, target_EVM_HE20_HE8, target_EVM_HE20_HE9, target_EVM_HE20_HE10, \
#     target_EVM_HE20_HE11, target_EVM_HE40_HE0, target_EVM_HE40_HE1, target_EVM_HE40_HE2, target_EVM_HE40_HE3, \
#     target_EVM_HE40_HE4, target_EVM_HE40_HE5, target_EVM_HE40_HE6, target_EVM_HE40_HE7, target_EVM_HE40_HE8, \
#     target_EVM_HE40_HE9, target_EVM_HE40_HE10, target_EVM_HE40_HE11, target_EVM_HE80_HE0, target_EVM_HE80_HE1, \
#     target_EVM_HE80_HE2, target_EVM_HE80_HE3, target_EVM_HE80_HE4, target_EVM_HE80_HE5, target_EVM_HE80_HE6, \
#     target_EVM_HE80_HE7, target_EVM_HE80_HE8, target_EVM_HE80_HE9, target_EVM_HE80_HE10, target_EVM_HE80_HE11, \
#     target_EVM_HE160_HE0, target_EVM_HE160_HE1, target_EVM_HE160_HE2, target_EVM_HE160_HE3, target_EVM_HE160_HE4, \
#     target_EVM_HE160_HE5, target_EVM_HE160_HE6, target_EVM_HE160_HE7, target_EVM_HE160_HE8, target_EVM_HE160_HE9, \
#     target_EVM_HE160_HE10, target_EVM_HE160_HE11 = [None] * 115
#
#     target_sens_1M, target_sens_2M, target_sens_5_5M, target_sens_11M, target_sens_6M, target_sens_9M, target_sens_12M, \
#     target_sens_18M, target_sens_24M, target_sens_36M, target_sens_48M, target_sens_54M, target_sens_HT20_MCS0, \
#     target_sens_HT20_MCS1, target_sens_HT20_MCS2, target_sens_HT20_MCS3, target_sens_HT20_MCS4, target_sens_HT20_MCS5, \
#     target_sens_HT20_MCS6, target_sens_HT20_MCS7, target_sens_HT40_MCS0, target_sens_HT40_MCS1, target_sens_HT40_MCS2, \
#     target_sens_HT40_MCS3, target_sens_HT40_MCS4, target_sens_HT40_MCS5, target_sens_HT40_MCS6, target_sens_HT40_MCS7, \
#     target_sens_VHT20_MCS0, target_sens_VHT20_MCS1, target_sens_VHT20_MCS2, target_sens_VHT20_MCS3, target_sens_VHT20_MCS4, \
#     target_sens_VHT20_MCS5, target_sens_VHT20_MCS6, target_sens_VHT20_MCS7, target_sens_VHT20_MCS8, target_sens_VHT40_MCS0, \
#     target_sens_VHT40_MCS1, target_sens_VHT40_MCS2, target_sens_VHT40_MCS3, target_sens_VHT40_MCS4, target_sens_VHT40_MCS5, \
#     target_sens_VHT40_MCS6, target_sens_VHT40_MCS7, target_sens_VHT40_MCS8, target_sens_VHT40_MCS9, target_sens_VHT80_MCS0, \
#     target_sens_VHT80_MCS1, target_sens_VHT80_MCS2, target_sens_VHT80_MCS3, target_sens_VHT80_MCS4, target_sens_VHT80_MCS5, \
#     target_sens_VHT80_MCS6, target_sens_VHT80_MCS7, target_sens_VHT80_MCS8, target_sens_VHT80_MCS9, \
#     target_sens_VHT160_MCS0, target_sens_VHT160_MCS1, target_sens_VHT160_MCS2, target_sens_VHT160_MCS3, \
#     target_sens_VHT160_MCS4, target_sens_VHT160_MCS5, target_sens_VHT160_MCS6, target_sens_VHT160_MCS7, \
#     target_sens_VHT160_MCS8, target_sens_VHT160_MCS9, target_sens_HE20_HE0, target_sens_HE20_HE1, target_sens_HE20_HE2, \
#     target_sens_HE20_HE3, target_sens_HE20_HE4, target_sens_HE20_HE5, \
#     target_sens_HE20_HE6, target_sens_HE20_HE7, target_sens_HE20_HE8, target_sens_HE20_HE9, target_sens_HE20_HE10, \
#     target_sens_HE20_HE11, target_sens_HE40_HE0, target_sens_HE40_HE1, target_sens_HE40_HE2, target_sens_HE40_HE3, \
#     target_sens_HE40_HE4, target_sens_HE40_HE5, target_sens_HE40_HE6, target_sens_HE40_HE7, target_sens_HE40_HE8, \
#     target_sens_HE40_HE9, target_sens_HE40_HE10, target_sens_HE40_HE11, target_sens_HE80_HE0, target_sens_HE80_HE1, \
#     target_sens_HE80_HE2, target_sens_HE80_HE3, target_sens_HE80_HE4, target_sens_HE80_HE5, target_sens_HE80_HE6, \
#     target_sens_HE80_HE7, target_sens_HE80_HE8, target_sens_HE80_HE9, target_sens_HE80_HE10, target_sens_HE80_HE11, \
#     target_sens_HE160_HE0, target_sens_HE160_HE1, target_sens_HE160_HE2, target_sens_HE160_HE3, target_sens_HE160_HE4, \
#     target_sens_HE160_HE5, target_sens_HE160_HE6, target_sens_HE160_HE7, target_sens_HE160_HE8, target_sens_HE160_HE9, \
#     target_sens_HE160_HE10, target_sens_HE160_HE11 = [None] * 115
#
#     target_aj_1M, target_aj_2M, target_aj_5_5M, target_aj_11M, target_aj_6M, target_aj_9M, target_aj_12M, \
#     target_aj_18M, target_aj_24M, target_aj_36M, target_aj_48M, target_aj_54M, target_aj_HT20_MCS0, \
#     target_aj_HT20_MCS1, target_aj_HT20_MCS2, target_aj_HT20_MCS3, target_aj_HT20_MCS4, target_aj_HT20_MCS5, \
#     target_aj_HT20_MCS6, target_aj_HT20_MCS7, target_aj_HT40_MCS0, target_aj_HT40_MCS1, target_aj_HT40_MCS2, \
#     target_aj_HT40_MCS3, target_aj_HT40_MCS4, target_aj_HT40_MCS5, target_aj_HT40_MCS6, target_aj_HT40_MCS7, \
#     target_aj_VHT20_MCS0, target_aj_VHT20_MCS1, target_aj_VHT20_MCS2, target_aj_VHT20_MCS3, target_aj_VHT20_MCS4, \
#     target_aj_VHT20_MCS5, target_aj_VHT20_MCS6, target_aj_VHT20_MCS7, target_aj_VHT20_MCS8, target_aj_VHT40_MCS0, \
#     target_aj_VHT40_MCS1, target_aj_VHT40_MCS2, target_aj_VHT40_MCS3, target_aj_VHT40_MCS4, target_aj_VHT40_MCS5, \
#     target_aj_VHT40_MCS6, target_aj_VHT40_MCS7, target_aj_VHT40_MCS8, target_aj_VHT40_MCS9, target_aj_VHT80_MCS0, \
#     target_aj_VHT80_MCS1, target_aj_VHT80_MCS2, target_aj_VHT80_MCS3, target_aj_VHT80_MCS4, target_aj_VHT80_MCS5, \
#     target_aj_VHT80_MCS6, target_aj_VHT80_MCS7, target_aj_VHT80_MCS8, target_aj_VHT80_MCS9, \
#     target_aj_VHT160_MCS0, target_aj_VHT160_MCS1, target_aj_VHT160_MCS2, target_aj_VHT160_MCS3, \
#     target_aj_VHT160_MCS4, target_aj_VHT160_MCS5, target_aj_VHT160_MCS6, target_aj_VHT160_MCS7, \
#     target_aj_VHT160_MCS8, target_aj_VHT160_MCS9, target_aj_HE20_HE0, target_aj_HE20_HE1, target_aj_HE20_HE2, \
#     target_aj_HE20_HE3, target_aj_HE20_HE4, target_aj_HE20_HE5, \
#     target_aj_HE20_HE6, target_aj_HE20_HE7, target_aj_HE20_HE8, target_aj_HE20_HE9, target_aj_HE20_HE10, \
#     target_aj_HE20_HE11, target_aj_HE40_HE0, target_aj_HE40_HE1, target_aj_HE40_HE2, target_aj_HE40_HE3, \
#     target_aj_HE40_HE4, target_aj_HE40_HE5, target_aj_HE40_HE6, target_aj_HE40_HE7, target_aj_HE40_HE8, \
#     target_aj_HE40_HE9, target_aj_HE40_HE10, target_aj_HE40_HE11, target_aj_HE80_HE0, target_aj_HE80_HE1, \
#     target_aj_HE80_HE2, target_aj_HE80_HE3, target_aj_HE80_HE4, target_aj_HE80_HE5, target_aj_HE80_HE6, \
#     target_aj_HE80_HE7, target_aj_HE80_HE8, target_aj_HE80_HE9, target_aj_HE80_HE10, target_aj_HE80_HE11, \
#     target_aj_HE160_HE0, target_aj_HE160_HE1, target_aj_HE160_HE2, target_aj_HE160_HE3, target_aj_HE160_HE4, \
#     target_aj_HE160_HE5, target_aj_HE160_HE6, target_aj_HE160_HE7, target_aj_HE160_HE8, target_aj_HE160_HE9, \
#     target_aj_HE160_HE10, target_aj_HE160_HE11 = [None] * 115
#
#     target_naj_1M, target_naj_2M, target_naj_5_5M, target_naj_11M, target_naj_6M, target_naj_9M, target_naj_12M, \
#     target_naj_18M, target_naj_24M, target_naj_36M, target_naj_48M, target_naj_54M, target_naj_HT20_MCS0, \
#     target_naj_HT20_MCS1, target_naj_HT20_MCS2, target_naj_HT20_MCS3, target_naj_HT20_MCS4, target_naj_HT20_MCS5, \
#     target_naj_HT20_MCS6, target_naj_HT20_MCS7, target_naj_HT40_MCS0, target_naj_HT40_MCS1, target_naj_HT40_MCS2, \
#     target_naj_HT40_MCS3, target_naj_HT40_MCS4, target_naj_HT40_MCS5, target_naj_HT40_MCS6, target_naj_HT40_MCS7, \
#     target_naj_VHT20_MCS0, target_naj_VHT20_MCS1, target_naj_VHT20_MCS2, target_naj_VHT20_MCS3, target_naj_VHT20_MCS4, \
#     target_naj_VHT20_MCS5, target_naj_VHT20_MCS6, target_naj_VHT20_MCS7, target_naj_VHT20_MCS8, target_naj_VHT40_MCS0, \
#     target_naj_VHT40_MCS1, target_naj_VHT40_MCS2, target_naj_VHT40_MCS3, target_naj_VHT40_MCS4, target_naj_VHT40_MCS5, \
#     target_naj_VHT40_MCS6, target_naj_VHT40_MCS7, target_naj_VHT40_MCS8, target_naj_VHT40_MCS9, target_naj_VHT80_MCS0, \
#     target_naj_VHT80_MCS1, target_naj_VHT80_MCS2, target_naj_VHT80_MCS3, target_naj_VHT80_MCS4, target_naj_VHT80_MCS5, \
#     target_naj_VHT80_MCS6, target_naj_VHT80_MCS7, target_naj_VHT80_MCS8, target_naj_VHT80_MCS9, \
#     target_naj_VHT160_MCS0, target_naj_VHT160_MCS1, target_naj_VHT160_MCS2, target_naj_VHT160_MCS3, \
#     target_naj_VHT160_MCS4, target_naj_VHT160_MCS5, target_naj_VHT160_MCS6, target_naj_VHT160_MCS7, \
#     target_naj_VHT160_MCS8, target_naj_VHT160_MCS9, target_naj_HE20_HE0, target_naj_HE20_HE1, target_naj_HE20_HE2, \
#     target_naj_HE20_HE3, target_naj_HE20_HE4, target_naj_HE20_HE5, \
#     target_naj_HE20_HE6, target_naj_HE20_HE7, target_naj_HE20_HE8, target_naj_HE20_HE9, target_naj_HE20_HE10, \
#     target_naj_HE20_HE11, target_naj_HE40_HE0, target_naj_HE40_HE1, target_naj_HE40_HE2, target_naj_HE40_HE3, \
#     target_naj_HE40_HE4, target_naj_HE40_HE5, target_naj_HE40_HE6, target_naj_HE40_HE7, target_naj_HE40_HE8, \
#     target_naj_HE40_HE9, target_naj_HE40_HE10, target_naj_HE40_HE11, target_naj_HE80_HE0, target_naj_HE80_HE1, \
#     target_naj_HE80_HE2, target_naj_HE80_HE3, target_naj_HE80_HE4, target_naj_HE80_HE5, target_naj_HE80_HE6, \
#     target_naj_HE80_HE7, target_naj_HE80_HE8, target_naj_HE80_HE9, target_naj_HE80_HE10, target_naj_HE80_HE11, \
#     target_naj_HE160_HE0, target_naj_HE160_HE1, target_naj_HE160_HE2, target_naj_HE160_HE3, target_naj_HE160_HE4, \
#     target_naj_HE160_HE5, target_naj_HE160_HE6, target_naj_HE160_HE7, target_naj_HE160_HE8, target_naj_HE160_HE9, \
#     target_naj_HE160_HE10, target_naj_HE160_HE11 = [None] * 115
#
#
#     # GEN REPORT
#     tx_result_name = sn + '_' + 'TX_Result' + '_' + now_time + '.csv'
#     rx_result_name = sn + '_' + 'RX_Result' + '_' + now_time + '.csv'
#     aj_result_name = sn + '_' + 'AJ_Result' + '_' + now_time + '.csv'
#     with open('./Result/' + tx_result_name, 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(['FREQ', 'DATA_RATE', 'CHAIN', 'TX_POWER', 'POWER', 'GAIN', 'LIMIT',
#                          'RESULT', 'EVM', 'LIMIT', 'RESULT', 'FREQ_ERROR', 'LIMIT', 'RESULT',
#                          'LOLEAKAGE', 'LIMIT', 'RESULT', 'OBW', 'LIMIT', 'RESULT',
#                          'MASK', 'LIMIT', 'RESULT', 'FLAsnESS', 'LIMIT', 'RESULT',
#                          'RAMPONTIME', 'LIMIT', 'RESULT', 'RAMPOFFTIME', 'LIMIT', 'RESULT'])
#
#     with open('./Result/' + rx_result_name, 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(['FREQ', 'DATA_RATE', 'CHAIN', 'SENSITIVITY SPEC', 'SENSITIVITY', 'RX PACKETS', 'RESULT'])
#
#     with open('./Result/' + aj_result_name, 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(['FREQ', 'DATA_RATE', 'CHAIN', 'Adjacent Channel Rejection SPEC', 'Adjacent Channel Rejection',
#                          'RESULT'])
#
#     if RX_DYNAMIC == '1':
#         rx_dynamic_result = sn + '_' + 'RX_Dynamic' + '_' + now_time + '.csv'
#         with open('./Result/' + rx_dynamic_result, 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(['FREQ', 'DATA_RATE', 'CHAIN', 'VSG_POWER', 'VSG_Packets', 'PER', 'RESULT'])
#
#     # connect equipments and dut
#     try:
#         iq_wanted = iq.IQxel(IQ_IP)
#     except Exception as err:
#         logger.info(err)
#         logger.info(Fore.RED + 'IQ connect fail!' + Style.RESET_ALL)
#     else:
#         mw_iq = iq_wanted.read_idn
#         logger.info('IQ connected!')
#     try:
#         iq_interfere = iq.IQxel(IQ_IP_INTERFERE)
#     except Exception as err:
#         logger.info(err)
#         logger.info(Fore.RED + 'INTERFERE IQ connect fail!' + Style.RESET_ALL)
#     else:
#         mw_iq_inter = iq_interfere.read_idn
#         logger.info('IQ connected!')
#     try:
#         dt = dut.DUT('COM' + DUT_COM, DUT_BAUDRATE)
#     except Exception as err:
#         logger.info(err + Fore.RED + 'DUT Open fail!' + Style.RESET_ALL)
#     else:
#         logger.info('DUT connected!')
#
#     # TEST FLOW
#     filename = 'TEST_FLOW.txt'
#     f = open(filename)
#     result = list()
#     for line in f.readlines():
#         #logger.debug(len(line))
#         if len(line) < 30 or line.startswith('//'):
#             continue
#             pass
#         else:
#             line = line.strip()
#             line = line.split()
#             # logger.debug(line)
#             # logger.debug('Channel:', line[1], 'Rate:', line[2], 'Chain:', line[3])
#             item = line[0]
#             item = re.sub('IQ_WIFI_TEST_', '', item)
#             logger.debug(item)
#             channel = line[1]
#             rate = line[2]
#             chain = line[3]
#
#             # mode,bw,rates
#             if rate == '1M' or rate == '2M' or rate == '5.5M' or rate == '11M':
#                 mode = '11b'
#                 bw = '20'
#                 rates = re.sub('M', '', rate)
#                 per_spec = float(RX_PACKETS) * 0.08
#             elif rate == '6M' or rate == '9M' or rate == '12M' or rate == '18M' \
#                     or rate == '24M' or rate == '36M' or rate == '48M' or rate == '54M':
#                 if int(channel) < 5000:
#                     mode = '11g'
#                 else:
#                     mode = '11a'
#                 bw = '20'
#                 rates = re.sub('M', '', rate)
#                 per_spec = float(RX_PACKETS) * 0.1
#             elif rate == 'HT20-MCS0' or rate == 'HT20-MCS1' or rate == 'HT20-MCS2' or rate == 'HT20-MCS3' \
#                     or rate == 'HT20-MCS4' or rate == 'HT20-MCS5' or rate == 'HT20-MCS6' or rate == 'HT20-MCS7':
#                 if int(channel) < 5000:
#                     mode = '11ng'
#                 else:
#                     mode = '11na'
#                 bw = '20'
#                 rates = re.sub('HT20-MCS', '', rate)
#                 per_spec = float(RX_PACKETS) * 0.1
#             elif rate == 'HT40-MCS0' or rate == 'HT40-MCS1' or rate == 'HT40-MCS2' or rate == 'HT40-MCS3' \
#                     or rate == 'HT40-MCS4' or rate == 'HT40-MCS5' or rate == 'HT40-MCS6' or rate == 'HT40-MCS7':
#                 if int(channel) < 5000:
#                     mode = '11ng'
#                 else:
#                     mode = '11na'
#                 bw = '40'
#                 rates = re.sub('HT40-MCS', '', rate)
#                 per_spec = float(RX_PACKETS) * 0.1
#                 #channel = int(channel) - 10
#             elif rate == 'VHT20-MCS0' or rate == 'VHT20-MCS1' or rate == 'VHT20-MCS2' or rate == 'VHT20-MCS3' \
#                     or rate == 'VHT20-MCS4' or rate == 'VHT20-MCS5' or rate == 'VHT20-MCS6' or rate == 'VHT20-MCS7' or \
#                     rate == 'VHT20-MCS8':
#                 mode = '11ac'
#                 bw = '20'
#                 rates = re.sub('VHT20-MCS', '', rate)
#                 per_spec = float(RX_PACKETS) * 0.1
#             elif rate == 'VHT40-MCS0' or rate == 'VHT40-MCS1' or rate == 'VHT40-MCS2' or rate == 'VHT40-MCS3' \
#                     or rate == 'VHT40-MCS4' or rate == 'VHT40-MCS5' or rate == 'VHT40-MCS6' or rate == 'VHT40-MCS7' or \
#                     rate == 'VHT40-MCS8' or rate == 'VHT40-MCS9':
#                 mode = '11ac'
#                 bw = '40'
#                 rates = re.sub('VHT40-MCS', '', rate)
#                 per_spec = float(RX_PACKETS) * 0.1
#                 #channel = int(channel) - 10
#             elif rate == 'VHT80-MCS0' or rate == 'VHT80-MCS1' or rate == 'VHT80-MCS2' or rate == 'VHT80-MCS3' \
#                     or rate == 'VHT80-MCS4' or rate == 'VHT80-MCS5' or rate == 'VHT80-MCS6' or rate == 'VHT80-MCS7' or \
#                     rate == 'VHT80-MCS8' or rate == 'VHT80-MCS9':
#                 mode = '11ac'
#                 bw = '80'
#                 rates = re.sub('VHT80-MCS', '', rate)
#                 per_spec = float(RX_PACKETS) * 0.1
#             elif rate == 'VHT160-MCS0' or rate == 'VHT160-MCS1' or rate == 'VHT160-MCS2' or rate == 'VHT160-MCS3' \
#                     or rate == 'VHT160-MCS4' or rate == 'VHT160-MCS5' or rate == 'VHT160-MCS6' or rate == 'VHT160-MCS7' or \
#                     rate == 'VHT160-MCS8' or rate == 'VHT160-MCS9':
#                 mode = '11ac'
#                 bw = '160'
#                 rates = re.sub('VHT160-MCS', '', rate)
#                 per_spec = float(RX_PACKETS) * 0.1
#             elif rate == 'HE20-HE0' or rate == 'HE20-HE1' or rate == 'HE20-HE2' or rate == 'HE20-HE3' \
#                     or rate == 'HE20-HE4' or rate == 'HE20-HE5' or rate == 'HE20-HE6' or rate == 'HE20-HE7' or \
#                     rate == 'HE20-HE8' or rate == 'HE20-HE9' or rate == 'HE20-HE10' or rate == 'HE20-HE11':
#                 mode = '11ax'
#                 bw = '20'
#                 rates = re.sub('HE20-HE', '', rate)
#                 per_spec = float(RX_PACKETS) * 0.1
#             elif rate == 'HE40-HE0' or rate == 'HE40-HE1' or rate == 'HE40-HE2' or rate == 'HE40-HE3' \
#                     or rate == 'HE40-HE4' or rate == 'HE40-HE5' or rate == 'HE40-HE6' or rate == 'HE40-HE7' or \
#                     rate == 'HE40-HE8' or rate == 'HE40-HE9' or rate == 'HE40-HE10' or rate == 'HE40-HE11':
#                 mode = '11ax'
#                 bw = '40'
#                 rates = re.sub('HE40-HE', '', rate)
#                 per_spec = float(RX_PACKETS) * 0.1
#                 #channel = int(channel) - 10
#             elif rate == 'HE80-HE0' or rate == 'HE80-HE1' or rate == 'HE80-HE2' or rate == 'HE80-HE3' \
#                     or rate == 'HE80-HE4' or rate == 'HE80-HE5' or rate == 'HE80-HE6' or rate == 'HE80-HE7' or \
#                     rate == 'HE80-HE8' or rate == 'HE80-HE9' or rate == 'HE80-HE10' or rate == 'HE80-HE11':
#                 mode = '11ax'
#                 bw = '80'
#                 rates = re.sub('HE80-HE', '', rate)
#                 per_spec = float(RX_PACKETS) * 0.1
#             elif rate == 'HE160-HE0' or rate == 'HE160-HE1' or rate == 'HE160-HE2' or rate == 'HE160-HE3' \
#                     or rate == 'HE160-HE4' or rate == 'HE160-HE5' or rate == 'HE160-HE6' or rate == 'HE160-HE7' or \
#                     rate == 'HE160-HE8' or rate == 'HE160-HE9' or rate == 'HE160-HE10' or rate == 'HE160-HE11':
#                 mode = '11ax'
#                 bw = '160'
#                 rates = re.sub('HE160-HE', '', rate)
#                 per_spec = float(RX_PACKETS) * 0.1
#             # chain
#             chain = re.sub('CHAIN', '', chain)
#             path = chain
#             # read spec
#             if int(channel) < 5000:
#                 # INIT SPEC
#                 # 2.4g
#                 spec_file_2g = load_workbook('./spec_2g.xlsx')
#                 # logger.debug(spec_file.sheesnames)
#                 sheet_2g = spec_file_2g['Sheet1']
#                 rows_2g = []
#                 ratelist_2g = ['1M', '2M', '5_5M', '11M', '6M', '9M', '12M', '18M', '24M', '36M', '48M', '54M',
#                                'HT20_MCS0', 'HT20_MCS1', 'HT20_MCS2', 'HT20_MCS3', 'HT20_MCS4', 'HT20_MCS5',
#                                'HT20_MCS6', 'HT20_MCS7', 'HT40_MCS0', 'HT40_MCS1', 'HT40_MCS2', 'HT40_MCS3',
#                                'HT40_MCS4', 'HT40_MCS5', 'HT40_MCS6', 'HT40_MCS7', 'VHT20_MCS0', 'VHT20_MCS1',
#                                'VHT20_MCS2', 'VHT20_MCS3', 'VHT20_MCS4', 'VHT20_MCS5', 'VHT20_MCS6', 'VHT20_MCS7',
#                                'VHT20_MCS8', 'VHT40_MCS0', 'VHT40_MCS1', 'VHT40_MCS2', 'VHT40_MCS3', 'VHT40_MCS4',
#                                'VHT40_MCS5', 'VHT40_MCS6', 'VHT40_MCS7', 'VHT40_MCS8', 'VHT40_MCS9', 'HE20_HE0',
#                                'HE20_HE1', 'HE20_HE2', 'HE20_HE3', 'HE20_HE4', 'HE20_HE5', 'HE20_HE6',
#                                'HE20_HE7', 'HE20_HE8', 'HE20_HE9', 'HE20_HE10', 'HE20_HE11', 'HE40_HE0',
#                                'HE40_HE1', 'HE40_HE2', 'HE40_HE3', 'HE40_HE4', 'HE40_HE5', 'HE40_HE6',
#                                'HE40_HE7', 'HE40_HE8', 'HE40_HE9', 'HE40_HE10', 'HE40_HE11']
#                 for row_2g in sheet_2g:
#                     rows_2g.append(row_2g)
#                     # logger.debug(rows)
#                 for r in range(sheet_2g.max_row):
#                     for c in range(sheet_2g.max_column):
#                         # logger.debug(rows[r][c].value)
#                         rows_2g[r][c].value = str(rows_2g[r][c].value).strip()
#                         rs = r + 1
#                         cs = c + 1
#                         if rows_2g[r][c].value == 'POWER_ACCURACY':
#                             spec_pwr = abs(rows_2g[r][cs].value)
#                         elif rows_2g[r][c].value == 'Power_Gain_Index':
#                             gain_24 = abs(rows_2g[r][cs].value)
#                         elif rows_2g[r][c].value == 'EVM_MARGIN':
#                             evm_margin = abs(rows_2g[r][cs].value)
#                         elif rows_2g[r][c].value == 'Symbol_Clock_Error':
#                             spec_symbol_clock_error = abs(rows_2g[r][cs].value)
#                         elif rows_2g[r][c].value == 'XCAP':
#                             xcap = abs(rows_2g[r][cs].value)
#                         elif rows_2g[r][c].value == 'LO_Leakage':
#                             spec_lo_leakage = -abs(rows_2g[r][cs].value)
#                         elif rows_2g[r][c].value == 'MASK':
#                             spec_mask = abs(rows_2g[r][cs].value)
#                         elif rows_2g[r][c].value == 'OBW_20M':
#                             spec_obw_20M = rows_2g[r][cs].value
#                         elif rows_2g[r][c].value == 'OBW_40M':
#                             spec_obw_40M = rows_2g[r][cs].value
#                         for x in ratelist_2g:
#                             if rows_2g[r][c].value == x + '_power':
#                                 exec('target_pwr_%s=%d' % (x, rows_2g[rs][c].value))
#                                 break
#                         for i in ratelist_2g:
#                             if rows_2g[r][c].value == i + '_evm':
#                                 exec('target_EVM_%s=%d' % (i, rows_2g[rs][c].value))
#                                 break
#                         for j in ratelist_2g:
#                             if rows_2g[r][c].value == j + '_sens':
#                                 exec('target_sens_%s=%d' % (j, rows_2g[rs][c].value))
#                                 break
#                         for y in ratelist_2g:
#                             if rows_2g[r][c].value == y + '_aj':
#                                 exec('target_aj_%s=%d' % (y, rows_2g[rs][c].value))
#                                 break
#                         for k in ratelist_2g:
#                             if rows_2g[r][c].value == k + '_naj':
#                                 exec('target_naj_%s=%d' % (k, rows_2g[rs][c].value))
#                                 break
#                         spec_obw_80M = spec_obw_160M = None
#             else:
#                 # 5g
#                 spec_file_5g = load_workbook('./spec_5g.xlsx')
#                 # logger.debug(spec_file.sheesnames)
#                 sheet_5g = spec_file_5g['Sheet1']
#                 rows_5g = []
#                 ratelist_5g = ['6M', '9M', '12M', '18M', '24M', '36M', '48M', '54M', 'HT20_MCS0', 'HT20_MCS1',
#                                'HT20_MCS2', 'HT20_MCS3', 'HT20_MCS4', 'HT20_MCS5', 'HT20_MCS6', 'HT20_MCS7',
#                                'HT40_MCS0', 'HT40_MCS1', 'HT40_MCS2', 'HT40_MCS3', 'HT40_MCS4', 'HT40_MCS5',
#                                'HT40_MCS6', 'HT40_MCS7', 'VHT20_MCS0', 'VHT20_MCS1', 'VHT20_MCS2', 'VHT20_MCS3',
#                                'VHT20_MCS4', 'VHT20_MCS5', 'VHT20_MCS6', 'VHT20_MCS7', 'VHT20_MCS8', 'VHT40_MCS0',
#                                'VHT40_MCS1', 'VHT40_MCS2', 'VHT40_MCS3', 'VHT40_MCS4', 'VHT40_MCS5', 'VHT40_MCS6',
#                                'VHT40_MCS7', 'VHT40_MCS8', 'VHT40_MCS9', 'VHT80_MCS0', 'VHT80_MCS1', 'VHT80_MCS2',
#                                'VHT80_MCS3', 'VHT80_MCS4', 'VHT80_MCS5', 'VHT80_MCS6', 'VHT80_MCS7', 'VHT80_MCS8',
#                                'VHT80_MCS9', 'VHT160_MCS0', 'VHT160_MCS1', 'VHT160_MCS2',
#                                'VHT160_MCS3', 'VHT160_MCS4', 'VHT160_MCS5', 'VHT160_MCS6', 'VHT160_MCS7', 'VHT160_MCS8',
#                                'VHT160_MCS9', 'HE20_HE0', 'HE20_HE1', 'HE20_HE2', 'HE20_HE3', 'HE20_HE4',
#                                'HE20_HE5', 'HE20_HE6', 'HE20_HE7', 'HE20_HE8', 'HE20_HE9', 'HE20_HE10',
#                                'HE20_HE11', 'HE40_HE0', 'HE40_HE1', 'HE40_HE2', 'HE40_HE3', 'HE40_HE4',
#                                'HE40_HE5', 'HE40_HE6', 'HE40_HE7', 'HE40_HE8', 'HE40_HE9', 'HE40_HE10',
#                                'HE40_HE11', 'HE80_HE0', 'HE80_HE1', 'HE80_HE2', 'HE80_HE3', 'HE80_HE4',
#                                'HE80_HE5', 'HE80_HE6', 'HE80_HE7', 'HE80_HE8', 'HE80_HE9', 'HE80_HE10',
#                                'HE80_HE11', 'HE160_HE0', 'HE160_HE1', 'HE160_HE2', 'HE160_HE3', 'HE160_HE4',
#                                'HE160_HE5', 'HE160_HE6', 'HE160_HE7', 'HE160_HE8', 'HE160_HE9', 'HE160_HE10',
#                                'HE160_HE11']
#                 ratelist_evm_5g = ['6M_EVM', '9M_EVM', '12M_EVM', '18M_EVM', '24M_EVM', '36M_EVM', '48M_EVM',
#                                    '54M_EVM', 'HT20_MCS0_EVM', 'HT20_MCS1_EVM', 'HT20_MCS2_EVM', 'HT20_MCS3_EVM',
#                                    'HT20_MCS4_EVM', 'HT20_MCS5_EVM', 'HT20_MCS6_EVM', 'HT20_MCS7_EVM', 'HT40_MCS0_EVM',
#                                    'HT40_MCS1_EVM', 'HT40_MCS2_EVM', 'HT40_MCS3_EVM', 'HT40_MCS4_EVM', 'HT40_MCS5_EVM',
#                                    'HT40_MCS6_EVM', 'HT40_MCS7_EVM', 'VHT20_MCS0_EVM', 'VHT20_MCS1_EVM',
#                                    'VHT20_MCS2_EVM', 'VHT20_MCS3_EVM', 'VHT20_MCS4_EVM', 'VHT20_MCS5_EVM',
#                                    'VHT20_MCS6_EVM', 'VHT20_MCS7_EVM', 'VHT20_MCS8_EVM', 'VHT40_MCS0_EVM',
#                                    'VHT40_MCS1_EVM', 'VHT40_MCS2_EVM', 'VHT40_MCS3_EVM', 'VHT40_MCS4_EVM',
#                                    'VHT40_MCS5_EVM', 'VHT40_MCS6_EVM', 'VHT40_MCS7_EVM', 'VHT40_MCS8_EVM',
#                                    'VHT40_MCS9_EVM', 'VHT80_MCS0_EVM', 'VHT80_MCS1_EVM', 'VHT80_MCS2_EVM',
#                                    'VHT80_MCS3_EVM', 'VHT80_MCS4_EVM', 'VHT80_MCS5_EVM', 'VHT80_MCS6_EVM',
#                                    'VHT80_MCS7_EVM', 'VHT80_MCS8_EVM', 'VHT80_MCS9_EVM', 'VHT160_MCS0_EVM',
#                                    'VHT160_MCS1_EVM', 'VHT160_MCS2_EVM', 'VHT160_MCS3_EVM', 'VHT160_MCS4_EVM',
#                                    'VHT160_MCS5_EVM', 'VHT160_MCS6_EVM', 'VHT160_MCS7_EVM', 'VHT160_MCS8_EVM',
#                                    'VHT160_MCS9_EVM', 'HE20_HE0_EVM', 'HE20_HE1_EVM', 'HE20_HE2_EVM',
#                                    'HE20_HE3_EVM', 'HE20_HE4_EVM', 'HE20_HE5_EVM', 'HE20_HE6_EVM',
#                                    'HE20_HE7_EVM', 'HE20_HE8_EVM', 'HE20_HE9_EVM', 'HE20_HE10_EVM',
#                                    'HE20_HE11_EVM', 'HE40_HE0_EVM', 'HE40_HE1_EVM', 'HE40_HE2_EVM',
#                                    'HE40_HE3_EVM', 'HE40_HE4_EVM', 'HE40_HE5_EVM', 'HE40_HE6_EVM',
#                                    'HE40_HE7_EVM', 'HE40_HE8_EVM', 'HE40_HE9_EVM', 'HE40_HE10_EVM',
#                                    'HE40_HE11_EVM', 'HE80_HE0_EVM', 'HE80_HE1_EVM', 'HE80_HE2_EVM',
#                                    'HE80_HE3_EVM', 'HE80_HE4_EVM', 'HE80_HE5_EVM', 'HE80_HE6_EVM',
#                                    'HE80_HE7_EVM', 'HE80_HE8_EVM', 'HE80_HE9_EVM', 'HE80_HE10_EVM',
#                                    'HE80_HE11_EVM', 'HE160_HE0_EVM', 'HE160_HE1_EVM', 'HE160_HE2_EVM',
#                                    'HE160_HE3_EVM', 'HE160_HE4_EVM', 'HE160_HE5_EVM', 'HE160_HE6_EVM',
#                                    'HE160_HE7_EVM', 'HE160_HE8_EVM', 'HE160_HE9_EVM', 'HE160_HE10_EVM',
#                                    'HE160_HE11_EVM']
#                 for row_5g in sheet_5g:
#                     rows_5g.append(row_5g)
#                     # logger.debug(rows)
#                 for rr in range(sheet_5g.max_row):
#                     for cc in range(sheet_5g.max_column):
#                         # logger.debug(rows[r][c].value)
#                         rows_5g[rr][cc].value = str(rows_5g[rr][cc].value).strip()
#                         rrs = rr + 1
#                         ccs = cc + 1
#                         if rows_5g[rr][cc].value == 'POWER_ACCURACY':
#                             spec_pwr = abs(rows_5g[rr][ccs].value)
#                         elif rows_5g[rr][cc].value == 'Power_Gain_Index':
#                             gain_5 = abs(rows_5g[rr][ccs].value)
#                         elif rows_5g[rr][cc].value == 'EVM_MARGIN':
#                             evm_margin = abs(rows_5g[rr][ccs].value)
#                         elif rows_5g[rr][cc].value == 'Symbol_Clock_Error':
#                             spec_symbol_clock_error = abs(rows_5g[rr][ccs].value)
#                         elif rows_5g[rr][cc].value == 'XCAP':
#                             xcap = abs(rows_5g[rr][ccs].value)
#                         elif rows_5g[rr][cc].value == 'LO_Leakage':
#                             spec_lo_leakage = -abs(rows_5g[rr][ccs].value)
#                         elif rows_5g[rr][cc].value == 'MASK':
#                             spec_mask = abs(rows_5g[rr][ccs].value)
#                         elif rows_5g[rr][cc].value == 'OBW_20M':
#                             spec_obw_20M = rows_5g[rr][ccs].value
#                         elif rows_5g[rr][cc].value == 'OBW_40M':
#                             spec_obw_40M = rows_5g[rr][ccs].value
#                         elif rows_5g[rr][cc].value == 'OBW_80M':
#                             spec_obw_80M = rows_5g[rr][ccs].value
#                         elif rows_5g[rr][cc].value == 'OBW_160M':
#                             spec_obw_160M = rows_5g[rr][ccs].value
#                         for xx in ratelist_5g:
#                             if rows_5g[rr][cc].value == xx + '_target':
#                                 exec('target_pwr_%s=%d' % (xx, rows_5g[rrs][cc].value))
#                                 break
#                         for ii in ratelist_evm_5g:
#                             if rows_5g[rr][cc].value == ii + '_target':
#                                 exec('target_%s=%d' % (ii, rows_5g[rrs][cc].value))
#                                 break
#                         for jj in ratelist_5g:
#                             if rows_5g[rr][cc].value == jj + '_sens':
#                                 exec('target_%s_sens=%d' % (jj, rows_5g[rrs][cc].value))
#                                 break
#
#             logger.info('*************************************************************')
#
#             logger.info('Mode: ' + mode + ' Channel: ' + channel + ' BW: ' + bw + ' Rate: ' + rate + ' Chain: ' + chain)
#
#             if item == 'TX':
#                 adjust_result = result_evm = result_symbol_clock_error = result_lo_leakage = result_mask = \
#                     result_flasness = 'Pass'
#                 # dt.set_default()
#                 dt.tx()
#                 # RESULT
#                 rate_t = re.sub('-', '_', rate)
#                 rate_t = re.sub('\.', '_', rate_t)
#                 targetpower = eval('target_pwr_' + rate_t)
#                 rate_e = rate_t + '_EVM'
#                 spec_evm = eval('target_' + rate_e)
#                 iq.set_port(targetpower)
#                 iq.analysis()
#                 pwr_len, txq_len, data_pwr, data_txq = iq.get_status()
#                 avg_power, result_evm, result_symbol_clock_error, result_lo_leakage, result_mask = \
#                     iq.get_data(pwr_len, txq_len, data_pwr, data_txq, mode, channel, rate, chain, tx_result_name,
#                                 targetpower, spec_pwr, gain, spec_evm, evm_margin, spec_symbol_clock_error,
#                                 spec_lo_leakage, spec_mask, spec_obw_20M, spec_obw_40M, spec_obw_80M)
#                 if super_mode == '1':
#                     # if avg_power == 'NA' or result_evm == 'NA':
#                     if avg_power == 'NA' or float(avg_power) > 99.000:
#                         logger.info(Fore.RED + 'Error!' + Style.RESET_ALL)
#                     else:
#                         # accuracy_limit_left = 0.5
#                         # accuracy_limit_right = 0.5
#                         power_accuracy_left = float(targetpower) - float(spec_pwr) + float(accuracy_limit_left)
#                         power_accuracy_right = float(targetpower) + float(spec_pwr) - float(accuracy_limit_right)
#                         max_power = float(targetpower + spec_pwr)
#                         delta_power = float(avg_power) - float(targetpower)
#                         delta_power = float('{:.3f}'.format(delta_power))
#                         logger.debug('Default Measurer Power: ' + avg_power)
#                         logger.debug('Target Power: ' + targetpower)
#                         logger.debug('Delta Power: ' + delta_power)
#                         # power is nomal but some is fail
#                         if targetpower <= avg_power <= max_power:
#                             if result_evm == 'Fail' or result_symbol_clock_error == 'Fail' \
#                                     or result_lo_leakage == 'Fail' or result_mask == 'Fail':
#                                 logger.info(Fore.RED + 'TX\'s quality are failed!' + Style.RESET_ALL)
#                             else:
#                                 logger.info('Get Good Result!')
#                         # power is not nomal
#                         else:
#                             low_power_counts = 0
#                             setup = 2
#                             setups = 2
#                             logger.debug('Step:' + setup)
#                             init_value = dt.get_paras()
#                             pwr_paras = init_value + setup
#                             pwr_paras = hex(pwr_paras)
#                             pwr_paras = re.sub('0x', '', pwr_paras)
#                             get_power = []
#                             get_delta_power = []
#                             c = 1
#                             get_power.append(avg_power)
#                             logger.debug('Measurer Power List: '+get_power)
#                             get_delta_power.append(delta_power)
#                             logger.debug('Power Deviation List: ' + get_delta_power)
#                             logger.debug('Adjust Counts:' + c)
#                             # ADJUST
#                             min_adj = avg_power - targetpower
#                             max_adj = avg_power - max_power
#                             while min_adj < 0 or max_adj > 0:
#                                 logger.info(Fore.GREEN + 'Adjust...' + Style.RESET_ALL)
#                                 if avg_power > max_power:
#                                     adj = -1
#                                 else:
#                                     adj = 1
#                                 c = c + 1
#                                 logger.debug('NEW VALUE(HEX):', channel_groups, pwr_paras)
#                                 gain = dt.adjust_power()
#                                 iq.analysis()
#                                 pwr_len, txq_len, data_pwr, data_txq = iq.get_status()
#                                 avg_power, result_evm, result_symbol_clock_error, result_lo_leakage, result_mask = \
#                                     iq.get_data(pwr_len, txq_len, data_pwr, data_txq, mode, channel, rate, chain,
#                                                 tx_result_name, targetpower, spec_pwr, gain, spec_evm, evm_margin,
#                                                 spec_symbol_clock_error, spec_lo_leakage, spec_mask, spec_obw_20M,
#                                                 spec_obw_40M, spec_obw_80M)
#                                 get_power.append(avg_power)
#                                 logger.debug('Measurer Power List: ' + get_power)
#                                 delta_power = float(avg_power) - targetpower
#                                 delta_power = float('{:.3f}'.format(delta_power))
#                                 avg_power = float(avg_power)
#                                 min_adj = avg_power - targetpower
#                                 max_adj = avg_power - max_power
#                                 get_delta_power.append(delta_power)
#                                 logger.debug('Power Deviation List: ' + get_delta_power)
#                                 logger.debug('Adjust Counts: ' + c)
#                                 adjust_status = get_delta_power[c - 1] - get_delta_power[c - 2]
#                                 adjust_status = float('{:.3f}'.format(adjust_status))
#                                 logger.debug('Power Added: ' + adjust_status)
#                                 if adjust_status < 0.1:
#                                     adjust_result = 'Pass'
#                                     setup = 2 * setups * adj
#                                     low_power_counts = low_power_counts + 1
#                                 elif adjust_status > 0.1:
#                                     adjust_status = 'Pass'
#                                     setup = 2 * adj
#                                 # logger.debug(low_power_counts)
#                                 if low_power_counts > 5:
#                                     logger.info(Fore.RED + 'Power added was too small, Power adjust stop' + Style.RESET_ALL)
#                                     adjust_result = 'Fail'
#                                 else:
#                                     logger.debug('Step: ' + setup)
#                                     pwr_paras = int(pwr_paras, 16)
#                                     pwr_paras = int(pwr_paras) + setup
#                                     pwr_paras = hex(pwr_paras)
#                                     pwr_paras = re.sub('0x', '', pwr_paras)
#                                     logger.debug(result_evm + result_symbol_clock_error + result_lo_leakage + result_mask)
#                                     logger.info('*************************************************************')
#                 dt.tx_off()
#             elif item == 'RX':
#                 start = int(line[4])
#                 stop = int(line[5])
#                 per_list = []
#                 sens_list = []
#                 logger.info('Start: ' + str(start) + ' Stop: ' + str(stop))
#                 # loss = iq.read_pathloss(channel, chain)
#                 # dt.set_default()
#                 dt.get_statistics() #reset counts
#                 dt.rx_on()
#                 dt.rx()
#                 # logger.debug(channel)
#                 iq.vsg()
#                 per = dt.get_statistics()
#                 per = int(per)
#                 per_list.append(per)
#                 sens_list.append(start)
#                 while start > stop and per <= int(per_spec):
#                     start = start - 1
#                     # dt.rx(mode, channel, bw, rates, chain)
#                     # dt.rx()
#                     iq.vsg()
#                     time.sleep(sleep_time)
#                     per = dt.get_statistics()
#                     per = int(per)
#                     per_list.append(per)
#                     sens_list.append(start)
#                     if rx_dynamic == '1':
#                         if per <= per_spec:
#                             per_result = 'Pass'
#                         else:
#                             per_result = 'Fail'
#                         with open('./Result/' + rx_dynamic_result, 'a+', newline='') as f2:
#                             writer2 = csv.writer(f2)
#                             writer2.writerow([channel, rate, chain, start, rx_packets, per, per_result])
#                 logger.debug(str(len(per_list))+str(per_list))
#                 logger.debug(str(len(sens_list))+str(sens_list))
#                 per = per_list[len(per_list) - 2]
#                 sens = sens_list[len(sens_list) - 2]
#                 logger.info('Sensitivity: ' + str(sens))
#                 rate_t = re.sub('-', '_', rate)
#                 rate_t = re.sub('\.', '_', rate_t)
#                 rate_e = rate_t + '_sens'
#                 sens_spec = eval('target_' + rate_e)
#                 if sens > sens_spec:
#                     result = 'Fail'
#                 else:
#                     result = 'Pass'
#                 with open('./Result/' + rx_result_name, 'a+', newline='') as f2:
#                     writer2 = csv.writer(f2)
#                     writer2.writerow([channel, rate, chain, sens_spec, sens, rx_packets, per, result])
#                 logger.info('*************************************************************')
#                 dt.rx_off()
#             elif item == 'AJ':
#                 # GET SENS
#                 start = int(line[4])
#                 sens_list = []
#                 per_list = []
#                 logger.info('Start: ' + str(start))
#                 dt.get_statistics()  # reset counts
#                 dt.rx_on()
#                 dt.rx()
#                 # logger.debug(channel)
#                 iq.vsg(mw_iq, start)
#                 per = dt.get_statistics()
#                 per_list.append(per)
#                 sens_list.append(start)
#                 while int(per) <= int(per_spec):
#                     start = start - 1
#                     # dt.rx(mode, channel, bw, rates, chain)
#                     # dt.rx()
#                     iq.vsg(mw_iq, start)
#                     per = dt.get_statistics()
#                     per_list.append(per)
#                     sens_list.append(start)
#                 logger.debug(str(len(per_list)) + str(per_list))
#                 logger.debug(str(len(sens_list)) + str(sens_list))
#                 per = per_list[-2]
#                 sens = sens_list[-2]
#                 logger.info('Sensitivity: ' + str(sens))
#                 # AJ TEST
#                 aj_list = []
#                 aj_per_list = []
#                 # AJ sens
#                 if mode == '11b':
#                     aj_sens = sens + 6
#                 else:
#                     aj_sens = sens + 3
#                 # GET SENS SPEC
#                 rate_t = re.sub('-', '_', rate)
#                 rate_t = re.sub('\.', '_', rate_t)
#                 aj_spec = eval('target_aj_' + rate_t)
#                 aj_start = aj_sens + aj_spec
#                 # AJ aj_vsg
#                 iq_interfere.vsg_aj(mw_iq_inter, aj_start)
#                 iq.vsg(mw_iq, aj_sens)
#                 aj_per = dt.get_statistics()
#                 aj_per_list.append(per)
#                 aj_list.append(aj_start)
#                 while int(aj_per) <= int(per_spec):
#                     aj_start = aj_start + 1
#                     # dt.rx(mode, channel, bw, rates, chain)
#                     # dt.rx()
#                     iq_interfere.vsg_aj(mw_iq_inter, aj_start)
#                     iq.vsg(mw_iq, aj_sens)
#                     aj_per = dt.get_statistics()
#                     aj_per_list.append(aj_per)
#                     aj_list.append(aj_start)
#                 logger.debug(str(len(aj_per_list)) + str(aj_per_list))
#                 logger.debug(str(len(aj_list)) + str(aj_list))
#                 aj_per = aj_per_list[-2]
#                 aj = aj_list[-2] - aj_sens
#                 logger.info('Adjacent Channel Rejection: ' + str(aj))
#                 # RESULT
#                 if aj > aj_spec:
#                     result = 'Fail'
#                 else:
#                     result = 'Pass'
#                 with open('./Result/' + aj_result_name, 'a+', newline='') as f2:
#                     writer2 = csv.writer(f2)
#                     writer2.writerow([channel, rate, chain, aj_spec, aj, result])
#                 logger.info('*************************************************************')
#                 dt.rx_off()
#
#     logger.info('************************TEST DONE****************************')
#     dt.close()
#     iq.close()
line = ''
print(line)
line = line.strip()
print(line)
line = line.split()
print(line)