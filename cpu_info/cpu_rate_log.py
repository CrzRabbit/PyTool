#!/usr/bin/python3.5
#coding=UTF-8

import os, sys
import xlwt
import re
import time
from xlwt.Formatting import Alignment, Borders

COL_WIDTH = 1000
ROW_HEIGHT = 0xFF

class record():
    def __init__(self, operation, id, channel, len, time):
        self.operation = operation
        self.id = id
        self.channel = channel
        self.len = len
        self.time = time
        self.r_rcord = None

    def __str__(self):
        return 'operation: {0} id: {1} chanel: {2} len: {3} time: {4} r_record: {5}'.format(self.operation, self.id,
                                                                              self.chanel, self.len, self.time, self.r_rcord)
class rrecord():
    def __init__(self, operation=None, start_s = None, start_ms = None, end_s = None, end_ms = None, len = 0, package_amount=0, rate=0):
        self.operation = operation
        self.start_s = start_s
        self.start_ms = start_ms
        self.end_s = end_s
        self.end_ms = end_ms
        self.len = len
        self.rate = rate
        self.package_amount = package_amount

    def set_rate(self):
        self.rate = self.len * 8

    def __str__(self):
        return 'operation: {0} start_s:{1} start_ms:{2} end_s:{3} end_ms:{4} len:{5} rate:{6}'.format(
            self.operation, self.start_s, self.start_ms, self.end_s, self.end_ms, self.len, self.rate
        )
def create_xml():
    workBook = xlwt.Workbook(encoding='utf-8')
    workSheet = workBook.add_sheet("record")
    workSheet1 = workBook.add_sheet("rate")

    workSheet.col(0).width = COL_WIDTH * 5
    workSheet.col(1).width = COL_WIDTH * 5
    workSheet.col(2).width = COL_WIDTH * 5
    workSheet.col(3).width = COL_WIDTH * 5
    workSheet.col(4).width = COL_WIDTH * 10
    workSheet.row(0).height = ROW_HEIGHT * 4

    workSheet1.col(0).width = COL_WIDTH * 8
    workSheet1.col(1).width = COL_WIDTH * 8
    workSheet1.col(2).width = COL_WIDTH * 8
    workSheet1.col(3).width = COL_WIDTH * 8

    font = xlwt.Font()
    font.bold = True
    font.colour_index = 0x09
    style = xlwt.XFStyle()
    style.font = font
    style.pattern.pattern = style.pattern.SOLID_PATTERN
    #style.pattern.pattern_back_colour = 0x0C
    style.pattern.pattern_fore_colour = 0x08
    borders = Borders()
    borders.left = Borders.MEDIUM
    borders.right = Borders.MEDIUM
    borders.top = Borders.MEDIUM
    borders.bottom = Borders.MEDIUM
    style.borders = borders
    aligment = Alignment()
    aligment.horz = Alignment.HORZ_CENTER
    aligment.vert = Alignment.VERT_CENTER
    style.alignment = aligment
    #style.alignment.wrap = Alignment.WRAP_AT_RIGHT

    content_font = xlwt.Font()
    content_style = xlwt.XFStyle()
    content_style.font = content_font
    content_style.alignment.horz = Alignment.HORZ_CENTER
    content_style.alignment.vert = Alignment.VERT_CENTER

    workSheet.write(0, 0, label="operation", style=style)
    workSheet.write(0, 1, label="id", style=style)
    workSheet.write(0, 2, label="channel", style=style)
    workSheet.write(0, 3, label="len", style=style)
    workSheet.write(0, 4, label="time", style=style)

    workSheet1.write(0, 0, label='operation', style=style)
    workSheet1.write(0, 1, label='start time', style=style)
    workSheet1.write(0, 2, label='end time(not include)', style=style)
    workSheet1.write(0, 3, label='package amount', style=style)
    workSheet1.write(0, 4, label='rate', style=style)

    return workBook, workSheet, workSheet1

