# -*- coding: utf-8 -*-
# @Time    : 2019/3/26 15:19
# @Author  : Ethan
"""the main control, get the configure for entire test system """

import os
import shutil
import time
import win32api, win32con
import config
import get_rssi
from get_file_client import get_RSSI_file
from att import Attenuate
from pdv import Controller
from chariot import chariot
from data.write_datas import channel_write, atten_write, angle_write, ap_rssi_write, tx_linkrate_write
import reporteight
import logging
LOG_FORMAT = "%(asctime)s - %(pathname)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

logging.basicConfig(filename='./log/log.txt', level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


def set_all_att(att_num, att_value):
    att_x = 1
    logging.info(format(att_x, att_num))
    get_ip = config.Config()
    while int(att_x) <= int(att_num):
        ip = eval('get_ip.Atten_%d_ip_get()' % att_x)
        logging.info('att ip:{0},{0}'.format(att_x, ip))
        Att_SetToEquip = Attenuate(ip)
        Att_SetToEquip.set_att(att_value)
        att_x += 1
    logging.info('Attenuate configure success!')


def set_swivel_table(angle, com):
    swivel_table_value = 360.0 / int(angle) * 0.5
    logging.info(format(swivel_table_value))
    wait_table_time = 80/int(angle)
    file = '.\swiveltable\panel_state.txt'
    f1 = open(file, 'w')
    f1.write('4096\r\n')
    f1.write('4096\r\n')
    f1.write('4096\r\n')
    f1.write('4096\r\n')
    f1.write('-12800.000000\r\n')
    f1.write('12800.000000\r\n')
    f1.write('12800.000000\r\n')
    f1.write('12800.000000\r\n')
    f1.write('128\r\n')
    f1.write('128\r\n')
    f1.write('128\r\n')
    f1.write('128\r\n')
    f1.write(str(swivel_table_value) + '\r\n')
    f1.write('1\r\n')
    f1.write('1\r\n')
    f1.write('1\r\n')
    f1.write(com + '\r\n')
    f1.write('4096\r\n')
    f1.write('0\r\n')
    f1.write('12800\r\n')
    f1.write('32767\r\n')
    f1.write('32767\r\n')
    f1.write('32767\r\n')
    f1.write('32767\r\n')
    f1.write('0\r\n')
    f1.write('1\r\n')
    f1.write('1\r\n')
    f1.write('1\r\n')
    f1.write('1\r\n')
    f1.close()
    return wait_table_time


def test():
    # ready for config
    conf = config.Config()
    # get ap name
    AP_TYPE = str(conf.Ap_type_get())
    # delete old data
    win32api.MessageBox(0, "When the test start, it will delete the result file,"
                           " Please transport your test result first!", "Warning", win32con.MB_OK)
    logging.warning('When the test start, it will delete the result file,'
                   ' Please transport your test result first!')
    directory_IX = os.path.exists(r'./Result/IxChariotOD/'+AP_TYPE)
    directory_DATA = os.path.exists(r'./Result/Data/'+AP_TYPE)
    if directory_IX is True:
        #os.remove(r'./Result/IxChariotOD/*.*')
        shutil.rmtree(r'./Result/IxChariotOD/'+AP_TYPE)
        logging.warning('Delete IxChariotOD file')
    if directory_DATA is True:
        shutil.rmtree(r'./Result/Data'+AP_TYPE)
        logging.warning('Delete Data file')
    # get ssid
    ssid = conf.SSID_get()
    # get att and generate att list
    atten_start = int(conf.Atten_start_get())
    atten_end = int(conf.Atten_end_get())
    atten_step = int(conf.Atten_step_get())
    att = atten_start
    attenuate_list = []
    while att <= atten_end:
        attenuate_list.append(att)
        att = att + atten_step
    logging.info('ATT LIST:{0}'.format(attenuate_list))
    # get att num
    att_num = conf.Atten_num_get()
    # get angle num and create angle list
    angle_num = conf.angle_num_get()
    logging.info('ANGLE NUM:{0}'.format(angle_num))
    angle_setup = 360.0 / float(angle_num)
    angle = 0
    angle_list = []
    while angle < 360.0:
        angle_list.append(angle)
        angle += angle_setup
    logging.info('ANGLE LIST:{0}'.format(angle_list))
    # get table COM
    com = conf.table_com_get()
    logging.info('COM:{0}'.format(com))
    # set swivel table
    wait_table_time = set_swivel_table(angle_num, com)
    # ready for get RSSI
    get_RSSI = get_rssi.get_rssi()
    sta_ip = conf.Sta_address()
    sta_user = conf.Sta_username()
    sta_pwd = conf.Sta_password()
    get_RSSI.login(sta_ip, sta_user, sta_pwd)
    get_RSSI.creat_ssid()

    #test
    for i in attenuate_list:
        logging.info('ATT:{0}'.format(i))
        retval = os.getcwd()
        logging.info('path check:{0}'.format(retval))
        att_set_config = config.Con_current_atten(i)
        att_set_config.write_atten()
        set_all_att(att_num, i)
        atten_write(str(i))
        # get channel
        channel = conf.Channel_get()
        channel_write(str(channel))
        for x in angle_list:
            logging.info('ANGLE:{0}'.format(x))
            retval = os.getcwd()
            logging.info('path check:{0}'.format(retval))
            angle_set_config = config.Con_current_angle(x)
            angle_set_config.write_angle()
            angle_write(str(x))
            if x == 0:
                pass
            else:
                Controller()
                time.sleep(wait_table_time)
            # excute rssi program on the station and gernerate AP's rssi file
            get_RSSI.get_rssi_value()
            # get rssi file
            rssi, link_rate = get_RSSI_file()
            # write ap's rssi and linkrate
            ap_rssi_write(str(rssi).strip())
            tx_linkrate_write(str(link_rate).strip())
            # get station's rssi and linkrate
            # sta_rssi()
            chariot()


if __name__ == "__main__":
    test()
    reporteight.Generate_Test_Report_eight()
