__author__ = 'DVTRF'

from xlsxwriter import Workbook
from data.data import *
from data.parameters import AP_TYPE, ANGLE_NUM, LINE_LOSS
from config import conf
import time
# import pandas as pd

now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
stop_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
test_ap = conf.Ap_type_get()
test_radio = conf.Radio_get()
filename = test_ap + "_Rate_over_Range_OTA_Test_Report_" + test_radio + '_' + now_time + ".xlsx"
print('Report:', filename)
workbook: Workbook = Workbook('./Report/' + filename)
worksheet_cover = workbook.add_worksheet("Overview")
worksheet_environment = workbook.add_worksheet("Environment")
worksheet_range = workbook.add_worksheet("Rate_over_Range")
if ANGLE_NUM > 1:
    worksheet_angle = workbook.add_worksheet("Rate_over_Angle")
    worksheet_angle.hide_gridlines(2)
worksheet_data = workbook.add_worksheet("Data")
worksheet_cover.hide_gridlines(2)
worksheet_environment.hide_gridlines(2)
worksheet_range.hide_gridlines(2)
worksheet_data.hide_gridlines(2)

# title
if ANGLE_NUM > 1:
    title = ['Channel', 'Path_Loss(dB)', 'Angle', 'DS_Throughput', 'DS_Throughput_avg', 'US_Throughput',
             'US_Throughput_avg', 'Sta_Rssi', 'Sta_Rssi_avg', 'AP_Rssi', 'AP_Rssi_avg', 'DS_Rate', 'DS_Rate_avg',
             'US_Rate', 'US_Rate_avg', 'Time', 'MCS(DS)', 'MCS(US)', 'NSS(DS)', 'NSS(US)', 'BW(DS)', 'BW(US)',
             'STA RSSI(per chain)', 'AP POWER', 'AP RSSI(per chain)', 'STA POWER']
else:
    title = ['Channel', 'Path_Loss(dB)', 'Angle', 'DS_Throughput', 'US_Throughput', 'Sta_Rssi', 'AP_Rssi', 'DS_Rate',
             'US_Rate', 'Time', 'MCS(DS)', 'NSS(DS)', 'BW(DS)', 'MCS(US)', 'NSS(US)', 'BW(US)', 'STA RSSI(per chain)',
             'AP POWER', 'AP RSSI(per chain)', 'STA POWER']


# 设置列宽
worksheet_cover.set_column('B:B', 12)
worksheet_cover.set_column('C:C', 24)
worksheet_cover.set_column('D:D', 35)
worksheet_cover.set_row(7, 35)

worksheet_data.set_column('A:A', 12)
worksheet_data.set_column('B:B', 20)
worksheet_data.set_column('C:C', 8)
worksheet_data.set_column('D:D', 20)
worksheet_data.set_column('E:E', 26)
worksheet_data.set_column('F:F', 20)
worksheet_data.set_column('G:G', 26)
worksheet_data.set_column('H:H', 12)
worksheet_data.set_column('I:I', 18)
worksheet_data.set_column('J:J', 12)
worksheet_data.set_column('K:K', 18)
worksheet_data.set_column('L:L', 10)
worksheet_data.set_column('M:M', 18)
worksheet_data.set_column('N:N', 10)
worksheet_data.set_column('O:O', 18)
worksheet_data.set_column('P:P', 8)
worksheet_data.set_column('Q:V', 12)
worksheet_data.set_column('W:W', 38)
worksheet_data.set_column('X:X', 25)
worksheet_data.set_column('Y:Y', 38)
worksheet_data.set_column('Z:Z', 25)

# 设置第一行的行宽
worksheet_data.set_row(0, 24, )
# 设置后面100行的行宽
for row in range(1, 100):
    worksheet_data.set_row(row, 16)

company_format = workbook.add_format({
    'align': 'left',
    #'valign': 'vcenter',
    'font_name': 'Arial Unicode MS',
})

report_name_format = workbook.add_format({
    'font_size': 28,
    'bold': True,
    'align': 'left',
    #'valign': 'vcenter',
    'font_name': 'Verdana',
})

