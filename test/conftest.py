#

import pytest
from argparse import Namespace


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
    return Namespace(keepallids=True,
                     legalnotice=None,
                     productname=name,
                     _productname=name,
                     productnumber=number,
                     _productnumber=number,
                     output=None,
                     db4=False,
                     conventions=None,
                     verbose=0,
                     params=[],
                     indexfile=None
                     )
