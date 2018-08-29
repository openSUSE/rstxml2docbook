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

"""
Implements CLI parsing
"""

import argparse
import logging
from logging.config import fileConfig
from os.path import exists
import sys
from lxml import etree

from . import __author__, __version__
from .common import ERROR_CODES
from .core import LOG_CONFIG, LOGFILECONFIGS, LOGLEVELS
from .xml import process


# fileConfig needs to come first before
lastfound = None
# We iterate from the last item as the
for s in reversed(LOGFILECONFIGS):  # pragma: no cover
    if exists(s):
        # If a file could be found, we are finish so break the loop
        lastfound = s
        break

if lastfound:
    fileConfig(lastfound)
else:
    # Provide minimum logging setup, if config files not found
    logging.config.dictConfig(LOG_CONFIG)  # pragma: no cover

log = logging.getLogger(__package__)


def prepareparams(params):
    """Convert the list with ``NAME=VALUE`` strings into
       tuples of ``('NAME', 'VALUE')``

       :param params: a list with ``NAME=VALUE`` entries
       :type params: list
       :return: a new list with ``('NAME', 'VALUE')`` entries
       :rtype: list
    """
    result = []
    if params is None:
        return result
    for item in params:
        try:
            name, value = item.split('=')
        except ValueError:
            log.warning("Parameter %r doesn't adhere to the "
                        "NAME=VALUE syntax. Skipping.",
                        item)
            continue
        result.append((name.strip(), value.strip()))
    return result


def print_all_xsl_params(parser):
    """Prints all availalbe XSLT parameters that can be used in -p/--param

    :param parser: the argument parser
    :type parser: :class:`argparse.ArgumentParse`
    """
    from .core import NSMAP, XSLTRST2DB
    print("--- Available XSLT Parameters, used with -p/--param ---")
    xslt = etree.parse(XSLTRST2DB)
    descrattr = str(etree.QName(NSMAP['doc'], 'descr'))
    for param in xslt.iterfind("xsl:param", namespaces=NSMAP):
        name = param.attrib.get('name')
        descr = param.attrib.get(descrattr)
        # Only print xsl:param's which has a doc description:
        if descr:
            print("{:>15}: {}".format(name, descr))

    parser.exit(0)


def check_arguments(parser, args):
    """Checks the parsed arguments for consistency

    :param parser: the argument parser
    :type parser: :class:`argparse.ArgumentParse`

    :param args: parsed arguments
    :type args: :class:`argparse.Namespace`

    :return: parsed arguments, possibly enriched with additional ``_productname`
             or ``_productnumber`` member variables
    :rtype: :class:`argparse.Namespace`
    """
    # We have to check for --help-xsl-param and a given INDEXFILE;
    # both can't be used at the same time:
    if args.help_xsl_params and args.indexfile:
        parser.error("Option--help-xsl-params and a INDEXFILE is mutually exclusive")

    if args.help_xsl_params:
        print_all_xsl_params(parser)

    if args.productname:
        # We save productname in _productname because as soon as etree.XSLT.strparam
        # is called, the original value cannot be retrieved anymore
        args._productname = args.productname
        args.params.append(('productname', args.productname))

    if args.productnumber:
        args._productnumber = args.productnumber
        args.params.append(('productnumber', args.productnumber))

    return args


def parsecli(cliargs=None):
    """Parse CLI with :class:`argparse.ArgumentParser` and return parsed result

    :param list cliargs: Arguments to parse or None (=use sys.argv)
    :return: parsed CLI result
    :rtype: :class:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(description=__doc__,
                                     epilog="Version %s written by %s " % (__version__, __author__)
                                     )

    parser.add_argument('--help-xsl-params',
                        help="Output all available parameters and their description",
                        action='store_true',
                        default=False,
                        )
    parser.add_argument('-v', '--verbose',
                        action='count',
                        default=0,
                        help="increase verbosity level")

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + __version__
                        )
    parser.add_argument('-o', '--output',
                        dest='output',
                        help='save DocBook XML file to the given path',
                        )
    parser.add_argument('-k', '--keep-all-ids',
                        dest='keepallids',
                        action='store_false',
                        default=True,
                        help='by default, IDs in bigfile are removed '
                             'if they are not referenced. '
                             'This option keeps all IDs. (default %(default)s)',
                        )
    parser.add_argument('-N', '--productname',
                        default='',
                        help='name of the product '
                             '(included into `book/bookinfo`)',
                        )
    parser.add_argument('-P', '--productnumber',
                        default='',
                        help='number/release etc. of the product '
                             '(included into `book/bookinfo`)',
                        )
    parser.add_argument('-4', '--db4',
                        action='store_true',
                        default=False,
                        help='Create DocBook 4 version (default %(default)s)',
                        )
    parser.add_argument('-c', '--conventions',
                        # default='',
                        help='path to filename which contains doc conventions '
                             'about the document (usually <preface> or '
                             '<chapter>); will replace the first chapter',
                        )
    parser.add_argument('-l', '--legalnotice',
                        help='path to filename which contains a <legalnotice> '
                             'element  (included into `book/bookinfo`)',
                        )
    parser.add_argument('-p', '--param',
                        dest='params',
                        action='append',
                        help='single XSLT parameter; use the syntax "NAME=VALUE" '
                             'Can be used multiple times. '
                             'Use --help-xsl-params to show all available parameters.',
                        )

    parser.add_argument('-ns', '--no-split',
                        dest='nsplit',
                        action='store_true',
                        default=False,
                        help='parameter which enables the splitting of the result XML file.',
                        )

    parser.add_argument('indexfile',
                        metavar="INDEXFILE",
                        # Currently, we have to mark INDEXFILE as optional here,
                        # because we can't use a mutually exclusive group with
                        # --help-xsl-param. :-(
                        nargs='?',
                        help='index file (XML) which refer all other files '
                             '(usually something like \'index.xml\')'
                        )

    args = parser.parse_args(args=cliargs)
    log.setLevel(LOGLEVELS.get(args.verbose, logging.NOTSET))
    args.params = prepareparams(args.params)
    log.info(args)

    if args.indexfile is None and not args.help_xsl_params:
        parser.print_help()
        sys.exit(10)

    return check_arguments(parser, args)


def main(cliargs=None):
    """Entry point for the application script

    :param list cliargs: Arguments to parse or None (=use :class:`sys.argv`)
    :return: True or False
    :rtype: bool
    """
    try:
        args = parsecli(cliargs)
        return process(args)

    except (etree.XMLSyntaxError) as error:
        log.fatal("%s in file %r", error, args.indexfile)  # exc_info=error, stack_info=True
        return ERROR_CODES.get(repr(type(error)), 255)

    except (FileNotFoundError, OSError) as error:
        log.fatal(error)
        return ERROR_CODES.get(repr(type(error)), 255)
