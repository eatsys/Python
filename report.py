__author__ = 'DVTRF'

from xlsxwriter import Workbook
from data.data import *
from data.parameters import AP_TYPE, RADIO, STA_TYPE, ANGLE_NUM, LINE_LOSS, RUN_TPYE
import time

now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
stop_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
if RUN_TPYE == 0:
    test_type = '_OTA'
elif RUN_TPYE == 1:
    test_type = '_Conductive'
else:
    test_type = ''
filename = AP_TYPE + '_' + RADIO + '_Rate_over_Range' + test_type + '_Test_Report_' + now_time + '.xlsx'
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
             'US_Rate', 'US_Rate_avg', 'Time', 'BW(DS)', 'NSS(DS)', 'MCS(DS)', 'BW(US)', 'NSS(US)', 'MCS(US)',
             'STA RSSI(per chain)', 'AP POWER', 'AP RSSI(per chain)', 'STA POWER']
else:
    title = ['Channel', 'Path_Loss(dB)', 'Angle', 'DS_Throughput', 'US_Throughput', 'Sta_Rssi', 'AP_Rssi',
             'DS_Rate', 'US_Rate', 'Time', 'BW(DS)', 'NSS(DS)', 'MCS(DS)', 'BW(US)', 'NSS(US)', 'MCS(US)',
             'STA RSSI(per chain)', 'AP POWER', 'AP RSSI(per chain)', 'STA POWER']

# 设置列宽
worksheet_cover.set_column('B:B', 12)
worksheet_cover.set_column('C:C', 24)
worksheet_cover.set_column('D:D', 35)
worksheet_cover.set_row(7, 35)

worksheet_data.set_column('A:A', 12)
worksheet_data.set_column('B:B', 20)
worksheet_data.set_column('C:C', 9)
worksheet_data.set_column('D:D', 22)
worksheet_data.set_column('E:E', 29)
worksheet_data.set_column('F:F', 22)
worksheet_data.set_column('G:G', 29)
worksheet_data.set_column('H:H', 13)
worksheet_data.set_column('I:I', 20)
worksheet_data.set_column('J:J', 13)
worksheet_data.set_column('K:K', 20)
worksheet_data.set_column('L:L', 13)
worksheet_data.set_column('M:M', 20)
worksheet_data.set_column('N:N', 13)
worksheet_data.set_column('O:O', 20)
worksheet_data.set_column('P:P', 8)
worksheet_data.set_column('Q:V', 12)
worksheet_data.set_column('W:W', 30)
worksheet_data.set_column('X:X', 18)
worksheet_data.set_column('Y:Y', 30)
worksheet_data.set_column('Z:Z', 18)
worksheet_data.set_row(0, 22)
for row in range(1, 100):
    worksheet_data.set_row(row, 16.5)

company_format = workbook.add_format({
    'align': 'left',
    'font_name': 'Arial Unicode MS',
})

report_name_format = workbook.add_format({
    'font_size': 28,
    'bold': True,
    'align': 'left',
    'font_name': 'Verdana',
})

info_format = workbook.add_format({
    'italic': True,
    'align': 'left',
    'font_name': 'Times New Roman',
})

head_format = workbook.add_format({
    'font_size': 14,
    'bold': True,
    'align': 'center',
    'valign': 'vcenter',
    'border': True,
    'bottom': 3,
    'top': 3,
    'left': 3,
    'right': 3,
    'fg_color': '#FFCC66',
    'font_name': 'Arial Unicode MS',
})

merge_atten_format = workbook.add_format(
    {
        'font_size': 11,
        'bold': True,
        'border': True,
        'bottom': 3,
        'top': 3,
        'left': 3,
        'right': 3,
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
        'bottom': 3,
        'top': 3,
        'left': 3,
        'right': 3,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#C5C1BB',
        'font_name': 'Arial Unicode MS',
    }
)

