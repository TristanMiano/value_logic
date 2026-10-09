"""Independent formula oracle for the integrated P3-06 action-feature module.

The imported implementation supplies reports; this checker reconstructs every
feature and scored consequence from the announced tables and reports, without
calling the implementation's feature, score, or accumulator-check helpers.
Contributor: ChatGPT (GPT-6 Astra Pro), independent reconstruction reviewer.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import importlib.util
import json
import sys
import time
import traceback


ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / 'v3/checks/06_defensive_forecasting.py'


def run():
    spec = importlib.util.spec_from_file_location('p306_independent_production_target', SOURCE)
    target = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = target
    spec.loader.exec_module(target)
    checks = 0

    def check(statement, message):
        nonlocal checks
        checks += 1
        if not statement:
            raise AssertionError(message)

    def norm2(v):
        return sum((x*x for x in v), F(0))

    alpha, beta, gamma = F(2, 3), F(3, 5), F(5, 7)
    names = ('zero', 'half', 'one')
    qs = (F(0), F(1, 2), F(1))
    tables = (
        ((F(0), F(1)), (F(1), F(-1))),
        ((F(2), F(-1)), (F(0), F(2))),
        ((F(1), F(3)), (F(4), F(-2))),
        ((F(0), F(0)), (F(1), F(0))),
        ((F(-2), F(4)), (F(3), F(-3))),
    )
    weights = (F(1, 2), F(1), F(3, 2), F(0), F(2))

    def independent_features(p, table, w, eta):
        (b0, d0), (b1, d1) = table
        delta = b1-b0+(d1-d0)*p
        s = min(F(1), max(F(0), F(1, 2)-delta/(2*eta)))
        mean_slope = d0+s*(d1-d0)
        features = tuple(w*alpha*(q-p) for q in qs)
        features += tuple(w*beta*max(F(0), 1-2*abs(p-F(j, 2))) for j in range(3))
        features += tuple(w*gamma*(mean_slope-di) for di in (d0, d1))
        return features, s

    def case(ys, cap):
        learner = target.Forecaster(names, bins=2, alpha=alpha, beta=beta,
                                    decision_features=True, gamma=gamma)
        residual = [F(0)]*8
        variance = allowance = own_square = mixture = slack = F(0)
        other_squares, distances = [F(0)]*3, [F(0)]*3
        other_actions, forecast_gaps = [F(0)]*2, [F(0)]*2
        trace = []
        misses = 0
        for t, y in enumerate(ys):
            table, w = tables[t%5], weights[t%5]
            eta = F(1, t+2)
            rows = tuple((b, b+d) for b, d in table)
            actions = target.ActionTable(rows, eta)
            pred = learner.issue(str(t), dict(zip(names, qs)), w, tolerance=F(1, 256),
                                 max_bisections=cap, actions=actions)
            p = pred.probability
            phi, s = independent_features(p, table, w, eta)
            value = sum((r*f for r, f in zip(residual, phi)), F(0))+(1-2*p)*norm2(phi)/2
            added_allowance = 2*max(F(0), (1-p)*value, -p*value)
            check(phi == pred.features, 'Production action and existing feature correspondence.')
            check(s == pred.action_one_probability, 'Production action mixture correspondence.')
            check(value == pred.score and added_allowance == pred.allowance,
                  'Production score and exact both-outcome allowance.')
            if pred.boundary:
                check(added_allowance == 0, 'Valid endpoint allowance.')
            elif cap is None:
                check(abs(value) <= pred.tolerance, 'Certified production root success.')
            check(pred.lipschitz_bound / 2**(pred.sufficient_bisections+1) <= pred.tolerance,
                  'Recorded sufficient root budget.')
            if pred.sufficient_bisections:
                check(pred.lipschitz_bound / 2**pred.sufficient_bisections > pred.tolerance,
                      'Smallest count licensed by recorded Lipschitz bound.')
            if not pred.tolerance_met:
                misses += 1
                check(cap is not None and pred.bisections == cap, 'Honest explicit root exhaustion.')
            for possible_y in (0, 1):
                updated = [r+(possible_y-p)*f for r, f in zip(residual, phi)]
                difference = norm2(updated)-norm2(residual)-p*(1-p)*norm2(phi)
                check(difference == 2*(possible_y-p)*value and difference <= added_allowance,
                      'Independently reconstructed counterfactual increment.')
            residual = [r+(y-p)*f for r, f in zip(residual, phi)]
            variance += p*(1-p)*norm2(phi)
            allowance += added_allowance
            own_square += w*(y-p)**2
            for i, q in enumerate(qs):
                other_squares[i] += w*(y-q)**2
                distances[i] += w*(q-p)**2
            actual_costs = tuple(b+d*y for b, d in table)
            forecast_costs = tuple(b+d*p for b, d in table)
            mix_y = (1-s)*actual_costs[0]+s*actual_costs[1]
            mix_p = (1-s)*forecast_costs[0]+s*forecast_costs[1]
            check(F(0) <= mix_p-min(forecast_costs) <= eta/8, 'Local production action slack.')
            mixture += w*mix_y
            slack += w*eta/8
            for i in (0, 1):
                other_actions[i] += w*actual_costs[i]
                forecast_gaps[i] += w*(mix_p-forecast_costs[i])
            learner.reveal(str(t), y, scope=learner.settings.scope)
            acc = learner.accumulator
            check(acc.residual == tuple(residual) and acc.variance == variance
                  and acc.allowance == allowance, 'Production potential state correspondence.')
            check(acc.own_loss == own_square and acc.expert_losses == tuple(other_squares)
                  and acc.expert_distances == tuple(distances), 'Production expert scoring correspondence.')
            check(acc.mixed_action_loss == mixture and acc.action_losses == tuple(other_actions)
                  and acc.forecast_action_gaps == tuple(forecast_gaps)
                  and acc.smoothing_slack == slack, 'Production decision scoring correspondence.')
            check(norm2(residual) <= variance+allowance, 'Production pathwise potential bound.')
            for i in (0, 1):
                regret = mixture-other_actions[i]
                check(regret == forecast_gaps[i]+residual[6+i]/gamma,
                      'Production changing-table action identity.')
                excess = regret-slack
                check(excess <= 0 or gamma*gamma*excess*excess <= variance+allowance,
                      'Production finite mixed-action regret consequence.')
            trace.append({'p': str(p), 'y': y, 's': str(s), 'root_steps': pred.bisections,
                          'allowance': str(added_allowance), 'tolerance_met': pred.tolerance_met})
        return {'ys': list(ys), 'cap': cap, 'root_misses': misses, 'trace': trace}

    cases = [case(ys, None) for ys in product((0, 1), repeat=5)]
    exhaustion = case((1, 0, 1, 1, 0, 0, 1, 0, 1, 0), 0)
    check(exhaustion['root_misses'] > 0, 'Exhaustion branch actually exercised.')
    # Independent enclosure check used by the new delayed aggregation.
    enclosure_cases = 0
    for value in (F(0), F(1, 1000000), F(2), F(3, 7), F(121, 81)):
        for bits in (0, 1, 8, 32):
            upper = target.sqrt_upper(value, bits)
            check(upper*upper >= value, 'Exact square-root upper enclosure.')
            if upper:
                check((upper-F(1, 2**bits))**2 < value, 'Least dyadic upper enclosure.')
            enclosure_cases += 1
    dyadic_widths = []
    for t in range(1, 257):
        eta = target.dyadic_eta(t, F(3, 7))
        expected = F(3, 7*(2**t.bit_length()))
        check(eta == expected and F(3, 14*(t+1)) <= eta <= F(3, 7*(t+1)),
              'Production dyadic schedule correspondence.')
        if t in (1, 3, 4, 16, 128, 256):
            dyadic_widths.append({'t': t, 'eta': str(eta)})
    return {'status': 'PASS', 'assertions': checks, 'production_version': target.VERSION,
            'binary_sequences': len(cases), 'cases': cases, 'root_exhaustion': exhaustion,
            'enclosure_cases': enclosure_cases, 'dyadic_widths': dyadic_widths,
            'scope': 'Independent finite formula correspondence, not new primary implementation or final evaluation.'}


if __name__ == '__main__':
    start_utc = datetime.now(timezone.utc).isoformat()
    start_ns = time.monotonic_ns()
    source_before = sha256(SOURCE.read_bytes()).hexdigest()
    try:
        result = run()
    except Exception:
        result = {'status': 'FAIL', 'traceback': traceback.format_exc()}
    source_after = sha256(SOURCE.read_bytes()).hexdigest()
    if source_before != source_after:
        result['status'] = 'SOURCE_CHANGED_DURING_REVIEW'
    result.update(start_utc=start_utc, end_utc=datetime.now(timezone.utc).isoformat(),
                  execution_ns=time.monotonic_ns()-start_ns,
                  source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                  reviewed_production_sha256=source_before,
                  production_sha256_after=source_after,
                  principal_research_time_credit_ns=0, subagent_research_effort='unmeasured')
    path = Path(__file__).with_name('production_action_review_probe_result.json')
    if path.exists():
        raise SystemExit('Refusing to overwrite prior review result.')
    path.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: result.get(k) for k in ('status', 'assertions', 'production_version',
                                              'reviewed_production_sha256', 'execution_ns')}))
    raise SystemExit(0 if result['status'] == 'PASS' else 1)
