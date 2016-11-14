#
# License: MIT (doc/LICENSE)
# Author: Todd Gaunt
#
# File: imgfetch/danbooru.py
# This file contains all relevant functions for interacting with the danbooru API

import json
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen

from imgfetch import logger, util, net
from imgfetch.structs import generic_post

def proceed(url, args):
    url = urlparse(url)
    posts = net.get_json(format_url(url))
    generic_posts = generic_post_gen(posts, url)

    # Creates dir based off of queries, or if its a single file it's name
    dest_dir = ''
    queries = parse_qs(url.query)
    if len(generic_posts) == 1:
        dest_dir = generic_posts[0].name
    elif queries:
        for i in queries['tags']:
            if len(dest_dir) < 20:
                dest_dir += i
    else:
        dest_dir = url.path
    util.make_dir(dest_dir)
    logger.output(args.verbose, "Download directory '" + dest_dir + "'")

    with util.cd(dest_dir):
        for post in generic_posts:
            # Does all the business in the dest_dir
            md5sums = []
            if args.method == "md5":
                md5sums = util.get_file_md5s()

                # danbooru uses hexidecimal representations of md5sums
                if md5sums:
                    for i in range(len(md5sums)):
                        md5sums[i] = (str.encode(md5sums[i].hex()))

            net.download_file(args.verbose, post, md5sums)
        logger.output(args.verbose, "All files downloaded to " + "'" + dest_dir + "'" + "\n")

def format_url(url):
    """Uses the given url string to fetch a json file"""
    query = ""
    if url.query:
        query = '?' + url.query
    json_url = url.scheme + "://" + url.netloc + url.path \
                       + ".json" + query
    return json_url

def generic_post_gen(posts, url):
    """Creates generic posts out of Danbooru posts"""
    generic_posts = []
    for post in posts:
        tmp = generic_post( \
            name = filename_gen(post), \
            ext = post['file_ext'], \
            url = url.scheme + "://" + url.netloc + str(post['file_url']), \
            md5 = str.encode(post['md5']))

        generic_posts.append(tmp)
    return generic_posts

def filename_gen(post):
    name = ""
    for character in post['tag_string_character'].split():
        if len(name) > 80:
            break;
        name += util.remove_chars(character) + '_'
    for tag in post['tag_string_general'].split():
        if len(name) > 80:
            break;
        name += util.remove_chars(tag) + '_'
    name += str(post['image_width']) + 'x' \
          + str(post['image_height']) + '.' \
          + str(post['file_ext'])

    return name
