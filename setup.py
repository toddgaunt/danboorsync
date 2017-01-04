#! /usr/bin/env python3
from distutils.core import setup

setup(
    description = 'File downloader for danbooru',
    author = 'Todd Gaunt',
    url = 'https://www.github.com/toddgaunt/danboorsync',
    download_url = 'https://www.github.com/toddgaunt/danboorsync',
    author_email = 'toddgaunt@protonmail.ch',
    version = '1.1',

    packages = ['danboorsync'],

    package_dir =  {'danboorsync':'danboorsync'},

    # Change these per distribution
    data_files = [('/usr/share/man/man1', ['doc/danboorsync.1']),
                  ('/usr/share/licenses/danboorsync/LICENSE', ['doc/LICENSE'])],

    scripts = ['bin/danboorsync'],
    name = 'danboorsync'
)
