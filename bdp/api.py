# -*- coding: utf-8 -*-
import os

import requests

from bdp.exceptions import ApiKeyNotFoundError, AccessTokenNotFoundError

AUTHORIZE_URL = "http://openapi.baidu.com/oauth/2.0/authorize"
USER_INFO_URL = "https://pan.baidu.com/rest/2.0/xpan/nas"
VOLUMN_INFO_URL = "https://pan.baidu.com/api/quota"
GB = 1024 * 1024 * 1024


def _check_api_key():
    if "API_KEY" not in os.environ:
        raise ApiKeyNotFoundError(
            "API_KEY not found in environment variables. Please set it to your application ApiKey"
        )


def _check_access_token():
    if "ACCESS_TOKEN" not in os.environ:
        raise ApiKeyNotFoundError(
            "ACCESS_TOKEN not found in environment variables. Please set it or use 'bdp authorize' to get the token"
        )


def authorize_request():
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


def get_user_info():
    _check_access_token()
    params = {
        "method": "uinfo",
        "access_token": os.getenv("ACCESS_TOKEN"),
    }
    response = requests.get(USER_INFO_URL, params=params)
    return response.json()


def get_volumn_info():
    _check_access_token()
    params = {
        "checkfree": 1,
        "checkexpire": 1,
        "access_token": os.getenv("ACCESS_TOKEN"),
    }
    response = requests.get(VOLUMN_INFO_URL, params=params)
    result = response.json()
    for key in ["total", "used"]:
        result[key] = "{}G".format(round(result[key] / GB, 1))
    return result
