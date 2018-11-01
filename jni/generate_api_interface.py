test1 = open('test1', 'r')
jni_interface = list()
for line in test1.readlines():
    if 'static' == line.split(' ')[0]:
        p1, p2 = line.split('(')
        ret = p1.split(' ')[1]
        function_name = p1.split(' ')[2]
        p2 = p2.split(')')[0]
        paras = dict()
        types = list()
        p_names = list()
        for para in p2.split(','):
            l = len(para.split(' '))
            if l == 2:
                t1, t2 = para.split(' ')
                types.append(t1)
                p_names.append(t2)
            elif l == 3:
                t1, t2, t3 = para.split(' ')
                types.append(t2)
                p_names.append(t3)
            elif l == 4:
                t1, t2, t3, t4 = para.split(' ')
                types.append(t2 + ' ' + t3)
                p_names.append(t4)
        types = types[2:]
        print(function_name, types, p_names)
        jni_i = '''    {"''' + function_name + '''", "('''
        for type in types:
            if type == 'jboolean':
                jni_i += 'Z'
            if type == 'jbyte':
                jni_i += 'B'
            if type == 'jint':
                jni_i += 'I'
            if type == 'jstring':
                jni_i += 'Ljava/lang/String;'

        jni_i += ')'
        if ret == 'jboolean':
            jni_i += 'Z'
        if ret == 'jbyte':
            jni_i += 'B'
        if ret == 'jint':
            jni_i += 'I'
        if ret == 'jstring':
            jni_i += 'Ljava/lang/String;'
        if ret == 'bool':
            jni_i += 'Z'
        if ret == 'void':
            jni_i += 'V'
        jni_i += '''", (void*)''' + function_name + '''},
'''
        jni_interface.append(jni_i)

jni_dec = open('jni_dec', 'w')
jni_dec.writelines(jni_interface)
jni_dec.close()