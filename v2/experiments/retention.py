"""F14 bounded retention challenge; development code, final execution is F15.

Contributor: GPT-6 Astra Pro retention sub-agent, 2026-10-04.
All numerical answers are rational. The native adapter uses the existing K
rules; source/decision calculations are ordinary exact linear programming.
The restricted solvers receive retained payloads, never the scoring law.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations, permutations, product
from math import comb
import hashlib
import json
import random
from time import perf_counter_ns

from v2.checks import f06_inference_rules as K
from v2.checks import f07_soundness as A
from v2.checks import f06_derived_cases as Codec
from v2.verification import case_reference as R
from v2.verification import case_retention as T
from v2.verification import c4_price_revision as C4


WORLDS = tuple(product((0, 1), repeat=3))
ORDERS = tuple(permutations(range(3)))
MOMENT_ORDER = tuple(s for size in range(1, 4) for s in combinations(range(3), size))
TAILORED_RESIDUAL_ORDER = ((1,), (2,), (0, 2), (1, 2))
RETAINED_SCHEMA = 'F14-retained-v2'
METHODS = ('fresh', 'cached_proof', 'full_joint', 'tailored',
           'exact_intervals', 'marginal_diagnostic')
VARIANTS = ('unchanged', 'small_price', 'small_negative_price',
            'large_price', 'large_negative_price', 'proportional',
            'program_edit', 'known_marginals', 'withdrawal', 'source_drift')


def defaults():
    """Root copies these explicitly into the prospective frozen config."""
    return {
        'generator_version': 'F14-retention-v1', 'retained_payload_schema': RETAINED_SCHEMA, 'k': 3,
        'old_prices': ['1', '1', '1'], 'old_penalty': '4',
        'fallback_cost': '5/2', 'small_price_change': '1/40',
        'large_price_change': '1', 'proportional_scale': '2',
        'small_negative_price_change': '-1/40', 'large_negative_price_change': '-1/2',
        'law_integer_weight_min': 1, 'law_integer_weight_max': 17,
        'numeric_tolerance': '1/20', 'decision_regret_tolerance': '1/20',
        'development_seeds': [14101, 14102],
        'variants': list(VARIANTS), 'methods': list(METHODS),
        'access_regimes': ['no_reacquisition', 'adaptive_reacquisition'],
        'acquisition_policy': 'query_if_any_numeric_refusal_or_decision_refusal',
        'acquisition_price_unit': 'one_exact_scalar_measurement',
        'stable_one_price_repair': 'two_new_order_means_for_old_mean_profiles',
        'horizons': [1, 4, 16, 64],
        'acquisition_costs': ['0', '1/20', '1/2'],
        'max_vertex_bases': 70, 'max_proof_steps': 128,
        'maximum_native_retries': 1,
    }


def _json(value):
    return json.dumps(K.serial(value), sort_keys=True, separators=(',', ':'))


def nbytes(value):
    return len(_json(value).encode('utf-8'))


def public_schema(config):
    """One public coordinate layout, charged equally to every method."""
    return {'version': RETAINED_SCHEMA, 'worlds': WORLDS, 'old_orders': ORDERS,
            'full_joint_moment_order': MOMENT_ORDER, 'marginal_order': (0, 1, 2),
            'tailored_profile': {'base_index': 0, 'residual_order': TAILORED_RESIDUAL_ORDER},
            'old_prices': config['old_prices'], 'old_penalty': config['old_penalty']}


def _check_payload_schema(payload):
    if payload.get('schema') != RETAINED_SCHEMA:
        raise ValueError('Unsupported retained payload schema; do not reinterpret old wire data.')


def _tailored_summary(payload):
    _check_payload_schema(payload)
    data = payload['data']
    if set(data) != {'profile'} or len(data['profile']) != 5:
        raise ValueError('A fixed five-value tailored profile is required.')
    values = tuple(map(Q, data['profile']))
    return values[0], dict(zip(TAILORED_RESIDUAL_ORDER, values[1:]))


def _dot(a, b):
    return sum((x*y for x, y in zip(a, b)), Q(0))


def _inverse(matrix):
    n = len(matrix)
    work = [list(map(Q, row))+[Q(i == j) for j in range(n)]
            for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if work[r][col]), None)
        if pivot is None:
            return None
        work[col], work[pivot] = work[pivot], work[col]
        scale = work[col][col]
        work[col] = [x/scale for x in work[col]]
        for r in range(n):
            if r != col:
                scale = work[r][col]
                if scale:
                    work[r] = [x-scale*y for x, y in zip(work[r], work[col])]
    return tuple(tuple(row[n:]) for row in work)


def _reduce(rows, values):
    """RREF equations preserve precisely the retained affine information."""
    matrix = [list(map(Q, row))+[Q(value)] for row, value in zip(rows, values)]
    pivot = 0
    for col in range(8):
        selected = next((r for r in range(pivot, len(matrix)) if matrix[r][col]), None)
        if selected is None:
            continue
        matrix[pivot], matrix[selected] = matrix[selected], matrix[pivot]
        scale = matrix[pivot][col]
        matrix[pivot] = [x/scale for x in matrix[pivot]]
        for r in range(len(matrix)):
            if r != pivot:
                scale = matrix[r][col]
                if scale:
                    matrix[r] = [x-scale*y for x, y in zip(matrix[r], matrix[pivot])]
        pivot += 1
        if pivot == len(matrix):
            break
    if any(not any(row[:8]) and row[8] for row in matrix[pivot:]):
        raise ValueError('Inconsistent retained equations.')
    return (tuple(tuple(row[:8]) for row in matrix[:pivot]),
            tuple(row[8] for row in matrix[:pivot]))


class Fiber:
    """Exact laws p>=0 with retained A p=b; at most C(8,4)=70 bases."""
    def __init__(self, rows=(), values=(), *, max_bases=70):
        self.solver_kind = 'exact_basis_enumeration'
        self.rows, self.values = _reduce(((Q(1),)*8,)+tuple(rows), (Q(1),)+tuple(values))
        self.rank = len(self.rows)
        self.basis_checks = 0
        bases, vertices = [], set()
        for columns in combinations(range(8), self.rank):
            if self.basis_checks >= max_bases:
                raise ValueError('vertex_basis_budget_exhausted')
            self.basis_checks += 1
            inverse = _inverse(tuple(tuple(row[j] for j in columns) for row in self.rows))
            if inverse is None:
                continue
            coordinates = tuple(_dot(row, self.values) for row in inverse)
            if any(x < 0 for x in coordinates):
                continue
            vertex = [Q(0)]*8
            for j, value in zip(columns, coordinates):
                vertex[j] = value
            vertex = tuple(vertex)
            vertices.add(vertex)
            bases.append((columns, inverse, vertex))
        if not vertices:
            raise ValueError('Empty probability-law fiber.')
        self.vertices, self.bases = tuple(sorted(vertices)), tuple(bases)

    @classmethod
    def point(cls, law):
        """Strong full-information control: direct dot products, no needless LP."""
        law = tuple(map(Q, law))
        if len(law) != 8 or min(law) < 0 or sum(law) != 1:
            raise ValueError('Normalized exact eight-world law required.')
        result = object.__new__(cls)
        result.rows = tuple(tuple(Q(i == j) for j in range(8)) for i in range(8))
        result.values, result.rank = law, 8
        result.basis_checks, result.solver_kind = 0, 'direct_joint_dot_products'
        result.vertices = (law,)
        result.bases = ((tuple(range(8)), result.rows, law),)
        return result

    def bounds(self, objective):
        values = tuple(_dot(objective, p) for p in self.vertices)
        return min(values), max(values)

    def maximum_with_dual(self, objective):
        """An optimal basic dual supports the ordinary upper bound."""
        best = None
        for columns, inverse, _ in self.bases:
            weights = tuple(sum((objective[columns[i]]*inverse[i][j]
                                 for i in range(self.rank)), Q(0))
                            for j in range(self.rank))
            slack = tuple(sum((row[j]*w for row, w in zip(self.rows, weights)), Q(0))
                          -objective[j] for j in range(8))
            if any(x < 0 for x in slack):
                continue
            candidate = (_dot(weights, self.values), weights, slack)
            if best is None or candidate < best:
                best = candidate
        if best is None or best[0] != self.bounds(objective)[1]:
            raise AssertionError('Primal/dual mismatch in the bounded exact reference.')
        return best


def _probability_term(coefficients):
    out = K.num(0, 'P')
    for index, value in enumerate(coefficients):
        if value:
            out = K.add(out, K.scale(value, K.src(f'p{index}')))
    return out


def _term(coefficients):
    """Known numeric task prices, normalized to one declared loss unit."""
    return K.convert('probability_to_declared_loss', _probability_term(coefficients))


def native_context(fiber, revision):
    rows = [K.Row(K.scale(-1, K.src(f'p{i}')), K.num(0, 'P')) for i in range(8)]
    for row, value in zip(fiber.rows, fiber.values):
        rows.extend((K.Row(_probability_term(row), K.num(value, 'P')),
                     K.Row(K.scale(-1, _probability_term(row)), K.num(-value, 'P'))))
    # A source-consistency witness must be derived from retained information.
    # Using the hidden scoring law here would leak discarded source information.
    witness = dict(zip((f'p{i}' for i in range(8)), fiber.vertices[0]))
    return K.context(tuple((name, 'P') for name in witness), rows, witness,
                     scope='F14-three-reset-retention-v1', revision=revision,
                     units=('P', 'U'), conversions=(K.Conversion(
                         'probability_to_declared_loss', 'P', 'U', Q(1)),))


def emit_proof(fiber, objective, context, *, max_steps=128):
    bound, weights, slack = fiber.maximum_with_dual(objective)
    builder = K.Builder(context, 'h')
    root = builder.constant(K.num(0, 'P'), K.num(0, 'P'))
    for i, weight in enumerate(weights):
        if weight:
            row = builder.row(8+2*i+int(weight < 0))
            root = builder.add(root, builder.scale(abs(weight), row))
    for i, weight in enumerate(slack):
        if weight:
            root = builder.add(root, builder.scale(weight, builder.row(i)))
    root = builder.conversion('probability_to_declared_loss', root)
    root = builder.rewrite(root, _term(objective), K.num(0))
    root = builder.all_cases((root,))
    proof = builder.proof(root)
    if len(proof.steps) > max_steps:
        return None, bound
    return proof, bound


def _law(rng, config):
    weights = [rng.randint(config['law_integer_weight_min'], config['law_integer_weight_max'])
               for _ in WORLDS]
    return tuple(Q(w, sum(weights)) for w in weights)


@dataclass(frozen=True)
class Case:
    seed: int
    variant: str
    old_law: tuple
    scoring_law: tuple
    prices: tuple
    penalty: Q
    orders: tuple
    revision: str
    facts_live: bool
    known_marginals: tuple


def generate_case(seed, variant, config=None):
    """Generate only when explicitly invoked; F14 invokes development seeds."""
    config = defaults() if config is None else config
    if type(seed) is not int or variant not in VARIANTS:
        raise ValueError('An integer seed and frozen revision variant are required.')
    rng = random.Random(f"{config['generator_version']}:{seed}")
    old = _law(rng, config)
    prices, penalty = list(map(Q, config['old_prices'])), Q(config['old_penalty'])
    orders, live, law = ORDERS, True, old
    if variant in ('small_price', 'large_price', 'small_negative_price', 'large_negative_price'):
        prices[2] += Q(config[f'{variant}_change'])
    elif variant == 'proportional':
        scale = Q(config['proportional_scale'])
        prices, penalty = [x*scale for x in prices], penalty*scale
    elif variant == 'program_edit':
        orders = tuple(permutations(range(3), 2))
    elif variant in ('withdrawal', 'source_drift'):
        live = False
        if variant == 'source_drift':
            law = _law(rng, config)
    marginals = tuple(sum((p for w, p in zip(WORLDS, law) if w[i]), Q(0))
                      for i in range(3)) if variant == 'known_marginals' else ()
    # Binding metadata must not reveal a generator seed that could be used to
    # reconstruct discarded information outside the declared source contract.
    revision = 'source-old' if live else f'source-{variant}'
    return Case(seed, variant, old, law, tuple(prices), penalty, orders, revision, live, marginals)


def _path_vector(order, prices, penalty):
    # This independent path interpreter was already separately tested in F13.
    return tuple(R.execute(world, order, prices, penalty)[0] for world in WORLDS)


def retain(law, method, config):
    law = tuple(map(Q, law))
    if len(law) != 8 or min(law) < 0 or sum(law) != 1 or method not in METHODS:
        raise ValueError('Normalized three-bit law and frozen method required.')
    if config.get('retained_payload_schema', RETAINED_SCHEMA) != RETAINED_SCHEMA:
        raise ValueError('Unsupported retained payload schema in configuration.')
    prices, penalty = tuple(map(Q, config['old_prices'])), Q(config['old_penalty'])
    meta = {'method': method, 'revision': 'old', 'schema': RETAINED_SCHEMA}
    if method in ('fresh', 'cached_proof'):
        data = {'law': list(map(str, law))}
    elif method == 'full_joint':
        data = {'moments': [str(sum((p for w, p in zip(WORLDS, law)
                                   if all(w[i] for i in subset)), Q(0)))
                            for subset in MOMENT_ORDER]}
    elif method == 'tailored':
        base, residuals = T.retain(dict(zip(WORLDS, law)), prices, penalty)
        data = {'profile': [str(base)]+[str(residuals[s]) for s in TAILORED_RESIDUAL_ORDER]}
    elif method == 'exact_intervals':
        data = {'means': [str(_dot(_path_vector(order, prices, penalty), law)) for order in ORDERS]}
    else:
        data = {'marginals': [str(sum((p for w, p in zip(WORLDS, law) if w[i]), Q(0)))
                              for i in range(3)]}
    return {**meta, 'data': data}


def payload_rows(payload, config):
    """Capability boundary: decode retained data without an original law."""
    _check_payload_schema(payload)
    method, data = payload['method'], payload['data']
    if method in ('fresh', 'cached_proof'):
        return tuple(tuple(Q(i == j) for j in range(8)) for i in range(8)), tuple(map(Q, data['law']))
    if method == 'full_joint':
        subsets = MOMENT_ORDER
        return (tuple(tuple(Q(all(w[i] for i in s)) for w in WORLDS) for s in subsets),
                tuple(map(Q, data['moments'])))
    if method == 'marginal_diagnostic':
        return tuple(tuple(Q(w[i]) for w in WORLDS) for i in range(3)), tuple(map(Q, data['marginals']))
    prices, penalty = tuple(map(Q, config['old_prices'])), Q(config['old_penalty'])
    if method == 'tailored':
        summary = _tailored_summary(payload)
        means = tuple(T.recover(summary, order, prices) for order in ORDERS)
    else:
        means = tuple(map(Q, data['means']))
    return tuple(_path_vector(order, prices, penalty) for order in ORDERS), means


class Acquisition:
    """Explicit separate source archive; archive bytes count even when unread."""
    def __init__(self, law):
        self._payload = {'schema': 'F14-exact-law-oracle-v1', 'law': list(map(str, law))}
        self.archive_bytes = nbytes(self._payload)
        self.calls = self.transferred_bytes = 0
        self.scalar_measurements = self.path_world_executions = 0
        self.kinds = []

    def acquire(self):
        self.calls += 1
        self.scalar_measurements += 8
        self.kinds.append('full_eight_world_law')
        self.transferred_bytes += self.archive_bytes
        return tuple(map(Q, self._payload['law']))

    def acquire_means(self, orders, prices, penalty):
        """Only the requested current means cross the acquisition boundary."""
        law = tuple(map(Q, self._payload['law']))
        means = tuple(_dot(_path_vector(order, prices, penalty), law) for order in orders)
        payload = {'schema': 'F14-current-order-means-v1', 'prices': prices, 'penalty': penalty,
                   'orders': orders, 'means': means}
        self.calls += len(orders)
        self.scalar_measurements += len(means)
        self.path_world_executions += 8*len(orders)
        self.transferred_bytes += nbytes(payload)
        self.kinds.append('two_current_order_means')
        return means


def recover_fiber(payload, config, *, facts_live=True, known_marginals=(), oracle=None):
    """No source law is accepted except via the explicit charged capability."""
    if oracle is not None:
        return Fiber.point(oracle.acquire())
    if facts_live:
        _check_payload_schema(payload)
    if facts_live and payload['method'] in ('fresh', 'cached_proof'):
        return Fiber.point(payload['data']['law'])
    if facts_live and payload['method'] == 'full_joint':
        subsets = MOMENT_ORDER
        moments = {(): Q(1), **dict(zip(subsets, map(Q, payload['data']['moments'])))}
        law = C4.invert_moments(moments, 3)
        return Fiber.point(tuple(law[w] for w in WORLDS))
    rows, values = payload_rows(payload, config) if facts_live else ((), ())
    if known_marginals:
        rows += tuple(tuple(Q(w[i]) for w in WORLDS) for i in range(3))
        values += tuple(map(Q, known_marginals))
    return Fiber(rows, values, max_bases=config['max_vertex_bases'])


def repair_from_new_means(payload, old_fiber, means, prices, config):
    """C4 constructive repair from retained old means and exactly two new ones."""
    old_prices = tuple(map(Q, config['old_prices']))
    penalty = Q(config['old_penalty'])
    if payload['method'] == 'tailored':
        summary = _tailored_summary(payload)
    elif payload['method'] == 'exact_intervals':
        # Every compatible law has the same old numeric profile and canonical
        # minimal summary. This vertex is computed from retained data, not truth.
        summary = T.retain(dict(zip(WORLDS, old_fiber.vertices[0])), old_prices, penalty)
    else:
        raise ValueError('A complete retained old mean profile is required.')
    moments = C4.repair_from_chain(summary, old_prices, penalty, prices[-1]-old_prices[-1], means)
    law = C4.invert_moments(moments, 3)
    return Fiber.point(tuple(law[w] for w in WORLDS))


def predictions(fiber, orders, prices, penalty, fallback, tau, epsilon):
    vectors = tuple(_path_vector(order, prices, penalty) for order in orders)
    vectors += ((fallback,)*8,)
    all_orders = tuple(orders)+(None,)
    intervals = tuple(fiber.bounds(v) for v in vectors)
    regrets = worst_regrets(fiber, vectors)
    selected = min(range(len(vectors)), key=lambda j: (regrets[j], intervals[j][1], j))
    refused = regrets[selected] > epsilon
    executed = len(vectors)-1 if refused else selected
    candidate = selected if not refused and selected < len(vectors)-1 else 0
    numeric = [{'order': order, 'lower': str(lo), 'upper': str(hi),
                'status': 'exact' if lo == hi else 'approximate' if hi-lo <= 2*tau else 'refused',
                'estimate': str((lo+hi)/2) if hi-lo <= 2*tau else None}
               for order, (lo, hi) in zip(all_orders[:-1], intervals[:-1])]
    return {
        'numeric': numeric, 'selected': all_orders[selected], 'executed': all_orders[executed],
        'selected_index': selected, 'executed_index': executed,
        'coherent_worst_regret': str(regrets[selected]), 'refused': refused,
        'useful_decision': not refused,
        'decision_status': ('refusal_to_fallback' if refused else
                            'certified_fallback' if all_orders[selected] is None else 'certified_order'),
        'native_candidate_order': all_orders[candidate],
        'native_certificate_role': ('selected_order' if not refused and selected < len(vectors)-1
                                    else 'diagnostic_option_only'),
        'vectors': vectors,
        'candidate_objective': tuple(x-fallback for x in vectors[candidate]),
    }


def worst_regrets(fiber, vectors):
    """Same-law comparisons: max_b max_p (C_a(p)-C_b(p))."""
    if len(fiber.vertices) == 1:
        values = tuple(_dot(v, fiber.vertices[0]) for v in vectors)
        best = min(values)
        return tuple(value-best for value in values)
    return tuple(max(fiber.bounds(tuple(x-y for x, y in zip(a, b)))[1]
                     for b in vectors) for a in vectors)


def _measure(fn):
    start = perf_counter_ns()
    value = fn()
    return value, perf_counter_ns()-start


def _native_result(fiber, objective, context, config, cached=None):
    time_parts = {'cache_check_ns': 0, 'proof_production_ns': 0, 'receipt_check_ns': 0}
    cache_status = 'not_applicable'
    bound = fiber.bounds(objective)[1]
    requested = A.request(context, None, _term(objective), K.num(0), Q(0))
    proof = None
    if cached is not None:
        start = perf_counter_ns()
        try:
            A.receive(context, cached, requested)
            proof, cache_status = cached, 'received'
        except (A.AuditError, K.ProofError):
            cache_status = 'rejected_then_replacement'
        time_parts['cache_check_ns'] = perf_counter_ns()-start
    if proof is None:
        (proof, produced_bound), time_parts['proof_production_ns'] = _measure(
            lambda: emit_proof(fiber, objective, context, max_steps=config['max_proof_steps']))
        if produced_bound != bound:
            raise AssertionError('Native producer failed exact bound agreement.')
    if proof is None:
        status = 'unavailable_budget'
    else:
        start = perf_counter_ns()
        # Always check the theorem actually produced; an insufficient theorem
        # must not be relabeled an accepted zero-budget current request.
        A.receive(context, proof, A.request(context, None, _term(objective), K.num(0), bound))
        if bound <= 0:
            A.receive(context, proof, requested)
            status = 'received'
        else:
            status = 'insufficient_current_request'
        time_parts['receipt_check_ns'] = perf_counter_ns()-start
    return ({'semantic_valid': bound <= 0, 'upper_bound': str(bound), 'status': status,
             'semantic_valid_scope': 'current_retained_or_repaired_probability_fiber',
             'cache': cache_status, 'proof_nodes': 0 if proof is None else len(proof.steps),
             'source_premises_used': 0 if proof is None else len({step.data[0]
                for step in proof.steps if step.rule == 'row'}),
             'proof_bytes': 0 if proof is None else nbytes(Codec.pack_proof(proof)), **time_parts}, proof)


def _run_method(case, method, access, config):
    def produce_payload():
        payload = retain(case.old_law, method, config)
        return payload, nbytes(payload)
    (payload, retained_bytes), production_ns = _measure(produce_payload)
    cached, cached_bytes, cached_context_bytes, initial_native_ns = None, 0, 0, 0
    if method == 'cached_proof':
        start = perf_counter_ns()
        initial_fiber = recover_fiber(payload, config)
        initial_context = native_context(initial_fiber, 'source-old')
        initial_prediction = predictions(initial_fiber, ORDERS, tuple(map(Q, config['old_prices'])),
            Q(config['old_penalty']), Q(config['fallback_cost']), Q(config['numeric_tolerance']),
            Q(config['decision_regret_tolerance']))
        initial_objective = initial_prediction['candidate_objective']
        cached, bound = emit_proof(initial_fiber, initial_objective, initial_context,
                                   max_steps=config['max_proof_steps'])
        if cached is not None:
            A.receive(initial_context, cached, A.request(initial_context, None,
                      _term(initial_objective), K.num(0), bound))
            cached_bytes = nbytes(Codec.pack_proof(cached))
        cached_context_bytes = nbytes(initial_context)
        initial_native_ns = perf_counter_ns()-start
    # All methods have the same priced acquisition capability in this panel.
    # First exhaust the declared retained-data quality criterion. A sufficient
    # full or selective summary never incurs an unnecessary source query.
    if access == 'adaptive_reacquisition':
        oracle, archive_production_ns = _measure(lambda: Acquisition(case.scoring_law))
    elif access == 'no_reacquisition':
        oracle, archive_production_ns = None, 0
    else:
        raise ValueError('Unknown frozen access regime.')
    acquisition_ns = 0
    fiber, solve_ns = _measure(lambda: recover_fiber(payload, config,
        facts_live=case.facts_live, known_marginals=case.known_marginals))
    def decide():
        return predictions(fiber, case.orders, case.prices, case.penalty,
            Q(config['fallback_cost']), Q(config['numeric_tolerance']),
            Q(config['decision_regret_tolerance']))
    result, decision_ns = _measure(decide)
    pre_repair = {'numeric_refusals': sum(row['status'] == 'refused' for row in result['numeric']),
                  'decision_refused': result['refused']}
    if oracle is not None and (pre_repair['numeric_refusals'] or pre_repair['decision_refused']):
        can_repair = (case.facts_live and method in ('tailored', 'exact_intervals')
            and case.variant in ('small_price', 'small_negative_price', 'large_price', 'large_negative_price'))
        if can_repair:
            orders = C4.chain_probe_orders(3)
            means, acquisition_ns = _measure(lambda: oracle.acquire_means(orders, case.prices, case.penalty))
            fiber, repair_solve_ns = _measure(lambda: repair_from_new_means(payload, fiber, means, case.prices, config))
        else:
            acquired, acquisition_ns = _measure(oracle.acquire)
            fiber, repair_solve_ns = _measure(lambda: Fiber.point(acquired))
        solve_ns += repair_solve_ns
        result, repair_decision_ns = _measure(decide)
        decision_ns += repair_decision_ns
    def produce_context():
        context = native_context(fiber, case.revision)
        return context, nbytes(context)
    (context, context_bytes), context_ns = _measure(produce_context)
    (native, _), native_total_ns = _measure(
        lambda: _native_result(fiber, result['candidate_objective'], context, config, cached))
    vectors = result.pop('vectors')
    native_objective = result.pop('candidate_objective')
    actual = tuple(_dot(v, case.scoring_law) for v in vectors)
    scoring_native_value = _dot(native_objective, case.scoring_law)
    regret = actual[result['executed_index']]-min(actual)
    numeric_errors = [None if row['estimate'] is None else str(abs(Q(row['estimate'])-actual[i]))
                      for i, row in enumerate(result['numeric'])]
    for i, row in enumerate(result['numeric']):
        if not Q(row['lower']) <= actual[i] <= Q(row['upper']):
            raise AssertionError('A returned interval excludes the scoring law.')
        if row['estimate'] is not None and abs(Q(row['estimate'])-actual[i]) > Q(config['numeric_tolerance']):
            raise AssertionError('A numerical admission violated its tolerance.')
    if result['useful_decision'] and regret > Q(config['decision_regret_tolerance']):
        raise AssertionError('False useful decision under the declared regret criterion.')
    stages = {'initial_production_ns': production_ns,
              'initial_native_production_and_check_ns': initial_native_ns,
              'source_archive_production_ns': archive_production_ns,
              'acquisition_ns': acquisition_ns, 'update_and_solve_ns': solve_ns,
              'current_context_production_ns': context_ns, 'decision_ns': decision_ns,
              'current_native_protocol_ns': native_total_ns}
    initial_ns = production_ns+initial_native_ns
    update_ns = sum(stages.values())-initial_ns
    arithmetic_ns = archive_production_ns+acquisition_ns+solve_ns+decision_ns
    update_metadata = {'revision': case.revision, 'facts_live': case.facts_live,
                       'known_marginals': case.known_marginals, 'prices': case.prices,
                       'penalty': case.penalty, 'orders': case.orders}
    dimensions = {'fresh': 8, 'cached_proof': 8, 'full_joint': 7, 'tailored': 5,
                  'exact_intervals': 6, 'marginal_diagnostic': 3}
    resource = {**stages, 'initial_total_ns': initial_ns, 'one_update_total_ns': update_ns,
                'one_update_arithmetic_ns': arithmetic_ns,
                'native_substages_ns': {k: native[k] for k in
                    ('cache_check_ns', 'proof_production_ns', 'receipt_check_ns')},
                'retained_payload_bytes': retained_bytes, 'retained_measurement_count': dimensions[method],
                'retained_affine_information_rank': min(dimensions[method], 7) if method != 'exact_intervals' else 5,
                'cached_source_context_bytes': cached_context_bytes, 'cached_proof_bytes': cached_bytes,
                'current_source_context_bytes': context_bytes, 'current_proof_bytes': native['proof_bytes'],
                'current_update_metadata_bytes': nbytes(update_metadata),
                'external_archive_bytes': 0 if oracle is None else oracle.archive_bytes,
                'acquisition_calls': 0 if oracle is None else oracle.calls,
                'acquisition_scalar_measurements': 0 if oracle is None else oracle.scalar_measurements,
                'initial_common_scalar_inputs': 8,
                'current_common_scalar_inputs': len(case.known_marginals),
                'acquisition_path_world_executions': 0 if oracle is None else oracle.path_world_executions,
                'acquisition_kinds': [] if oracle is None else oracle.kinds,
                'acquisition_transferred_bytes': 0 if oracle is None else oracle.transferred_bytes,
                'schema_bytes': nbytes(public_schema(config)),
                'retained_payload_schema': RETAINED_SCHEMA,
                'solver_kind': fiber.solver_kind,
                'fiber_equation_rank': fiber.rank, 'fiber_vertex_count': len(fiber.vertices),
                'basis_checks': fiber.basis_checks, 'peak_basis_candidates': comb(8, fiber.rank),
                'peak_probability_coordinates_per_candidate': 8,
                'stored_feasible_basis_count': len(fiber.bases),
                'inverse_rational_cells_per_basis': fiber.rank**2,
                'native_source_rows': len(context.cases[0].rows),
                'horizon_arithmetic_ns': {str(h): production_ns+h*arithmetic_ns for h in config['horizons']},
                'horizon_compute_ns': {str(h): initial_ns+h*update_ns for h in config['horizons']}}
    resource['resident_bytes'] = (resource['retained_payload_bytes']+cached_context_bytes+cached_bytes)
    resource['resident_plus_archive_bytes'] = resource['resident_bytes']+resource['external_archive_bytes']
    resource['resident_byte_definition'] = 'durable initial payload plus cached old context and proof'
    resource['active_serialized_upper_bytes'] = (resource['resident_bytes']
        +resource['current_source_context_bytes']+resource['current_proof_bytes']
        +resource['current_update_metadata_bytes']+resource['schema_bytes'])
    resource['total_stored_serialized_upper_bytes'] = (resource['active_serialized_upper_bytes']
        +resource['external_archive_bytes'])
    direct_revised_query = case.variant in ('small_price', 'large_price', 'small_negative_price',
                                            'large_negative_price', 'program_edit')
    native['useful_derivation_candidate'] = (direct_revised_query
        and result['native_certificate_role'] == 'selected_order' and native['status'] == 'received'
        and Q(native['upper_bound']) <= -Q(config['numeric_tolerance'])
        and native['source_premises_used'] >= 2)
    native['candidate_order'] = result['native_candidate_order']
    native['certificate_role'] = result['native_certificate_role']
    native['comparison'] = 'candidate_expected_cost_minus_fallback'
    native['requested_budget'] = '0'
    return {'method': method, 'access': access, **result, 'native': native, 'resources': resource,
            'pre_repair': pre_repair,
            'scoring': {'actual_executed_cost': str(actual[result['executed_index']]),
                        'full_information_oracle_best_cost': str(min(actual)),
                        'realized_regret': str(regret), 'numeric_errors': numeric_errors,
                        'full_source_semantic_value': str(scoring_native_value),
                        'full_source_semantic_valid': scoring_native_value <= 0,
                        'full_source_scope': 'exact stipulated current law; scoring/reference information',
                        'oracle_has_native_proof': False,
                        'oracle_information': 'scoring law; differs from selective/no-reacquisition access'},
            'acquisition_sensitivity': [{'per_scalar_measurement_cost': charge,
                'initial_common_source_loss': str(8*Q(charge)),
                'current_common_source_loss': str(len(case.known_marginals)*Q(charge)),
                'method_specific_acquisition_loss': str(Q(charge)
                    *(0 if oracle is None else oracle.scalar_measurements)),
                'decision_plus_acquisition_loss': str(actual[result['executed_index']]
                    +Q(charge)*(len(case.known_marginals)
                               +(0 if oracle is None else oracle.scalar_measurements))),
                'horizon_decision_plus_source_loss': {str(h): str(8*Q(charge)+h*(
                    actual[result['executed_index']]+Q(charge)*(len(case.known_marginals)
                        +(0 if oracle is None else oracle.scalar_measurements))))
                    for h in config['horizons']}}
                for charge in config['acquisition_costs']]}


def run_case(case, config=None, *, generation_ns=None):
    config = defaults() if config is None else config
    start = perf_counter_ns()
    old_input = {'schema': 'F14-old-exact-source-input-v1', 'law': case.old_law}
    current_truth = {'schema': 'F14-scorer-current-law-v1', 'law': case.scoring_law}
    current_facts = {'revision': case.revision, 'facts_live': case.facts_live,
                     'known_marginals': case.known_marginals}
    current_query = {'prices': case.prices, 'penalty': case.penalty, 'orders': case.orders,
                     'fallback': config['fallback_cost']}
    common = {'old_source_input_bytes': nbytes(old_input),
              'scorer_only_current_truth_bytes': nbytes(current_truth),
              'current_shared_source_facts_bytes': nbytes(current_facts),
              'current_shared_query_bytes': nbytes(current_query),
              'old_source_scalar_inputs': 8, 'current_shared_scalar_inputs': len(case.known_marginals)}
    common['input_serialization_ns'] = perf_counter_ns()-start
    common['generation_ns'] = generation_ns
    common['observed_common_production_ns'] = common['input_serialization_ns']+(generation_ns or 0)
    common['generation_observed'] = generation_ns is not None
    common['charge'] = 'once per case; identical common charge to every method/access arm'
    common['scope'] = ('synthetic input/generator production, including current truth and exact marginals; '
                       'not real sampling, workload acquisition, or deployable source-estimation cost')
    methods = [_run_method(case, method, access, config)
               for access in config['access_regimes'] for method in config['methods']]
    for item in methods:
        resource = item['resources']
        resource['one_case_method_plus_common_ns'] = (common['observed_common_production_ns']
            +resource['initial_total_ns']+resource['one_update_total_ns'])
        resource['horizon_compute_plus_common_ns'] = {str(h): common['observed_common_production_ns']
            +resource['horizon_compute_ns'][str(h)] for h in config['horizons']}
        resource['initial_with_supplied_source_serialized_upper_bytes'] = (resource['resident_bytes']
            +common['old_source_input_bytes']+resource['schema_bytes'])
        resource['peak_serialized_working_state_upper_bytes'] = max(
            resource['initial_with_supplied_source_serialized_upper_bytes'],
            resource['active_serialized_upper_bytes'])
    comparisons = []
    for access in config['access_regimes']:
        fresh = next((x for x in methods if x['method'] == 'fresh' and x['access'] == access), None)
        if fresh is None:
            continue
        f = fresh['resources']
        for item in (x for x in methods if x['access'] == access):
            r = item['resources']
            extra_setup = r['initial_total_ns']-f['initial_total_ns']
            saving = f['one_update_total_ns']-r['one_update_total_ns']
            # Strict win I_method+h U_method < I_fresh+h U_fresh.
            threshold = (max(1, extra_setup//saving+1) if saving > 0 else
                         1 if saving == 0 and extra_setup < 0 else None)
            comparisons.append({'method': item['method'], 'access': access,
                'extra_setup_ns': extra_setup, 'per_update_saving_ns': saving,
                'steady_repeated_update_break_even': threshold,
                'horizon_wins': {str(h): r['horizon_compute_ns'][str(h)] < f['horizon_compute_ns'][str(h)]
                                 for h in config['horizons']},
                'scope': 'single measured update extrapolated; not repeated-update runtime evidence'})
    return {'seed': case.seed, 'variant': case.variant,
            'case_hash': hashlib.sha256(_json(case).encode()).hexdigest(),
            'facts_live': case.facts_live, 'common_input_accounting': common,
            'methods': methods, 'break_even': comparisons}


def run_generated_case(seed, variant, config=None):
    """Execute one generated episode, measuring common source/input production."""
    config = defaults() if config is None else config
    case, generation_ns = _measure(lambda: generate_case(seed, variant, config))
    return run_case(case, config, generation_ns=generation_ns)


def run_development(config=None):
    config = defaults() if config is None else config
    return {'split': 'development', 'generator_version': config['generator_version'],
            'cases': [run_generated_case(seed, variant, config)
                      for seed in config['development_seeds'] for variant in config['variants']],
            'claim': 'implementation validation only; no final empirical conclusion'}


def development_sentinels():
    """Permanent development fixtures for distinct logical boundary failures."""
    config = defaults()
    uniform = (Q(1, 8),)*8
    payload = retain(uniform, 'fresh', config)
    fiber = recover_fiber(payload, config)
    old = native_context(fiber, 'sentinel-old')
    new = native_context(fiber, 'sentinel-new')
    objective = tuple(x-Q(5, 2) for x in _path_vector(ORDERS[0], (Q(1),)*3, Q(4)))
    proof, bound = emit_proof(fiber, objective, old)
    A.receive(old, proof, A.request(old, None, _term(objective), K.num(0), 0))
    rejected = {}
    for name, context, query in (
        ('stale_revision', new, objective),
        ('changed_current_pair', old, tuple(x-Q(5, 2) for x in
             _path_vector(ORDERS[0], (Q(1), Q(1), Q(41, 40)), Q(4))))):
        try:
            A.receive(context, proof, A.request(context, None, _term(query), K.num(0), 0))
        except (A.AuditError, K.ProofError):
            rejected[name] = True
        else:
            raise AssertionError(f'{name} was accepted.')
    limited, limit_bound = emit_proof(fiber, objective, old, max_steps=0)
    if limited is not None or limit_bound > 0:
        raise AssertionError('Search/production refusal did not preserve semantic validity.')
    x = K.src('x')
    conversions = (K.Conversion('p_to_l', 'P', 'L', Q(1)),
                   K.Conversion('p_to_a', 'P', 'A', Q(1)))
    inaccessible = K.context((('x', 'P'),), (
        K.Row(K.num(0, 'P'), x), K.Row(x, K.num(1, 'P')),
        K.Row(K.convert('p_to_a', x), K.num(0, 'A'))), {'x': Q(0)},
        scope='F14-unreachable-unit-development', revision='1',
        units=('P', 'L', 'A'), conversions=conversions)
    builder = K.Builder(inaccessible, 'h')
    root = builder.conversion('p_to_l', builder.row(1))
    root = builder.rewrite(root, K.convert('p_to_l', x), K.num(0, 'L'))
    root = builder.all_cases((root,))
    inaccessible_proof = builder.proof(root)
    A.receive(inaccessible, inaccessible_proof, A.request(inaccessible, None,
        K.convert('p_to_l', x), K.num(0, 'L'), 1, 'L'))
    try:
        A.receive(inaccessible, inaccessible_proof, A.request(inaccessible, None,
            K.convert('p_to_l', x), K.num(0, 'L'), 0, 'L'))
    except A.AuditError:
        pass
    else:
        raise AssertionError('An unreachable-unit bound was treated as a native zero proof.')
    return {'split': 'permanent_development', 'old_bound': str(bound), **rejected,
            'budget_limited_valid_request': limited is None,
            'unreachable_unit': {'full_source_maximum': '0', 'target_reduct_maximum': '1',
                'full_source_valid': True, 'native_zero_unavailable': True,
                'target_reduct_countermodel': {'x': '1'},
                'current_zero_receipt_rejected': True}}
