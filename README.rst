Convert RST to DocBook XML
**************************

License: GPL 3+

.. image:: https://travis-ci.org/openSUSE/rstxml2docbook.svg?branch=develop
    :target: https://travis-ci.org/openSUSE/rstxml2docbook
    :alt: Travis CI
.. image:: https://codeclimate.com/github/openSUSE/rstxml2docbook/badges/gpa.svg
    :target: https://codeclimate.com/github/openSUSE/rstxml2docbook
    :alt: Code Climate
.. image:: https://scrutinizer-ci.com/g/openSUSE/rstxml2docbook/badges/quality-score.png?b=develop
    :target: https://scrutinizer-ci.com/g/openSUSE/rstxml2docbook/?branch=develop
    :alt: Scrutinizer Code Quality
.. image:: https://codecov.io/github/openSUSE/rstxml2docbook/coverage.svg?branch=develop
    :target: https://codecov.io/github/openSUSE/rstxml2docbook?branch=develop
    :alt: Code Coverage

The :program:`rstxml2db` script converts RST XML files back to DocBook XML.


Quick Start
===========

To use the program without :command:`pip`, use the following command:

::
    $ PYTHONPATH=src python3 -m rstxml2db -h



Installation
============

To install :program:`rstxml2db`, use the following steps:

1. Create a Python 3 environment and activate it::

    $ pyvenv .env
    $ source .env/bin/activate

2. Update `pip` and `setuptools`::

    $ pip install -U pip setuptools

3. Install the package::

    $ pip install git+https://github.com/openSUSE/rstxml2docbook.git@develop
    or use
    $ pip install -e .

After the installation in your Python virtual environment, two executable
scripts are available: :program:`rstxml2db` and :program:`rstxml2docbook`.
Both are the same, it's just for convenience.


Building the Intermediate XML Files
===================================

Usually, you first create the intermediate XML file (using the XML
builder with the `-b` option)::

   $ sphinx-build -b xml -d .../build/html.doctree src/ xml/

The `src/` directory contains all of your RST files, whereas the `xml/`
directory is the output directory.

Each RST file generates a corresponding XML file.


Building the DocBook Files
==========================

After you have created the intermediate XML files, it's now time to
use the :program:`rstxml2db` script. The script reads in all XML files and
creates DocBook files, for example::

   $ rstxml2db xml/index.xml 

The previous step uses the `index.xml` file and writes all DocBook files
into the `out/` directory.


The Internal Workflow
=====================

The workflow from converting RST XML files into DocBook involves these steps:

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


Things to Know During Convertion
================================

The convertion internally creates a single RST XML tree. This tree contains
*all* information which is needed.

For example, the following things work:

* Internal referencing from one section to another (element ``reference[@internal='True']``)
* Internal references to a glossary entry (element ``reference[@internal='True']``, but
  with ``@refuri`` containing an ``#`` character
* External referencing to a remote site (element ``reference[@refuri]``)
* Different, nested sections are corretly converted into the DocBook structures
  (book, chapter, section etc.)
* Admonition elements
* Tables and figures
* Lists like ``bullet_list``, ``definition_list``, and ``enumerated_list``
* Glossary entries
* Inline elements like ``strong``, ``literal_emphasis``

The following issues are still problematic:

* **Double IDs**
  When RST contains the same title, the same IDs are generated from the RST
  XML builder. I consider it as a bug.
