README
******

License: GPL 3+

.. image:: https://travis-ci.org/tomschr/rstxml2docbook.svg?branch=develop
    :target: https://travis-ci.org/tomschr/rstxml2docbook
    :alt: Travis CI
.. image:: https://codeclimate.com/github/tomschr/rstxml2docbook/badges/gpa.svg
    :target: https://codeclimate.com/github/tomschr/rstxml2docbook
    :alt: Code Climate
.. image:: https://scrutinizer-ci.com/g/tomschr/rstxml2docbook/badges/quality-score.png?b=develop
    :target: https://scrutinizer-ci.com/g/tomschr/rstxml2docbook/?branch=develop
    :alt: Scrutinizer Code Quality
.. image:: https://codecov.io/github/tomschr/rstxml2docbook/coverage.svg?branch=develop
    :target: https://codecov.io/github/tomschr/rstxml2docbook?branch=develop
    :alt: Code Coverage

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


The Internal Workflow
=====================

The workflow from the RST XML files to DocBook involves these steps:

1. Load the ``index.xml`` file.

2. Resolve all external references to other files; create one single RST XML tree.

3. If ``--legalnotice`` is used, add the legalnotice file into ``bookinfo``.

4. If ``--conventions`` is used, replace first chapter with ``preface`` content.

5. Clean up XML:

   a. Remove IDs with no corresponding ``<xref/>``.
   b. Fix absolute colum width into relative value.
   c. Add processing instruction in ``<screen>``, if the maximum characters
      inside screen exceeds a certain value.

6. Transform DocBook 4 tree into DocBook 5, if option ``--db4`` is not set.

7. Output tree, either by saving it or by printing it to std out.


The transformation from separate RST XML files into a single RST XML tree
uses mainly the element ``list_item[@classes='toctree-l1']``. Anything that
is referenced is used as a file for inclusion. Everything else is copied
as it is.


The transformation from the single RST XML tree into DocBook 4 use the
``rstxml2db.xsl`` stylesheet.
