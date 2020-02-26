#!/user/bin/env python
# encoding: utf-8
# @Author  : Ethan
# @time    : 2020/1/14 11:28

from __future__ import division
from colorama import init, Fore, Style
from parameters import SA_IP, SG_WANTED_IP, SG_JAMMER1_IP, SG_JAMMER2_IP, DUT_IP, DUT_USERNAME, DUT_PASSWORD, \
    EXT1, EXT2, EXT3, LOG_ENABLE, PATHLOSS_SA, PATHLOSS_SG_WANTED, PATHLOSS_SG_JAMMER
from sa import SA
from sg import SG
from dut import DUT
import logging
import os
import time
import sys
import re
logger = logging.getLogger


def folder():
    # generate result and log
    directory_r = os.path.exists(r'./Result')
    if directory_r is False:
        os.makedirs('Result')

    directory_l = os.path.exists(r'./log')
    if directory_l is False:
        os.makedirs('log')


if __name__ == '__main__':
    init(autoreset=True)

    # GEN TIME
    now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())

    # log
    logger.setLevel(logging.DEBUG)  # logger level

    #  create a handler，for log.txt
    file_handler = logging.FileHandler('./log/log_' + now_time + '.txt', mode='w')
    file_handler.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
    # log formatter
    file_handler.setFormatter(
        logging.Formatter(
            fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
    )
    # add handler to logger
    logger.addHandler(file_handler)

    # create a handler，for output to screen
    console_handler = logging.StreamHandler()
    if LOG_ENABLE == '1':
        console_handler.setLevel(logging.DEBUG)  # log level
    else:
        console_handler.setLevel(logging.INFO)  # log level
    console_handler.setFormatter(
        logging.Formatter(
            fmt='%(asctime)s - %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
    )
    logger.addHandler(console_handler)

    try:
        Number = sys.argv[1]
    except:
        Number = input("SN:")
    sn = "SN_" + Number

    try:
        filename = sys.argv[2]
    except:
        filename = 'TEST_FLOW.txt'

    # connect equipments and dut
    try:
        sa = SA(SA_IP)
    except Exception as err:
        logger.info(err)
        sa = None
        logger.info(Fore.RED + 'SA connect fail!' + Style.RESET_ALL)
        exit(1)
    else:
        sa.read_idn
        sa.set_pathloss(PATHLOSS_SA)
        logger.info('SA connected!')
    try:
        sg_wanted = SG(SG_WANTED_IP)
    except Exception as err:
        logger.info(err)
        sg_wanted = None
        logger.info(Fore.RED + 'SG connect fail!' + Style.RESET_ALL)
    else:
        sg_wanted.read_idn
        sg_wanted.set_pathloss(PATHLOSS_SG_WANTED)
        logger.info('SG connected!')
    try:
        sg_jammer1 = SG(SG_JAMMER1_IP)
    except Exception as err:
        logger.info(err)
        sg_jammer1 = None
        logger.info(Fore.RED + 'SG JAMMER1 connect fail!' + Style.RESET_ALL)
    else:
        sg_jammer1.read_idn
        sg_jammer1.set_pathloss(PATHLOSS_SG_JAMMER)
        logger.info('SG connected!')
    try:
        sg_jammer2 = SG(SG_JAMMER2_IP)
    except Exception as err:
        logger.info(err)
        sg_jammer2 = None
        logger.info(Fore.RED + 'SG JAMMER2 connect fail!' + Style.RESET_ALL)
    else:
        sg_jammer2.read_idn
        sg_jammer2.set_pathloss(PATHLOSS_SG_JAMMER)
        logger.info('SG connected!')
    try:
        dt = DUT()
    except Exception as err:
        logger.info(err + Fore.RED + 'DUT Open fail!' + Style.RESET_ALL)
    else:
        dt.login(DUT_IP, DUT_USERNAME, DUT_PASSWORD)
        dt.init(EXT1, EXT2, EXT3)
        logger.info('DUT connected!')

        # TEST FLOW
        # filename = 'TEST_FLOW.txt'
        f = open(filename)
        result = list()
        for line in f.readlines():
            # logger.debug(len(line))
            if len(line) < 30 or line.startswith('//') or line.isspace():
                continue
                pass
            else:
                line = line.strip()
                line = line.split()
                # logger.debug(line)
                # logger.debug('Channel:', line[1], 'Rate:', line[2], 'Chain:', line[3])
                item = line[0]
                item = re.sub('5G_TEST_', '', item)
                logger.debug(item)
                channel = line[1]
                rate = line[2]
                chain = line[3]