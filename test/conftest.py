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
    name = 'FooObfuscator'
    number = '1.0.1'
    legal = None
    conv = None
    params = [('productname',   name),
              ('productnumber', number),
              # ('legalnotice',   legal),
              # ('conventions',   conv),
              ]

    return Namespace(keepallids = True,
                     legalnotice = legal,
                     # _legalnotice = legal,
                     productname = etree.XSLT.strparam(name),
                     _productname = name,
                     productnumber = etree.XSLT.strparam(number),
                     _productnumber = number,
                     output = None,
                     conventions = conv,
                     # _conventions = conv,
                     verbose = 0,
                     params = [], # [(p[0], etree.XSLT.strparam(p[1])) for p in params],
                     indexfile = None
                     )
