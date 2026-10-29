"""Development-only inner/outer receipt-range service, using exact rationals.

Unknown local cells retain their outer box. Only checked evidence changes state.
Explicit finite coordinate bounds are a prototype input requirement.
"""
from copy import deepcopy
from fractions import Fraction as F
from range_service import V, advance, subsets, smaller, greater
from certificate_transport import implied_box, box_extrema


class IntervalImage:
    """The anchor construction on arbitrary interval tables, with backpointers."""

    def __init__(self, tables, k):
        self.tables, self.k = tables, k
        self.n, self.full = len(tables), (1 << k)-1
        self.prefix, self.pc = [{0: None}], [{}]
        for table in tables:
            values, choices = advance(self.prefix[-1], table, k)
            self.prefix.append(values)
            self.pc.append(choices)
        self.suffix, self.sc = [None]*(self.n+1), [None]*(self.n+1)
        self.suffix[-1], self.sc[-1] = {0: None}, {}
        for i in range(self.n-1, -1, -1):
            self.suffix[i], self.sc[i] = advance(self.suffix[i+1], tables[i], k)
        self.anchors = []
        for i, table in enumerate(tables):
            for mask, (lo, hi) in table.items():
                outside = self.full ^ mask
                found, cap, split = False, None, None
                for left in subsets(outside):
                    right = outside ^ left
                    if left not in self.prefix[i] or right not in self.suffix[i+1]:
                        continue
                    value = smaller(self.prefix[i][left], self.suffix[i+1][right])
                    if not found or greater(value, cap):
                        found, cap, split = True, value, left
                if found and lo <= smaller(hi, cap):
                    self.anchors.append((lo, smaller(hi, cap), i, mask, split))
        self.ranges = V.normalize([(a, b) for a, b, *_ in self.anchors])

    def assignment(self, q):
        anchor = next((a for a in self.anchors if a[0] <= q <= a[1]), None)
        V.require(anchor is not None, 'not witnessed')
        _, _, i, assigned, left = anchor
        masks = [0]*self.n
        masks[i] = assigned
        remaining = left
        for j in range(i-1, -1, -1):
            masks[j] = self.pc[j+1][remaining]
            remaining ^= masks[j]
        V.require(remaining == 0, 'prefix reconstruction')
        remaining = self.full ^ assigned ^ left
        for j in range(i+1, self.n):
            masks[j] = self.sc[j][remaining]
            remaining ^= masks[j]
        V.require(remaining == 0, 'suffix reconstruction')
        return i, masks


