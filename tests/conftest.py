#
import pytest
from argparse import Namespace
import py

from rstxml2db.core import RESULT_TREE_DIR

DATADIR = py.path.local(__file__).parts()[-2] / "data"

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
                     nsplit=True,
                     conventions=None,
                     verbose=0,
                     params=[],
                     indexfile=None,
                     result_tree=False,
                     result_tree_dir=RESULT_TREE_DIR,
                     )


def pytest_generate_tests(metafunc):
    """Replace the xmltestcases fixture by all *.xml files in test/data"""
    if 'xmltestcase' in metafunc.fixturenames:
        testcases = DATADIR.listdir('*.xml')
        ids = [f.purebasename for f in testcases]
        metafunc.parametrize("xmltestcase", testcases, ids=ids)
