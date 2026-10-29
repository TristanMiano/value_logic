"""Exact gap over a bracket for continuous piecewise-affine scalar losses."""
from fractions import Fraction as F
from decision_cells import rational, union


def affine(knots, values, segment, action):
    a,b = knots[segment:segment+2]
    slope = (values[segment+1][action]-values[segment][action])/(b-a)
    return slope,values[segment][action]-slope*a


def value(knots,values,q,action):
    for i,(a,b) in enumerate(zip(knots,knots[1:])):
        if a <= q <= b:
            slope,offset = affine(knots,values,i,action)
            return slope*q+offset
    raise ValueError('query outside loss domain')


def assess(bracket, knot_strings, loss_rows):
    knots = list(map(rational,knot_strings))
    values = [list(map(rational,row)) for row in loss_rows]
    if len(knots) < 2 or knots != sorted(set(knots)):
        raise ValueError('strictly increasing loss knots required')
    if len(values) != len(knots) or not values[0] or any(len(row) != len(values[0]) for row in values):
        raise ValueError('loss row shape')
    inner,outer = union(bracket['inner']),union(bracket['outer'])
    if any(not any(c <= a <= b <= d for c,d in outer) for a,b in inner):
        raise ValueError('inner outside outer')
    if any(a < knots[0] or b > knots[-1] for a,b in outer):
        raise ValueError('outer exceeds loss domain')
    if not outer:
        return dict(status='INCONSISTENT_BRACKET')
    m = len(values[0])
    known_points = sorted({q for a,b in inner for q in [a,b]+[k for k in knots if a <= k <= b]})
    lower = [max(value(knots,values,q,a) for q in known_points) if known_points else None for a in range(m)]
    pieces = [(max(a,u),min(b,v),i) for a,b in outer for i,(u,v) in enumerate(zip(knots,knots[1:])) if max(a,u) <= min(b,v)]
    bounds,witnesses = [],[]
    evaluations = 0
    for a in range(m):
        best,qstar,bcomp = F(0),outer[0][0],None
        for b in range(m):
            if b == a:
                continue
            for lo,hi,i in pieces:
                points = {lo,hi}
                slope,offset = affine(knots,values,i,b)
                if lower[b] is not None and slope:
                    root = (lower[b]-offset)/slope
                    if lo <= root <= hi:
                        points.add(root)
                for q in sorted(points):
                    evaluations += 1
                    rival = value(knots,values,q,b)
                    if lower[b] is not None:
                        rival = max(rival,lower[b])
                    gap = value(knots,values,q,a)-rival
                    if gap > best:
                        best,qstar,bcomp = gap,q,b
        worst = [value(knots,values,qstar,b) if lower[b] is None else
                 max(lower[b],value(knots,values,qstar,b)) for b in range(m)]
        if worst[a]-min(worst) != best:
            raise AssertionError('continuous support witness mismatch')
        bounds.append(str(best))
        witnesses.append(dict(q=str(qstar),comparator=bcomp,worst_losses=list(map(str,worst)),
                              support='the supplied inner set union this point; signature scope only'))
    return dict(status='BOUNDED_CONTINUOUS_DECISION',sharp_improvement_bounds=bounds,
                witnesses=witnesses,candidate_evaluations=evaluations,
                assumes_nonempty_source=not bool(inner),criterion='worst loss of deterministic actions')
