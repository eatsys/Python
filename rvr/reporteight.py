__author__ = 'DVTRF'

from xlsxwriter.workbook import Workbook
from data.data import *
from data.parameters import ANGLE
from data.parameters import AP_TYPE
from Throught import Generate_TP_To_Txt
from config import conf
import time

now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
test_ap = conf.Ap_type_get()
test_radio = conf.Radio_get()
filename = test_ap + "_Rate_over_Range OTA Test Report_" + test_radio + '_' + now_time + ".xlsx"
# filename="Rate_over_Range OTA test result_"
print('Report:', filename)
workbook = Workbook('./Report/' + filename)
worksheet = workbook.add_worksheet("Rate_over_Range")


# title
title = ['Channel', 'Path Loss(dB)', 'Angle', 'Tx_Throughput', 'Rx_Throughput', 'Sta Rssi', 'AP Rssi', 'Tx Rate',
         'Rx Rate', 'Time', 'MCS(Rx)', 'MCS(Tx)', 'NSS(Tx)', 'NSS(Rx)', 'BW(Tx)', 'BW(Rx)']
# 设置列宽
worksheet.set_column('A:A', 18)
worksheet.set_column('B:B', 20)
worksheet.set_column('C:C', 11)
worksheet.set_column('D:E', 18)
worksheet.set_column('F:I', 11)
worksheet.set_column('J:J', 10)
worksheet.set_column('K:L', 58)
worksheet.set_column('M:N', 38)
worksheet.set_column('O:P', 45)

# 设置第一行的行宽
worksheet.set_row(0, 24, )
# 设置后面100行的行宽
for row in range(1, 100):
    worksheet.set_row(row, 16)

# insert line graph
chart_rx = workbook.add_chart({"type": "line"})
chart_tx = workbook.add_chart({"type": "line"})

head_format = workbook.add_format({
    'font_size': 14,
    'bold': True,
    'align': 'center',
    'valign': 'center',
    'border': True,
    'fg_color': '#FFA07A',
})

merge_atten_format = workbook.add_format(
    {
        'font_size': 11,
        'bold': True,
        'border': True,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#C5C1AA',
    }
)

merge_channel_format = workbook.add_format(
    {
        'font_size': 11,
        'bold': True,
        'border': True,
        'align': 'center',
        'valign': 'vcenter',
    }
)

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


def write_row():
    worksheet.write_row("A1", title, head_format)


def write_Channel():
    posX = ord('A')
    posY = 2
    posZ = 9
    for channel in Channel:
        worksheet.merge_range(str(chr(posX) + str(posY) + ":" + chr(posX) + str(posZ)), channel, merge_channel_format)
        posY += 8
        posZ += 8


def write_Attenuation():
    posX = ord('B')
    posY = 2
    posZ = 9
    for attenvalue in Att_rep:
        worksheet.merge_range(str(chr(posX) + str(posY) + ":" + chr(posX) + str(posZ)), attenvalue, merge_atten_format)
        posY += 8
        posZ += 8


def write_Angle():
    posX = ord('C')
    posY = 2
    for angle in Angle:
        worksheet.write(chr(posX) + str(posY), angle, data_formate)
        posY += 1


def write_Tx():
    cur_row_axis = str(len(Att_rep) * 8 - 6)
    cur_row_x = str(len(Att_rep) * 8 + 1)
    cur_row_chart = str(len(Att_rep) * 8 + 2)
    posX = ord('D')
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
        'categories': "=Rate_over_Range!$A$2:$A$" + cur_row_axis,
        'values': '=Rate_over_Range!$D$2:$D$' + cur_row_x,
        'marker': {
            'type': 'circle',
            'size': 5,
            'border': {'color': 'red'},
            'fill': {'color': 'yellow'}
        },
    })
    worksheet.insert_chart('A' + cur_row_chart, chart_tx)


def write_Rx():
    cur_row_axis = str(len(Att_rep) * 8 - 6)
    cur_row_x = str(len(Att_rep) * 8 + 1)
    cur_row_chart = str(len(Att_rep) * 8 + 2)
    posX = ord('E')
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
        'categories': "=Rate_over_Range!$A$2:$A$" + cur_row_axis,
        'values': '=Rate_over_Range!$E$2:$E$' + cur_row_x,
        'marker': {
            'type': 'circle',
            'size': 5,
            'border': {'color': 'red'},
            'fill': {'color': 'yellow'}
        },
    })
    worksheet.insert_chart('F' + cur_row_chart, chart_rx)


def write_STA_Rssi():
    posX = ord('F')
    posY = 2
    for starssi in Sta_Rssi:
        worksheet.write(chr(posX) + str(posY), int(starssi), data_formate)
        posY += 1


