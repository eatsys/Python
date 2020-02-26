#!/user/bin/env python
# encoding: utf-8
#@time      : 2019/11/14 15:09

__author__ = 'Ethan'

from config import conf

# Equip
SA_IP = str(conf.SA_ip_get()).strip()
SG_WANTED_IP = str(conf.SGWANGTED_ip_get()).strip()
SG_JAMMER1_IP = str(conf.SGJAMMER1_ip_get()).strip()
SG_JAMMER2_IP = str(conf.SGJAMMER2_ip_get()).strip()

# PATHLOSS
PATHLOSS_SA = str(conf.pathloss_sawanted_get()).strip()
PATHLOSS_SG_WANTED = str(conf.pathloss_sgwanted_get())
PATHLOSS_SG_JAMMER = str(conf.pathloss_sgjammer_get())

# DUT
DUT_IP = str(conf.DUT_ip_get()).strip()
DUT_COM = str(conf.DUT_com_get()).strip()
DUT_BAUDRATE = str(conf.DUT_baudrate_get()).strip()
DUT_USERNAME = str(conf.DUT_username_get()).strip()
DUT_PASSWORD = str(conf.DUT_password_get()).strip()
EXT1 = str(conf.DUT_ext1_get()).strip()
EXT2 = str(conf.DUT_ext2_get()).strip()
EXT3 = str(conf.DUT_ext3_get()).strip()

# LOG
LOG_ENABLE = str(conf.log_get()).strip()

# CALIBRATION
CALI = str(conf.calibration_get()).strip()

# TEST
AUTO_ADJUST_POWER = str(conf.auto_adjustpower_get()).strip()
accuracy_limit_left = str(conf.accuracylimit_left_get()).strip()
accuracy_limit_right = str(conf.accuracylimit_right_get()).strip()
RX_PACKETS = str(conf.RX_packets_get()).strip()
RX_DYNAMIC = str(conf.rx_dynamic_get()).strip()
