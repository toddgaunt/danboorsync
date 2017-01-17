imgfetch
========

### A file downloader for Danbooru

imgfetch lets you syncronize a directory of pictures according to a tag search on danbooru

### SUPPORTED SITES

imgfetch-danbooru -> https://danbooru.donmai.us/

### USAGE

Run by entering:
```python
imgfetch [ options ] [ command ] 
```

### SUBCOMMANDS

##### imgfetch-danbooru

| command | description |
| --- | --- |
| -p range | Specify a page range to download from, e.g. "imgfetch -p 1-5,10,15-20" |
| --- | --- |
| URL | Required argument, the url of the image search to download e.g. "http://danbooru.donmai.us/posts?tags=nanakorobi_nene" |

#####

### INSTALLATION

Enter the following commands:
```sh
git clone https://www.github.com/toddgaunt/imgfetch
cd imgfetch
./setup.py build
sudo ./setup.py install
```

### LICENSE
The MIT License (MIT)

Copyright (c) 2016 Todd Gaunt

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
