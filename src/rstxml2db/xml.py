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


from lxml import etree

from .cleanup import cleanupxml, remove_double_ids
from .core import XSLTRST2DB, XSLTRESOLVE, DOCTYPE
from .log import log


def process(args):
    """Process arguments from CLI parser

    :param args: result from `argparse` parser
    :return: True or False
    :rtype: bool
    """
    doc = etree.parse(args.indexfile)
    # Create tree structure of both stylesheets
    rstresolve_xslt = etree.parse(XSLTRESOLVE)
    rst2db_xslt = etree.parse(XSLTRST2DB)

    # Create XSLT object of both tree structures
    resolve_trans = etree.XSLT(rstresolve_xslt)
    rst2db_trans = etree.XSLT(rst2db_xslt)

    # Transform
    rst = resolve_trans(doc)
    xml = rst2db_trans(rst, **dict(args.params))

    # Cleanup
    remove_double_ids(xml)
    cleanupxml(xml)

    if args.output is not None:
        with open(args.output, 'w') as f:
            log.info("Writing results to %r...", args.output)
            f.write(etree.tostring(xml,
                                   encoding='unicode',
                                   pretty_print=True,
                                   doctype=DOCTYPE.format(xml.getroot().tag),
                                   )
                    )
    else:
        print(str(xml))
    return 0