def parse_log(file):

    workBook, workSheet, workSheet1 = create_xml()

    records = []
    r_rrd = None
    w_rrd = None

    r_rrecords = []
    w_rrecords = []

    r_start_s = None
    r_start_ms = None
    r_end_s = None
    r_end_ms = None
    w_start_s = None
    w_start_ms = None
    w_end_s = None
    w_end_ms = None

    r_len = 0
    w_len = 0
    r_count = 0
    w_count = 0

    log = open(file, 'r')
    lines = log.readlines()
    count = 0
    for line in lines:
        info = line.split()
        operation = 'read'
        if info.__len__() > 2 and info[2] == 'IscWrite':
            operation = 'write'
        elif info.__len__() > 2 and info[2] == 'IscRead':
            operation = 'read'
        else:
            continue

        rd = record(operation, info[5][:-1], info[8][:-1], info[11][:-1], info[14])

        s, ms = info[1][:-1].split('.')
        if operation == 'read':
            if r_start_ms == None:
                r_start_ms = ms
                r_start_s = s
                r_len = int(rd.len)
                #print('={}'.format(r_len))
                #count += 1
                r_count = 1
            elif (s > r_start_s and ms > r_start_ms) or int(s) > int(r_start_s) + 1:
                r_end_ms = ms
                r_end_s = s
                r_rrd = rrecord(operation, r_start_s, r_start_ms, r_end_s, r_end_ms, r_len, r_count)
                r_rrd.set_rate()
                r_rrecords.append(r_rrd)
                rd.r_rcord = r_rrd
                r_rrd = None
                r_start_ms = r_end_ms
                r_start_s = r_end_s
                r_end_s = None
                r_end_ms = None
                r_len = int(rd.len)
                #print('={}'.format(rd.len))
                #count += 1
                r_count = 1

            else:
                r_len += int(rd.len)
                #print('+{0} {1}'.format(rd.len, r_len))
                #count += 1
                r_count += 1

        else:
            if w_start_ms == None:
                w_start_ms = ms
                w_start_s = s
                w_len = int(rd.len)
                w_count = 1
            elif (s > w_start_s and s > w_start_ms) or int(s) > int(w_start_s) + 1:
                w_end_s = s
                w_end_ms = ms
                w_rrd = rrecord(operation, w_start_s, w_start_ms, w_end_s, w_end_ms, w_len, w_count)
                w_rrd.set_rate()
                w_rrecords.append(w_rrd)
                rd.r_rcord = w_rrd
                w_rrd = None
                w_start_ms = w_end_ms
                w_start_s = w_end_s
                w_end_s = None
                w_end_ms = None
                w_len = int(rd.len)
                w_count = 1
            else:
                w_len += int(rd.len)
                w_count += 1

        records.append(rd)
        rd = None

    row = 1
    for rd in records:
        workSheet.write(row, 0, rd.operation)
        workSheet.write(row, 1, int(rd.id))
        workSheet.write(row, 2, int(rd.channel))
        workSheet.write(row, 3, int(rd.len))
        workSheet.write(row, 4, float(rd.time))
        if rd.r_rcord:
            workSheet.write(row, 5, int(rd.r_rcord.len))
        row += 1

    row = 1
    for r_rrd in r_rrecords:
        workSheet1.write(row, 0, r_rrd.operation)
        workSheet1.write(row, 1, float(r_rrd.start_s + '.' + r_rrd.start_ms))
        workSheet1.write(row, 2, float(r_rrd.end_s + '.' + r_rrd.end_ms))
        workSheet1.write(row, 3, r_rrd.package_amount)
        workSheet1.write(row, 4, r_rrd.rate)
        row += 1

    for w_rrd in w_rrecords:
        workSheet1.write(row, 0, w_rrd.operation)
        workSheet1.write(row, 1, float(w_rrd.start_s + '.' + w_rrd.start_ms))
        workSheet1.write(row, 2, float(w_rrd.end_s + '.' + w_rrd.end_ms))
        workSheet1.write(row, 3, w_rrd.package_amount)
        workSheet1.write(row, 4, w_rrd.rate)
        row += 1

    workBook.save(file.split('.')[0]+'.xls')

if __name__ == '__main__':
    os.chdir('./log/')
    # for file in os.listdir('./'):
    #     if os.path.isfile(file):
    #         parse_log(file)
    parse_log('carplay.txt')
    parse_log('setting_cut.txt')
    parse_log('telnumberSync.txt')
    parse_log('usb_music.txt')