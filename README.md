Danboorsync
========

### A file downloader for Danbooru

Danboorsync lets you syncronize a directory of pictures according to a tag search on danbooru

#### SUPPORTED SITES

Danbooru -> https://danbooru.donmai.us/

#### USAGE

run by entering:
```python
python3 danboorsync [ options ] URL [URL ...]
```

#### OPTIONS

Options | explanation
--------|------------
-p range | Specify a page range to download from, e.g. "danboorsync -p 1-5,10,15-20"
-h | Show a help message and exit
-o dir | Specify a directory to download to. Default is current directory.
-q | Turns off all output
-v | Display files downloaded
URL | Url to download from
#### INSTALLATION
run by entering:
```python
git clone https://www.github.com/toddgaunt/danboorsync
cd danboorsync
./setup.py build
sudo ./setup.py install
```

#### LICENSE
The MIT License (MIT)

Copyright (c) 2016 Todd Gaunt

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

