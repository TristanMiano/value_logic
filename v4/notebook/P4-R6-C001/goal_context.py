"""Contextual goals, adequate codes, and shared facts. Codex (GPT-6)."""
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
import random


def partitions(n):
    def extend(prefix):
        if len(prefix) == n:
            yield tuple(prefix)
        else:
            for value in range(max(prefix)+2):
                yield from extend(prefix+[value])
    yield from extend([0])


def refines(fine, coarse):
    return all(fine[i] != fine[j] or coarse[i] == coarse[j]
               for i in range(len(fine)) for j in range(i))


def graph_checks():
    counts, comparisons = [], 0
    for n in range(1, 6):
        pairs = list(combinations(range(n), 2))
        parts = list(partitions(n))
        coarsest_count = 0
        for mask in range(1 << len(pairs)):
            edges = {pair for bit, pair in enumerate(pairs) if mask & (1 << bit)}
            adjacent = lambda i,j: (min(i,j),max(i,j)) in edges
            adequate = [p for p in parts if all(p[i] != p[j] for i,j in edges)]
            coarsest = [c for c in adequate if all(refines(p,c) for p in adequate)]
            transitive = all(adjacent(i,j) or adjacent(j,k) or not adjacent(i,k)
                             for i in range(n) for j in range(n) for k in range(n))
            assert bool(coarsest) == transitive
            assert len(coarsest) <= 1
            coarsest_count += int(bool(coarsest))
            comparisons += len(parts)
        counts.append({'vertices': n, 'graphs': 1 << len(pairs),
                       'with_coarsest_adequate_partition': coarsest_count})
    return {'graph_counts': counts, 'graph_partition_comparisons': comparisons}


def primitive(t, z, density_constant, density_slope):
    return (density_constant*z*t+(density_slope*z-density_constant)*t*t/2
            -density_slope*t*t*t/3)


def loss(part, mu, exposure, features, constant=F(1), slope=F(0)):
    total, squared, floor = F(0), F(0), F(0)
    goals = len(features)
    for j in range(goals):
        alpha = min(row[j] for row in exposure)
        for cell in range(max(part)+1):
            members = [i for i,p in enumerate(part) if p == cell]
            weights = [mu[i]*exposure[i][j] for i in members]
            weight = sum(weights)
            if weight:
                mean = sum(w*features[j][i] for i,w in zip(members,weights))/weight
                for i,w in zip(members,weights):
                    z = features[j][i]
                    total += w*(primitive(z,z,constant,slope)-primitive(mean,z,constant,slope))
                    squared += w*(z-mean)**2
            unweighted_mean = sum(mu[i]*features[j][i] for i in members)/sum(mu[i] for i in members)
            floor += alpha*sum(mu[i]*(features[j][i]-unweighted_mean)**2 for i in members)
    return total, constant*squared/2, constant*floor/2


def random_checks():
    rng = random.Random(61401)
    checked, zero_loss_checks, nonzero_floor_checks = 0, 0, 0
    for case in range(120):
        n, goals = rng.randint(3,5), 3
        masses = [F(rng.randint(1,9)) for _ in range(n)]
        mu = [x/sum(masses) for x in masses]
        exposure = []
        for _ in range(n):
            raw = [F(rng.randint(1 if case % 2 else 0,8)) for _ in range(goals)]
            if sum(raw) == 0:
                raw[0] = F(1)
            exposure.append([v/sum(raw) for v in raw])
        features = [[F(rng.randint(0,4),4) for _ in range(n)] for _ in range(goals)]
        edges = [(i,j) for i,j in combinations(range(n),2)
                 if any(exposure[i][g]*exposure[j][g] > 0 and features[g][i] != features[g][j]
                        for g in range(goals))]
        for p in partitions(n):
            coloring = all(p[i] != p[j] for i,j in edges)
            for constant,slope in ((F(1),F(0)),(F(1,2),F(1))):
                actual,bound,floor = loss(p,mu,exposure,features,constant,slope)
                assert actual >= bound >= floor >= 0
                assert (actual == 0) == coloring
                if slope == 0:
                    assert actual == bound
                nonzero_floor_checks += int(floor > 0)
                zero_loss_checks += 1
                checked += 1
    return {'seed': 61401, 'models': 120, 'regret_and_bound_checks': checked,
            'coloring_equivalence_checks': zero_loss_checks,
            'positive_exposure_bound_checks': nonzero_floor_checks}


def frontier():
    rows = []
    parts = list(partitions(3))
    mu = [F(1,3)]*3
    features = [[F(0),F(1,2),F(1)],[F(0)]*3]
    for numerator in range(11):
        eps = F(numerator,10)
        alpha, beta = 1-eps/2, eps/2
        exposure = [[alpha,beta],[beta,alpha],[alpha,beta]]
        values = {p:loss(p,mu,exposure,features)[0] for p in parts}
        best = {k:min(v for p,v in values.items() if max(p)+1 == k) for k in (1,2,3)}
        d1,d2 = alpha/12,eps*alpha/48
        assert best == {1:d1,2:d2,3:F(0)}
        for kappa in (F(0),F(1,200),F(1,50),F(1,10)):
            objective = {p:v+kappa*max(p) for p,v in values.items()}
            minimum = min(objective.values())
            chosen = [p for p,v in objective.items() if v == minimum]
            predicted = [k for k,d in best.items() if d+kappa*(k-1) == minimum]
            assert sorted(set(max(p)+1 for p in chosen)) == predicted
            rows.append({'epsilon': str(eps), 'cell_price': str(kappa),
                         'minimum_total_loss': str(minimum), 'cell_counts': predicted,
                         'optimal_partitions': chosen})
    zero_exposure_adequate = [p for p in parts if loss(p,mu,[[F(1),F(0)],[F(0),F(1)],[F(1),F(0)]],features)[0] == 0]
    assert (0,0,1) in zero_exposure_adequate and (0,1,1) in zero_exposure_adequate
    assert not any(all(refines(p,c) for p in zero_exposure_adequate) for c in zero_exposure_adequate)
    return {'settings': rows, 'zero_exposure_adequate_partitions': zero_exposure_adequate,
            'full_retention_threshold_at_price_0_005': '1-sqrt(13/25)'}


def main():
    result = {'status':'passed','graphs':graph_checks(),'regret':random_checks(),'frontier':frontier()}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'frontier'},indent=2))
    print('cost settings',len(result['frontier']['settings']))


if __name__ == '__main__':
    main()
