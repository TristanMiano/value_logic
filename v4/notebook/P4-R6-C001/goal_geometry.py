"""Exact practical-goal checks for R6.1; Codex (GPT-6), 2026-11-12.

Forward-integrate realized trade payoffs, then compare with the proposed
quadratic bound. Enumerate every partition of the eight-context shared-hazard
world. This is finite evidence, not a substitute for the general proof.
"""
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path


def simplex(denominator):
    for a in range(denominator + 1):
        for b in range(denominator + 1 - a):
            yield (Q(a, denominator), Q(b, denominator),
                   Q(denominator-a-b, denominator))


def dot(left, right):
    return sum((a*b for a, b in zip(left, right)), Q(0))


def trade_payoff(outcome_value, forecast_value, price_law):
    """Integrate the payoff of the forecast's buy/decline rule by price piece."""
    total = Q(0)
    for low, high, density in price_law:
        end = min(high, forecast_value)
        if end > low:
            total += density*(outcome_value*(end-low)-(end*end-low*low)/2)
    return total


def score(truth, forecast, contracts):
    return sum((weight * sum((truth[y]*trade_payoff(values[y], dot(forecast, values), law)
                              for y in range(len(truth))), Q(0))
                for weight, values, law in contracts), Q(0))


def quadratic(truth, forecast, contracts):
    return sum((weight*min(piece[2] for piece in law)
                *(dot(truth, values)-dot(forecast, values))**2/2
                for weight, values, law in contracts), Q(0))


def partitions(size):
    def append(prefix):
        if len(prefix) == size:
            yield tuple(prefix)
            return
        for label in range(max(prefix)+2):
            yield from append(prefix+[label])
    yield from append([0])


def determines(labels, target):
    return all(labels[i] != labels[j] or target[i] == target[j]
               for i in range(len(labels)) for j in range(i))


def common_partition(required):
    size = len(required[0])
    components = list(range(size))
    for labels in required:
        for i in range(size):
            for j in range(i):
                if labels[i] == labels[j]:
                    old, new = components[i], components[j]
                    components = [new if value == old else value for value in components]
    names = {}
    return tuple(names.setdefault(value, len(names)) for value in components)


def representation_values(labels, contexts):
    law = ((Q(0), Q(1), Q(1)),)
    members = {label: [i for i, value in enumerate(labels) if value == label]
               for label in set(labels)}
    values = []
    for feature in range(3):
        total = Q(0)
        for indices in members.values():
            forecast = Q(sum(contexts[i][feature] for i in indices), len(indices))
            total += sum((trade_payoff(Q(contexts[i][feature]), forecast, law)
                          for i in indices), Q(0))/len(contexts)
        values.append(total)
    return tuple(values)


