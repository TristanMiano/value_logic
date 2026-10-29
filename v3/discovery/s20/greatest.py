"""Restricted exact range shortcut; max-closure machinery is established.

The minimum-report input uses nonpositive one-coordinate receipt forms.
Future readouts are coordinatewise nondecreasing. See greatest.md.
"""
from copy import deepcopy
from fractions import Fraction as F
from range_service import V
from lp_witness import minimize
from audit_inputs import encoded


def prepare(problem):
    V.require(set(problem) == {'generators', 'receipts'}, 'problem fields')
    n, k = len(problem['generators']), len(problem['receipts'])
    V.require(n > 0, 'no generators')
    for i, g in enumerate(problem['generators']):
        _, _, c, _ = V.constraints(problem, i, (1 << k)-1)
        V.require(all(a >= 0 for a in c), 'future is not monotone')
        for row in g['A']:
            V.require(sum(a > 0 for a in V.vector(row,len(c))) <= 1,
                      'base row is not syntactically max-closed')
        for receipt in problem['receipts']:
            h = V.vector(receipt['forms'][i]['c'],len(c))
            V.require(all(a <= 0 for a in h) and sum(a != 0 for a in h) <= 1,
                      'receipt is not a negated nonnegative coordinate form')
    return n, k


def clean(entry):
    return encoded({key:value for key,value in entry.items() if key != 'numerical_status'})


def response(problem, j, i, x):
    form = problem['receipts'][j]['forms'][i]
    return V.dot(V.vector(form['c'],len(x)), x)+V.rational(form['d'])


def forced_masks(problem, points):
    """Compute all outside minima in O(n*k), including tied minima."""
    n, k = len(points), len(problem['receipts'])
    masks = [0]*n
    for j, receipt in enumerate(problem['receipts']):
        values = [response(problem,j,i,x) for i,x in enumerate(points)]
        smallest = min(values)
        count = sum(v == smallest for v in values)
        second = min((v for v in values if v > smallest),default=None)
        hi = V.rational(receipt['hi'])
        for i, value in enumerate(values):
            outside = smallest if value != smallest or count > 1 else second
            if outside is None or outside > hi:
                masks[i] |= 1 << j
    return masks


def optimum(rows, rhs, c, entry):
    V.require(set(entry) == {'kind','point','value','dual'} and entry['kind'] == 'optimum',
              'optimum certificate fields')
    x = V.vector(entry['point'],len(c))
    value = V.rational(entry['value'])
    V.require(all(V.dot(row,x) <= b for row,b in zip(rows,rhs)), 'infeasible primal')
    dual_bound = V.check_dual(rows,rhs,entry['dual'],[-a for a in c])
    V.require(V.dot(c,x) == value == -dual_bound, 'unmatched optimum')
    return x, value


def empty(rows, rhs, d, entry):
    V.require(set(entry) == {'kind','dual'} and entry['kind'] == 'empty','empty certificate fields')
    V.require(V.check_dual(rows,rhs,entry['dual'],[F(0)]*d) < 0, 'non-strict Farkas')


def produce(problem):
    n, k = prepare(problem)
    peaks, points = [], []
    for i in range(n):
        rows,rhs,c,_ = V.constraints(problem,i,0)
        entry = clean(minimize(rows,rhs,[-F(1)]*len(c)))
        if entry['kind'] == 'empty':
            return dict(kind='empty_block',problem_sha256=V.digest(problem),block=i,proof=entry)
        peaks.append(entry)
        points.append(list(map(F,entry['point'])))
    for j, receipt in enumerate(problem['receipts']):
        if min(response(problem,j,i,x) for i,x in enumerate(points)) > V.rational(receipt['hi']):
            return dict(kind='missed_receipt',problem_sha256=V.digest(problem),
                        peaks=peaks,receipt=j)
    masks = forced_masks(problem,points)
    lows, values = [], []
    for i,mask in enumerate(masks):
        rows,rhs,c,d = V.constraints(problem,i,mask)
        entry = clean(minimize(rows,rhs,c))
        V.require(entry['kind'] == 'optimum','greatest point should make forced cell feasible')
        lows.append(entry)
        values.append(F(entry['value'])+d)
    upper = min(V.dot(V.vector(g['c'],len(x)),x)+V.rational(g['d'])
                for g,x in zip(problem['generators'],points))
    return dict(kind='interval',problem_sha256=V.digest(problem),peaks=peaks,lows=lows,
                range=[str(min(values)),str(upper)])


