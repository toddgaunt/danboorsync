#
# License: MIT (doc/LICENSE)
# Author: Todd Gaunt
#
# File: imgfetch/util.py
# This file contains various utility functions

import re
import os
import hashlib

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, new_path):
        self.new_path = os.path.expanduser(new_path)

    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)

def get_file_md5sums(directory="."):
    """Creates a list of unencoded md5sums of files in the optional directory
    argument"""
    files = os.listdir(directory)
    md5sums = {}
    for i in files:
        fhash = hashlib.md5()
        with open(i, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                fhash.update(chunk)
        md5sums[fhash.digest().hex()] = i
    return md5sums

def make_dir(directory):
    """Trys to create a directory, prints the output"""
    try:
        os.mkdir(directory)
    except FileExistsError:
        return

def remove_chars(string):
    """Removes all non-alphanumeric and non-underscore/dashes from a string"""
    tmp_string = []
    string = string.split(' ')
    for i in range(len(string)):
        tmp = ''
        for j in string[i]:
            if re.match(r'\w', j):
                tmp += j
        if tmp != '':
            tmp_string.append(tmp)
    return '_'.join(tmp_string)

# End of File
