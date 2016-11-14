#
# License: MIT (doc/LICENSE)
# Author: Todd Gaunt
#
# File: imgfetch/util/net.py
# This file contains generic network related operations for imgfetch

import re
import os
import json
from urllib.request import urlopen

from imgfetch import logger

def download_file(loglevel, post, md5sums):
    """Downloads 'posts' and checks there md5sums against files in the system already to avoid
    redownloading duplicate images"""
    url = post.url
    filename = post.name
    md5 = post.md5
    dir_contents = os.listdir()

    if md5sums:
        method = "md5"
        # Renames the file to include a section of the md5 hash
        # So no unique files are overwritten.
        param = md5 not in md5sums
        if param and filename in dir_contents:
            tmp = ''
            for i in range(5):
                if re.match(r'\w', str(md5[i])):
                    tmp += str(md5[i])
            filename = tmp + filename
    else:
        method = "name"
        param = filename not in dir_contents
    # Now to actually write the file
    if param:
        with open(filename, 'wb') as file:
            file.write(urlopen(url).read())
            logger.output(loglevel, url + " downloaded: " + filename)
    else:
        logger.output(loglevel, url + " " + method + " match: " + filename)

def get_json(url):
    """Fetches the json file, returns a list of its contents"""
    data = urlopen(url).read()
    json_file = json.loads(data.decode('utf-8'))
    # Standalone posts aren't in a list, so make it a list with one index
    if not type(json_file) is list:
        json_file = [json_file]
    return json_file
