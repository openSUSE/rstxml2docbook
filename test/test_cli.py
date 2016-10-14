
import pytest
from rstxml2db.cli import prepareparams, parsecli


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
  (['a.xml'], dict(indexfile='a.xml')),
  (['--verbose', 'a.xml'],
   dict(verbose=1)
   ),
  (['-vv', 'a.xml'],
   dict(verbose=2)
   ),
  (['-l', 'legal.xml', 'a.xml'],
   dict(legalnotice='legal.xml')
   ),
  (['-c', 'preface.xml', 'a.xml'],
   dict(conventions='preface.xml')
   ),
  (['-o', 'foo', 'a.xml'],
   dict(output='foo')
   ),
  (['-k', 'a.xml'],
   dict(keepallids=False)
   ),
  (['--productname', 'Foo', 'a.xml'],
   dict(_productname='Foo')
   ),
  (['--productnumber', '42', 'a.xml'],
   dict(_productnumber='42')
   ),
  (['--productname', 'Foo', '--productnumber', '42', 'a.xml'],
   dict(_productname='Foo', _productnumber='42')
   ),
  (['-p', 'a=2', '-p', 'b=4', 'a.xml'],
   dict(params=[('a', '2'), ('b', '4')])
   ),
  (['--param', 'a=2', '--param', 'b=4', 'a.xml'],
   dict(params=[('a', '2'), ('b', '4')])
   ),
])
def test_parsecli(cli, expected):
    result = parsecli(cli)
    # Create set difference and only compare this with the expected dictionary
    diff = set(result.__dict__) & set(expected)
    result = {i: getattr(result, i) for i in diff}
    assert result == expected
