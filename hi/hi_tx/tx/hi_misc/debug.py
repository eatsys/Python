# -*- coding: utf-8 -*-
# @Time    : 2019/1/18 13:23
# @Author  : Ethan
# @FileName: test_set.py
import sys
import os
import socket
import datetime
import time
import telnetlib
import serial
from openpyxl import Workbook
import csv


pathloss_file = csv.reader(open('./pathloss.csv'))
next(pathloss_file)
for rows in pathloss_file:
    print rows[0]