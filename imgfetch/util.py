#
# License: MIT (doc/LICENSE)
# Author: Todd Gaunt

import re
import os
import hashlib

class cd:
    """ cd
    description:
        Context manager for changing the current working directory

    examples:
        >> print(os.getcwd())
        /
        >> with cd("/path/to/dir"):
        >>     print(os.getcwd())
        /path/to/dir
        >> print(os.getcwd())
        /
    """
    def __init__(self, new_path):
        self.new_path = os.path.expanduser(new_path)

    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)

def get_file_md5sums(path="."):
    """ get_file_md5sums

    description:
        Creates a dictionary of hex-encoded md5sums of files in the given path
        recursively.

    args:
        param1(str): path to files

    return:
        dict[str, str]:
            upon success, will return a dictionary with
            the relation [md5sum:filename]

            upon failure, will return an empty dictionary

    example:
        >> md5sums = get_file_md5sums("/path/to/files")
        >> print(md5sums)
        ["md5sum1": "filename", "md5sum2": "filename"]
    """
    md5sums = {}
    roots = [path]
    while(roots != []):
        branch = roots.pop()
        for twig in os.listdir(branch):
            twig = os.path.join(branch, twig)
            if os.path.isdir(twig):
                roots.append(twig)
            else:
                fhash = hashlib.md5()
                with open(twig, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        fhash.update(chunk)
                md5sums[fhash.digest().hex()] = twig
    return md5sums

def remove_non_posix_chars(string):
    """ remove_chars

    description:
        Removes all non-alphanumeric and non-underscore/dashes from a string

    args:
        param1(str): string to strip characters from

    return:
        (str): new string object derived from input string

    example:
        >> str1 = "AB--@**(twenty?_2"
        >> str2 = remove_chars(str1)
        >> print(str2)
        AB--twenty_2

    """
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
