#! /usr/bin/env python3
from distutils.core import setup

setup(
    description = 'File downloader for danbooru',
    author = 'Todd Gaunt',
    url = 'https://www.github.com/toddgaunt/imgfetch',
    download_url = 'https://www.github.com/toddgaunt/imgfetch',
    author_email = 'toddgaunt@protonmail.ch',
    version = '2.1.0',

    packages = ['imgfetch'],

    package_dir =  {'imgfetch':'imgfetch'},

    # Change these per distribution
    data_files = [('/usr/share/man/man1', ['doc/imgfetch.1']),
                  ('/usr/share/man/man1', ['doc/imgfetch-danbooru.1']),
                  ('/usr/share/licenses/imgfetch/LICENSE', ['doc/LICENSE'])],

    scripts = ['bin/imgfetch'],
    name = 'imgfetch'
)
