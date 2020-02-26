#!/user/bin/env python
# encoding: utf-8
# @time      : 2020/1/14 13:50

__author__ = 'Ethan'

import visa
import logging
logger = logging.getLogger()


class SA:
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

    def save_image(self, imgname, fmt):
        """
        if save image
        :param imagname:
        :param fmt:
        :return:
        """
        assert fmt in ['jpg', 'png'], 'Invalid postfix of image'
        logger.debug('MMEM:STOR:IMAG "%s.%s"' % (imgname, fmt))
        self.instance.write('MMEM:STOR:IMAG "%s.%s"' % (imgname, fmt))

    def reset(self):
        self.instance.write('*RST')

    @property
    def read_idn(self):
        idn = self.instance.query('*IDN?')
        logger.info(idn)

    def freq(self, channel):
        self.instance.write('CCAR:REF %sMHz' % channel)

    def power(self, channel, bw):
        self.instance.write('CONF:CHP')
        self.instance.write('INIT:CHP')
        self.instance.write('CHP:AVER:COUN 15')
        self.instance.write('CCAR:REF %sMHz' % channel)
        self.instance.write('RAD:STAN:PRES B%s' % bw)
        self.instance.write('POW:RANG:OPT IMM')
        self.instance.write('INIT:CONT OFF')
        self.instance.write('INIT:REST')
        self.instance.write('CALC:DATA1?')
        self.instance.write('MMEM:STOR:SCR')

    def evm(self, channel, bw, tbl, mcs):
        self.instance.write('CONF:EVM')
        self.instance.write('INIT:EVM')
        self.instance.write('SERV:EVM:PHA:COMP 0')
        self.instance.write('CCAR:REF %sMHz' % channel)
        self.instance.write('RAD:STAN:PRES B%s' % bw)
        self.instance.write('EVM:CCAR0:NUMB:PDSC 1')
        self.instance.write('EVM:CCAR0:PDSC1:MCS:TABL TABL%s' % tbl)
        self.instance.write('EVM:CCAR0:PDSC1:MCS %s' % mcs)
        self.instance.write('EVM:CCAR0:DC:PUNC 1')
        self.instance.write('POW:EATT:STAT ON')
        self.instance.write('POW:RANG:OPT IMM')
        self.instance.write('INIT:CONT OFF')
        self.instance.write('INIT:REST')
        self.instance.write('CALC:DATA1?')
        self.instance.write('CCALC:CLIM:FAIL?')
        self.instance.write('MMEM:STOR:SCR')

    def aclr(self, channel, bw):
        self.instance.write('CONF:ACP')
        self.instance.write('INIT:ACP')
        self.instance.write('CCAR:REF %sMHz' % channel)
        self.instance.write('RAD:STAN:PRES B%s' % bw)
        self.instance.write('POW:RANG:OPT IMM')
        self.instance.write('INIT:CONT OFF')
        self.instance.write('INIT:REST')
        self.instance.write('CALC:DATA1?')
        self.instance.write('CCALC:CLIM:FAIL?')
        self.instance.write('MMEM:STOR:SCR')

    def obue(self, channel, bw):
        self.instance.write('CONF:SEM')
        self.instance.write('INIT:SEM')
        self.instance.write('SEM:AVER ON')
        self.instance.write('CCAR:REF %sMHz' % channel)
        self.instance.write('RAD:STAN:PRES B%s' % bw)
        self.instance.write('POW:RANG:OPT IMM')
        self.instance.write('INIT:CONT OFF')
        self.instance.write('INIT:REST')
        self.instance.write('CALC:DATA1?')
        self.instance.write('CCALC:CLIM:FAIL?')
        self.instance.write('MMEM:STOR:SCR')

    def obw(self, channel, bw):
        self.instance.write('CONF:OBW')
        self.instance.write('INIT:OBW')
        self.instance.write('SEM:AVER ON')
        self.instance.write('CCAR:REF %sMHz' % channel)
        self.instance.write('RAD:STAN:PRES B%s' % bw)
        self.instance.write('POW:RANG:OPT IMM')
        self.instance.write('INIT:CONT OFF')
        self.instance.write('INIT:REST')
        self.instance.write('CALC:DATA1?')
        self.instance.write('MMEM:STOR:SCR')

    def spur(self):
        self.instance.write('CONF:SPUR')
        self.instance.write('INP:COUP DC')
        self.instance.write('SPUR:AVER:COUNt 1')
        self.instance.write('POW:RF:RANGE:OPT:ATT COMB')
        self.instance.write('POW:RANGE:OPT IMM')
        self.instance.write('TRIG:SPUR:SOUR FRAM')
        self.instance.write('TRIG:FRAM:PER 10 ms')
        self.instance.write('TRIG:RFB:LEV:ABS -24.7 dBm')
        self.instance.write('SPUR:DET AVER')
        self.instance.write('SPUR:PEAK:EXC 6')
        self.instance.write('SPUR:PEAK:THReshold -130')
        self.instance.write('SPUR:STATE ON,OFF,OFF,OFF,OFF,OFF,OFF,OFF')
        self.instance.write('SPUR:BAND:RES 1KHZ')
        self.instance.write('SPUR:BAND:VID:AUTO ON')
        self.instance.write('SPUR:FREQ:START 9KHz')
        self.instance.write('SPUR:FREQ:STOP 150KHz')
        self.instance.write('CALC:SPUR:LIM:ABS:DATA -36dBm')
        self.instance.write('CALC:SPUR:LIM:ABS:DATA:STOP -36dBm')
        self.instance.write('SPUR:ATT:AUTO 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0')
        self.instance.write('SPUR:ATT 0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB,0dB')
        self.instance.write('POW:ATT 0')
        self.instance.write('INIT:CONT ON')
        self.instance.write('INIT:REST')
        self.instance.write('INIT:CONT OFF')
        self.instance.write('FETC:SPUR1?')
        self.instance.write('MMEM:STOR:SCR')
        self.instance.write('INIT:CONT ON')

    def ccdf(self, channel, bw):
        self.instance.write('CONF:PST')
        self.instance.write('PST:COUN 2000000')
        self.instance.write('CCAR:REF %sMHz' % channel)
        self.instance.write('RAD:STAN:PRES B%s' % bw)
        self.instance.write('POW:RANG:OPT IMM')
        self.instance.write('INIT:CONT OFF')
        self.instance.write('INIT:REST')
        self.instance.write('CALC:DATA1?')
        self.instance.write('MMEM:STOR:SCR')


if __name__ == '__main__':
    sa = SA('192.168.100.55')
    sa.reset()
    sa.read_idn
    sa.freq(2412)
    sa.ccdf(2412, 20)
    sa.close()
