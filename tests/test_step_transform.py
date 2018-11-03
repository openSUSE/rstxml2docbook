from rstxml2db.xml.process import step_blockelements_transform
from lxml import etree

from py.path import local

DATADIR = local(__file__).parts()[-2] / "data"

def test_block_in_para():
    xmlstr = (DATADIR / "paragraph-with-block.xml").read()
    xml = etree.fromstring(xmlstr)
    result = step_blockelements_transform(xml, {})
    # First element is <title>
    assert result.xpath("/*/*/*[2][self::paragraph]")
    assert result.xpath("/*/*/*[3][self::bullet_list]")
    assert result.xpath("/*/*/*[4][self::paragraph]")
    assert result.xpath("/*/*/bullet_list/list_item/paragraph/text()") == ['First item']
