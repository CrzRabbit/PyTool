#-*- encoding:UTF-8 -*-
import re

#test中存放函数的声明
f = open('test', 'r')
#函数
functions = list()
#声明
function_dec = list()
#stub里面的定义
function_stub = list()
#bt_callbacks_t结构体定义
struct_dec = list()
#jni回调的定义
function_names = list()
#methodid声明
method_callbacks_dec = list()
#从java获取的method
get_callbacks = list()

for line in f.readlines():
    p1, p2 = line.split('(')
    function_name = p1.split(' ')[1]
    p2 = p2.split(')')[0]
    paras = dict()
    types = list()
    p_names = list()
    m_cb = '''static jmethodID method_'''
    g_cb = '''  method_'''
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

    if re.match(r'^audio', function_name):
        stub_name = 'BtAudioStub::'
    else:
        stub_name = 'BtStub::'
    func_stub = 'void ' + stub_name + function_name + '('
    i = 0
    j = len(types)
    for type in types:
        if i == 0 and j != 1:
            func_stub += types[i] + ' ' + p_names[i] + ','
        elif i == 0 and j == 1:
            func_stub += types[i] + ' ' + p_names[i]
        elif i == j - 1:
            func_stub += ' ' + types[i] + ' ' + p_names[i]
        else:
            func_stub += ' ' + types[i] + ' ' + p_names[i] + ','
        i += 1
    func_stub += ''')
{'''
    i = 0
    t_names = list(p_names)
    for type in types:
        if p_names[i] == 'addr':
            t_names[i] = 'saddr'
            func_stub += '''
    android::String8 saddr;
    BtConversion::bdAddrToStr(addr, saddr);'''
            break
        i += 1
    func_stub += '''
    sBluetoothCallbacks->''' + function_name + '('

    i = 0
    j = len(types)
    for type in types:
        if i == 0 and j != 1:
            func_stub += t_names[i] + ','
        elif i == 0 and j == 1:
            func_stub += t_names[i]
        elif i == j - 1:
            func_stub += ' ' + t_names[i]
        else:
            func_stub += ' ' + t_names[i] + ','
        i += 1
    func_stub += ''');'''
    func_stub += '''
}

'''
    function_stub.append(func_stub)
    m_cb += function_name +''';
'''
    g_cb += function_name + ''' =
        env->GetMethodID(jniCallbackClass, "''' + function_name + '''", "('''
    func = 'static void ' + function_name + '('
    dec = 'typedef void (*' +function_name + '_callback)('
    st_dec = '''    ''' + function_name + '_callback ' + function_name + ''';
'''
    struct_dec.append(st_dec)
    func_name = '    ' + function_name + ''',
    '''
    function_names.append(func_name)
    i = 0
    j = len(types)
    for type in types:
        if p_names[i] == 'addr':
            types[i] = 'android::String8&'
        if i == 0 and j != 1:
            func += types[i] + ' ' + p_names[i] + ','
            dec += types[i] + ' ' + p_names[i] + ','
        elif i == 0 and j == 1:
            func += types[i] + ' ' + p_names[i]
            dec += types[i] + ' ' + p_names[i]
        elif i == j - 1:
            func += ' ' + types[i] + ' ' + p_names[i]
            dec += ' ' + types[i] + ' ' + p_names[i]
        else:
            func += ' ' + types[i] + ' ' + p_names[i] + ','
            dec += ' ' + types[i] + ' ' + p_names[i] + ','
        i += 1
    dec += ''');
'''
    for type in types:
        if type == 'int8_t':
            g_cb += 'B'
        elif type == 'android::String8&':
            g_cb += 'Ljava/lang/String;'
        elif type == 'bool':
            g_cb += 'Z'
        elif type == 'int32_t':
            g_cb += 'I'
    g_cb += ''')V");
'''
    func += '''){
    CallbackEnv sCallbackEnv(__func__);
    if (!sCallbackEnv.valid()) return;
    
'''
    i = 0
    for type in types:
        if p_names[i] == 'addr':
            type = 'android::String8&'
        if type == 'android::String8&':
            name = p_names[i]
            mname = 'm' + name
            p_names[i] = mname
            func += '''    '''
            func += 'jstring ' + mname + ' = sCallbackEnv->NewStringUTF(' + name + '.string());' + '\n'
        i += 1

    func += '''    '''
    func += '''sCallbackEnv->CallVoidMethod(sJniCallbacksObj, method_''' + function_name
    for n in p_names:
        func += ', ' + n
    func += ''');
}

'''
    #print(func)
    functions.append(func)
    function_dec.append(dec)
    method_callbacks_dec.append(m_cb)
    get_callbacks.append(g_cb)


result = open('result', 'w')
result.writelines(functions)
result.close()

func_dec = open('function_dec', 'w')
func_dec.writelines(function_dec)
func_dec.close()

str_dec = open('struct_dec', 'w')
str_dec.writelines(struct_dec)
str_dec.close()

func_s = open('function_stub', 'w')
func_s.writelines(function_stub)
func_s.close()

func_n = open('function_name', 'w')
func_n.writelines(function_names)
func_n.close()

method_dec = open('method_callbacks_dec', 'w')
method_dec.writelines(method_callbacks_dec)
method_dec.close()

get_cb = open('get_callbacks', 'w')
get_cb.writelines(get_callbacks)
get_cb.close()

f.close()
