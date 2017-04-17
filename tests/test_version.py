#!/usr/bin/env python3


def test_version():
    """Check if version is available and set"""
    from rstxml2db import __version__
    assert __version__


def test_version_from_cli(capsys):
    """Checks if option --version creates a correct version"""
    from rstxml2db.cli import main
    import pytest

    with pytest.raises(SystemExit):
        main(["--version"])
