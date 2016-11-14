#
# License: MIT (doc/LICENSE)
# Author: Todd Gaunt
#
# File: imgfetch/fourchan.py
# This file contains all relevant functions for interacting with the 4chan API

import json
import base64
from urllib.parse import urlparse
from urllib.request import urlopen

from imgfetch import logger, util, net
from imgfetch.structs import generic_post

def proceed(url, args):
    site, parsed_url, thread, board = format_url(url)
    generic_posts = generic_post_gen(net.get_json(parsed_url +'.json')[0]['posts'])

    # Creates dir based off of thread name
    dest_dir = thread
    util.make_dir(dest_dir)
    logger.output(args.verbose, "Download directory '" + dest_dir + "'")

    with util.cd(dest_dir):
        # Does all the business in the arg directory
        for post in generic_posts:
            md5sums = []
            if args.method == "md5":
                md5sums = util.get_file_md5s()

                # fourchan hashes their md5sums with base64
                if md5sums:
                    for i in range(len(md5sums)):
                        md5sums[i] = base64.b64encode(md5sums[i])

            # Fill in some data that wasn't in the json
            post.url = "https://i.4cdn.org/" + str(board) \
                            + "/" + str(post.url) + str(post.ext)

            net.download_file(args.verbose, post, md5sums)
        logger.output(args.verbose, "All files downloaded to " + "'" + dest_dir + "'" + "\n")

def format_url(url):
    """Grabs the url without thread name, thread name, and board.
    Returns a tuple with all three"""
    urlpath = urlparse(url).path.split("/") # For grabbing thread name and board name
    url = url.split("/")
    thread = urlpath[-1] # threadname is last part of path
    board = urlpath[1] # boardname is first part of path
    url = "/".join(url[0:-1]) # cuts off the thread name for when the json file is fetched
    site = urlparse(url).netloc
    return (site, url, thread, board)

def generic_post_gen(posts):
    """parses json files for any info on images, and return
    a list of image objects that hold the data."""
    generic_posts = []
    for i in posts:
        try:
            filename = (str(i['filename']) + '_' + str(i['w']) + 'x' + str(i['h']) \
                       + str(i['ext']))
            tmp = generic_post(\
                name = filename, \
                ext = i['ext'], \
                url = i['tim'], \
                md5 = str.encode(i['md5']))

            generic_posts.append(tmp)
        except KeyError as key:
            # Not every 4chan post has a file, so skip it if no filename
            if str(key) != "'filename'":
                logger.error(1, "Json key error: " + str(key) + " not found")
            else:
                continue
    return generic_posts
