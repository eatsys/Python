#!/usr/bin/python
# -*- coding: UTF-8 -*-
import visa
import time
# start of Untitled

ip = '192.168.100.222'
rm = visa.ResourceManager()
address = 'TCPIP0::%s::inst0::INSTR' % ip
N1911A_2 = rm.open_resource(address)
serialNumber = N1911A_2.query('*IDN?')
print(serialNumber)
N1911A_2.close()
rm.close()

# end of Untitled