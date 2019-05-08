__author__ = 'WBU'

from xlsxwriter.workbook import Workbook
from data.data import *
from data.parameters import AP_TYPE
from Throught import Generate_TP_To_Txt
import time
import config

Generate_TP_To_Txt()
rep_to_excel = Reportdata_Get()
rep_to_excel.Rx_tp_get()
rep_to_excel.Tx_tp_get()
rep_to_excel.Tx_rate_get()
rep_to_excel.Ap_rssi_get()
rep_to_excel.Rx_rate_get()
rep_to_excel.Sta_rssi_get()
rep_to_excel.Ch_get()
rep_to_excel.Att_get()
rep_to_excel.Dura_Time_get()
rep_to_excel.MCS_TxRate_get()
rep_to_excel.MCS_RxRate_get()
rep_to_excel.NSS_TxRate_get()
rep_to_excel.NSS_RxRate_get()
rep_to_excel.BW_TxRate_get()
rep_to_excel.BW_RxRate_get()

title = ["Path Loss(dB)", "Channel", "Tx_Throughput", "Rx_Throughput", "Sta Rssi", "AP Rssi",
         "Tx Rate", "Rx Rate", "Time", "MCS（Tx）", "MCS（Rx）", "NSS（Tx）", "NSS（Rx）",
         "BW（Tx）", "BW（Rx）"]


# now_time=time.strftime("%Y-%m-%d %H%M%S",time.localtime())
now_time = time.strftime("%Y-%m-%d", time.localtime())
conf = config.Config
test_ap = conf.Ap_type_get()
test_radio = conf.Radio_get()

filename = "Rate Over Range OTA test result_" + test_ap + '_' + test_radio + "1 angle_" + now_time
workbook = Workbook(filename + ".xlsx")
worksheet = workbook.add_worksheet("Rate over range conducted")

worksheet.set_column('A:A', 21)
worksheet.set_column('B:B', 11)
worksheet.set_column('C:D', 18)
worksheet.set_column('E:H', 11)
worksheet.set_column('I:I', 10)
worksheet.set_column('J:K', 42)
worksheet.set_column('L:M', 28)
worksheet.set_column('N:O', 33)
worksheet.set_row(0, 24, )
for row in range(1, 100):
    worksheet.set_row(row, 16)

chart_rx = workbook.add_chart({"type": "line"})
chart_tx = workbook.add_chart({"type": "line"})

head_format = workbook.add_format({
    'font_size': 14,
    'bold': True,
    'align': 'center',
    'valign': 'vcenter',
    'border': True,
    'fg_color': '#FFA07A',
})

sl_formate = workbook.add_format({
    'align': 'center',
    'border': True,
    'fg_color': '#C5C1AA'
})

channel_formate = workbook.add_format({
    'border': True,
    'align': 'center',
})
data_formate = workbook.add_format({
    'border': True,
})

rate_info_formate = workbook.add_format({
    'font_size': 9,
    'border': True,
})


def write_row():
    worksheet.write_row("A1", title, head_format)


def write_Attenuation():
    posX = ord('A')
    posY = 2
    for attenuation in Att_rep:
        worksheet.write(chr(posX) + str(posY), attenuation, sl_formate)
        posY += 1


def write_Channel():
    posX = ord('B')
    posY = 2
    for channel in Channel:
        worksheet.write(chr(posX) + str(posY), channel, channel_formate)
        posY += 1


def write_Tx():
    cur_row = str(len(Att_rep) + 1)
    cur_chart = str(len(Att_rep) + 2)
    posX = ord('C')
    posY = 2
    for tx in Tx_Throught:
        worksheet.write(chr(posX) + str(posY), tx, data_formate)
        posY += 1
    chart_tx.set_title({
        "name": "TX Graph"
    })
    chart_tx.set_y_axis({
        "name": "Mbps"
    })
    chart_tx.set_x_axis(
        {
            'name': 'Path Loss(dB)'

        }
    )
    chart_tx.add_series({
        'name': "TX",
        'categories': "=Rate over Range!$A$2:$A$" + cur_row,
        'values': '=Rate over Range!$C$2:$C$' + cur_row,
        'marker': {
            'type': 'circle',
            'size': 5,
            'border': {'color': 'red'},
            'fill': {'color': 'yellow'}
        },
    })
    worksheet.insert_chart('A' + cur_chart, chart_tx)