tp_format = workbook.add_format({
    'border': True,
    'bottom': 3,
    'top': 3,
    'left': 3,
    'right': 3,
    'num_format': '0.000',
    'font_name': 'Arial Unicode MS',
})

rssi_format = workbook.add_format({
    'border': True,
    'bottom': 3,
    'top': 3,
    'left': 3,
    'right': 3,
    'num_format': '0',
    'font_name': 'Arial Unicode MS',
})

rate_format = workbook.add_format({
    'border': True,
    'bottom': 3,
    'top': 3,
    'left': 3,
    'right': 3,
    'num_format': '0',
    'font_name': 'Arial Unicode MS',
})

data_format = workbook.add_format({
    'border': True,
    'bottom': 3,
    'top': 3,
    'left': 3,
    'right': 3,
    'font_name': 'Arial Unicode MS',
})

merge_format = workbook.add_format(
    {
        'font_size': 11,
        'border': True,
        'bottom': 3,
        'top': 3,
        'left': 3,
        'right': 3,
        'align': 'center',
        'valign': 'vcenter',
        'num_format': '0',
        'font_name': 'Arial Unicode MS',
    }
)

border_format = workbook.add_format(
    {
        'border': True,
        'bottom': 3,
        'top': 3,
        'left': 3,
        'right': 3,
    }
)


def write_row():
    att_num = Reportdata_Get.Att_get()
    border_range = ANGLE_NUM * int(len(att_num))
    for r in range(len(title)):
        for c in range(border_range + 1):
            worksheet_data.write(c, r, None, border_format)
    worksheet_data.write_row("A1", title, head_format)


def write_Channel():
    posX = ord('A')
    posY = 2
    posZ = posY + int(ANGLE_NUM) - 1
    for channel in Channel:
        if ANGLE_NUM > 1:
            worksheet_data.merge_range(str(chr(posX) + str(posY) + ":" + chr(posX) + str(posZ)), channel,
                                       merge_channel_format)
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
            worksheet_data.merge_range(str(chr(posX) + str(posY) + ":" + chr(posX) + str(posZ)), attenvalue,
                                       merge_atten_format)
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
        worksheet_data.write(chr(posX) + str(posY), int(aprssi), rssi_format)
        posY += 1
    return posX


def write_STA_Rssi(posX=None):
    posX = posX + 1
    posY = 2
    for starssi in Sta_Rssi:
        worksheet_data.write(chr(posX) + str(posY), int(starssi), rssi_format)
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
                                     '=AVERAGE(' + chr(posXX) + str(posY) + ':' + chr(posXX) + str(posZ) + ')',
                                     merge_format)
        posY += int(ANGLE_NUM)
        posZ += int(ANGLE_NUM)
    return posX


