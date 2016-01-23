#

from rstxml2db.core import BOOKTREE
from rstxml2db.xml import process
from argparse import Namespace

from lxml import etree
from py.path import local
import pytest
import os

HERE = local(local(__file__).dirname)
DOCDIR= HERE / 'doc.001'


def test_integration(tmpdir):
    DOCDIR.copy(tmpdir)
    bigfile = tmpdir / 'bigfile.xml'
    outdir = tmpdir / 'out'
    indexfile = tmpdir / 'index.xml'

    # Construct a fake parsed cli argparser object
    args = Namespace(booktree = BOOKTREE,
                     bigfile = str(bigfile),
                     keepallids = True,
                     legalnotice = etree.XSLT.strparam(''),
                     productname = etree.XSLT.strparam('FooObfuscator'),
                     productnumber = etree.XSLT.strparam('1.0.1'),
                     outputdir = str(outdir),
                     verbose = 0,
                     params = None,
                     #
                     indexfile = str(indexfile)
                     )

    process(args)

    assert (tmpdir / BOOKTREE).exists()
    assert bigfile.exists()

    xml = etree.parse(str(bigfile))
    productname = xml.xpath('/book/bookinfo/productname')
    assert productname
    assert productname[0].text == 'FooObfuscator'
    productnumber = xml.xpath('/book/bookinfo/productnumber')
    assert productnumber
    assert productnumber[0].text == '1.0.1'
    assert len(xml.xpath('/book/chapter')) == 2


def test_filenotfound():
    # Construct a fake parsed cli argparser object
    args = Namespace(booktree = BOOKTREE,
                     bigfile = str('big.xml'),
                     keepallids = True,
                     legalnotice = etree.XSLT.strparam(''),
                     productname = etree.XSLT.strparam('FooObfuscator'),
                     productnumber = etree.XSLT.strparam('1.0.1'),
                     outputdir = str('out'),
                     verbose = 0,
                     params = None,
                     #
                     indexfile = str('file-does-not-exist.xml')
                     )

    with pytest.raises((FileNotFoundError, OSError)):
        process(args)
