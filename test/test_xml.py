#

from lxml import etree
from py.path import local
import pytest
from unittest.mock import patch, Mock
from rstxml2db.xml import addchapter


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


def test_addchaper_only_prefix(monkeypatch):
    xmlstr = """<book id="book">
  <title>Test</title>
  <preface id="pref.intro">
    <title>Intro</title>
    <para>Nothing.</para>
  </preface>
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
    assert 0 == 1
