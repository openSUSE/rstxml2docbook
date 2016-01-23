:orphan:

.. rstxml2docbook documentation master file, created by
   sphinx-quickstart on Thu Jan 14 14:35:57 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

rstxml2db Manual Page Version 0.0.2
===================================

Synopsis
--------

**rstxml2docbook** [*options*] <*INDEXFILE*>


Description
-----------

:program:`rstxml2db` generates DocBook XML files from an `index.xml`
file. This `index.xml` file is generated through the :program:`sphinx-build`
script with the XML builder (option :option:`-b xml`).


Options
-------

-h, --help                     Prints the help text
-v, --verbose                  Increase verbosity (can be repeated)
-t <file>, --booktree <file>   Save book tree structure in separate file
                               (default `.booktree.xml`)
-d <dir>, --output-dir <dir>   Save XML files into <dir> directory
                               (default `out`)
-b <BIGFILE>, --bigfile <BIGFILE>
                               Create a single DocBook XML file
-k, --keep-all-ids             By default, IDs in bigfile are removed if they
                               are not referenced. This option keeps all IDs.
-n <PRODUCTNAME>, --productname <PRODUCTNAME>
                               Name of the product (included into `book/bookinfo`)
-p <PRODUCTNUMBER>, --productnumber <PRODUCTNUMBER>
                               Number/release etc. of the product (also
                               included into `book/bookinfo`)
-l <LEGALNOTICE>, --legalnotice <LEGALNOTICE>
                               Path to filename which contains a `legalnotice`
                               element (also included into `book/bookinfo`)
<INDEXFILE>                    Index file (XML) which refer all other files




See also
--------

:manpage:`sphinx--build`


Author
------

Thomas Schraitle <toms AT suse.de> for SUSE Linux GmbH
