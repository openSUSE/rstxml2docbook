#

import pytest
import py.path
from argparse import Namespace
from lxml import etree


# ------------------------------------------------------
# Fixtures
#

@pytest.fixture
def args():
    """Fixture: simulates result from CLI parsing from
       argparser
    """
    return Namespace(keepallids = True,
                     legalnotice = etree.XSLT.strparam(''),
                     productname = etree.XSLT.strparam('FooObfuscator'),
                     _productname = 'FooObfuscator',
                     productnumber = etree.XSLT.strparam('1.0.1'),
                     _productnumber = '1.0.1',
                     output = None,
                     verbose = 0,
                     params = [],
                     indexfile = None
                     )
