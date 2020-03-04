#!/user/bin/env python
# encoding: utf-8
# @time      : 2019/8/9 10:54

__author__ = 'Ethan'

from xlsxwriter import Workbook
import csv
import time
import os
import sys
import re

try:
    filename = sys.argv[1]
except:
    filename = input('Input the csv filename:')

now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
filename = re.sub('.csv', '', filename)
report_name = filename + ".xlsx"
print('Report:', report_name)
workbook: Workbook = Workbook('./Report/' + report_name)

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

# COVER
worksheet_cover = workbook.add_worksheet("Overview")
worksheet_cover.hide_gridlines(2)
worksheet_cover.set_column('B:B', 18)
worksheet_cover.set_column('C:C', 24)
worksheet_cover.set_column('D:D', 35)
worksheet_cover.set_row(7, 35)
worksheet_cover.insert_image('B1', './images/CIG.png')
worksheet_cover.merge_range('B4:I4', 'Cambridge Industries Group (CIG)', company_format)
worksheet_cover.merge_range('B5:I5', 'Partnership for the Next Generation Broadband Access', company_format)
worksheet_cover.merge_range('B7:I7', 'WIFI Performance Test Report', report_name_format)
worksheet_cover.write('B10', 'Finish Time', company_format)
worksheet_cover.write('C10', now_time, info_format)
worksheet_cover.write('B12', 'DUT', company_format)
worksheet_cover.write('C12', '', info_format)
worksheet_cover.write('B13', 'Hardware Version', company_format)
worksheet_cover.write('C13', '', info_format)
worksheet_cover.write('B14', 'Software Version', company_format)
worksheet_cover.write('C14', '', info_format)
worksheet_cover.write('B15', 'Test Tools', company_format)
worksheet_cover.write('C15', '', info_format)
worksheet_cover.write('B16', 'Tester', company_format)
worksheet_cover.write('C16', '', info_format)
worksheet_cover.write('B18', 'TEST RESULT', company_format)
worksheet_cover.write('C18', 'PASS', info_format)

# contents
worksheet_contents = workbook.add_worksheet("Contents")
worksheet_contents.hide_gridlines(2)
contents_title = ['Test Article', 'Test Items', 'Test Result', 'Comments']
worksheet_contents.write_row("A1", contents_title, head_format)

worksheet_environment = workbook.add_worksheet("Environment")
worksheet_environment.hide_gridlines(2)
worksheet_environment.write('B1', 'TEST DIAGRAM AND ENVIRONMENT', company_format)
worksheet_environment.insert_image('B3', './images/OTA.PNG')
worksheet_environment.insert_image('B3', './images/OTA.PNG')

worksheet_data = workbook.add_worksheet("Data")
worksheet_data.hide_gridlines(2)

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


if __name__ == "__main__":
    directory = os.path.exists(r'./Report')
    if directory is False:
        os.makedirs('Report')
    posX = ord('C')
    try:
        print(filename)
        dut_file = csv.reader(open('Result/' + filename + '.csv'))
        for x, col in enumerate(dut_file):
            if x > 2:
                col = float(col[1])
                print(col)
                # colum.append(col)
        # write_value(posX)
        # posX += 1
        posY = 2

    except Exception as err:
        print('no file ' + filename)
    workbook.close()