def write_Rx():
    cur_row = str(len(Att_rep) + 1)
    cur_chart = str(len(Att_rep) + 2)
    posX = ord('D')
    posY = 2
    for rx in Rx_Throught:
        worksheet.write(chr(posX) + str(posY), rx, data_formate)
        posY += 1
    chart_rx.set_title({
        "name": "RX Graph"
    })
    chart_rx.set_y_axis({
        "name": "Mbps"
    })
    chart_rx.add_series({
        'name': "RX",
        'categories': "=Rate over Range!$A$2:$A$" + cur_row,
        'values': '=Rate over Range!$D$2:$D$' + cur_row,
        'marker': {
            'type': 'circle',
            'size': 5,
            'border': {'color': 'red'},
            'fill': {'color': 'yellow'}
        },
    })
    worksheet.insert_chart('E' + cur_chart, chart_rx)


def write_STA_Rssi():
    posX = ord('E')
    posY = 2
    for starssi in Sta_Rssi:
        worksheet.write(chr(posX) + str(posY), int(starssi), data_formate)
        posY += 1


def write_AP_Rssi():
    posX = ord('F')
    posY = 2

    for aprssi in Ap_Rssi:
        worksheet.write(chr(posX) + str(posY), int(aprssi), data_formate)
        posY += 1


def write_Tx_Rate():
    posX = ord('G')
    posY = 2
    for txrate in Tx_Rate:
        worksheet.write(chr(posX) + str(posY), int(txrate), data_formate)
        posY += 1


def write_Rx_Rate():
    posX = ord('H')
    posY = 2
    for rxrate in Rx_Rate:
        worksheet.write(chr(posX) + str(posY), int(rxrate), data_formate)
        posY += 1


def write_Time():
    posX = ord('I')
    posY = 2
    for time in Dura_Time:
        worksheet.write(chr(posX) + str(posY), int(time), data_formate)
        posY += 1


def write_TX_MCS():
    posX = ord('J')
    posY = 2
    for tx_mcs in MCS_Tx_Rate:
        worksheet.write(chr(posX) + str(posY), tx_mcs, rate_info_formate)
        posY += 1


def write_RX_MCS():
    posX = ord('K')
    posY = 2
    for rx_mcs in MCS_Rx_Rate:
        worksheet.write(chr(posX) + str(posY), rx_mcs, rate_info_formate)
        posY += 1


def write_TX_NSS():
    posX = ord('L')
    posY = 2
    for tx_nss in NSS_Tx_Rate:
        worksheet.write(chr(posX) + str(posY), tx_nss, rate_info_formate)
        posY += 1


def write_RX_NSS():
    posX = ord('M')
    posY = 2
    for rx_nss in NSS_Rx_Rate:
        worksheet.write(chr(posX) + str(posY), rx_nss, rate_info_formate)
        posY += 1


def write_TX_BW():
    posX = ord('N')
    posY = 2
    for tx_bw in BW_Tx_Rate:
        worksheet.write(chr(posX) + str(posY), tx_bw, rate_info_formate)
        posY += 1


def write_RX_BW():
    posX = ord('O')
    posY = 2
    for rx_bw in BW_Rx_Rate:
        worksheet.write(chr(posX) + str(posY), rx_bw, rate_info_formate)
        posY += 1


def Generate_Test_Report_one():
    if AP_TYPE == "WF-1931":
        write_row()
        write_Attenuation()
        write_Channel()
        write_Rx()
        write_Tx()
        write_AP_Rssi()
        write_STA_Rssi()
        write_Rx_Rate()
        write_Tx_Rate()
        write_Time()
        write_TX_MCS()
        write_RX_MCS()
        write_TX_NSS()
        write_RX_NSS()
        write_TX_BW()
        write_RX_BW()
    else:
        write_row()
        write_Attenuation()
        write_Channel()
        write_Rx()
        write_Tx()
        write_AP_Rssi()
        write_STA_Rssi()
        write_Rx_Rate()
        write_Tx_Rate()
        write_Time()


Generate_Test_Report_one()
workbook.close()
