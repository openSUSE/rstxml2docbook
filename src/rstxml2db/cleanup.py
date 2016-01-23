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

from .log import log


def finddoubleids(allids):
    """Find all double IDs

    :param allids: list with :class:`etree.Element`
    """
    d = dict()
    for i in allids:
        idattr = i.attrib['id']
        try:
            d[idattr] += d.setdefault(idattr, 1)
        except KeyError:
            d[idattr] = 1
    double = list() # [(i,k) for i,k in d.items() if k>1]
    for i, k in d.items():
        if k>1:
            double.append((i,k))

    return double


def allelementswithid(xml):
    """Generator: yielding all elements with an 'id' attribute

    :param xml: root tree or element
    """
    tree = xml.getroottree()  if hasattr(xml, 'getroottree') else xml

    for item in tree.iter():
        if item.attrib.get('id'):
            yield item


def cleanupxml(xml, usedoubleids=True):
    """Cleanup step to remove all IDs with no corresponding xref

    :param xml: :class:`lxml.etree._ElementTree`
    :param finddoubleids: boolean to execute additional check to find
           double ids or not (default True)
    """

    linkends = set([i.attrib['linkend'] for i in xml.iter('xref')])

    for item in allelementswithid(xml): #.xpath("//*[@id]"):
        idattr = item.attrib['id']
        if idattr not in linkends:
            log.info("Removing unused %r attribute", idattr)
            del item.attrib['id']

    if usedoubleids:
        double = finddoubleids(xml.xpath("//*[@id]"))
        log.warning("Double ids found: %s", double)