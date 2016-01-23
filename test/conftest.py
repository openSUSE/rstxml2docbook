#

import pytest
import py.path
from argparse import Namespace
from lxml import etree

from rstxml2db.core import BOOKTREE, OUTDIR


# ------------------------------------------------------
# Fixtures
#

@pytest.fixture
def args():
    """Fixture: simulates result from CLI parsing from
       argparser
    """
    return Namespace(booktree = BOOKTREE,
                     keepallids = True,
                     legalnotice = etree.XSLT.strparam(''),
                     productname = etree.XSLT.strparam('FooObfuscator'),
                     _productname = 'FooObfuscator',
                     productnumber = etree.XSLT.strparam('1.0.1'),
                     _productnumber = '1.0.1',
                     outputdir = str(OUTDIR),
                     verbose = 0,
                     params = [],
                     #
                     # Will be filled from the special test case:
                     bigfile = None,
                     indexfile = None
                     )
