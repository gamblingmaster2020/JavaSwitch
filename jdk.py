# -*- coding: utf-8 -*-

from __future__ import print_function

import ctypes
import os
import sys
from winreg import *

java_list = [
    # 修改这里
    r'C:\Program Files\Java\jdk-15.0.1',
    r'C:\Users\foyou\.jdks\openjdk-15',
    r'C:\Program Files\BellSoft\LibericaJDK-11-Full',
    r'C:\Program Files\Java\jdk1.8.0_271',
    r'C:\Program Files\Android\Android Studio\jre',
]


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def input_jdk_name():
    for index in range(len(java_list)):
        print(index, java_list[index], sep=': ', end="\n")
    return int(input('请输入序号: '))


def todo():
    java_home = java_list[input_jdk_name()]

    # jdk_bin = r''
    jdk_bin = java_home + r'\bin'
    # jre_home = r''
    jre_home = java_home + r'\jre'

    reg_root = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    sub_dir = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
    sub_key = "Path"
    key_handle = OpenKey(reg_root, sub_dir, 0, KEY_READ | KEY_SET_VALUE)

    sys_path = ''

    for path in str(QueryValueEx(key_handle, sub_key)[0]).split(';'):

        # 判断是否为空, 排除最后一个
        if len(path) == 0:
            continue

        # 是否有 \
        if not path.endswith('\\'):
            path += '\\'

        # 是否是 jdk\bin
        if os.path.exists(path + r'java.exe'):
            continue

        sys_path += path + ';'

    sys_path = jdk_bin + r'\;' + sys_path

    SetValueEx(key_handle, sub_key, 0, REG_EXPAND_SZ, sys_path)
    SetValueEx(key_handle, "java_home", 0, REG_EXPAND_SZ, java_home + '\\')
    SetValueEx(key_handle, "jre_home", 0, REG_EXPAND_SZ, jre_home + '\\')

    CloseKey(key_handle)
    CloseKey(reg_root)

    input('执行完毕, 回车结束~')


if __name__ == '__main__':
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    else:
        todo()

