# -*- coding: utf-8 -*-
# @Time    : 2019/1/18 13:23
# @Author  : Ethan
# @FileName: tx_test.py
"""add 5g and RX
   add calibration"""

from __future__ import division
from parameters import RX_PACKETS, ID_2G, ID_5G_LOW, ID_5G_HIGH
import serial
import time
import re
import logging
logger = logging.getLogger()


def __isset__(v: object) -> object:
    try:
        type(eval(v))
    except Exception as error:
        return 0
    else:
        return 1


class DUT():
    """
    for serial connect
    """

    def __init__(self, com, baudrate):
        """
        param, timeout must set if use readline() or readlines()
        :param com:
        :param baudrate:
        """
        self.com = com
        self.baudrate = baudrate
        self.sn = serial.Serial(self.com, self.baudrate)
        self.sn.timeout = 0.5

    def close(self):
        if self.sn is not None:
            self.sn.close()
            self.sn = None

    def login(self, username, password):
        """

        :param username:
        :param password:
        :return:
        """
        if username is not None:
            self.sn.read_until(b'Login: ')
            self.sn.write(username.encode('ascii') + b'\n')
        if password is not None:
            self.sn.read_until(b'Password:')
            self.sn.write(password.encode('ascii') + b'\n')

        time.sleep(1)
        command_result = self.sn.readlines()
        for result in command_result:
            logger.debug(result.strip().decode('utf-8'))
        if 'wrong' not in command_result:
            logging.info('%s Sign up' % username)
            return True
        else:
            logging.warning('%s Login Fail' % username)
            return False

    def init(self, str1, str2, str3, str4):
        """
        additional command if you need to excite
        :param str1:
        :param str2:
        :param str3:
        :return:
        """
        self.sn.write(b'\r\n')
        self.sn.write(str1.encode('ascii') + b'\r\n')
        self.sn.write(str2.encode('ascii') + b'\r\n')
        self.sn.write(str3.encode('ascii') + b'\r\n')
        self.sn.write(str4.encode('ascii') + b'\r\n')
        command_result = self.sn.readlines()
        for result in command_result:
            logger.debug(result.strip().decode('utf-8'))

    def init_cali(self):
        """
        init for calibration, cancel it and use init() or manual
        :return:
        """
        logger.info('Initialization for calibration...')
        self.sn.write(b'shell sh\r\n')
        time.sleep(1)
        self.sn.write(b'stty echo\r\n')
        time.sleep(1)
        self.sn.write(b'cd /mnt/caldata\r\n')
        time.sleep(1)
        self.sn.write(b'rm mtdblock0\r\n')
        time.sleep(1)
        self.sn.write(b'rm cfg_ont_hisi.ini\r\n')
        time.sleep(1)
        self.sn.write(b'exit\r\n')
        time.sleep(1)
        self.sn.write(b'wifi calibrate test parameter init\r\n')
        time.sleep(2)
        self.sn.write(b'shell WifiChipInit.sh \r\n')
        time.sleep(5)
        command_result = self.sn.readlines()
        for result in command_result:
            logger.debug(result.strip().decode('utf-8'))

    def init_ppm(self):
        """
        output a tx signal for ppm cali
        :return:
        """
        if band == '1':
            self.sn.write(b'shell iwpriv Hisilicon0 adjust_ppm 0\r\n')
            logger.debug('shell iwpriv Hisilicon0 adjust_ppm 0')
            self.sn.write(b'shell WifiTxInit.sh 1 11g 20 1 54 0001\r\n')
            logger.debug('shell WifiTxInit.sh 1 11g 20 1 54 0001')
            time.sleep(3)
        else:
            self.sn.write(b'shell iwpriv Hisilicon1 adjust_ppm 0\r\n')
            logger.debug('shell iwpriv Hisilicon1 adjust_ppm 0')
            self.sn.write(b'shell WifiTxInit.sh 2 11a 20 36 54 0001\r\n')
            logger.debug('shell WifiTxInit.sh 2 11a 20 36 54 0001')
            time.sleep(3)
        command_result = self.sn.readlines()
        for result in command_result:
            logger.debug(result.strip().decode('utf-8'))

    def adjust_ppm(self, ppm):
        """
        adjust ppm to 0
        :param ppm:
        :return:
        """
        if band == '1':
            hi_id = '0'
        else:
            hi_id = '1'
        self.sn.write(b'shell iwpriv Hisilicon%s adjust_ppm %s\r\n' % (hi_id.encode('ascii'), str(ppm).encode('ascii')))
        command_result = self.sn.readlines()
        for result in command_result:
            logger.debug(result.strip().decode('utf-8'))

    def write_ppm(self, ppm):
        """
        write ppm to flash
        :param ppm:
        :return:
        """
        self.sn.write(b'wifi calibrate test parameter write wifichip %s type freqoffset len 4 value %s\r\n'
                      % (band.encode('ascii'), ppm.encode('ascii')))
        command_result = self.sn.readlines()
        for result in command_result:
            logger.debug(result.strip().decode('utf-8'))

    def cali_pwr(self, cali_channel, chain):
        """
        send a tx signal for cali
        :param cali_channel:
        :param chain:
        :return:
        """
        if band == '1':
            cali_mode = '11b'
            cali_rate = '11'
        else:
            cali_mode = '11a'
            cali_rate = '6'
        if chain == '0':
            chains = '01'
        else:
            chains = '10'
        self.sn.write(b'shell WifiTxPowerInit.sh %s %s 20 %s %s 00%s\r\n' %
                      (band.encode('ascii'), cali_mode.encode('ascii'), str(cali_channel).encode('ascii'),
                       cali_rate.encode('ascii'), str(chain).encode('ascii')) + b'\r\n')
        time.sleep(2)
        logger.debug(f'shell WifiTxPowerInit.sh {band} {cali_mode} 20 {cali_channel} {cali_rate} 00{chains}')
        command_result = self.sn.readlines()
        for result in command_result:
            logger.debug(result.strip().decode('utf-8'))

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
        self.sn.write(b'shell iwpriv vap%s txpower %s\r\n' % (vap.encode('ascii'), str(adjust_power).encode('ascii')))
        logger.debug(f'shell iwpriv vap{vap} txpower {adjust_power}')
        command_result = self.sn.readlines()
        for result in command_result:
            logger.debug(result.strip().decode('utf-8'))

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
        self.sn.write(b'shell iwpriv Hisilicon%s cali_power "%s %s %s %s %s"\r\n' %
                      (hi_id.encode('ascii'), str(cali_chain).encode('ascii'), subband.encode('ascii'),
                       str(adjust_power_list[0]).encode('ascii'), str(adjust_power_list[1]).encode('ascii'),
                       str(adjust_power_list[2]).encode('ascii')) + b'\r\n')
        logger.debug(f'shell iwpriv Hisilicon{hi_id} cali_power "{cali_chain} {subband} {adjust_power_list[0]} '
                     f'{adjust_power_list[1]} {adjust_power_list[2]}"')
        command_result = self.sn.readlines()
        for result in command_result:
            logger.debug(result.strip().decode('utf-8'))

    def cali_para_write(self):
        """
        get the cali param and write to flash
        :return:
        """
        if band == '1':
            hi_id = '0'
        else:
            hi_id = '1'
        self.sn.write(b'\r\n')
        self.sn.write(b'shell iwpriv Hisilicon%s get_power_param\r\n' % hi_id.encode('ascii') + b'\r\n')
        logger.debug(f'shell iwpriv Hisilicon{hi_id} get_power_param')
        self.sn.write(b'ls\r\n')
        command_result = self.sn.read_until(b'Enabled')
        logger.debug(command_result)
        pwrcali_para = re.findall(b'get_power_param:\r+\n+(.+)\r+', command_result)[0].decode('utf-8')
        logger.debug(command_result)
        self.sn.write(b'wifi calibrate test parameter write wifichip %s type power len %s value %s\r\n' %
                      (band.encode('ascii'), radio_adress.encode('ascii'), pwrcali_para.encode('ascii')) + b'\r\n')
        logger.debug(
            f'wifi calibrate test parameter write wifichip {band} type power len {radio_adress} value {pwrcali_para}')
        command_result = self.sn.readlines()
        for result in command_result:
            logger.debug(result.strip().decode('utf-8'))
        self.sn.write(b'wifi calibrate test parameter read wifichip %s type power len %s\r\n' %
                      (band.encode('ascii'), radio_adress.encode('ascii')) + b'\r\n')
        logger.debug((f'wifi calibrate test parameter read wifichip %s type power len {radio_adress}'))
        pwrcali_result = self.sn.read_until(b'success!')
        logger.debug(pwrcali_result)

    def crc(self):
        """
        crc cali
        :return:
        """
        self.sn.write(b'wifi calibrate parameter crc calc\r\n')
        self.sn.write(b'wifi calibrate parameter crc check\r\n')
        command_result = self.sn.readlines()
        for result in command_result:
            logger.debug(result.strip().decode('utf-8'))

    def ex_command(self, command):
        """
        not use
        :param command:
        :return:
        """
        self.sn.write(command.encode('ascii') + b'\n')
        time.sleep(2)
        command_result = self.sn.read_very_eager().decode('ascii')
        logging.info('\n%s' % command_result)

    def tx(self):
        """
        for tx test, set a tx signal
        :return:
        """
        if int(channel) < 5000:
            band = ID_2G
        elif int(channel) < 5500:
            band = ID_5G_LOW
        else:
            band = ID_5G_HIGH
        self.sn.write(b'shell WifiTxRxSwitch.sh %s tx off\r\n' % band.encode('ascii'))
        logger.debug(channel)
        if bw == '40':
            channels = int(channel) - 10
        elif bw == '80':
            channels = int(channel) - 30
        else:
            channels = channel
        if int(channel) < 5000:
            channels = '{:.0f}'.format((int(channels) - 2407) / 5)  # 2407+5*1=2412
        else:
            channels = '{:.0f}'.format((int(channels) - 5000) / 5)  # 2407+5*1=2412
        if chain == '0':
            chains = '01'
        else:
            chains = '10'
        # tx
        self.sn.write(b'\r\n')
        self.sn.write(b'shell WifiTxInit.sh %s %s %s %s %s 00%s' %
                      (band.encode('ascii'), mode.encode('ascii'), bw.encode('ascii'), str(channels).encode('ascii'),
                       rates.encode('ascii'), chains.encode('ascii')) + b'\r\n')
        logger.debug(f'shell WifiTxInit.sh {band} {mode} {bw} {channels} {rates} 00{chains}')
        command_result = self.sn.readlines()
        for result in command_result:
            logger.debug(result.strip().decode('utf-8'))
        logger.info('TX COMMANDS DONE')

    def tx_off(self):
        """
        off the tx signal
        :return:
        """
        if int(channel) < 5000:
            band = ID_2G
        elif int(channel) < 5500:
            band = ID_5G_LOW
        else:
            band = ID_5G_HIGH
        self.sn.write(b'shell WifiTxRxSwitch.sh %s tx off\r\n' % band.encode('ascii'))
        logger.debug(f'shell WifiTxRxSwitch.sh {band} tx off')
        command_result = self.sn.readlines()
        for result in command_result:
            logger.debug(result.strip().decode('utf-8'))

    def get_paras(self):
        """
        not use
        :return:
        """
        if int(channel) < 5000:
            gain = gain_24
        else:
            gain = gain_5
        if int(channel) < 5000:
            band = ID_2G
        elif int(channel) < 5500:
            band = ID_5G_LOW
        else:
            band = ID_5G_HIGH
        # power para
        if int(channel) < 2437 and chain == '0':
            channel_groups = '98'
        elif int(channel) < 2437 and chain == '1':
            channel_groups = 'a8'
        elif 2437 < int(channel) < 2462 and chain == '0':
            channel_groups = '94'
        elif 2437 < int(channel) < 2462 and chain == '1':
            channel_groups = 'a4'
        elif int(channel) >= 2462 and chain == '0':
            channel_groups = '90'
        elif int(channel) >= 2462 and chain == '1':
            channel_groups = 'a0'
        else:
            logger.info('5g need add')
        self.sn.write(b'hipriv.sh "vap%s set_tx_pow rf_reg_ctl 1"' % band.encode('ascii') + b'\n')

        self.sn.write(b'hipriv.sh "vap%s reginfo soc 0x200380%s 0x200380%s";dmesg -c'
                      % (band.encode('ascii'), channel_groups.encode('ascii'), channel_groups.encode('ascii')) + b'\n')
        # command_result = self.sn.read_very_eager().decode('ascii')
        command_result = self.sn.read_until(b'value=0x\w+\r\r\nWAP(Dopra Linux) # ', timeout=2)
        command_result = re.search(b'value=0x\w+', command_result)
        default_value = re.sub('value=0x', '', command_result.group().decode('ascii'))
        logger.info('Default Value(HEX): ' + default_value)
        default_value = int(default_value, 16)
        return default_value

    def adjust_power(self):
        """
        not use
        :return:
        """
        if int(channel) < 5000:
            band = ID_2G
        elif int(channel) < 5500:
            band = ID_5G_LOW
        else:
            band = ID_5G_HIGH
        # power para
        if int(channel) < 2437 and chain == '0':
            channel_groups = '98'
        elif int(channel) < 2437 and chain == '1':
            channel_groups = 'a8'
        elif 2437 < int(channel) < 2462 and chain == '0':
            channel_groups = '94'
        elif 2437 < int(channel) < 2462 and chain == '1':
            channel_groups = 'a4'
        elif int(channel) >= 2462 and chain == '0':
            channel_groups = '90'
        elif int(channel) >= 2462 and chain == '1':
            channel_groups = 'a0'
        else:
            logger.info('5g need add')
        self.sn.write(b'hipriv.sh "vap%s regwrite soc 0x200380%s 0x%s"'
                      % (band.encode('ascii'), channel_groups.encode('ascii'), pwr_paras.encode('ascii')) + b'\n')

        self.sn.write(b'hipriv.sh "vap%s reginfo soc 0x200380%s 0x200380%s";dmesg -c'
                      % (band.encode('ascii'), channel_groups.encode('ascii'), channel_groups.encode('ascii')) + b'\n')
        command_result = self.sn.read_until(b'value=0x\w+\r\r\nWAP(Dopra Linux) # ', timeout=1)
        command_result = re.search(b'value=0x\w+', command_result)
        default_value = re.sub('value=0x', '', command_result.group().decode('ascii'))
        logger.info('Check Value(HEX): ' + default_value)
        gain = default_value
        return gain

    def set_default(self):
        """
        off all the tx and rx
        :return:
        """
        self.sn.write(b'shell WifiTxRxSwitch.sh 1 tx off\r\n')
        self.sn.write(b'shell WifiTxRxSwitch.sh 2 tx off\r\n')
        self.sn.write(b'shell WifiTxRxSwitch.sh 1 rx off\r\n')
        self.sn.write(b'shell WifiTxRxSwitch.sh 2 rx off\r\n')
        # self.sn.write(b'shell WifiRxReset.sh %s' % band.encode('ascii') + b'\r\n')
        command_result = self.sn.readlines()
        for result in command_result:
            # logger.debug(result.decode('utf-8'))
            logger.debug(result.strip().decode('utf-8'))

    def rx_on(self):
        """
        turn on the rx
        :return:
        """
        if int(channel) < 5000:
            band = ID_2G
        elif int(channel) < 5500:
            band = ID_5G_LOW
        else:
            band = ID_5G_HIGH
        self.sn.write(b'shell WifiTxRxSwitch.sh %s rx on' % band.encode('ascii') + b'\r\n')
        command_result = self.sn.readlines()
        for result in command_result:
            logger.debug(result.strip().decode('utf-8'))

    def rx_off(self):
        """
        turn off the rx
        :return:
        """
        if int(channel) < 5000:
            band = ID_2G
        elif int(channel) < 5500:
            band = ID_5G_LOW
        else:
            band = ID_5G_HIGH
        self.sn.write(b'shell WifiTxRxSwitch.sh %s rx off' % band.encode('ascii') + b'\r\n')
        command_result = self.sn.readlines()
        for result in command_result:
            logger.debug(result.strip().decode('utf-8'))

    def rx(self):
        """
        set for rx test
        :return:
        """
        if int(channel) < 5000:
            band = ID_2G
        elif int(channel) < 5500:
            band = ID_5G_LOW
        else:
            band = ID_5G_HIGH
        logger.debug(band)
        logger.debug(mode)
        logger.debug(bw)
        logger.debug(channel)
        logger.debug(chain)
        # self.sn.write(b'shell WifiRxReset.sh %s\r\n' % band.encode('ascii'))
        # self.sn.write(b'shell WifiTxRxSwitch.sh %s tx off\r\n' % band.encode('ascii'))
        # self.sn.write(b'shell WifiTxRxSwitch.sh %s rx on' % band.encode('ascii') + b'\r\n')
        # self.sn.write(b'\r\n')
        logger.debug(channel)
        if bw == '40':
            channels = int(channel) - 10
        elif bw == '80':
            channels = int(channel) - 30
        else:
            channels = int(channel)

        if int(channel) < 5000:
            channels = '{:.0f}'.format((int(channels) - 2407) / 5)
        else:
            channels = '{:.0f}'.format((int(channels) - 5000) / 5)
        logger.debug(channels)
        if chain == '0':
            chains = '01'
        else:
            chains = '10'
        # if mode == '11b':
        #     modes = ''
        #     rates = 'rate'
        # elif mode == '11g':
        #     modes = '11ng'
        #     rates = 'mcs'
        # logger.debug('chain set',chain,type(chain),chains)
        self.sn.write(b'shell WifiRxInit.sh %s %s %s %s 00%s' % (band.encode('ascii'), mode.encode('ascii'),
                                                                 bw.encode('ascii'), str(channels).encode('ascii'),
                                                                 chains.encode('ascii')) + b'\r\n')
        logger.debug(f'shell WifiRxInit.sh {band} {mode} {bw} {channels} 00{chains}')
        command_result = self.sn.readlines()
        for result in command_result:
            logger.debug(result.strip().decode('utf-8'))
        logger.info('RX COMMANDS DONE')

    def get_statistics(self):
        """
        get the per result
        :return:
        """
        if int(channel) < 5000:
            vap = VAP_2G
        else:
            vap = VAP_5G
        self.sn.write(b'shell iwpriv vap%s get_rx_info' % vap.encode('ascii') + b'\r\n')
        time.sleep(3)
        command_result = self.sn.readlines()
        logger.debug(command_result)
        for result in command_result:
            logger.debug(result.strip().decode('utf-8'))
        logger.debug(command_result[2])
        rx_good = re.findall(b'RX OK:(\d+)', command_result[2])[0].decode('utf-8')
        logger.debug(rx_good)
        # command_result = self.sn.read_until(b'RX ERROR')
        # command_result = re.search(b'RX OK:\w+', command_result)
        # logger.debug(command_result)
        # logger.debug(command_result.group())
        # rx_good = re.sub('RX OK:', '', command_result.group().decode('ascii'))
        PER_value = (int(RX_PACKETS) - int(rx_good)) / int(RX_PACKETS)
        logger.info('Packets: ' + str(RX_PACKETS) + 'PER: ' + str(PER_value))
        # self.sn.write(b'shell WifiTxRxSwitch.sh %s rx off' % band.encode('ascii') + b'\r\n')
        return PER_value


if __name__ == '__main__':

    # INIT DUT
    dt = dut('COM'+dut_com, baudrate)
    dt.set_default()
    dt.login(user, pwd)
    dt.init(add1, add2, add3, add4)
