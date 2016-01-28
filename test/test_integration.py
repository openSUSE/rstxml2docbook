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
    assert xml.xpath('/book/bookinfo')
    assert len(xml.xpath('/book/chapter')) == 2
    assert xml.xpath('/book/@lang')
    assert not xml.xpath('/book/bookinfo/productname')
    assert not xml.xpath('/book/bookinfo/productnumber')


def test_integration_with_conventions(tmpdir, args):
    DOCDIR.copy(tmpdir)
    result = tmpdir / 'result.xml'
    indexfile = tmpdir / 'index.xml'
    conventions = tmpdir / 'preface.xml'

    # Use the faked parsed cli argparser object
    args.output = str(result)
    args.indexfile = str(indexfile)
    args.conventions = str(conventions)

    process(args)

    assert result.exists()
    xml = etree.parse(str(result))
    preface_title = xml.xpath('/book/preface/title')
    assert preface_title
    preface_para = xml.xpath('/book/preface/para')
    assert preface_para
    book = xml.getroot()
    assert [i.tag for i in book.iterchildren()] ==  ['title',
                                                     'bookinfo',
                                                     'preface',
                                                     'chapter']


def test_integration_with_legalnotice(tmpdir, args):
    DOCDIR.copy(tmpdir)
    result = tmpdir / 'result.xml'
    indexfile = tmpdir / 'index.xml'
    legalfile = tmpdir / 'legal.xml'

    # Use the faked parsed cli argparser object
    args.output = str(result)
    args.indexfile = str(indexfile)
    args.legalnotice = str(legalfile)

    process(args)
    assert result.exists()
    xml = etree.parse(str(result))
    legalnotice = xml.xpath('/book/bookinfo/legalnotice')
    assert legalnotice
    title = xml.xpath('/book/bookinfo/legalnotice/title')
    assert title
    assert title[0].text == 'Legal Notice'


def test_integration_with_productname(tmpdir, args):
    DOCDIR.copy(tmpdir)
    result = tmpdir / 'result.xml'
    indexfile = tmpdir / 'index.xml'

    # Use the faked parsed cli argparser object
    args.output = str(result)
    args.indexfile = str(indexfile)
    print(">>>args.params=", args.params)

    process(args)
    assert result.exists()
    xml = etree.parse(str(result))
    assert xml.xpath('/book')


def test_wrong_xml(tmpdir):
    from rstxml2db import main
    badxml = str(tmpdir / 'bad.xml')
    with open(badxml, 'w') as fh:
        fh.write("<bad_tag>")
    with pytest.raises(SystemExit):
        main(['-o', 'result.xml', badxml])