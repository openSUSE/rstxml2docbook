
import pytest
from rstxml2db.cli import prepareparams, parsecli
from rstxml2db.core import BOOKTREE, OUTDIR
from argparse import Namespace


def ns(**kwargs):
    params = dict(booktree = BOOKTREE,
                  bigfile = None,
                  keepallids = True,
                  legalnotice = None,
                  productname = None,
                  productnumber = None,
                  outputdir = OUTDIR,
                  verbose = None,
                  params = [],
                  indexfile = 'a.xml',
                  )
    params.update(kwargs)
    return Namespace(**params)


def compare(ns1, ns2):
    """Compare two Namespaces"""
    values={'bigfile', 'booktree', 'indexfile', 'keepallids',
            # 'legalnotice', 'productnumber', 'productname',
            'params', 'verbose'
            }
    for value in values:
        assert getattr(ns1, value) == getattr(ns2, value)


@pytest.mark.parametrize('params, expected', [
    (["a=2"],                   [('a', '2')]),
    (["a=2", "b=3"],            [('a', '2'), ('b', '3')]),
    (["a =2", "b= 3"],          [('a', '2'), ('b', '3')]),
    (["a = 2", "b = 3"],        [('a', '2'), ('b', '3')]),
    (["a.x = abc", "b.y = 4"],  [('a.x', 'abc'), ('b.y', '4')]),
    (["a=2", "b"],              [('a', '2')]),
    (["a=2", "b ="],            [('a', '2'), ('b', '')]),
])
def test_prepareparams(params, expected):
    result = prepareparams(params)
    assert result == expected


@pytest.mark.parametrize('cli,expected', [
  (['a.xml'], ns()),
  (['--verbose', 'a.xml'],
   ns(verbose=1,)
   ),
  (['-vv', '-t', 't.xml', 'a.xml'],
   ns(verbose=2, booktree='t.xml')
   ),
  (['-b', 'b.xml', 'a.xml'],
   ns(bigfile='b.xml')
   ),
  (['-d', 'foo', 'a.xml'],
   ns(outputdir='foo')
   ),
  (['-k', 'a.xml'],
   ns(keepallids=False)
   ),
  (['-p', 'a=2', '-p', 'b=4', 'a.xml'],
   ns(params=[('a', '2'), ('b', '4')])
   ),
  (['--param', 'a=2', '--param', 'b=4', 'a.xml'],
   ns(params=[('a', '2'), ('b', '4')])
   ),
])
def test_parsecli(cli, expected):
    result = parsecli(cli)
    compare(result, expected)