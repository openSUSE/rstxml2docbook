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

__all__ = ('__version__', 'main', 'parsecli')
__version__ = "0.2.0"
__author__ = "Thomas Schraitle <toms (AT) suse DOT de>"


from .cli import parsecli
from .log import log
from .xml import process
from lxml import etree
import sys


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
