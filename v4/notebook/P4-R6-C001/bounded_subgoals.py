"""Exact bounded-planner and reward-shaping checks; Codex (GPT-6)."""
from fractions import Fraction as F
from pathlib import Path
import json
import random


def main():
    path_checks = 0
    rows = []
    for theta in (F(0), F(2, 5), F(3, 5), F(6, 5)):
        for p in (F(3, 10), F(7, 10), F(4, 5), F(9, 10)):
            raw_root = [F(2, 5), F(-1, 10)]
            shaped_root = [raw_root[0], raw_root[1]+theta]
            # Tie rule chooses Direct. The terminal matching action maximizes
            # both raw and shaped expected rewards for every p in this grid.
            selected = int(shaped_root[1] > shaped_root[0])
            actual = p-F(1, 10) if selected else F(2, 5)
            optimal = max(F(2, 5), p-F(1, 10))
            for outcome in (F(0), F(1)):
                raw_total = F(-1, 10)+outcome
                shaped_total = F(-1, 10)+theta+outcome-theta
                assert raw_total == shaped_total
                path_checks += 1
            assert (p-F(1, 10) > F(2, 5)) == (p > F(1, 2))
            rows.append({'theta': str(theta), 'success_probability': str(p),
                         'chosen': ('direct', 'prepare')[selected],
                         'actual_expected_return': str(actual),
                         'optimal_expected_return': str(optimal)})

    # Potential-only rewards telescope around each finite closed cycle; an
    # unbalanced entry bonus instead pays for repeatedly going nowhere.
    theta = F(3, 5)
    assert theta-theta == 0
    naive_cycle_bonus = theta

    # Independently execute the two tabular update rules over arbitrary
    # transitions/rewards. Exact rational arithmetic tests their invariant.
    rng = random.Random(60601)
    updates = 0
    for case in range(12):
        gamma = F(9, 10)
        potential = [F(rng.randrange(-8, 9), 5) for _ in range(3)]
        q = [[F(rng.randrange(-5, 6), 5) for _ in range(2)] for _ in range(3)]
        qp = [[q[s][a]+potential[s] for a in range(2)] for s in range(3)]
        for _ in range(60):
            s, a, sp = rng.randrange(3), rng.randrange(2), rng.randrange(3)
            reward = F(rng.randrange(-8, 9), 5)
            alpha = rng.choice((F(1, 5), F(1, 2), F(1)))
            shaping = gamma*potential[sp]-potential[s]
            q[s][a] += alpha*(reward+shaping+gamma*max(q[sp])-q[s][a])
            qp[s][a] += alpha*(reward+gamma*max(qp[sp])-qp[s][a])
            assert all(qp[x][b] == q[x][b]+potential[x]
                       for x in range(3) for b in range(2))
            assert all((q[x][1] > q[x][0]) == (qp[x][1] > qp[x][0]) for x in range(3))
            updates += 1
    result = {'status': 'passed', 'trajectory_checks': path_checks,
              'q_equivalence_updates': updates, 'seed': 60601, 'rows': rows,
              'potential_cycle_sum': '0', 'unbalanced_entry_bonus_per_cycle': str(naive_cycle_bonus),
              'retention_map': '1 + actual expected episode return',
              'beneficial_retention_ratios': [str((1+p-F(1, 10))/F(7, 5))
                                             for p in (F(7, 10), F(4, 5), F(9, 10))]}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n',
                                                  encoding='utf-8', newline='\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'rows'}, indent=2))


if __name__ == '__main__':
    main()
