# -*- coding: utf-8 -*-
import abc
import os

import requests

from bdp.exceptions import ApiKeyNotFoundError, AccessTokenNotFoundError
from bdp.formatters import (
    Formatter,
    UserInfoBaseFormatter,
    VolumeInfoBaseFormatter,
    ListInfoBaseFormatter,
    ListInfoLongFormatter,
)

AUTHORIZE_URL = "http://openapi.baidu.com/oauth/2.0/authorize"


def _check_api_key():
    """check if api key is available in environment variables"""
    if "API_KEY" not in os.environ:
        raise ApiKeyNotFoundError(
            "API_KEY not found in environment variables. Please set it to your application ApiKey"
        )


def _check_access_token():
    """check if access token is available in environment variables"""
    if "ACCESS_TOKEN" not in os.environ:
        raise AccessTokenNotFoundError(
            "ACCESS_TOKEN not found in environment variables. Please set it or use 'bdp authorize' to get the token"
        )


def authorize():
    """show the authorization link for the user to get access token"""
    _check_api_key()
    params = {
        "response_type": "token",
        "client_id": os.getenv("API_KEY"),
        "redirect_uri": "oob",
        "scope": "basic,netdisk",
        "display": "page",
    }

    url = requests.Request("GET", AUTHORIZE_URL, params=params).prepare().url
    print("Please click url below to get the access token: \n{}".format(url))


class ApiRequest(abc.ABC):
    def __init__(self, formatter=Formatter):
        self.method = None
        self.url = None
        self.params = None
        self.files = None
        self.data = None
        self.headers = None
        self.formatter = formatter

    def prepare(self):
        _check_api_key()

    def execute(self):
        self.prepare()
        response = requests.request(
            self.method,
            self.url,
            params = self.params,
            data=self.data,
            files=self.files,
            headers=self.headers,
        )
        return self.formatter().format(response.json())


class GetApiRequest(ApiRequest, abc.ABC):
    def __init__(self, formatter=Formatter):
        super().__init__(formatter)
        self.method = "GET"


class PostApiRequest(ApiRequest, abc.ABC):
    def __init__(self, formatter=Formatter):
        super().__init__(formatter)
        self.method = "POST"


class UserInfoRequest(GetApiRequest):
    """get basic user info like name, avatar_url, vip etc."""

    def __init__(self, formatter=UserInfoBaseFormatter):
        super().__init__(formatter)
        self.params = {}
        self.url = "https://pan.baidu.com/rest/2.0/xpan/nas"

    def prepare(self):
        super().prepare()
        self.params = {
            "method": "uinfo",
            "access_token": os.getenv("ACCESS_TOKEN"),
        }


class VolumeInfoRequest(GetApiRequest):
    """"get volumn usage condition of the net disk"""

    def __init__(self, formatter=VolumeInfoBaseFormatter):
        super().__init__(formatter)
        self.params = {}
        self.url = "https://pan.baidu.com/api/quota"

    def prepare(self):
        super().prepare()
        self.params = {
            "checkfree": 1,
            "checkexpire": 1,
            "access_token": os.getenv("ACCESS_TOKEN"),
        }


def create_list_request(directory, long_format, recursive):
    formatter = ListInfoLongFormatter if long_format else ListInfoBaseFormatter
    if recursive:
        return RecursiveListRequest(directory, formatter)
    else:
        return ListRequest(directory, formatter)


class ListRequest(GetApiRequest):
    """list directory contents"""

    def __init__(self, directory, formatter):
        super().__init__(formatter)
        self.directory = directory
        self.params = None
        self.url = "https://pan.baidu.com/rest/2.0/xpan/file?method=list"

    def prepare(self):
        super().prepare()
        self.params = {
            "dir": self.directory,
            "access_token": os.getenv("ACCESS_TOKEN"),
        }


class RecursiveListRequest(ListRequest):
    """recursive list direcotry contents"""

    def __init__(self, directory, formatter):
        super().__init__(directory, formatter)
        self.url = "https://pan.baidu.com/rest/2.0/xpan/multimedia?method=listall"

    def prepare(self):
        super(ListRequest, self).prepare()
        self.params = {
            "path": self.directory,
            "access_token": os.getenv("ACCESS_TOKEN"),
            "recursion": 1,
        }
