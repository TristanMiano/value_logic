"""Independent development audit of the frozen integrated scalar v2.1 source.

Contributor: ChatGPT (GPT-6 Astra Pro), independent implementation reviewer.
This script makes no edits to production or preserved historical evidence.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
import dataclasses
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import platform
import sys
import time
import traceback

sys.dont_write_bytecode = True


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def detached(value):
    if isinstance(value, F):
        return ('F', value.numerator, value.denominator)
    if dataclasses.is_dataclass(value):
        return (type(value).__name__, tuple((f.name, detached(getattr(value, f.name)))
                                            for f in dataclasses.fields(value)))
    if isinstance(value, dict):
        return ('dict', tuple(sorted((repr(k), detached(v)) for k, v in value.items())))
    if isinstance(value, (list, tuple)):
        return (type(value).__name__, tuple(map(detached, value)))
    if isinstance(value, (set, frozenset)):
        return (type(value).__name__, tuple(sorted(map(repr, value))))
    if hasattr(value, '__dict__'):
        return (type(value).__name__, detached(vars(value)))
    return value


def norm(values):
    return sum((v * v for v in values), F(0))


def external_features(cfg, p, qs, weight, actions):
    out = tuple(weight * cfg.alpha * (q - p) for q in qs)
    out += tuple(weight * cfg.beta * max(F(0), 1 - abs(cfg.bins * p - j))
                 for j in range(cfg.bins + 1))
    if actions is not None:
        costs = [row[0] + p * (row[1] - row[0]) for row in actions.rows]
        s = min(F(1), max(F(0), F(1, 2) - (costs[1] - costs[0]) / (2 * actions.eta)))
        slopes = [row[1] - row[0] for row in actions.rows]
        mean = (1 - s) * slopes[0] + s * slopes[1]
        out += tuple(weight * cfg.gamma * (mean - d) for d in slopes)
    return out


def score_from(cfg, residual, p, qs, weight, actions):
    phi = external_features(cfg, p, qs, weight, actions)
    return sum((r * v for r, v in zip(residual, phi)), F(0)) + (1 - 2 * p) * norm(phi) / 2


def ceil_sqrt_independent(value, bits):
    """Integer interval search, distinct from production's isqrt formula."""
    scaled_numerator = value.numerator * (1 << (2 * bits))
    denominator = value.denominator
    if scaled_numerator == 0:
        return F(0)
    lo, hi = 0, 1
    while hi * hi * denominator < scaled_numerator:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid * mid * denominator >= scaled_numerator:
            hi = mid
        else:
            lo = mid
    return F(hi, 1 << bits)


class Checks:
    def __init__(self):
        self.count = 0
        self.groups = {}
        self.rejections = []

    def require(self, condition, group, **context):
        self.count += 1
        self.groups[group] = self.groups.get(group, 0) + 1
        if not condition:
            raise AssertionError(json.dumps({'group': group, **context}, default=str))

    def reject_unchanged(self, name, obj, operation):
        before = detached(obj)
        error = None
        try:
            operation()
        except Exception as exc:
            error = {'type': type(exc).__name__, 'message': str(exc)}
        self.require(error is not None and detached(obj) == before,
                     'rejected_call_transactional', name=name, error=error)
        self.rejections.append({'name': name, 'error': error, 'state_unchanged': True})