info_format = workbook.add_format({
    'italic': True,
    'align': 'left',
    #'valign': 'vcenter',
    'font_name': 'Times New Roman',
})

head_format = workbook.add_format({
    'font_size': 14,
    'bold': True,
    'align': 'center',
    'valign': 'vcenter',
    'border': True,
    'fg_color': '#FFCC66',
    'font_name': 'Arial Unicode MS',
})

merge_atten_format = workbook.add_format(
    {
        'font_size': 11,
        'bold': True,
        'border': True,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#C5C1AA',
        'font_name': 'Arial Unicode MS',
    }
)

merge_channel_format = workbook.add_format(
    {
        'font_size': 11,
        'bold': True,
        'border': True,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#C5C1BB',
        'font_name': 'Arial Unicode MS',
    }
)

tp_format = workbook.add_format({
    'border': True,
    'num_format': '0.000',
    'font_name': 'Arial Unicode MS',
})

rssi_format = workbook.add_format({
    'border': True,
    'num_format': '0',
    'font_name': 'Arial Unicode MS',
})

rate_format = workbook.add_format({
    'border': True,
    'num_format': '0.0',
    'font_name': 'Arial Unicode MS',
})

data_format = workbook.add_format({
    'border': True,
    'font_name': 'Arial Unicode MS',
})

merge_format = workbook.add_format(
    {
        'font_size': 11,
        'border': True,
        'align': 'center',
        'valign': 'vcenter',
        'num_format': '0.000',
        'font_name': 'Arial Unicode MS',
    }
)


def write_row():
    worksheet_data.write_row("A1", title, head_format)


def write_Channel():
    posX = ord('A')
    posY = 2
    posZ = posY + int(ANGLE_NUM) - 1
    for channel in Channel:
        if ANGLE_NUM > 1:
            worksheet_data.merge_range(str(chr(posX) + str(posY) + ":" + chr(posX) + str(posZ)), channel, merge_channel_format)
            posY += int(ANGLE_NUM)
            posZ += int(ANGLE_NUM)
        else:
            worksheet_data.write(chr(posX) + str(posY), channel, data_format)
            posY += 1


def write_Attenuation():
    posX = ord('B')
    posY = 2
    posZ = posY + int(ANGLE_NUM) - 1
    for attenvalue in Att_rep:
        attenvalue = attenvalue + LINE_LOSS
        if ANGLE_NUM > 1:
            worksheet_data.merge_range(str(chr(posX) + str(posY) + ":" + chr(posX) + str(posZ)), attenvalue, merge_atten_format)
            posY += int(ANGLE_NUM)
            posZ += int(ANGLE_NUM)
        else:
            worksheet_data.write(chr(posX) + str(posY), attenvalue, data_format)
            posY += 1


def write_Angle():
    posX = ord('C')
    posY = 2
    for angle in Angle:
        worksheet_data.write(chr(posX) + str(posY), angle, data_format)
        posY += 1


def write_Tx():
    posX = ord('D')
    posY = 2
    for tx in Tx_Throught:
        worksheet_data.write(chr(posX) + str(posY), tx, tp_format)
        posY += 1
    return posX


def write_Rx(posX=None):
    posX = posX + 1
    posY = 2
    for rx in Rx_Throught:
        worksheet_data.write(chr(posX) + str(posY), rx, tp_format)
        posY += 1
    return posX


def write_AP_Rssi(posX=None):
    posX = posX + 1
    posY = 2
    for aprssi in Ap_Rssi:
        worksheet_data.write(chr(posX) + str(posY), int(aprssi), data_format)
        posY += 1
    return posX


def write_STA_Rssi(posX=None):
    posX = posX + 1
    posY = 2
    for starssi in Sta_Rssi:
        worksheet_data.write(chr(posX) + str(posY), int(starssi), data_format)
        posY += 1
    return posX


def write_Tx_Rate(posX=None):
    posX = posX + 1
    posY = 2
    for txrate in Tx_Rate:
        worksheet_data.write(chr(posX) + str(posY), float(txrate), rate_format)
        posY += 1
    return posX


