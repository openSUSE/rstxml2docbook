#

from rstxml2db.cleanup import add_pi_in_screen
from lxml import etree


def test_if_screen_is_empty():
    xml = etree.XML("<screen/>")
    add_pi_in_screen(xml)
    assert not xml.xpath("processing-instruction()")