def run(module, legacy, saved):
    checks = Checks()
    regression = []
    names = ('zero', 'one', 'previous')
    comparable = ('probability', 'expert_values', 'weight', 'features', 'score', 'allowance',
                  'tolerance_met', 'bisections', 'score_evaluations')
    for case in saved['cases']:
        current = module.Forecaster(names, bins=3, scope='legacy-comparison')
        old = legacy.Forecaster(names, bins=3, scope='legacy-comparison')
        for t, y in enumerate(case['outcomes']):
            qs = {'zero': 0, 'one': 1, 'previous': case['outcomes'][t - 1] if t else F(1, 2)}
            weight = (F(1), F(3), F(1, 2))[t % 3]
            a = current.issue(str(t), qs, weight, F(1, 128), 24)
            b = old.issue(str(t), qs, weight, F(1, 128), 24)
            checks.require(all(getattr(a, key) == getattr(b, key) for key in comparable),
                           'legacy_prediction_identity', outcomes=case['outcomes'], round=t)
            checks.require(str(a.probability) == case['trace'][t]['p']
                           and str(a.allowance) == case['trace'][t]['allowance'],
                           'saved_result_identity', outcomes=case['outcomes'], round=t)
            current.reveal(str(t), y, scope='legacy-comparison')
            old.reveal(str(t), y)
            acc = current.accumulator
            checks.require(tuple(old.residual) == acc.residual and old.variance == acc.variance
                           and old.allowance == acc.allowance and old.own_loss == acc.own_loss
                           and tuple(old.expert_losses) == acc.expert_losses,
                           'legacy_accumulator_identity')
        regression.append({'outcomes': case['outcomes'], 'own_loss': str(current.accumulator.own_loss)})

    pair = ('zero', 'one')
    qs = {'zero': 0, 'one': 1}
    invalid = [
        {'query': ''}, {'query': 7}, {'query': []},
        {'experts': None}, {'experts': {'zero': 0}},
        {'experts': {'zero': 0, 'one': 1, 'extra': 0}},
        {'experts': {'zero': -1, 'one': 1}}, {'experts': {'zero': 2, 'one': 1}},
        {'experts': {'zero': True, 'one': 1}}, {'experts': {'zero': 0.5, 'one': 1}},
        {'weight': -1}, {'weight': True}, {'weight': 0.5}, {'weight': '1/0'},
        {'tolerance': 0}, {'tolerance': -1}, {'tolerance': True},
        {'max_bisections': -1}, {'max_bisections': True}, {'max_bisections': 1.5},
        {'actions': 'not-an-action-table'},
    ]
    for index, change in enumerate(invalid):
        args = {'query': 'bad', 'experts': qs, **change}
        for cls, busy in ((module.Forecaster, False), (module.DelayedPool, False), (module.DelayedPool, True)):
            obj = cls(pair)
            if busy:
                obj.issue('pending', qs)
            checks.reject_unchanged(f'{cls.__name__}-issue-{index}-busy={busy}', obj,
                                    lambda: obj.issue(**args))
    for cls in (module.Forecaster, module.DelayedPool):
        for label in (None, -1, 2, False, True, 1.0, F(1), '1'):
            obj = cls(pair)
            obj.issue('label', qs)
            checks.reject_unchanged(f'{cls.__name__}-label-{repr(label)}', obj,
                                    lambda: obj.reveal('label', label, scope=obj.settings.scope))
        obj = cls(pair)
        obj.issue('label', qs)
        for scope in ('wrong-version', '', 7, None):
            checks.reject_unchanged(f'{cls.__name__}-scope-{repr(scope)}', obj,
                                    lambda: obj.reveal('label', 0, scope=scope))
        checks.reject_unchanged(f'{cls.__name__}-unknown', obj,
                                lambda: obj.reveal('other', 0, scope=obj.settings.scope))
        obj.reveal('label', 0, scope=obj.settings.scope)
        checks.reject_unchanged(f'{cls.__name__}-duplicate', obj,
                                lambda: obj.reveal('label', 0, scope=obj.settings.scope))
        checks.reject_unchanged(f'{cls.__name__}-reuse', obj,
                                lambda: obj.issue('label', qs))

    for cls in (module.Forecaster, module.DelayedPool):
        for arguments in ({'experts': ()}, {'experts': ('a', 'a')}, {'experts': ([],)},
                          {'bins': 0}, {'bins': True}, {'scope': ''}, {'scope': 7},
                          {'alpha': 0}, {'beta': -1}, {'gamma': False}, {'decision_features': 1}):
            error = None
            try:
                cls(**{'experts': pair, **arguments})
            except Exception as exc:
                error = type(exc).__name__
            checks.require(error == 'ValueError', 'eager_constructor_validation', arguments=arguments)
    external_names = list(pair)
    f = module.Forecaster(external_names)
    pred = f.issue('detached', qs)
    external_names.append('new')
    f.reveal('detached', 1, scope=f.settings.scope)
    checks.require(f.experts == pair, 'caller_configuration_detached')
    for record, field, value in ((pred, 'probability', F(0)), (f.accumulator, 'settled', 0),
                                 (f.history[0], 'outcome', 0), (f.settings, 'scope', 'edited')):
        checks.reject_unchanged('immutable-' + type(record).__name__, record,
                                lambda: setattr(record, field, value))

    row_input = [[0, 1], [1, 0]]
    table = module.ActionTable(row_input, 1)
    row_input[0][0] = 999
    checks.require(table.rows == ((F(0), F(1)), (F(1), F(0))), 'action_table_detached')
    for rows, eta in (([], 1), ([[0, 1]], 1), ([[0, 1], [1]], 1), ([[0, 1], [1, 0]], 0),
                      ([[0, 1], [1, 0]], True), ([[0, 1], [1, 0]], '1/0'),
                      ([[0, 1.0], [1, 0]], 1)):
        error = None
        try:
            module.ActionTable(rows, eta)
        except Exception as exc:
            error = type(exc).__name__
        checks.require(error == 'ValueError', 'action_table_validation')
    for cls in (module.Forecaster, module.DelayedPool):
        obj = cls(pair, decision_features=True)
        checks.reject_unchanged('missing-action-input', obj, lambda: obj.issue('bad', qs))
        checks.reject_unchanged('bad-action-type', obj, lambda: obj.issue('bad', qs, actions={'rows': []}))
        obj = cls(pair, decision_features=False)
        checks.reject_unchanged('undeclared-actions', obj, lambda: obj.issue('bad', qs, actions=table))

    # Superseded ownership and empty-state precision defects now have direct probes.
    pool = module.DelayedPool(pair)
    pool.issue('owned', qs)
    snapshot = pool.copies[0]
    checks.require(not hasattr(snapshot, 'reveal') and not hasattr(snapshot, 'issue'), 'no_live_copy_handle')
    checks.reject_unchanged('frozen-copy-snapshot', snapshot, lambda: setattr(snapshot, 'pending', None))
    copied_pending = pool.pending
    copied_pending.clear()
    checks.require(pool.pending == {'owned': 0}, 'pending_mapping_detached')
    old_snapshot = detached(snapshot)
    pool.reveal('owned', 0, scope=pool.settings.scope)
    checks.require(detached(snapshot) == old_snapshot and snapshot.accumulator.settled == 0,
                   'copy_snapshot_historical')
    checks.require(pool.audit()['settled'] == 1 and pool.audit()['pending'] == 0, 'owned_coverage')
    for bits in (-1, True, 1.5):
        empty = module.DelayedPool(pair)
        checks.reject_unchanged('empty-invalid-precision', empty, lambda: empty.audit(sqrt_bits=bits))
        checks.reject_unchanged('nonempty-invalid-precision', pool, lambda: pool.audit(sqrt_bits=bits))

    for value, bits in product((F(0), F(1, 3), F(2), F(4), F(17, 257), F(1, 10**10), F(1000001, 7)),
                               (0, 1, 7, 32)):
        upper = module.sqrt_upper(value, bits)
        checks.require(upper == ceil_sqrt_independent(value, bits), 'independent_sqrt_enclosure')
        checks.require(upper * upper >= value and (upper == 0 or (upper - F(1, 1 << bits))**2 < value),
                       'sqrt_enclosure_minimality')
    for lip, tol in product((F(0), F(1, 7), F(1), F(127, 3), F(1000000)), (F(1), F(1, 257))):
        k = module.sufficient_bisections(lip, tol)
        checks.require(lip <= tol * (1 << (k + 1)) and (k == 0 or lip > tol * (1 << k)),
                       'sufficient_bisection_minimality')

    # New action features and certified root work: reconstruct their costs and
    # piecewise score from rows, without using production feature/mix methods.
    action_runs = []
    tables = (((-3, -2), (4, -5)), ((0, 1), (1, 0)), ((2, 3), (2, 3)),
              ((1, 2), (4, 5)), ((10**20, 10**20 + 1), (10**20 + 1, 10**20)))
    for outcomes in product((0, 1), repeat=5):
        f = module.Forecaster(names, bins=3, alpha=F(3, 2), beta=F(2, 3),
                              decision_features=True, gamma=F(5, 4))
        mixed = F(0)
        direct_action_losses = [F(0), F(0)]
        for t, y in enumerate(outcomes):
            q = {'zero': 0, 'one': 1, 'previous': outcomes[t - 1] if t else F(1, 2)}
            w = (F(0), F(1), F(3), F(1, 4), F(2))[t]
            actions = module.ActionTable(tables[t], module.dyadic_eta(t + 1))
            before = f.accumulator.residual
            pred = f.issue(str(t), q, w, F(1, 1024), None, actions)
            phi = external_features(f.settings, pred.probability, pred.expert_values, w, actions)
            checks.require(phi == pred.features and score_from(f.settings, before, pred.probability,
                           pred.expert_values, w, actions) == pred.score, 'decision_features_reconstructed')
            checks.require(pred.tolerance_met and pred.bisections <= pred.sufficient_bisections
                           and (pred.boundary or abs(pred.score) <= pred.tolerance), 'certified_root_contract')
            for possible in (0, 1):
                next_r = [r + (possible - pred.probability) * value for r, value in zip(before, phi)]
                delta = norm(next_r) - norm(before) - pred.probability * (1 - pred.probability) * norm(phi)
                checks.require(delta <= pred.allowance, 'decision_both_outcomes_potential')
            points = {F(k, 16) for k in range(17)} | {F(j, 3) for j in range(4)}
            intercept = actions.rows[1][0] - actions.rows[0][0]
            slope = (actions.rows[1][1] - actions.rows[1][0]) - (actions.rows[0][1] - actions.rows[0][0])
            if slope:
                points |= {p for p in ((actions.eta - intercept) / slope, (-actions.eta - intercept) / slope)
                           if 0 < p < 1}
            points = sorted(points)
            values = [score_from(f.settings, before, p, pred.expert_values, w, actions) for p in points]
            for left, right, sa, sb in zip(points, points[1:], values, values[1:]):
                checks.require(abs(sb - sa) <= pred.lipschitz_bound * (right - left), 'score_lipschitz_probe')
            p = pred.probability
            forecasts = [row[0] + p * (row[1] - row[0]) for row in actions.rows]
            s = min(F(1), max(F(0), F(1, 2) - (forecasts[1] - forecasts[0]) / (2 * actions.eta)))
            forecast_mix = (1 - s) * forecasts[0] + s * forecasts[1]
            checks.require(s == pred.action_one_probability and forecast_mix - min(forecasts) <= actions.eta / 8,
                           'smooth_decision_slack')
            mixed += w * ((1 - s) * actions.rows[0][y] + s * actions.rows[1][y])
            direct_action_losses = [loss + w * actions.rows[i][y] for i, loss in enumerate(direct_action_losses)]
            f.reveal(str(t), y, scope=f.settings.scope)
            checks.require(f.accumulator.mixed_action_loss == mixed
                           and f.accumulator.action_losses == tuple(direct_action_losses), 'direct_action_loss_accounting')
            for own, fixed in ((mixed, loss) for loss in direct_action_losses):
                excess = own - fixed - f.accumulator.smoothing_slack
                checks.require(excess <= 0 or excess * excess * f.settings.gamma**2 <= f.accumulator.bound,
                               'decision_regret_certificate')
        action_runs.append({'outcomes': outcomes, 'mixed_loss': str(mixed),
                            'action_losses': list(map(str, direct_action_losses)),
                            'bound_squared': str(f.accumulator.bound)})

    # Common offsets must change absolute cost while leaving forecasts and regret unchanged.
    offset_pair = [module.Forecaster(pair, decision_features=True) for _ in range(2)]
    offset_total = F(0)
    for t, y in enumerate((0, 1, 1, 0, 0, 1)):
        shift = F(2**128 + t, 3)
        base_rows = ((0, 1), (1, 0))
        shifted_rows = tuple(tuple(F(x) + shift for x in row) for row in base_rows)
        predictions = [f.issue(str(t), qs, t + 1, actions=module.ActionTable(rows, F(1, 4)))
                       for f, rows in zip(offset_pair, (base_rows, shifted_rows))]
        checks.require(predictions[0].probability == predictions[1].probability
                       and predictions[0].features == predictions[1].features, 'common_offset_prediction_invariance')
        for f in offset_pair:
            f.reveal(str(t), y, scope=f.settings.scope)
        offset_total += (t + 1) * shift
    checks.require(offset_pair[1].accumulator.mixed_action_loss - offset_pair[0].accumulator.mixed_action_loss
                   == offset_total, 'common_offset_absolute_cost')

    # Delayed settled subsets, zero weights, explicit scopes, and aggregate bounds.
    pool = module.DelayedPool(names, bins=3, alpha=F(3, 2), beta=F(2, 3),
                              decision_features=True, gamma=F(5, 4), scope='delay-scope')
    issued = {}
    settled = set()
    delayed_reports = []

    def audit_delay():
        residual = [F(0)] * pool.settings.dimension
        direct_loss = total_weight = F(0)
        for query in settled:
            pred, y = issued[query]
            phi = external_features(pool.settings, pred.probability, pred.expert_values, pred.weight, pred.actions)
            residual = [r + (y - pred.probability) * v for r, v in zip(residual, phi)]
            direct_loss += pred.weight * (pred.probability - y)**2
            total_weight += pred.weight
        prior_bound = None
        for bits in (0, 3, 16):
            report = pool.audit(bits)
            copy_bounds = []
            for snapshot in pool.copies:
                bound = F(0)
                for observation in snapshot.history:
                    pred = observation.prediction
                    phi = external_features(pool.settings, pred.probability, pred.expert_values, pred.weight, pred.actions)
                    bound += pred.probability * (1 - pred.probability) * norm(phi) + pred.allowance
                    checks.require(pred.query in settled, 'no_unadmitted_history')
                copy_bounds.append(bound)
            h = sum((ceil_sqrt_independent(b, bits) for b in copy_bounds), F(0))
            cauchy = sum(b > 0 for b in copy_bounds) * sum(copy_bounds, F(0))
            checks.require(report['sum_sqrt_upper'] == h and report['bound_squared'] == min(cauchy, h*h),
                           'delayed_enclosure_reconstructed')
            checks.require(tuple(residual) == report['residual'] and norm(residual) <= report['bound_squared'],
                           'delayed_residual_reconstructed')
            checks.require(report['settled'] == len(settled) and report['pending'] == len(issued) - len(settled)
                           and report['settled_weight'] == total_weight and report['own_loss'] == direct_loss,
                           'settled_coverage_reconstructed')
            checks.require(prior_bound is None or report['bound_squared'] <= prior_bound,
                           'precision_tightens_enclosure')
            prior_bound = report['bound_squared']
        delayed_reports.append(report)

    for t in range(24):
        query = 'delay-' + str(t)
        q = {'zero': 0, 'one': 1, 'previous': F(sum(issued[k][1] for k in settled) + 1, len(settled) + 2)}
        actions = module.ActionTable(tables[t % 5], module.dyadic_eta(t + 1))
        pred = pool.issue(query, q, (F(0), F(1), F(3), F(1, 5))[t % 4], actions=actions)
        issued[query] = (pred, t % 2)
        audit_delay()
        candidates = [t - 3] + ([t - 1] if t % 4 == 0 else [])
        for index in candidates:
            old_query = 'delay-' + str(index)
            if old_query in pool.pending:
                pool.reveal(old_query, issued[old_query][1], scope='delay-scope')
                settled.add(old_query)
                audit_delay()
    for query in tuple(pool.pending):
        pool.reveal(query, issued[query][1], scope='delay-scope')
        settled.add(query)
        audit_delay()

    return {'status': 'PASS', 'checks': checks.count, 'checks_by_group': checks.groups,
            'rejections': checks.rejections, 'legacy_regression': regression,
            'decision_runs': action_runs, 'delayed_reports': delayed_reports,
            'scope': 'Independent finite development checks; no final evaluation or principal time credit.'}


