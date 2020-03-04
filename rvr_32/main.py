# -*- coding: utf-8 -*-
# @Time    : 2019/3/26 15:19
# @Author  : Ethan
"""the main control, get the configure for entire test system
    2019.8.8 增加switch控制， STA类型还未使用，暂注释
             空口及传导测试类型已增加
    """

import logging
import os
import shutil
import time
import threading
import win32api
import win32con

from config import Config, Con_current_atten, Con_current_angle
from Throught import Throught
from att import Attenuate
from chariot import chariot_tx, chariot_rx
from data.parameters import AP_TYPE, HOST_IP, RADIO, USER_NAME, PASSWORD, SSID, RADIO, CHANNEL, AP_COM, AP_BAUDRATE, \
    STA_TYPE, STA_ADDRESS, STA_USERNAME, STA_PASSWORD, STA_SWITCHIP, STA_SWITCHPORT, ATTENUATE_LIST, ATTEN_NUM, \
    ANGLE_LIST, ANGLE_NUM, TABLE_COM, RUN_TPYE
from data.write_datas import channel_write, atten_write, angle_write, ap_rssi_write, tx_linkrate_write, \
    sta_rssi_write, rx_linkrate_write, mcs_txrate_write, mcs_rxrate_write, nss_txrate_write, nss_rxrate_write, \
    bw_txrate_write, bw_rxrate_write, rssi_txant_write, power_txant_write, rssi_rxant_write, power_rxant_write
from report import Generate_Test_Report
from rssi_product import product_RSSI_telnet, product_RSSI_ssh, product_RSSI_com
from rssi_wirelesscard_ssh import get_rssi
from switch import Switch
from pdv_dll import PDV

logger = logging.getLogger()

AP_COM = 'COM' + AP_COM


def set_all_att(att_num, att_value):
    att_x = 1
    get_ip = Config()
    if int(CHANNEL) < 30:
        att_value = int(att_value) + 12
    else:
        att_value = int(att_value) + 18
    while int(att_x) <= int(att_num):
        ip = eval(f'get_ip.Atten_{att_x}_ip_get()')
        logger.info('att ip:{0},{0}'.format(att_x, ip))
        Att_SetToEquip = Attenuate(ip)
        Att_SetToEquip.set_att(att_value)
        att_x += 1
    logger.info('Attenuate configure success!')


def set_swivel_table(angle, com, direction):
    pdv = PDV(com)
    pdv.open()
    pdv.set_maxspeed()
    if direction == 'clockwise':
        pdv.set_distance(-12800.000000)
        swivel_table_value = 360.0 / int(angle) * 0.5
        logger.info(format(swivel_table_value))
        wait_table_time = 80 / int(angle)
    else:
        pdv.set_distance(12800.000000)
        swivel_table_value = 360.0 / int(angle) * 0.5 * (int(angle) - 1)
        logger.info(format(swivel_table_value))
        wait_table_time = 20
    pdv.join_data()
    pdv.action()
    pdv.stop()
    return wait_table_time


