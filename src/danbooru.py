#
# License: MIT (doc/LICENSE)
# Author: Todd Gaunt

import json
from urllib.parse import urlparse
from urllib.request import urlopen

from danboorsync import util

SCHEME = "http"
NETLOC = "danbooru.donmai.us"

def jsonize(raw_url):
    """Uses the given url string to fetch a json file"""
    url = urlparse(raw_url)
    json_url = url.scheme+"://"+url.netloc+url.path+".json"+"?"+url.query
    data = urlopen(json_url).read()
    json_file = json.loads(data.decode('utf-8'))
    # If not already a list, make it a list with one index.
    if not type(json_file) is list:
        json_file = [json_file]
    return json_file

def appendqueries(raw_url, queries):
    url = urlparse(raw_url)
    query = url.query
    for i in queries:
        query += "&"+str(i)
    newurl = url.scheme+"://"+url.netloc+url.path+"?"+query
    return newurl

def download_post(post):
    url = SCHEME + "://" + NETLOC + str(post['file_url'])
    filename = filename_gen(post)
    with open(filename, 'wb') as fd:
        fd.write(urlopen(url).read())
    return filename

def filename_gen(post):
    """Generates a filename for Danbooru files using the post information"""
    name = ""
    md5sum = str(post['md5'])
    extension = str(post['file_ext'])

    max_name_len = 200 - len(md5sum) - (len(extension) + 1)
    for character in post['tag_string_character'].split():
        next_tag = util.remove_chars(character) + '_'
        if len(name) + len(next_tag) >= max_name_len:
            break
        name += next_tag

    for tag in post['tag_string_general'].split():
        next_tag = util.remove_chars(tag) + '_'
        if len(name) + len(next_tag) >= max_name_len:
            break
        name += next_tag
    name += md5sum
    name += "." + extension

    return name

def verify_picture(post):
    keys = post.keys()
    if "md5" not in keys:
        return False
    if "image_width" in keys:
        return True
    else:
        return False

# End of File