if __name__ == '__main__':
    here = Path(__file__).resolve().parent
    target = here / 'audit_result.json'
    if target.exists():
        raise SystemExit('Refusing to overwrite an existing audit result.')
    source = here / 'scalar_v2_1.py'
    legacy_source = here.parent / 'preserved_rerun_v1/defensive_forecasting.py'
    saved_source = here.parent / 'preserved_rerun_v1/development_result.json'
    module = load('independent_integrated_scalar', source)
    legacy = load('independent_legacy_scalar', legacy_source)
    saved = json.loads(saved_source.read_text())
    start = time.monotonic_ns()
    start_utc = datetime.now(timezone.utc).isoformat()
    try:
        result = run(module, legacy, saved)
    except Exception:
        result = {'status': 'FAIL', 'traceback': traceback.format_exc()}
    production = here.parents[3] / 'checks/06_defensive_forecasting.py'
    result.update({'schema': 'value_logic.p306.independent_integrated_audit_result.v1',
        'start_utc': start_utc, 'end_utc': datetime.now(timezone.utc).isoformat(),
        'execution_ns': time.monotonic_ns() - start, 'python': platform.python_version(),
        'module_version': module.VERSION, 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'production_matches_snapshot': production.read_bytes() == source.read_bytes(),
        'legacy_source_sha256': hashlib.sha256(legacy_source.read_bytes()).hexdigest(),
        'legacy_result_sha256': hashlib.sha256(saved_source.read_bytes()).hexdigest(),
        'audit_source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'contributor': 'ChatGPT (GPT-6 Astra Pro), independent implementation reviewer',
        'research_time_credit_ns': 0})
    target.write_text(json.dumps(result, indent=2, default=str) + '\n')
    print(json.dumps({'status': result['status'], 'checks': result.get('checks'),
                      'execution_ns': result['execution_ns'], 'result': str(target)}))
    raise SystemExit(0 if result['status'] == 'PASS' else 1)
