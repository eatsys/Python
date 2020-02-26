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

    def freq(self, channel):
        channels = float(channel)*1000000
        self.instance.write('FREQ:FIX %sHz' % channels)

    def amptd(self, pathloss, amp):
        self.instance.write('POW:OFFS %sdBm' % pathloss)
        self.instance.write('POW %sdBm' % str(amp))

    def rf_on(self):
        self.instance.write('OUTP ON')

    def rf_off(self):
        self.instance.write('OUTP OFF')

    def mod_on(self, wave):
        self.instance.write('RAD:ARB:WAV %s' % wave)
        self.instance.write('RAD:ARB ON')
        self.instance.write('OUTP:MOD ON')

    def mod_off(self):
        self.instance.write('OUTP:MOD OFF')


if __name__ == '__main__':
    sg = SG('192.168.1.240')
    sg.reset()
    sg.read_idn
    sg.freq(2412)
    sg.amptd(5, 8)
    sg.rf_on()
    sg.mod_off()
    sg.mod_on('"TDD_ETM31_20M.WFM"')
    sg.close()


