#
# License: MIT (doc/LICENSE)
# Author: Todd Gaunt

# package imports
import argparse
import re
import os
from urllib.parse import urlparse, parse_qs

# module imports
from danboorsync import danbooru
from danboorsync import logger

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

def parse_args():
    parser = argparse.ArgumentParser(description='Downloads images en masse from Danbooru')

    parser.add_argument('-o', '--output', metavar='dir',
                        type=str,
                        help='Specify a directory to create the download directory')

    parser.add_argument('-p', '--pages', metavar='range',
                        type=str, default="1",
                        help='Specify a page range to download from, \
                                e.g. danboorsync -p 1-5,10,15-20')

    parser.add_argument('-q', '--quiet',
                        action="store_true", default=False,
                        help='Turn off all output')

    parser.add_argument('-v', '--verbose',
                        action="count", default=1,
                        help='Display files downloaded')

    parser.add_argument('url', metavar='url',
                    type=str,
                    help='Url to download from')

    args = parser.parse_args()

    # Set the verbosity
    if args.quiet:
        args.verbose = 0

    lg = logger.logger(__name__, args.verbose);

    if urlparse(args.url).netloc != "danbooru.donmai.us":
        logger.error(lg, "Invalid url, doesn't match danbooru netloc")

    if not args.output:
        args.output = "."
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

    return args

# End of file
