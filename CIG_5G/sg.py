#!/user/bin/env python
# encoding: utf-8
# @time      : 2020/1/15 14:49

__author__ = 'Ethan'

import visa
import logging
logger = logging.getLogger()


class SG:
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
        logger.info(idn)

    def ss(self):
        print
        'INIT SG...'
        Host = sg_ip
        Port = 5023
        tn = telnetlib.Telnet(Host, Port, timeout=3)
        tn.set_debuglevel(0);
        tn.read_until(b"SCPI>")
        n = tn.write(b"\r\n")
        tn.read_until(b"SCPI>")
        n = tn.write(b":SYST:PRES" + b"\r\n")
        # tn.read_until(b"SCPI>")
        # n = tn.write(b":RAD:ARB:TRIG:TYPE:CONT TRIG" + b"\r\n") #设置Trigger Type
        # tn.read_until(b"SCPI>")
        # n = tn.write(b":RAD:ARB:TRIG:EXT:SLOP POS" + b"\r\n") #设置EXT Polarity
        # tn.read_until(b"SCPI>")
        # n = tn.write(b":RAD:ARB:TRIG:EXT:DEL:STAT ON" + b"\r\n") #打开时延
        # tn.read_until(b"SCPI>")
        # n = tn.write(b":RAD:ARB:TRIG:EXT:DEL 11usec" + b"\r\n") #设置时延时间
        ######################################################################
        Keysight_Set.SA(ip, type)
        ##################信号源设置########################################################
        print
        "**************** Starting Test ********************"
        n = tn.write(b"\r\n")
        tn.read_until(b"SCPI>")
        n = tn.write(b":RAD:ARB:WAV " + wavef + b"\r\n")  # 加载波形文件
        tn.read_until(b"SCPI>")
        n = tn.write(b":RAD:ARB ON" + b"\r\n")  # 打开ARB开关
        tn.read_until(b"SCPI>")
        n = tn.write(b":FREQ:FIX " + channel + "MHz" + b"\r\n")  # 配置信道
        tn.read_until(b"SCPI>")
        n = tn.write(b":OUTP:MOD ON" + b"\r\n")  # 打开mode开关
        tn.read_until(b"SCPI>")
        n = tn.write(b":OUTP ON" + b"\r\n")  # 打开RF 开关
        tn.read_until(b"SCPI>")
        n = tn.write(b":POW:OFFS " + pathloss + "dBm" + b"\r\n")
        tn.read_until(b"SCPI>")
        x = 0
        while (starf <= stopf):
            rsamp = float(starf)  ####################设置测试初始信号强度
            n = tn.write(b":POW " + str(rsamp) + "dBm" + b"\r\n")
            tn.read_until(b"SCPI>")