def write_Rx_Rate(posX=None):
    posX = posX + 1
    posY = 2
    for rxrate in Rx_Rate:
        worksheet_data.write(chr(posX) + str(posY), float(rxrate), rate_format)
        posY += 1
    return posX


def write_Time(posX=None):
    posX = posX + 1
    posY = 2
    for time in Dura_Time:
        worksheet_data.write(chr(posX) + str(posY), int(time), data_format)
        posY += 1
    return posX


def write_TX_MCS(posX=None):
    posX = posX + 1
    posY = 2
    for tx_mcs in MCS_Tx_Rate:
        worksheet_data.write(chr(posX) + str(posY), tx_mcs, data_format)
        posY += 1
    return posX


def write_TX_NSS(posX=None):
    posX = posX + 1
    posY = 2
    for tx_nss in NSS_Tx_Rate:
        worksheet_data.write(chr(posX) + str(posY), tx_nss, data_format)
        posY += 1
    return posX


def write_TX_BW(posX=None):
    posX = posX + 1
    posY = 2
    for tx_bw in BW_Tx_Rate:
        worksheet_data.write(chr(posX) + str(posY), tx_bw, data_format)
        posY += 1
    return posX


def write_RX_MCS(posX=None):
    posX = posX + 1
    posY = 2
    for rx_mcs in MCS_Rx_Rate:
        worksheet_data.write(chr(posX) + str(posY), rx_mcs, data_format)
        posY += 1
    return posX


def write_RX_NSS(posX=None):
    posX = posX + 1
    posY = 2
    for rx_nss in NSS_Rx_Rate:
        worksheet_data.write(chr(posX) + str(posY), rx_nss, data_format)
        posY += 1
    return posX


def write_RX_BW(posX=None):
    posX = posX + 1
    posY = 2
    for rx_bw in BW_Rx_Rate:
        worksheet_data.write(chr(posX) + str(posY), rx_bw, data_format)
        posY += 1
    return posX


def write_TX_ANTRSSI(posX=None):
    posX = posX + 1
    posY = 2
    for txant_rssi in TX_RSSI_ANT:
        worksheet_data.write(chr(posX) + str(posY), txant_rssi, data_format)
        posY += 1
    return posX


def write_TX_ANTPOWER(posX=None):
    posX = posX + 1
    posY = 2
    for txant_power in TX_POWER_ANT:
        worksheet_data.write(chr(posX) + str(posY), txant_power, data_format)
        posY += 1
    return posX


def write_RX_ANTRSSI(posX=None):
    posX = posX + 1
    posY = 2
    for rxant_rssi in RX_RSSI_ANT:
        worksheet_data.write(chr(posX) + str(posY), rxant_rssi, data_format)
        posY += 1
    return posX


def write_RX_ANTPOWER(posX=None):
    posX = posX + 1
    posY = 2
    for rxant_power in RX_POWER_ANT:
        worksheet_data.write(chr(posX) + str(posY), rxant_power, data_format)
        posY += 1
    return posX


# for average
def write_avg(posX=None):
    posXX = posX
    posX = posX + 1
    posY = 2
    posZ = posY + int(ANGLE_NUM) - 1
    for attenvalue in Att_rep:
        worksheet_data.merge_range(chr(posX) + str(posY) + ":" + chr(posX) + str(posZ), '', merge_format)
        worksheet_data.write_formula(chr(posX) + str(posY),
                                     '=AVERAGE('+chr(posXX)+str(posY)+':'+chr(posXX)+str(posZ)+')', merge_format)
        posY += int(ANGLE_NUM)
        posZ += int(ANGLE_NUM)
    return posX


