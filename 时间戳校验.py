import time

def timeStr_to_time(time_str, structure="年/月/日-时:分:秒"):

    structure_dict = {
        '年':'%Y',
        '月':'%m',
        '日':'%d',
        '时':'%H',
        '分':'%M',
        '秒':'%S'
    }

    keys = structure_dict.keys()

    structure_str = ''
    for i in structure:
        if i in keys:
            structure_str += structure_dict[i]
        else:
            structure_str += i

    return time.mktime(time.strptime(time_str, structure_str))

if (time.time() <= timeStr_to_time('2026/6/7-23:59:59')):
    pass
