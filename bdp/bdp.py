# -*- coding: utf-8 -*-

import click

from bdp.api import (
    authorize,
    UserInfoRequest,
    VolumnInfoRequest,
    create_list_request,
)
from bdp.format import format_user_info, format_volumn_info, format_file_list_info


@click.group()
def cli():
    pass


@cli.command()
def authorize():
    """获取授权链接，授权后可获取授权码"""
    authorize()


@cli.command()
def uinfo():
    """获取基本用户信息"""
    user_info = UserInfoRequest().execute()
    print(format_user_info(user_info))


@cli.command()
def volumn():
    """获取网盘容量使用情况"""
    volumn_info = VolumnInfoRequest().execute()
    print(format_volumn_info(volumn_info))


@cli.command()
@click.option("-r", "--recursive", is_flag=True)
@click.argument("directory", default="/")
def ls(recursive, directory):
    file_list_info = create_list_request(directory, recursive).execute()
    print(format_file_list_info(file_list_info))


if __name__ == "__main__":
    cli()
