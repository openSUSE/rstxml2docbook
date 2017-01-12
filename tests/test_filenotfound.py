
import pytest
from rstxml2db.xml.process import process


def test_filenotfound1(args):
    #
    args.output = 'result.xml'
    args.indexfile = 'file-does-not-exist.xml'

    with pytest.raises((FileNotFoundError, OSError)):
        process(args)


def test_filenotfound2():
    #
    from rstxml2db import main

    with pytest.raises(SystemExit):
        main(['-o', 'result.xml', 'file-does-not-exist.xml'])
