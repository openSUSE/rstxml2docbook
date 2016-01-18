README
******

The `rstxml2db` script converts RST XML files back to DocBook XML.


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
use the `rstxml2db` script. The script reads in all XML files and
creates DocBook files, for example::

   $ rstxml2db xml/index.xml 

The previous step uses the `index.xml` file and writes all DocBook files
into the `out/` directory.

