#! /usr/bin/env python3
from distutils.core import setup

setup(
    description = 'File downloader for danbooru and fourchan',
    author = 'Todd Gaunt',
    url = 'https://www.github.com/toddgaunt/imgfetch',
    download_url = 'https://www.github.com/toddgaunt/imgfetch',
    author_email = 'toddgaunt@protonmail.ch',
    version = '1.3',

    packages = ['imgfetch',
                'imgfetch.api'],

    package_dir =  {'imgfetch':'src',
                    'imgfetch.api':'src/api'},

    # Change these per distribution
    data_files = [('usr/share/man/man1', ['doc/imgfetch.1']),
                  ('usr/share/licenses/imgfetch/LICENSE', ['doc/LICENSE'])],

    scripts = ['bin/imgfetch'],
    name = 'imgfetch'
)
