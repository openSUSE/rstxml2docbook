from rstxml2db.xml.process import write_result_tree
from rstxml2db.core import RESULT_TREE_DIR
from lxml import etree

from py.path import local

DATADIR = local(__file__).parts()[-2] / "data"


def test_result_tree_with_default_dir(args):
    args.result_tree = True
    resdir = local(RESULT_TREE_DIR)
    xml = etree.XML("<ok/>").getroottree()
    write_result_tree(xml, "ok.xml", args)
    assert resdir.listdir()

def test_result_tree_with_default_dir(tmpdir, args):
    args.result_tree = True
    args.result_tree_dir = str(tmpdir)
    xml = etree.XML("<ok/>").getroottree()
    write_result_tree(xml, "ok.xml", args)
    assert tmpdir.listdir()