def test():
    retval = os.getcwd()
    result_file = retval + '/Result/Data/' + AP_TYPE + '_' + RADIO + '/'
    ixchraiot_file = retval + '/Result/IxChariotOD/' + AP_TYPE + '_' + RADIO + '/'
    win32api.MessageBox(0, "测试开始前会清空和测试项目名称一致的数据文件夹(Result)，若数据有用，请备份后再点击确认开始测试\r\n"
                           "When the test start, it will delete the result file,"
                           " Please transport your test result firstly!", "Warning", win32con.MB_OK)
    logger.warning('When the test start, it will delete the result file,Please transport your test result firstly!')

    isExists_rf = os.path.exists(result_file)
    isExists_if = os.path.exists(ixchraiot_file)
    if not isExists_rf:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(result_file)
        logger.info(result_file + ' Create Success')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        logger.info(result_file + ' file is exist, delete and create new')
        shutil.rmtree(result_file)
        os.makedirs(result_file)

    if not isExists_if:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(ixchraiot_file)
        logger.info(ixchraiot_file + ' Create Success')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        logger.info(ixchraiot_file + ' file is exist, delete and create new')
        shutil.rmtree(ixchraiot_file)
        os.makedirs(ixchraiot_file)
    # set swivel table
    # wait_table_time = set_swivel_table(ANGLE_NUM, TABLE_COM, 'clockwise')
    # # set sta type
    # swt = Switch(STA_SWITCHIP)
    # swt.set_default()
    # swt.set_switch_sta(STA_SWITCHPORT)
    # set run type OTA or Conductive
    swta = Switch('192.168.100.41')
    # swta.set_default()
    swta.set_switch_runtype()
    if ATTEN_NUM > 4:
        swtb = Switch('192.168.100.42')
        swtb.set_default()
        swtb.set_switch_runtype()
    # test
    # set swivel counts
    swivel_count = 0
    for i in ATTENUATE_LIST:
        if RUN_TPYE == '0' and int(CHANNEL) < 20:
            i += 56
        elif RUN_TPYE == '0' and int(CHANNEL) > 30:
            i += 69
        elif RUN_TPYE == '1' and int(channel) < 20:
            i += 12
        elif RUN_TPYE == '1' and int(CHANNEL) > 30:
            i += 18
        logger.info(f'ATT:{i}')
        retval = os.getcwd()
        logger.info(f'path check:{retval}')
        att_set_config = Con_current_atten(i)
        att_set_config.write_atten()
        set_all_att(ATTEN_NUM, i)
        ## set fixed ota att
        atten_write(str(i))
        logger.info('Wait for single good!')
        time.sleep(1)
        # get channel
        channel_write(str(CHANNEL))
        # swivel table set to default
        if ANGLE_NUM > 1 and swivel_count == 0:
            pass
        elif ANGLE_NUM > 1 and swivel_count > 0:
            wait_table_time = set_swivel_table(ANGLE_NUM, TABLE_COM, 'counter')
            # Controller()
            logger.info('Waiting for swivel table back to zero...')
            time.sleep(wait_table_time)

        swivel_count += 1
        for x in ANGLE_LIST:
            logger.info(f'ANGLE:{x}')
            retval = os.getcwd()
            logger.info(f'path check:{retval}')
            angle_set_config = Con_current_angle(x)
            angle_set_config.write_angle()
            angle_write(str(x))
            if x == 0:
                pass
            else:
                # Controller()
                wait_table_time = set_swivel_table(ANGLE_NUM, TABLE_COM, 'clockwise')
                time.sleep(wait_table_time)
            # get RSSI and link rate info

            if AP_TYPE == 'WF-194' and STA_TYPE == 'WirelessCard':
                # run chariot
                chariot_tx()
                # get AP's RSSI and link rate info
                sta_rssi, tx_link_rate = get_rssi(STA_ADDRESS, STA_USERNAME, STA_PASSWORD)
                # get station's rssi and linkrate
                P_sta_rssi = product_RSSI_telnet(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                channel, tx_link_rate, rx_link_rate, sta_rssi = P_sta_rssi.get_RSSI(RADIO)
            elif AP_TYPE == 'WF-194' and STA_TYPE == 'WF-194':
                def get_statistics_tx():
                    # get  info
                    P_ap = product_RSSI_telnet(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                    # P_ap.login(USER_NAME, PASSWORD)
                    # P_sta.login(STA_USERNAME, STA_PASSWORD)
                    # get radio id
                    ap_power, ap_radio_2g, ap_radio_5g = P_ap.get_testradio_qca()
                    get_channel, tx_link_rate, rx_link_rate, ap_rssi, tx_nss_avg, rx_nss_avg = \
                        P_ap.get_APRSSI_qca(RADIO, ap_radio_2g, ap_radio_5g)
                    # write ap's rssi and linkrate
                    # ap_rssi_write(str(ap_rssi).strip())
                    # channel_write(str(get_channel))
                    tx_linkrate_write(str(tx_link_rate).strip())
                    power_txant_write(str(ap_power).strip())
                    P_ap.close()

                    P_sta = product_RSSI_telnet(STA_ADDRESS, STA_USERNAME, STA_PASSWORD, RADIO, AP_TYPE)
                    sta_power, sta_radio_2g, sta_radio_5g = P_sta.get_testradio_qca()
                    sta_rssi, tx_mcs, tx_nss, tx_bw, sta_rssi_chain0, sta_rssi_chain1, sta_rssi_chain2, \
                    sta_rssi_chain3, sta_rssi_chain4, sta_rssi_chain5, sta_rssi_chain6, sta_rssi_chain7 = \
                        P_sta.get_rxcounts_qca(RADIO, sta_radio_2g, sta_radio_5g)
                    sta_rssi_write(str(sta_rssi).strip())
                    rssi_txant_write(str(sta_rssi_chain0).strip() + str(sta_rssi_chain1).strip() +
                                     str(sta_rssi_chain2).strip() + str(sta_rssi_chain3).strip() +
                                     str(sta_rssi_chain4).strip() + str(sta_rssi_chain5).strip() +
                                     str(sta_rssi_chain6).strip() + str(sta_rssi_chain7).strip())
                    P_sta.close()

                def get_statistics_rx():
                    # get  info
                    P_ap = product_RSSI_telnet(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                    # P_ap.login(USER_NAME, PASSWORD)
                    # P_sta.login(STA_USERNAME, STA_PASSWORD)
                    # get radio id
                    ap_power, ap_radio_2g, ap_radio_5g = P_ap.get_testradio_qca()
                    get_channel, tx_link_rate, rx_link_rate, ap_rssi, tx_nss_avg, rx_nss_avg = \
                        P_ap.get_APRSSI_qca(RADIO, ap_radio_2g, ap_radio_5g)
                    ap_rssi_nouse, rx_mcs, rx_nss, rx_bw, ap_rssi_chain0, ap_rssi_chain1, ap_rssi_chain2, \
                    ap_rssi_chain3, ap_rssi_chain4, ap_rssi_chain5, ap_rssi_chain6, ap_rssi_chain7 = \
                        P_ap.get_rxcounts_qca(RADIO, ap_radio_2g, ap_radio_5g)
                    # write ap's rssi and linkrate
                    ap_rssi_write(str(ap_rssi).strip())
                    rx_linkrate_write(str(rx_link_rate).strip())
                    power_rxant_write(str(sta_power).strip())
                    rssi_rxant_write(str(ap_rssi_chain0).strip() + str(ap_rssi_chain1).strip() +
                                     str(ap_rssi_chain2).strip() + str(ap_rssi_chain3).strip() +
                                     str(ap_rssi_chain4).strip() + str(ap_rssi_chain5).strip() +
                                     str(ap_rssi_chain6).strip() + str(ap_rssi_chain7).strip())
                    P_ap.close()

                # main
                # tx
                P_sta = product_RSSI_telnet(STA_ADDRESS, STA_USERNAME, STA_PASSWORD, RADIO, AP_TYPE)
                # P_sta.login(STA_USERNAME, STA_PASSWORD)
                P_sta.qca_reset()
                P_sta.close()
                # run chariot and get rssi
                threads_tx = []
                threads_tx.append(threading.Thread(target=chariot_tx))
                threads_tx.append(threading.Thread(target=get_statistics_tx))
                logger.debug(threads_tx)
                for tx in threads_tx:
                    logger.debug(tx)
                    tx.start()
                for tx in threads_tx:
                    tx.join()
                # get counts
                P_sta = product_RSSI_telnet(STA_ADDRESS, STA_USERNAME, STA_PASSWORD, RADIO, AP_TYPE)
                sta_power, sta_radio_2g, sta_radio_5g = P_sta.get_testradio_qca()
                sta_rssi, tx_mcs, tx_nss, tx_bw, sta_rssi_chain0, sta_rssi_chain1, sta_rssi_chain2, \
                sta_rssi_chain3, sta_rssi_chain4, sta_rssi_chain5, sta_rssi_chain6, sta_rssi_chain7 = \
                    P_sta.get_rxcounts_qca(RADIO, sta_radio_2g, sta_radio_5g)
                # write data
                mcs_txrate_write(str(tx_mcs).strip())
                nss_txrate_write(str(tx_nss).strip())
                bw_txrate_write(str(tx_bw).strip())

                # rx
                P_ap = product_RSSI_telnet(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                P_ap.qca_reset()
                P_ap.close()
                # run chariot and get rssi
                threads_rx = []
                threads_rx.append(threading.Thread(target=chariot_rx))
                threads_rx.append(threading.Thread(target=get_statistics_rx))
                logger.debug(threads_rx)
                for rx in threads_rx:
                    logger.debug(rx)
                    rx.start()
                for rx in threads_rx:
                    rx.join()

                # write
                # write ap's rssi and linkrate
                # get counts
                P_ap = product_RSSI_telnet(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                ap_power, ap_radio_2g, ap_radio_5g = P_ap.get_testradio_qca()
                ap_rssi, rx_mcs, rx_nss, rx_bw, ap_rssi_chain0, ap_rssi_chain1, ap_rssi_chain2, \
                ap_rssi_chain3, ap_rssi_chain4, ap_rssi_chain5, ap_rssi_chain6, ap_rssi_chain7 = \
                    P_ap.get_rxcounts_qca(RADIO, ap_radio_2g, ap_radio_5g)
                # write data
                mcs_rxrate_write(str(rx_mcs).strip())
                nss_rxrate_write(str(rx_nss).strip())
                bw_rxrate_write(str(rx_bw).strip())
            elif AP_TYPE == 'WF-8186' and STA_TYPE == 'WF-8186':
                def get_statistics_tx():
                    # get AP's RSSI and link rate info
                    P_ap_counts = product_RSSI_telnet(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                    P_ap_counts.login(USER_NAME, PASSWORD)
                    channel, ap_link_rate, ap_mcs, ap_nss, ap_bw, ap_power_ant0, ap_power_ant1, ap_power_ant2, \
                    ap_power_ant3 = P_ap_counts.get_counts_bcm(RADIO)
                    # get sta rssi
                    P_sta_rssi = product_RSSI_telnet(STA_ADDRESS, STA_USERNAME, STA_PASSWORD, RADIO, AP_TYPE)
                    P_sta_rssi.login(STA_USERNAME, STA_PASSWORD)
                    sta_rssi, sta_rssi_ant0, sta_rssi_ant1, sta_rssi_ant2, sta_rssi_ant3 = P_sta_rssi.get_RSSI_bcm(
                        RADIO)
                    # write tx rssi and linkrate
                    # channel.write(str(channel).strip())
                    sta_rssi_write(str(sta_rssi).strip())
                    tx_linkrate_write(str(ap_link_rate).strip())
                    mcs_txrate_write(str(ap_mcs).strip())
                    nss_txrate_write(str(ap_nss).strip())
                    bw_txrate_write(str(ap_bw).strip())
                    rssi_txant_write(
                        str(
                            'rssi[0]' + sta_rssi_ant0 + ' ' + 'rssi[1]' + sta_rssi_ant1 + ' ' + 'rssi[2]' + sta_rssi_ant2
                            + ' ' + 'rssi[3]' + sta_rssi_ant3))
                    power_txant_write(
                        str(ap_power_ant0 + ' ' + ap_power_ant1 + ' ' + ap_power_ant2 + ' ' + ap_power_ant3))
                    P_ap_counts.close()
                    P_sta_rssi.close()

                def get_statistics_rx():
                    # get station's rssi and linkrate
                    P_sta_counts = product_RSSI_telnet(STA_ADDRESS, STA_USERNAME, STA_PASSWORD, RADIO, AP_TYPE)
                    P_sta_counts.login(STA_USERNAME, STA_PASSWORD)
                    channel, sta_link_rate, sta_mcs, sta_nss, sta_bw, sta_power_ant0, sta_power_ant1, sta_power_ant2, \
                    sta_power_ant3 = P_sta_counts.get_counts_bcm(RADIO)
                    P_ap_rssi = product_RSSI_telnet(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                    P_ap_rssi.login(USER_NAME, PASSWORD)
                    ap_rssi, ap_rssi_ant0, ap_rssi_ant1, ap_rssi_ant2, ap_rssi_ant3 = P_ap_rssi.get_RSSI_bcm(
                        RADIO)
                    # write sta's rssi and linkrate
                    ap_rssi_write(str(ap_rssi).strip())
                    rx_linkrate_write(str(sta_link_rate).strip())
                    mcs_rxrate_write(str(sta_mcs).strip())
                    nss_rxrate_write(str(sta_nss).strip())
                    bw_rxrate_write(str(sta_bw).strip())
                    rssi_rxant_write(str('rssi[0]' + ap_rssi_ant0 + ' ' + 'rssi[1]' + ap_rssi_ant1 + ' ' + 'rssi[2]' +
                                         ap_rssi_ant2 + ' ' + 'rssi[3]' + ap_rssi_ant3))
                    power_rxant_write(
                        str(sta_power_ant0 + ' ' + sta_power_ant1 + ' ' + sta_power_ant2 + ' ' + sta_power_ant3))

                # MAIN
                threads_tx = []
                threads_tx.append(threading.Thread(target=chariot_tx))
                threads_tx.append(threading.Thread(target=get_statistics_tx))
                logger.debug(threads_tx)
                for tx in threads_tx:
                    logger.debug(tx)
                    tx.start()
                for tx in threads_tx:
                    tx.join()

                threads_rx = []
                threads_rx.append(threading.Thread(target=chariot_rx))
                threads_rx.append(threading.Thread(target=get_statistics_rx))
                logger.debug(threads_rx)
                for rx in threads_rx:
                    logger.debug(rx)
                    rx.start()
                for rx in threads_rx:
                    rx.join()
            elif AP_TYPE == 'WF-8186' and STA_TYPE == 'ASUS':
                def get_statistics_tx():
                    sta_rssi = ap_link_rate = ap_mcs = ap_nss = ap_bw = sta_rssi_ant0 = sta_rssi_ant1 = sta_rssi_ant2 \
                        = sta_rssi_ant3 = ap_power_ant0 = ap_power_ant1 = ap_power_ant2 = ap_power_ant3 = '999'
                    # get AP's RSSI and link rate info
                    P_ap_counts = product_RSSI_telnet(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                    P_ap_counts.login(USER_NAME, PASSWORD)
                    channel, ap_link_rate, ap_mcs, ap_nss, ap_bw, ap_power_ant0, ap_power_ant1, ap_power_ant2, \
                    ap_power_ant3 = P_ap_counts.get_counts_bcm(RADIO)
                    # get sta rssi
                    # P_sta_rssi = product_RSSI_telnet(STA_ADDRESS, STA_USERNAME, STA_PASSWORD, RADIO, AP_TYPE)
                    # sta_rssi, sta_rssi_ant0, sta_rssi_ant1, sta_rssi_ant2, sta_rssi_ant3 = P_sta_rssi.get_RSSI_bcm(RADIO)
                    # write tx rssi and linkrate
                    sta_rssi_write(str(sta_rssi).strip())
                    tx_linkrate_write(str(ap_link_rate).strip())
                    mcs_txrate_write(str(ap_mcs).strip())
                    nss_txrate_write(str(ap_nss).strip())
                    bw_txrate_write(str(ap_bw).strip())
                    rssi_txant_write(
                        str(
                            'rssi[0]' + sta_rssi_ant0 + ' ' + 'rssi[1]' + sta_rssi_ant1 + ' ' + 'rssi[2]' + sta_rssi_ant2
                            + ' ' + 'rssi[3]' + sta_rssi_ant3))
                    power_txant_write(
                        str(ap_power_ant0 + ' ' + ap_power_ant1 + ' ' + ap_power_ant2 + ' ' + ap_power_ant3))
                    P_ap_counts.close()
                    # P_sta_rssi.close()

                def get_statistics_rx():
                    ap_rssi = sta_link_rate = sta_mcs = sta_nss = sta_bw = ap_rssi_ant0 = ap_rssi_ant1 = ap_rssi_ant2 \
                        = ap_rssi_ant3 = sta_power_ant0 = sta_power_ant1 = sta_power_ant2 = sta_power_ant3 = '999'
                    # get station's rssi and linkrate
                    # P_sta_counts = product_RSSI_telnet(STA_ADDRESS, STA_USERNAME, STA_PASSWORD, RADIO, AP_TYPE)
                    # #P_sta_rssi.login(USER_NAME, PASSWORD)
                    # channel, sta_link_rate, sta_mcs, sta_nss, sta_bw, sta_power_ant0, sta_power_ant1, sta_power_ant2, \
                    # sta_power_ant3 = P_sta_counts.get_counts_bcm(RADIO)
                    P_ap_rssi = product_RSSI_telnet(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                    P_ap_rssi.login(USER_NAME, PASSWORD)
                    ap_rssi, ap_rssi_ant0, ap_rssi_ant1, ap_rssi_ant2, ap_rssi_ant3 = P_ap_rssi.get_RSSI_bcm(
                        RADIO)
                    # write sta's rssi and linkrate
                    ap_rssi_write(str(ap_rssi).strip())
                    rx_linkrate_write(str(sta_link_rate).strip())
                    mcs_rxrate_write(str(sta_mcs).strip())
                    nss_rxrate_write(str(sta_nss).strip())
                    bw_rxrate_write(str(sta_bw).strip())
                    rssi_rxant_write(str('rssi[0]' + ap_rssi_ant0 + ' ' + 'rssi[1]' + ap_rssi_ant1 + ' ' + 'rssi[2]' +
                                         ap_rssi_ant2 + ' ' + 'rssi[3]' + ap_rssi_ant3))
                    power_rxant_write(
                        str(sta_power_ant0 + ' ' + sta_power_ant1 + ' ' + sta_power_ant2 + ' ' + sta_power_ant3))
                    P_ap_rssi.close()

                threads_tx = []
                threads_tx.append(threading.Thread(target=chariot_tx))
                threads_tx.append(threading.Thread(target=get_statistics_tx))
                logger.debug(threads_tx)
                for tx in threads_tx:
                    logger.debug(tx)
                    tx.start()
                for tx in threads_tx:
                    tx.join()

                threads_rx = []
                threads_rx.append(threading.Thread(target=chariot_rx))
                threads_rx.append(threading.Thread(target=get_statistics_rx))
                logger.debug(threads_rx)
                for rx in threads_rx:
                    logger.debug(rx)
                    rx.start()
                for rx in threads_rx:
                    rx.join()
            elif AP_TYPE == 'WF-8401' and STA_TYPE == 'WF-8186':
                def get_statistics_tx():
                    # # get tx linkrate
                    # P_ap = product_RSSI_telnet_ssh(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                    # ap_link_rate, NONE_RSSI, NONE_ANT0_AVG, NONE_ANT1_AVG, NONE_ANT2_AVG, NONE_ANT3_AVG = P_ap.get_RSSI_marvellap(RADIO)
                    # get sta rssi
                    P_sta_rssi = product_RSSI_telnet(STA_ADDRESS, STA_USERNAME, STA_PASSWORD, RADIO, AP_TYPE)
                    P_sta_rssi.login(STA_USERNAME, STA_PASSWORD)
                    sta_rssi, sta_rssi_ant0, sta_rssi_ant1, sta_rssi_ant2, sta_rssi_ant3 = P_sta_rssi.get_RSSI_bcm(
                        RADIO)
                    # write tx rssi and linkrate
                    sta_rssi_write(str(sta_rssi).strip())
                    rssi_txant_write(
                        str(
                            'rssi[0]' + sta_rssi_ant0 + ' ' + 'rssi[1]' + sta_rssi_ant1 + ' ' + 'rssi[2]' + sta_rssi_ant2
                            + ' ' + 'rssi[3]' + sta_rssi_ant3))
                    P_sta_rssi.close()

                def get_statistics_rx():
                    # get AP rssi and linkrate
                    P_ap_rssi = product_RSSI_ssh(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                    ap_linkrate_none, ap_rssi, ap_rssi_ant0, ap_rssi_ant1, ap_rssi_ant2, ap_rssi_ant3 = P_ap_rssi.get_RSSI_marvellap(
                        RADIO)
                    # get counts in sta
                    P_sta_counts = product_RSSI_telnet(STA_ADDRESS, STA_USERNAME, STA_PASSWORD, RADIO, AP_TYPE)
                    P_sta_counts.login(STA_USERNAME, STA_PASSWORD)
                    channel, sta_link_rate, sta_mcs, sta_nss, sta_bw, sta_power_ant0, sta_power_ant1, sta_power_ant2, \
                    sta_power_ant3 = P_sta_counts.get_counts_bcm(RADIO)
                    # write sta's rssi and linkrate
                    ap_rssi_write(str(ap_rssi).strip())
                    rx_linkrate_write(str(sta_link_rate).strip())
                    mcs_rxrate_write(str(sta_mcs).strip())
                    nss_rxrate_write(str(sta_nss).strip())
                    bw_rxrate_write(str(sta_bw).strip())
                    rssi_rxant_write(str('rssi[0]' + ap_rssi_ant0 + ' ' + 'rssi[1]' + ap_rssi_ant1 + ' ' + 'rssi[2]' +
                                         ap_rssi_ant2 + ' ' + 'rssi[3]' + ap_rssi_ant3))
                    power_rxant_write(
                        str(sta_power_ant0 + ' ' + sta_power_ant1 + ' ' + sta_power_ant2 + ' ' + sta_power_ant3))
                    P_ap_rssi.close()
                    P_sta_counts.close()

                # for 8401 tx
                P_ap_counts = product_RSSI_ssh(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                P_ap_counts.counts_reset()
                ap_link_rate, NONE_RSSI, NONE_ANT0_AVG, NONE_ANT1_AVG, NONE_ANT2_AVG, NONE_ANT3_AVG = P_ap_counts.get_RSSI_marvellap(
                    RADIO)
                tx_linkrate_write(str(ap_link_rate).strip())
                P_ap_counts.close()

                threads_tx = []
                threads_tx.append(threading.Thread(target=chariot_tx))
                threads_tx.append(threading.Thread(target=get_statistics_tx))
                logger.debug(threads_tx)
                for tx in threads_tx:
                    logger.debug(tx)
                    tx.start()
                for tx in threads_tx:
                    tx.join()

                P_ap_counts = product_RSSI_ssh(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                ap_mcs = P_ap_counts.get_txcounts_marvellap(RADIO)
                mcs_txrate_write(str(ap_mcs).strip())
                ap_nss = ap_mcs
                nss_txrate_write(str(ap_nss).strip())
                ap_bw = ap_mcs
                bw_txrate_write(str(ap_bw).strip())
                power_txant_write('')
                P_ap_counts.close()

                # for 8401 rx
                threads_rx = []
                threads_rx.append(threading.Thread(target=chariot_rx))
                threads_rx.append(threading.Thread(target=get_statistics_rx))
                logger.debug(threads_rx)
                for rx in threads_rx:
                    logger.debug(rx)
                    rx.start()
                for rx in threads_rx:
                    rx.join()
            elif AP_TYPE == 'Marvell_Demo' and STA_TYPE == 'WF-8186':
                def get_statistics_tx():
                    # # get tx linkrate
                    # P_ap = product_RSSI_telnet_ssh(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                    # ap_link_rate, NONE_RSSI, NONE_ANT0_AVG, NONE_ANT1_AVG, NONE_ANT2_AVG, NONE_ANT3_AVG = P_ap.get_RSSI_marvellap(RADIO)
                    # get sta rssi
                    P_sta_rssi = product_RSSI_telnet(STA_ADDRESS, STA_USERNAME, STA_PASSWORD, RADIO, AP_TYPE)
                    P_sta_rssi.login(STA_USERNAME, STA_PASSWORD)
                    sta_rssi, sta_rssi_ant0, sta_rssi_ant1, sta_rssi_ant2, sta_rssi_ant3 = P_sta_rssi.get_RSSI_bcm(
                        RADIO)
                    # write tx rssi and linkrate
                    sta_rssi_write(str(sta_rssi).strip())
                    rssi_txant_write(
                        str(
                            'rssi[0]' + sta_rssi_ant0 + ' ' + 'rssi[1]' + sta_rssi_ant1 + ' ' + 'rssi[2]' + sta_rssi_ant2
                            + ' ' + 'rssi[3]' + sta_rssi_ant3))
                    P_sta_rssi.close()

                def get_statistics_rx():
                    # get AP rssi and linkrate
                    # P_ap_rssi = product_RSSI_ssh(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                    # ap_linkrate_none, ap_rssi, ap_rssi_ant0, ap_rssi_ant1, ap_rssi_ant2, ap_rssi_ant3 = P_ap_rssi.get_RSSI_marvellap(
                    #     RADIO)
                    ap_rssi = ap_rssi_ant0 = ap_rssi_ant1 = ap_rssi_ant2 = ap_rssi_ant3 = '100'
                    # get counts in sta
                    P_sta_counts = product_RSSI_telnet(STA_ADDRESS, STA_USERNAME, STA_PASSWORD, RADIO, AP_TYPE)
                    P_sta_counts.login(STA_USERNAME, STA_PASSWORD)
                    channel, sta_link_rate, sta_mcs, sta_nss, sta_bw, sta_power_ant0, sta_power_ant1, sta_power_ant2, \
                    sta_power_ant3 = P_sta_counts.get_counts_bcm(RADIO)
                    # write sta's rssi and linkrate
                    ap_rssi_write(str(ap_rssi).strip())
                    rx_linkrate_write(str(sta_link_rate).strip())
                    mcs_rxrate_write(str(sta_mcs).strip())
                    nss_rxrate_write(str(sta_nss).strip())
                    bw_rxrate_write(str(sta_bw).strip())
                    rssi_rxant_write(str('rssi[0]' + ap_rssi_ant0 + ' ' + 'rssi[1]' + ap_rssi_ant1 + ' ' + 'rssi[2]' +
                                         ap_rssi_ant2 + ' ' + 'rssi[3]' + ap_rssi_ant3))
                    power_rxant_write(
                        str(sta_power_ant0 + ' ' + sta_power_ant1 + ' ' + sta_power_ant2 + ' ' + sta_power_ant3))
                    # P_ap_rssi.close()
                    P_sta_counts.close()

                # for 8401 tx
                # P_ap_counts = product_RSSI_ssh(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                # P_ap_counts.counts_reset()
                # ap_link_rate, NONE_RSSI, NONE_ANT0_AVG, NONE_ANT1_AVG, NONE_ANT2_AVG, NONE_ANT3_AVG = P_ap_counts.get_RSSI_marvellap(
                #     RADIO)
                ap_link_rate = '100'
                tx_linkrate_write(str(ap_link_rate).strip())
                # P_ap_counts.close()

                threads_tx = []
                threads_tx.append(threading.Thread(target=chariot_tx))
                threads_tx.append(threading.Thread(target=get_statistics_tx))
                logger.debug(threads_tx)
                for tx in threads_tx:
                    logger.debug(tx)
                    tx.start()
                for tx in threads_tx:
                    tx.join()

                # P_ap_counts = product_RSSI_ssh(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                # ap_mcs = P_ap_counts.get_txcounts_marvellap(RADIO)
                ap_mcs = '100'
                mcs_txrate_write(str(ap_mcs).strip())
                ap_nss = ap_mcs
                nss_txrate_write(str(ap_nss).strip())
                ap_bw = ap_mcs
                bw_txrate_write(str(ap_bw).strip())
                power_txant_write('')
                # P_ap_counts.close()

                # for 8401 rx
                threads_rx = []
                threads_rx.append(threading.Thread(target=chariot_rx))
                threads_rx.append(threading.Thread(target=get_statistics_rx))
                logger.debug(threads_rx)
                for rx in threads_rx:
                    logger.debug(rx)
                    rx.start()
                for rx in threads_rx:
                    rx.join()
            elif AP_TYPE == 'WF-8401' and STA_TYPE == 'Marvell_Demo':
                def get_statistics_tx():
                    pass
                    # get tx linkrate
                    # P_ap = product_RSSI_ssh(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                    # ap_link_rate, NONE_RSSI, NONE_ANT0_AVG, NONE_ANT1_AVG, NONE_ANT2_AVG, NONE_ANT3_AVG = P_ap.get_RSSI_marvellap(RADIO)
                    # get sta rssi
                    # P_sta_rssi = product_RSSI(STA_ADDRESS, STA_USERNAME, STA_PASSWORD, RADIO, AP_TYPE)
                    # P_sta_rssi.login(STA_USERNAME, STA_PASSWORD)
                    # sta_rssi, sta_rssi_ant0, sta_rssi_ant1, sta_rssi_ant2, sta_rssi_ant3 = P_sta_rssi.get_RSSI_bcm(
                    #     RADIO)
                    # # write tx rssi and linkrate
                    # sta_rssi_write(str(sta_rssi).strip())
                    # rssi_txant_write(
                    #     str(
                    #         'rssi[0]' + sta_rssi_ant0 + ' ' + 'rssi[1]' + sta_rssi_ant1 + ' ' + 'rssi[2]' + sta_rssi_ant2
                    #         + ' ' + 'rssi[3]' + sta_rssi_ant3))
                    # P_sta_rssi.close()

                def get_statistics_rx():
                    # get AP rssi and linkrate
                    P_ap_rssi = product_RSSI_ssh(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                    ap_linkrate_none, ap_rssi, ap_rssi_ant0, ap_rssi_ant1, ap_rssi_ant2, ap_rssi_ant3 = P_ap_rssi.get_RSSI_marvellap(
                        RADIO)
                    # get counts in sta
                    # P_sta_counts = product_RSSI(STA_ADDRESS, STA_USERNAME, STA_PASSWORD, RADIO, AP_TYPE)
                    # P_sta_counts.login(STA_USERNAME, STA_PASSWORD)
                    # channel, sta_link_rate, sta_mcs, sta_nss, sta_bw, sta_power_ant0, sta_power_ant1, sta_power_ant2, \
                    # sta_power_ant3 = P_sta_counts.get_counts_bcm(RADIO)
                    # write sta's rssi and linkrate
                    ap_rssi_write(str(ap_rssi).strip())
                    # rx_linkrate_write(str(sta_link_rate).strip())
                    # mcs_rxrate_write(str(sta_mcs).strip())
                    # nss_rxrate_write(str(sta_nss).strip())
                    # bw_rxrate_write(str(sta_bw).strip())
                    rssi_rxant_write(str('rssi[0]' + ap_rssi_ant0 + ' ' + 'rssi[1]' + ap_rssi_ant1 + ' ' + 'rssi[2]' +
                                         ap_rssi_ant2 + ' ' + 'rssi[3]' + ap_rssi_ant3))
                    # power_rxant_write(
                    #     str(sta_power_ant0 + ' ' + sta_power_ant1 + ' ' + sta_power_ant2 + ' ' + sta_power_ant3))
                    P_ap_rssi.close()
                    # P_sta_counts.close()

                # for 8401 tx
                P_ap_counts = product_RSSI_ssh(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                P_ap_counts.counts_reset()
                ap_link_rate, NONE_RSSI, NONE_ANT0_AVG, NONE_ANT1_AVG, NONE_ANT2_AVG, NONE_ANT3_AVG = P_ap_counts.get_RSSI_marvellap(
                    RADIO)
                tx_linkrate_write(str(ap_link_rate).strip())
                P_ap_counts.close()

                threads_tx = []
                threads_tx.append(threading.Thread(target=chariot_tx))
                threads_tx.append(threading.Thread(target=get_statistics_tx))
                logger.debug(threads_tx)
                for tx in threads_tx:
                    logger.debug(tx)
                    tx.start()
                for tx in threads_tx:
                    tx.join()

                P_ap_counts = product_RSSI_ssh(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                ap_mcs = P_ap_counts.get_txcounts_marvellap(RADIO)
                mcs_txrate_write(str(ap_mcs).strip())
                ap_nss = ap_mcs
                nss_txrate_write(str(ap_nss).strip())
                ap_bw = ap_mcs
                bw_txrate_write(str(ap_bw).strip())
                power_txant_write('')
                P_ap_counts.close()

                # for 8401 rx
                threads_rx = []
                threads_rx.append(threading.Thread(target=chariot_rx))
                threads_rx.append(threading.Thread(target=get_statistics_rx))
                logger.debug(threads_rx)
                for rx in threads_rx:
                    logger.debug(rx)
                    rx.start()
                for rx in threads_rx:
                    rx.join()
            elif AP_TYPE == 'WF-8401' and STA_TYPE == 'ASUS':
                def get_statistics_tx():
                    pass
                    # get tx linkrate
                    # P_ap = product_RSSI_ssh(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                    # ap_link_rate, NONE_RSSI, NONE_ANT0_AVG, NONE_ANT1_AVG, NONE_ANT2_AVG, NONE_ANT3_AVG = P_ap.get_RSSI_marvellap(RADIO)
                    # get sta rssi
                    # P_sta_rssi = product_RSSI(STA_ADDRESS, STA_USERNAME, STA_PASSWORD, RADIO, AP_TYPE)
                    # P_sta_rssi.login(STA_USERNAME, STA_PASSWORD)
                    # sta_rssi, sta_rssi_ant0, sta_rssi_ant1, sta_rssi_ant2, sta_rssi_ant3 = P_sta_rssi.get_RSSI_bcm(
                    #     RADIO)
                    # # write tx rssi and linkrate
                    sta_rssi = '999'
                    sta_rssi_ant0 = sta_rssi_ant1 = sta_rssi_ant2 = sta_rssi_ant3 = '999'
                    sta_rssi_write(str(sta_rssi).strip())
                    rssi_txant_write(
                        str(
                            'rssi[0]' + sta_rssi_ant0 + ' ' + 'rssi[1]' + sta_rssi_ant1 + ' ' + 'rssi[2]' + sta_rssi_ant2
                            + ' ' + 'rssi[3]' + sta_rssi_ant3))
                    # P_sta_rssi.close()

                def get_statistics_rx():
                    # get AP rssi and linkrate
                    P_ap_rssi = product_RSSI_ssh(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                    ap_linkrate_none, ap_rssi, ap_rssi_ant0, ap_rssi_ant1, ap_rssi_ant2, ap_rssi_ant3 = P_ap_rssi.get_RSSI_marvellap(
                        RADIO)
                    # get counts in sta
                    # P_sta_counts = product_RSSI(STA_ADDRESS, STA_USERNAME, STA_PASSWORD, RADIO, AP_TYPE)
                    # P_sta_counts.login(STA_USERNAME, STA_PASSWORD)
                    # channel, sta_link_rate, sta_mcs, sta_nss, sta_bw, sta_power_ant0, sta_power_ant1, sta_power_ant2, \
                    # sta_power_ant3 = P_sta_counts.get_counts_bcm(RADIO)
                    # write sta's rssi and linkrate
                    ap_rssi_write(str(ap_rssi).strip())
                    sta_link_rate = '999'
                    rx_linkrate_write(str(sta_link_rate).strip())
                    # mcs_rxrate_write(str(sta_mcs).strip())
                    # nss_rxrate_write(str(sta_nss).strip())
                    # bw_rxrate_write(str(sta_bw).strip())
                    rssi_rxant_write(str('rssi[0]' + ap_rssi_ant0 + ' ' + 'rssi[1]' + ap_rssi_ant1 + ' ' + 'rssi[2]' +
                                         ap_rssi_ant2 + ' ' + 'rssi[3]' + ap_rssi_ant3))
                    # power_rxant_write(
                    #     str(sta_power_ant0 + ' ' + sta_power_ant1 + ' ' + sta_power_ant2 + ' ' + sta_power_ant3))
                    P_ap_rssi.close()
                    # P_sta_counts.close()

                # for 8401 tx
                P_ap_counts = product_RSSI_ssh(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                P_ap_counts.counts_reset()
                ap_link_rate, NONE_RSSI, NONE_ANT0_AVG, NONE_ANT1_AVG, NONE_ANT2_AVG, NONE_ANT3_AVG = P_ap_counts.get_RSSI_marvellap(
                    RADIO)
                tx_linkrate_write(str(ap_link_rate).strip())
                P_ap_counts.close()

                threads_tx = []
                threads_tx.append(threading.Thread(target=chariot_tx))
                threads_tx.append(threading.Thread(target=get_statistics_tx))
                logger.debug(threads_tx)
                for tx in threads_tx:
                    logger.debug(tx)
                    tx.start()
                for tx in threads_tx:
                    tx.join()

                P_ap_counts = product_RSSI_ssh(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                ap_mcs = P_ap_counts.get_txcounts_marvellap(RADIO)
                mcs_txrate_write(str(ap_mcs).strip())
                ap_nss = '999'
                nss_txrate_write(str(ap_nss).strip())
                ap_bw = '999'
                bw_txrate_write(str(ap_bw).strip())
                ap_power = '999'
                power_txant_write(str(ap_power).strip())
                P_ap_counts.close()

                # for 8401 rx
                P_sta_counts = product_RSSI_ssh(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                P_sta_counts.counts_reset()
                P_sta_counts.close()

                threads_rx = []
                threads_rx.append(threading.Thread(target=chariot_rx))
                threads_rx.append(threading.Thread(target=get_statistics_rx))
                logger.debug(threads_rx)
                for rx in threads_rx:
                    logger.debug(rx)
                    rx.start()
                for rx in threads_rx:
                    rx.join()

                P_sta_counts = product_RSSI_ssh(HOST_IP, USER_NAME, PASSWORD, RADIO, AP_TYPE)
                sta_mcs = P_sta_counts.get_txcounts_marvellap(RADIO)
                mcs_rxrate_write(str(sta_mcs).strip())
                sta_nss = '999'
                nss_rxrate_write(str(sta_nss).strip())
                sta_bw = '999'
                bw_rxrate_write(str(sta_bw).strip())
                sta_power = '999'
                power_rxant_write(str(sta_power).strip())
                P_sta_counts.close()
            elif AP_TYPE == 'AR610' and STA_TYPE == 'WirelessCard':
                def get_statistics_tx():
                    # get  info
                    P_ap = product_RSSI_com(AP_COM, AP_BAUDRATE)
                    P_ap.login(USER_NAME, PASSWORD)
                    # P_sta.login(STA_USERNAME, STA_PASSWORD)
                    # get radio id
                    get_channel, ap_radio_2g, ap_radio_5g = P_ap.get_testradio_hi()
                    sta_mac = P_ap.get_sta_mac(RADIO, ap_radio_2g, ap_radio_5g)
                    tx_link_rate = P_ap.get_txlinkrate(RADIO, ap_radio_2g, ap_radio_5g)
                    sta_rssi = P_ap.get_starssi(RADIO, ap_radio_2g, ap_radio_5g, sta_mac)
                    channel_write(str(get_channel))
                    tx_linkrate_write(str(tx_link_rate).strip())
                    ap_power = None
                    power_txant_write(str(ap_power).strip())
                    sta_rssi_write(str(sta_rssi).strip())
                    sta_rssi_chain0 = sta_rssi_chain1 = None
                    rssi_txant_write(str(sta_rssi_chain0).strip() + str(sta_rssi_chain1).strip())
                    tx_mcs = tx_nss = tx_bw = None
                    mcs_txrate_write(str(tx_mcs).strip())
                    nss_txrate_write(str(tx_nss).strip())
                    bw_txrate_write(str(tx_bw).strip())
                    P_ap.close()

                def get_statistics_rx():
                    # get  info
                    P_ap = product_RSSI_com(AP_COM, AP_BAUDRATE)
                    P_ap.login(USER_NAME, PASSWORD)
                    # P_sta.login(STA_USERNAME, STA_PASSWORD)
                    # get radio id
                    get_channel, ap_radio_2g, ap_radio_5g = P_ap.get_testradio_hi()
                    rx_link_rate = P_ap.get_rxlinkrate(RADIO, ap_radio_2g, ap_radio_5g)
                    ap_rssi, ap_rssi_chain0, ap_rssi_chain1 = P_ap.get_aprssi(RADIO, ap_radio_2g, ap_radio_5g)
                    rx_linkrate_write(str(rx_link_rate).strip())
                    sta_power = None
                    power_rxant_write(str(sta_power).strip())
                    ap_rssi_write(str(ap_rssi).strip())
                    rssi_rxant_write(str(ap_rssi_chain0).strip() + str(ap_rssi_chain1).strip())
                    rx_mcs = rx_nss = rx_bw = None
                    mcs_rxrate_write(str(rx_mcs).strip())
                    nss_rxrate_write(str(rx_nss).strip())
                    bw_rxrate_write(str(rx_bw).strip())
                    P_ap.close()

                # main
                # tx
                # run chariot and get rssi
                threads_tx = []
                threads_tx.append(threading.Thread(target=chariot_tx))
                threads_tx.append(threading.Thread(target=get_statistics_tx))
                logger.debug(threads_tx)
                for tx in threads_tx:
                    logger.debug(tx)
                    tx.start()
                for tx in threads_tx:
                    tx.join()

                # rx
                # run chariot and get rssi
                threads_rx = []
                threads_rx.append(threading.Thread(target=chariot_rx))
                threads_rx.append(threading.Thread(target=get_statistics_rx))
                logger.debug(threads_rx)
                for rx in threads_rx:
                    logger.debug(rx)
                    rx.start()
                for rx in threads_rx:
                    rx.join()

            else:
                chariot_tx()
                chariot_rx()

            # write tp value
            rx = RADIO + '_' + CHANNEL + '_' + str(i) + '_' + str(x) + '_Rx.txt'
            tx = RADIO + '_' + CHANNEL + '_' + str(i) + '_' + str(x) + '_Tx.txt'
            throught = Throught(rx, tx)
            throught.get_tx_throught_simple()
            throught.get_rx_throught_simple()


if __name__ == "__main__":
    test()
    Generate_Test_Report()