def main():
    features = ((Q(1, 5), (Q(0), Q(1), Q(0))),
                (Q(2, 5), (Q(-1), Q(0), Q(2))),
                (Q(2, 5), (Q(1, 2), Q(1), Q(3, 2))))
    contracts = {}
    for kind in ('uniform', 'piecewise'):
        rows = []
        for weight, values in features:
            low, high = min(values), max(values)
            width, middle = high-low, (low+high)/2
            law = ((low, high, 1/width),) if kind == 'uniform' else (
                (low, middle, 1/(2*width)), (middle, high, 3/(2*width)))
            assert sum((density*(b-a) for a, b, density in law), Q(0)) == 1
            rows.append((weight, values, law))
        contracts[kind] = rows
    grid = list(simplex(6))
    checks = {}
    for kind, rows in contracts.items():
        count = 0
        for truth, forecast in product(grid, repeat=2):
            regret = score(truth, truth, rows)-score(truth, forecast, rows)
            bound = quadratic(truth, forecast, rows)
            assert regret >= bound >= 0
            if kind == 'uniform':
                assert regret == bound
            assert (regret == 0) == (truth == forecast)
            count += 1
        checks[kind] = count

    feature = (Q(1), Q(0))
    truth, forecast = (Q(3, 5), Q(2, 5)), (Q(2, 5), Q(3, 5))
    gap_law = ((Q(0), Q(1, 4), Q(2)), (Q(3, 4), Q(1), Q(2)))
    gap_rows = [(Q(1), feature, gap_law)]
    uniform_rows = [(Q(1), feature, ((Q(0), Q(1), Q(1)),))]
    gap_regret = score(truth, truth, gap_rows)-score(truth, forecast, gap_rows)
    repaired_regret = score(truth, truth, uniform_rows)-score(truth, forecast, uniform_rows)
    assert gap_regret == 0 and repaired_regret == Q(1, 50)
    null_truth, null_forecast = (Q(1, 4), Q(1, 4), Q(1, 2)), (Q(1, 4), Q(1, 2), Q(1, 4))
    null_rows = [(Q(1), (Q(1), Q(0), Q(0)), ((Q(0), Q(1), Q(1)),))]
    assert score(null_truth, null_truth, null_rows) == score(null_truth, null_forecast, null_rows)

    contexts = list(product((0, 1), repeat=3))
    required = [tuple((h, a) for h, a, b in contexts),
                tuple((h, b) for h, a, b in contexts)]
    common = common_partition(required)
    hazard = tuple(h for h, a, b in contexts)
    assert determines(common, hazard) and determines(hazard, common)
    private_common = common_partition([tuple(a for h, a, b in contexts),
                                       tuple(b for h, a, b in contexts)])
    assert len(set(private_common)) == 1
    assert len(set(zip(*required))) == 8
    support_specific = common_partition([(0, 1, 2), (0, 1, 4)])
    assert len(set(support_specific)) == 3

    profiles = {'agent_1': (Q(1, 2), Q(1, 2), Q(0)),
                'agent_2': (Q(1, 2), Q(0), Q(1, 2)),
                'joint_payoff': (Q(1), Q(1, 2), Q(1, 2))}
    frontier = {name: {} for name in profiles}
    all_rows = []
    count, adequacy_checks = 0, 0
    for labels in partitions(8):
        values = representation_values(labels, contexts)
        for i in range(2):
            name = 'agent_'+str(i+1)
            achieved = dot(profiles[name], values)
            assert (achieved == Q(1, 4)) == determines(labels, required[i])
            adequacy_checks += 1
        cells = len(set(labels))
        for name, weights in profiles.items():
            achieved = dot(weights, values)
            previous = frontier[name].get(cells)
            if previous is None or achieved > previous['value']:
                frontier[name][cells] = {'value': achieved, 'labels': labels, 'ties': 1,
                                        'all_best_determine_H': determines(labels, hazard)}
            elif achieved == previous['value']:
                previous['ties'] += 1
                previous['all_best_determine_H'] &= determines(labels, hazard)
        all_rows.append((labels, values))
        count += 1
    assert count == 4140 and adequacy_checks == 8280
    chosen = {}
    for cost in (Q(1, 200), Q(1, 100), Q(1, 50), Q(1, 20), Q(1, 10), Q(1, 5)):
        best = max(dot(profiles['joint_payoff'], values)-cost*(len(set(labels))-1)
                   for labels, values in all_rows)
        winners = [labels for labels, values in all_rows
                   if dot(profiles['joint_payoff'], values)-cost*(len(set(labels))-1) == best]
        chosen[str(cost)] = {'net_joint_payoff': str(best),
                             'best_cell_counts': sorted({len(set(labels)) for labels in winners}),
                             'optimal_partitions': len(winners),
                             'all_best_determine_H': all(determines(labels, hazard) for labels in winners),
                             'one_optimal_partition': winners[0]}
    encoded_frontier = {
        name: {str(k): {**row, 'value': str(row['value']),
                       'gain_over_constant': str(row['value']-dot(weights, (Q(1, 8),)*3))}
               for k, row in sorted(frontier[name].items())}
        for name, weights in profiles.items()}
    output = {'author': 'Codex (GPT-6)', 'cycle': 'P4-R6-C001', 'status': 'passed',
              'scope': 'exact finite payoff and partition checks; no general theorem or empirical prevalence claim',
              'three_outcome_forecast_pairs': checks,
              'price_gap_regret': str(gap_regret), 'repaired_price_regret': str(repaired_regret),
              'feature_nullspace_witness': {'truth': list(map(str, null_truth)),
                                           'forecast': list(map(str, null_forecast)), 'regret': '0'},
              'contexts_H_A_B': contexts, 'partitions_checked': count,
              'individual_adequacy_checks': adequacy_checks,
              'required_common_partition': common, 'pooled_cells': 8,
              'private_only_common_cells': 1, 'support_specific_common_cells': 3,
              'gross_frontiers': encoded_frontier, 'costly_joint_representation': chosen}
    destination = Path(__file__).with_suffix('.json')
    destination.write_text(json.dumps(output, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({'status': 'passed', 'forecast_pair_checks': checks,
                      'partitions_checked': count, 'adequacy_checks': adequacy_checks,
                      'costly_joint_representation': chosen}, indent=2))


if __name__ == '__main__':
    main()
