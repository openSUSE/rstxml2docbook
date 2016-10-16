#

from lxml import etree
import json
from unittest.mock import patch
from py.path import local
import pytest
from unittest.mock import patch, Mock
from rstxml2db.xml import addchapter, transform
from rstxml2db.core import NSMAP


def test_addchaper(monkeypatch):
    xmlstr = """<book id="book">
  <title>Test</title>
  <chapter id="cha.intro">
    <title>Intro</title>
    <para>Nothing.</para>
  </chapter>
</book>
    """
    def mockreturn(path):
       chapstr = """<chapter id="foo">
          <title>I'm the Foo</title>
          <para>Nothing to see.</para>
        </chapter>"""
       return etree.fromstring(chapstr).getroottree()

    # Patching etree.parse
    monkeypatch.setattr('rstxml2db.xml.etree.parse', mockreturn)
    xml = etree.fromstring(xmlstr).getroottree()
    addchapter(xml, 'fake.xml')
    result = etree.tostring(xml, encoding="unicode")
    assert xml.xpath("/book/chapter[1]/@id") == ['foo']


@pytest.mark.skip
@patch('rstxml2db.xml.etree.parse')
@patch('rstxml2db.log.log.isEnabledFor')
def test_addchaper_mocklog(mock_log, mock_etreeparse):
    xmlstr = """<book id="book">
  <title>Test</title>
  <chapter id="cha.intro">
    <title>Intro</title>
    <para>Nothing.</para>
  </chapter>
</book>
    """
    chapstr = """<chapter id="empty"/>"""
    mock_log.return_value = True
    xml = etree.fromstring(xmlstr).getroottree()
    mock_etreeparse.return_value = etree.fromstring(chapstr).getroottree()
    addchapter(xml, 'fake.xml')
    assert mock_log.called


def test_xmltestcases(xmltestcase, args):
    """Runs one XML testcase"""
    jsonfile = xmltestcase.new(ext=".params.json")
    if not jsonfile.exists():
        raise pytest.skip('Missing %r file, skipped.' % str(jsonfile))

    params = json.load(jsonfile)

    doc = etree.parse(str(xmltestcase))
    resultxml = transform(doc, args)
    resultxmlstr = etree.tostring(resultxml, encoding="unicode")

    for param in params:
        xpath, expected = param
        assert resultxml.xpath(xpath, namespaces=NSMAP) == expected
