# -*- coding: utf-8 -*-

import click

from bdp.api import authorize_request, get_user_info, get_volumn_info


@click.group()
def cli():
    pass


@cli.command()
def authorize():
    """获取授权链接，授权后可获取授权码"""
    authorize_request()


@cli.command()
def uinfo():
    """获取基本用户信息"""
    user_info = get_user_info()
    print(
        "用户名: {}\n头像链接: {}\nVIP: {}".format(
            user_info["baidu_name"],
            user_info["avatar_url"],
            "是" if user_info["vip_type"] else "否",
        )
    )


@cli.command()
def volumn():
    """获取网盘容量使用情况"""
    volumn_info = get_volumn_info()
    print("总容量: {}, 已使用容量: {}".format(volumn_info["total"], volumn_info["used"]))


if __name__ == "__main__":
    cli()
