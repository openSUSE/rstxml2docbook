
import pytest
from rstxml2db.cli import prepareparams, parsecli
from argparse import Namespace


def ns(**kwargs):
    params = dict(keepallids = True,
                  legalnotice = None,
                  productname = None,
                  productnumber = None,
                  output = None,
                  verbose = None,
                  params = [],
                  conventions = None,
                  db4 = False,
                  indexfile = 'a.xml',
                  )
    params.update(kwargs)
    return Namespace(**params)
    params = [('productname',   name),
              ('productnumber', number),
              ('legalnotice',   legal),
              ]


def compare(ns1, ns2):
    """Compare two Namespaces"""
    values={'output', 'indexfile', 'keepallids',
            # 'params',
            # 'booktree', 'legalnotice', 'productnumber', 'productname',
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
  (['-vv', 'a.xml'],
   ns(verbose=2)
   ),
  (['-l', 'legal.xml', 'a.xml'],
   ns(legalnotice='legal.xml')
   ),
  (['-c', 'preface.xml', 'a.xml'],
   ns(conventions='preface.xml')
   ),
  (['-o', 'foo', 'a.xml'],
   ns(output='foo')
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

