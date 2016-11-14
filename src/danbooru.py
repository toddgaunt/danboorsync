#
# License: MIT (doc/LICENSE)
# Author: Todd Gaunt

import json
from urllib.parse import urlparse
from urllib.request import urlopen

from danboorsync import util

class image_post():
    """ image_post

    description:
        a class for containing information pertaining to a danbooru post with
        information regarding an image file
    """

    def __init__(self):
        self.md5sum = ""

        self.character_tags = ""
        self.general_tags = ""
        self.artist_tags = ""

        self.filename = ""
        self.file_url = ""
        self.file_ext = ""

def new_post(item):
    """ new post

    description:
        Creates and returns a new post object based on a dictionary from
        a danbooru json file's data

    args:
        dict[str,str]: a single entry from json file data

    return:
        post: a post object with all fields filled out according to the
        json file data
    """

    post = image_post()

    post.md5sum = item["md5"]

    post.character_tags = item["tag_string_character"]
    post.general_tags = item["tag_string_general"]
    post.artist_tags = item["tag_string_artist"]

    post.file_url = item["file_url"]
    post.file_ext = item["file_ext"]

    return post

def extract_image_posts(json):
    """ extract_image_posts

    description:
        Converts any posts in the given json data that refer to images into
        post objects

    args:
        param1(list[dict[str,str]]): a loaded json file, usually from jsonize()

    return:
        list[post]: a list of post objects generated from the json data
    """

    posts = [];
    for item in json:
        # Load all the keys from the json dictionary
        keys = item.keys()
        # Skip the post in the jason file if it doesn't contain these keys
        if "md5" not in keys:
            continue
        if "image_width" not in keys:
            continue
        # Construct a new post derived from the json file data
        posts.append(new_post(item))

    return posts

def download_post(post, scheme, netloc):
    """ download_post

    description:
        Writes the file that the given post refers to

    args:
        param1(image_post): a image_post object

    return:
        str: the filename the file was written to

    example:
        >> post = image_post()
        >> filename = download_post(post)
    """

    url = "{}://{}{}".format(scheme, netloc, post.file_url)
    filename = filename_gen(post)
    with open(filename, 'wb') as fd:
        fd.write(urlopen(url).read())
    return filename

def filename_gen(post):
    """ filename_gen

    description:
        Generates a filename for Danbooru files using the post information

    args:
        param1(image_post): a image_post object

    return:
        str: the filename generated from the post object

    example:
        >> post = image_post()
        >> filename = filename_gen(post)
    """

    name = ""
    md5sum = str(post.md5sum)
    extension = str(post.file_ext)

    max_name_len = 200 - len(md5sum) - (len(extension) + 1)

    for character in post.character_tags.split():
        next_tag = util.remove_chars(character) + '_'
        if len(name) + len(next_tag) >= max_name_len:
            break
        name += next_tag

    for tag in post.general_tags.split():
        next_tag = util.remove_chars(tag) + '_'
        if len(name) + len(next_tag) >= max_name_len:
            break
        name += next_tag
    name += md5sum
    name += "." + extension

    return name

def jsonize(raw_url):
    """ jsonize

    description:
        Uses the given url string to fetch a related json file

    args:
        param1(str): a url string

    return:
        list[dict[str:str]]: this is the loaded json file

    example:
        In the below example, assuming post.html had a corresponding post.json,
        jsonize would download and convert it into a python list[dict[str,str]]
        >> json_dict = jsonize("www.example.com/post.html")
    """
    url = urlparse(raw_url)
    json_url = url.scheme+"://"+url.netloc+url.path+".json"+"?"+url.query
    data = urlopen(json_url).read()
    json_file = json.loads(data.decode('utf-8'))
    # If not already a list, make it a list with one index.
    # This is for cases when there is a single post from the danbooru url
    if not type(json_file) is list:
        json_file = [json_file]
    return json_file

def appendqueries(raw_url, queries):
    """ appendqueries

    description:
        append additional queries to the end of a url string

    args:
        param1(str): a url string

        param2(list[str]): a list of query strings

    return:
        str: a new url with the appended queries

    example:
        >> url = "www.example.com/file?v=1"
        >> q = ["page=1", "zerg=cool"]
        >> appendqueries(url, q)
        >> print(url)
        www.example.com/file?v=1&page=1&zerg=cool
    """
    url = urlparse(raw_url)
    # Start with the queries already present
    query = url.query
    for i in queries:
        query += "&"+i
    # Return a string of the new url
    return (url.scheme+"://"+url.netloc+url.path+"?"+query)

# End of File
