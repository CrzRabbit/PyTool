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
    def __init__(self, busy_time=None, total_time=None, totalCpuUsage=None, p_name=None, t_name=None, id=None, usr_cpu=None, sys_cpu=None, usage=None):
        self.busy_time = busy_time
        self.total_time = total_time
        self.totalCpuUsage = totalCpuUsage
        self.p_name = p_name
        self.t_name = t_name
        self.id = id
        self.usr_cpu = usr_cpu
        self.sys_cpu = sys_cpu
        self.usage = usage

'''   def __str__(self):
        return 'operation: {0} id: {1} chanel: {2} len: {3} time: {4} r_record: {5}'.format(self.operation, self.id,
                                                                              self.channel, self.len, self.time, self.r_rcord)
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
        )'''

def create_xml():
    workBook = xlwt.Workbook(encoding='utf-8')
    workSheet = workBook.add_sheet("cpu_rate")

    workSheet.col(0).width = COL_WIDTH * 3
    workSheet.col(1).width = COL_WIDTH * 3
    workSheet.col(2).width = COL_WIDTH * 5
    workSheet.col(3).width = COL_WIDTH * 5
    workSheet.col(4).width = COL_WIDTH * 5
    workSheet.col(5).width = COL_WIDTH * 5
    workSheet.col(6).width = COL_WIDTH * 5
    workSheet.col(7).width = COL_WIDTH * 5
    workSheet.col(8).width = COL_WIDTH * 5
    workSheet.row(0).height = ROW_HEIGHT * 4

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

    workSheet.write(0, 0, label="busy time", style=style)
    workSheet.write(0, 1, label="total time", style=style)
    workSheet.write(0, 2, label="totalCpuUsage", style=style)
    workSheet.write(0, 3, label="process name", style=style)
    workSheet.write(0, 4, label="thread name", style=style)
    workSheet.write(0, 5, label="pid/tid", style=style)
    workSheet.write(0, 6, label="user cpu", style=style)
    workSheet.write(0, 7, label="sys cpu", style=style)
    workSheet.write(0, 8, label="usage", style=style)

    return workBook, workSheet

def parse_log(file):

    workBook, workSheet = create_xml()

    records = []

    log = open(file, 'r')
    lines = log.readlines()
    count = 0

    for line in lines:
        if re.search(r'busy time', line.split(',')[0]):
            l = []
            for part in line.split(','):
                l.append(part.split(': ')[1])
            l[2] = l[2][:-1]
            records.append(record(l[0],l[1],l[2]))

        if re.search(r'prceoss name', line.split(',')[0]):
            l = []
            for part in line.split(','):
                l.append(part.split(': ')[1])
            l[4] = l[4][:-1]
            records.append(record(None,None,None,l[0],None,l[1],l[2],l[3],l[4]))

        if re.search(r'thread name',line.split(',')[0]):
            l = []
            for part in line.split(','):
                l.append(part.split(': ')[1])
            l[4] = l[4][:-1]
            records.append(record(None,None,None,None,l[0],l[1],l[2],l[3],l[4]))

    row = 1
    for rd in records:
        if rd.busy_time:
            workSheet.write(row, 0, rd.busy_time)
        if rd.total_time:
            workSheet.write(row, 1, rd.total_time)
        if rd.totalCpuUsage:
            workSheet.write(row, 2, rd.totalCpuUsage)
        if rd.p_name:
            workSheet.write(row, 3, rd.p_name)
        if rd.t_name:
            workSheet.write(row, 4, rd.t_name)
        if rd.id:
            workSheet.write(row, 5, int(rd.id))
        if rd.usr_cpu:
            workSheet.write(row, 6, int(rd.usr_cpu))
        if rd.sys_cpu:
            workSheet.write(row, 7, int(rd.sys_cpu))
        if rd.usage:
            workSheet.write(row, 8, float(rd.usage))
        row += 1

    workBook.save(file.split('.')[0]+'.xls')

if __name__ == '__main__':
    parse_log('cpu_info')