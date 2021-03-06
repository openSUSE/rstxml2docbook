#

from rstxml2db.xml.process import process
from rstxml2db.core import NSMAP, XSLTSPLIT

from lxml import etree
from py.path import local
import pytest

HERE = local(local(__file__).dirname)


def assert_xpaths(xml, xpath, args):
    productname = xml.xpath(xpath[0], namespaces=NSMAP)
    assert productname
    assert productname[0].text == args._productname
    productnumber = xml.xpath(xpath[1], namespaces=NSMAP)
    assert productnumber
    assert productnumber[0].text == args._productnumber
    assert len(xml.xpath(xpath[2], namespaces=NSMAP)) == 2
    assert xml.xpath(xpath[3], namespaces=NSMAP)


@pytest.mark.parametrize('xpath', [
    # For DocBook 5
    ['/d:book/d:info/d:productname',
      '/d:book/d:info/d:productnumber',
      '/d:book/d:chapter',
      '/d:book/@xml:lang']
])
def test_integration(xpath, tmpdir, args):
    DOCDIR = HERE / 'data/doc.001'
    DOCDIR.copy(tmpdir)
    result = tmpdir / 'result.xml'
    indexfile = tmpdir / 'index.xml'

    # Use the faked parsed cli argparser object
    args.output = str(result)
    args.indexfile = str(indexfile)
    args.params.append(('productname',   args.productname))
    args.params.append(('productnumber', args.productnumber))
    args.nsplit = True

    process(args)

    assert result.exists()
    xml = etree.parse(str(result))
    assert_xpaths(xml, xpath, args)


@pytest.mark.parametrize('xpath', [
    # For DocBook 5
    ['//d:figure[1]',  # '/d:book/d:chapter[2]/d:section[1]/d:figure[1]'
     'd:title']
])
def test_integration_figure(xpath, tmpdir, args):
    DOCDIR = HERE / 'data/doc.001'
    DOCDIR.copy(tmpdir)
    result = tmpdir / 'result.xml'
    indexfile = tmpdir / 'index.xml'

    # Use the faked parsed cli argparser object
    args.output = str(result)
    args.indexfile = str(indexfile)
    args.nsplit = True

    process(args)

    assert result.exists()
    xml = etree.parse(str(result))

    figure = xml.find(xpath[0], namespaces=NSMAP)
    assert figure is not None
    title = figure.find(xpath[1], namespaces=NSMAP)
    assert title is not None
    assert title.text == 'Foo Image'


@pytest.mark.parametrize('xpath', [
    # For DocBook 5
    ['/d:book/d:preface/d:title',
     '/d:book/d:preface/d:para',
     ['title', 'info', 'preface', 'chapter', 'glossary']
    ]
])
def test_integration_with_conventions(xpath, tmpdir, args):
    DOCDIR = HERE / 'data/doc.001'
    DOCDIR.copy(tmpdir)
    result = tmpdir / 'result.xml'
    indexfile = tmpdir / 'index.xml'
    conventions = tmpdir / 'preface.xml'

    # Use the faked parsed cli argparser object
    args.output = str(result)
    args.indexfile = str(indexfile)
    args.conventions = str(conventions)
    args.params.append(('productname',   args.productname))
    args.params.append(('productnumber', args.productnumber))
    args.nsplit = True

    process(args)

    assert result.exists()
    xml = etree.parse(str(result))
    preface_title = xml.xpath(xpath[0], namespaces=NSMAP)
    assert preface_title
    preface_para = xml.xpath(xpath[1], namespaces=NSMAP)
    assert preface_para
    book = xml.getroot()
    assert [etree.QName(i.tag).localname for i in book.iterchildren()] == xpath[2]


@pytest.mark.parametrize('xpath', [
    # For DocBook 5
    ['/d:book/d:info/d:productname',
      '/d:book/d:info/d:productnumber',
      '/d:book/d:chapter',
      '/d:book/@xml:lang'
    ]
])
def test_integration_with_stdout(xpath, tmpdir, capsys, args):
    DOCDIR = HERE / 'data/doc.001'
    DOCDIR.copy(tmpdir)
    # result = str(tmpdir / 'result.xml')
    indexfile = tmpdir / 'index.xml'

    args.output = None
    args.indexfile = str(indexfile)
    args.params.append(('productname',   args.productname))
    args.params.append(('productnumber', args.productnumber))
    args.nsplit = True
    process(args)
    out, err = capsys.readouterr()
    assert out
    assert not err
    # with open(result, 'w') as fh:
    #    fh.write(out)
    xml = etree.fromstring(out)
    assert_xpaths(xml, xpath, args)


