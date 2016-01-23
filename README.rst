README
******

.. image:: https://travis-ci.org/tomschr/rstxml2docbook.svg?branch=develop
    :target: https://travis-ci.org/tomschr/rstxml2docbook
.. image:: https://codeclimate.com/github/tomschr/rstxml2docbook/badges/gpa.svg
    :target: https://codeclimate.com/github/tomschr/rstxml2docbook
    :alt: Code Climate

The :program:`rstxml2db` script converts RST XML files back to DocBook XML.

Installation
============

To install :program:`rstxml2db`, use one of the following methods:

1. Create a Python 3 environment::

    $ pyvenv .env

2. Update `pip` and `setuptools`::

    $ pip install -U pip setuptools

3. Install the package::

    $ pip install git+https://github.com/tomschr/rstxml2docbook.git@develop

After the installation in your Python virtual environment, two executable
scripts are available: :program:`rstxml2db` and :program:`rstxml2docbook`.
Both are the same, it's just for convenience.


Building the Intermediate XML Files
===================================

Usually, you first create the intermediate XML file (using the XML
builder with the `-b` option)::

   $ sphinx-build -b xml -d .../build/html.doctree src/ xml/

The `src/` directory contains the RST files, whereas the `xml/`
directory is the output directory.

Each RST file generates a corresponding XML file.


Building the DocBook Files
==========================

After you have created the intermediate XML files, it's now the time to
use the :program:`rstxml2db` script. The script reads in all XML files and
creates DocBook files, for example::

   $ rstxml2db xml/index.xml 

The previous step uses the `index.xml` file and writes all DocBook files
into the `out/` directory.

