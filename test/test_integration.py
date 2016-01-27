#

from rstxml2db.xml import process

from lxml import etree
from py.path import local
import pytest
import os

HERE = local(local(__file__).dirname)
DOCDIR= HERE / 'doc.001'


def test_integration(tmpdir, args):
    DOCDIR.copy(tmpdir)
    result = tmpdir / 'result.xml'
    indexfile = tmpdir / 'index.xml'

    # Use the faked parsed cli argparser object
    args.output = str(result)
    args.indexfile = str(indexfile)

    process(args)

    assert result.exists()
    xml = etree.parse(str(result))
    # productname = xml.xpath('/book/bookinfo/productname')
    # assert productname
    # assert productname[0].text == args._productname
    # productnumber = xml.xpath('/book/bookinfo/productnumber')
    # assert productnumber
    # assert productnumber[0].text == args._productnumber
    assert len(xml.xpath('/book/chapter')) == 2
    assert xml.xpath('/book/@lang')


def test_filenotfound(args):
    #
    args.output = 'result.xml'
    args.indexfile = 'file-does-not-exist.xml'

    with pytest.raises((FileNotFoundError, OSError)):
        process(args)
