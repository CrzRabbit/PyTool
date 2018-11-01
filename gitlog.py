#!/usr/bin/python3.5
#coding=UTF-8

import os, sys
import xlwt
import re
import time
from xlwt.Formatting import Alignment, Borders

PROJECT_PATH = "/home/wangjiangchuan/BlueTooth/SuntecBt"
BASE_BRANCH_NAME = "master"
TARGET_BRANCH_NAME = "master"
MAX_AMOUNT = 50
RESULT_NAME = "master_master_branch_diff.xls"

year = int(time.strftime("%4Y"))
month = int(time.strftime("%2m"))
day = int(time.strftime("%2d"))

#SINCE_TIME = "{0}/{1}/{2}".format(year, (month + 9) % 12 + 1, day)
SINCE_TIME = "2018/1/1"

max_amount = MAX_AMOUNT
base_branch_name = BASE_BRANCH_NAME
target_branch_name = TARGET_BRANCH_NAME
since_time = SINCE_TIME
result_name = RESULT_NAME

help_info = '''
    eg: ./gitlog.py -t 2018/7/7 -m 10 -b master bluetec2
        -t: 指定时间 默认两个月前
        -m: 指定数量 默认50
        -b: 指定base和target分支 默认都是master
        '''

COL_WIDTH = 1000
ROW_HDEGHT = 0xFF

'''9 files changed, 156 insertions(+), 10 deletions(-)'''
INC_RE_MODULE = r"\s\d+\sinsertion\w*\(\+\)"
DEC_RE_MODULE = r"\s\d+\sdeletion\w*\(\-\)"

'''
    workSheet.write(0, 0, label="担当", style=style)
    workSheet.write(0, 1, label="commitSubject", style=style)
    workSheet.write(0, 2, label="commit time", style=style)
    workSheet.write(0, 3, label="branch", style=style)
    workSheet.write(0, 4, label="commitID", style=style)
    workSheet.write(0, 5, label="changefile", style=style)
    workSheet.write(0, 6, label="add/delete line", style=style)
'''

class Commit():
    def __init__(self, author, commit_subject, commit_time,
                 branch, commit_ID, change_file, add_delete_line):
        self.author = author
        self.commit_subject = commit_subject
        self.commit_time = commit_time
        self.branch = branch
        self.commit_ID = commit_ID
        self.change_file = change_file
        self.add_delete_line = add_delete_line
    def get_info(self):
        return (self.author, self.commit_subject, self.commit_time,
                self.branch, self.commit_ID, self.change_file, self.add_delete_line)

    test = {"author": "", "commit_subject": "", "commit_time": "",
            "branch": "", "commit_ID": "", "change_file": "", "add_delete_line": ""}

def get_commits(amount, time, branch):
    # cmd = "git log -50 --pretty=format:'%an%n%s%n%cd%n%H' --date=format:'%4Y/%2m/%2d %2H:%2M:%2S' --stat master"
    cmd = "git log -{0} --pretty=format:'%n%an%n%s%n%cd%n%H' --date=format:'%4Y/%2m/%2d %2H:%2M:%2S' --since={1} --stat {2} > ret.txt".format(
        amount, time, branch)
    print(cmd)
    os.system(cmd)
    # add flag for end
    os.system("echo \"\n\" >> ret.txt")
    f = open("ret.txt")
    lines = f.readlines()
    row = 1
    col = 0
    temp = ""
    ret = {}
    commits = []
    inc_ret = 0
    dec_ret = 0
    for line in lines:
        line = line[:-1]
        if line.__len__() == 0:
            if col != 0:
                if col == 5:
                    # workSheet.write(row, 6, label="+0/-0", style=content_style)
                    ret[5] = None
                    ret[6] = None
                # workSheet.write(row, 5, label=temp)
                ret[5] = temp
                temp = ""
                row = row + 1
                col = 0
                inc_ret = 0
                dec_ret = 0
                if ret[6]:
                    commits.append(Commit(ret[0], ret[1], ret[2], ret[3], ret[4], ret[5], ret[6]))
                ret = {}
            continue
        if re.search(INC_RE_MODULE, line):
            incs = re.search(INC_RE_MODULE, line).group()
            inc_ret = incs.split(' ')[1]
            col = 6
        if re.search(DEC_RE_MODULE, line):
            decs = re.search(DEC_RE_MODULE, line).group()
            dec_ret = decs.split(' ')[1]
            col = 6
        if col == 6:
            # workSheet.write(row, col, label="+{0}/-{1}".format(inc_ret, dec_ret), style=content_style)
            ret[col] = "+{0}/-{1}".format(inc_ret, dec_ret)
            col += 1
            continue
        if col == 5 and line.__len__() != 0:
            if temp.__len__() == 0:
                temp = temp + line.split(' ')[1]
            else:
                temp = temp + "\n" + line.split(' ')[1]
            continue
        if col == 3:
            # workSheet.write(row, col, label=branch, style=content_style)
            ret[col] = branch
            col = col + 1
        # workSheet.write(row, col, label=line, style=content_style)
        ret[col] = line
        col = col + 1

    f.close()
    os.system("rm ret.txt")
    return commits

