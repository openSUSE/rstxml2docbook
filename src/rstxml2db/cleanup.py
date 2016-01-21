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


def cleanupxml(xml):
    """Cleanup step to remove all unresolved IDs

    :param xml: :class:`lxml.etree._ElementTree`
    """
    allxrefs = xml.xpath('//xref')
    allids = xml.xpath('//*[@id]')

    linkends = set([i.attrib['linkend'] for i in allxrefs])
    # ids = set([i.attrib['id'] for i in allids])

    for item in allids:
        idattr = item.attrib['id']
        if idattr not in linkends:
            log.info("Removing unused %r attribute", idattr)
            del item.attrib['id']
