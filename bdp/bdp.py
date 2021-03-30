# -*- coding: utf-8 -*-

import click

from bdp.api import (
    authorize,
    UserInfoRequest,
    VolumeInfoRequest,
    create_list_request,
)


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
    print(UserInfoRequest().execute())


@cli.command()
def volume():
    """获取网盘容量使用情况"""
    print(VolumeInfoRequest().execute())


@cli.command()
@click.argument("directory", default="/")
@click.option("-l", "--long_format", is_flag=True)
@click.option("-r", "--recursive", is_flag=True)
def ls(directory, long_format, recursive):
    print(create_list_request(directory, long_format, recursive).execute())


if __name__ == "__main__":
    cli()
