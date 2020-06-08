import m18_lab_2_6

def from_py_to_json(obj, tabs):
    name = obj.__class__.__name__
    try:
        if(name == 'bool'):
            return get_bool(obj)
        if(name == 'int'):
            return get_number(obj)
        if(name == 'NoneType'):
            return 'null' 
        if(name == 'float'):
            return get_number(obj)  
        if(name == 'list' or name == 'tuples'):
            return object_writer(obj, tabs, False)
        if(name == 'dict'):
            return object_writer(obj, tabs)   
        if(name == 'str'):
            return get_str(obj)
    except:
        raise TypeError('Wrong data')

def get_tabs(count):
    return '  ' * count

def get_key(key):
    return ('"' + key + '": ')

def get_bool(obj):
    if(obj):
        return ('true')
    else:
        return ('false')

def get_number(obj):
    if(obj == float('-inf')):
        return '-Infinity'
    if(obj == float('inf')):
        return 'Infinity'
    if(obj == float('nan')):
        return 'NaN'
    return (str(obj))

def get_str(obj):
    return ('"' + obj + '"')


def object_writer(obj, tabs, flag = True):
    result = ''
    if(flag):
        result += ('{\n')
    else:
        result += ('[\n')
    tabs+=1
    inner = []
    if(flag):
        for k, v in obj.items():
            key = get_key(k)
            value = from_py_to_json(v, tabs)
            inner.append(get_tabs(tabs) + key + value)
    else:
        for v in obj:
            value = from_py_to_json(v, tabs)
            inner.append(get_tabs(tabs) + value)
    if(flag):
        return result + ',\n'.join(inner) + '\n' + get_tabs(tabs - 1) + '}'
    else:
        return result + ',\n'.join(inner) + '\n' + get_tabs(tabs - 1) + ']'



def to_json(obj, flag):
    if flag:
        file = open('json.txt','w+')
        tabs = 0
        if(obj.__class__.__name__ == 'dict'):
            file.write(object_writer(obj, tabs))
        else:
            if(obj.__class__.__name__ == 'list' or obj.__class__.__name__ == 'tuples'):
                file.write(object_writer(obj, tabs, False))
            else:
                file.write(from_py_to_json(obj, tabs))
        file.close()
    else:
        tabs = 0
        if(obj.__class__.__name__ == 'dict'):
            return object_writer(obj, tabs)
        else:
            if(obj.__class__.__name__ == 'list' or obj.__class__.__name__ == 'tuples'):
                return object_writer(obj, tabs, False)
            else:
                return from_py_to_json(obj, tabs)

print(to_json(m18_lab_2_6.from_json('testjson.txt', True), True))