def write_AP_Rssi():
    posX = ord('G')
    posY = 2

    for aprssi in Ap_Rssi:
        worksheet.write(chr(posX) + str(posY), int(aprssi), data_formate)
        posY += 1


def write_Tx_Rate():
    posX = ord('H')
    posY = 2
    for txrate in Tx_Rate:
        worksheet.write(chr(posX) + str(posY), int(txrate), data_formate)
        posY += 1


def write_Rx_Rate():
    posX = ord('I')
    posY = 2
    for rxrate in Rx_Rate:
        worksheet.write(chr(posX) + str(posY), int(rxrate), data_formate)
        posY += 1


def write_Time():
    posX = ord('J')
    posY = 2
    for time in Dura_Time:
        worksheet.write(chr(posX) + str(posY), int(time), data_formate)
        posY += 1


def write_TX_MCS():
    posX = ord('K')
    posY = 2
    for tx_mcs in MCS_Tx_Rate:
        worksheet.write(chr(posX) + str(posY), tx_mcs, data_formate)
        posY += 1


def write_RX_MCS():
    posX = ord('L')
    posY = 2
    for rx_mcs in MCS_Rx_Rate:
        worksheet.write(chr(posX) + str(posY), rx_mcs, data_formate)
        posY += 1


def write_TX_NSS():
    posX = ord('M')
    posY = 2
    for tx_nss in NSS_Tx_Rate:
        worksheet.write(chr(posX) + str(posY), tx_nss, data_formate)
        posY += 1


def write_RX_NSS():
    posX = ord('N')
    posY = 2
    for rx_nss in NSS_Rx_Rate:
        worksheet.write(chr(posX) + str(posY), rx_nss, data_formate)
        posY += 1


def write_TX_BW():
    posX = ord('O')
    posY = 2
    for tx_bw in BW_Tx_Rate:
        worksheet.write(chr(posX) + str(posY), tx_bw, data_formate)
        posY += 1


def write_RX_BW():
    posX = ord('P')
    posY = 2
    for rx_bw in BW_Rx_Rate:
        worksheet.write(chr(posX) + str(posY), rx_bw, data_formate)
        posY += 1


def Generate_Test_Report_eight():
    Generate_TP_To_Txt()
    if AP_TYPE == 'WF-1931':
        rep_to_excel = Reportdata_Get()
        rep_to_excel.Rx_tp_get()
        rep_to_excel.Tx_tp_get()
        rep_to_excel.Tx_rate_get()
        rep_to_excel.Ap_rssi_get()
        ##rep_to_excel.Rx_rate_get()
        ##rep_to_excel.Sta_rssi_get()
        rep_to_excel.Ch_get()
        rep_to_excel.Att_get()
        rep_to_excel.Angle_get()
        ##rep_to_excel.Dura_Time_get()
        ##rep_to_excel.MCS_TxRate_get()
        ##rep_to_excel.MCS_RxRate_get()
        ##rep_to_excel.NSS_TxRate_get()
        ##rep_to_excel.NSS_RxRate_get()
        ##rep_to_excel.BW_TxRate_get()
        ##rep_to_excel.BW_RxRate_get()

        write_row()
        write_Attenuation()
        write_Channel()
        write_Angle()
        write_Rx()
        write_Tx()
        write_AP_Rssi()
        #write_STA_Rssi()
        #write_Rx_Rate()
        write_Tx_Rate()
        #write_Time()
        #write_TX_MCS()
        #write_RX_MCS()
        #write_TX_NSS()
        #write_RX_NSS()
        #write_TX_BW()
        #write_RX_BW()
    elif AP_TYPE == "WF-8174A":
        print('XXXX', AP_TYPE)
        rep_to_excel = Reportdata_Get()
        rep_to_excel.Rx_tp_get()
        rep_to_excel.Tx_tp_get()
        rep_to_excel.Tx_rate_get()
        rep_to_excel.Ap_rssi_get()
        #rep_to_excel.Rx_rate_get()
        # rep_to_excel.Sta_rssi_get()
        rep_to_excel.Ch_get()
        rep_to_excel.Att_get()
        rep_to_excel.Angle_get()
        rep_to_excel.Dura_Time_get()

        write_row()
        write_Attenuation()
        write_Channel()
        write_Angle()
        write_Rx()
        write_Tx()
        # write_AP_Rssi()
        # write_STA_Rssi()
        #write_Rx_Rate()
        write_Tx_Rate()
        write_Time()
    else:
        print('NO TYPE')
    workbook.close()



if __name__ == "__main__":
    print('AP is ', AP_TYPE)
    Generate_Test_Report_eight()




