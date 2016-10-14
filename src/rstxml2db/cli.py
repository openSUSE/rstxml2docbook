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
This module implements the cli parser.
"""

import argparse

from .log import log, setloglevel
from .version import __version__, __author__


def prepareparams(params):
    """Convert the list with "NAME=VALUE" entries into
       a tuple with ('NAME', 'VALUE')

       :param params: a list with "NAME=VALUE" entries
       :return: a tuple with ('NAME', 'VALUE') entries
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
                             'Can be used multiple times',
                        )

    parser.add_argument('indexfile',
                        metavar="INDEXFILE",
                        help='index file (XML) which refer all other files '
                             '(usually something like \'index.xml\')'
                        )

    args = parser.parse_args(args=cliargs)
    setloglevel(args.verbose)

    args.params = prepareparams(args.params)

    if args.productname:
        # We save productname in _productname because as soon as etree.XSLT.strparam
        # is called, the original value cannot be retrieved anymore
        args._productname = args.productname
        args.params.append(('productname', args.productname))

    if args.productnumber:
        args._productnumber = args.productnumber
        args.params.append(('productnumber', args.productnumber))

    log.info(args)
    return args
