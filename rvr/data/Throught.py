__author__ = 'DVTRF'

import os
from config import conf
import data.write_datas
from data.parameters import RADIO, CHANNEL, ANGLE, ATTENUATE_LIST
import re
import logging


LOG_FORMAT = "%(asctime)s - %(pathname)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

logging.basicConfig(filename='./log/log.txt', level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)

test_ap = conf.Ap_type_get()
retval = os.getcwd()
print('11', retval)
result_file = retval + '/Result/IxChariotOD/ ' + test_ap + '/'
print('22', result_file)


# for Generate test report
class Throught(object):
    def __init__(self, RX, TX):
        self.RX = RX
        self.TX = TX

    def get_tx_throught(self):
        for tx_data in self.TX:
            try:
                file_path = result_file + tx_data
                #print('33', file_path)
                f = open(file_path, "r")
                #print('44', f)
            except Exception as err:
                logging.error(err)
            else:
                result = f.read()
                txthrought = (re.findall(r'Totals:\s+\d.+', result)[0].split()[1].encode("ascii")).decode("ascii")
                #print(txthrought)
                data.write_datas.tx_tp_wirte(txthrought)
                logging.info("tx_throught is    : {0} ".format(txthrought))
                #print(txthrought)
                f.close()

    def get_rx_throught(self):
        for rx_data in self.RX:
            try:
                file_path = result_file + rx_data
                f = open(file_path, "r")
            except Exception as err:
                logging.error(err)
            else:
                result = f.read()
                rxthrought = re.findall(r'Totals:\s+\d.+', result)[0].split()[1].encode("ascii").decode('utf-8')
                data.write_datas.rx_tp_write(rxthrought)
                logging.info("rx_throught is    : {0} ".format(rxthrought))
                #print(rxthrought)
                f.close()


# for print  throught to gui
def tx_throught(i):
    try:
        tx_path = result_file + " " + str(i) + "_Tx.txt"
        f_tx = open(tx_path, "r")
    except:
        logging.error("fail to open test result")
    try:
        tx_result = f_tx.read()
        tx = re.findall(r'Totals:\s+\d.+', tx_result)[0].split()[1].encode("ascii")

    except:
        pass
    finally:
        f_tx.close()


# for print  throught to gui
def rx_throught(i):
    try:
        rx_path = result_file + " " + str(i) + "_Rx.txt"
        f_rx = open(rx_path, "r")
    except:
        logging.error("fail to open test result")
    try:
        rx_result = f_rx.read()
        rx = re.findall(r'Totals:\s+\d.+', rx_result)[0].split()[1].encode("ascii").decode("ascii")
    except:
        pass
    finally:
        f_rx.close()


# gen file name
def Generate_TP_To_Txt():
    if ANGLE == 1:
        for i in ATTENUATE_LIST:
            for angle in [0]:
                RX = []
                TX = []
                rx = " " + RADIO + "_ " + CHANNEL + "_ " + str(i) + "_ " + str(angle) + "_Rx.txt"
                tx = " " + RADIO + "_ " + CHANNEL + "_ " + str(i) + "_ " + str(angle) + "_Tx.txt"
                RX.append(rx)
                TX.append(tx)
                throught = Throught(RX, TX)
                throught.get_tx_throught()
                throught.get_rx_throught()
                print('TX', TX)
                print('RX', RX)
    elif ANGLE == 4:
        for i in ATTENUATE_LIST:
            for angle in [0, 90.0, 180.0, 270.0]:
                RX = []
                TX = []
                rx = " " + RADIO + "_ " + CHANNEL + "_ " + str(i) + "_ " + str(angle) + "_Rx.txt"
                tx = " " + RADIO + "_ " + CHANNEL + "_ " + str(i) + "_ " + str(angle) + "_Tx.txt"
                RX.append(rx)
                TX.append(tx)
                throught = Throught(RX, TX)
                throught.get_tx_throught()
                throught.get_rx_throught()
                print('TX', TX)
                print('RX', RX)
    elif ANGLE == 8:
        # for i in range(ATTEN_START+LINE_LOSS,ATTEN_END+LINE_LOSS+ATTEN_STEP,ATTEN_STEP):
        for i in ATTENUATE_LIST:
            for angle in [0, 45.0, 90.0, 135.0, 180.0, 225.0, 270.0, 315.0]:
                RX = []
                TX = []
                rx = " " + RADIO + "_ " + CHANNEL + "_ " + str(i) + "_ " + str(angle) + "_Rx.txt"
                tx = " " + RADIO + "_ " + CHANNEL + "_ " + str(i) + "_ " + str(angle) + "_Tx.txt"
                RX.append(rx)
                TX.append(tx)
                throught = Throught(RX, TX)
                throught.get_tx_throught()
                throught.get_rx_throught()
                print('TX', TX)
                print('RX', RX)


if __name__ == "__main__":

    angles = 8
    if angles == 1:
        for i in range(30, 70, 10):
            for angle in [0]:
                RX = []
                TX = []
                rx = " " + str(i) + "_" + " " + str(angle) + "_Rx.txt"
                tx = " " + str(i) + "_" + " " + str(angle) + "_Tx.txt"
                RX.append(rx)
                TX.append(tx)
                throught = Throught(RX, TX)
                throught.get_tx_throught()
                throught.get_rx_throught()
    elif angles == 4:
        for atten in range(30, 70, 10):
            for angle in [0, 90, 180, 270]:
                rx = " " + str(atten) + "_" + " " + str(angle) + "_Rx.txt"
                tx = " " + str(atten) + "_" + " " + str(angle) + "_Tx.txt"
                RX = []
                TX = []
                RX.append(rx)
                TX.append(tx)
                throught = Throught(RX, TX)
                throught.get_tx_throught()
                throught.get_rx_throught()
    elif angles == 8:
        for atten in range(30, 70, 10):
            for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
                rx = " " + str(atten) + "_" + " " + str(angle) + "_Rx.txt"
                tx = " " + str(atten) + "_" + " " + str(angle) + "_Tx.txt"
                RX = []
                TX = []
                RX.append(rx)
                TX.append(tx)
                throught = Throught(RX, TX)
                throught.get_tx_throught()
                throught.get_rx_throught()
