import sys, os, re
file = ''
def remove_number(file):
    p = open(file, 'r')
    lines = p.readlines()
    temp_lines = list()
    for line in lines:
        for index in range(0, len(line)):
            if line[index] >= '0' and line[index] <= '9':
                continue
            else:
                temp_lines.append(line[index:])
                break
    pt = open('temp' + file, 'w')
    pt.writelines(temp_lines)
    p.close()
    pt.close()

if __name__ == '__main__':
    for file in os.listdir('.'):
        if os.path.isfile(file) and file != 'copy.py' and re.match(r'^temp*', file) == None:
            remove_number(file)
