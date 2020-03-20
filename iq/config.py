#!/user/bin/env python
# encoding: utf-8
#@time      : 2019/11/14 15:09

__author__ = 'Ethan'

import configparser
import logging
logger = logging.getLogger()

config_file = "./config.ini"


class Config:
    def __init__(self):
        self.conf = configparser.ConfigParser()
        self.conf.read(config_file)

    # IQ
    def IQ_ip_get(self):
        iq_ip = self.conf.get("IQ_SETUP", "IQ_IP")
        logger.info(f'IQ IP:{iq_ip}')
        return iq_ip

    def IQ_port_get(self):
        iq_port = self.conf.get("IQ_SETUP", "IQ_PORT")
        logger.info(f'IQ PORT:{iq_port}')
        return iq_port

    def IQ_rout_get(self):
        iq_rout = self.conf.get("IQ_SETUP", "IQ_ROUT")
        logger.info(f'IQ ROUT:{iq_rout}')
        return iq_rout

    def evm_11ag_get(self):
        evm_ag = self.conf.get("IQ_SETUP", "11a/g_Channel_Estimation")
        logger.info(f'11a/g_Channel_Estimation:{evm_ag}')
        return evm_ag

    def evm_11n_get(self):
        evm_n = self.conf.get("IQ_SETUP", "11n_Channel_Estimation")
        logger.info(f'11n_Channel_Estimation:{evm_n}')
        return evm_n

    def evm_11ac_get(self):
        evm_ac = self.conf.get("IQ_SETUP", "11ac_Channel_Estimation")
        logger.info(f'11ac_Channel_Estimation:{evm_ac}')
        return evm_ac

    def evm_11ax_get(self):
        evm_ax = self.conf.get("IQ_SETUP", "11ax_Channel_Estimation")
        logger.info(f'11ax_Channel_Estimation:{evm_ax}')
        return evm_ax

    def Reference_level_get(self):
        rl = self.conf.get("IQ_SETUP", "Auto Reference Level")
        logger.info(f'Auto Reference Level:{rl}')
        return rl

    def interiq_ip_get(self):
        interiq_ip = self.conf.get("IQ_SETUP", "INTERFERE_IQ_IP")
        logger.info(f'IQ IP:{interiq_ip}')
        return interiq_ip

    def interiq_port_get(self):
        interiq_port = self.conf.get("IQ_SETUP", "INTERFERE_IQ_PORT")
        logger.info(f'IQ IP:{interiq_port}')
        return interiq_port

    def interiq_rout_get(self):
        interiq_rout = self.conf.get("IQ_SETUP", "INTERFERE_IQ_ROUT")
        logger.info(f'IQ IP:{interiq_rout}')
        return interiq_rout

    # MIMO
    def mimo_get(self):
        mimo = self.conf.get("IQ_SETUP_MIMO", "MIMO")
        logger.info(f'IQ IP:{mimo}')
        return mimo

    def masteriq_ip_get(self):
        masteriq_ip = self.conf.get("IQ_SETUP_MIMO", "MASTER_IQ_IP")
        logger.info(f'IQ IP:{masteriq_ip}')
        return masteriq_ip

    def masteriq_port_get(self):
        masteriq_port = self.conf.get("IQ_SETUP_MIMO", "MASTER_IQ_PORT")
        logger.info(f'IQ IP:{masteriq_port}')
        return masteriq_port

    def masteriq_rout_get(self):
        masteriq_rout = self.conf.get("IQ_SETUP_MIMO", "MASTER_IQ_ROUT")
        logger.info(f'IQ IP:{masteriq_rout}')
        return masteriq_rout

    def slave1iq_ip_get(self):
        slave1iq_ip = self.conf.get("IQ_SETUP_MIMO", "SLAVE1_IQ_IP")
        logger.info(f'IQ IP:{slave1iq_ip}')
        return slave1iq_ip

    def slave1iq_port_get(self):
        slave1iq_port = self.conf.get("IQ_SETUP_MIMO", "SLAVE1_IQ_PORT")
        logger.info(f'IQ IP:{slave1iq_port}')
        return slave1iq_port

    def slave1iq_rout_get(self):
        slave1iq_rout = self.conf.get("IQ_SETUP_MIMO", "SLAVE1_IQ_ROUT")
        logger.info(f'IQ IP:{slave1iq_rout}')
        return slave1iq_rout

    def slave2iq_ip_get(self):
        slave2iq_ip = self.conf.get("IQ_SETUP_MIMO", "SLAVE2_IQ_IP")
        logger.info(f'IQ IP:{slave2iq_ip}')
        return slave2iq_ip

    def slave2iq_port_get(self):
        slave2iq_port = self.conf.get("IQ_SETUP_MIMO", "SLAVE2_IQ_PORT")
        logger.info(f'IQ IP:{slave2iq_port}')
        return slave2iq_port

    def slave2iq_rout_get(self):
        slave2iq_rout = self.conf.get("IQ_SETUP_MIMO", "SLAVE2_IQ_ROUT")
        logger.info(f'IQ IP:{slave2iq_rout}')
        return slave2iq_rout

    def slave3iq_ip_get(self):
        slave3iq_ip = self.conf.get("IQ_SETUP_MIMO", "SLAVE3_IQ_IP")
        logger.info(f'IQ IP:{slave3iq_ip}')
        return slave3iq_ip

    def slave3iq_port_get(self):
        slave3iq_port = self.conf.get("IQ_SETUP_MIMO", "SLAVE3_IQ_PORT")
        logger.info(f'IQ IP:{slave3iq_port}')
        return slave3iq_port

    def slave3iq_rout_get(self):
        slave3iq_rout = self.conf.get("IQ_SETUP_MIMO", "SLAVE3_IQ_ROUT")
        logger.info(f'IQ IP:{slave3iq_rout}')
        return slave3iq_rout

    # PATHLOSS
    def pathloss_wanted_get(self):
        pathloss_wanted = self.conf.get("PATHLOSS_SETUP", "IQ_WANTED")
        logger.info(f'DUT_IP:{pathloss_wanted}')
        return pathloss_wanted

    def pathloss_interfere_get(self):
        pathloss_interfere = self.conf.get("PATHLOSS_SETUP", "IQ_INTERFERE")
        logger.info(f'DUT_IP:{pathloss_interfere}')
        return pathloss_interfere

    # DUT
    def DUT_ip_get(self):
        dut_ip = self.conf.get("DUT_SETUP", "DUT_IP")
        logger.info(f'DUT_IP:{dut_ip}')
        return dut_ip

    def DUT_com_get(self):
        dut_com = self.conf.get("DUT_SETUP", "DUT_COM")
        logger.info(f'DUT_COM:{dut_com}')
        return dut_com

    def DUT_baudrate_get(self):
        dut_baudrate = self.conf.get("DUT_SETUP", "DUT_BAUDRATE")
        logger.info(f'DUT_BAUDRATE:{dut_baudrate}')
        return dut_baudrate

    def DUT_username_get(self):
        dut_username = self.conf.get("DUT_SETUP", "DUT_Username")
        logger.info(f'DUT_Username:{dut_username}')
        return dut_username

    def DUT_password_get(self):
        dut_password = self.conf.get("DUT_SETUP", "DUT_Password")
        logger.info(f'DUT_Password:{dut_password}')
        return dut_password

    def DUT_id2g_get(self):
        dut_id2g = self.conf.get("DUT_SETUP", "2G_ID")
        logger.info(f'2G_ID:{dut_id2g}')
        return dut_id2g

    def DUT_id5gl_get(self):
        dut_id5gl = self.conf.get("DUT_SETUP", "5G_Low_ID")
        logger.info(f'5G_Low_ID:{dut_id5gl}')
        return dut_id5gl

    def DUT_id5gh_get(self):
        dut_id5gh = self.conf.get("DUT_SETUP", "5G_High_ID")
        logger.info(f'5G_High_ID:{dut_id5gh}')
        return dut_id5gh

    def DUT_vap2g_get(self):
        vap_2g = self.conf.get("DUT_SETUP", "2G_vap_value")
        logger.info(f'5G_High_ID:{vap_2g}')
        return vap_2g

    def DUT_vap5g_get(self):
        vap_5g = self.conf.get("DUT_SETUP", "5G_vap_value")
        logger.info(f'5G_High_ID:{vap_5g}')
        return vap_5g

    def DUT_ext1_get(self):
        ext1 = self.conf.get("DUT_SETUP", "EXT1")
        logger.info(f'5G_High_ID:{ext1}')
        return ext1

    def DUT_ext2_get(self):
        ext2 = self.conf.get("DUT_SETUP", "EXT2")
        logger.info(f'5G_High_ID:{ext2}')
        return ext2

    def DUT_ext3_get(self):
        ext3 = self.conf.get("DUT_SETUP", "EXT3")
        logger.info(f'5G_High_ID:{ext3}')
        return ext3

    # LOG
    def log_get(self):
        log_enable = self.conf.get("LOG_SETUP", "DEBUG_LOG")
        logger.info(f'Debug_Log:{log_enable}')
        return log_enable

    # CALIBRATION
    def calibration_2g_get(self):
        cali_2g = self.conf.get("CALIBRATION_SETUP", "Calibration_2G")
        logger.info(f'Calibration 2G:{cali_2g}')
        return cali_2g

    def calibration_5g_get(self):
        cali_5g = self.conf.get("CALIBRATION_SETUP", "Calibration_5G")
        logger.info(f'Calibration 2G:{cali_5g}')
        return cali_5g

    # TEST
    def auto_adjustpower_get(self):
        ad_pwr = self.conf.get("TEST_SETUP", "AUTO Adjust Power")
        logger.info(f'AUTO Adjust Power:{ad_pwr}')
        return ad_pwr

    def accuracylimit_left_get(self):
        accuracy_limit_left = self.conf.get("TEST_SETUP", "accuracy_limit_left")
        logger.info(f'accuracy_limit_left:{accuracy_limit_left}')
        return accuracy_limit_left

    def accuracylimit_right_get(self):
        accuracy_limit_right = self.conf.get("TEST_SETUP", "accuracy_limit_right")
        logger.info(f'accuracy_limit_right:{accuracy_limit_right}')
        return accuracy_limit_right

    def RX_packets_get(self):
        rx_packets = self.conf.get("TEST_SETUP", "RX_Packets")
        logger.info(f'RX Packets:{rx_packets}')
        return rx_packets

    def rx_dynamic_get(self):
        rx_dynamic = self.conf.get("TEST_SETUP", "RX Dynamic")
        logger.info(f'RX Dynamic:{rx_dynamic}')
        return rx_dynamic

    def sleep_time_get(self):
        sleep_time = self.conf.get("TEST_SETUP", "SLEEP TIME")
        logger.info(f'Sleep Time:{sleep_time}')
        return sleep_time


conf = Config()

if __name__ == "__main__":
    get = Config()
    ip = get.IQ_ip_get()
    print(ip)