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
Core variables, used in other modules.
"""

import os
from logging import (BASIC_FORMAT,
                     CRITICAL,
                     DEBUG,
                     FATAL,
                     ERROR,
                     INFO,
                     NOTSET,
                     WARN,
                     WARNING,
                     )


HERE = os.path.dirname(os.path.abspath(__file__))

#: Stylesheet to transform RST XML tree into DocBook 5
XSLTRST2DB = os.path.join(HERE, 'rstxml2db.xsl')

#: Stylesheet to resolves RST XML :file:``index.xml``
#: file into one, single RST XML file
XSLTRESOLVE = os.path.join(HERE, 'resolve.xsl')

#: Stylesheet to split up the XML file
XSLTSPLIT = os.path.join(HERE, 'split_xml.xsl')

#: Stylesheet to move block elements out of <paragraph>
XSLTMOVEBLOCKS = os.path.join(HERE, 'move-blocks-outof-para.xsl')

#: Stylesheet to move outplaced inlines into paragraph
XSLTINLINES = os.path.join(HERE, 'move-inlines-into-para.xsl')

#: Namespace mappings
NSMAP = dict(xi='http://www.w3.org/2001/XInclude',
             d='http://docbook.org/ns/docbook',
             xl='http://www.w3.org/1999/xlink',
             xsl='http://www.w3.org/1999/XSL/Transform',
             # Namespace inside XSLT, used to describe xsl:param's:
             doc='urn:x-suse:xslt-doc',
             )

#: DOCTYPE declaration with placeholders
DOCTYPE = r"""<!DOCTYPE {}
[
<!--
  <!ENTITY % entities SYSTEM "entity-decl.ent">
  %entities;
-->
]>"""

#: Map verbosity to log levels
LOGLEVELS = {None: WARNING,  # 0
             0: WARNING,
             1: INFO,
             2: DEBUG,
             }

#: Map log numbers to log names
LOGNAMES = {NOTSET: 'NOTSET',      # 0
            None:  'NOTSET',
            DEBUG:  'DEBUG',       # 10
            INFO:   'INFO',        # 20
            WARN:    'WARNING',    # 30
            WARNING: 'WARNING',    # 30
            ERROR:  'ERROR',       # 40
            CRITICAL: 'CRITICAL',  # 50
            FATAL: 'CRITICAL',     # 50
            }

#: log config files to search for
LOGFILECONFIGS = (os.path.join(os.path.dirname(__file__),
                               'logging.conf'),
                  os.path.expanduser("~/.config/rstxml2db/logging.conf"),
                  )

#: logging format for debugging purposes
DEBUG_FORMAT = "[%(levelname)s] %(name)s:%(lineno)s %(message)s"

#: fallback logging configuration
LOG_CONFIG = {
        'version': 1,
        'formatters': {'rstxml2db': {'format': DEBUG_FORMAT,
                                     'datefmt': '%Y%m%dT%H:%M:%S'},
                       'default': {'format': BASIC_FORMAT,
                                   'datefmt': '%Y-%m-%d %H:%M:%S'},
                       },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'NOTSET',
                'formatter': 'default',
            },
            'rstxml2db': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'rstxml2db',
            },
        },
        'loggers': {
            'rstxml2db': {
                'handlers': ['rstxml2db'],
                'propagate': False,
            }
        },
        'root': {
            'level': 'DEBUG',
            # Default %(levelname)s:%(name)s:%(message)s
            # 'handlers': ['console'],
        },
    }
