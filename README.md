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
