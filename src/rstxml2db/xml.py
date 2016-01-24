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


import os
import sys

from lxml import etree

from .cleanup import cleanupxml
from .core import BOOKTREE
from .core import XSLTRST2DB
from .log import log
from .log import setloglevel
from .treebuilder import process_index
from .xslt import transform


def bigfile(args):
    """Resolve all XIncludes and save file

    :param args: :class:`argparse.Namespace`
    """

    indexfile = os.path.join(args.outputdir, os.path.basename(args.indexfile))
    xml = etree.parse(indexfile)
    # Resolve all XIncludes
    xml.xinclude()

    # Search for all <xref/>s and remove unused IDs
    if args.keepallids:
        cleanupxml(xml)

    rootname = xml.getroot().tag
    doctype = r"""<!DOCTYPE {} PUBLIC
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

def prepare_process(args):
    """Some preparation steps before running process()

    :param args: result from `argparse` parser
    :return: None
    """
    if args.booktree == BOOKTREE:
        args.booktree = os.path.join(os.path.dirname(args.indexfile), args.booktree)
        log.info("Using booktree %r", args.booktree)

    if not os.path.exists(args.outputdir):
        log.info("Creating output dir %r", args.outputdir)
        os.makedirs(args.outputdir)


def process_iter_ref(args, index, xslt):
    """Iterate over all ref elements and transform RST XML -> DocBook XML

    :param args: result from `argparse` parser
    :param index: XML tree of booktree structure
    :param xslt: :class:`etree.XSLT` from stylesheet
    :return: None
    """
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
        result, errors = transform(xslt,
                                   infile,
                                   os.path.abspath(args.booktree),
                                   productname=args.productname,
                                   productnumber=args.productnumber,
                                   legalnotice=args.legalnotice,
                                   **dict(args.params)
                                   )
        result.write(outfile,
                     encoding='utf-8',
                     pretty_print=True,
                     )
        log.info("Writing transformation results to %r", outfile)
        for entry in errors:
            print(entry, file=sys.stderr)


def process(args):
    """Process arguments from CLI parser

    :param args: result from `argparse` parser
    :return: True or False
    """
    # init log module
    setloglevel(args.verbose)
    prepare_process(args)

    index = process_index(args.indexfile, args.booktree)
    log.info('')

    xslt = etree.XSLT(etree.parse(XSLTRST2DB))
    process_iter_ref(args, index, xslt)

    bigfile(args)
    return 0
