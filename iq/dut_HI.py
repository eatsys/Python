# -*- coding: utf-8 -*-
# @Time    : 2019/1/18 13:23
# @Author  : Ethan
# @FileName: tx_test.py
"""add 5g and RX """

from __future__ import division
from colorama import init, Fore, Style
from parameters import ID_2G, ID_5G_LOW, ID_5G_HIGH, LOG_ENABLE, RX_PACKETS, CALI_2G, CALI_5G
import telnetlib
import time
import re
import logging
logger = logging.getLogger()


class DUT:
    def __init__(self):
        self.tn = telnetlib.Telnet()
        self.tn.set_debuglevel(LOG_ENABLE)

    def close(self):
        if self.tn is not None:
            self.tn.close()
            self.tn = None

    def login(self, host, username, password):
        self.tn.open(host, port=23)
        time.sleep(1)
        command_result = self.tn.read_very_eager().decode('ascii')
        logger.debug(command_result)
        self.tn.read_until(b'Login: ', timeout=1)
        self.tn.write(username.encode('ascii') + b'\n')
        self.tn.read_until(b'Password:', timeout=1)
        self.tn.write(password.encode('ascii') + b'\n')

        time.sleep(1)
        command_result = self.tn.read_very_eager().decode('ascii')
        logger.debug(command_result)
        if 'wrong' not in command_result:
            logging.info('%s Sign up' % host)
            return True
        else:
            logging.warning('%s Login Fail' % host)
            return False

    def init(self, str1, str2, str3):
        self.tn.read_until(b'WAP>', timeout=1)
        self.tn.write(str1.encode('ascii') + b'\n')

        self.tn.read_until(b'SU_WAP>', timeout=1)
        self.tn.write(str2.encode('ascii') + b'\n')

        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(str3.encode('ascii') + b'\n')

        # command_result = self.tn.read_very_eager().decode('ascii')
        # logging.info('\n%s' % command_result)

    def ex_command(self, command):
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(command.encode('ascii') + b'\n')
        time.sleep(2)
        command_result = self.tn.read_very_eager().decode('ascii')
        logging.info('\n%s' % command_result)

    def reset_cali(self):
        if CALI_2G == '1':
            self.tn.write(b'wifi calibrate test parameter write wifichip 1 type power len 77 value default\r\n')
        elif CALI_5G == '1':
            self.tn.write(b'wifi calibrate test parameter write wifichip 2 type power len 155 value default\r\n')

    def reset_upc(self):
        if CALI_2G == '1':
            self.tn.write(b'wifi calibrate test parameter write wifichip 1 type upc len 12 value default\r\n')
        elif CALI_5G == '1':
            self.tn.write(b'wifi calibrate test parameter write wifichip 2 type upc len 28 value default\r\n')

    def init_cali(self):
        if CALI_2G == '1':
            self.tn.write(b'wifi_equipment.sh init chip 1\r\n')
            # self.tn.write(b'killall hostapd\r\n')
        elif CALI_5G == '1':
            self.tn.write(b'wifi_equipment.sh init chip 2\r\n')

    def init_ppm(self):
        """
        output a tx signal for ppm cali
        :return:
        """
        if int(channel) < 5000:
            band = ID_2G
        elif int(channel) < 5500:
            band = ID_5G_LOW
        else:
            band = ID_5G_HIGH
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv Hisilicon%s adjust_ppm 0\r\n' % band.encode('ascii'))

    def adjust_ppm(self, ppm):
        """
        adjust ppm to 0
        :param ppm:
        :return:
        """
        if int(channel) < 5000:
            band = ID_2G
        elif int(channel) < 5500:
            band = ID_5G_LOW
        else:
            band = ID_5G_HIGH
        self.tn.write(b'shell iwpriv Hisilicon%s adjust_ppm %s\r\n' % (band.encode('ascii'), str(ppm).encode('ascii')))

    def write_ppm(self, ppm):
        """
        write ppm to flash
        :param ppm:
        :return:
        """
        self.tn.write(b'wifi calibrate test parameter write wifichip %s type freqoffset len 4 value %s\r\n'
                      % (band.encode('ascii'), ppm.encode('ascii')))

    def get_pwr_para(self):
        self.tn.write(b'wifi_equipment.sh get_txpower chip %s para 3\r\n' % band.encode('ascii'))
        command_result = self.tn.read_until('ss')
        para_list = command_result
        return para_list

    def cali_pwr(self, cali_channel, chain):
        """
        send a tx signal for cali
        :param cali_channel:
        :param chain:
        :return:
        """
        if int(cali_channel) < 5000:
            vap = VAP_2G
            cali_mode = '11g'
        else:
            vap = VAP_5G
            cali_mode = '11a'
        if chain == '0':
            chains = '01'
        else:
            chains = '10'
        self.tn.write(b'iwpriv vap%s txpower 300\r\n' % vap.encode('ascii'))
        self.tn.write(b'iwpriv vap%s mode %s\r\n' % cali_mode.encode('ascii'))
        self.tn.write(b'iwpriv vap%s bw 20\r\n')
        self.tn.write(b'iwpriv vap%s freq %s\r\n' % cali_channel.encode('ascii'))
        self.tn.write(b'iwpriv vap%s rate 6\r\n')
        self.tn.write(b'iwpriv vap%s txch 00%s\r\n' % chains.encode('ascii'))
        logger.debug(f'vap{vap} mode{cali_mode} 20 {cali_channel} 6 00{chains}')

    def adjust_pwr(self, adjust_power):
        """
        adjust the cali signal power, 200,160,120
        :param adjust_power:
        :return:
        """
        if int(channel) < 5000:
            vap = VAP_2G
        else:
            vap = VAP_5G
        self.tn.write(b'iwpriv vap%s txpower %s\r\n' % (vap.encode('ascii'), str(adjust_power).encode('ascii')))
        logger.debug(f'iwpriv vap{vap} txpower {adjust_power}')

    def cali_pwr_write(self, adjust_power_list):
        """
        write the test power to cali power
        :param adjust_power_list:
        :return:
        """
        if band == '1':
            hi_id = '0'
        else:
            hi_id = '1'
        if cali_channel < 5:
            subband = '0'
        elif cali_channel == 8 or cali_channel == 40:
            subband = '1'
        elif cali_channel == 12 or cali_channel == 56:
            subband = '2'
        elif cali_channel == 104:
            subband = '3'
        elif cali_channel == 120:
            subband = '4'
        elif cali_channel == 136:
            subband = '5'
        elif cali_channel == 157:
            subband = '6'
        else:
            subband = '0'
        self.tn.write(b'iwpriv Hisilicon%s cali_power "%s %s %s %s %s"\r\n' %
                      (hi_id.encode('ascii'), str(cali_chain).encode('ascii'), subband.encode('ascii'),
                       str(adjust_power_list[0]).encode('ascii'), str(adjust_power_list[1]).encode('ascii'),
                       str(adjust_power_list[2]).encode('ascii')) + b'\r\n')
        logger.debug(f'shell iwpriv Hisilicon{hi_id} cali_power "{cali_chain} {subband} {adjust_power_list[0]} '
                     f'{adjust_power_list[1]} {adjust_power_list[2]}"')

    def cali_para_write(self):
        """
        get the cali param and write to flash
        :return:
        """
        if int(channel) < 5000:
            vap = VAP_2G
        else:
            vap = VAP_5G
        self.tn.write(b'\r\n')
        self.tn.write(b'iwpriv vap%s get_power_param\r\n' % vap.encode('ascii') + b'\r\n')
        logger.debug(f'iwpriv vap{vap} get_power_param')
        self.tn.write(b'ls\r\n')
        command_result = self.tn.read_until(b'Enabled')
        logger.debug(command_result)
        pwrcali_para = re.findall(b'get_power_param:\r+\n+(.+)\r+', command_result)[0].decode('utf-8')
        logger.debug(command_result)
        self.tn.write(b'wifi calibrate test parameter write wifichip %s type power len %s value %s\r\n' %
                      (band.encode('ascii'), radio_adress.encode('ascii'), pwrcali_para.encode('ascii')) + b'\r\n')
        logger.debug(f'wifi calibrate test parameter write wifichip {band} type power len {radio_adress} value {pwrcali_para}')
        command_result = self.tn.read_all()
        for result in command_result:
            logger.debug(result.strip().decode('utf-8'))
        self.tn.write(b'wifi calibrate test parameter read wifichip %s type power len %s\r\n' %
                      (band.encode('ascii'), radio_adress.encode('ascii')) + b'\r\n')
        logger.debug((f'wifi calibrate test parameter read wifichip %s type power len {radio_adress}'))
        pwrcali_result = self.tn.read_until(b'success!')
        logger.debug(pwrcali_result)

    def upc_write(self):
        if int(channel) < 5000:
            vap = VAP_2G
        else:
            vap = VAP_5G
        self.tn.write(b'\r\n')
        self.tn.write(b'iwpriv vap%s get_upc_param\r\n' % vap.encode('ascii') + b'\r\n')
        logger.debug(f'iwpriv vap{vap} get_power_param')
        self.tn.write(b'ls\r\n')
        command_result = self.tn.read_until(b'Enabled')
        logger.debug(command_result)
        pwrcali_para = re.findall(b'get_upc_param:\r+\n+(.+)\r+', command_result)[0].decode('utf-8')
        logger.debug(command_result)
        self.tn.write(b'wifi calibrate test parameter write wifichip %s type upc len %s value %s\r\n' %
                      (band.encode('ascii'), upc_lenth.encode('ascii'), pwrcali_para.encode('ascii')) + b'\r\n')
        logger.debug(f'wifi calibrate test parameter write wifichip {band} type power len {upc_lenth} value {pwrcali_para}')
        command_result = self.tn.read_all()
        for result in command_result:
            logger.debug(result.strip().decode('utf-8'))

    def crc(self):
        """
        crc cali
        :return:
        """
        self.tn.write(b'wifi calibrate parameter crc calc\r\n')
        self.tn.write(b'wifi calibrate parameter crc check\r\n')
        command_result = self.tn.readlines()
        for result in command_result:
            logger.debug(result.strip().decode('utf-8'))

    def tx(self):
        if int(channel) < 5000:
            band = ID_2G
        elif int(channel) < 5500:
            band = ID_5G_LOW
        else:
            band = ID_5G_HIGH
        # for 2.4g
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'\r\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap%s al_tx 0' % band.encode('ascii') + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'ifconfig vap%s down' % band.encode('ascii') + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap%s setessid Hi' % band.encode('ascii') + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap%s mode %s' % (band.encode('ascii'), mode.encode('ascii')) + b'\n')
        # logger(channel)
        if bw == '40':
            channels = int(channel) - 10
        elif bw == '80':
            channels = int(channel) - 30
        else:
            channels = channel
        if int(channel) < 5000:
            channels = '{:.0f}'.format((int(channels) - 2407) / 5)  # 2407+5*1=2412
        else:
            channels = '{:.0f}'.format((int(channels) - 5000) / 5)  # 5000+5*36=5180
        channels = str(channels)
        # logger(channel)
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap%s channel %s' % (band.encode('ascii'), channels.encode('ascii')) + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap%s privflag 1' % band.encode('ascii') + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap%s al_rx 0' % band.encode('ascii') + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'hipriv.sh "vap%s 2040bss_enable 0"' % band.encode('ascii') + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'hipriv.sh "vap%s radartool enable 0"' % band.encode('ascii') + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'hipriv.sh "vap%s acs sw 0"' % band.encode('ascii') + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'ifconfig vap%s up' % band.encode('ascii') + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap%s al_tx 0' % band.encode('ascii') + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'hipriv.sh "vap%s add_user 07:06:05:04:03:02 1"\n' % band.encode('ascii'))
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap%s bw %s' % (band.encode('ascii'), bw.encode('ascii')) + b'\n')
        if mode == '11b' or mode == '11g':
            rates = 'rate'
        elif mode == '11n':
            rates = 'mcs'
        elif mode == '11ac':
            rates = 'mcsac'
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(
            b'iwpriv vap%s %s %s' % (band.encode('ascii'), rates.encode('ascii'), rate.encode('ascii')) + b'\n')
        if chain == '0':
            chains = '01'
        else:
            chains = '10'
        # logger('chain set',chain,type(chain),chains)
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap%s txch 00%s' % (band.encode('ascii'), chains.encode('ascii')) + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap%s al_tx "1 2 1000"' % band.encode('ascii') + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'hipriv.sh "vap%s set_tx_pow rf_reg_ctl 0"' % band.encode('ascii') + b'\n')
        logger('TX COMMANDS DONE')

    def tx_off(self):
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap%s al_tx 0' % band.encode('ascii') + b'\n')

    def get_paras(self):
        if int(channel) < 5000:
            band = ID_2G
        elif int(channel) < 5500:
            band = ID_5G_LOW
        else:
            band = ID_5G_HIGH
        if int(channel) < 2437 and chain == '0':
            channel_groups = '098'
        elif int(channel) < 2437 and chain == '1':
            channel_groups = '0a8'
        elif 2437 < int(channel) < 2462 and chain == '0':
            channel_groups = '094'
        elif 2437 < int(channel) < 2462 and chain == '1':
            channel_groups = '0a4'
        elif int(channel) >= 2462 and chain == '0':
            channel_groups = '090'
        elif int(channel) >= 2462 and chain == '1':
            channel_groups = '0a0'
        elif 5100 < int(channel) <= 5240 and chain == '0':
            channel_groups = '0c4'
        elif 5100 < int(channel) <= 5240 and chain == '1':
            channel_groups = '0f0'
        elif 5260 <= int(channel) <= 5320 and chain == '0':
            channel_groups = '0c8'
        elif 5260 <= int(channel) <= 5320 and chain == '1':
            channel_groups = '0f4'
        elif 5500 <= int(channel) <= 5560 and chain == '0':
            channel_groups = '0cc'
        elif 5500 <= int(channel) <= 5560 and chain == '1':
            channel_groups = '0f8'
        elif 5580 <= int(channel) <= 5620 and chain == '0':
            channel_groups = '0d0'
        elif 5580 <= int(channel) <= 5620 and chain == '1':
            channel_groups = '0fc'
        elif 5640 <= int(channel) <= 5720 and chain == '0':
            channel_groups = '0d4'
        elif 5640 <= int(channel) <= 5720 and chain == '1':
            channel_groups = '100'
        elif 5745 <= int(channel) <= 5825 and chain == '0':
            channel_groups = '0d8'
        elif 5745 <= int(channel) <= 5825 and chain == '1':
            channel_groups = '104'
        logger.info(channel_groups)
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'hipriv.sh "vap%s set_tx_pow rf_reg_ctl 1"' % band.encode('ascii') + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'hipriv.sh "vap%s reginfo soc 0x20038%s 0x20038%s";dmesg -c'
                      % (band.encode('ascii'), channel_groups.encode('ascii'), channel_groups.encode('ascii')) + b'\n')
        command_result = self.tn.read_until(b'value=0x\w+\r\r\nWAP(Dopra Linux) # ', timeout=2)
        command_result = re.search(b'value=0x\w+', command_result)
        default_value = re.sub('value=0x', '', command_result.group().decode('ascii'))
        logger('Default Value(HEX):', default_value)
        default_value = int(default_value, 16)
        return default_value

    def adjust_power(self):
        if int(channel) < 5000:
            band = ID_2G
        elif int(channel) < 5500:
            band = ID_5G_LOW
        else:
            band = ID_5G_HIGH
            # power para
        if int(channel) < 2437 and chain == '0':
            channel_groups = '098'
        elif int(channel) < 2437 and chain == '1':
            channel_groups = '0a8'
        elif 2437 < int(channel) < 2462 and chain == '0':
            channel_groups = '094'
        elif 2437 < int(channel) < 2462 and chain == '1':
            channel_groups = '0a4'
        elif int(channel) >= 2462 and chain == '0':
            channel_groups = '090'
        elif int(channel) >= 2462 and chain == '1':
            channel_groups = '0a0'
        elif 5100 < int(channel) <= 5240 and chain == '0':
            channel_groups = '0c4'
        elif 5100 < int(channel) <= 5240 and chain == '1':
            channel_groups = '0f0'
        elif 5260 <= int(channel) <= 5320 and chain == '0':
            channel_groups = '0c8'
        elif 5260 <= int(channel) <= 5320 and chain == '1':
            channel_groups = '0f4'
        elif 5500 <= int(channel) <= 5560 and chain == '0':
            channel_groups = '0cc'
        elif 5500 <= int(channel) <= 5560 and chain == '1':
            channel_groups = '0f8'
        elif 5580 <= int(channel) <= 5620 and chain == '0':
            channel_groups = '0d0'
        elif 5580 <= int(channel) <= 5620 and chain == '1':
            channel_groups = '0fc'
        elif 5640 <= int(channel) <= 5720 and chain == '0':
            channel_groups = '0d4'
        elif 5640 <= int(channel) <= 5720 and chain == '1':
            channel_groups = '100'
        elif 5745 <= int(channel) <= 5825 and chain == '0':
            channel_groups = '0d8'
        elif 5745 <= int(channel) <= 5825 and chain == '1':
            channel_groups = '104'
        logger.info(channel_groups)
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'hipriv.sh "vap%s regwrite soc 0x20038%s 0x%s"\r\n'
                      % (band.encode('ascii'), channel_groups.encode('ascii'), pwr_paras.encode('ascii')))
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'hipriv.sh "vap%s reginfo soc 0x20038%s 0x20038%s";dmesg -c\r\n'
                      % (band.encode('ascii'), channel_groups.encode('ascii'), channel_groups.encode('ascii')))
        command_result = self.tn.read_until(b'value=0x\w+\r\r\nWAP(Dopra Linux) # ', timeout=1)
        command_result = re.search(b'value=0x\w+', command_result)
        default_value = re.sub('value=0x', '', command_result.group().decode('ascii'))
        logger('Check Value(HEX):', default_value)
        gain = default_value
        return gain

    def set_default(self):
        if int(channel) < 5000:
            band = ID_2G
            self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
            self.tn.write(b'exit' + b'\n')
            self.tn.read_until(b'SU_WAP>', timeout=1)
            self.tn.write(b'wifi calibrate test parameter write wifichip 1 type power len 77 value default\r\n')
            time.sleep(2)
            self.tn.read_until(b'SU_WAP>', timeout=1)
            self.tn.write(b'shell' + b'\n')
            self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
            self.tn.write(b'wifi_equipment.sh init chip 1' + b'\n')
            time.sleep(2)
            self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
            self.tn.write(
                b'hipriv.sh "vap%s set_tx_pow rf_reg_ctl 0"' % (band.encode('ascii'), band.encode('ascii')) + b'\n')
        elif int(channel) < 5500:
            band = ID_5G_LOW
            self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
            self.tn.write(b'exit' + b'\n')
            self.tn.read_until(b'SU_WAP>', timeout=1)
            self.tn.write(b'wifi calibrate test parameter write wifichip 2 type power len 155 value default\r\n')
            time.sleep(2)
            self.tn.read_until(b'SU_WAP>', timeout=1)
            self.tn.write(b'shell' + b'\n')
            self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
            self.tn.write(b'wifi_equipment.sh init chip 2' + b'\n')
            time.sleep(2)
            self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
            self.tn.write(
                b'hipriv.sh "vap%s set_tx_pow rf_reg_ctl 0"' % (band.encode('ascii'), band.encode('ascii')) + b'\n')
        else:
            band = ID_5G_HIGH
            self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
            self.tn.write(b'exit' + b'\n')
            self.tn.read_until(b'SU_WAP>', timeout=1)
            self.tn.write(b'wifi calibrate test parameter write wifichip 2 type power len 155 value default\r\n')
            time.sleep(2)
            self.tn.read_until(b'SU_WAP>', timeout=1)
            self.tn.write(b'shell' + b'\n')
            self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
            self.tn.write(b'wifi_equipment.sh init chip 2' + b'\n')
            time.sleep(2)
            self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
            self.tn.write(
                b'hipriv.sh "vap%s set_tx_pow rf_reg_ctl 0"' % (band.encode('ascii'), band.encode('ascii')) + b'\n')

    def rx(self):
        if int(channel) < 5000:
            band = ID_2G
        elif int(channel) < 5500:
            band = ID_5G_LOW
        else:
            band = ID_5G_HIGH
        # for 2.4g
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'hipriv.sh "vap%s rx_fcs_info 1 2";dmesg -c' % band.encode('ascii') + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'\r\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap%s al_tx 0' % band.encode('ascii') + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap%s al_rx 0' % band.encode('ascii') + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'ifconfig vap%s down' % band.encode('ascii') + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'ifconfig vap%s hw ether 00:E0:52:22:22:14' % band.encode('ascii') + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap%s al_rx 1' % band.encode('ascii') + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap%s setessid Hi' % band.encode('ascii') + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap%s mode %s' % (band.encode('ascii'), mode.encode('ascii')) + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap%s bw %s' % (band.encode('ascii'), bw.encode('ascii')) + b'\n')
        if int(channel) < 5000:
            channels = '{:.0f}'.format((int(channel) - 2407) / 5)
        else:
            channels = '{:.0f}'.format((int(channel) - 5000) / 5)
        channels = str(channels)
        # logger(channel)
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap%s channel %s' % (band.encode('ascii'), channels.encode('ascii')) + b'\n')
        if chain == '0':
            chains = '01'
        else:
            chains = '10'
        # logger('chain set',chain,type(chain),chains)
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap%s rxch 00%s' % (band.encode('ascii'), chains.encode('ascii')) + b'\n')
        if mode == '11b' or mode == '11g':
            rates = 'rate'
        elif mode == '11n':
            rates = 'mcs'
        elif mode == '11ac':
            rates = 'mcsac'
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap%s %s %s' % (band.encode('ascii'), rates.encode('ascii'), rate.encode('ascii')) + b'\n')
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'ifconfig vap%s up' % band.encode('ascii') + b'\n')
        logger('RX COMMANDS DONE')

    def rx_off(self):
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'iwpriv vap%s al_rx 0' % band.encode('ascii') + b'\n')

    def get_statistics(self):
        if int(channel) < 5000:
            band = ID_2G
        elif int(channel) < 5500:
            band = ID_5G_LOW
        else:
            band = ID_5G_HIGH
        self.tn.read_until(b'WAP(Dopra Linux) # ', timeout=1)
        self.tn.write(b'hipriv.sh "vap%s rx_fcs_info 1 2";dmesg -c' % band.encode('ascii') + b'\n')
        command_result = self.tn.read_until(b'rssi', timeout=2)
        logger(command_result)
        command_result = re.search(b'succ:\w+', command_result)
        logger(command_result)
        logger(command_result.group())
        PER_value = re.sub('succ:', '', command_result.group().decode('ascii'))
        logger('Packets:', RX_PACKETS, 'PER:', PER_value)
        return PER_value


if __name__ == '__main__':
    init(autoreset=True)    
    dt.close()
