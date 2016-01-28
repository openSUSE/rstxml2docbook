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
from .core import DOCTYPE, XSLTRST2DB, XSLTRESOLVE, XSLTDB4TO5
from .log import log


def addchapter(xml, convfile):
    """Replace first chapter with content of conventions file

    :param xml: :class:`lxml.etree._ElementTree`
    :param convfile: filename to some conventions, usually as root element
                        `<preface>` or `<chapter>`
    """
    conv = etree.parse(convfile)
    preface = conv.getroot()
    book = xml.getroot()
    try:
        pos = [i for i in range(len(book)) if etree.QName(book[i].tag).localname == 'chapter'][0]
    except KeyError:
        pos = 0

    firstchapter = book.find('chapter[1]')
    if firstchapter is not None:
        book.remove(firstchapter)
    book.insert(pos, conv.getroot())


def addlegalnotice(xml, legalfile):
    """Add legalnotice file into book/bookinfo

    :param xml: :class:`lxml.etree._ElementTree`
    :param convfile: filename with root element `<legalnotice>`
    """
    legal = etree.parse(legalfile).getroot()
    bookinfo = xml.getroot().find('bookinfo')
    bookinfo.append(legal)


def quoteparams(args):
    """Quote parameters with :func:`etree.XSLT.strparam`

    :param args: result from `argparse` parser
    :return: parameter list with quoted values
    :rtype: list
    """
    return [(p[0], p[1] if p[0].startswith('_') else etree.XSLT.strparam(p[1]))
            for p in args.params]

def transform(doc, args):
    """
    """
    rstresolve_xslt = etree.parse(XSLTRESOLVE)
    rst2db_xslt = etree.parse(XSLTRST2DB)

    # Create XSLT object of both tree structures
    resolve_trans = etree.XSLT(rstresolve_xslt)
    rst2db_trans = etree.XSLT(rst2db_xslt)

    # Resolve RST XML -> single RST XML structure
    # then, transform RST XML -> DocBook
    rst = resolve_trans(doc)
    xml = rst2db_trans(rst, **dict(args.params))

    if args.legalnotice is not None:
        addlegalnotice(xml, args.legalnotice)
    if args.conventions is not None:
        addchapter(xml, args.conventions)

    # Cleanup
    cleanupxml(xml)

    if not args.db4:
        db4o5_xslt = etree.parse(XSLTDB4TO5)
        db4o5_trans = etree.XSLT(db4o5_xslt)
        xml = db4o5_trans(xml, **dict(args.params))

    return xml


def process(args):
    """Process arguments from CLI parser

    :param args: result from `argparse` parser
    :return: True or False
    :rtype: bool
    """
    args.params = quoteparams(args)
    doc = etree.parse(args.indexfile)
    #
    xml = transform(doc, args)

    xmldict = dict(encoding='unicode',
                   pretty_print=True,
                   )
    if args.db4:
        xmldict.update(doctype=DOCTYPE.format(xml.getroot().tag))
    outstring = etree.tostring(xml, **xmldict)

    if args.output is not None:
        with open(args.output, 'w') as f:
                log.info("Writing results to %r...", args.output)
                f.write(outstring)
    else:
        print(outstring)
    return 0
