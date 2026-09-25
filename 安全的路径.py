#标准文件名应为 -> 'path.py'

import os
import re
from typing import Literal
from pathlib import Path

#[常量] 非法字符列表
Lib_Path_illegal_chars = [
    '<', '>', ':', '"', '/', '\\', '|', '?', '*',
    '\x00', '\x01', '\x02', '\x03', '\x04', '\x05',
    '\x06', '\x07', '\x08', '\x09', '\x0a', '\x0b',
    '\x0c', '\x0d', '\x0e', '\x0f', '\x10', '\x11',
    '\x12', '\x13', '\x14', '\x15', '\x16', '\x17',
    '\x18', '\x19', '\x1a', '\x1b', '\x1c', '\x1d',
    '\x1e', '\x1f',
]

#[定义函数] 拆散路径为 目录路径与文件名
def split_path(path:str) -> tuple[str, str]:
    path = Path(path).resolve().as_posix()
    parts = path.split('/')
    return ('/'.join(parts[:-1]), parts[-1])

#[定义函数] 输入字符串, 返回安全的文件名字符串
def safe_file_name(file_name:str, replacement:str='_') -> str:

    if file_name == '':
        return ''

    pattern = re.compile(f"[{''.join(re.escape(c) for c in Lib_Path_illegal_chars)}]")

    #替换字符
    cleaned = pattern.sub(replacement, file_name)

    #去除空白字符
    cleaned = cleaned.strip()

    return cleaned

#[定义函数] 传入目录与文件名, 返回不受路径字符数限制的路径字符串
def safe_file_path(dir:str, file_name:str, replacement:str='_') -> str:

    if file_name == '':
        abs_path = str(Path(dir).resolve())
        if not abs_path.startswith('\\\\?\\'):
            abs_path = '\\\\?\\' + abs_path
        return abs_path

    safe_name = safe_file_name(file_name, replacement)
    full_path = os.path.join(dir, safe_name)
    abs_path = os.path.abspath(full_path)

    if not abs_path.startswith('\\\\?\\'):
        abs_path = '\\\\?\\' + abs_path

    return abs_path

#[定义函数] 传入目录和文件名, 返回一个不重名的文件路径
def not_repeat_path(dir:str, name:str, replacement:str = '_', is_dir:Literal['auto']|bool='auto') -> str:

    base_path = Path(dir) / name
    
    #截取主文件名和后缀
    stem = base_path.stem
    suffix = base_path.suffix
    
    #如果原路径不存在, 直接返回
    if not base_path.exists():
        return str(base_path)

    #正则匹配 '{stem}{replacement}{数字}{suffix}'
    pattern = re.compile(rf'^{re.escape(stem)}{re.escape(replacement)}(\d+){re.escape(suffix)}$')
    max_num = 0

    #仅遍历当前目录, 寻找最大数字后缀
    for entry in os.listdir(dir):
        full_path = os.path.join(dir, entry)
        if not os.path.exists(full_path):
            continue
        match = pattern.match(entry)
        if match:
            max_num = max(max_num, int(match.group(1)))

    #直接基于最大值 + 1 生成新名称
    new_name = f'{stem}{replacement}{max_num + 1}{suffix}'
    new_path = str(base_path.parent / new_name)

    #自动判断目标类型
    if is_dir == 'auto':
        #自动判断模式：优先判断是否为文件夹, 其次判断是否为文件
        if base_path.is_dir():
            is_dir = True
        elif base_path.is_file():
            is_dir = False
        else:
            #不是文件和文件夹 (例如损坏的符号链接等), 默认按文件处理
            is_dir = False

    #根据类型进行原子性创建
    try:
        if is_dir:
            #创建文件夹 (exist_ok=False 保证并发安全)
            os.makedirs(new_path, exist_ok=False)
        else:
            #创建文件 (O_EXCL 保证并发安全)
            fd = os.open(new_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
        return new_path
        
    except FileExistsError:
        #极端并发冲突时, 回退到逐个尝试
        counter = max_num + 2
        while True:
            fallback_name = f'{stem}{replacement}{counter}{suffix}'
            fallback_path = str(base_path.parent / fallback_name)
            try:
                if is_dir:
                    os.makedirs(fallback_path, exist_ok=False)
                else:
                    fd = os.open(fallback_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                    os.close(fd)
                return fallback_path
            except FileExistsError:
                counter += 1
                if counter > max_num + 10000:
                    raise FileExistsError(f'[Lib-error] {name} 已重名路径数量超出阈值')