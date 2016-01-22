#

from rstxml2db.treebuilder import process_index
import os
from py.path import local
from lxml import etree

HERE = os.path.dirname(os.path.abspath(__file__))

def test_process_index(tmpdir):
    """
    """
    docname = 'doc.001.xml'
    doc = local(HERE) / 'doc' / docname
    doc.copy(tmpdir)
    docfile = tmpdir / docname
    treefile = tmpdir / 'tree.xml'
    xml = process_index(str(docfile), str(treefile))
    assert xml
    assert os.path.exists(str(treefile))
    assert xml.getroot().tag == 'ref'
    assert xml.getroot().attrib['href'] == docname


def test_process_index1(tmpdir):
    docname = 'doc.001.xml'
    doc = local(HERE) / 'doc' / docname
    doc.copy(tmpdir)
    docfile = tmpdir / docname
    treefile = tmpdir / 'tree.xml'
    xml = process_index(str(docfile), str(treefile))
    assert xml
    assert os.path.exists(str(treefile))

