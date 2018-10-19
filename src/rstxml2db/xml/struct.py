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
from ..core import NSMAP


def addchapter(xml, convfile):
    """Replace first chapter with content of conventions file

    :param xml: :class:`lxml.etree._ElementTree`
    :param convfile: filename to some conventions, usually as root element
                        ``<preface>`` or ``<chapter>``
    """
    conv = etree.parse(convfile)
    book = xml.getroot()
    try:
        pos = [i for i in range(len(book))
               if etree.QName(book[i].tag).localname == 'chapter'][0]
    except (KeyError, IndexError):
        pos = 1

    firstchapter = book.find('d:chapter[1]', namespaces=NSMAP)
    if firstchapter is not None:
        book.remove(firstchapter)
    book.insert(pos, conv.getroot())


def addlegalnotice(xml, legalfile):
    """Add legalnotice file into book/bookinfo

    :param xml: :class:`lxml.etree._ElementTree`
    :param legalfile: filename with root element ``<legalnotice>``
    """
    legal = etree.parse(legalfile).getroot()
    bookinfo = xml.getroot().find('d:info', namespaces=NSMAP)
    bookinfo.append(legal)
