import visa
import time
# start of Untitled


class IQxel():
    def __init__(self, ip):
        self.ip = ip
        self.rm = visa.ResourceManager()

    def open(self):
        self.IQXEL = self.rm.open_resource('TCPIP0::%s::hislip0::INSTR' % self.ip)

    def get_data(self):
        self.IQXEL.write('ROUT1;PORT:RES RF1,VSA1')
        self.IQXEL.write('VSA1;FREQ:cent 2412000000')
        self.IQXEL.write('VSA1;SRAT 160000000')
        #self.IQXEL.write('WIFI;CLE:POW;*wai;*opc?')
        self.IQXEL.write('VSA1;CAPT:TIME 0.02')
        self.IQXEL.write('VSA1 ;RLEVel:AUTO')
        self.IQXEL.write('CHAN1')
        self.IQXEL.write('VSA1 ;init')
        self.IQXEL.write('WIFI')
        self.IQXEL.write('calc:pow 0, 10')
        retval = self.IQXEL.query('WIFI;FETC:SEGM:POW:AVER?')
        print(retval)

    def close(self):
        self.IQXEL.close()
        self.rm.close()

if __name__ == '__main__':
    iq = IQxel('192.168.100.254')
    iq.open()
    iq.get_data()
    iq.close()

# end of Untitled