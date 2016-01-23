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

"""Converts RST XML (Sphinx/ReST) into DocBook XML
"""


from .core import BOOKTREE
from .log import log
from .xml import process

import argparse
from lxml import etree
import sys

__all__ = ('__version__', 'main', 'parsecli')
__version__ = "0.0.3"
__author__ = "Thomas Schraitle <toms (AT) suse DOT de>"


def parsecli(cliargs=None):
    """Parse CLI and return ArgumentParser result

    :param list cliargs: Arguments to parse or None (=use sys.argv)
    :return: `argparse` result
    """
    parser = argparse.ArgumentParser(description=__doc__,
                                     epilog="Version %s written by %s " % (__version__, __author__)
                                     )

    parser.add_argument('-v', '--verbose', action='count',
                        help="increase verbosity level")

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + __version__
                        )
    parser.add_argument('-t', '--booktree',
                        default=BOOKTREE,
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
                        help='create a single DocBook XML file',
                        )
    parser.add_argument('-k', '--keep-all-ids',
                        dest='keepallids',
                        action='store_false',
                        default=True,
                        help='by default, IDs in bigfile are removed '
                             'if they are not referenced. '
                             'This option keeps all IDs. (default %(default)s)',
                        )
    parser.add_argument('-n', '--productname',
                        default='',
                        help='name of the product '
                             '(included into `book/bookinfo`)',
                        )
    parser.add_argument('-p', '--productnumber',
                        default='',
                        help='number/release etc. of the product '
                             '(included into `book/bookinfo`)',
                        )
    parser.add_argument('-l', '--legalnotice',
                        default='',
                        help='path to filename which contains a <legalnotice> '
                             'element  (included into `book/bookinfo`)',
                        )

    parser.add_argument('indexfile',
                        help='index file (XML) which refer all other files '
                             '(usually something like \'index.xml\')'
                        )

    args = parser.parse_args(args=cliargs)
    args.productname = etree.XSLT.strparam(args.productname)
    args.productnumber = etree.XSLT.strparam(args.productnumber)
    args.legalnotice = etree.XSLT.strparam(args.legalnotice)

#    if not os.path.exists(args.indexfile):
#        raise FileNotFoundError('Cannot find file %r' % args.indexfile)

    log.info(args)
    return args


def main(cliargs=None):
    """Entry point for the application script

    :param list cliargs: Arguments to parse or None (=use sys.argv)
    :return: True or False
    """
    try:
        args = parsecli(cliargs)
        return process(args)
    except etree.XSLTApplyError as err:
        log.error(err)
        sys.exit(10)
    except (FileNotFoundError, OSError) as err:
        log.error(err)
        sys.exit(20)
