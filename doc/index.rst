:orphan:

.. rstxml2docbook documentation master file, created by
   sphinx-quickstart on Thu Jan 14 14:35:57 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

rstxml2db Manual Page Version 0.4.2
===================================

Synopsis
--------

**rstxml2docbook** [*options*] <*INDEXFILE*>

**rstxml2db** [*options*] <*INDEXFILE*>


Description
-----------

:program:`rstxml2db` generates DocBook 5 XML files from an `index.xml`
file. This `index.xml` file is generated through the :program:`sphinx-build`
script with the XML builder (option :option:`-b xml`).

<INDEXFILE> denotes the index file (XML) which refer all other files.


Options
-------

-h, --help                     Prints the help text.
-4, --db4                      Create DocBook 4 version (default False).
-c <CONVENTIONS>, --conventions <CONVENTIONS>
                               path to filename which contains doc conventions
                               about the document (usually ``<preface>`` or
                               ``<chapter>``);
                               will replace the first chapter.
-k, --keep-all-ids             By default, IDs in bigfile are removed if they
                               are not referenced. This option keeps all IDs.
-l <LEGALNOTICE>, --legalnotice <LEGALNOTICE>
                               Path to filename which contains a `legalnotice`
                               element (also included into ``book/bookinfo``).
-N <PRODUCTNAME>, --productname <PRODUCTNAME>
                               Name of the product (included into
                               ``book/bookinfo``).
-P <PRODUCTNUMBER>, --productnumber <PRODUCTNUMBER>
                               Number/release etc. of the product (also
                               included into ``book/bookinfo``).
-p <PARAM>, --param <PARAM>    single XSLT parameter; use the syntax "NAME=VALUE",
                                 can be used multiple times.
-o <output>, --output <output>   save DocBook XML file to the given path.
-v, --verbose                  Increase verbosity (can be repeated).



Examples
--------

* Create DocBook 5 XML from ``index.xml`` and output it to stdout::

    $ rstxml2db index.xml

* Create DocBook 5 XML from ``index.xml`` and save it to `output.xml`::

    $ rstxml2db -o output.xml index.xml

* Create DocBook 4 XML from ``index.xml`` and save it to `output.xml`::

    $ rstxml2db --db4 -o output.xml index.xml

* Create DocBook 5 XML from ``index.xml`` and use `FooObfuscator` as
  productname::

    $ rstxml2db --productname 'FooObfuscator' -o output.xml index.xml

* Create DocBook 5 XML from `index.xml`` and append legal notice from
  file `legal.xml`::

    $ rstxml2db -o output.xml --legalnotice legal.xml index.xml

* Create DocBook 5 XML from ``index.xml``, save it to `output.xml`,
  and use some parameters::

    $ rstxml2db  -o output.xml --param "a=2" --param "b=5" index.xml

See also
--------

:manpage:`sphinx--build`


Author
------

Thomas Schraitle <toms AT suse.de> for SUSE Linux GmbH
