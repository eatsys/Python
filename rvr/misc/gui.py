# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(673, 739)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(712, 814))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(206, 240, 229))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(230, 247, 242))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(103, 120, 114))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(137, 160, 153))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(206, 240, 229))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(230, 247, 242))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(206, 240, 229))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(230, 247, 242))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(103, 120, 114))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(137, 160, 153))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(206, 240, 229))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(230, 247, 242))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(103, 120, 114))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(206, 240, 229))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(230, 247, 242))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(103, 120, 114))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(137, 160, 153))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(103, 120, 114))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(103, 120, 114))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(206, 240, 229))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(206, 240, 229))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(206, 240, 229))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        MainWindow.setPalette(palette)
        MainWindow.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.APframe = QtWidgets.QFrame(self.centralwidget)
        self.APframe.setGeometry(QtCore.QRect(0, 0, 351, 241))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.APframe.setFont(font)
        self.APframe.setFrameShape(QtWidgets.QFrame.Box)
        self.APframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.APframe.setLineWidth(1)
        self.APframe.setObjectName("APframe")
        self.label = QtWidgets.QLabel(self.APframe)
        self.label.setGeometry(QtCore.QRect(10, 10, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.APframe)
        self.label_2.setGeometry(QtCore.QRect(60, 20, 61, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.ApType = QtWidgets.QComboBox(self.APframe)
        self.ApType.setGeometry(QtCore.QRect(150, 30, 81, 22))
        self.ApType.setObjectName("ApType")
        self.ApType.addItem("")
        self.ApType.setItemText(0, "")
        self.ApType.addItem("")
        self.ApType.addItem("")
        self.ApType.addItem("")
        self.ApType.addItem("")
        self.label_3 = QtWidgets.QLabel(self.APframe)
        self.label_3.setGeometry(QtCore.QRect(60, 80, 61, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.APframe)
        self.label_4.setGeometry(QtCore.QRect(60, 110, 61, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.APframe)
        self.label_5.setGeometry(QtCore.QRect(60, 140, 61, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.ApIp = QtWidgets.QLineEdit(self.APframe)
        self.ApIp.setGeometry(QtCore.QRect(130, 90, 121, 22))
        self.ApIp.setObjectName("ApIp")
        self.Username = QtWidgets.QLineEdit(self.APframe)
        self.Username.setGeometry(QtCore.QRect(130, 120, 121, 22))
        self.Username.setObjectName("Username")
        self.Password = QtWidgets.QLineEdit(self.APframe)
        self.Password.setGeometry(QtCore.QRect(130, 150, 121, 22))
        self.Password.setObjectName("Password")
        self.radioButton2 = QtWidgets.QRadioButton(self.APframe)
        self.radioButton2.setGeometry(QtCore.QRect(140, 180, 89, 16))
        self.radioButton2.setObjectName("radioButton2")
        self.label_6 = QtWidgets.QLabel(self.APframe)
        self.label_6.setGeometry(QtCore.QRect(60, 170, 61, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.radioButton5 = QtWidgets.QRadioButton(self.APframe)
        self.radioButton5.setGeometry(QtCore.QRect(210, 180, 61, 16))
        self.radioButton5.setObjectName("radioButton5")
        self.label_7 = QtWidgets.QLabel(self.APframe)
        self.label_7.setGeometry(QtCore.QRect(60, 200, 61, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.Channel = QtWidgets.QLineEdit(self.APframe)
        self.Channel.setGeometry(QtCore.QRect(130, 200, 61, 22))
        self.Channel.setObjectName("Channel")
        self.label_20 = QtWidgets.QLabel(self.APframe)
        self.label_20.setGeometry(QtCore.QRect(60, 50, 71, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.StaType = QtWidgets.QComboBox(self.APframe)
        self.StaType.setGeometry(QtCore.QRect(150, 60, 81, 22))
        self.StaType.setObjectName("StaType")
        self.StaType.addItem("")
        self.StaType.setItemText(0, "")
        self.StaType.addItem("")
        self.StaType.addItem("")
        self.StaType.addItem("")
        self.StaType.addItem("")
        self.StaType.addItem("")
        self.APframe_2 = QtWidgets.QFrame(self.centralwidget)
        self.APframe_2.setGeometry(QtCore.QRect(0, 240, 351, 131))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.APframe_2.setFont(font)
        self.APframe_2.setFrameShape(QtWidgets.QFrame.Box)
        self.APframe_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.APframe_2.setLineWidth(1)
        self.APframe_2.setObjectName("APframe_2")
        self.label_8 = QtWidgets.QLabel(self.APframe_2)
        self.label_8.setGeometry(QtCore.QRect(10, 10, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_10 = QtWidgets.QLabel(self.APframe_2)
        self.label_10.setGeometry(QtCore.QRect(60, 30, 61, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.APframe_2)
        self.label_11.setGeometry(QtCore.QRect(200, 30, 61, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.APframe_2)
        self.label_12.setGeometry(QtCore.QRect(60, 60, 61, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.APframe_2)
        self.label_13.setGeometry(QtCore.QRect(200, 60, 71, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.Start = QtWidgets.QLineEdit(self.APframe_2)
        self.Start.setGeometry(QtCore.QRect(120, 40, 61, 22))
        self.Start.setObjectName("Start")
        self.Step = QtWidgets.QLineEdit(self.APframe_2)
        self.Step.setGeometry(QtCore.QRect(280, 40, 61, 22))
        self.Step.setObjectName("Step")
        self.End = QtWidgets.QLineEdit(self.APframe_2)
        self.End.setGeometry(QtCore.QRect(120, 70, 61, 22))
        self.End.setObjectName("End")
        self.LineLoss = QtWidgets.QLineEdit(self.APframe_2)
        self.LineLoss.setGeometry(QtCore.QRect(280, 70, 61, 22))
        self.LineLoss.setObjectName("LineLoss")
        self.label_18 = QtWidgets.QLabel(self.APframe_2)
        self.label_18.setGeometry(QtCore.QRect(60, 90, 71, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.NumberButton2_2 = QtWidgets.QRadioButton(self.APframe_2)
        self.NumberButton2_2.setGeometry(QtCore.QRect(130, 100, 89, 16))
        self.NumberButton2_2.setObjectName("NumberButton2_2")
        self.NumberButton4_4 = QtWidgets.QRadioButton(self.APframe_2)
        self.NumberButton4_4.setGeometry(QtCore.QRect(200, 100, 61, 16))
        self.NumberButton4_4.setObjectName("NumberButton4_4")
        self.APframe_3 = QtWidgets.QFrame(self.centralwidget)
        self.APframe_3.setGeometry(QtCore.QRect(-10, 370, 361, 151))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(225, 240, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 247, 237))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(112, 120, 110))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(150, 160, 147))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(225, 240, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 247, 237))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(225, 240, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 247, 237))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(112, 120, 110))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(150, 160, 147))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(225, 240, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 247, 237))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(112, 120, 110))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(225, 240, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 247, 237))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(112, 120, 110))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(150, 160, 147))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(112, 120, 110))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(112, 120, 110))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(225, 240, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(225, 240, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(225, 240, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.APframe_3.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.APframe_3.setFont(font)
        self.APframe_3.setFrameShape(QtWidgets.QFrame.Box)
        self.APframe_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.APframe_3.setLineWidth(1)
        self.APframe_3.setObjectName("APframe_3")
        self.label_9 = QtWidgets.QLabel(self.APframe_3)
        self.label_9.setGeometry(QtCore.QRect(10, 10, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_14 = QtWidgets.QLabel(self.APframe_3)
        self.label_14.setGeometry(QtCore.QRect(70, 20, 61, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.APframe_3)
        self.label_15.setGeometry(QtCore.QRect(70, 50, 61, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.APframe_3)
        self.label_16.setGeometry(QtCore.QRect(70, 80, 61, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.APframe_3)
        self.label_17.setGeometry(QtCore.QRect(70, 110, 91, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.PcIp = QtWidgets.QLineEdit(self.APframe_3)
        self.PcIp.setGeometry(QtCore.QRect(170, 30, 121, 22))
        self.PcIp.setObjectName("PcIp")
        self.StaIp = QtWidgets.QLineEdit(self.APframe_3)
        self.StaIp.setGeometry(QtCore.QRect(170, 60, 121, 22))
        self.StaIp.setObjectName("StaIp")
        self.Duration = QtWidgets.QLineEdit(self.APframe_3)
        self.Duration.setGeometry(QtCore.QRect(170, 90, 61, 22))
        self.Duration.setObjectName("Duration")
        self.PairNumber = QtWidgets.QLineEdit(self.APframe_3)
        self.PairNumber.setGeometry(QtCore.QRect(170, 120, 61, 22))
        self.PairNumber.setObjectName("PairNumber")
        self.Confirm = QtWidgets.QPushButton(self.centralwidget)
        self.Confirm.setGeometry(QtCore.QRect(90, 680, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.Confirm.setFont(font)
        self.Confirm.setObjectName("Confirm")
        self.Run = QtWidgets.QPushButton(self.centralwidget)
        self.Run.setGeometry(QtCore.QRect(330, 680, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.Run.setFont(font)
        self.Run.setObjectName("Run")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(360, 0, 311, 661))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.textBrowser = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 361, 641))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.tabWidget.addTab(self.tab, "")
        self.Report = QtWidgets.QPushButton(self.centralwidget)
        self.Report.setGeometry(QtCore.QRect(570, 680, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.Report.setFont(font)
        self.Report.setObjectName("Report")
        self.APframe_5 = QtWidgets.QFrame(self.centralwidget)
        self.APframe_5.setGeometry(QtCore.QRect(0, 610, 351, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.APframe_5.setFont(font)
        self.APframe_5.setFrameShape(QtWidgets.QFrame.Box)
        self.APframe_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.APframe_5.setLineWidth(1)
        self.APframe_5.setObjectName("APframe_5")
        self.label_22 = QtWidgets.QLabel(self.APframe_5)
        self.label_22.setGeometry(QtCore.QRect(10, 10, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.radioButton = QtWidgets.QRadioButton(self.APframe_5)
        self.radioButton.setGeometry(QtCore.QRect(110, 20, 89, 16))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.radioButton.setFont(font)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.APframe_5)
        self.radioButton_2.setGeometry(QtCore.QRect(230, 20, 89, 16))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")
        self.APframe_6 = QtWidgets.QFrame(self.centralwidget)
        self.APframe_6.setGeometry(QtCore.QRect(0, 520, 351, 91))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.APframe_6.setFont(font)
        self.APframe_6.setFrameShape(QtWidgets.QFrame.Box)
        self.APframe_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.APframe_6.setLineWidth(1)
        self.APframe_6.setObjectName("APframe_6")
        self.compass = QtWidgets.QLabel(self.APframe_6)
        self.compass.setGeometry(QtCore.QRect(10, 10, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.compass.setFont(font)
        self.compass.setObjectName("compass")
        self.Angle1 = QtWidgets.QLabel(self.APframe_6)
        self.Angle1.setGeometry(QtCore.QRect(60, 20, 61, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.Angle1.setFont(font)
        self.Angle1.setObjectName("Angle1")
        self.Angle4 = QtWidgets.QLabel(self.APframe_6)
        self.Angle4.setGeometry(QtCore.QRect(190, 20, 61, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.Angle4.setFont(font)
        self.Angle4.setObjectName("Angle4")
        self.Angle8 = QtWidgets.QLabel(self.APframe_6)
        self.Angle8.setGeometry(QtCore.QRect(60, 50, 61, 31))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.Angle8.setFont(font)
        self.Angle8.setObjectName("Angle8")
        self.CompassButton1 = QtWidgets.QRadioButton(self.APframe_6)
        self.CompassButton1.setGeometry(QtCore.QRect(120, 30, 89, 16))
        self.CompassButton1.setText("")
        self.CompassButton1.setObjectName("CompassButton1")
        self.CompassButton2 = QtWidgets.QRadioButton(self.APframe_6)
        self.CompassButton2.setGeometry(QtCore.QRect(250, 30, 89, 16))
        self.CompassButton2.setText("")
        self.CompassButton2.setObjectName("CompassButton2")
        self.CompassButton3 = QtWidgets.QRadioButton(self.APframe_6)
        self.CompassButton3.setGeometry(QtCore.QRect(120, 60, 89, 16))
        self.CompassButton3.setText("")
        self.CompassButton3.setObjectName("CompassButton3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 673, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CIG Rate over Range test tool v1.0"))
        self.label.setText(_translate("MainWindow", "AP"))
        self.label_2.setText(_translate("MainWindow", "AP Type："))
        self.ApType.setItemText(1, _translate("MainWindow", "AP-365"))
        self.ApType.setItemText(2, _translate("MainWindow", "WF-1931"))
        self.ApType.setItemText(3, _translate("MainWindow", "WF-8174A"))
        self.ApType.setItemText(4, _translate("MainWindow", "WF-1821"))
        self.label_3.setText(_translate("MainWindow", "AP IP："))
        self.label_4.setText(_translate("MainWindow", "Username："))
        self.label_5.setText(_translate("MainWindow", "Password："))
        self.radioButton2.setText(_translate("MainWindow", "2G"))
        self.label_6.setText(_translate("MainWindow", "Radio："))
        self.radioButton5.setText(_translate("MainWindow", "5G"))
        self.label_7.setText(_translate("MainWindow", "Channel："))
        self.label_20.setText(_translate("MainWindow", "STA Type："))
        self.StaType.setItemText(1, _translate("MainWindow", "STA"))
        self.StaType.setItemText(2, _translate("MainWindow", "AP-365"))
        self.StaType.setItemText(3, _translate("MainWindow", "WF-180"))
        self.StaType.setItemText(4, _translate("MainWindow", "WF-8174A"))
        self.StaType.setItemText(5, _translate("MainWindow", "WF-1821"))
        self.label_8.setText(_translate("MainWindow", "ATTENUATION"))
        self.label_10.setText(_translate("MainWindow", "Start："))
        self.label_11.setText(_translate("MainWindow", "Step："))
        self.label_12.setText(_translate("MainWindow", "End："))
        self.label_13.setText(_translate("MainWindow", "Cable Loss："))
        self.label_18.setText(_translate("MainWindow", "Number"))
        self.NumberButton2_2.setText(_translate("MainWindow", "2"))
        self.NumberButton4_4.setText(_translate("MainWindow", "4"))
        self.label_9.setText(_translate("MainWindow", "CHARIOT"))
        self.label_14.setText(_translate("MainWindow", "PC IP："))
        self.label_15.setText(_translate("MainWindow", "STA IP："))
        self.label_16.setText(_translate("MainWindow", "Duration："))
        self.label_17.setText(_translate("MainWindow", "Pair Number："))
        self.Confirm.setText(_translate("MainWindow", "Confirm"))
        self.Run.setText(_translate("MainWindow", "Run"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Log Window"))
        self.Report.setText(_translate("MainWindow", "Report"))
        self.label_22.setText(_translate("MainWindow", "TEST TYPE"))
        self.radioButton.setText(_translate("MainWindow", "Continue"))
        self.radioButton_2.setText(_translate("MainWindow", "Restart"))
        self.compass.setText(_translate("MainWindow", "COMPASS"))
        self.Angle1.setText(_translate("MainWindow", "Angle 1："))
        self.Angle4.setText(_translate("MainWindow", "Angle 4："))
        self.Angle8.setText(_translate("MainWindow", "Angle 8："))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

