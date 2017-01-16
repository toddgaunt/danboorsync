#
# License: MIT (doc/LICENSE)
# Author: Todd Gaunt

import argparse
import re
import os
import json
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen

from imgfetch import danbooru
from imgfetch import logger
from imgfetch import util

class image_post():
    """ image_post.__init__
    description:
        Creates and returns a new post object based on a dictionary from
        a danbooru json file's data

    args:
        dict[str,str]: a single entry from json file data

    return:
        post: a post object with all fields filled out according to the
        json file data
    """
    def __init__(self, item=None):
        if (None == item):
            self.md5sum = ""

            self.character_tags = ""
            self.general_tags = ""
            self.artist_tags = ""

            self.filename = ""
            self.file_url = ""
            self.file_ext = ""
        else:
            self.md5sum = item["md5"]

            self.character_tags = item["tag_string_character"]
            self.general_tags = item["tag_string_general"]
            self.artist_tags = item["tag_string_artist"]

            self.file_url = item["file_url"]
            self.file_ext = item["file_ext"]

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
        posts.append(image_post(item))

    return posts

def download_image_post(filename, post, scheme, netloc):
    """ download_image_post

    description:
        Writes the file that the given post refers to

    args:
        param1(image_post): a image_post object

    return:
        str: the filename the file was written to

    example:
        >> post = image_post()
        >> filename = download_image_post(post)
    """

    url = "{}://{}{}".format(scheme, netloc, post.file_url)
    with open(filename, 'wb') as fd:
        fd.write(urlopen(url).read())
    return filename

def image_post_path_gen(post):
    path = ""
    max_path_len = 200

    if post.character_tags != "":
        for character in post.character_tags.split():
            next_tag = util.remove_chars(character) + '-'
            if len(path) + len(next_tag) >= max_path_len:
                break
            path += next_tag
        return path[0:-1]
    else:
        return "no_character_tag"

def image_post_name_gen(post):
    name = ""
    md5sum = str(post.md5sum)
    extension = str(post.file_ext)

    max_name_len = 200 - len(md5sum) - (len(extension) + 1)

    for character in post.character_tags.split():
        next_tag = util.remove_chars(character) + '-'
        if len(name) + len(next_tag) >= max_name_len:
            break
        name += next_tag

    for tag in post.general_tags.split():
        next_tag = util.remove_chars(tag) + '-'
        if len(name) + len(next_tag) >= max_name_len:
            break
        name += next_tag
    name += md5sum
    name += "." + extension

    return name

def jsonize_post_url(raw_url):
    """ jsonize_post_url

    description:
        Uses the given url string to fetch a related json file

    args:
        param1(str): a url string

    return:
        list[dict[str:str]]: this is the loaded json file

    example:
        In the below example, assuming post.html had a corresponding post.json,
        jsonize_post_url would download and convert it into a python list[dict[str,str]]
        >> json_dict = jsonize_post_url("www.example.com/post.html")
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

def string_range_parse(numbers):
    """ string_range_parse

    description:
        transforms a list of number rangs represented as string to a list
        of integers derived from the input.

    args:
        param1(string): list of number ranges

    return:
        list[str]: will always return a list

        will return an empty list upon failure

    example:
        >> ranges = ['1-3', '32-33', '99']
        >> ranges = string_range_parse(ranges)
        >> print(ranges)
        [1,2,3,32,33,99]
    """
    lg = logger.logger(__name__, 1);

    pages = []
    for i in numbers:
        rangematch = re.match(r'\s*(\d+)-(\d+)\s*', i)
        singlematch = re.match(r'\s*(\d+)\s*', i)
        if rangematch != None:
            for j in range(int(rangematch.group(1)), int(rangematch.group(2))+1):
                pages.append(j)
        elif singlematch:
            pages.append(int(singlematch.group(1)))
        else:
            logger.warning(lg, "Invalid number range {}".format(i))
    return pages

# Driver of danbooru
def run(argv):
    parser = argparse.ArgumentParser(description='Downloads images en masse from Danbooru')

    parser.add_argument('-o', '--output', metavar='dir',
                        type=str,
                        help='Specify a directory to create the download directory')

    parser.add_argument('-p', '--pages', metavar='range',
                        type=str, default="1",
                        help='Specify a page range to download from, \
                                e.g. -p 1-5,10,15-20')

    parser.add_argument('-q', '--quiet',
                        action="store_true", default=False,
                        help='Turn off all output')

    parser.add_argument('-v', '--verbose',
                        action="count", default=1,
                        help='Display files downloaded')

    parser.add_argument('url', metavar='url',
                    type=str,
                    help='Url to download from')

    args = parser.parse_args(argv)

    # Set the verbosity
    if args.quiet:
        args.verbose = 0

    lg = logger.logger("danbooru", args.verbose)

    if not args.output:
        logger.error(lg, "Please specify an output directory with the -o flag")

    if not os.path.exists(args.output):
        logger.info(lg, "Creating new directory: {}".format(args.output))
        try:
            os.mkdir(args.output)
        except FileExistsError:
            logger.error(lg, "Could not create directory: {}".format(args.output))
    else:
        logger.info(lg, "Using existing directory: {}".format(args.output))

    # Turn the string of numbers into a usable list
    args.pages = string_range_parse(args.pages.split(','))

    # Change directory to the target download directory,
    # then download all pages specified
    with util.cd(args.output):
        # Calculate all md5sums in target download directory recursively
        md5sums = util.get_file_md5sums()
        for pg_num in args.pages:
            # Append which page to be downloaded as a query on the url
            page_url = danbooru.appendqueries(args.url, \
                    ["page={}".format(pg_num)])
            # Download the json file into a list
            json = danbooru.jsonize_post_url(page_url)
            # Transform the json list into a list of post objects
            posts = danbooru.extract_image_posts(json)

            # The trunc variable decides how much to truncate the filenames for output
            if (args.verbose == 0):
                trunc = 0
            if (args.verbose == 1):
                trunc = 30
            if (args.verbose == 2):
                trunc = None
            for post in posts:
                filepath = danbooru.image_post_path_gen(post)
                filename = danbooru.image_post_name_gen(post)
                fullpath = filepath + "/" + filename
                try:
                    os.mkdir(filepath)
                except FileExistsError:
                    pass
                if post.md5sum not in md5sums:
                    danbooru.download_image_post(fullpath, post, "http", \
                            "danbooru.donmai.us")

                    logger.info(lg, "<\033[33mNEW FILE\033[0m> {}".format(fullpath[0:trunc + 32]+"..."))
                    # Add the new file to the dict of calculated md5sums
                    md5sums[post.md5sum] = fullpath
                else:
                    logger.info(lg, \
                        "<\033[32mFILE MATCH\033[0m> \"{}\" -> \"{}\"".format( \
                        fullpath[0:trunc], md5sums[post.md5sum][0:trunc]+"..."))
# End of File
