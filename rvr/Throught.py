__author__ = 'DVTRF'

import os
import data.write_datas
from data.parameters import AP_TYPE, RADIO, CHANNEL, ANGLE_NUM, ANGLE_LIST, ATTENUATE_LIST, DURA_TIME
import re
import logging
logger = logging.getLogger()

retval = os.getcwd()
result_file = retval + '/Result/IxChariotOD/' + AP_TYPE + '_' + RADIO + '/'


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
                logger.error(err)
            else:
                result = f.read()
                txthrought = re.sub(',', '', (re.findall(r'Totals:\s+\d.+', result)[0].split()[1].encode("ascii")).decode("utf-8"))
                #print(txthrought)
                data.write_datas.tx_tp_wirte(txthrought)
                logger.info("tx_throught is    : {0} ".format(txthrought))
                #print(txthrought)
                f.close()

    def get_rx_throught(self):
        for rx_data in self.RX:
            try:
                file_path = result_file + rx_data
                f = open(file_path, "r")
            except Exception as err:
                logger.error(err)
            else:
                result = f.read()
                rxthrought = re.sub(',', '', re.findall(r'Totals:\s+\d.+', result)[0].split()[1].encode("ascii").decode('utf-8'))
                data.write_datas.rx_tp_write(rxthrought)
                logger.info("rx_throught is    : {0} ".format(rxthrought))
                #print(rxthrought)
                f.close()

    def get_tx_throught_simple(self):
        try:
            file_path = result_file + self.TX
            #print('33', file_path)
            f = open(file_path, "r")
            #print('44', f)
        except Exception as err:
            logger.error(err)
        else:
            result = f.read()
            txthrought = re.sub(',', '', (re.findall(r'Totals:\s+\d.+', result)[0].split()[1].encode("ascii")).decode("utf-8"))
            #print(txthrought)
            data.write_datas.tx_tp_wirte(txthrought)
            logger.info("tx_throught is    : {0} ".format(txthrought))
            #data.write_datas.test_time_write(DURA_TIME)
            #print(txthrought)
            f.close()

    def get_rx_throught_simple(self):
        try:
            file_path = result_file + self.RX
            f = open(file_path, "r")
        except Exception as err:
            logger.error(err)
        else:
            result = f.read()
            rxthrought = re.sub(',', '', re.findall(r'Totals:\s+\d.+', result)[0].split()[1].encode("ascii").decode('utf-8'))
            data.write_datas.rx_tp_write(rxthrought)
            logger.info("rx_throught is    : {0} ".format(rxthrought))
            data.write_datas.test_time_write(DURA_TIME)
            #print(rxthrought)
            f.close()


# for print  throught to gui
def tx_throught(i):
    try:
        tx_path = result_file + " " + str(i) + "_Tx.txt"
        f_tx = open(tx_path, "r")
    except:
        logger.error("fail to open test result")
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
        logger.error("fail to open test result")
    try:
        rx_result = f_rx.read()
        rx = re.findall(r'Totals:\s+\d.+', rx_result)[0].split()[1].encode("ascii").decode("ascii")
    except:
        pass
    finally:
        f_rx.close()


# gen file name
def Generate_TP_To_Txt():
    if ANGLE_NUM == 1:
        for i in ATTENUATE_LIST:
            for angle in [0]:
                RX = []
                TX = []
                rx = RADIO + "_" + CHANNEL + "_" + str(i) + "_" + str(angle) + "_Rx.txt"
                tx = RADIO + "_" + CHANNEL + "_" + str(i) + "_" + str(angle) + "_Tx.txt"
                RX.append(rx)
                TX.append(tx)
                throught = Throught(RX, TX)
                throught.get_tx_throught()
                throught.get_rx_throught()
                print('TX', TX)
                print('RX', RX)
    elif ANGLE_NUM == 4:
        for i in ATTENUATE_LIST:
            for angle in [0, 90.0, 180.0, 270.0]:
                RX = []
                TX = []
                rx = RADIO + "_" + CHANNEL + "_" + str(i) + "_" + str(angle) + "_Rx.txt"
                tx = RADIO + "_" + CHANNEL + "_" + str(i) + "_" + str(angle) + "_Tx.txt"
                RX.append(rx)
                TX.append(tx)
                throught = Throught(RX, TX)
                throught.get_tx_throught()
                throught.get_rx_throught()
                print('TX', TX)
                print('RX', RX)
    elif ANGLE_NUM == 8:
        # for i in range(ATTEN_START+LINE_LOSS,ATTEN_END+LINE_LOSS+ATTEN_STEP,ATTEN_STEP):
        for i in ATTENUATE_LIST:
            for angle in ANGLE_LIST:
                RX = []
                TX = []
                rx = f'{RADIO}_{CHANNEL}_{str(i)}_{str(angle)}_Rx.txt'
                tx = f'{RADIO}_{CHANNEL}_{str(i)}_{str(angle)}_Tx.txt'
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
