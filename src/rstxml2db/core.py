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

__all__ = ('DOCTYPE', 'HERE', 'NSMAP',
           'XSLTRST2DB', 'XSLTRESOLVE', 'XSLTDB4TO5')

import os

HERE = os.path.dirname(os.path.abspath(__file__))

# Stylesheets
XSLTRST2DB = os.path.join(HERE, 'rstxml2db.xsl')
XSLTRESOLVE = os.path.join(HERE, 'resolve.xsl')
XSLTDB4TO5 = os.path.join(HERE, 'suse-upgrade.xsl')

NSMAP = dict(xi='http://www.w3.org/2001/XInclude',
             d='http://docbook.org/ns/docbook',
             xl='http://www.w3.org/1999/xlink',
             )

DOCTYPE = r"""<!DOCTYPE {} PUBLIC
"-//OASIS//DTD DocBook XML V4.5//EN"
"http://docbook.org/xml/4.5/docbookx.dtd"
[
<!--
  <!ENTITY % entities SYSTEM "entity-decl.ent">
  %entities;
-->
]>"""