class CheckedGreatest:
    def __init__(self, problem, certificate):
        self._problem = deepcopy(problem)
        certificate = deepcopy(certificate)
        n,k = prepare(self._problem)
        self._digest = V.digest(self._problem)
        V.require(certificate['problem_sha256'] == self._digest,'problem digest mismatch')
        self._range = None
        kind = certificate.get('kind')
        if kind == 'empty_block':
            V.require(set(certificate) == {'kind','problem_sha256','block','proof'},'empty block fields')
            i = certificate['block']
            V.require(type(i) is int and 0 <= i < n,'block index')
            rows,rhs,c,_ = V.constraints(self._problem,i,0)
            empty(rows,rhs,len(c),certificate['proof'])
            return
        expected = {'kind','problem_sha256','peaks','receipt'} if kind == 'missed_receipt' else {'kind','problem_sha256','peaks','lows','range'}
        V.require(kind in ('missed_receipt','interval') and set(certificate) == expected,
                  'certificate fields')
        V.require(len(certificate['peaks']) == n,'peak count')
        points = []
        for i,entry in enumerate(certificate['peaks']):
            rows,rhs,c,_ = V.constraints(self._problem,i,0)
            x,_ = optimum(rows,rhs,[-F(1)]*len(c),entry)
            points.append(x)
        if kind == 'missed_receipt':
            j = certificate['receipt']
            V.require(type(j) is int and 0 <= j < k,'receipt index')
            V.require(min(response(self._problem,j,i,x) for i,x in enumerate(points)) >
                      V.rational(self._problem['receipts'][j]['hi']), 'receipt actually feasible')
            return
        for j,receipt in enumerate(self._problem['receipts']):
            V.require(min(response(self._problem,j,i,x) for i,x in enumerate(points)) <=
                      V.rational(receipt['hi']), 'greatest source misses receipt')
        V.require(len(certificate['lows']) == n,'lower certificate count')
        masks = forced_masks(self._problem,points)
        lows, values = [], []
        for i,(mask,entry) in enumerate(zip(masks,certificate['lows'])):
            rows,rhs,c,d = V.constraints(self._problem,i,mask)
            x,value = optimum(rows,rhs,c,entry)
            lows.append(x)
            values.append(value+d)
        anchor = min(range(n),key=lambda i:values[i])
        lower = values[anchor]
        upper = min(V.dot(V.vector(g['c'],len(x)),x)+V.rational(g['d'])
                    for g,x in zip(self._problem['generators'],points))
        V.require(certificate['range'] == [str(lower),str(upper)] and lower <= upper,
                  'range mismatch')
        self._range = (lower,upper)
        self._greatest = points
        self._lower_source = deepcopy(points)
        self._lower_source[anchor] = lows[anchor]
        self._masks = masks

    @property
    def problem_sha256(self):
        return self._digest

    def ranges(self):
        return [] if self._range is None else [[str(a) for a in self._range]]

    def source(self, value):
        q = V.rational(value)
        V.require(self._range is not None and self._range[0] <= q <= self._range[1],
                  'value outside range')
        starts, slopes = [], []
        for g,z,p in zip(self._problem['generators'],self._lower_source,self._greatest):
            c,d = V.vector(g['c'],len(z)),V.rational(g['d'])
            starts.append(V.dot(c,z)+d)
            slopes.append(V.dot(c,[b-a for a,b in zip(z,p)]))
        t = max([F(0)]+[(q-a)/s for a,s in zip(starts,slopes) if s > 0])
        V.require(0 <= t <= 1 and all(a >= q for a,s in zip(starts,slopes) if s == 0),
                  'source path invariant')
        xs = [[a+t*(b-a) for a,b in zip(z,p)] for z,p in zip(self._lower_source,self._greatest)]
        V.require(min(a+t*s for a,s in zip(starts,slopes)) == q,'readout path invariant')
        return dict(problem_sha256=self._digest,q=str(q),source=encoded(xs),t=str(t))