class PartialRange:
    def __init__(self, problem):
        self._problem = deepcopy(problem)
        V.require(set(problem) == {'generators', 'receipts'}, 'problem fields')
        self.n = len(problem['generators'])
        self.k = len(problem['receipts'])
        V.require(self.n > 0, 'no generators')
        self.full = (1 << self.k)-1
        self._digest = V.digest(self._problem)
        self._boxes, self._inner, self._outer = [], [], []
        self._evidence = []
        self.compilations = 0
        for i, generator in enumerate(self._problem['generators']):
            _, _, c, d = V.constraints(self._problem, i, self.full)
            box = implied_box(generator)
            lo, hi = box_extrema(c, box)
            self._boxes.append(box)
            self._inner.append({})
            self._outer.append({t: (lo+d, hi+d) for t in range(1 << self.k)})

    @property
    def problem_sha256(self):
        return self._digest

    def _indices(self, i, mask, digest):
        V.require(digest == self._digest, 'problem digest mismatch')
        V.require(type(i) is int and 0 <= i < self.n, 'block index')
        V.require(type(mask) is int and 0 <= mask <= self.full, 'mask index')

    def _point(self, i, point):
        rows, rhs, c, d = V.constraints(self._problem, i, 0)
        x = tuple(V.vector(point, len(c)))
        V.require(all(V.dot(row, x) <= b for row, b in zip(rows, rhs)),
                  'point violates base or receipt lower bound')
        cover = 0
        for j, receipt in enumerate(self._problem['receipts']):
            form = receipt['forms'][i]
            value = V.dot(V.vector(form['c'], len(c)), x)+V.rational(form['d'])
            if value <= V.rational(receipt['hi']):
                cover |= 1 << j
        return cover, V.dot(c, x)+d, x

    def _dual(self, i, mask, side, weights):
        rows, rhs, c, d = V.constraints(self._problem, i, mask)
        V.require(side in ('lower', 'upper', 'empty'), 'dual side')
        target = [-a for a in c] if side == 'lower' else c if side == 'upper' else [F(0)]*len(c)
        bound = V.check_dual(rows, rhs, weights, target)
        if side == 'empty':
            V.require(bound < 0, 'nonnegative Farkas bound')
        # The verifier interleaves lower rows with selected upper rows.
        cursor = len(self._problem['generators'][i]['A'])
        core = 0
        for j in range(self.k):
            cursor += 1
            if mask >> j & 1:
                if V.rational(weights[cursor]):
                    core |= 1 << j
                cursor += 1
        V.require(cursor == len(rows), 'row indexing')
        value = d-bound if side == 'lower' else d+bound
        return core, side, value

    def _apply(self, i, points, bounds, evidence):
        """Prepare all affected entries, check invariants, then commit atomically."""
        inner, outer = dict(self._inner[i]), dict(self._outer[i])
        for cover, value, point in points:
            for mask in subsets(cover):
                if mask not in inner:
                    inner[mask] = (value, value, point, point)
                else:
                    lo, hi, xlo, xhi = inner[mask]
                    inner[mask] = (min(lo, value), max(hi, value),
                                   point if value < lo else xlo,
                                   point if value > hi else xhi)
        touched = set()
        for core, side, value in bounds:
            for extra in subsets(self.full ^ core):
                mask = core | extra
                touched.add(mask)
                if mask not in outer:
                    continue
                lo, hi = outer[mask]
                if side == 'lower':
                    lo = max(lo, value)
                elif side == 'upper':
                    hi = min(hi, value)
                if side == 'empty' or lo > hi:
                    del outer[mask]
                else:
                    outer[mask] = (lo, hi)
        for mask, (lo, hi, *_points) in inner.items():
            V.require(mask in outer and outer[mask][0] <= lo <= hi <= outer[mask][1],
                      'evidence conflicts with witnessed point')
        self._inner[i], self._outer[i] = inner, outer
        self._evidence.append(deepcopy(evidence))
        return dict(inner_masks=len(inner), outer_masks=len(outer),
                    bound_masks_touched=len(touched))

    def add_point(self, i, point, digest):
        self._indices(i, 0, digest)
        prepared = self._point(i, point)
        result = self._apply(i, [prepared], [], dict(kind='point', block=i, point=point))
        return dict(result, cover=prepared[0])

    def add_dual(self, i, mask, side, weights, digest):
        self._indices(i, mask, digest)
        prepared = self._dual(i, mask, side, weights)
        result = self._apply(i, [], [prepared],
                             dict(kind='dual', block=i, mask=mask, side=side, weights=weights))
        return dict(result, core=prepared[0])

    def add_certificate(self, i, mask, entry, digest):
        self._indices(i, mask, digest)
        rows, rhs, c, d = V.constraints(self._problem, i, mask)
        points, bounds = [], []
        if entry.get('kind') == 'empty':
            V.require(set(entry) == {'kind', 'dual'}, 'empty fields')
            bounds.append(self._dual(i, mask, 'empty', entry['dual']))
        else:
            V.require(entry.get('kind') == 'bounded' and
                      set(entry) == {'kind', 'lo', 'hi', 'xlo', 'xhi', 'dlo', 'dhi'},
                      'bounded fields')
            lo, hi = V.rational(entry['lo']), V.rational(entry['hi'])
            V.require(lo <= hi, 'endpoint order')
            for key, expected in (('xlo', lo), ('xhi', hi)):
                point = self._point(i, entry[key])
                V.require(point[0] & mask == mask, 'point misses assigned receipt')
                V.require(point[1] == expected, 'primal objective')
                points.append(point)
            for side, key, expected in (('lower', 'dlo', lo), ('upper', 'dhi', hi)):
                bound = self._dual(i, mask, side, entry[key])
                V.require(bound[2] == expected, 'dual objective')
                bounds.append(bound)
        return self._apply(i, points, bounds,
                           dict(kind='certificate', block=i, mask=mask, entry=entry))

    def propagate_box(self, i, mask, passes=2):
        self._indices(i, mask, self._digest)
        V.require(type(passes) is int and passes >= 0, 'sweep budget')
        rows, rhs, c, d = V.constraints(self._problem, i, mask)
        box = list(self._boxes[i])
        empty, row_visits, updates = False, 0, 0
        for _ in range(passes):
            changed = False
            for row, b in zip(rows, rhs):
                row_visits += 1
                minimum = box_extrema(row, box)[0]
                if minimum > b:
                    empty = True
                    break
                for j, a in enumerate(row):
                    if not a:
                        continue
                    others = sum((min(v*l, v*u) for h, (v, (l, u)) in
                                  enumerate(zip(row, box)) if h != j), F(0))
                    value = (b-others)/a
                    lo, hi = box[j]
                    new = (lo, min(hi, value)) if a > 0 else (max(lo, value), hi)
                    if new[0] > new[1]:
                        empty = True
                        break
                    if new != box[j]:
                        box[j], changed = new, True
                        updates += 1
                if empty:
                    break
            if empty or not changed:
                break
        if empty:
            bounds = [(mask, 'empty', F(0))]
        else:
            lo, hi = box_extrema(c, box)
            bounds = [(mask, 'lower', lo+d), (mask, 'upper', hi+d)]
        result = self._apply(i, [], bounds,
                             dict(kind='box', block=i, mask=mask, passes=passes))
        return dict(result, empty=empty, row_visits=row_visits,
                    coordinate_updates=updates, lp_calls=0)

    def _images(self):
        self.compilations += 2
        tables = [{t: pair[:2] for t, pair in row.items()} for row in self._inner]
        return IntervalImage(tables, self.k), IntervalImage(self._outer, self.k)

    def bracket(self):
        inner, outer = self._images()
        return dict(problem_sha256=self._digest,
                    inner=[[str(a), str(b)] for a, b in inner.ranges],
                    outer=[[str(a), str(b)] for a, b in outer.ranges],
                    exact=inner.ranges == outer.ranges,
                    inconsistent=not outer.ranges)

    def query(self, lower, upper):
        lo, hi = V.rational(lower), V.rational(upper)
        V.require(lo <= hi, 'reversed query band')
        inner, outer = self._images()
        hit = next((max(a, lo) for a, b in inner.ranges if a <= hi and lo <= b), None)
        if hit is not None:
            anchor, masks = inner.assignment(hit)
            points = [self._inner[i][mask][3] for i, mask in enumerate(masks)]
            low, high, xlo, xhi = self._inner[anchor][masks[anchor]]
            ratio = F(0) if low == high else (hit-low)/(high-low)
            points[anchor] = tuple(a+ratio*(b-a) for a, b in zip(xlo, xhi))
            return dict(status='ATTAINABLE', problem_sha256=self._digest, q=str(hit),
                        assignment=masks, source=[[str(a) for a in x] for x in points])
        possible = any(a <= hi and lo <= b for a, b in outer.ranges)
        return dict(status='UNRESOLVED' if possible else 'EXCLUDED',
                    problem_sha256=self._digest, inconsistent=not outer.ranges)

    def state(self):
        """Detached inspection data; inspecting it does not compile a bracket."""
        return deepcopy(dict(inner=self._inner, outer=self._outer,
                             evidence=self._evidence, boxes=self._boxes))
