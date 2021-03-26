# -*- coding: utf-8 -*-
import abc
import os

import requests

from bdp.exceptions import ApiKeyNotFoundError, AccessTokenNotFoundError

AUTHORIZE_URL = "http://openapi.baidu.com/oauth/2.0/authorize"
USER_INFO_URL = "https://pan.baidu.com/rest/2.0/xpan/nas"
VOLUMN_INFO_URL = "https://pan.baidu.com/api/quota"
FILE_LIST_URL = "https://pan.baidu.com/rest/2.0/xpan/file?method=list"
FILE_LIST_RECURSIVE_URL = (
    "https://pan.baidu.com/rest/2.0/xpan/multimedia?method=listall"
)


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


def authorize_request():
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
    def __init__(self):
        self.url = None
        self.method = requests.get

    def prepare_request(self):
        _check_api_key()

    def execute_request(self, *args, **kwargs):
        response = self.method(self.url, *args, **kwargs)
        return response.json()


def get_user_info():
    """get basic user info like name, avatar_url, vip etc."""
    _check_access_token()
    params = {
        "method": "uinfo",
        "access_token": os.getenv("ACCESS_TOKEN"),
    }
    response = requests.get(USER_INFO_URL, params=params)
    return response.json()


def get_volumn_info():
    """get volumn usage condition of the net disk"""
    _check_access_token()
    params = {
        "checkfree": 1,
        "checkexpire": 1,
        "access_token": os.getenv("ACCESS_TOKEN"),
    }
    response = requests.get(VOLUMN_INFO_URL, params=params)
    return response.json()


def get_file_list_info(directory, recursive=False):
    """list directory contents"""
    _check_access_token()
    if recursive:
        params = {
            "path": directory,
            "access_token": os.getenv("ACCESS_TOKEN"),
            "recursion": 1,
        }
        url = FILE_LIST_RECURSIVE_URL
    else:
        params = {
            "dir": directory,
            "access_token": os.getenv("ACCESS_TOKEN"),
        }
        url = FILE_LIST_URL
    response = requests.get(url, params=params)
    return response.json()
