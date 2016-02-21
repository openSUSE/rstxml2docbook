:orphan:

.. rstxml2docbook documentation master file, created by
   sphinx-quickstart on Thu Jan 14 14:35:57 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

rstxml2db Manual Page Version 0.4.4
===================================

Synopsis
--------

.. _invocation:

.. sourcecode:: bash

     $ rstxml2docbook [options] <INDEXFILE>
     $ rstxml2db [options] <INDEXFILE>

Run the script either by :program:`rstxml2docbook` or :program:`rstxml2db`, both are the same.


Description
-----------

:program:`rstxml2db` generates DocBook 5 XML files from an :file:`index.xml`
file. This :file:`index.xml` file is generated through the :program:`sphinx-build`
script with the XML builder (option ``-b xml``). Standard options are:

.. program:: rstxml2db
.. program:: rstxml2docbook

.. option:: -h, --help, --version

   Display usage summary or script version.

.. option:: -v, --verbose

   Increase verbosity (can be repeated).

.. option:: INDEXFILE

   denotes the index file (XML) which refer all other files.


Options
-------

.. option:: -4, --db4

   Create DocBook 4 version (default False).

.. option:: -c <CONVENTIONS>, --conventions <CONVENTIONS>

   Path to filename which contains doc conventions about the
   document (usually ``<preface>`` or ``<chapter>``); will
   replace the first chapter.

.. option:: -k, --keep-all-ids

   By default, IDs in a bigfile are removed if they are not
   referenced. This option keeps all IDs.

.. option:: -l <LEGALNOTICE>, --legalnotice <LEGALNOTICE>

   Path to filename which contains a `legalnotice` element
   (also included into ``book/bookinfo``).

.. option:: -P <PRODUCTNUMBER>, --productnumber <PRODUCTNUMBER>

   Number/release etc. of the product (also included into
   ``book/bookinfo``).

.. option:: -p <PARAM>, --param <PARAM>

   single XSLT parameter; use the syntax "NAME=VALUE",
   can be used multiple times.

.. option:: -o <output>, --output <output>

   save DocBook XML file to the given path.


Examples
--------

* Create a DocBook 5 XML file from :file:`index.xml` and print its output to stdout::

    $ rstxml2db index.xml

* Create a DocBook 5 XML file rom :file:`index.xml` and save it to :file:`output.xml`::

    $ rstxml2db -o output.xml index.xml

* Create a DocBook 4 XML file from :file:`index.xml`, use the option :option:`--db4`
  and save it to :file:`output.xml`::

    $ rstxml2db --db4 -o output.xml index.xml

* Create a DocBook 5 XML file from :file:`index.xml` and use ``FooObfuscator`` as
  productname::

    $ rstxml2db --productname 'FooObfuscator' -o output.xml index.xml

* Create a DocBook 5 XML file from :file:`index.xml` and append legal notice from
  file :file:`legal.xml`::

    $ rstxml2db -o output.xml --legalnotice legal.xml index.xml

* Create a DocBook 5 XML file from :file:`index.xml`, save it to :file:`output.xml`,
  and use some parameters::

    $ rstxml2db  -o output.xml --param "a=2" --param "b=5" index.xml

See also
--------

:manpage:`sphinx-build`


Author
------

Thomas Schraitle <toms AT suse.de> for SUSE Linux GmbH
