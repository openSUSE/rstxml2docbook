#
# Copyright (c) 2017 SUSE Linux GmbH
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 3 of the GNU General Public License as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, contact SUSE LLC.
#
# To contact SUSE about this file by physical or electronic mail,
# you may find current contact information at www.suse.com


import inspect
import pytest
import re
import rstxml2db


def getallfunctions(module=rstxml2db):
    def getfunctions(_module):
        for _, func, in inspect.getmembers(_module,
                                           inspect.isfunction):
            # Make sure you only investigate functions from our modules:
            if func.__module__.startswith(_module.__name__):
                yield func
    def getmodules(_module):
        for _, m, in inspect.getmembers(_module,
                                        inspect.ismodule):
            if m.__package__.startswith(_module.__package__):
                yield m

    # allfunctions = []
    for ff in getfunctions(module):
         yield ff
    for mm in getmodules(module):
        for ff in getfunctions(mm):
            yield ff

modfuncs = list(getallfunctions())
modfuncsnames = [".".join([ff.__module__, ff.__name__]) for ff in modfuncs]


@pytest.mark.parametrize("func",
                         modfuncs,
                         ids=modfuncsnames
                         )
def test_docstrings_nonempty(func):
    fname = func.__name__
    doc = func.__doc__

    # If our function name starts with "_", it's private so we skip this test:
    if fname.startswith('_'):
        return True

    assert doc is not None, "Need an non-empty docstring for %r" % fname


@pytest.mark.parametrize("func",
                         modfuncs,
                         ids=modfuncsnames
                         )
def test_docstrings_args(func):
    fname = func.__name__
    doc = func.__doc__

    # If our function name starts with "_", it's private so we skip this test:
    if fname.startswith('_'):
        return True

    assert doc is not None
    if func.__code__.co_argcount:
        for arg in inspect.getfullargspec(func).args:
            m = re.search(r":param\s+\w*\s*%s:" % arg, doc)
            assert m, "Func argument %r " \
                "not explained in docstring " \
                "of function %r" % (arg, fname)
