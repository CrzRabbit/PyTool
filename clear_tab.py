
file = open('legithost.py', 'r')
lines = file.readlines()
for i, l in enumerate(lines):
    index = 0
    while True:
        if(l[index] == '\t'):
            print(i)
            l = '{0}    {1}'.format(l[:index], l[index + 1:])
            index += 4
        else:
            break

file1 = open('', 'w')
file1.writelines(lines)

file.close()
file1.close()