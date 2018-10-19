How to Develop rstxml2docbook
*****************************

.. docutils: http://docutils.sourceforge.net/

The following sections helps you in developing :program:`rstxml2docbook`.


Preparations
============

#. Create a Python 3 environment and activate it::

    $ pyvenv .env
    $ source .env/bin/activate

#. Update the ``pip`` and ``setuptools`` modules::

    $ pip install -U pip setuptools

#. Install the package::

    $ ./setup.py develop

After you have completed the previous steps, the scripts :program:`rstxml2db`
and :program:`rstxml2docbook` are available in your path (``.env/bin``).


Executing the Test Cases
========================

To execute all the tests, run::

   $ ./setup.py test

To use :command:`pytest`, run::

   $ pytest

In case the :command:`pytest` command fails, use :file:`setup.py`.

To get a more verbose output, use the options ``-l`` and ``-vv``::

   $ pytest -l -vv

To select only a single test, use the complete test filename::

   $ pytest tests/test_foo.py

This will execute *all* tests inside the file :file:`test_foo.py`.
To execute only a specific test function inside a file, use this notation::

  $ pytest test/test_foo.py::test_bar


Writing Test Cases
==================

Each test consists of the following files:

:file:`NAME-001.xml`
   is the XML file in the Docutils format. The project is located on
   http://docutils.sourceforge.net/.

:file:`NAME-001.params.json`
   is the parameter file which contains XPaths and results.

It's important that you name your testcase with the extensions :file:`.xml`
and :file:`.params.json`. The testing framework searches for these extensions.
When it cannot find a corresponding file, it will skip the test.

The idea behind this structure was to avoid issues with formatting. Comparing
two XML structures which only distinguish between formatting may show differences.
However, from a XML perspective, these differences are not important due to
formatting issues. For example, attribute order, order of namespaces, indendation
etc. are not relevant to XML.

If you want to create a new test case, proceed as follows:

#. Create a XML file and use the extension :file:`.xml`. It's easier if
   you use the DTD from the Docutils project.
   The content should contain a minimal structure. Remove anything that is
   unneccessary.

#. Create a parameters file and use the extension :file:`.params.json`.
   This file is a json file and contains a list. The list contains a pair of
   XPath expressions and the result.
   For example, the following JSON file contains two XPath expressions and
   the expected result:

   .. code-block:: json

      [
         ["namespace-uri(/*)", "http://docbook.org/ns/docbook"],
         ["local-name(/*)", "book"]
      ]

#. Run the test/test suite.

#. Fix any problems.


Things to Watch For
===================

* The JSON file has to be valid; any syntax errors leads to an exception.
* No commas at the last list!
* The parameter file needs to have XPath expressions which returns booleans
  (true/false), strings, numbers, or a list.
  Other structures are not supported and probably doesn't make any sense.