def write_range_att(posA, posB, posC, posX):
    chart = workbook.add_chart({"type": "line"})
    cur_row_axis = str(len(Att_rep) * int(ANGLE_NUM) + 1)
    chart.set_title(
        {
            "name": 'RVR'
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
            'name': 'Attenuation(dB)',
        }
    )

    chart.set_chartarea({
        'border': {'none': True},
        'fill': {'none': True},
        'gradient': {'colors': ['#BBFFFF', '#AEEEEE', '#96CDCD']}
    })
    if ANGLE_NUM > 1:
        tptx_list_forrange = []
        att_list_forrange = []
        tprx_list_forrange = []
        posY = 2
        for att in Att_rep:
            tp_tx = 'Data!$' + chr(posA) + '$' + str(posY)
            tptx_list_forrange.append(tp_tx)
            tp_rx = 'Data!$' + chr(posC) + '$' + str(posY)
            tprx_list_forrange.append(tp_rx)
            att = 'Data!$' + chr(posB) + '$' + str(posY)
            att_list_forrange.append(att)
            posY += int(ANGLE_NUM)
        tptx_list_forrange = tuple(tptx_list_forrange)
        att_list_forrange = tuple(att_list_forrange)
        tprx_list_forrange = tuple(tprx_list_forrange)
        tptx_list_forrange = ','.join(tptx_list_forrange)
        att_list_forrange = ','.join(att_list_forrange)
        tprx_list_forrange = ','.join(tprx_list_forrange)
        tptx_list_forrange = str(tptx_list_forrange)
        att_list_forrange = str(att_list_forrange)
        tprx_list_forrange = str(tprx_list_forrange)
        chart.add_series({
            'name': 'DS Throughput',
            'categories': '=(' + att_list_forrange + ')',
            'values': '=(' + tptx_list_forrange + ')',
            'line': ({'color': '#3399FF'}),
            'smooth': True,
            'gradient': {'colors': ['#BBFFFF', '#AEEEEE', '#96CDCD']},
            'marker': {
                'type': 'diamond',
                'size': 3,
                'border': {'color': 'red'},
                'fill': {'color': 'yellow'},
            },
        })
        chart.add_series({
            'name': 'US Throughput',
            'categories': '=(' + att_list_forrange + ')',
            'values': '=(' + tprx_list_forrange + ')',
            'line': ({'color': '#33CC66'}),
            'smooth': True,
            'gradient': {'colors': ['#BBFFFF', '#AEEEEE', '#96CDCD']},
            'marker': {
                'type': 'circle',
                'size': 3,
                'border': {'color': 'red'},
                'fill': {'color': 'yellow'},
            },
        })
    else:
        chart.add_series({
            'name': 'DS Throughput',
            'categories': '=Data!$' + chr(posB) + '$2:$' + chr(posB) + '$' + cur_row_axis,
            'values': '=Data!$' + chr(posA) + '$2:$' + chr(posA) + '$' + cur_row_axis,
            'line': {'color': '#3399FF'},
            'smooth': True,
            'marker': {
                'type': 'diamond',
                'size': 3,
                'border': {'color': 'red'},
                'fill': {'color': 'yellow'},
            },
        })
        chart.add_series({
            'name': 'US Throughput',
            'categories': '=Data!$' + chr(posB) + '$2:$' + chr(posB) + '$' + cur_row_axis,
            'values': '=Data!$' + chr(posC) + '$2:$' + chr(posC) + '$' + cur_row_axis,
            'line': {'color': '#33CC66'},
            'smooth': True,
            'marker': {
                'type': 'circle',
                'size': 3,
                'border': {'color': 'red'},
                'fill': {'color': 'yellow'},
            },
        })
    chart.set_plotarea({
        'border': {'none': True},
        'fill': {'none': False},
        # 'gradient': {'colors': ['#BBFFFF', '#AEEEEE', '#96CDCD']}
    })

    # chart.set_legend({'none': True})
    worksheet_range.insert_chart('B' + str(posX), chart, {'x_scale': 2.5, 'y_scale': 1.2})


