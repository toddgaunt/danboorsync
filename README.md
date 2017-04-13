imgfetch
========

### A picture file downloader

imgfetch lets you syncronize a directory of pictures.

### SUPPORTED SITES

imagefetch-danbooru: https://danbooru.donmai.us/

### USAGE

Run by entering:
```python
imgfetch [ options ] SUBCOMMAND
```

### SUBCOMMANDS

##### imgfetch-danbooru [-p <range>] TAGS...

| command | description |
| --- | --- |
| -p range | Specify a page range to download from, e.g. "-p 1-5,10,15-20". |
| TAGS... | The image tags that specify which images to download, e.g.
"hatsune_miku cute". |

#####

An example of this subcommand would be:
```sh
imgfetch -o vocaloid danbooru -p 1-5 hatsune_miku cute
```

### DOWNLOAD AND INSTALLATION

Enter the following commands:
```sh
git clone https://www.github.com/toddgaunt/imgfetch
cd imgfetch
./setup.py build
sudo ./setup.py install
```
