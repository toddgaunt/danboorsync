#
# License: MIT (doc/LICENSE)
# Author: Todd Gaunt
#
# File: imgfetch/structs.py
# This file contains stucts that store data about a post

class generic_post:
    """Generic class used for storing the important atrributes of the posts from the json files"""
    def __init__(self, name, ext, url, md5):

        # Generic data, all posts expected to have it
        self.name = name    # file name with extension
        self.ext = ext              # file extension
        self.url = url    # file url
        self.md5 = md5              # md5sum of file
