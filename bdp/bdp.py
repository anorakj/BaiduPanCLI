# -*- coding: utf-8 -*-

import click

from bdp.api import (
    authorize_request,
    get_user_info,
    get_volumn_info,
    get_file_list_info,
)
from bdp.format import format_user_info, format_volumn_info, format_file_list_info


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
    print(format_user_info(user_info))


@cli.command()
def volumn():
    """获取网盘容量使用情况"""
    volumn_info = get_volumn_info()
    print(format_volumn_info(volumn_info))


@cli.command()
@click.option("-r", "--recursive", is_flag=True)
@click.argument("directory", default="/")
def ls(recursive, directory):
    file_list_info = get_file_list_info(directory, recursive)
    print(format_file_list_info(file_list_info))


if __name__ == "__main__":
    cli()
