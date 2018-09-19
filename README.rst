Convert RST to DocBook XML
**************************


.. image:: https://img.shields.io/badge/license-gpl-blue.svg
    :target: https://github.com/openSUSE/rstxml2docbook/blob/develop/LICENSE
    :alt: License GPL 3+
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

The :program:`rstxml2db` script converts RST XML files to DocBook XML.


Quick Start
===========

To use the program without :command:`pip` and virtual environment, use the
following command after cloning this repository::

    $ PYTHONPATH=src python3 -m rstxml2db -h


Installing
==========

To install :program:`rstxml2db` in a Python virtual environment,
use the following steps:

#. Clone this repository::

    $ git clone http://github.com/openSUSE/rstxml2docbook.git
    $ cd rstxml2docbook

#. Create a Python 3 environment and activate it::

    $ python3 -m venv .env
    $ source .env/bin/activate

#. Update the ``pip`` and ``setuptools`` modules::

    $ pip install -U pip setuptools

#. Install the package::

    $ ./setup.py develop

If you need to install it from GitHub directly, use this URL::

    git+https://github.com/openSUSE/rstxml2docbook.git@develop

After the installation in your Python virtual environment, two executable
scripts are available: :program:`rstxml2db` and :program:`rstxml2docbook`.
Both are the same, it's just for convenience.


Workflow
========

The script does the following steps:

#. Read the intermediate XML files from a previous Sphinx conversion step
   (see :ref:`sec.build.xml.files`).

#. Resolves any references to external files and create a single XML tree
   in memory.

#. Transform the tree with XSLT into DocBook and if requested, split it
   into several smaller files.

#. Output to stdout or save it into one or more file, depending on if
   splitting mode is activated.


.. _sec.build.xml.files:

Building the Intermediate XML Files
===================================

Usually, you first create the intermediate XML file (using the XML
builder with the :option:`-b` option)::

   $ sphinx-build -b xml -d .../build/html.doctree src/ xml/

The ``src/`` directory contains all of your RST files, whereas the ``xml/``
directory is the output directory.

Each RST file generates a corresponding XML file.


Building the DocBook Files
==========================

After you have created the intermediate XML files, it's now time to
use the :program:`rstxml2db` script. The script reads in all XML files and
creates DocBook files, for example::

   $ rstxml2db xml/index.xml

By default, the previous step uses the :file:`index.xml` file and
generates several DocBook files all located in the ``out/`` directory.

If you need one DocBook file, use the option :option:`-ns` to output the
result DocBook file on stdout.


The Internal Workflow
=====================

The workflow from converting RST XML files into DocBook involves these steps:

#. Load the :file:`index.xml` file.

#. Resolve all external references to other files; create one single RST XML tree.

#. If :option:`--legalnotice` is used, add the legalnotice file into
   :code:`bookinfo`.

#. If :option:`--conventions` is used, replace first chapter with
   :code:`preface` content.

#. Clean up XML:

   a. Remove IDs with no corresponding :code:`<xref/>`.
   b. Fix absolute colum width into relative value.
   c. Add processing instruction in :code:`<screen>`, if the maximum characters
      inside screen exceeds a certain value.

#. Output tree, either by saving it or by printing it to std out.


The transformation from separate RST XML files into a single RST XML tree
uses mainly the element :code:`list_item[@classes='toctree-l1']`. Anything that
is referenced is used as a file for inclusion. Everything else is copied
as it is.


The transformation from the single RST XML tree into DocBook 5 uses the
:file:`rstxml2db.xsl` stylesheet.


Things to Know During Convertion
================================

The convertion internally creates a single RST XML tree. This tree contains
*all* information which is needed.

For example, the following things work:

* Internal referencing from one section to another (element
  :code:`reference[@internal='True']`)
* Internal references to a glossary entry (element
  :code:`reference[@internal='True']`, but
  with :code:`@refuri` containing an :code:`#` character
* External referencing to a remote site (element ``reference[@refuri]``)
* Different, nested sections are corretly converted into the DocBook structures
  (book, chapter, section etc.)
* Admonition elements
* Tables and figures
* Lists like :code:`bullet_list`, :code:`definition_list`, and
  :code:`enumerated_list`
* Glossary entries
* Inline elements like :code:`strong`, :code:`literal_emphasis`

The following issues are still problematic:

* **Double IDs**
  When RST contains the same title, the same IDs are generated from the RST
  XML builder. I consider it as a bug.

* **Invalid Structures**
  RST allows structures which are not valid for DocBook. For example, when
  you have sections and add after the last section you add more paragraphs.
  This will lead to validation errors in DocBook.
  The script currently does not detect these structural issues. You need to
  adapt the structure manually.
