"""Exact representation reuse frontier. Codex (GPT-6)."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
from goal_geometry import partitions, determines


def main():
    hidden = list(product((0, 1), repeat=3))
    profiles = []
    for c in partitions(8):
        k = max(c)+1
        gross = []
        for g in (0, 1):
            score = F(0)
            for cell in range(k):
                members = [i for i in range(8) if c[i] == cell]
                numerator = sum(1+3*hidden[i][g] for i in members)
                score += F(numerator*numerator, 400*len(members))
            gross.append(score)
        profiles.append((c, k, gross))
    rows = []
    kappa = F(1, 50)
    comparisons = 0
    for alpha in (F(0), F(1,5), F(2,5), F(1,2), F(4,5), F(1)):
        m = min(alpha, 1-alpha)
        gross = [alpha*g[0]+(1-alpha)*g[1] for _, _, g in profiles]
        envelope = {k: max(v for (_, kk, _), v in zip(profiles, gross) if kk == k) for k in range(1, 9)}
        assert envelope[1] == F(1, 8)
        assert envelope[2] == F(1,8)+F(9,200)*max(alpha, 1-alpha)
        assert envelope[3] == F(17,100)-F(9,400)*m
        assert all(envelope[k] == F(17,100) for k in range(4,9))
        for uses in range(1,11):
            values = [uses*v-kappa*(k-1) for (_, k, _), v in zip(profiles, gross)]
            optimum = max(values)
            indices = [i for i, v in enumerate(values) if v == optimum]
            cells = sorted(set(profiles[i][1] for i in indices))
            if m > 0 and uses > kappa/(F(9,400)*m):
                assert cells == [4]
                for i in indices:
                    c = profiles[i][0]
                    assert determines(c, [x[0] for x in hidden])
                    assert determines(c, [x[1] for x in hidden])
            if m == 0:
                assert cells == [2]
            comparisons += len(profiles)
            rows.append({'common_goal_probability': str(alpha), 'uses': uses,
                         'best_total_value': str(optimum), 'optimal_cell_counts': cells,
                         'optimal_partition_count': len(indices)})
    output = {'status': 'passed', 'contract': {'partitions': len(profiles), 'setup_price': str(kappa),
              'cost_paid_once': True, 'known_outcome_law': True, 'implemented_learner': False},
              'exact_partition_comparisons': comparisons, 'settings': rows}
    Path(__file__).with_suffix('.json').write_text(json.dumps(output, indent=2)+'\n', encoding='utf-8',newline='\n')
    print(json.dumps({'status': 'passed', 'exact_partition_comparisons': comparisons, 'settings': len(rows)}))


if __name__ == '__main__':
    main()