@pytest.mark.parametrize('xpath', [
    # For DocBook 5
    ['/d:book/d:info/d:legalnotice',
      '/d:book/d:info/d:legalnotice/d:title',
    ]
])
def test_integration_with_legalnotice(xpath, tmpdir, args):
    DOCDIR = HERE / 'data/doc.001'
    DOCDIR.copy(tmpdir)
    result = tmpdir / 'result.xml'
    indexfile = tmpdir / 'index.xml'
    legalfile = tmpdir / 'legal.xml'

    # Use the faked parsed cli argparser object
    args.output = str(result)
    args.indexfile = str(indexfile)
    args.legalnotice = str(legalfile)
    args.nsplit = True
    process(args)
    assert result.exists()
    xml = etree.parse(str(result))
    legalnotice = xml.xpath(xpath[0], namespaces=NSMAP)
    assert legalnotice
    title = xml.xpath(xpath[1], namespaces=NSMAP)
    assert title
    assert title[0].text == 'Legal Notice'


def test_integration_with_productname(tmpdir, args):
    DOCDIR = HERE / 'data/doc.001'
    DOCDIR.copy(tmpdir)
    result = tmpdir / 'result.xml'
    indexfile = tmpdir / 'index.xml'

    # Use the faked parsed cli argparser object
    args.output = str(result)
    args.indexfile = str(indexfile)
    args.params.append(('productname',   args.productname))
    args.nsplit = True
    process(args)
    assert result.exists()
    xml = etree.parse(str(result))
    assert xml.xpath('/d:book', namespaces=NSMAP)


def test_wrong_xml(tmpdir):
    from rstxml2db.cli import main
    badxml = str(tmpdir / 'bad.xml')
    with open(badxml, 'w') as fh:
        fh.write("<bad_tag>")

    result = main(['-o', 'result.xml', badxml])
    assert result != 0


def test_single_output_file(tmpdir, args):
   #set the tmpdir and the indexfile
   DOCDIR = HERE / 'data/doc.002'
   DOCDIR.copy(tmpdir)
   indexfile = tmpdir / 'index.xml'
   #arguments...
   args.output = str(tmpdir / "out/foo.xml" )
   args.indexfile = str(indexfile)
   args.nsplit = True
   process(args)

   assert local(args.output).exists()
   tree = etree.parse(args.output)
   assert tree.xpath('/d:book', namespaces=NSMAP)


def test_multiple_output_files(tmpdir, args):
   #set the tmpdir and the indexfile
   DOCDIR = HERE / 'data/doc.002'
   DOCDIR.copy(tmpdir)
   indexfile = tmpdir / 'index.xml'
   outdir = tmpdir / "out"
   #arguments...
   args.indexfile = str(indexfile)
   args.output = str(tmpdir / "out/foo.xml" )
   args.nsplit = False
   process(args)

   assert outdir.exists()
   assert len(outdir.listdir()) == 2


def test_multiple_output_files_with_root_ns(tmpdir):
    #set the tmpdir and the indexfile
    DOCDIR = HERE / 'data/doc.003'
    DOCDIR.copy(tmpdir)
    outdir = tmpdir.mkdir("out")

    # params = dict()
    params = {'basedir':  etree.XSLT.strparam(outdir.strpath+"/")}
    xml = etree.parse(str(tmpdir / "docbook.xml"))
    trans = etree.XSLT(etree.parse(XSLTSPLIT))
    trans(xml, **params)

    assert outdir.exists()
    assert len(outdir.listdir()) == 3

    # We need to test, if root element have more than one namespace:
    for xmlfile in outdir.listdir():
        xml = etree.parse(xmlfile.strpath)
        nsmap = (xml.getroot()).nsmap
        assert xml.getroot().attrib.get('version')
        assert len(nsmap) > 1
        assert set(nsmap.values()) == set(['http://docbook.org/ns/docbook',
                                           'http://www.w3.org/1999/xlink',
                                           'http://www.w3.org/2001/XInclude'])

