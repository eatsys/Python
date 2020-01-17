#!/user/bin/env python
# encoding: utf-8
#@time      : 2019/11/14 15:09

__author__ = 'Ethan'

import time
from colorama import init, Fore, Style
from parameters import IQ_PORT, IQ_ROUT, EVM_AG, EVM_N, EVM_AC, EVM_AX, RX_PACKETS, RL
import visa
import csv
import logging
logger = logging.getLogger()
now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
# logger.debug(now_time)
logger.setLevel(logging.DEBUG)  # logger的总开关，只有大于Debug的日志才能被logger对象处理

# 第二步，创建一个handler，用于写入日志文件
file_handler = logging.FileHandler('./log/log_' + now_time + '.txt', mode='w')
file_handler.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
# 创建该handler的formatter
file_handler.setFormatter(
    logging.Formatter(
        fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
)
# 添加handler到logger中
logger.addHandler(file_handler)

# 第三步，创建一个handler，用于输出到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # 输出到控制台的log等级的开关
# 创建该handler的formatter
console_handler.setFormatter(
    logging.Formatter(
        fmt='%(asctime)s - %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
)
logger.addHandler(console_handler)


def __isset__(v: object) -> object:
    try:
        type(eval(v))
    except Exception as error:
        return 0
    else:
        return 1


class IQxel():
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
                    pathloss = path_loss[path+1]
                    logger.debug(pathloss)
                    self.instance.write('MEM:TABLE "' + str(path) + '";MEMory:TABLe:INSert:POINt %s MHz,%s' %
                                            (channel, pathloss))
                self.instance.write('MEMory:TABLe "' + str(path) + '";MEMory:TABLe:STORe')

    def use_pathloss(self, mw):
        self.instance.write('%sVSA%s;RFC:USE "%s",RF%s' % (mw, IQ_ROUT, chain, IQ_PORT))
        self.instance.write('%sVSA%s;RFC:STAT  ON,RF%s' % (mw, IQ_ROUT, IQ_PORT))
        self.instance.write('%sVSG%s;RFC:USE "%s",RF%s' % (mw, IQ_ROUT, chain, IQ_PORT))
        self.instance.write('%sVSG%s;RFC:STAT  ON,RF%s' % (mw, IQ_ROUT, IQ_PORT))

    def vsa(self, mw):
        # print(mw, IQ_ROUT, IQ_PORT, IQ_ROUT)
        self.instance.write('%sROUT%s;PORT:RES RF%s,VSA%s' % (mw, IQ_ROUT, IQ_PORT, IQ_ROUT))
        self.instance.write('CHAN1;WIFI')
        self.instance.write('VSA1;TRIG:SOUR VIDeo')
        logger.debug(channel)
        channels = int(channel) * 1000000
        logger.debug(channels)
        self.instance.write('%sVSA%s;FREQ:cent %s' % (mw, IQ_ROUT, str(channels)))
        if RL == '1':
            self.instance.write('%sVSA%s;RLEVel:AUTO' % (mw, IQ_ROUT))
        else:
            rlevel = target_power + 12
            logger.debug(str(rlevel))
            self.instance.write('%sVSA%s;RLEV %d;*wai;*opc?' % (mw, IQ_ROUT, rlevel))
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
            capture_time = 10
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

    def analysis(self):
        """
        let iq get the data and analysis
        :return:
        """
        if mode == '11b':
            logger.debug('DSSS')
            self.instance.write('CHAN1')
            self.instance.write('VSA%s ;init' % IQ_ROUT)
            self.instance.write('WIFI')
            self.instance.write('calc:pow 0, 2')
            time.sleep(1)
            self.instance.write('calc:txq 0, 2')
            time.sleep(1)
            self.instance.write('calc:ccdf 0, 2')
            self.instance.write('calc:ramp 0, 2')
            self.instance.write('calc:spec 0, 2')
            self.instance.query('WIFI;FETC:SEGM:POW:AVER?')
        else:
            logger.debug('OFDM')
            self.instance.write('CHAN1')
            self.instance.write('VSA%s ;init' % IQ_ROUT)
            self.instance.write('WIFI')
            self.instance.write('calc:pow 0, 2')
            time.sleep(1)
            self.instance.write('calc:txq 0, 2')
            time.sleep(1)
            self.instance.write('calc:ccdf 0, 2')
            self.instance.write('calc:ramp 0, 2')
            self.instance.write('calc:spec 0, 2')
            self.instance.query('WIFI;FETC:SEGM:POW:AVER?')

    def get_status(self):
        """
        get the data and check
        :return:
        """
        time.sleep(1)
        data_pwr = self.instance.query_ascii_values('WIFI;FETC:SEGM:POW:AVER?')
        if mode == '11b':
            data_txq = self.instance.query_ascii_values('WIFI;FETC:SEGM:TXQ:DSSS:AVER?')
            txqlen = 10
        else:
            data_txq = self.instance.query_ascii_values('WIFI;FETC:SEGM:TXQ:OFDM:AVER?')
            txqlen = 8
        pwr_len = len(data_pwr)
        txq_len = len(data_txq)
        logger.debug(data_pwr)
        logger.debug(pwr_len)
        logger.debug(data_txq)
        logger.debug(txq_len)
        status = 0
        while pwr_len != 2 or txq_len != txqlen:
            self.analysis()
            data_pwr = self.instance.query_ascii_values('WIFI;FETC:SEGM:POW:AVER?')
            if mode == '11b':
                data_txq = self.instance.query_ascii_values('WIFI;FETC:SEGM:TXQ:DSSS:AVER?')
            else:
                data_txq = self.instance.query_ascii_values('WIFI;FETC:SEGM:TXQ:OFDM:AVER?')
            pwr_len = len(data_pwr)
            txq_len = len(data_txq)
            logger.debug(data_pwr)
            logger.debug(pwr_len)
            logger.debug(data_txq)
            logger.debug(txq_len)
            status += 1
            if status > 2:
                break
        return pwr_len, txq_len, data_pwr, data_txq

    def get_data(self, pwr_len, txq_len, data_pwr, data_txq, mode, channel, rate, chain, result_name, targetpower,
                 spec_pwr, gain, spec_evm, evm_margin, spec_symbol_clock_error, spec_lo_leakage, spec_mask,
                 spec_obw_20M, spec_obw_40M, spec_obw_80M, spec_obw_160M):
        """
        get the test data and write to report
        :param pwr_len:
        :param txq_len:
        :param data_pwr:
        :param data_txq:
        :param mode:
        :param channel:
        :param rate:
        :param chain:
        :param tx_result_name:
        :param target_power:
        :param spec_pwr:
        :param pwra_paras:
        :param spec_evm:
        :param evm_margin:
        :param spec_symbol_clock_error:
        :param spec_lo_leakage:
        :param spec_mask:
        :param spec_obw_20M:
        :param spec_obw_40M:
        :param spec_obw_80M:
        :return:
        """
        if mode == '11b':
            if pwr_len < 2:
                logger.error('Error: ' + str(data_pwr))
                avg_power = 'NA'
                result_pwr = 'NA'
            else:
                # logger.debug(data_pwr)
                avg_power = data_pwr[1]
                logger.debug(avg_power)
                avg_power = self.__formats__(avg_power)
                delta_pwr = abs(float(avg_power) - target_power)
                logger.debug(delta_pwr)
                # spec_pwr = 2
                if delta_pwr > spec_pwr:
                    logger.info('Power:               ' + Fore.RED + avg_power + Style.RESET_ALL + 'dBm')
                    result_pwr = 'Fail'
                else:
                    logger.info('Power:               ' + Fore.BLUE + avg_power + Style.RESET_ALL + 'dBm')
                    result_pwr = 'Pass'
            # txquality
            if txq_len < 10:
                logger.error('Error:' + str(data_txq))
                avg_evm = 'NA'
                result_evm = 'NA'
                symbol_clock_error = 'NA'
                result_symbol_clock_error = 'NA'
                lo_leakage = 'NA'
                result_lo_leakage = 'NA'
            else:
                avg_evm = data_txq[1]
                avg_evm = self.__formats__(avg_evm)
                peak_evm = data_txq[2]
                peak_evm = self.__formats__(peak_evm)
                freq_error = data_txq[4]
                freq_error = self.__formats__(freq_error)
                peak_freq_error = data_txq[5]
                peak_freq_error = self.__formats__(peak_freq_error)
                symbol_clock_error = data_txq[6]
                symbol_clock_error = self.__formats__(symbol_clock_error)
                lo_leakage = data_txq[7]
                lo_leakage = self.__formats__(lo_leakage)
                # rate = rate + 'EVM'
                spec_evm = spec_evm - evm_margin
                if float(avg_evm) > spec_evm:
                    logger.info('EVM:                 ' + Fore.RED + avg_evm + Style.RESET_ALL + 'dB')
                    result_evm = 'Fail'
                else:
                    logger.info('EVM:                 ' + Fore.BLUE + avg_evm + Style.RESET_ALL + 'dB')
                    result_evm = 'Pass'
                logger.info('EVM Peak:            ' + peak_evm + 'dB')
                logger.info('Frequency Error:     ' + freq_error + 'kHz')
                logger.info('Frequency Error Peak:' + peak_freq_error + 'kHz')
                # spec_symbol_clock_error = eval('target_evm_'+rate)
                if abs(float(symbol_clock_error)) > abs(float(spec_symbol_clock_error)):
                    logger.info('Symbol Clock Error:  ' + Fore.RED + symbol_clock_error + Style.RESET_ALL + 'ppm')
                    result_symbol_clock_error = 'Fail'
                else:
                    logger.info('Symbol Clock Error:  ' + Fore.BLUE + symbol_clock_error + Style.RESET_ALL + 'ppm')
                    result_symbol_clock_error = 'Pass'
                # spec_lo_leakage = -15
                if abs(float(lo_leakage)) < abs(float(spec_lo_leakage)):
                    logger.info('LO Leakage:          ' + Fore.RED + lo_leakage + Style.RESET_ALL + 'dB')
                    result_lo_leakage = 'Fail'
                else:
                    logger.info('LO Leakage:          ' + Fore.BLUE + lo_leakage + Style.RESET_ALL + 'dB')
                    result_lo_leakage = 'Pass'
            # mask
            data_mask = self.instance.query_ascii_values('WIFI;FETC:SEGM:SPEC:AVER:VIOL?')
            time.sleep(time.sleep_time)
            logger.debug(data_mask)
            data_mask_len = len(data_mask)
            logger.debug(data_mask_len)
            if data_mask_len != 2:
                logger.error('Error: ' + str(data_mask))
                mask = 'NA'
                result_mask = 'NA'
            else:
                # logger.debug(data_mask)
                mask = data_mask[1]
                mask = self.__formats__(mask)
                # spec_mask = 5.12
                if abs(float(mask)) > spec_mask:
                    logger.info('Mask:                ' + Fore.RED + mask + Style.RESET_ALL + '%')
                    result_mask = 'Fail'
                else:
                    logger.info('Mask:                ' + Fore.BLUE + mask + Style.RESET_ALL + '%')
                    result_mask = 'Pass'
            # OBW
            data_obw = self.instance.query_ascii_values('WIFI;FETC:SEGM:SPEC:AVER:OBW?')
            time.sleep(time.sleep_time)
            logger.debug(data_obw)
            spec_obw = spec_obw_20M
            data_obw_len = len(data_obw)
            logger.debug(data_obw_len)
            if data_obw_len != 4:
                logger.error('Error: ' + str(data_obw))
                obw = 'NA'
                result_obw = 'NA'
            else:
                # logger.debug(data_obw)
                obw = data_obw[1]
                obw = self.__formats__(obw)
                obw = round(float(obw) / 1000000, 3)
                if obw > spec_obw:
                    logger.info('OBW:                 ' + Fore.RED + str(obw) + Style.RESET_ALL + 'MHz')
                    result_obw = 'Fail'
                else:
                    logger.info('OBW:                 ' + Fore.BLUE + str(obw) + Style.RESET_ALL + 'MHz')
                    result_obw = 'Pass'
            # RAMP
            # on time
            data_ontime = self.instance.query_ascii_values('WIFI;FETC:SEGM:RAMP:ON:TRIS?')
            time.sleep(time.sleep_time)
            logger.debug(data_ontime)
            spec_ramp_on_time = 2.0
            data_ontime_len = len(data_ontime)
            logger.debug(data_ontime_len)
            if data_ontime_len < 4:
                logger.error('Error: ' + str(data_ontime))
                ramp_on_time = 'NA'
                result_ramp_on_time = 'NA'
            else:
                # logger.debug(data_ontime)
                ramp_on_time = data_ontime[1]
                ramp_on_time = float(ramp_on_time) * 1000000
                ramp_on_time = self.__formats__(ramp_on_time)
                if float(ramp_on_time) > spec_ramp_on_time:
                    logger.info('Ramp On Time:        ' + Fore.RED + ramp_on_time + Style.RESET_ALL + 'us')
                    result_ramp_on_time = 'Fail'
                else:
                    logger.info('Ramp On Time:        ' + Fore.BLUE + ramp_on_time + Style.RESET_ALL + 'us')
                    result_ramp_on_time = 'Pass'
            # off time
            data_offtime = self.instance.query_ascii_values('WIFI;FETC:SEGM:RAMP:OFF:TRIS?')
            time.sleep(time.sleep_time)
            logger.debug(data_offtime)
            spec_ramp_off_time = 2.0
            data_offtime_len = len(data_offtime)
            logger.debug(data_offtime_len)
            if data_offtime_len < 4:
                logger.error('Error: ' + str(data_offtime))
                ramp_off_time = 'NA'
                result_ramp_off_time = 'NA'
            else:
                # logger.debug(data_offtime)
                ramp_off_time = data_offtime[1]
                ramp_off_time = float(ramp_off_time) * 1000000
                ramp_off_time = self.__formats__(ramp_off_time)
                if float(ramp_off_time) > spec_ramp_off_time:
                    logger.info('Ramp Off Time:       ' + Fore.RED + ramp_off_time + Style.RESET_ALL + 'us')
                    result_ramp_off_time = 'Fail'
                else:
                    logger.info('Ramp Off Time:       ' + Fore.BLUE + ramp_off_time + Style.RESET_ALL + 'us')
                    result_ramp_off_time = 'Pass'
            flasness = 'NA'
            spec_flasness = 'NA'
            result_flasness = 'NA'

        else:
            logger.debug('OFDM')
            if pwr_len < 2:
                logger.error('Error: ' + str(data_pwr))
                avg_power = 'NA'
                result_pwr = 'NA'
            else:
                # logger.debug(data)
                avg_power = data_pwr[1]
                avg_power = self.__formats__(avg_power)
                delta_pwr = abs(float(avg_power) - target_power)
                logger.debug(delta_pwr)
                ##spec_pwr = 2
                if delta_pwr > spec_pwr:
                    logger.info('Power:               ' + Fore.RED + avg_power + Style.RESET_ALL + 'dBm')
                    result_pwr = 'Fail'
                else:
                    logger.info('Power:               ' + Fore.BLUE + avg_power + Style.RESET_ALL + 'dBm')
                    result_pwr = 'Pass'
            # txquality
            if txq_len < 8:
                logger.error('Error: ' + str(data_txq))
                avg_evm = 'NA'
                result_evm = 'NA'
                symbol_clock_error = 'NA'
                result_symbol_clock_error = 'NA'
                lo_leakage = 'NA'
                result_lo_leakage = 'NA'
            else:
                logger.debug(data_txq)
                avg_evm = data_txq[1]
                avg_evm = self.__formats__(avg_evm)
                freq_error = data_txq[3]
                freq_error = self.__formats__(freq_error)
                symbol_clock_error = data_txq[4]
                symbol_clock_error = self.__formats__(symbol_clock_error)
                lo_leakage = data_txq[5]
                lo_leakage = self.__formats__(lo_leakage)
                spec_evm = spec_evm - abs(evm_margin)
                # logger.info(spec_evm)
                if float(avg_evm) > spec_evm:
                    logger.info('EVM:                 ' + Fore.RED + avg_evm + Style.RESET_ALL + 'dB')
                    result_evm = 'Fail'
                else:
                    logger.info('EVM:                 ' + Fore.BLUE + avg_evm + Style.RESET_ALL + 'dB')
                    result_evm = 'Pass'
                logger.info('Frequency Error:     ' + freq_error + 'kHz')
                # spec_symbol_clock_error = 10.0
                if abs(float(symbol_clock_error)) > abs(float(spec_symbol_clock_error)):
                    logger.info('Symbol Clock Error:  ' + Fore.RED + symbol_clock_error + Style.RESET_ALL + 'ppm')
                    result_symbol_clock_error = 'Fail'
                else:
                    logger.info('Symbol Clock Error:  ' + Fore.BLUE + symbol_clock_error + Style.RESET_ALL + 'ppm')
                    result_symbol_clock_error = 'Pass'
                # spec_lo_leakage = -15
                if abs(float(lo_leakage)) < abs(float(spec_lo_leakage)):
                    logger.info('LO Leakage:          ' + Fore.RED + lo_leakage + Style.RESET_ALL + 'dB')
                    result_lo_leakage = 'Fail'
                else:
                    logger.info('LO Leakage:          ' + Fore.BLUE + lo_leakage + Style.RESET_ALL + 'dB')
                    result_lo_leakage = 'Pass'
            # mask
            data_mask = self.instance.query_ascii_values('WIFI;FETC:SEGM:SPEC:AVER:VIOL?')
            time.sleep(time.sleep_time)
            logger.debug(data_mask)
            data_mask_len = len(data_mask)
            logger.debug(data_mask_len)
            if data_mask_len != 2:
                logger.error('Error: ' + str(data_mask))
                mask = 'NA'
                result_mask = 'NA'
            else:
                # logger.debug(data_mask)
                mask = data_mask[1]
                mask = self.__formats__(mask)
                # spec_mask = 5.12
                if abs(float(mask)) > spec_mask:
                    logger.info('Mask:                ' + Fore.RED + mask + Style.RESET_ALL + '%')
                    result_mask = 'Fail'
                else:
                    logger.info('Mask:                ' + Fore.BLUE + mask + Style.RESET_ALL + '%')
                    result_mask = 'Pass'
            # OBW
            data_obw = self.instance.query_ascii_values('WIFI;FETC:SEGM:SPEC:AVER:OBW?')
            time.sleep(time.sleep_time)
            logger.debug(data_obw)
            if bw == '80':
                spec_obw = spec_obw_80M
            elif bw == '40':
                spec_obw = spec_obw_40M
            elif bw == '20':
                spec_obw = spec_obw_20M
            else:
                spec_obw = spec_obw_160M
            data_obw_len = len(data_obw)
            logger.debug(data_obw_len)
            if data_obw_len != 4:
                logger.error('Error: ' + str(data_obw))
                obw = 'NA'
                result_obw = 'NA'
            else:
                # logger.debug(data_obw)
                obw = data_obw[1]
                obw = self.__formats__(obw)
                obw = round(float(obw) / 1000000, 3)
                if obw > spec_obw:
                    logger.info('OBW:                 ' + Fore.RED + str(obw) + Style.RESET_ALL + 'MHz')
                    result_obw = 'Fail'
                else:
                    logger.info('OBW:                 ' + Fore.BLUE + str(obw) + Style.RESET_ALL + 'MHz')
                    result_obw = 'Pass'
            # flasness
            # datas = self.instance.query('FETC:SEGM1:OFDM:SFL:SIGN1:AVER?')
            # time.sleep(time.sleep_time)
            # time.sleep(10)
            # logger.info('flasness', datas)
            data_flasness = self.instance.query('WIFI;FETC:SEGM:OFDM:SFL:AVER:CHEC?')
            # data_flasness = self.query('WIFI;FETC:SEGM:OFDM:SFL:AVER?')
            time.sleep(time.sleep_time)
            logger.debug(data_flasness)
            data_flasness = data_flasness.split(',')
            spec_flasness = 0
            data_flasness_len = len(data_flasness)
            logger.debug(data_flasness_len)
            if data_flasness_len < 2:
                logger.error('Error: ' + str(data_flasness))
                flasness = 'NA'
                result_flasness = 'NA'
            else:
                # logger.debug(data_flasness)
                flasness = data_flasness[0]
                if int(flasness) == spec_flasness:
                    logger.info('Flasness:            ' + Fore.BLUE + flasness + Style.RESET_ALL)
                    result_flasness = 'Pass'
                else:
                    logger.info('Flasness:            ' + Fore.RED + flasness + Style.RESET_ALL)
                    result_flasness = 'Fail'
            ramp_on_time = 'NA'
            spec_ramp_on_time = 'NA'
            result_ramp_on_time = 'NA'
            ramp_off_time = 'NA'
            spec_ramp_off_time = 'NA'
            result_ramp_off_time = 'NA'

        if super_mode == '1' and avg_power != 'NA':
            if float(avg_power) < float(power_accuracy_left) or float(avg_power) > float(power_accuracy_right):
                logger.info('Adjust power')
            else:
                with open('./Result/' + result_name, 'a+', newline='') as write_result:
                    writer_file = csv.writer(write_result)
                    writer_file.writerow(
                        [channel, rate, chain, target_power, avg_power, pwra_paras, spec_pwr, result_pwr,
                         avg_evm, spec_evm, result_evm, symbol_clock_error, spec_symbol_clock_error,
                         result_symbol_clock_error, lo_leakage, spec_lo_leakage, result_lo_leakage, obw,
                         spec_obw, result_obw, mask, spec_mask, result_mask, flasness, spec_flasness,
                         result_flasness, ramp_on_time, spec_ramp_on_time, result_ramp_on_time,
                         ramp_off_time, spec_ramp_off_time, result_ramp_off_time])
        else:
            with open('./Result/' + result_name, 'a+', newline='') as write_result:
                writer_file = csv.writer(write_result)
                writer_file.writerow([channel, rate, chain, target_power, avg_power, pwra_paras, spec_pwr, result_pwr,
                                      avg_evm, spec_evm, result_evm, symbol_clock_error, spec_symbol_clock_error,
                                      result_symbol_clock_error, lo_leakage, spec_lo_leakage, result_lo_leakage, obw,
                                      spec_obw, result_obw, mask, spec_mask, result_mask, flasness, spec_flasness,
                                      result_flasness, ramp_on_time, spec_ramp_on_time, result_ramp_on_time,
                                      ramp_off_time, spec_ramp_off_time, result_ramp_off_time])

        return avg_power, result_evm, result_symbol_clock_error, result_lo_leakage, result_mask

    def get_power(self):
        """
        just for calibration, only for power calibration
        :return:
        """
        if pwr_len < 2:
            logger.error('Error: ' + str(data_pwr))
            avg_power = 'NA'
        else:
            # logger.debug(data_pwr)
            avg_power = data_pwr[1]
            logger.debug(avg_power)
            avg_power = self.__formats__(avg_power)
            delta_pwr = abs(float(avg_power) - target_power)
            logger.debug(delta_pwr)
            spec_pwr = 2
            if delta_pwr > spec_pwr:
                logger.info('Power:               ' + Fore.RED + avg_power + Style.RESET_ALL + 'dBm')
            else:
                logger.info('Power:               ' + Fore.BLUE + avg_power + Style.RESET_ALL + 'dBm')
        return avg_power

    def get_ppm(self):
        """
        just for calibration, for ppm calibration only
        :return:
        """
        # txquality
        if txq_len < 8:
            logger.error('Error: ' + str(data_txq))
            avg_evm = 'NA'
            result_evm = 'NA'
            symbol_clock_error = 'NA'
            result_symbol_clock_error = 'NA'
            lo_leakage = 'NA'
            result_lo_leakage = 'NA'
        else:
            logger.debug(data_txq)
            symbol_clock_error = data_txq[4]
            symbol_clock_error = self.__formats__(symbol_clock_error)
            spec_symbol_clock_error = 5.0
            if abs(float(symbol_clock_error)) > abs(float(spec_symbol_clock_error)):
                logger.info('Symbol Clock Error:  ' + Fore.RED + symbol_clock_error + Style.RESET_ALL + 'ppm')
            else:
                logger.info('Symbol Clock Error:  ' + Fore.BLUE + symbol_clock_error + Style.RESET_ALL + 'ppm')
        return symbol_clock_error

    def vsg(self, mw, rlevel):
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
        elif mode == '11ng' or mode == '11na':
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

    def vsg_aj(self, mw, rlevel):
        self.instance.write('%sROUT%s;PORT:RES RF%s,VSG%s' % (mw, IQ_ROUT_INTERFERE, IQ_PORT_INTERFERE, IQ_ROUT_INTERFERE))
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

    def vsg_naj(self, mw, rlevel):
        self.instance.write('%sROUT%s;PORT:RES RF%s,VSG%s' % (mw, IQ_ROUT_INTERFERE, IQ_PORT_INTERFERE, IQ_ROUT_INTERFERE))
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


if __name__ == '__main__':
    iq = IQxel('192.168.100.254')
    chain = '0'
    mw = iq.read_idn
    iq.set_pathloss()
    #iq.use_pathloss(mw)
