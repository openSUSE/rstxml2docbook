#
# Copyright (c) 2015 SUSE Linux GmbH
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

from lxml import etree
import io
import os
import sys


NSMAP = dict(xi='http://www.w3.org/2001/XInclude',
             d='http://docbook.org/ns/docbook',
             )
__all__=('NSMAP', 'buildcompounds', 'process_index')


def buildcompounds(xf, doc, source=None):
    """Build the output tree

    :param xf: context manager
    :param doc: element tree
    :param source: filename
    """
    try:
        log.debug(">>> buildcompounds: %s, %r", doc, source)
        try:
            dirname = os.path.dirname(source)
            # source = os.path.basename(source)
            log.debug("Using source %r and dirname %r", source, dirname)
        except AttributeError:
            # Fall back
            # dirname = os.path.dirname(doc.getroottree().docinfo.URL)
            dirname = ''

        with xf.element('section', id=doc.attrib.get('ids')):
            if doc.find('title') is not None:
                xf.write(doc.find('title'))

            for item in doc.iter('list_item'):
                if item.attrib.get('classes') == 'toctree-l1':
                    ref = item.xpath("*/reference[@internal='True']")[0]
                    if ref is not None:
                        href = "%s.xml" % ref.attrib.get('refuri')

                        with xf.element('ref', href=href):
                            d = os.path.join(dirname, href)
                            log.info("Trying to load %r", d)
                            xml = etree.parse(d)
                            document = xml.getroot()
                            iter_sections(xf, document, d)
                            xml = None
                            document = None

                        ref = None
    except Exception as err:
        #import pdb
        #pdb.post_mortem()
        log.warn(err)


def iter_sections(xf, doc, source=None):
    """Iterate over all sections

    :param xf: context manager
    :param doc: element tree
    :param source: filename
    """
    log.debug(">>> iter_sections: %s, %r", doc, source)
    for item in doc.iter('section'):
        buildcompounds(xf, item, source)


def process_index(indexfile, output=None, format=False):
    """Process the index file, converted from RST to XML

    :param indexfile:
    :param format: format output file?
    :return: None
    """
    def indent(output):
        os.rename(output, "%s.tmp" % output)
        xml = etree.parse("%s.tmp" % output)
        xml.write(output,
                  encoding="utf-8",
                  pretty_print=True,
                  )
        log.info("Writing to %r", output)
        os.remove("%s.tmp" % output)
        xml.docinfo.URL = output
        return xml

    log.info("Reading indexfile %r", indexfile)
    xml = etree.parse(indexfile)
    document = xml.getroot()

    with etree.xmlfile(output) as xf:
        with xf.element('root'):
            iter_sections(xf, document, indexfile)

    xml = indent(output)
    return xml

