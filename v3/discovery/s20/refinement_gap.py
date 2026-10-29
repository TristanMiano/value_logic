"""Sharp robust-action gap over a partial attainable-cell signature."""
from fractions import Fraction as F
import decision_cells as cells


def assess(bracket, breakpoints, losses, criterion='loss'):
    result = cells.assess(bracket, breakpoints, losses, criterion)
    if result['status'] != 'BOUNDED_DECISION':
        return result
    values = [[F(v) for v in row] for row in losses]
    if criterion == 'regret':
        values = [[v-min(row) for v in row] for row in values]
    known, possible = result['known_cells'], result['possible_cells']
    m = len(values[0])
    lower = [max(values[j][b] for j in known) if known else None for b in range(m)]
    gaps, witnesses = [], []
    for a in range(m):
        best = F(0)
        support = sorted(known or [possible[0]])
        comparator = None
        for b in range(m):
            if b == a:
                continue
            for j in possible:
                rival = values[j][b] if lower[b] is None else max(lower[b], values[j][b])
                value = values[j][a]-rival
                if value > best:
                    best, comparator = value, b
                    support = sorted(set(known)|{j})
        worst = [max(values[j][b] for j in support) for b in range(m)]
        if worst[a]-min(worst) != best:
            raise AssertionError('support witness does not attain sharp bound')
        gaps.append(best)
        witnesses.append(dict(support=support, comparator=comparator,
                              worst_losses=list(map(str,worst)),
                              scope='signature-compatible; no original-source witness claimed'))
    result['sharp_improvement_bounds'] = list(map(str,gaps))
    result['sharp_support_witnesses'] = witnesses
    result['sharp_certified_optimal_actions'] = [a for a in range(m) if gaps[a] == 0]
    result['smallest_sharp_gap_action'] = min(range(m),key=lambda a:(gaps[a],a))
    return result
