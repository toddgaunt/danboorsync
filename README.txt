IMGFETCH(1)                 General Commands Manual                IMGFETCH(1)



NAME
       imgfetch - File fetching utility.


SYNOPSIS
       imgfetch [-h] [-v] [-q] [-o <path>] SUBCOMMAND

DESCRIPTION
       Download image batches from a website specified with subcommand.


OPTIONS
       -h     Show a help message and exit.

       -q     Lower more verbose output. Can be flagged multiple times.

       -v     Increase more verbose output. Can be flagged multiple times.

       -o <path>
              Specify a directory to download to. Default is current directory
              ('.').


SUBCOMMAND OPTIONS
       Please see the manpage for each subcommand.


SUBCOMMANDS
       imgfetch-danbooru
              Syncronize a local directory with a danbooru tag search url.


BUGS
       Please report bugs by emailing me at  toddgaunt@protonmail.ch,  or  fix
       them  yourself  and  make a pull request to https://www.github.com/tod‐
       dgaunt/imgfetch if you've got nothing better to do.


AUTHOR
       This man page and imgfetch itself  were  originally  authored  by  Todd
       Gaunt.


SEE ALSO
       imgfetch-danbooru(1)



                                   imgfetch                        IMGFETCH(1)
