# -*- coding: utf-8 -*-
import abc

from datetime import datetime

from bdp.utils import byte2kmg


class Formatter(object):
    def format(self, data):
        return str(data)


class UserInfoBaseFormatter(Formatter):
    def format(self, data):
        return "用户名: {}\n头像链接: {}\nVIP: {}".format(
            data["baidu_name"],
            data["avatar_url"],
            "是" if data["vip_type"] else "否",
        )


class VolumeInfoBaseFormatter(Formatter):
    def format(self, data):
        return "总容量: {}, 已使用容量: {}".format(
            byte2kmg(data["total"]), byte2kmg(data["used"])
        )


class ListInfoBaseFormatter(Formatter):
    def format(self, data):
        lines = ["path"]
        for path_info in data["list"]:
            name = path_info["path"]
            if path_info["isdir"]:
                name += "/"
            lines.append(name)
        return "\n".join(lines)


class ListInfoLongFormatter(Formatter):
    def format(self, data):
        lines = ["{:>7}   {:20}{:10}".format("size", "ctime", "path")]
        for path_info in data["list"]:
            size = byte2kmg(path_info["size"]) if not path_info["isdir"] else "-"
            ctime = datetime.fromtimestamp(path_info["server_ctime"]).strftime(
                "%Y.%m.%d %H:%M"
            )
            name = path_info["path"]
            if path_info["isdir"]:
                name += "/"
            lines.append("{:>7}   {:20}{:10}".format(size, ctime, name))
        return "\n".join(lines)
