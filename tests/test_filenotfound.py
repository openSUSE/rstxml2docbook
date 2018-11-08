
import pytest
from rstxml2db.xml.process import process, transform
from rstxml2db.common import ERROR_CODES

from lxml import etree


def test_filenotfound1(args):
    #
    args.output = 'result.xml'
    args.indexfile = 'file-does-not-exist.xml'

    with pytest.raises((FileNotFoundError, OSError)):
        process(args)


def test_filenotfound2():
    #
    from rstxml2db.cli import main

    result = main(['-o', 'result.xml', 'file-does-not-exist.xml'])
    assert result == ERROR_CODES[FileNotFoundError]


def test_catch_XSLTApplyError(args):
    def create_xml_tree():
        xml = """<document source="doc/source/admin/index.rst">
 <section ids="test-guide" names="test\ guide">
  <title>Test Guide</title>
  <compound classes="toctree-wrapper">
  <compact_paragraph toctree="True">
    <bullet_list>
    <list_item classes="toctree-l1">
      <compact_paragraph classes="toctree-l1">
       <reference anchorname="" internal="True" refuri="unknown-file"
       >File which does not exist</reference>
      </compact_paragraph>
     </list_item>
    </bullet_list>
   </compact_paragraph>
  </compound>
  </section>
</document>
"""
        return etree.fromstring(xml).getroottree()

    args.output = 'result.xml'
    args.indexfile = 'fake-index.xml'

    doc = create_xml_tree()
    with pytest.raises(etree.XSLTApplyError):
        result = transform(doc, args)
