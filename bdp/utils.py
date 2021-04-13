# -*- coding: utf-8 -*-
import hashlib
import math
import os
from tempfile import TemporaryDirectory

from bdp.constants import KB, MB, GB


def byte2kmg(nbyte, precision=2):
    """change byte into KB, MB or GB according to its number"""
    if nbyte < MB:
        return str(round(nbyte / KB, precision)) + "KB"
    elif nbyte < GB:
        return str(round(nbyte / MB, precision)) + "MB"
    else:
        return str(round(nbyte / GB, precision)) + "GB"


def slice_file(file_path, des_directory, chunk_size=4 * MB):
    files = []
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    with open(file_path, "rb") as f:
        for i in range(math.ceil(file_size / chunk_size)):
            chunk = f.read(chunk_size)
            file_info = {
                "path": os.path.join(des_directory, "{}_part_{}".format(file_name, i)),
                "md5": hashlib.md5(chunk).hexdigest(),
            }
            with open(file_info["path"], "wb") as chunk_f:
                chunk_f.write(chunk)
            files.append(file_info)
    return files


class SliceFileManager(object):
    """manage file slicing and cleaning locally"""

    def __init__(self, target_file_path, chunk_size=4 * MB):
        self.target_file_path = target_file_path
        self.sliced = False
        self.chunk_size = chunk_size
        self._sliced_files_info = []
        self._tempdir = None

    @property
    def sliced_files_info(self):
        if not self.sliced:
            self._tempdir = TemporaryDirectory()
            self._sliced_files_info = slice_file(self.target_file_path, self._tempdir.name, chunk_size=self.chunk_size)
            self.sliced = True
        return self._sliced_files_info

    def cleanup(self):
        self._tempdir.cleanup()
