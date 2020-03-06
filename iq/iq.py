#!/user/bin/env python
# encoding: utf-8
# @time      : 20200218

__author__ = 'Ethan'

import time
from colorama import init, Fore, Style
from parameters import IQ_PORT, IQ_ROUT, EVM_AG, EVM_N, EVM_AC, EVM_AX, RL, IQ_PORT_INTERFERE, \
    IQ_ROUT_INTERFERE, RX_PACKETS, LOG_ENABLE
import visa
import csv
import re
import logging

logger = logging.getLogger()


# # GEN TIME
# now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
# # logger.debug(now_time)
# logger.setLevel(logging.DEBUG)  # logger的总开关，只有大于Debug的日志才能被logger对象处理
#
# # 第二步，创建一个handler，用于写入日志文件
# file_handler = logging.FileHandler('./log/log_' + now_time + '.txt', mode='w')
# file_handler.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
# # 创建该handler的formatter
# file_handler.setFormatter(
#     logging.Formatter(
#         fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
#         datefmt='%Y-%m-%d %H:%M:%S')
# )
# # 添加handler到logger中
# logger.addHandler(file_handler)
#
# # 第三步，创建一个handler，用于输出到控制台
# console_handler = logging.StreamHandler()
# if LOG_ENABLE == '1':
#     console_handler.setLevel(logging.DEBUG)  # 输出到控制台的log等级的开关
# else:
#     console_handler.setLevel(logging.INFO)  # 输出到控制台的log等级的开关
# # 创建该handler的formatter
# console_handler.setFormatter(
#     logging.Formatter(
#         fmt='%(asctime)s - %(levelname)s: %(message)s',
#         datefmt='%Y-%m-%d %H:%M:%S')
# )
# logger.addHandler(console_handler)


