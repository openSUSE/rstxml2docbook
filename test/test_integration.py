#

from rstxml2db.xml import process
from rstxml2db.core import NSMAP

from lxml import etree
from py.path import local
import pytest
import os

HERE = local(local(__file__).dirname)
DOCDIR= HERE / 'doc.001'

def assert_xpaths(xml, xpath, args):
    productname = xml.xpath(xpath[0], namespaces=NSMAP)
    assert productname
    assert productname[0].text == args._productname
    productnumber = xml.xpath(xpath[1], namespaces=NSMAP)
    assert productnumber
    assert productnumber[0].text == args._productnumber
    assert len(xml.xpath(xpath[2], namespaces=NSMAP)) == 2
    assert xml.xpath(xpath[3], namespaces=NSMAP)


@pytest.mark.parametrize('xpath,db4', [
    (['/book/bookinfo/productname',
      '/book/bookinfo/productnumber',
      '/book/chapter',
      '/book/@lang',
     ],
     True
    ),
    # For DocBook 5
    (
    ['/d:book/d:info/d:productname',
     '/d:book/d:info/d:productnumber',
     '/d:book/d:chapter',
     '/d:book/@xml:lang',
     ],
    False
    ),
])
def test_integration(xpath, db4, tmpdir, args):
    DOCDIR.copy(tmpdir)
    result = tmpdir / 'result.xml'
    indexfile = tmpdir / 'index.xml'

    # Use the faked parsed cli argparser object
    args.output = str(result)
    args.indexfile = str(indexfile)
    args.db4 = db4

    process(args)

    assert result.exists()
    xml = etree.parse(str(result))
    assert_xpaths(xml, xpath, args)

@pytest.mark.parametrize('xpath,db4', [
    (['/book/preface/title',
      '/book/preface/para',
      ['title', 'bookinfo', 'preface', 'chapter']
     ],
     True),
    # For DocBook 5
    (['/d:book/d:preface/d:title',
      '/d:book/d:preface/d:para',
      ['title', 'info', 'preface', 'chapter']
     ],
     False),
])
def test_integration_with_conventions(xpath, db4, tmpdir, args):
    DOCDIR.copy(tmpdir)
    result = tmpdir / 'result.xml'
    indexfile = tmpdir / 'index.xml'
    conventions = tmpdir / 'preface.xml'

    # Use the faked parsed cli argparser object
    args.output = str(result)
    args.indexfile = str(indexfile)
    args.conventions = str(conventions)
    args.db4 = db4

    process(args)

    assert result.exists()
    xml = etree.parse(str(result))
    preface_title = xml.xpath(xpath[0], namespaces=NSMAP)
    assert preface_title
    preface_para = xml.xpath(xpath[1], namespaces=NSMAP)
    assert preface_para
    book = xml.getroot()
    assert [etree.QName(i.tag).localname for i in book.iterchildren()] == xpath[2]


@pytest.mark.parametrize('xpath,db4', [
    (['/book/bookinfo/productname',
      '/book/bookinfo/productnumber',
      '/book/chapter',
      '/book/@lang',
     ],
     True
    ),
    # For DocBook 5
    (
    ['/d:book/d:info/d:productname',
     '/d:book/d:info/d:productnumber',
     '/d:book/d:chapter',
     '/d:book/@xml:lang',
     ],
    False
    ),
])
def test_integration_with_stdout(xpath, db4, tmpdir, capsys, args):
    DOCDIR.copy(tmpdir)
    result = str(tmpdir / 'result.xml')
    indexfile = tmpdir / 'index.xml'

    args.output = None
    args.db4 = db4
    args.indexfile = str(indexfile)
    process(args)
    out, err = capsys.readouterr()
    assert out
    assert not err
    #with open(result, 'w') as fh:
    #    fh.write(out)
    xml = etree.fromstring(out)
    assert_xpaths(xml, xpath, args)


def test_filenotfound(args):
    #
    args.output = 'result.xml'
    args.indexfile = 'file-does-not-exist.xml'

    with pytest.raises((FileNotFoundError, OSError)):
        process(args)
