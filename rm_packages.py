import re

file = open('a1.txt', 'r')
file2 = open('aa.txt', 'w')

for line in file.readlines():
    packagename = re.match(r'^\w*[-]*\w*[-]*\w*', line)
    packageversion = re.search(r'[0-9]+[.]*[0-9]*[.]*[0-9]*', line)
    # if packagename != None and packageversion != None:
    #     print(packagename.group(0) + "==" + packageversion.group(0))
    file2.write(packagename.group(0) + "==" + packageversion.group(0) + '\n')

# for line in file2.readlines():
#     print(line)