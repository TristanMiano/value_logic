"""Finite robust observation value under incomplete cell support."""
from fractions import Fraction as F
import decision_cells as cells


def costs(values, support, signals):
    m = len(values[0])
    baseline = min(max(values[j][a] for j in support) for a in range(m))
    policy, branch = {}, []
    for s in sorted({signals[j] for j in support}):
        local = [j for j in support if signals[j] == s]
        losses = [max(values[j][a] for j in local) for a in range(m)]
        a = min(range(m),key=lambda a:(losses[a],a))
        policy[s] = a
        branch.append(losses[a])
    return baseline, max(branch), policy


def upper(values, known, possible, signals):
    m = len(values[0])
    groups = {s:[j for j in possible if signals[j] == s] for s in sorted({signals[j] for j in possible})}
    thresholds = sorted({v for j in possible for v in values[j]})
    full = (1 << m)-1
    best, witness = None, None
    transitions = 0
    for t in thresholds:
        for b in thresholds:
            if b < t or (best is not None and b-t <= best):
                continue
            states = {0:[]}
            for s,ids in groups.items():
                required = set(known)&set(ids)
                options = []
                for h in range(m):
                    allowed = [j for j in ids if values[j][h] <= t]
                    if not required <= set(allowed):
                        continue
                    mask = sum(1 << a for a in range(m) if any(values[j][a] >= b for j in allowed))
                    options.append((mask,s,h,allowed))
                following = {}
                for mask,path in states.items():
                    for add,s,h,allowed in options:
                        transitions += 1
                        following.setdefault(mask|add,path+[(s,h,allowed)])
                states = following
                if not states:
                    break
            if full in states:
                best = b-t
                chosen = states[full]
                support = sorted({j for _,_,allowed in chosen for j in allowed})
                witness = dict(support=support,threshold_before=str(b),threshold_after=str(t),
                               policy={str(s):h for s,h,_ in chosen})
    if best is None:
        raise AssertionError('a nonempty support should make some threshold pair feasible')
    before,after,_ = costs(values,witness['support'],signals)
    if before-after != best:
        raise AssertionError('threshold witness does not attain final upper value')
    witness.update(before=str(before),after=str(after),scope='signature only; not an original-source witness')
    return best,witness,transitions


def assess(bracket,breakpoints,losses,signals,criterion='loss'):
    result = cells.assess(bracket,breakpoints,losses,criterion)
    if len(signals) != len(losses) or any(type(s) is not int or s < 0 for s in signals):
        raise ValueError('one nonnegative integer signal per cell required')
    if result['status'] != 'BOUNDED_DECISION':
        return result
    values = [list(map(F,row)) for row in losses]
    if criterion == 'regret':
        values = [[v-min(row) for v in row] for row in values]
    known,possible = result['known_cells'],result['possible_cells']
    bp,qp,policy = costs(values,possible,signals)
    if known:
        bk,qk,_ = costs(values,known,signals)
        lower = max(F(0),bk-qp)
    else:
        qk = min(v for j in possible for v in values[j])
        lower = F(0)
    sharp,witness,transitions = upper(values,known,possible,signals)
    return dict(status='BOUNDED_OBSERVATION',criterion=criterion,
        assumes_nonempty_source=not bool(known),known_cells=known,possible_cells=possible,
        guaranteed_improvement_lower=str(lower),coarse_improvement_upper=str(bp-qk),
        sharp_improvement_upper=str(sharp),support_witness=witness,
        implementable_outer_policy={str(s):a for s,a in policy.items()},
        outer_policy_worst_loss=str(qp),dp_transitions=transitions,
        cost_contract='fixed acquisition fee must be subtracted separately')
