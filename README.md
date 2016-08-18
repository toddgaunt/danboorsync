imgfetch
========

### A file downloader for 4chan and Danbooru

imgfetch is a simple image downloader for 4chan and Danbooru written in python3. It only uses standard python3 modules and has multiple commandline arguments. The script utitlizes APIs of various sites so extending it's cabapilities to work with imageboards that use these APIs is very easy. Imgfetch also fully supports md5 has checking on downloaded images so a thread can be downloaded every few minutes to download the latest images without having to download/create duplicate files.

#### SUPPORTED SITES

Danbooru -> https://danbooru.donmai.us/ (possibly others but untested)

4chan -> https://www.4chan.org/

#### USAGE

run by entering:
```python
python imgfetch [ options ] URL [URL ...]
```

#### OPTIONS

Options | explanation
--------|------------
-h | Displays a help message
-d DIR | Takes an argument 'dir' that refers to the directory imgfetch will download to
-q | Quiets imgfetch's output
-v | Prints images downloaded and md5sums (if available) to terminal
-m METHOD | Uses METHOD to determine how it should check incoming files against files on disk ("md5", "name"). md5sum checking is deafult behavior, while name is fallback.
URL ... | Takes any number of urls and processes them all one at a time

#### INSTALLATION
run by entering:
```python
git clone https://www.github.com/toddgaunt/imgfetch
cd imgfetch
./setup.py build
./setup.py install
```

then copy the script bin/imgfetch to somewhere in your PATH, and invoke it with your shell



#### LICENSE
The MIT License (MIT)

Copyright (c) 2016 Todd Gaunt

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

