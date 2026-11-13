"""Exact sensor value and provision game; Codex (GPT-6), 2026-11-12."""
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path

from goal_geometry import trade_payoff


def sensor_advantage(error):
    law = ((Q(0), Q(1), Q(1)),)
    informed = Q(0)
    uninformed = Q(0)
    for hazard, report in product((0, 1), repeat=2):
        probability = Q(1, 2)*(1-error if hazard == report else error)
        forecast = 1-error if report else error
        informed += probability*trade_payoff(Q(hazard), forecast, law)
        uninformed += probability*trade_payoff(Q(hazard), Q(1, 2), law)
    return informed-uninformed


def game_payoff(contributions, benefits, cost):
    if sum(contributions) < cost:
        return (Q(0), Q(0))
    return tuple(b-c for b, c in zip(benefits, contributions))


def equilibria(benefits, cost):
    choices = (Q(0), cost/2, cost)
    result = []
    for profile in product(choices, repeat=2):
        payoff = game_payoff(profile, benefits, cost)
        if all(game_payoff(tuple(choice if k == agent else profile[k]
                                 for k in range(2)), benefits, cost)[agent] <= payoff[agent]
               for agent in range(2) for choice in choices):
            result.append({'contributions': list(map(str, profile)),
                           'payoffs': list(map(str, payoff)),
                           'provided': sum(profile) >= cost})
    return result


def main():
    rows = []
    for error in (Q(0), Q(1, 10), Q(1, 4), Q(1, 2)):
        gain = sensor_advantage(error)
        assert gain == (1-2*error)**2/8
        for uses in (1, 2, 4):
            benefit = uses*gain/2
            cost = Q(1, 10)
            rows.append({'error': str(error), 'uses': uses,
                         'benefit_per_agent': str(benefit),
                         'coalition_surplus': str(2*benefit-cost),
                         'strict_sequential_provision': benefit > cost/2,
                         'simultaneous_equilibria': equilibria((benefit, benefit), cost)})
    assert rows[0]['strict_sequential_provision']
    assert {r['provided'] for r in rows[0]['simultaneous_equilibria']} == {False, True}
    assert not rows[3]['strict_sequential_provision']
    assert rows[4]['strict_sequential_provision']
    result = {'status': 'passed', 'rows': rows,
              'scope': 'Finite contribution choices; the zero-contribution equilibrium proof also covers continuous contributions.'}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2)+'\n',
                                                  encoding='utf-8', newline='\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
