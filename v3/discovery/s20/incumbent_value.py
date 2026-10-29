"""Incumbent-aware observation bounds; names the baseline explicitly."""
from fractions import Fraction as F
import observation_value as observe
import refinement_gap as refine


def upper_all(values, known, possible, signals):
    m = len(values[0])
    groups = {s:[j for j in possible if signals[j] == s] for s in sorted({signals[j] for j in possible})}
    levels = sorted({v for j in possible for v in values[j]})
    best, witnesses = [None]*m, [None]*m
    inspections = 0
    for t in levels:
        options = {}
        for s,ids in groups.items():
            required = set(known)&set(ids)
            options[s] = []
            for h in range(m):
                allowed = [j for j in ids if values[j][h] <= t]
                if required <= set(allowed):
                    options[s].append((h,allowed))
        if any(not opts for opts in options.values()):
            continue
        for a in range(m):
            candidate, chosen = None, None
            for s,opts in options.items():
                for h,allowed in opts:
                    for j in allowed:
                        inspections += 1
                        if candidate is None or values[j][a] > candidate:
                            candidate,chosen = values[j][a],(s,h,allowed)
            if candidate is None or (best[a] is not None and candidate-t <= best[a]):
                continue
            selected = {s:opts[0] for s,opts in options.items()}
            selected[chosen[0]] = chosen[1:]
            support = sorted({j for _,allowed in selected.values() for j in allowed})
            best[a] = candidate-t
            witnesses[a] = dict(support=support,threshold_after=str(t),
                policy={str(s):h for s,(h,_) in selected.items()},
                scope='signature only; not an original-source witness')
    for a,witness in enumerate(witnesses):
        if witness is None:
            raise AssertionError('nonempty support has no incumbent witness')
        _,after,_ = observe.costs(values,witness['support'],signals)
        before = max(values[j][a] for j in witness['support'])
        if before-after != best[a] or best[a] < 0:
            raise AssertionError('incumbent witness does not attain upper value')
        witness.update(before=str(before),after=str(after))
    return best,witnesses,inspections


def assess(bracket,breakpoints,losses,signals,incumbent,criterion='loss'):
    base = observe.assess(bracket,breakpoints,losses,signals,criterion)
    if type(incumbent) is not int or not 0 <= incumbent < len(losses[0]):
        raise ValueError('valid explicit incumbent action required')
    if base['status'] != 'BOUNDED_OBSERVATION':
        return base
    values = [list(map(F,row)) for row in losses]
    if criterion == 'regret':
        values = [[v-min(row) for v in row] for row in values]
    known,possible = base['known_cells'],base['possible_cells']
    best,witnesses,inspections = upper_all(values,known,possible,signals)
    gaps = refine.assess(bracket,breakpoints,losses,criterion)['sharp_improvement_bounds']
    coarse = [F(g)+F(base['sharp_improvement_upper']) for g in gaps]
    if not all(a <= b for a,b in zip(best,coarse)):
        raise AssertionError('incumbent decomposition bound violated')
    lower = max(F(0),max(values[j][incumbent] for j in known)-F(base['outer_policy_worst_loss'])) if known else F(0)
    return dict(status='BOUNDED_INCUMBENT_OBSERVATION',criterion=criterion,
        incumbent=incumbent,baseline='the stated current action; includes computational suboptimality',
        sharp_improvement_upper=str(best[incumbent]),
        guaranteed_improvement_lower=str(lower),
        all_incumbent_upper_bounds=list(map(str,best)),
        decomposition_upper_bounds=list(map(str,coarse)),
        ideal_baseline_observation_upper=base['sharp_improvement_upper'],
        support_witness=witnesses[incumbent],all_support_witnesses=witnesses,
        implementable_outer_policy=base['implementable_outer_policy'],
        outer_policy_worst_loss=base['outer_policy_worst_loss'],
        inspected_cell_action_options=inspections,
        cost_contract='fixed acquisition plus policy-computation fee must be subtracted separately')