def write_range(mode, posA, posB, posX):
    if mode == 'DS':
        name = 'DS Graph'
        tp_name = 'DS Throughput'
        chart = 'chart_tx'
        color_line = '#3399FF'
    elif mode == 'US':
        name = 'US Graph'
        tp_name = 'US Throughput'
        chart = 'chart_rx'
        color_line = '#33CC66'
    chart_tx = workbook.add_chart({"type": "line"})
    chart_rx = workbook.add_chart({"type": "line"})
    chart = eval(chart)
    # insert line graph
    cur_row_axis = str(len(Att_rep) * int(ANGLE_NUM) + 1)
    #cur_row_x = str(len(Att_rep) * int(ANGLE_NUM) + 1)
    #cur_row_chart = str(len(Att_rep) * int(ANGLE_NUM) + 2)
    chart.set_title(
        {
            "name": name
        }
    )
    chart.set_y_axis(
        {
            "name": "Mbps",
            'major_gridlines': {'visible': False},
            'minor_gridlines': {'visible': False},
        }
    )
    chart.set_x_axis(
        {
            'name': 'RSSI(dBm)',
        }
    )
    if mode == 'DS':
        chart.set_chartarea({
            'border': {'none': True},
            'fill': {'none': True},
            'gradient': {'colors': ['#FFE9D7', '#FFD4B2', '#FFC18B']}
        })
    else:
        chart.set_chartarea({
            'border': {'none': True},
            'fill': {'none': True},
            'gradient': {'colors': ['#FFE2E2', '#FFC7C6', '#FFA5A4']}
        })
    if ANGLE_NUM > 1:
        tp_list_forrange = []
        rssi_list_forrange = []
        posY = 2
        for att in Att_rep:
            tp = 'Data!$' + chr(posA) + '$' + str(posY)
            tp_list_forrange.append(tp)
            rssi = 'Data!$' + chr(posB) + '$' + str(posY)
            rssi_list_forrange.append(rssi)
            posY += int(ANGLE_NUM)
        tp_list_forrange = tuple(tp_list_forrange)
        rssi_list_forrange = tuple(rssi_list_forrange)
        tp_list_forrange = ','.join(tp_list_forrange)
        rssi_list_forrange = ','.join(rssi_list_forrange)
        tp_list_forrange = str(tp_list_forrange)
        rssi_list_forrange = str(rssi_list_forrange)
        chart.add_series({
            'name': tp_name,
            'categories': '=('+rssi_list_forrange+')',
            'values': '=('+tp_list_forrange+')',
            'line': ({'color': color_line}),
            'gradient': {'colors': ['#FFE9D7', '#FFD4B2', '#FFC18B']},
            'marker': {
                'type': 'circle',
                'size': 3,
                'border': {'color': 'red'},
                'fill': {'color': 'yellow'},
            },
        })
    else:
        chart.add_series({
            'name': tp_name,
            'categories': '=Data!$' + chr(posB) + '$2:$' + chr(posB) + '$' + cur_row_axis,
            'values': '=Data!$' + chr(posA) + '$2:$' + chr(posA) + '$' + cur_row_axis,
            'line': {'color': color_line},
            'marker': {
                'type': 'circle',
                'size': 3,
                'border': {'color': 'red'},
                'fill': {'color': 'yellow'},
            },
        })
    if mode == 'DS':
        chart.set_plotarea({
            'border': {'none': True},
            'fill': {'none': True},
            #'gradient': {'colors': ['#FFE9E1', '#FFD4B2', '#FFC18B']}
            'gradient': {'colors': ['#FFE4CE', '#FFD4B2', '#FFC695']}
        })
    else:
        chart.set_plotarea({
            'border': {'none': True},
            'fill': {'none': True},
            'gradient': {'colors': ['#FFDBDB', '#FFC7C6', '#FFADAC']}
        })
    # chart.set_legend({'none': True})
    worksheet_range.insert_chart('B'+str(posX), chart, {'x_scale': 2.5, 'y_scale': 1.2})


