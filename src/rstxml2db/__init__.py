#
# Copyright (c) 2016 SUSE Linux GmbH
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 3 of the GNU General Public License as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, contact SUSE LLC.
#
# To contact SUSE about this file by physical or electronic mail,
# you may find current contact information at www.suse.com

from .log import log, setloglevel
from .treebuilder import process_index
from .xslt import transform

import argparse
from itertools import chain
from lxml import etree
import os

HERE = os.path.dirname(os.path.abspath(__file__))
__all__ = ('__version__', 'main', )
__version__ = "0.0.1"
_booktree = '.booktree.xml'
_xsltfile = os.path.join(HERE, 'rstxml2db.xsl')


def main(cliargs=None):
    """Entry point for the application script

    :param list cliargs: Arguments to parse or None (=use sys.argv)
    :return: True or False
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose', action='count',
                        help="Increase verbosity level")

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + __version__
                        )
    parser.add_argument('-t', '--booktree',
                        default=_booktree,
                        help='save book tree to a given file (default %(default)r)',
                        )
    parser.add_argument('-d', '--output-dir',
                        dest='outputdir',
                        default='out',
                        help='save XML files given directory (default %(default)r)',
                        )
    parser.add_argument('-b', '--bigfile',
                        dest='bigfile',
                        default=None,
                        help='Create one, big file',
                        )

    parser.add_argument('indexfile',
                        help='index file (XML) which refer all other files')

    args = parser.parse_args(args=cliargs)
    log.info(args)

    # init log module
    setloglevel(args.verbose)

    if args.booktree == _booktree:
        args.booktree = os.path.join(os.path.dirname(args.indexfile), args.booktree)
        log.info("Using booktree %r", args.booktree)

    if not os.path.exists(args.outputdir):
        log.info("Creating output dir %r", args.outputdir)
        os.makedirs(args.outputdir)

    index = process_index(args.indexfile, args.booktree)
    log.info('')

    xslt = etree.XSLT(etree.parse(_xsltfile))

    for inputfile in index.iter('ref'):
        href = inputfile.attrib.get('href')
        infile = os.path.join(os.path.dirname(args.indexfile), href)
        outfile = os.path.join(args.outputdir, href)
        log.info("Using %r -> %r", infile, outfile)

        # Also create output structure
        try:
            os.makedirs(os.path.dirname(outfile))
        except OSError:
            pass

        # TODO: also process **params
        result, errors = transform(xslt, infile, os.path.abspath(args.booktree))
        result.write(outfile,
                     encoding='utf-8',
                     pretty_print=True,
                     )
        log.info("Writing transformation results to %r", outfile)
        for entry in errors:
            print(entry)

    if args.bigfile is not None:
        indexfile = os.path.join(args.outputdir, os.path.basename(args.indexfile))
        xml = etree.parse(indexfile)
        # Resolve all XIncludes
        xml.xinclude()
        #xml.write(args.bigfile,
        #          encoding='unicode',
        #          pretty_print=True,
        #          )
        rootname = xml.getroot().tag
        doctype="""<!DOCTYPE {} PUBLIC
  "-//OASIS//DTD DocBook XML V4.5//EN"
  "http://docbook.org/xml/4.5/docbookx.dtd"
[
   <!--
    <!ENTITY % entities SYSTEM "entity-decl.ent">
    %entities;
    -->
]>""".format(rootname)
        with open(args.bigfile, 'w') as f:
            log.info("Writing bigfile to %r", args.bigfile)
            f.write(etree.tostring(xml,
                                   encoding='unicode',
                                   pretty_print=True,
                                   doctype=doctype,
                                   )
            )