def branch_diff(base_commits, target_commits):

    diff_commits = []
    found = False
    for t_commit in target_commits:
        for b_commit in base_commits:
            if (t_commit.commit_subject == b_commit.commit_subject) and \
                (t_commit.add_delete_line == b_commit.add_delete_line):
                found = True
                break
        if not found:
            diff_commits.append(t_commit)
            found = False
    return diff_commits

if __name__ == "__main__":

    index = 1
    while index < sys.argv.__len__():
        if sys.argv[index] == "-b":
            base_branch_name = sys.argv[index + 1]
            target_branch_name = sys.argv[index + 2]
            index += 2
        elif sys.argv[index] == "-m":
            max_amount = sys.argv[index + 1]
            index += 1
        elif sys.argv[index] == "-t":
            since_time = sys.argv[index + 1]
            index += 1
        elif sys.argv[index] == "-h" or sys.argv[index] == "--help":
            print(help_info)
            exit(1)
        else:
            print("错误的参数")
            print(help_info)
            exit(1)
        index += 1

    workBook = xlwt.Workbook(encoding='utf-8')
    workSheet = workBook.add_sheet("commit messages")
    workSheet.col(0).width = COL_WIDTH * 5
    workSheet.col(1).width = COL_WIDTH * 14
    workSheet.col(2).width = COL_WIDTH * 7
    workSheet.col(3).width = COL_WIDTH * 6
    workSheet.col(4).width = COL_WIDTH * 14
    workSheet.col(5).width = COL_WIDTH * 6
    workSheet.col(6).width = COL_WIDTH * 5
    workSheet.row(0).height = ROW_HDEGHT * 4

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

    workSheet.write(0, 0, label="担当", style=style)
    workSheet.write(0, 1, label="commitSubject", style=style)
    workSheet.write(0, 2, label="commit time", style=style)
    workSheet.write(0, 3, label="branch", style=style)
    workSheet.write(0, 4, label="commitID", style=style)
    workSheet.write(0, 5, label="changefile", style=style)
    workSheet.write(0, 6, label="add/delete line", style=style)

    base_commits = get_commits(max_amount, since_time, base_branch_name)
    target_commits = get_commits(max_amount, since_time, target_branch_name)

    diff_commits = branch_diff(base_commits, target_commits)

    row = 1
    col = 0
    for commit in diff_commits:
        workSheet.write(row, 0, commit.author)
        workSheet.write(row, 1, commit.commit_subject)
        workSheet.write(row, 2, commit.commit_time)
        workSheet.write(row, 3, commit.branch)
        workSheet.write(row, 4, commit.commit_ID)
        workSheet.write(row, 5, commit.change_file)
        workSheet.write(row, 6, commit.add_delete_line)
        row += 1
    result_name = "{0}_{1}_branch_diff.xls".format(base_branch_name, target_branch_name)
    workBook.save(result_name)