
import pytest
from rstxml2db.xml.process import process
from rstxml2db.common import ERROR_CODES


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
