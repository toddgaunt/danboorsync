#
# License: MIT (doc/LICENSE)
# Author: Todd Gaunt
#
# File: imgfetch/util.py
# This file contains various utility functions

import re
import os
import hashlib

from imgfetch import logger

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, new_path):
        self.new_path = os.path.expanduser(new_path)

    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)


def remove_chars(list):
    """Removes all non-alphanumeric and non-underscore/dashes from a string"""
    tmp_list = []
    list = list.split(' ')
    for i in range(len(list)):
        tmp = ''
        for j in list[i]:
            if re.match(r'\w', j):
                tmp += j
        if tmp != '':
            tmp_list.append(tmp)
    return '_'.join(tmp_list)

def get_file_md5s():
    """Creates a list of unencoded md5sums of files in the current directory"""
    files = os.listdir()
    md5sums = []
    for i in files:
        hash = hashlib.md5()
        with open(i, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash.update(chunk)
        md5sums.append(hash.digest())
    return md5sums

def make_dir(directory):
    """Trys to create a directory, logs the output"""
    try:
        os.mkdir(directory)
    except FileExistsError:
        logger.warning(0, "File " + "'" + directory + "'" + " already exists")