def write_range(mode, posA, posB, posX):
    if mode == 'DS':
        name = 'Downstream Graph'
        tp_name = 'DS Throughput'
        chart = 'chart_tx'
        color_line = '#3399FF'
        marker_type = 'diamond'
    elif mode == 'US':
        name = 'Upstream Graph'
        tp_name = 'US Throughput'
        chart = 'chart_rx'
        color_line = '#33CC66'
        marker_type = 'circle'
    chart_tx = workbook.add_chart({"type": "line"})
    chart_rx = workbook.add_chart({"type": "line"})
    chart = eval(chart)
    # insert line graph
    cur_row_axis = str(len(Att_rep) * int(ANGLE_NUM) + 1)
    # cur_row_x = str(len(Att_rep) * int(ANGLE_NUM) + 1)
    # cur_row_chart = str(len(Att_rep) * int(ANGLE_NUM) + 2)
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
        att_list_forrange = []
        posY = 2
        for att in Att_rep:
            tp = 'Data!$' + chr(posA) + '$' + str(posY)
            tp_list_forrange.append(tp)
            rssi = 'Data!$' + chr(posB) + '$' + str(posY)
            att_list_forrange.append(rssi)
            posY += int(ANGLE_NUM)
        tp_list_forrange = tuple(tp_list_forrange)
        att_list_forrange = tuple(att_list_forrange)
        tp_list_forrange = ','.join(tp_list_forrange)
        att_list_forrange = ','.join(att_list_forrange)
        tp_list_forrange = str(tp_list_forrange)
        att_list_forrange = str(att_list_forrange)
        chart.add_series({
            'name': tp_name,
            'categories': '=(' + att_list_forrange + ')',
            'values': '=(' + tp_list_forrange + ')',
            'line': ({'color': color_line}),
            'smooth': True,
            'gradient': {'colors': ['#FFE9D7', '#FFD4B2', '#FFC18B']},
            'marker': {
                'type': marker_type,
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
            'smooth': True,
            'marker': {
                'type': marker_type,
                'size': 3,
                'border': {'color': 'red'},
                'fill': {'color': 'yellow'},
            },
        })
    if mode == 'DS':
        chart.set_plotarea({
            'border': {'none': True},
            'fill': {'none': False},
            # 'gradient': {'colors': ['#FFE4CE', '#FFD4B2', '#FFC695']}
        })
    else:
        chart.set_plotarea({
            'border': {'none': True},
            'fill': {'none': False},
            # 'gradient': {'colors': ['#FFDBDB', '#FFC7C6', '#FFADAC']}
        })
    # chart.set_legend({'none': True})
    worksheet_range.insert_chart('B' + str(posX), chart, {'x_scale': 2.5, 'y_scale': 1.2})


def write_radar(posA, posE, max_tp=None):
    posB = ord('C')
    posY = 2
    posD = 2
    if posE == 'B':
        tp_type = 'DS Throughput'
        marker_type = 'circle'
        color_line = '#3399FF'
    elif posE == 'J':
        tp_type = 'US Throughput'
        marker_type = 'diamond'
        color_line = '#33CC66'
    else:
        print('Check postion')
        pass
    for att in Att_rep:
        # insert line graph
        # radar = radar_name = 'radar' + str(att)
        radar = workbook.add_chart({"type": "radar"})
        # radar = eval(radar)
        radar.set_title({
            "name": 'Attenuation=' + str(att) + 'dB'
        })
        radar.set_y_axis({
            "name": "Mbps",
            "min": 0,
            "max": max_tp,
            "major_unit": max_tp // 8,
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
                'line': {'color': color_line},
                'smooth': True,
                'gradient': {'colors': ['#FFE9D7', '#FFD4B2', '#FFC18B']},
                'marker': {
                    'type': marker_type,
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
                'fill': {'none': False},
                # 'gradient': {'colors': ['#E6DCF4', '#DED2F1', '#CBB8E9']}
            })
        else:
            radar.set_plotarea({
                'border': {'none': True},
                'fill': {'none': False},
                # 'gradient': {'colors': ['#DCF7FF', '#C3F1FF', '#A2EBFF']}
            })
        worksheet_angle.insert_chart(posE + str(posD), radar, {'x_scale': 1, 'y_scale': 1.4})
        posY += int(ANGLE_NUM)
        posD += 20


# add Auxiliary column
def addac_for_angle():
    worksheet_data.write_row('AA1', ['ac_for_angle'], head_format)
    posY = 2
    posYY = 2
    posYC = 0
    for angle in Angle:
        worksheet_data.write_formula('AA' + str(posY), '=$B$' + str(posYY) + '&"-"&C' + str(posY))
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

def set_properties():
    workbook.set_properties({
        'title': 'WIFI Performance Test Report',
        'subject': 'WIFI TEST',
        'author': 'DVT',
        'manager': 'DVT',
        'company': 'Cambridge Industries Group (CIG)',
        'category': 'Test Report',
        'keywords': 'RF, WIFI, Throughput',
        'comments': 'Created with Python and XlsxWriter'})


def book_close():
    workbook.close()


def Generate_Test_Report():
    worksheet_cover.insert_image('B1', './images/CIG.png')
    # worksheet_cover.write_blank('B1', None)
    # worksheet_cover.set_header('&L&G', {'image_left': 'CIG.png'})
    worksheet_cover.merge_range('B4:I4', 'Cambridge Industries Group (CIG)', company_format)
    # worksheet_cover.write('B4', 'Cambridge Industries Group (CIG)', company_format)
    worksheet_cover.merge_range('B5:I5', 'Partnership for the Next Generation Broadband Access', company_format)
    # worksheet_cover.write('B5', 'Partnership for the Next Generation Broadband Access', company_format)
    worksheet_cover.merge_range('B7:I7', 'WIFI Performance Test Report', report_name_format)
    # worksheet_cover.write('B9', 'StartTime', company_format)
    worksheet_cover.write('B10', 'Finish Time', company_format)
    worksheet_cover.write('C10', stop_time, info_format)
    worksheet_cover.write('B12', 'DUT(AP)', company_format)
    worksheet_cover.write('C13', 'Product', company_format)
    worksheet_cover.write('D13', AP_TYPE, info_format)
    worksheet_cover.write('C14', 'Hardware Version', company_format)
    worksheet_cover.write('C15', 'Software Version', company_format)
    worksheet_cover.write('C16', 'Operating Band', company_format)
    worksheet_cover.write('D16', RADIO, info_format)
    worksheet_cover.write('C17', '2.4G Operation Mode', company_format)
    worksheet_cover.write('C18', '2.4G Antenna Configuration', company_format)
    worksheet_cover.write('C19', '5G Operation Mode', company_format)
    worksheet_cover.write('C20', '5G Antenna Configuration', company_format)
    worksheet_cover.write('B22', 'STATION', company_format)
    worksheet_cover.write('C23', 'Station Type', company_format)
    worksheet_cover.write('D23', STA_TYPE, info_format)
    worksheet_cover.write('C24', 'Model', company_format)
    worksheet_cover.write('C25', 'Version', company_format)
    worksheet_cover.write('C26', 'Operating Band', company_format)
    worksheet_cover.write('D26', RADIO, info_format)
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
    if RUN_TPYE == 0:
        worksheet_environment.insert_image('B3', './images/OTA.PNG')
    else:
        worksheet_environment.insert_image('B3', './images/CDT.PNG')
    try:
        worksheet_environment.insert_image('M3', './images/tp.PNG')
    except:
        logger.error('No Environment Photo')
    else:
        try:
            worksheet_environment.insert_image('M3', './images/TP.PNG')
        except:
            logger.error('No Environment Photo')

    worksheet_range.write('V2', '***Note:Upstream and Downstream are based on Client***', info_format)
    if ANGLE_NUM > 1:
        worksheet_angle.write('S2', '***Note:Upstream and Downstream are based on Client***', info_format)

    try:
        rep_to_excel = Reportdata_Get()
    except:
        logger.error('No file')
    else:
        write_row()
        try:
            rep_to_excel.Ch_get()
            write_Channel()
        except:
            logger.error('No file')
        try:
            # rep_to_excel.Att_get()
            write_Attenuation()
        except:
            logger.error('No file')
        try:
            rep_to_excel.Angle_get()
            write_Angle()
        except:
            logger.error('No file')
        try:
            tx_tp = rep_to_excel.Tx_tp_get()
            posX = write_Tx()
            posX_txtp_avg = posX + 1
        except:
            logger.error('No file')
            posX += 1
            posX_txtp_avg = posX
        if ANGLE_NUM > 1:
            posX = write_avg(posX)
        try:
            rx_tp = rep_to_excel.Rx_tp_get()
            posX = write_Rx(posX)
            posX_rxtp_avg = posX + 1
        except:
            logger.error('No file')
            posX += 1
            posX_rxtp_avg = posX
        if ANGLE_NUM > 1:
            posX = write_avg(posX)
        try:
            rep_to_excel.Sta_rssi_get()
            posX = write_STA_Rssi(posX)
            posX_STARSSI_avg = posX + 1
        except:
            logger.error('No file')
            posX += 1
            posX_STARSSI_avg = posX
        if ANGLE_NUM > 1:
            posX = write_avg(posX)
        try:
            rep_to_excel.Ap_rssi_get()
            posX = write_AP_Rssi(posX)
            posX_APRSSI_avg = posX + 1
        except:
            logger.error('No file')
            posX += 1
            posX_APRSSI_avg = posX
        if ANGLE_NUM > 1:
            posX = write_avg(posX)
        try:
            rep_to_excel.Tx_rate_get()
            posX = write_Tx_Rate(posX)
        except:
            logger.error('No file')
            posX += 1
        if ANGLE_NUM > 1:
            posX = write_avg(posX)
        try:
            rep_to_excel.Rx_rate_get()
            posX = write_Rx_Rate(posX)
        except:
            logger.error('No file')
            posX += 1
        if ANGLE_NUM > 1:
            posX = write_avg(posX)
        try:
            rep_to_excel.Dura_Time_get()
            posX = write_Time(posX)
        except:
            logger.error('No file')
            posX += 1
        try:
            rep_to_excel.BW_TxRate_get()
            posX = write_TX_BW(posX)
        except:
            logger.error('No file')
            posX += 1
        try:
            rep_to_excel.NSS_TxRate_get()
            posX = write_TX_NSS(posX)
        except:
            logger.error('No file')
            posX += 1
        try:
            rep_to_excel.MCS_TxRate_get()
            posX = write_TX_MCS(posX)
        except:
            logger.error('No file')
            posX += 1
        try:
            rep_to_excel.BW_RxRate_get()
            posX = write_RX_BW(posX)
        except:
            logger.error('No file')
            posX += 1
        try:
            rep_to_excel.NSS_RxRate_get()
            posX = write_RX_NSS(posX)
        except:
            logger.error('No file')
            posX += 1
        try:
            rep_to_excel.MCS_RxRate_get()
            posX = write_RX_MCS(posX)
        except:
            logger.error('No file')
            posX += 1
        try:
            rep_to_excel.RSSI_TXANT_get()
            posX = write_TX_ANTRSSI(posX)
        except:
            logger.error('No file')
            posX += 1
        try:
            rep_to_excel.POWER_TXANT_get()
            posX = write_TX_ANTPOWER(posX)
        except:
            logger.error('No file')
            posX += 1
        try:
            rep_to_excel.RSSI_RXANT_get()
            posX = write_RX_ANTRSSI(posX)
        except:
            logger.error('No file')
            posX += 1
        try:
            rep_to_excel.POWER_RXANT_get()
            write_RX_ANTPOWER(posX)
        except:
            logger.error('No file')
            posX += 1
        try:
            write_range_att(posX_txtp_avg, 66, posX_rxtp_avg, 2)
            write_range('DS', posX_txtp_avg, posX_APRSSI_avg, 20)
            write_range('US', posX_rxtp_avg, posX_STARSSI_avg, 38)
        except:
            logger.error('No data')
        if ANGLE_NUM > 1:
            tx_tp = [float(tx.decode('ascii')) for tx in tx_tp]
            rx_tp = [float(rx.decode('ascii')) for rx in rx_tp]
            max_txtp = int(max(tx_tp)) + 100.0
            max_rxtp = int(max(rx_tp)) + 100.0
            write_radar(posX_txtp_avg - 1, 'B', max_txtp)
            write_radar(posX_rxtp_avg - 1, 'J', max_rxtp)
    set_properties()
    workbook.close()


if __name__ == "__main__":
    print('AP is ', AP_TYPE)
    Generate_Test_Report()
