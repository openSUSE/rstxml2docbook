#

from rstxml2db.cleanup import (cleanupxml,
                               finddoubleids,
                               allelementswithid,
                               fix_colspec_width,
                               )
from py.path import local
from lxml import etree


def test_cleanup():
    xmlstr = """<book id="book">
  <title>Test</title>
  <chapter id="chapter.without.xref">
    <title>Test Chapter without xref</title>
    <para>Nothing.</para>
  </chapter>
  <chapter id="chapter.with.xref">
    <title>Test Chapter with xref</title>
    <para>See <xref linkend="chapter.with.xref"/></para>
  </chapter>
</book>
    """
    xml = etree.fromstring(xmlstr)
    xml = xml.getroottree()
    assert len(xml.xpath("//*[@id]")) == 3
    cleanupxml(xml, False)
    assert len(xml.xpath("//*[@id]")) == 1
    assert xml.xpath("//*[@id='chapter.with.xref']")


def test_finddoubleids():
    xmlstr = """<book id="book">
  <title>Test</title>
  <chapter id="chapter">
    <title>Test Chapter 1</title>
    <para/>
  </chapter>
  <chapter id="chapter">
    <title>Test Chapter 2</title>
    <para/>
  </chapter>
</book>
    """
    from itertools import chain

    xml = etree.fromstring(xmlstr)
    xml = xml.getroottree()
    assert len(xml.xpath("//*[@id]")) == 3

    double = finddoubleids(chain(xml.xpath("/*[@id]"),
                                 xml.iterfind("*[@id]"))
                           )
    assert double == [('chapter', 2)]


def test_allelementswithid():
    xmlstr = """<book id="book">
  <title>Test</title>
  <chapter id="chapter">
    <title>Test Chapter 1</title>
    <para/>
  </chapter>
  <chapter id="chapter">
    <title>Test Chapter 2</title>
    <para/>
  </chapter>
</book>
    """
    xml = etree.fromstring(xmlstr)
    xml = xml.getroottree()
    ids = list(allelementswithid(xml))
    print(ids)
    assert len(ids) == 3
    assert [item.tag for item in ids] == [ 'book', 'chapter', 'chapter' ]


def test_fix_colspec_width():
    xmlstr = """<table>
    <title>OpenStack services and clients</title>
    <tgroup cols="4">
      <colspec colwidth="20"/>
      <colspec colwidth="10"/>
      <colspec colwidth="41"/>
      <colspec colwidth="29"/>
      <thead/>
      <tbody/>
    </tgroup>
</table>"""
    xml = etree.fromstring(xmlstr)
    xml = xml.getroottree()
    fix_colspec_width(xml)

    assert xml.xpath('/table/tgroup/colspec/@colwidth') == ['20.0*', '10.0*', '41.0*', '29.0*']