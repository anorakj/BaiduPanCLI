# -*- coding: utf-8 -*-
from bdp.constants import KB, MB, GB


def byte2kmg(nbyte, precision=1):
    """change byte into KB, MB or GB according to its number"""
    if nbyte < MB:
        return str(round(nbyte / KB, precision)) + 'KB'
    elif nbyte < GB:
        return str(round(nbyte / MB, precision)) + 'MB'
    else:
        return str(round(nbyte / GB, precision)) + 'GB'
