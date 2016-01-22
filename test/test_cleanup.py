#

from rstxml2db.cleanup import cleanupxml
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