def write_radar(posA, posE):
    posB = ord('C')
    posY = 2
    posD = 2
    if posE == 'B':
        tp_type = 'DS Throughput'
    elif posE == 'J':
        tp_type = 'US Throughput'
    else:
        print('Check postion')
        pass
    for att in Att_rep:
        # insert line graph
        radar = radar_name = 'radar' + str(att)
        radar = workbook.add_chart({"type": "radar"})
        #radar = eval(radar)
        radar.set_title({
            "name": 'Attenuation='+str(att)+'dB'
        })
        radar.set_y_axis({
            "name": "Mbps"
        })
        radar.set_x_axis(
            {
                'name': 'Angle'
            }
        )
        if posE == 'B':
            radar.set_chartarea({
                'border': {'none': True},
                'gradient': {'colors': ['#EEE7F8', '#DED2F1', '#CBB8E9']}
            })
        else:
            radar.set_chartarea({
                'border': {'none': True},
                'gradient': {'colors': ['#EEF8FF', '#C3F1FF', '#A2EBFF']}
            })
        if ANGLE_NUM > 1:
            radar.add_series({
                'name': tp_type,
                'categories': '=Data!$' + chr(posB) + '$' + str(posY) + ':$' + chr(posB) + '$' +
                              str(int(ANGLE_NUM) + posY - 1),
                'values': '=Data!$' + chr(posA) + '$' + str(posY) + ':$' + chr(posA) + '$' +
                              str(int(ANGLE_NUM) + posY - 1),
                'line': {'color': '#3399FF'},
                'gradient': {'colors': ['#FFE9D7', '#FFD4B2', '#FFC18B']},
                'marker': {
                    'type': 'circle',
                    'size': 3,
                    'border': {'color': 'red'},
                    'fill': {'color': 'yellow'},
                },
            })
        else:
            pass
        if posE == 'B':
            radar.set_plotarea({
                'border': {'none': True},
                'fill': {'none': True},
                #'gradient': {'colors': ['#EEE7F8', '#DED2F1', '#CBB8E9']}
                'gradient': {'colors': ['#E6DCF4', '#DED2F1', '#CBB8E9']}
            })
        else:
            radar.set_plotarea({
                'border': {'none': True},
                'fill': {'none': True},
                #'gradient': {'colors': ['#EEF8FF', '#C3F1FF', '#A2EBFF']}
                'gradient': {'colors': ['#DCF7FF', '#C3F1FF', '#A2EBFF']}
            })
        worksheet_angle.insert_chart(posE+str(posD), radar, {'x_scale': 1, 'y_scale': 1.4})
        posY += int(ANGLE_NUM)
        posD += 20


# add Auxiliary column
def addac_for_angle():
    worksheet_data.write_row('AA1', ['ac_for_angle'], head_format)
    posY = 2
    posYY = 2
    posYC = 0
    for angle in Angle:
        worksheet_data.write_formula('AA' + str(posY), '=$B$'+str(posYY)+'&"-"&C'+str(posY))
        posY += 1
        posYC += 1
        if posYC % 8 == 0:
            posYY += int(ANGLE_NUM)
    worksheet_data.set_column('AA:AA', None, None, {'hidden': True})


# def pivot_table(filename):
#     io = pd.ExcelFile('./Report/' + filename)
#     df = pd.read_excel(io, sheet_name='Data')
#     mydata = df.drop([0], axis=0)
#     table = pd.pivot_table(df, index=['ac_for_angle'], values=['Rx_Throughput', 'Tx_Throughput'])
#     table.to_excel(io, sheet_name='Rate_over_Angle')


def book_close():
    workbook.close()


