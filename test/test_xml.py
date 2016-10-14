#

from lxml import etree
import json
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
