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

from .log import log

__all__ = ('transform', )


def transform(xslt, xmlfile, indexfile, **params):
    """Transforms one RSTXML file into DocBook

    :param xslt: XSLT node from `etree.XSLT`
    :param xmlfile: the RSTXML file to transform
    :param indexnode: all nodes of the indexfile name
    :param params: parameters for XSLT
    """
    log.info("transform: %s, %r, %r, %s", xslt, xmlfile, indexfile, params)
    xmlroot = etree.parse(xmlfile)
    t = xslt(xmlroot,
             indexfile=etree.XSLT.strparam(indexfile),
             **params)
    return t, xslt.error_log
