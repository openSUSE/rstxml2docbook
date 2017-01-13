#

from rstxml2db.cleanup import (remove_double_ids,
                               finddoubleids,
                               allelementswithid,
                               fix_colspec_width,
                               add_pi_in_screen,
                               normalize_source_attr,
                               )
from lxml import etree
import pytest


def test_remove_double_ids():
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
    remove_double_ids(xml, False)
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
    assert [item.tag for item in ids] == ['book', 'chapter', 'chapter']


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


@pytest.mark.parametrize('xmlstr,limit,expected', [
    ("""<screen>x</screen>""",                                  10, False),
    ("""<screen>{}</screen>""".format('0123456789'*5+'012345'), 10, True),
    ("""<screen>01234567890123456789</screen>""",               10, True),
    ("""<screen>01234567890123456789</screen>""",               40, False),
])
def test_add_pi_in_screen(xmlstr, limit, expected):
    xml = etree.fromstring(xmlstr)
    xml = xml.getroottree()
    add_pi_in_screen(xml, limit=limit)

    assert bool(xml.xpath("/screen/processing-instruction('dbsuse-fo')")) == expected

@pytest.mark.parametrize('xpath, expected', [
    ("/document/@source", "zoo.rst"),
    ("/document/section/document/@source", "blub.rst"),
])
def test_normalize_source_attr(xpath, expected):
    xmlstr = """<document source="/foo/bar/zoo.rst">
 <section ids="foo" names="foo">
  <title></title>
  <paragraph></paragraph>
  <document source="/foo/bar/blub.rst">
    <section ids="bar" names="bar">
        <title>Bar</title>
        <paragraph></paragraph>
    </section>
  </document>
 </section>
</document>"""
    xml = etree.fromstring(xmlstr)
    xml = xml.getroottree()
    normalize_source_attr(xml)
    assert xml.xpath(xpath) == [expected]