def Generate_Test_Report():
    worksheet_cover.insert_image('B1', './images/CIG.png')
    #worksheet_cover.write_blank('B1', None)
    #worksheet_cover.set_header('&L&G', {'image_left': 'CIG.png'})
    worksheet_cover.merge_range('B4:I4', 'Cambridge Industries Group (CIG)', company_format)
    #worksheet_cover.write('B4', 'Cambridge Industries Group (CIG)', company_format)
    worksheet_cover.merge_range('B5:I5', 'Partnership for the Next Generation Broadband Access', company_format)
    #worksheet_cover.write('B5', 'Partnership for the Next Generation Broadband Access', company_format)
    worksheet_cover.merge_range('B7:I7', 'WIFI Performance Test Report', report_name_format)
    #worksheet_cover.write('B9', 'StartTime', company_format)
    worksheet_cover.write('B10', 'Finish Time', company_format)
    worksheet_cover.write('C10', stop_time, info_format)
    worksheet_cover.write('B12', 'DUT(AP)', company_format)
    worksheet_cover.write('C13', 'Product', company_format)
    worksheet_cover.write('D13', AP_TYPE, info_format)
    worksheet_cover.write('C14', 'Hardware Version', company_format)
    worksheet_cover.write('C15', 'Software Version', company_format)
    worksheet_cover.write('C16', 'Operating Band', company_format)
    worksheet_cover.write('C17', '2.4G Operation Mode', company_format)
    worksheet_cover.write('C18', '2.4G Antenna Configuration', company_format)
    worksheet_cover.write('C19', '5G Operation Mode', company_format)
    worksheet_cover.write('C20', '5G Antenna Configuration', company_format)
    worksheet_cover.write('B22', 'STATION', company_format)
    worksheet_cover.write('C23', 'Station Type', company_format)
    worksheet_cover.write('C24', 'Model', company_format)
    worksheet_cover.write('C25', 'Version', company_format)
    worksheet_cover.write('C26', 'Operating Band', company_format)
    worksheet_cover.write('C27', '2.4G Operation Mode', company_format)
    worksheet_cover.write('C28', '2.4G Antenna Configuration', company_format)
    worksheet_cover.write('C27', '5G Operation Mode', company_format)
    worksheet_cover.write('C28', '5G Antenna Configuration', company_format)
    worksheet_cover.write('B30', 'TEST TOOLS', company_format)
    worksheet_cover.write('C31', 'Test Software', company_format)
    worksheet_cover.write('D31', 'Ixchroit6.7', info_format)
    worksheet_cover.write('C32', 'Test Script', company_format)
    worksheet_cover.write('D32', 'High_Performance_Throughput.scr', info_format)

    worksheet_environment.write('B1', 'TEST DIAGRAM AND ENVIRONMENT', company_format)
    worksheet_environment.insert_image('B3', './images/environment.PNG')
    worksheet_environment.insert_image('M3', './images/tp.PNG')

    if AP_TYPE == 'WF-194':
        rep_to_excel = Reportdata_Get()
        rep_to_excel.Rx_tp_get()
        rep_to_excel.Tx_tp_get()
        rep_to_excel.Tx_rate_get()
        rep_to_excel.Sta_rssi_get()
        rep_to_excel.Rx_rate_get()
        rep_to_excel.Ap_rssi_get()
        rep_to_excel.Ch_get()
        rep_to_excel.Att_get()
        rep_to_excel.Angle_get()
        rep_to_excel.Dura_Time_get()
        rep_to_excel.MCS_TxRate_get()
        rep_to_excel.MCS_RxRate_get()
        rep_to_excel.NSS_TxRate_get()
        rep_to_excel.NSS_RxRate_get()
        rep_to_excel.BW_TxRate_get()
        rep_to_excel.BW_RxRate_get()
        rep_to_excel.RSSI_TXANT_get()
        rep_to_excel.POWER_TXANT_get()
        rep_to_excel.RSSI_RXANT_get()
        rep_to_excel.POWER_RXANT_get()

        write_row()
        write_Attenuation()
        write_Channel()
        write_Angle()
        if ANGLE_NUM > 1:
            posX_tx_tp = write_Tx()
            posX_txtp_avg = write_avg(posX_tx_tp)
            posX_rx_tp = write_Rx(posX_txtp_avg)
            posX_rxtp_avg = write_avg(posX_rx_tp)
            posX_STA_RSSI = write_STA_Rssi(posX_rxtp_avg)
            posX_STARSSI_avg = write_avg(posX_STA_RSSI)
            posX_AP_RSSI = write_AP_Rssi(posX_STARSSI_avg)
            posX_APRSSI_avg = write_avg(posX_AP_RSSI)
            posX_tx_rate = write_Tx_Rate(posX_APRSSI_avg)
            posX_txrate_avg = write_avg(posX_tx_rate)
            posX_rx_rate = write_Rx_Rate(posX_txrate_avg)
            posX_rxrate_avg = write_avg(posX_rx_rate)
            write_range('DS', posX_txtp_avg, posX_APRSSI_avg, 2)
            write_range('US', posX_rxtp_avg, posX_STARSSI_avg, 20)
            write_radar(posX_tx_tp, 'B')
            write_radar(posX_rx_tp, 'J')
        else:
            posX_tx_tp = write_Tx()
            posX_rx_tp = write_Rx(posX_tx_tp)
            posX_STA_RSSI = write_STA_Rssi(posX_rx_tp)
            posX_AP_RSSI = write_AP_Rssi(posX_STA_RSSI)
            posX_tx_rate = write_Tx_Rate(posX_AP_RSSI)
            posX_rxrate_avg = write_Rx_Rate(posX_tx_rate)
            write_range('DS', posX_tx_tp, posX_STA_RSSI, 2)
            write_range('US', posX_rx_tp, posX_AP_RSSI, 20)
        posX = write_Time(posX_rxrate_avg)
        posX = write_TX_MCS(posX)
        posX = write_TX_NSS(posX)
        posX = write_TX_BW(posX)
        posX = write_RX_MCS(posX)
        posX = write_RX_NSS(posX)
        posX = write_RX_BW(posX)
        posX = write_TX_ANTRSSI(posX)
        posX = write_TX_ANTPOWER(posX)
        posX = write_RX_ANTRSSI(posX)
        posX = write_RX_ANTPOWER(posX)
    elif AP_TYPE == 'WF-8186':
        rep_to_excel = Reportdata_Get()
        rep_to_excel.Rx_tp_get()
        rep_to_excel.Tx_tp_get()
        rep_to_excel.Tx_rate_get()
        rep_to_excel.Sta_rssi_get()
        rep_to_excel.Rx_rate_get()
        rep_to_excel.Ap_rssi_get()
        rep_to_excel.Ch_get()
        rep_to_excel.Att_get()
        rep_to_excel.Angle_get()
        rep_to_excel.Dura_Time_get()
        rep_to_excel.MCS_TxRate_get()
        rep_to_excel.MCS_RxRate_get()
        rep_to_excel.NSS_TxRate_get()
        rep_to_excel.NSS_RxRate_get()
        rep_to_excel.BW_TxRate_get()
        rep_to_excel.BW_RxRate_get()
        rep_to_excel.RSSI_TXANT_get()
        rep_to_excel.POWER_TXANT_get()
        rep_to_excel.RSSI_RXANT_get()
        rep_to_excel.POWER_RXANT_get()

        write_row()
        write_Attenuation()
        write_Channel()
        write_Angle()
        if ANGLE_NUM > 1:
            posX_tx_tp = write_Tx()
            posX_txtp_avg = write_avg(posX_tx_tp)
            posX_rx_tp = write_Rx(posX_txtp_avg)
            posX_rxtp_avg = write_avg(posX_rx_tp)
            posX_STA_RSSI = write_STA_Rssi(posX_rxtp_avg)
            posX_STARSSI_avg = write_avg(posX_STA_RSSI)
            posX_AP_RSSI = write_AP_Rssi(posX_STARSSI_avg)
            posX_APRSSI_avg = write_avg(posX_AP_RSSI)
            posX_tx_rate = write_Tx_Rate(posX_APRSSI_avg)
            posX_txrate_avg = write_avg(posX_tx_rate)
            posX_rx_rate = write_Rx_Rate(posX_txrate_avg)
            posX_rxrate_avg = write_avg(posX_rx_rate)
            write_range('DS', posX_txtp_avg, posX_APRSSI_avg, 2)
            write_range('US', posX_rxtp_avg, posX_STARSSI_avg, 20)
            write_radar(posX_tx_tp, 'B')
            write_radar(posX_rx_tp, 'J')
        else:
            posX_tx_tp = write_Tx()
            posX_rx_tp = write_Rx(posX_tx_tp)
            posX_STA_RSSI = write_STA_Rssi(posX_rx_tp)
            posX_AP_RSSI = write_AP_Rssi(posX_STA_RSSI)
            posX_tx_rate = write_Tx_Rate(posX_AP_RSSI)
            posX_rxrate_avg = write_Rx_Rate(posX_tx_rate)
            write_range('DS', posX_tx_tp, posX_STA_RSSI, 2)
            write_range('US', posX_rx_tp, posX_AP_RSSI, 20)
        posX = write_Time(posX_rxrate_avg)
        posX = write_TX_MCS(posX)
        posX = write_RX_MCS(posX)
        posX = write_TX_NSS(posX)
        posX = write_RX_NSS(posX)
        posX = write_TX_BW(posX)
        posX = write_RX_BW(posX)
        posX = write_TX_ANTRSSI(posX)
        posX = write_TX_ANTPOWER(posX)
        posX = write_RX_ANTRSSI(posX)
        posX = write_RX_ANTPOWER(posX)
        # pivot
        # addac_for_angle()
    else:
        print('NO TYPE')
        rep_to_excel = Reportdata_Get()
        rep_to_excel.Ch_get()
        rep_to_excel.Att_get()
        rep_to_excel.Angle_get()
        rep_to_excel.Dura_Time_get()
        rep_to_excel.Rx_tp_get()
        rep_to_excel.Tx_tp_get()
        # rep_to_excel.Tx_rate_get()
        # rep_to_excel.Ap_rssi_get()
        # rep_to_excel.Rx_rate_get()
        # rep_to_excel.Sta_rssi_get()
        # rep_to_excel.MCS_TxRate_get()
        # rep_to_excel.MCS_RxRate_get()
        # rep_to_excel.NSS_TxRate_get()
        # rep_to_excel.NSS_RxRate_get()
        # rep_to_excel.BW_TxRate_get()
        # rep_to_excel.BW_RxRate_get()
        # rep_to_excel.RSSI_TXANT_get()
        # rep_to_excel.POWER_TXANT_get()
        # rep_to_excel.RSSI_RXANT_get()
        # rep_to_excel.POWER_RXANT_get()

        write_row()
        write_Attenuation()
        write_Channel()
        write_Angle()
        if ANGLE_NUM > 1:
            posX_tx_tp = write_Tx()
            posX_txtp_avg = write_avg(posX_tx_tp)
            posX_rx_tp = write_Rx(posX_txtp_avg)
            posX_rxtp_avg = write_avg(posX_rx_tp)
            write_range('DS', posX_txtp_avg, ord('B'), 2)
            write_range('US', posX_rxtp_avg, ord('B'), 20)
            write_radar(posX_tx_tp, 'B')
            write_radar(posX_rx_tp, 'J')

            # posX_STA_RSSI = write_STA_Rssi(posX_rxtp_avg)
            # posX_STARSSI_avg = write_avg(posX_STA_RSSI)
            # posX_AP_RSSI = write_AP_Rssi(posX_STARSSI_avg)
            # posX_APRSSI_avg = write_avg(posX_AP_RSSI)
            # posX_tx_rate = write_Tx_Rate(posX_APRSSI_avg)
            # posX_txrate_avg = write_avg(posX_tx_rate)
            # posX_rx_rate = write_Rx_Rate(posX_txrate_avg)
            # posX_rxrate_avg = write_avg(posX_rx_rate)

        else:
            posX_tx_tp = write_Tx()
            posX_rx_tp = write_Rx(posX_tx_tp)
            # posX_STA_RSSI = write_STA_Rssi(posX_rx_tp)
            # posX_AP_RSSI = write_AP_Rssi(posX_STA_RSSI)
            # posX_tx_rate = write_Tx_Rate(posX_AP_RSSI)
            # posX_rxrate_avg = write_Rx_Rate(posX_tx_rate)
            # write_range('DS', posX_tx_tp, posX_STA_RSSI, 2)
            # write_range('US', posX_rx_tp, posX_AP_RSSI, 20)
        # posX = write_Time(posX_rxrate_avg)
        # posX = write_TX_MCS(posX)
        # posX = write_TX_NSS(posX)
        # posX = write_TX_BW(posX)
        # posX = write_RX_MCS(posX)
        # posX = write_RX_NSS(posX)
        # posX = write_RX_BW(posX)
        # posX = write_TX_ANTRSSI(posX)
        # posX = write_TX_ANTPOWER(posX)
        # posX = write_RX_ANTRSSI(posX)
        # posX = write_RX_ANTPOWER(posX)
    workbook.close()


if __name__ == "__main__":
    print('AP is ', AP_TYPE)
    #Generate_TP_To_Txt()
    Generate_Test_Report()





