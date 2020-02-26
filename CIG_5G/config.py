#!/user/bin/env python
# encoding: utf-8
# @time      : 2019/11/14 15:09

__author__ = 'Ethan'

import configparser
import logging

logger = logging.getLogger()

config_file = "./config.ini"


class Config:
    def __init__(self):
        self.conf = configparser.ConfigParser()
        self.conf.read(config_file)

    def SA_ip_get(self):
        sa_ip = self.conf.get("SA_SETUP", "SA_IP")
        logger.info(f'SA IP:{sa_ip}')
        return sa_ip

    def SGWANGTED_ip_get(self):
        sgw_ip = self.conf.get("SG_SETUP", "SG_WANTED_IP")
        logger.info(f'IQ IP:{sgw_ip}')
        return sgw_ip

    def SGJAMMER1_ip_get(self):
        sgj1_ip = self.conf.get("IQ_SETUP", "SG_JAMMER1_IP")
        logger.info(f'IQ IP:{sgj1_ip}')
        return sgj1_ip

    def SGJAMMER2_ip_get(self):
        sgj2_ip = self.conf.get("IQ_SETUP", "SG_JAMMER2_IP")
        logger.info(f'IQ IP:{sgj2_ip}')
        return sgj2_ip

    # PATHLOSS
    def pathloss_sa_get(self):
        pathloss_sa = self.conf.get("PATHLOSS_SETUP", "SA")
        logger.info(f'DUT_IP:{pathloss_sa}')
        return pathloss_sa

    def pathloss_sgwanted_get(self):
        pathloss_sgwanted = self.conf.get("PATHLOSS_SETUP", "SG_WANTED")
        logger.info(f'DUT_IP:{pathloss_sgwanted}')
        return pathloss_sgwanted

    def pathloss_sgjammer_get(self):
        pathloss_sgjammer = self.conf.get("PATHLOSS_SETUP", "SG_JAMMER")
        logger.info(f'DUT_IP:{pathloss_sgjammer}')
        return pathloss_sgjammer

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
        log_enable = self.conf.get("LOG_SETUP", "LOG_PRINT")
        logger.info(f'LOG_PRINT:{log_enable}')
        return log_enable

    # CALIBRATION
    def calibration_get(self):
        cali = self.conf.get("CALIBRATION_SETUP", "Calibration")
        logger.info(f'Calibration 2G:{cali}')
        return cali

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


conf = Config()

if __name__ == "__main__":
    get = Config()
    ip = get.SA_ip_get()
    print(ip)
