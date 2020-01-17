# -*- coding: utf-8 -*-
# @Time    : 2019/3/11 16:43
# @Author  : Ethan
# @FileName: pdv.py

from ctypes import *
import logging

logger = logging.getLogger()


class PDV:
    def __init__(self, port):
        self.port = port
        self.pdv = WinDLL("./vector_generator.dll")

    def open(self):
        self.pdv.SetComPortn(self.port)

    def close(self):
        self.pdv.CloseCommPort(self.port)

    def set_speed(self):
        self.pdv.SetSpeed(0, 0)

    def set_distance(self):
        self.pdv.SetDistance(0, 12800.0000)

    def set_maxspeed(self):
        self.pdv.SetMaxSpeed(0, 4096)

    def action(self):
        self.pdv.TrigJointAction(0)

    def get_display(self):
        self.pdv.GetDisplay(0)

    def get_status(self):
        self.pdv.GetStatus(0)

    def join_data(self):
        self.pdv.SetJointData(0)

    def stop(self):
        self.pdv.Stop()


if __name__ == '__main__':
    pd = PDV(11)
    pd.open()
    pd.close()
