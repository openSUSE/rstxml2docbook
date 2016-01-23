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
-d <dir>, --output-dir <dir>   Save XML files into <dir> directory
<INDEXFILE>                    Index file (XML) which refer all other files


See also
--------

:manpage:`sphinx--build`


Author
------

Thomas Schraitle <toms AT suse.de>
