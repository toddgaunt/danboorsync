# See LICENSE file for copyright and license details

import re
import os

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

def remove_non_posix_chars(string):
    """
    Removes all non-alphanumeric and non-underscore/dashes from a string

    return:
        (str): new string object derived from input string

    example:
        "AB--@**(twenty?_2" -> "AB--twenty_2"
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

def find_hash(path, hash_func):
    """
    return:
        dict[str, str]:
            upon success, will return a dictionary with
            the relation [chksum:filename]

            upon failure, will return an empty dictionary
    """
    chksums = {}
    roots = [path]
    while(roots != []):
        branch = roots.pop()
        for twig in os.listdir(branch):
            twig = os.path.join(branch, twig)
            if os.path.isdir(twig):
                roots.append(twig)
            else:
                hash = hash_func()
                with open(twig, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash.update(chunk)
                chksums[hash.digest().hex()] = twig
    return chksums

# End of File
