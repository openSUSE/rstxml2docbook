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
Collect several cleanup steps

"""

import logging
from lxml import etree
from collections import defaultdict

log = logging.getLogger(__name__)


def finddoubleids(allids):
    """Find all double IDs

    :param allids: list with :class:`lxml.etree.Element`
    :type allids: list
    :return: all nodes which contains more than one IDs; èach entry
             represented as ``(node, number)``
    :rtype: list
    """
    d = defaultdict(int)
    for node in allids:
        idattr = node.attrib['id']
        d[idattr] += 1
    return [(node, v) for node, v in d.items() if v > 1]


def allelementswithid(xml):
    """Generator: yielding all elements with an 'id' attribute

    :param xml: root tree or element
    :yield: XML element with ``id``
    :rtype: Iterator[:class:`lxml.etree.Element`]
    """
    tree = xml.getroottree() if hasattr(xml, 'getroottree') else xml

    for item in tree.iter():
        if item.attrib.get('id'):
            yield item


def alltableelements(xml):
    """Generator: yield all table or informaltable elements

    :param xml: root tree or element node
    :yield: XML node, either ``table`` or ``informaltable``
    :rtype: Iterator[:class:`lxml.etree.Element`]
    """
    tree = xml.getroottree() if hasattr(xml, 'getroottree') else xml
    for item in tree.iter():
        if item.tag in ('table', 'informaltable'):
            yield item


def fix_colspec_width(xml):
    """Fix ``columspec/@width`` from simple absolute values into the relative
       star notation

    :param xml: root tree or element node
    :type xml: :class:`lxml.etree.Element`
    """
    for table in alltableelements(xml):
        colspecsum = table.xpath('tgroup/colspec/@colwidth')
        colspecsum = sum([int(x) for x in colspecsum])
        for colspec in table.xpath('tgroup/colspec'):
            colwidth = 100*int(colspec.attrib.get('colwidth'))
            colspec.attrib['colwidth'] = "{:.1f}*".format(colwidth/colspecsum)


def add_pi_in_screen(xml, limit=83, target='dbsuse-fo', fontsize='8pt'):
    """Add processing-instruction for long texts in screens

    .. note::
       This function modifies directly the XML tree

    :param xml: XML tree
    :type xml: :class:`lxml.etree._ElementTree`

    :param limit: maximum number of characters allowed
    :type limit: int

    :param target: name of processing instruction
    :type target: str

    :param fontsize: font size to use
    :type fontsize: str
    """
    tree = xml.getroottree() if hasattr(xml, 'getroottree') else xml
    for screen in tree.iter('screen'):
        if screen.text is not None:
            if any([len(i) > limit for i in screen.text.split("\n")]):
                pi = etree.ProcessingInstruction(target,
                                                'font-size="{}"'.format(fontsize))
                pi.tail = screen.text
                screen.text = ''
                screen.insert(0, pi)


def remove_double_ids(xml, usedoubleids=True):
    """Cleanup step to remove all IDs with no corresponding xref

    .. note::
       This function modifies directly the XML tree

    :param xml: XML tree
    :type xml: :class:`lxml.etree._ElementTree`

    :param usedoubleids: boolean to execute additional check to find
           double ids or not (default True)
    :type usedoubleids: bool
    """
    linkends = set([i.attrib['linkend'] for i in xml.iter('xref')])
    unusedattr = [item for item in allelementswithid(xml)
                  if item.attrib['id'] not in linkends]
    # idattrs = [item.attrib['id'] for item in unusedattr]
    for item in unusedattr:
        del item.attrib['id']
    # log.debug('Unused IDs, removed from output: %s', ', '.join(idattrs))

    if usedoubleids:
        double = finddoubleids(xml.xpath("//*[@id]"))
        if double:  # pragma: no cover
            log.warning("Double IDs found: %s", double)


def cleanupxml(xml):
    """Cleanup steps to execute

    .. note::
       This function modifies directly the XML tree

    :param xml: XML tree
    :type xml: :class:`lxml.etree._ElementTree`
    """
    remove_double_ids(xml)
    fix_colspec_width(xml)
    add_pi_in_screen(xml)
