# -*- coding: utf-8 -*-
from datetime import datetime

from bdp.utils import byte2kmg


def format_user_info(user_info):
    """format user info response into human-readable text"""
    return "用户名: {}\n头像链接: {}\nVIP: {}".format(
        user_info["baidu_name"],
        user_info["avatar_url"],
        "是" if user_info["vip_type"] else "否",
    )


def format_volumn_info(volumn_info):
    """format volumn info response into human-readable text"""
    for key in ["total", "used"]:
        volumn_info[key] = "{}G".format(round(byte2kmg(volumn_info[key]), 1))
    return "总容量: {}, 已使用容量: {}".format(volumn_info["total"], volumn_info["used"])


def format_file_list_info(file_list_info):
    lines = ["{:>7}   {:20}{:10}".format("size", "ctime", "path")]
    for path_info in file_list_info['list']:
        size = byte2kmg(path_info['size']) if not path_info['isdir'] else '-'
        ctime = datetime.fromtimestamp(path_info['server_ctime']).strftime('%Y.%m.%d %H:%M')
        name = path_info['path']
        if path_info['isdir']:
            name += '/'
        lines.append("{:>7}   {:20}{:10}".format(size, ctime, name))
    return '\n'.join(lines)
