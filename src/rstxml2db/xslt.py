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

__all__ = ('transform', )

def transform(xsltfile, xmlfile, indexfile, **params):
    """Transforms one RSTXML file into DocBook

    :param xsltfile: XSLT stylesheet
    :param xmlfile: the RSTXML file to transform
    :param indexfile: the indexfile name
    :param params: parameters for XSLT
    """
    xsltroot = etree.parse(xsltfile)
    trans = etree.XSLT(xsltroot)
    xmlroot = etree.parse(xmlfile)
    t = trans(xmlroot)
    return t, trans.error_log
