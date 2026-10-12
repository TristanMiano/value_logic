"""Ordinary exact parametric-closure profile with checked interval certificates."""
from bisect import bisect_left
from fractions import Fraction as F
from flow_v2 import check
from price_flow import exact


def line(terms, prices, bits):
    return (sum((r for mask, r in terms if mask & bits == mask), F(0)),
            sum((q for i, q in enumerate(prices) if bits >> i & 1), F(0)))


def build(terms, prices):
    assert terms and prices and all(mask > 0 for mask, _ in terms)
    assert all(q > 0 for q in prices)
    total = sum((r for _, r in terms), F(0))
    end = total / min(prices) + 1
    nodes = {}
    def oracle(x):
        if x not in nodes:
            allocation, witness = exact(terms, [x*q for q in prices])
            bits = (1 << len(prices)) - 1 if x == 0 else witness['bits']
            a, c = line(terms, prices, bits)
            assert a - x*c == witness['value']
            nodes[x] = dict(price=x, bits=bits, a=a, c=c, value=witness['value'], allocation=allocation)
        return nodes[x]
    pieces = []
    def emit(lo, hi, bits):
        if lo < hi: pieces.append(dict(lo=lo, hi=hi, bits=bits))
    def divide(lo, hi):
        left, right = oracle(lo), oracle(hi)
        if (left['a'],left['c']) == (right['a'],right['c']):
            emit(lo, hi, left['bits']); return
        assert left['c'] > right['c'] and right['bits'] & left['bits'] == right['bits']
        cross = (left['a'] - right['a']) / (left['c'] - right['c'])
        assert lo <= cross <= hi
        middle = oracle(cross)
        if middle['value'] == left['a'] - cross*left['c']:
            emit(lo, cross, left['bits']); emit(cross, hi, right['bits'])
        else:
            assert lo < cross < hi
            assert middle['value'] > left['a'] - cross*left['c']
            divide(lo, cross); divide(cross, hi)
    divide(F(0), end)
    # Adjacent same-cut intervals need only their external endpoint flows.
    merged = []
    for p in pieces:
        if merged and merged[-1]['bits'] == p['bits']:
            assert merged[-1]['hi'] == p['lo']; merged[-1]['hi'] = p['hi']
        else: merged.append(p.copy())
    needed = {x for p in merged for x in (p['lo'], p['hi'])}
    return dict(end=end, pieces=merged, endpoints=[nodes[x] for x in sorted(needed)], oracle_calls=len(nodes))


def verify(terms, prices, profile):
    """Feasible endpoint flows plus matching cut prove every interior price."""
    assert terms and prices and all(isinstance(q,F) and q>0 for q in prices)
    assert all(isinstance(r,F) and r>=0 and type(mask) is int and 0<mask<1<<len(prices) for mask,r in terms)
    end = profile['end']; total = sum((r for _,r in terms), F(0))
    assert isinstance(end,F) and end > total/min(prices)
    points = {}; cuts = []; last = F(0)
    for p in profile['endpoints']:
        x = p['price']; assert isinstance(x,F) and 0 <= x <= end and x not in points
        points[x] = check(terms, [x*q for q in prices], p['allocation'])['upper']
    for p in profile['pieces']:
        lo,hi,bits = p['lo'],p['hi'],p['bits']
        assert lo == last and lo < hi <= end and type(bits) is int and 0<=bits<1<<len(prices)
        a,c = line(terms,prices,bits)
        assert points[lo] == a-lo*c and points[hi] == a-hi*c
        cuts.append((hi,a,c,bits)); last=hi
    assert last == end and cuts and cuts[-1][1] == 0 and cuts[-1][2] == 0
    return tuple(cuts)


def prepare(terms, prices, profile, version):
    # Certificate checked once; graph meaning/version supplied by the caller.
    rows = verify(tuple(terms), tuple(prices), profile)
    thresholds = tuple(r[0] for r in rows)
    def answer(x, query_version):
        assert query_version == version and isinstance(x,F) and x >= 0
        if x > thresholds[-1]: return F(0), 0
        _,a,c,bits = rows[bisect_left(thresholds,x)]
        return a-x*c, bits
    return answer