class IQxel:
    def __init__(self, ip, visaDLL=None, *args):
        self.ip = ip
        # self.visaDLL = 'C:\windows\system32\visa64.dll' if visaDLL is None else visaDLL
        self.address = 'TCPIP0::%s::hislip0::INSTR' % self.ip
        # self.resourceManager = visa.ResourceManager(self.visaDLL)
        self.resourceManager = visa.ResourceManager()
        self.instance = self.resourceManager.open_resource(self.address)

    def close(self):
        if self.instance is not None:
            self.resourceManager.close()
            self.instance = None

    def __formats__(self, format_spec: object) -> object:
        """
        format the result
        :param format_spec:
        :return:
        """
        self.format_spec = format_spec
        format_spec = float(format_spec)
        format_spec = '{:.3f}'.format(format_spec)
        return format_spec

    def save_image(self, imagname, fmt):
        """
        if save image
        :param imagname:
        :param fmt:
        :return:
        """
        assert fmt in ['jpg', 'png'], 'Invalid postfix of image'
        logger.debug('MMEM:STOR:IMAG "%s.%s"' % (imagname, fmt))
        self.instance.write('MMEM:STOR:IMAG "%s.%s"' % (imagname, fmt))

    def reset(self):
        self.instance.write('*RST')

    @property
    def read_idn(self):
        idn = self.instance.query('*IDN?')
        logger.debug(idn)
        iq_model = idn.split(',')[1]
        logger.debug(iq_model)
        iq_model = iq_model[1]
        logger.debug(iq_model)
        IQ_PORT_model = IQ_PORT.isdigit()
        logger.debug(IQ_PORT_model)
        if iq_model == 'IQXEL' and IQ_PORT_model is True:
            mw = ''
        elif iq_model == 'IQXEL-M' and IQ_PORT_model is False:
            mw = ''
        elif iq_model == 'IQXEL-MW' and IQ_PORT_model is False:
            mw = 'M'
        elif iq_model == 'IQXEL-M2W' and IQ_PORT_model is False:
            mw = ''
        else:
            mw = ''
        logger.debug(mw)
        return mw

    def set_pathloss(self, pathloss):
        """
        set pathloss, needs to change to support to 8x8 or any path
        2019-11-15 support for any path
        :return:
        """
        pathloss_list = []
        with open(pathloss) as f:
            pathloss = csv.reader(f)
            for path_loss in pathloss:
                logger.debug(path_loss)
                pathloss_list.append(path_loss)
            # write pathloss to iq
            rows = [row for row in pathloss_list]
            path_num = len(rows[0]) - 1
            for path in range(path_num):
                logger.debug(path)
                self.instance.write('MEM:TABLE "' + str(path) + '"; MEM:TABLE:DEFINE "FREQ,LOSS"')
                for path_loss in pathloss_list:
                    channel = path_loss[0]
                    pathloss = path_loss[path + 1]
                    logger.debug(pathloss)
                    self.instance.write('MEM:TABLE "' + str(path) + '";MEMory:TABLe:INSert:POINt %s MHz,%s' %
                                        (channel, pathloss))
                self.instance.write('MEMory:TABLe "' + str(path) + '";MEMory:TABLe:STORe')

    def use_pathloss(self, mw, chain):
        self.instance.write('%sVSA%s;RFC:USE "%s",RF%s' % (mw, IQ_ROUT, chain, IQ_PORT))
        self.instance.write('%sVSA%s;RFC:STAT  ON,RF%s' % (mw, IQ_ROUT, IQ_PORT))
        self.instance.write('%sVSG%s;RFC:USE "%s",RF%s' % (mw, IQ_ROUT, chain, IQ_PORT))
        self.instance.write('%sVSG%s;RFC:STAT  ON,RF%s' % (mw, IQ_ROUT, IQ_PORT))

    def vsa(self, mw, mode, bw, rates, channel, target_power):
        # print(mw, IQ_ROUT, IQ_PORT, IQ_ROUT)
        self.instance.write('%sROUT%s;PORT:RES RF%s,VSA%s' % (mw, IQ_ROUT, IQ_PORT, IQ_ROUT))
        self.instance.write('CHAN1;WIFI')
        self.instance.write('VSA1;TRIG:SOUR VIDeo')
        logger.debug(channel)
        channels = int(channel) * 1000000
        logger.debug(channels)
        self.instance.write('%sVSA%s;FREQ:cent %s' % (mw, IQ_ROUT, str(channels)))
        if RL == '1':
            self.instance.query_ascii_values('%sVSA%s;RLEVel:AUTO;*wai;*opc?' % (mw, IQ_ROUT))
        else:
            rlevel = target_power + 10
            logger.debug(str(rlevel))
            self.instance.query_ascii_values('%sVSA%s;RLEV %d;*wai;*opc?' % (mw, IQ_ROUT, rlevel))
        if int(bw) > 80:
            sampling_rate = 240000000
        else:
            sampling_rate = 160000000
        self.instance.write('%sVSA%s;SRAT %d' % (mw, IQ_ROUT, sampling_rate))
        if mode == '11b':
            capture_time = (32 - float(rates) * 2) / 1000
            standard = 'DSSS'
            mask_limit = 'AUTO'
        elif mode == '11g' or mode == '11a':
            capture_time = (13.2 - float(rates) * 3 / 16) / 1000
            standard = 'OFDM'
            mask_limit = 'AUTO'
        elif mode == '11n':
            capture_time = (12 - float(rates) * 10 / 7) / 1000
            standard = 'OFDM'
            mask_limit = 'AUTO'
        elif mode == '11ac':
            capture_time = (8 - float(rates) * 2 / 3) / 1000
            standard = 'OFDM'
            mask_limit = 'AUTO'
        elif mode == '11ax':
            capture_time = (9 - float(rates) * 2 / 3) / 1000
            standard = 'OFDM'
            mask_limit = '11AX'
        else:
            capture_time = 0.01
            standard = 'OFDM'
            mask_limit = 'AUTO'
        if mode == '11a' and EVM_AG == '1':
            channel_estimation = 'DATA'
        elif mode == '11g' and EVM_AG == '1':
            channel_estimation = 'DATA'
        elif mode == '11n' and EVM_N == '1':
            channel_estimation = 'DATA'
        elif mode == '11ac' and EVM_AC == '1':
            channel_estimation = 'DATA'
        elif mode == '11ax' and EVM_AX == '1':
            channel_estimation = 'DATA'
        else:
            channel_estimation = 'LTF'
        logger.debug('Captime: ' + str(capture_time))
        self.instance.write('CHAN1;WIFI;CONF:STAN %s' % standard)
        self.instance.write('CHAN1;WIFI;CONF:OFDM:CEST %s' % channel_estimation)
        self.instance.write('CHAN1;WIFI;CONF:SPEC:HLIM:TYPE %s' % mask_limit)
        self.instance.write('VSA%s;CAPT:TIME %s' % (IQ_ROUT, capture_time))

    def analysis(self, mode, rates):
        """
        let iq get the data and analysis
        :return:
        """
        self.instance.write('CHAN1')
        self.instance.write('VSA%s ;init' % IQ_ROUT)
        self.instance.write('WIFI')
        status_pwr = self.instance.query_ascii_values('calc:pow 0, 2;*wai;*opc?')
        logger.debug(status_pwr)
        status_txq = self.instance.query_ascii_values('calc:txq 0, 2;*wai;*opc?')
        logger.debug(status_txq)
        status_ccdf = self.instance.query_ascii_values('calc:ccdf 0, 2;*wai;*opc?')
        logger.debug(status_ccdf)
        status_ramp = self.instance.query_ascii_values('calc:ramp 0, 2;*wai;*opc?')
        logger.debug(status_ramp)
        status_spec = self.instance.query_ascii_values('calc:spec 0, 2;*wai;*opc?')
        logger.debug(status_spec)
        status = 0
        # print(status_pwr,type(status_pwr),status_pwr[0],type(status_pwr[0]))
        while status_pwr[0] != 1.0 or status_txq[0] != 1.0 or status_spec[0] != 1.0 or status_ramp[0] != 1.0 or \
                status_ccdf[0] != 1.0:
            status_pwr = self.instance.query_ascii_values('calc:pow 0, 2;*wai;*opc?')
            logger.debug(status_pwr)
            status_txq = self.instance.query_ascii_values('calc:txq 0, 2;*wai;*opc?')
            logger.debug(status_txq)
            status_ccdf = self.instance.query_ascii_values('calc:ccdf 0, 2;*wai;*opc?')
            logger.debug(status_ccdf)
            status_ramp = self.instance.query_ascii_values('calc:ramp 0, 2;*wai;*opc?')
            logger.debug(status_ramp)
            status_spec = self.instance.query_ascii_values('calc:spec 0, 2;*wai;*opc?')
            logger.debug(status_spec)
            status += 1
            if status > 2:
                logger.error('No capture data for segment!')
                break
        if mode == '11b':
            wait_time = (32 - float(rates) * 2) / 10
        elif mode == '11g' or mode == '11a':
            wait_time = (13.2 - float(rates) * 3 / 16) / 10
        elif mode == '11n':
            wait_time = (12 - float(rates) * 10 / 7) / 10
        elif mode == '11ac':
            wait_time = (8 - float(rates) * 2 / 3) / 10
        elif mode == '11ax':
            wait_time = (9 - float(rates) * 2 / 3) / 10
        else:
            wait_time = 1
        time.sleep(wait_time)
        logger.debug('wait...' + str(wait_time))

    def get_power(self, stream, target_power, spec_pwr):
        """
        get power
        :return:
        """
        data_pwr = self.instance.query_ascii_values('WIFI;FETC:SEGM:POW:SIGN%s:AVER?' % str(stream))
        logger.debug(data_pwr)
        if data_pwr[0] == 0.0:
            avg_power = data_pwr[1]
            logger.debug(avg_power)
            avg_power = self.__formats__(avg_power)
            delta_pwr = abs(float(avg_power) - float(target_power))
            logger.debug(delta_pwr)
            if delta_pwr > spec_pwr:
                logger.info('Power:               ' + Fore.RED + avg_power + Style.RESET_ALL + 'dBm')
                result_pwr = 'Fail'
            else:
                logger.info('Power:               ' + Fore.BLUE + avg_power + Style.RESET_ALL + 'dBm')
                result_pwr = 'Pass'
        else:
            logger.error('Error: ' + str(data_pwr[0]))
            avg_power = 'NA'
            result_pwr = 'NA'
        return avg_power, result_pwr

    def get_evm(self, mode, spec_evm, evm_margin):
        """
        get evm
        :return:
        """
        if mode == '11b':
            data_txq = self.instance.query_ascii_values('WIFI;FETC:SEGM:TXQ:DSSS:AVER?')
        else:
            data_txq = self.instance.query_ascii_values('WIFI;FETC:SEGM:TXQ:OFDM:AVER?')
        if data_txq[0] == 0.0:
            avg_evm = data_txq[1]
            avg_evm = self.__formats__(avg_evm)
            peak_evm = data_txq[2]
            peak_evm = self.__formats__(peak_evm)
            spec_evm = float(spec_evm) - float(evm_margin)
            if float(avg_evm) > float(spec_evm):
                logger.info('EVM:                 ' + Fore.RED + avg_evm + Style.RESET_ALL + 'dB')
                result_evm = 'Fail'
            else:
                logger.info('EVM:                 ' + Fore.BLUE + avg_evm + Style.RESET_ALL + 'dB')
                result_evm = 'Pass'
            logger.info('EVM Peak:            ' + peak_evm + 'dB')
        else:
            logger.error('Error: ' + str(data_txq[0]))
            avg_evm = 'NA'
            result_evm = 'NA'
        return avg_evm, result_evm

    def get_ppm(self, mode, spec_symbol_clock_error):
        """
        get ppm
        :return:
        """
        if mode == '11b':
            data_txq = self.instance.query_ascii_values('WIFI;FETC:SEGM:TXQ:DSSS:AVER?')
        else:
            data_txq = self.instance.query_ascii_values('WIFI;FETC:SEGM:TXQ:OFDM:AVER?')
        if data_txq[0] == 0.0:
            symbol_clock_error = data_txq[4]
            symbol_clock_error = self.__formats__(symbol_clock_error)
            if abs(float(symbol_clock_error)) > abs(float(spec_symbol_clock_error)):
                logger.info('Symbol Clock Error:  ' + Fore.RED + symbol_clock_error + Style.RESET_ALL + 'ppm')
                result_symbol_clock_error = 'Fail'
            else:
                logger.info('Symbol Clock Error:  ' + Fore.BLUE + symbol_clock_error + Style.RESET_ALL + 'ppm')
                result_symbol_clock_error = 'Pass'
        else:
            logger.error('Error: ' + str(data_txq[0]))
            symbol_clock_error = 'NA'
            result_symbol_clock_error = 'NA'
        return symbol_clock_error, result_symbol_clock_error

    def get_lo_leakage(self, mode, spec_lo_leakage):
        """
        get LO leakage
        :return:
        """
        if mode == '11b':
            data_txq = self.instance.query_ascii_values('WIFI;FETC:SEGM:TXQ:DSSS:AVER?')
        else:
            data_txq = self.instance.query_ascii_values('WIFI;FETC:SEGM:TXQ:OFDM:AVER?')
        if data_txq[0] == 0.0:
            lo_leakage = data_txq[5]
            lo_leakage = self.__formats__(lo_leakage)
            # spec_lo_leakage = -15
            if abs(float(lo_leakage)) < abs(float(spec_lo_leakage)):
                logger.info('LO Leakage:          ' + Fore.RED + lo_leakage + Style.RESET_ALL + 'dB')
                result_lo_leakage = 'Fail'
            else:
                logger.info('LO Leakage:          ' + Fore.BLUE + lo_leakage + Style.RESET_ALL + 'dB')
                result_lo_leakage = 'Pass'
        else:
            logger.error('Error: ' + str(data_txq[0]))
            lo_leakage = 'NA'
            result_lo_leakage = 'NA'
        return lo_leakage, result_lo_leakage

    def get_mask(self, spec_mask):
        """
        get mask
        :return:
        """
        data_mask = self.instance.query_ascii_values('WIFI;FETC:SEGM:SPEC:AVER:VIOL?')
        if data_mask[0] == 0.0:
            mask = data_mask[1]
            mask = self.__formats__(mask)
            # spec_mask = 5.12
            if abs(float(mask)) > float(spec_mask):
                logger.info('Mask:                ' + Fore.RED + mask + Style.RESET_ALL + '%')
                result_mask = 'Fail'
            else:
                logger.info('Mask:                ' + Fore.BLUE + mask + Style.RESET_ALL + '%')
                result_mask = 'Pass'
        else:
            logger.error('Error: ' + str(data_mask[0]))
            mask = 'NA'
            result_mask = 'NA'
        return mask, result_mask

    def get_obw(self, bw, spec_obw_20M, spec_obw_40M, spec_obw_80M, spec_obw_160M):
        """
        get obw
        :return:
        """
        data_obw = self.instance.query_ascii_values('WIFI;FETC:SEGM:SPEC:AVER:OBW?')
        if data_obw[0] == 0.0:
            obw = data_obw[1]
            obw = self.__formats__(obw)
            obw = round(float(obw) / 1000000, 3)
            if bw == '80':
                spec_obw = spec_obw_80M
            elif bw == '40':
                spec_obw = spec_obw_40M
            elif bw == '160':
                spec_obw = spec_obw_160M
            else:
                spec_obw = spec_obw_20M
            if obw > float(spec_obw):
                logger.info('OBW:                 ' + Fore.RED + str(obw) + Style.RESET_ALL + 'MHz')
                result_obw = 'Fail'
            else:
                logger.info('OBW:                 ' + Fore.BLUE + str(obw) + Style.RESET_ALL + 'MHz')
                result_obw = 'Pass'
        else:
            logger.error('Error: ' + str(data_obw[0]))
            obw = 'NA'
            spec_obw = 'NA'
            result_obw = 'NA'
        return obw, spec_obw, result_obw

    def get_flatness(self, mode):
        """
        get flatness
        :return:
        """
        if mode == '11b':
            flatness = 'NA'
            spec_flatness = 'NA'
            result_flatness = 'NA'
            pass
        else:
            data_flatness = self.instance.query('WIFI;FETC:SEGM:OFDM:SFL:AVER:CHEC?')
            if data_flatness[0] == '0':
                flatness = data_flatness[0]
                spec_flatness = 0
                if int(flatness) == spec_flatness:
                    logger.info('Flatness:            ' + Fore.BLUE + flatness + Style.RESET_ALL)
                    result_flatness = 'Pass'
                else:
                    logger.info('Flatness:            ' + Fore.RED + flatness + Style.RESET_ALL)
                    result_flatness = 'Fail'
            else:
                logger.error('Error: ' + str(data_flatness[0]))
                flatness = 'NA'
                spec_flatness = 'NA'
                result_flatness = 'NA'
        return flatness, spec_flatness, result_flatness

    def get_ramp_time(self, mode):
        if mode == '11b':
            data_on_time = self.instance.query_ascii_values('WIFI;FETC:SEGM:RAMP:ON:TRIS?')
            time.sleep(0.2)
            spec_ramp_on_time = 2.0
            if data_on_time[0] == 0.0:
                ramp_on_time = data_on_time[1]
                ramp_on_time = float(ramp_on_time) * 1000000
                ramp_on_time = self.__formats__(ramp_on_time)
                if float(ramp_on_time) > spec_ramp_on_time:
                    logger.info('Ramp On Time:        ' + Fore.RED + ramp_on_time + Style.RESET_ALL + 'us')
                    result_ramp_on_time = 'Fail'
                else:
                    logger.info('Ramp On Time:        ' + Fore.BLUE + ramp_on_time + Style.RESET_ALL + 'us')
                    result_ramp_on_time = 'Pass'
            else:
                logger.error('Error: ' + str(data_on_time[0]))
                ramp_on_time = 'NA'
                result_ramp_on_time = 'NA'
            data_off_time = self.instance.query_ascii_values('WIFI;FETC:SEGM:RAMP:OFF:TRIS?')
            time.sleep(0.2)
            spec_ramp_off_time = 2.0
            if data_off_time[0] == 0.0:
                ramp_off_time = data_off_time[1]
                ramp_off_time = float(ramp_off_time) * 1000000
                ramp_off_time = self.__formats__(ramp_off_time)
                if float(ramp_off_time) > spec_ramp_off_time:
                    logger.info('Ramp Off Time:       ' + Fore.RED + ramp_off_time + Style.RESET_ALL + 'us')
                    result_ramp_off_time = 'Fail'
                else:
                    logger.info('Ramp Off Time:       ' + Fore.BLUE + ramp_off_time + Style.RESET_ALL + 'us')
                    result_ramp_off_time = 'Pass'
            else:
                logger.error('Error: ' + str(data_off_time[0]))
                ramp_off_time = 'NA'
                result_ramp_off_time = 'NA'
        else:
            ramp_on_time = result_ramp_on_time = ramp_off_time = result_ramp_off_time = 'NA'
        return ramp_on_time, result_ramp_on_time, ramp_off_time, result_ramp_off_time

    # for normal rx sensitivity test
    def vsg(self, mw, mode, bw, rates, channel, rlevel):
        # rint(mw, IQ_ROUT, IQ_PORT, IQ_ROUT)
        self.instance.write('%sROUT%s;PORT:RES RF%s,VSG%s' % (mw, IQ_ROUT, IQ_PORT, IQ_ROUT))
        self.instance.write('CHAN1;WIFI')
        channels = int(channel) * 1000000
        self.instance.write('%sVSG%s;FREQ:cent %d' % (mw, IQ_ROUT, channels))
        if int(bw) > 80:
            sampling_rate = 240000000
        else:
            sampling_rate = 160000000
        self.instance.write('%sVSA%s;SRAT %d' % (mw, IQ_ROUT, sampling_rate))
        # rlevel = start + loss
        logger.debug(rlevel)
        self.instance.write('%sVSG%s;POW:lev %d' % (mw, IQ_ROUT, rlevel))
        self.instance.write('VSG1;POW:STAT ON')
        self.instance.write('VSG1;MOD:STAT ON')
        self.instance.write('VSG1;WAVE:EXEC OFF')
        self.instance.write('VSG1;WLIS:COUN %d' % int(RX_PACKETS))
        # wave = 'OFDM-6'
        if mode == '11b' and rates == '1':
            wave = 'DSSS-1'
            vsg_delay = int(RX_PACKETS) / 100 + 5 - int(rates) * int(RX_PACKETS) / 1000
        elif mode == '11b' and rates == '2':
            wave = 'DSSS-2L'
            vsg_delay = int(RX_PACKETS) / 100 - int(rates) * int(RX_PACKETS) / 1000
        elif mode == '11b' and rates == '5.5':
            wave = 'CCK-5_5S'
            vsg_delay = int(RX_PACKETS) / 100 - int(float(rates) * int(RX_PACKETS) / 1000)
        elif mode == '11b' and rates == '11':
            wave = 'CCK-11S'
            vsg_delay = int(RX_PACKETS) / 100 - int(rates) * int(RX_PACKETS) / 1800
        elif mode == '11g' or mode == '11a':
            wave = 'OFDM-' + rates
            vsg_delay = int(RX_PACKETS) / 100 - int(rates) * int(RX_PACKETS) / 6000
        elif mode == '11n':
            wave = 'HT' + bw + '_MCS' + rates
            vsg_delay = int(RX_PACKETS) / 100 - int(rates) * int(RX_PACKETS) / 1000
        elif mode == '11ac':
            wave = '11AC_VHT' + bw + '_S1_MCS' + rates
            vsg_delay = int(RX_PACKETS) / 100 - int(rates) * int(RX_PACKETS) / 1000
        elif mode == '11ax':
            wave = '11AX_HE' + bw + '_S1_HE' + rates
            vsg_delay = int(RX_PACKETS) / 100 - int(rates) * int(RX_PACKETS) / 1200
        # logger.info(wave)
        logger.info('Delay Time:' + str(vsg_delay))
        self.instance.write('VSG1; WAVE:LOAD "/user/WiFi_%s.iqvsg"' % wave)
        self.instance.write('VSG1 ;wave:exec off')
        self.instance.write('WLIST:WSEG1:DATA "/user/WiFi_%s.iqvsg"' % wave)
        self.instance.write('wlist:wseg1:save')
        self.instance.write('WLIST:COUNT:ENABLE WSEG1')
        self.instance.write('WAVE:EXEC ON, WSEG1')
        time.sleep(vsg_delay)
        self.instance.write('VSG1 ;WAVE:EXEC OFF')
        self.instance.write('WLIST:COUNT:DISABLE WSEG1')

    # # for LDPC
    # def vsg(self, mw, mode, bw, rates, channel, rlevel):
    #     # rint(mw, IQ_ROUT, IQ_PORT, IQ_ROUT)
    #     self.instance.write('%sROUT%s;PORT:RES RF%s,VSG%s' % (mw, IQ_ROUT, IQ_PORT, IQ_ROUT))
    #     self.instance.write('CHAN1;WIFI')
    #     channels = int(channel) * 1000000
    #     self.instance.write('%sVSG%s;FREQ:cent %d' % (mw, IQ_ROUT, channels))
    #     if int(bw) > 80:
    #         sampling_rate = 240000000
    #     else:
    #         sampling_rate = 160000000
    #     self.instance.write('%sVSA%s;SRAT %d' % (mw, IQ_ROUT, sampling_rate))
    #     # rlevel = start + loss
    #     logger.debug(rlevel)
    #     self.instance.write('%sVSG%s;POW:lev %d' % (mw, IQ_ROUT, rlevel))
    #     self.instance.write('VSG1;POW:STAT ON')
    #     self.instance.write('VSG1;MOD:STAT ON')
    #     self.instance.write('VSG1;WAVE:EXEC OFF')
    #     self.instance.write('VSG1;WLIS:COUN %d' % int(RX_PACKETS))
    #     # wave = 'OFDM-6'
    #     if mode == '11b' and rates == '1':
    #         wave = 'CCK_1_Fs160'
    #         vsg_delay = int(RX_PACKETS) / 100 + 5 - int(rates) * int(RX_PACKETS) / 1000
    #     elif mode == '11b' and rates == '2':
    #         wave = 'DSSS-2L'
    #         vsg_delay = int(RX_PACKETS) / 100 - int(rates) * int(RX_PACKETS) / 1000
    #     elif mode == '11b' and rates == '5.5':
    #         wave = 'CCK-5_5S'
    #         vsg_delay = int(RX_PACKETS) / 100 - int(float(rates) * int(RX_PACKETS) / 1000)
    #     elif mode == '11b' and rates == '11':
    #         wave = 'CCK_11_Fs160'
    #         vsg_delay = int(RX_PACKETS) / 100 - int(rates) * int(RX_PACKETS) / 1800
    #     elif mode == '11g' or mode == '11a':
    #         wave = 'LEG' + rates + '_1500bytes_100us_Fs160'
    #         vsg_delay = int(RX_PACKETS) / 100 - int(rates) * int(RX_PACKETS) / 6000
    #     elif mode == '11n':
    #         wave = 'MCS' + rates + '_HT' + bw + '_BCC_MM_LGI_1000bytes_PG100us_Fs160'
    #         vsg_delay = int(RX_PACKETS) / 100 - int(rates) * int(RX_PACKETS) / 1000
    #     elif mode == '11ac':
    #         wave = 'MCS' + rates + '_NSS1_VHT' + bw + '_SGI_LDPC_MM_4000B_PG100us'
    #         vsg_delay = int(RX_PACKETS) / 100 - int(rates) * int(RX_PACKETS) / 1000
    #     elif mode == '11ax':
    #         if rates == '0':
    #             length = '1000'
    #         else:
    #             length = '4000'
    #         wave = 'HE' + rates + '_NSS1_HE' + bw + '_LDPC_' + length + 'b_PG100us_CPLTF1_PE2'
    #         vsg_delay = int(RX_PACKETS) / 100 - int(rates) * int(RX_PACKETS) / 1200
    #     # logger.info(wave)
    #     logger.info('Delay Time:' + str(vsg_delay))
    #     self.instance.write('VSG1; WAVE:LOAD "/user/%s.iqvsg"' % wave)
    #     self.instance.write('VSG1 ;wave:exec off')
    #     self.instance.write('WLIST:WSEG1:DATA "/user/%s.iqvsg"' % wave)
    #     self.instance.write('wlist:wseg1:save')
    #     self.instance.write('WLIST:COUNT:ENABLE WSEG1')
    #     self.instance.write('WAVE:EXEC ON, WSEG1')
    #     time.sleep(vsg_delay)
    #     self.instance.write('VSG1 ;WAVE:EXEC OFF')
    #     self.instance.write('WLIST:COUNT:DISABLE WSEG1')

    def vsg_aj(self, mw, mode, bw, rates, channel, rlevel):
        self.instance.write(
            '%sROUT%s;PORT:RES RF%s,VSG%s' % (mw, IQ_ROUT_INTERFERE, IQ_PORT_INTERFERE, IQ_ROUT_INTERFERE))
        self.instance.write('CHAN1;WIFI')
        if int(bw) == 20 and 2400 < int(channel) < 2440:
            channel_aj = int(channel) + 25
        elif int(bw) == 20 and 2440 < int(channel) < 2483.5:
            channel_aj = int(channel) - 25
        elif int(bw) == 40 and int(channel) == 2422:
            channel_aj = int(channel) + 50
        elif int(bw) == 40 and int(channel) == 2452:
            channel_aj = int(channel) - 50
        elif int(bw) == 20:
            if 5100 < int(channel) < 5250 or 5500 <= int(channel) <= 5600 or 5745 <= int(channel) <= 5785:
                channel_aj = int(channel) + 20
            elif 5250 < int(channel) <= 5320 or 5600 < int(channel) < 5745 or 5785 < int(channel) <= 5825:
                channel_aj = int(channel) - 20
        elif int(bw) == 40:
            if 5100 < int(channel) < 5250 or 5500 <= int(channel) <= 5600 or 5745 <= int(channel) <= 5785:
                channel_aj = int(channel) + 40
            elif 5250 < int(channel) <= 5320 or 5600 < int(channel) < 5745 or 5785 < int(channel) <= 5825:
                channel_aj = int(channel) - 40
        elif int(bw) == 80:
            if 5100 < int(channel) < 5250 or 5500 <= int(channel) <= 5600:
                channel_aj = int(channel) + 80
            elif 5250 < int(channel) <= 5320 or 5600 < int(channel) < 5745 or 5745 < int(channel) <= 5825:
                channel_aj = int(channel) - 80
        elif int(bw) == 160:
            if 5100 < int(channel) < 5500:
                channel_aj = int(channel) + 160
            elif 5500 < int(channel) <= 5825:
                channel_aj = int(channel) - 160
        else:
            logger.info('Test Channel is not right! No adjacent channel!')
            return False
        channels = channel_aj * 1000000
        self.instance.write('%sVSG%s;FREQ:cent %d' % (mw, IQ_ROUT, channels))
        if int(bw) > 80:
            sampling_rate = 240000000
        else:
            sampling_rate = 160000000
        self.instance.write('%sVSA%s;SRAT %d' % (mw, IQ_ROUT, sampling_rate))
        # rlevel = start + loss
        logger.debug(rlevel)
        self.instance.write('%sVSG%s;POW:lev %d' % (mw, IQ_ROUT, rlevel))
        # wave = 'OFDM-6'
        if mode == '11b' and rates == '1':
            wave = 'DSSS-1'
        elif mode == '11b' and rates == '2':
            wave = 'DSSS-2L'
        elif mode == '11b' and rates == '5.5':
            wave = 'CCK-5_5S'
        elif mode == '11b' and rates == '11':
            wave = 'CCK-11S'
        elif mode == '11g' or mode == '11a':
            wave = 'OFDM-' + rates
        elif mode == '11ng' or mode == '11na':
            wave = 'HT' + bw + '_MCS' + rates
        elif mode == '11ac':
            wave = '11AC_VHT' + bw + '_S1_MCS' + rates
        elif mode == '11ax':
            wave = '11AX_HE' + bw + '_S1_HE' + rates
        # logger.info(wave)
        self.instance.write('VSG1; WAVE:LOAD "/user/WiFi_%s.iqvsg"' % wave)
        self.instance.write('VSG1;WAVE:EXEC ON')
        self.instance.write('VSG1;POW:STAT ON')
        self.instance.write('VSG1;MOD:STAT ON')

    def vsg_naj(self, mw, mode, bw, rates, channel, rlevel):
        self.instance.write(
            '%sROUT%s;PORT:RES RF%s,VSG%s' % (mw, IQ_ROUT_INTERFERE, IQ_PORT_INTERFERE, IQ_ROUT_INTERFERE))
        self.instance.write('CHAN1;WIFI')
        if int(bw) == 20 and 2400 < int(channel) <= 2422:
            channel_naj = int(channel) + 50
        elif int(bw) == 20 and 2462 <= int(channel) < 2483.5:
            channel_naj = int(channel) - 50
        elif int(bw) == 20:
            if 5100 < int(channel) < 5250 or 5500 <= int(channel) <= 5600 or 5745 <= int(channel) <= 5785:
                channel_naj = int(channel) + 40
            elif 5250 < int(channel) <= 5320 or 5600 < int(channel) < 5745 or 5785 < int(channel) <= 5825:
                channel_naj = int(channel) - 40
        elif int(bw) == 40:
            if 5100 < int(channel) < 5250 or 5500 <= int(channel) <= 5600 or 5745 <= int(channel) <= 5785:
                channel_naj = int(channel) + 80
            elif 5250 < int(channel) <= 5320 or 5600 < int(channel) < 5745 or 5785 < int(channel) <= 5825:
                channel_naj = int(channel) - 80
        elif int(bw) == 80:
            if 5100 < int(channel) < 5250 or 5500 <= int(channel) <= 5600:
                channel_naj = int(channel) + 160
            elif 5250 < int(channel) <= 5320 or 5600 < int(channel) < 5745 or 5745 < int(channel) <= 5825:
                channel_naj = int(channel) - 160
        elif int(bw) == 160:
            if 5100 < int(channel) < 5500:
                channel_naj = int(channel) + 320
            elif 5500 < int(channel) <= 5825:
                channel_naj = int(channel) - 320
        else:
            logger.info('Test Channel is not right! No adjacent channel!')
            return False
        channels = channel_naj * 1000000
        self.instance.write('%sVSG%s;FREQ:cent %d' % (mw, IQ_ROUT, channels))
        if int(bw) > 80:
            sampling_rate = 240000000
        else:
            sampling_rate = 160000000
        self.instance.write('%sVSA%s;SRAT %d' % (mw, IQ_ROUT, sampling_rate))
        # rlevel = start + loss
        logger.debug(rlevel)
        self.instance.write('%sVSG%s;POW:lev %d' % (mw, IQ_ROUT, rlevel))
        # wave = 'OFDM-6'
        if mode == '11b' and rates == '1':
            wave = 'DSSS-1'
        elif mode == '11b' and rates == '2':
            wave = 'DSSS-2L'
        elif mode == '11b' and rates == '5.5':
            wave = 'CCK-5_5S'
        elif mode == '11b' and rates == '11':
            wave = 'CCK-11S'
        elif mode == '11g' or mode == '11a':
            wave = 'OFDM-' + rates
        elif mode == '11ng' or mode == '11na':
            wave = 'HT' + bw + '_MCS' + rates
        elif mode == '11ac':
            wave = '11AC_VHT' + bw + '_S1_MCS' + rates
        elif mode == '11ax':
            wave = '11AX_HE' + bw + '_S1_HE' + rates
        # logger.info(wave)
        self.instance.write('VSG1; WAVE:LOAD "/user/WiFi_%s.iqvsg"' % wave)
        self.instance.write('VSG1;WAVE:EXEC ON')
        self.instance.write('VSG1;POW:STAT ON')
        self.instance.write('VSG1;MOD:STAT ON')

    def vsg_off(self):
        self.instance.write('VSG1 ;WAVE:EXEC OFF')

    def mimo_port(self):
        # reset port
        self.instance.write('SYS;MROUT:DEL;SYS;MVSA:DEL;SYS;MVSG:DEL')
        # reset settings
        self.instance.write('WiFi;MRST')
        # 2x2 mimo for 80M(JUST FOR IQXEL160)
        self.instance.write('MVSA:DEF:ADD VSA1;MVSA:DEF:ADD VSA12;MROUT:DEF:ADD ROUT1;MROUT:DEF:ADD ROUT12')
        self.instance.write('MROUT1;PORT:RES RF1,VSA11;MROUT2;PORT:RES RF2,VSA12')
        # other
        self.instance.write('AMOD?')

    def vsa_mimo(self, mode, bw, rates, channel, target_power):
        self.instance.write('CHAN1;WIFI')
        self.instance.write('MVSAAL;TRIG:SOUR VIDeo')
        logger.debug(channel)
        channels = int(channel) * 1000000
        logger.debug(channels)
        self.instance.write('MVSAAL;FREQ:cent %s' % str(channels))
        if RL == '1':
            self.instance.write('MVSAAL;RLEVel:AUTO' % IQ_ROUT)
        else:
            rlevel = target_power + 12
            logger.debug(str(rlevel))
            self.instance.write('MVSAAL;RLEV %d;*wai;*opc?' % rlevel)
        if int(bw) > 80:
            sampling_rate = 240000000
        else:
            sampling_rate = 160000000
        self.instance.write('MVSAAL;SRAT %d' % sampling_rate)
        if mode == '11n':
            capture_time = (12 - float(rates) * 10 / 7) / 1000
            standard = 'OFDM'
            mask_limit = 'AUTO'
        elif mode == '11ac':
            capture_time = (8 - float(rates) * 2 / 3) / 1000
            standard = 'OFDM'
            mask_limit = 'AUTO'
        elif mode == '11ax':
            capture_time = (9 - float(rates) * 2 / 3) / 1000
            standard = 'OFDM'
            mask_limit = '11AX'
        else:
            capture_time = 10
            standard = 'OFDM'
            mask_limit = 'AUTO'
        if mode == '11n' and EVM_N == '1':
            channel_estimation = 'DATA'
        elif mode == '11ac' and EVM_AC == '1':
            channel_estimation = 'DATA'
        elif mode == '11ax' and EVM_AX == '1':
            channel_estimation = 'DATA'
        else:
            channel_estimation = 'LTF'
        logger.debug('Captime: ' + str(capture_time))
        self.instance.write('CHAN1;WIFI;CONF:STAN %s' % standard)
        self.instance.write('CHAN1;WIFI;CONF:OFDM:CEST %s' % channel_estimation)
        self.instance.write('CHAN1;WIFI;CONF:SPEC:HLIM:TYPE %s' % mask_limit)
        self.instance.write('MVSAALL;CAPT:TIME %s' % capture_time)

    def analysis_mimo(self):
        """
        let iq get the data and analysis
        :return:
        """
        logger.debug('MIMO')
        self.instance.write('CHAN1')
        self.instance.write('MVSAALL ;MVSGALL:INST:COUN 1;MVSAALL:INST:COUN 1;init')
        self.instance.write('WIFI')
        status_pwr = self.instance.write('calc:pow 0, 2;*wai;*opc?')
        time.sleep(1)
        status_txq = self.instance.write('calc:txq 0, 2;*wai;*opc?')
        time.sleep(1)
        status_ccdf = self.instance.write('calc:ccdf 0, 2;*wai;*opc?')
        status_ramp = self.instance.write('calc:ramp 0, 2;*wai;*opc?')
        status_spec = self.instance.write('calc:spec 0, 2;*wai;*opc?')
        status = 0
        while status_pwr != '1' or status_txq != '1' or status_spec != '1' or status_ramp != '1' or status_ccdf != '1':
            status_pwr = self.instance.write('calc:pow 0, 2;*wai;*opc?')
            time.sleep(1)
            status_txq = self.instance.write('calc:txq 0, 2;*wai;*opc?')
            time.sleep(1)
            status_ccdf = self.instance.write('calc:ccdf 0, 2;*wai;*opc?')
            status_ramp = self.instance.write('calc:ramp 0, 2;*wai;*opc?')
            status_spec = self.instance.write('calc:spec 0, 2;*wai;*opc?')
            logger.debug(status_pwr)
            status += 1
            if status > 2:
                logger.error('No capture data for segment!')
                break


if __name__ == '__main__':
    iq = IQxel('192.168.100.253')
    mw = iq.read_idn
    iq.set_pathloss('pathloss.csv')
    iq.use_pathloss(mw, '0')
    iq.vsa(mw, '11n', '20', '6', '5180', '20')
    iq.analysis()
    iq.close()
