# -*- coding: utf-8 -*-
from pprint import pprint

import click

from bdp.api import authorize_request, get_user_info, get_volumn_info


@click.group()
def cli():
    pass


@cli.command()
def authorize():
    authorize_request()


@cli.command()
def uinfo():
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
    volumn_info = get_volumn_info()
    print("总容量: {}, 已使用容量: {}".format(volumn_info["total"], volumn_info["used"]))


if __name__ == "__main__":
    cli()
