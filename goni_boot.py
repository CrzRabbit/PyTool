import platform
import shutil
import os
import re

# print(platform.system())

platform = platform.system()
splitmark = ''
if platform == "Linux":
    splitmark = '/'
else:
    splitmark = '\\'
abspath = os.path.abspath('.')
os.chdir('goni_reboot')
currentpath = '.'
count = 0

def find_dt_log(currentpath):
    global count
    for name in os.listdir(currentpath):
        if name == 'TRC_LINUX_BT.dat':
            temp = ''
            for menu in currentpath.split(splitmark):
                if menu != '.':
                    if temp == '':
                        temp = menu
                    else:
                        temp = temp + '#' + menu
            shutil.copyfile(currentpath + splitmark + name, abspath + splitmark + 'goni_reboot' + splitmark + temp +'#' + name)
            count += 1
            print('{}'.format(count) + ': ' + abspath + splitmark + temp + name)
        else:
            find_dt_log(currentpath + splitmark + name)

def put_dt_log(currentpath):
    global count
    for name in os.listdir(currentpath):
        if os.path.isfile(name):
            temp = '.'
            for menu in name.split('#'):
                temp = temp + splitmark + menu
            count += 1
            print('{}'.format(count) + ' ' + name + ': ' + temp)
            #shutil.copyfile(name, temp)

def change_file(currentpath):
    for name in os.listdir(currentpath):
        if os.path.isfile(name):
            temp = '.'
            for menu in name.split('#'):
                if re.search(r'TRC_LINUX_BT.dat', menu):
                    n = re.search(r'TRC_LINUX_BT.dat', menu).start()
                    # print(re.search(r'TRC_LINUX_BT.dat', menu).start())
                    temp = temp + splitmark + menu[:n] + splitmark + menu[n:-4] + '.txt'
                else:
                    temp = temp + splitmark + menu
            #os.rename(name, temp)
            #print(name + ' ' + temp)
            shutil.copyfile(name, temp)

if __name__ == '__main__':
    #find_dt_log(currentpath)
    #put_dt_log(currentpath)
    change_file(currentpath)