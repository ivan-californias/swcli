import json

def _print_txt_dict(d, fields):
    line = []
    for k in d:
        if not fields or k in fields:
            if type(d[k]) is list:
                line.append('%s: %s' % (k, d[k]))
            else:
                line.append('%s: "%s"' % (k, d[k]))
    print(', '.join(line))

def _print_txt_list(l, fields):
    for i in l:
        _print_txt_dict(i, fields)

def _print_text(data, fields):
    if type(data) is list:
        _print_txt_list(data, fields)
    elif type(data) is dict:
        _print_txt_dict(data, fields)
    else:
        print(data)

def _filter_obj_fields(data, fields):
    obj = {}
    for field in fields:
        if field in data:
            obj[field] = data[field]
    return obj

def _print_json(data, fields):
    if fields:
        print_data = []
        if type(data) is list:
            for item in data:
                print_data.append(_filter_obj_fields(item, fields))
        elif type(data) is dict:
            print_data = _filter_obj_fields(data, fields)

        print(json.dumps(print_data, indent=4, sort_keys=True))
    else:
        print(json.dumps(data, indent=4, sort_keys=True))

def _print_list(data, fields):
    for item in data:
        print('- %s' % item['url'])
        for key in item:
            if not fields or key in fields:
                print('  - %s: %s' % (key, item[key]))

def print_data(data, fmt, fields=[]):
    if fmt == 'json':
        _print_json(data, fields)
    elif fmt == 'list':
        _print_list(data, fields)
    else:
        _print_text(data, fields)

    
