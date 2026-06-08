import time

def timeStr_to_time(time_str, structure="年/月/日-时:分:秒"):

    dict_ = {
        '年':'%Y',
        '月':'%m',
        '日':'%d',
        '时':'%H',
        '分':'%M',
        '秒':'%S'
    }

    keys = dict_.keys()

    str_ = ''
    for i in structure:
        if i in keys:
            str_ += dict_[i]
        else:
            str_ += i

    return time.mktime(time.strptime(time_str, str_))

if (time.time() <= timeStr_to_time('2026/6/7-23:59:59')):
    pass