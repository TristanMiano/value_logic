"""Exact, development-only query service for a verified scalar-range certificate.

No optimizer is used here. Compilation and source output are charged work.
The historical verifier is imported unchanged; input snapshots are copied.
"""
from bisect import bisect_left, bisect_right
from copy import deepcopy
from fractions import Fraction as F
import importlib.util
from pathlib import Path

_path = Path(__file__).resolve().parent.parent / 's19/range_cert_verify.py'
_spec = importlib.util.spec_from_file_location('range_service_verifier', _path)
V = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(V)


def smaller(a, b):
    """None denotes positive infinity; unavailable states are absent keys."""
    if a is None:
        return b
    if b is None:
        return a
    return min(a, b)


def greater(a, b):
    if a is None:
        return b is not None
    return b is not None and a > b


def subsets(mask):
    sub = mask
    while True:
        yield sub
        if sub == 0:
            break
        sub = (sub - 1) & mask


def advance(previous, table, k):
    values, choices = {}, {}
    for mask in range(1 << k):
        for sub in subsets(mask):
            rest = mask ^ sub
            if sub not in table or rest not in previous:
                continue
            candidate = smaller(previous[rest], table[sub][1])
            if mask not in values or greater(candidate, values[mask]):
                values[mask], choices[mask] = candidate, sub
    return values, choices


class CheckedRange:
    """A source snapshot. Rational query inputs must be exact strings.

    This is not a sandbox for adversarially large JSON or a model-authentication
    service. Correctness is conditional on the caller's supplied model.
    """

    def __init__(self, problem, certificate):
        self._problem, self._certificate = deepcopy(problem), deepcopy(certificate)
        result = V.verify(self._problem, self._certificate)
        self.problem_sha256 = result['problem_sha256']
        self._ranges = tuple(tuple(map(F, r)) for r in result['ranges'])
        self._ends = tuple(b for _, b in self._ranges)
        self._n = len(self._problem['generators'])
        self._k = len(self._problem['receipts'])
        self._tables = []
        for row in self._certificate['faces']:
            self._tables.append({t: (F(e['lo']), F(e['hi']))
                                 for t, e in enumerate(row) if e['kind'] == 'bounded'})
        self._prefix = [{0: None}]
        self._prefix_choice = [{}]
        for table in self._tables:
            values, choice = advance(self._prefix[-1], table, self._k)
            self._prefix.append(values)
            self._prefix_choice.append(choice)
        self._suffix = [None] * (self._n + 1)
        self._suffix_choice = [None] * (self._n + 1)
        self._suffix[self._n] = {0: None}
        self._suffix_choice[self._n] = {}
        for i in range(self._n - 1, -1, -1):
            values, choice = advance(self._suffix[i + 1], self._tables[i], self._k)
            self._suffix[i], self._suffix_choice[i] = values, choice

        full = (1 << self._k) - 1
        anchors = []
        for i, table in enumerate(self._tables):
            for t, (lo, hi) in table.items():
                outside = full ^ t
                found, cap, split = False, None, None
                for left in subsets(outside):
                    right = outside ^ left
                    if left not in self._prefix[i] or right not in self._suffix[i + 1]:
                        continue
                    candidate = smaller(self._prefix[i][left], self._suffix[i + 1][right])
                    if not found or greater(candidate, cap):
                        found, cap, split = True, candidate, left
                if found:
                    end = smaller(hi, cap)
                    if lo <= end:
                        anchors.append((lo, end, i, t, split))
        self._anchors = tuple(sorted(anchors))
        self._starts = tuple(a[0] for a in self._anchors)
        self._prefix_best = []
        for j, anchor in enumerate(self._anchors):
            prev = self._prefix_best[-1] if self._prefix_best else None
            best = j if prev is None or anchor[1] > self._anchors[prev][1] else prev
            self._prefix_best.append(best)
        V.require(V.normalize([(a[0], a[1]) for a in self._anchors]) == list(self._ranges),
                  'service reconstruction differs from verified range')

    def ranges(self):
        return [[str(a), str(b)] for a, b in self._ranges]

    def _anchor(self, q):
        index = bisect_right(self._starts, q) - 1
        if index < 0:
            return None
        candidate = self._anchors[self._prefix_best[index]]
        return candidate if q <= candidate[1] else None

    def contains(self, value):
        return self._anchor(V.rational(value)) is not None

    def band(self, lower, upper):
        lo, hi = V.rational(lower), V.rational(upper)
        V.require(lo <= hi, 'reversed query band')
        j = bisect_left(self._ends, lo)
        if j < len(self._ranges) and self._ranges[j][0] <= hi:
            return dict(status='INTERSECTS', q=str(max(lo, self._ranges[j][0])),
                        problem_sha256=self.problem_sha256)
        return dict(status='DISJOINT',
                    left=None if j == 0 else str(self._ranges[j - 1][1]),
                    right=None if j == len(self._ranges) else str(self._ranges[j][0]),
                    problem_sha256=self.problem_sha256)

    def source(self, value):
        q = V.rational(value)
        anchor = self._anchor(q)
        V.require(anchor is not None, 'value outside verified range')
        _, _, i, assigned, left = anchor
        full = (1 << self._k) - 1
        masks = [0] * self._n
        masks[i] = assigned
        remaining = left
        for j in range(i - 1, -1, -1):
            masks[j] = self._prefix_choice[j + 1][remaining]
            remaining ^= masks[j]
        V.require(remaining == 0, 'prefix reconstruction')
        remaining = full ^ assigned ^ left
        for j in range(i + 1, self._n):
            masks[j] = self._suffix_choice[j][remaining]
            remaining ^= masks[j]
        V.require(remaining == 0, 'suffix reconstruction')
        entries = [row[t] for row, t in zip(self._certificate['faces'], masks)]
        points = [list(map(F, e['xhi'])) for e in entries]
        e = entries[i]
        low, high = F(e['lo']), F(e['hi'])
        if low == high:
            points[i] = list(map(F, e['xlo']))
        else:
            fraction = (q - low) / (high - low)
            points[i] = [F(a) + fraction * (F(b) - F(a))
                         for a, b in zip(e['xlo'], e['xhi'])]
        return dict(problem_sha256=self.problem_sha256, q=str(q), anchor=i,
                    assignment=masks, source=[[str(v) for v in x] for x in points])
