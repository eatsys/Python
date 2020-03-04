#!/user/bin/env python
# encoding: utf-8
#@time      : 2019/11/14 15:09

__author__ = 'Ethan'

from config import conf

# IQ
IQ_IP = str(conf.IQ_ip_get()).strip()
IQ_PORT = str(conf.IQ_port_get()).strip()
IQ_ROUT = str(conf.IQ_rout_get()).strip()
EVM_AG = str(conf.evm_11ag_get()).strip()
EVM_N = str(conf.evm_11n_get()).strip()
EVM_AC = str(conf.evm_11ac_get()).strip()
EVM_AX = str(conf.evm_11ax_get()).strip()
RL = str(conf.Reference_level_get()).strip()
IQ_IP_INTERFERE = str(conf.interiq_ip_get()).strip()
IQ_PORT_INTERFERE = str(conf.interiq_port_get()).strip()
IQ_ROUT_INTERFERE = str(conf.interiq_rout_get()).strip()

# MIMO
MIMO = str(conf.mimo_get()).strip()
IQ_IP_MASTER = str(conf.masteriq_ip_get()).strip()
IQ_PORT_MASTER = str(conf.masteriq_port_get()).strip()
IQ_ROUT_MASTER = str(conf.masteriq_rout_get()).strip()
IQ_IP_SLAVE1 = str(conf.slave1iq_ip_get()).strip()
IQ_PORT_SLAVE1 = str(conf.slave1iq_port_get()).strip()
IQ_ROUT_SLAVE1 = str(conf.slave1iq_rout_get()).strip()
IQ_IP_SLAVE2 = str(conf.slave2iq_ip_get()).strip()
IQ_PORT_SLAVE2 = str(conf.slave2iq_port_get()).strip()
IQ_ROUT_SLAVE2 = str(conf.slave2iq_rout_get()).strip()
IQ_IP_SLAVE3 = str(conf.slave3iq_ip_get()).strip()
IQ_PORT_SLAVE3 = str(conf.slave3iq_port_get()).strip()
IQ_ROUT_SLAVE3 = str(conf.slave3iq_rout_get()).strip()

# PATHLOSS
PATHLOSS_WANGTED = str(conf.pathloss_wanted_get()).strip()
PATHLOSS_INTERFERE = str(conf.pathloss_interfere_get())

# DUT
DUT_IP = str(conf.DUT_ip_get()).strip()
DUT_COM = str(conf.DUT_com_get()).strip()
DUT_BAUDRATE = str(conf.DUT_baudrate_get()).strip()
DUT_USERNAME = str(conf.DUT_username_get()).strip()
DUT_PASSWORD = str(conf.DUT_password_get()).strip()
ID_2G = str(conf.DUT_id2g_get()).strip()
ID_5G_LOW = str(conf.DUT_id5gl_get()).strip()
ID_5G_HIGH = str(conf.DUT_id5gh_get()).strip()
VAP_2G = str(conf.DUT_vap2g_get()).strip()
VAP_5G = str(conf.DUT_vap5g_get()).strip()
EXT1 = str(conf.DUT_ext1_get()).strip()
EXT2 = str(conf.DUT_ext2_get()).strip()
EXT3 = str(conf.DUT_ext3_get()).strip()

# LOG
LOG_ENABLE = str(conf.log_get()).strip()

# CALIBRATION
CALI_2G = str(conf.calibration_2g_get()).strip()
CALI_5G = str(conf.calibration_5g_get()).strip()

# TEST
AUTO_ADJUST_POWER = str(conf.auto_adjustpower_get()).strip()
accuracy_limit_left = str(conf.accuracylimit_left_get()).strip()
accuracy_limit_right = str(conf.accuracylimit_right_get()).strip()
RX_PACKETS = str(conf.RX_packets_get()).strip()
RX_DYNAMIC = str(conf.rx_dynamic_get()).strip()
