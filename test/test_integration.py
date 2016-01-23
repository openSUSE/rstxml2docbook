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


def test_integration(tmpdir, args):
    DOCDIR.copy(tmpdir)
    bigfile = tmpdir / 'bigfile.xml'
    outdir = tmpdir / 'out'
    indexfile = tmpdir / 'index.xml'

    # Use the faked parsed cli argparser object
    args.bigfile = str(bigfile)
    args.indexfile = str(indexfile)

    process(args)

    assert (tmpdir / BOOKTREE).exists()
    assert bigfile.exists()

    xml = etree.parse(str(bigfile))
    productname = xml.xpath('/book/bookinfo/productname')
    assert productname
    assert productname[0].text == args._productname
    productnumber = xml.xpath('/book/bookinfo/productnumber')
    assert productnumber
    assert productnumber[0].text == args._productnumber
    assert len(xml.xpath('/book/chapter')) == 2


def test_filenotfound(args):
    #
    args.bigfile = 'big.xml'
    args.indexfile = 'file-does-not-exist.xml'

    with pytest.raises((FileNotFoundError, OSError)):
        process(args)
