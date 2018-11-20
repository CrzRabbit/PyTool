import re

f = open('test2', 'r')
lines = f.readlines()
f.close()

functions = list()

for line in lines:
    parts = line.split(' ')

    ret = ''
    function_name = ''
    stub = 'BTSTUB'
    types = list()
    params = list()

    function = None
    temp_function_name = None

    #print(parts)
    for i in range(0, parts.__len__()):
        if i == 0:
            if len(parts[i]) > 1:
                ret = parts[i]
        elif i == 1:
            ps = parts[i].split('(')
            function_name = ps[0]
            if i != parts.__len__() - 1:
                types.append(ps[1])
        elif i % 2 == 0 and i != parts.__len__() - 1:
            if re.search(r',$', parts[i]):
                params.append(parts[i][:-1])
            else:
                params.append(parts[i])
        elif i % 2 == 1 and i != parts.__len__() - 1:
            types.append(parts[i])
        elif i == parts.__len__() - 1:
            params.append(parts[i].split(')')[0])

    if ret == '':
        continue

    #print(ret, function_name, types, params)
    if re.match(r'^BTIFAdapter|^BTIFHandfree|^BTIFPhonebook|^BTIFAudio', function_name):
        start = re.match(r'^BTIFAdapter|^BTIFHandfree|^BTIFPhonebook|^BTIFAudio', function_name).span()[1]
        temp_function_name = function_name[start:]
        temp_function_name = temp_function_name[0].lower() + temp_function_name[1:]
        temp_function_name += 'Native'
    #print(temp_function_name)
    else:
        temp_function_name = function_name + 'Native'

    if re.match(r'^BTAudio', function_name):
        stub = 'BTAUDIOSTUB'

    function = '''static '''
    if ret == 'void':
        ret = 'bool'
    elif ret == 'int32_t':
        ret = 'jint'
    elif ret == 'int8_t':
        ret = 'jbyte'
    elif ret == 'android::String8':
        ret = 'jstring'
    else:
        ret = 'jobject'
    function += ret

    function += ''' ''' + temp_function_name + '''(JNIEnv* env, jobject obj'''

    for i in range(0, types.__len__()):
        function += ''', '''
        if types[i] == 'bool':
            types[i] = 'jboolean'
        elif types[i] == 'int8_t':
            types[i] = 'jbyte'
        elif types[i] == 'int32_t':
            types[i] = 'jint'
        elif types[i] == '::android::String8&':
            types[i] = 'jstring'
        function += types[i]
        function += ''' ''' + params[i]
    function += ''')
{
    ALOGD("%s", __func__);
    '''
    for i in range(0, types.__len__()):
        if types[i] == 'jstring':
            function += '''const char* c''' + (params[i][0].upper() + params[i][1:]) + ''' = NULL;
    if (''' + params[i] + ''' != NULL) {
        c''' + (params[i][0].upper() + params[i][1:]) + ''' = env->GetStringUTFChars(''' + params[i] + ''', NULL);
    }
    android::String8 m''' + (params[i][0].upper() + params[i][1:]) + '''(c''' + (params[i][0].upper() + params[i][1:]) + ''');
    '''
            params[i] = 'm' + (params[i][0].upper() + params[i][1:])
        if types[i] == 'jboolean':
            params[i] = params[i] + ' == JNI_TRUE ? 1 : 0'

    transfer = stub + '''->''' + function_name

    if params.__len__() == 0:
        transfer += '''();'''
    else:
        transfer += '''('''
        for i in range(0, params.__len__()):
            transfer += params[i]
            if i == params.__len__() - 1:
                transfer += ''');'''
            else:
                transfer += ''', '''

    if ret == 'jstring':
        function += '''android::String8 mTemp = ''' + transfer + '''
    jstring temp = env->NewStringUTF(mTemp.String());
    return temp;
}

'''

    elif ret == 'jbyte' or ret == 'jint':
        function += '''return ''' + transfer + '''
}

'''
    elif ret == 'bool':
        function += transfer + '''
    return JNI_TRUE;
}

'''
    elif ret == 'jobject':
        function += '''//TODO: return jobject

    ''' + transfer + '''
}

'''
    functions.append(function)

t = open('functions', 'w')
t.writelines(functions)
t.close()
print(str(1))

