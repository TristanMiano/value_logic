#!/usr/bin/env python3
"""Fixed Option-B development inputs and an independent scalar reference.

Contributor: ChatGPT (GPT-6 Astra Pro), integration reviewer, 2026-10-10.
R-P3-B-B DEVELOPMENT only. Exactly four streams and six current requests per
stream. No random generation, policy execution or benchmark runs at import.

Frame/Request identities reuse the inherited shared module names. The scalar
reference evaluates the admitted expression grammar directly, without calling
ADD, interval, portfolio, or certificate-verifier evaluation. Reference output
is an exhaustive development diagnostic, not itself a portable certificate.
If a deployed exact-table control uses it, its source and execution must be paid.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from typing import Any
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
_NAME = '_p305_portfolio_base'
if _NAME in sys.modules:
    M = sys.modules[_NAME]
else:
    _spec = importlib.util.spec_from_file_location(
        _NAME, Path(__file__).with_name('05_counterfactual_transport.py'))
    if _spec is None or _spec.loader is None:
        raise ImportError('Missing unchanged P3-05 Frame dependency.')
    M = importlib.util.module_from_spec(_spec)
    sys.modules[_NAME] = M
    _spec.loader.exec_module(M)
K = M.K
if sys.modules.get('_p305_inherited_p304') is not K:
    raise ImportError('Inherited grammar module identity is inconsistent.')

VERSION = 'rp3bb-certificate-cases-v1'
SCHEMA = 'value_logic.rp3bb.certificate_delivery_cases.v1'
COVERAGE = 'ENTIRE_CURRENT_INCUMBENT_SUBLEVEL_INCLUDING_ALL_MINIMIZERS'
UNIT = 'declared-loss-unit'


def _point(point: Any, nbits: int) -> tuple[int, ...]:
    if (type(point) is not tuple or len(point) != nbits
            or any(type(b) is not int or b not in (0, 1) for b in point)):
        raise ValueError('A complete immutable integer-bit assignment is required.')
    return point


@dataclass(frozen=True)
class Case:
    name: str
    frame: Any
    witness: tuple[int, ...]
    bound: F
    named_witnesses: tuple[tuple[str, tuple[int, ...]], ...] = ()

    def __post_init__(self):
        if type(self.name) is not str or not self.name:
            raise ValueError('A nonempty fixed case name is required.')
        if type(self.frame) is not M.Frame:
            raise ValueError('The shared inherited Frame type is required.')
        self.frame.__post_init__()
        _point(self.witness, self.frame.request.nbits)
        object.__setattr__(self, 'bound', K.rational(self.bound))
        if type(self.named_witnesses) is not tuple:
            raise ValueError('Named development witnesses must be immutable.')
        names = set()
        for row in self.named_witnesses:
            if type(row) is not tuple or len(row) != 2:
                raise ValueError('Malformed named development witness.')
            name, point = row
            if type(name) is not str or not name or name in names:
                raise ValueError('Named witnesses must have distinct nonempty names.')
            names.add(name)
            _point(point, self.frame.request.nbits)

    @property
    def handle(self) -> str:
        """Stable distinct admission handle for an old case, when used as one."""
        return self.name

    def record(self) -> dict:
        current = self.frame.record()
        return {
            'name': self.name,
            'frame': json.loads(current),
            'current_record': current,
            'witness': list(self.witness),
            'bound': [self.bound.numerator, self.bound.denominator],
            'bound_text': str(self.bound),
            'named_witnesses': [
                {'name': name, 'assignment': list(point)}
                for name, point in self.named_witnesses],
        }


@dataclass(frozen=True)
class Stream:
    name: str
    nbits: int
    order: tuple[int, ...]
    old: tuple[Case, ...]
    edits: tuple[Case, ...]
    protected_free_bit: int | None = None

    def __post_init__(self):
        if type(self.name) is not str or not self.name:
            raise ValueError('A fixed stream name is required.')
        if type(self.nbits) is not int or not 1 <= self.nbits <= 10:
            raise ValueError('The declared finite bit cap is 1 through 10.')
        if (type(self.order) is not tuple
                or any(type(i) is not int for i in self.order)
                or tuple(sorted(self.order)) != tuple(range(self.nbits))):
            raise ValueError('The complete immutable variable order is required.')
        if type(self.old) is not tuple or type(self.edits) is not tuple or len(self.edits) != 6:
            raise ValueError('Fixed streams have immutable old cases and exactly six edits.')
        names = set()
        for case in self.old + self.edits:
            if type(case) is not Case or case.frame.request.nbits != self.nbits:
                raise ValueError('Every case must match the stream dimension.')
            if case.name in names:
                raise ValueError('Case names must be distinct within a stream.')
            names.add(case.name)
        if self.protected_free_bit is not None and (
                type(self.protected_free_bit) is not int
                or not 0 <= self.protected_free_bit < self.nbits):
            raise ValueError('Invalid protected parity coordinate.')

    @property
    def identity_replacements(self) -> tuple:
        return tuple(K.bit(i) for i in range(self.nbits))

    def record(self) -> dict:
        return {
            'name': self.name, 'nbits': self.nbits, 'order': list(self.order),
            'protected_free_bit': self.protected_free_bit,
            'identity_replacements': [['bit', i] for i in range(self.nbits)],
            'old': [case.record() for case in self.old],
            'edits': [case.record() for case in self.edits],
        }


def _frame(family, nbits, phase, index, difference, hard=(), soft=(), *, role=None):
    scope = f'{VERSION}/{family}/{phase}/{index:02d}'
    metadata = {
        'stage': 'DEVELOPMENT', 'task': 'R-P3-B-B',
        'fixture_version': VERSION, 'family': family,
        'phase': phase, 'sequence_index': index,
        'source_scope_version': scope,
        'coordinate_interpretation': 'Named Boolean coordinates; exact rational expression grammar.',
        'rank_interpretation': 'Single tier; sum of positive weights for false soft formulas.',
        'loss_interpretation': 'Independently fixed receiving loss difference in declared-loss-unit.',
        'evidence_service': COVERAGE,
    }
    if role is not None:
        metadata['old_domain_role'] = role
    request = K.Request(
        nbits, tuple(hard), tuple(soft), (('D', difference),), scope,
        json.dumps(metadata, sort_keys=True, separators=(',', ':'), allow_nan=False))
    return M.Frame(request, 'D', UNIT)


def _soft(name, expression, weight=1):
    return K.Soft(name, expression, F(weight), 0)


def _parity(indices):
    if not indices:
        raise ValueError('Parity has at least one input.')
    result = K.bit(indices[0])
    for index in indices[1:]:
        result = K.neg(K.eq(result, K.bit(index)))
    return result


def _constant_stream():
    name = 'constant_n3'
    b0, b1, b2 = (K.bit(i) for i in range(3))
    specifications = (
        ((), (), (0, 0, 0)),
        ((K.neg(b0),), (_soft('prefer_b1', b1, 1),), (0, 0, 0)),
        ((b0,), (_soft('prefer_b1', b1, 2),), (1, 1, 0)),
        ((K.neg(b2),), (_soft('prefer_not_b1', K.neg(b1), F(1, 2)),), (0, 0, 0)),
        ((K.eq(b0, b1),), (_soft('prefer_b2', b2, 3),), (1, 1, 1)),
        ((K.OR(b0, b2),), (_soft('prefer_not_b1', K.neg(b1), 2),), (1, 0, 0)),
    )
    edits = tuple(Case(
        f'{name}/edit/{j:02d}',
        _frame(name, 3, 'edit', j, K.lit(-1), hard, soft),
        witness, F(-1))
        for j, (hard, soft, witness) in enumerate(specifications))
    # Deliberately no old certificates: constant/no-reuse overhead control.
    return Stream(name, 3, (0, 1, 2), (), edits)


def _parity_stream():
    name = 'parity_reassociation_n6'
    n = 6
    bits = tuple(K.bit(i) for i in range(n))
    difference = K.sub(_parity(tuple(range(n))), _parity(tuple(reversed(range(n)))))
    old = (Case(f'{name}/old/full_cube',
                _frame(name, n, 'old', 0, difference, role='full_cube'),
                (0,) * n, F(0)),)
    specifications = (
        ((), (_soft('prefer_b0', bits[0], 1),), (0, 0, 0, 0, 0, 0)),
        ((K.neg(bits[0]),), (_soft('prefer_b1', bits[1], 1),), (0, 0, 0, 0, 0, 0)),
        ((bits[0],), (_soft('prefer_not_b1', K.neg(bits[1]), 2),), (1, 0, 0, 0, 0, 0)),
        ((K.eq(bits[0], bits[1]),), (_soft('prefer_b2', bits[2], F(1, 2)),), (1, 1, 0, 0, 0, 0)),
        ((K.OR(bits[2], bits[3]),), (_soft('prefer_not_b4', K.neg(bits[4]), 3),), (0, 0, 1, 0, 0, 0)),
        ((K.neg(bits[0]),), (_soft('prefer_b1', bits[1], 2),
                            _soft('prefer_not_b2', K.neg(bits[2]), 1)),
         (0, 0, 1, 0, 0, 0)),
    )
    edits = tuple(Case(
        f'{name}/edit/{j:02d}',
        _frame(name, n, 'edit', j, difference, hard, soft),
        witness, F(0))
        for j, (hard, soft, witness) in enumerate(specifications))
    return Stream(name, n, tuple(range(n)), old, edits, n - 1)


def _complement_stream(k):
    if k not in (3, 5):
        raise ValueError('Only the two prospectively declared complement dimensions exist.')
    n = k + 2
    name = f'complementary_k{k}_n{n}'
    p, q = K.bit(0), K.bit(1)
    indices = tuple(range(2, n))
    free = n - 1
    other = tuple(range(2, free))
    forward, reverse = _parity(indices), _parity(tuple(reversed(indices)))
    difference = K.add(K.sub(p, q), K.sub(forward, reverse))
    source = K.OR(K.AND(K.neg(p), forward), K.AND(q, K.neg(forward)))
    bootstrap_witness = (0, 1) + (0,) * k
    old = (
        Case(f'{name}/old/left_not_p',
             _frame(name, n, 'old', 0, difference, (K.neg(p),), role='left_not_p'),
             bootstrap_witness, F(0)),
        Case(f'{name}/old/right_q',
             _frame(name, n, 'old', 1, difference, (q,), role='right_q'),
             bootstrap_witness, F(0)),
    )
    edits = []
    for j in range(6):
        ui, vi = other[j % len(other)], other[(j + 1) % len(other)]
        u, v = K.bit(ui), K.bit(vi)
        point = [0] * n
        point[1] = 1
        if j == 0:
            extra = ()
            soft = (_soft('prefer_u', u, 1),)
        elif j == 1:
            extra = (K.neg(u),)
            soft = (_soft('prefer_v', v, 2),)
        elif j == 2:
            extra = (u,)
            soft = (_soft('prefer_not_v', K.neg(v), F(1, 2)),)
            point[ui] = 1
        elif j == 3:
            extra = (K.eq(u, v),)
            soft = (_soft('prefer_u', u, 1), _soft('prefer_not_v', K.neg(v), 2))
        elif j == 4:
            extra = (K.OR(u, v),)
            soft = (_soft('prefer_not_u', K.neg(u), F(3, 2)), _soft('prefer_v', v, F(1, 2)))
            point[ui] = 1
        else:
            extra = (K.neg(u), v)
            soft = (_soft('prefer_u', u, 2), _soft('prefer_not_v', K.neg(v), 1))
            point[vi] = 1
        witness = tuple(point)
        shift = F(1, 2) if j == 5 else F(0)
        current_difference = K.add(difference, K.lit(shift)) if shift else difference
        # Extra hard/rank rows never mention p, q, or the protected free bit.
        # Named witnesses share all ranked/constrained coordinates with witness.
        fixed_parity = sum(point[i] for i in other) % 2
        left = point.copy()
        left[0], left[1], left[free] = 0, 0, 1 ^ fixed_parity
        right = point.copy()
        right[0], right[1], right[free] = 1, 1, fixed_parity
        examples = (
            ('left_exclusive_parity_one', tuple(left)),
            ('right_exclusive_parity_zero', tuple(right)),
            ('intersection_incumbent', witness),
        )
        frame = _frame(name, n, 'edit', j, current_difference, (source,) + extra, soft)
        edits.append(Case(f'{name}/edit/{j:02d}', frame, witness, shift, examples))
    return Stream(name, n, tuple(range(n)), old, tuple(edits), free)


def streams() -> tuple[Stream, ...]:
    """Return exactly the declared immutable streams; no random or truth search."""
    return (_constant_stream(), _parity_stream(), _complement_stream(3), _complement_stream(5))


def declaration() -> dict:
    """Public preparation record; this function performs no scalar truth audit."""
    items = streams()
    return {
        'schema': SCHEMA, 'version': VERSION, 'stage': 'DEVELOPMENT',
        'task': 'R-P3-B-B', 'stream_count': 4, 'current_requests_per_stream': 6,
        'old_case_count': sum(len(s.old) for s in items),
        'current_case_count': sum(len(s.edits) for s in items),
        'variable_order': 'Ascending named coordinate index in every stream.',
        'coverage': COVERAGE,
        'constant_control': 'No old certificates; fixed constant difference and bound minus one.',
        'complement_contract': 'Last parity bit absent from extra hard/rank rows; p0q1 incumbent; last edit shifts difference and requested bound by one half.',
        'named_witness_scope': 'Public development diagnostics; not proof authority and not automatically supplied to policy interfaces.',
        'truth_reference_executed': False,
        'streams': [s.record() for s in items],
    }


def _scalar(expression, point, work=None):
    if work is not None:
        work['scalar_expression_nodes'] = work.get('scalar_expression_nodes', 0) + 1
    tag = expression[0]
    if tag == 'lit':
        return F(expression[1])
    if tag == 'bit':
        return F(point[expression[1]])
    if tag == 'not':
        return F(1) - _scalar(expression[1], point, work)
    if tag == 'scale':
        return F(expression[1]) * _scalar(expression[2], point, work)
    left = _scalar(expression[1], point, work)
    right = _scalar(expression[2], point, work)
    if tag == 'add':
        return left + right
    if tag == 'min':
        return min(left, right)
    if tag == 'max':
        return max(left, right)
    if tag == 'eq':
        return F(left == right)
    if tag == 'and':
        return F(left == 1 and right == 1)
    if tag == 'or':
        return F(left == 1 or right == 1)
    raise ValueError('Unknown admitted scalar-expression operation.')


def scalar_value(expression, point: tuple[int, ...], work=None) -> F:
    """Exact point semantics, independent of interval/ADD/portfolio evaluation."""
    if type(point) is not tuple or not 1 <= len(point) <= 10:
        raise ValueError('A bounded immutable complete point is required.')
    _point(point, len(point))
    K.validate(expression, len(point))
    return _scalar(expression, point, work)


def scalar_report(frame, witness, bound, *, expected_current_record=None, work=None) -> dict:
    """Exhaustively assess the entire current incumbent sublevel.

    This is a reference computation, not a proof object. A false requested bound
    returns BOUND_VIOLATED and its first actual counterexample. Malformed inputs
    or an infeasible advertised incumbent raise ValueError. No optimized solver,
    interval enclosure or certificate acceptance is used to compute truth.
    """
    if type(frame) is not M.Frame:
        raise ValueError('The shared inherited Frame type is required.')
    frame.__post_init__()
    n = frame.request.nbits
    _point(witness, n)
    bound = K.rational(bound)
    current = frame.record()
    if expected_current_record is not None and (
            type(expected_current_record) is not str or expected_current_record != current):
        raise ValueError('Independent current record mismatch.')
    hard = frame.request.hard
    soft = frame.request.soft
    def feasible(point):
        return all(_scalar(h, point, work) == 1 for h in hard)
    def rank(point):
        return sum((F(s.weight) * (1 - _scalar(s.formula, point, work)) for s in soft), F(0))
    if not feasible(witness):
        raise ValueError('The advertised incumbent is not feasible.')
    cutoff = rank(witness)
    hard_count = sublevel_count = 0
    minimum_rank = None
    minimizer_count = 0
    lower = upper = None
    lower_witness = upper_witness = counterexample = None
    for point in product((0, 1), repeat=n):
        if work is not None:
            work['scalar_assignments'] = work.get('scalar_assignments', 0) + 1
        if not feasible(point):
            continue
        hard_count += 1
        value_rank = rank(point)
        if minimum_rank is None or value_rank < minimum_rank:
            minimum_rank, minimizer_count = value_rank, 1
        elif value_rank == minimum_rank:
            minimizer_count += 1
        if value_rank > cutoff:
            continue
        sublevel_count += 1
        difference = _scalar(frame.difference, point, work)
        if lower is None or difference < lower:
            lower, lower_witness = difference, point
        if upper is None or difference > upper:
            upper, upper_witness = difference, point
        if counterexample is None and difference > bound:
            counterexample = point
    if not sublevel_count:
        raise AssertionError('A feasible incumbent must belong to its own sublevel.')
    return {
        'status': 'CURRENT_BOUND_CERTIFIED' if counterexample is None else 'BOUND_VIOLATED',
        'reference_version': VERSION,
        'current_record': current,
        'bound': str(bound), 'requested_bound': str(bound),
        'feasibility': 'NONEMPTY',
        'incumbent_rank': str(cutoff),
        'coverage': COVERAGE,
        'selected_identities_claimed': False,
        'holds': counterexample is None,
        'non_deterioration': counterexample is None and bound <= 0,
        'diagnostic_only': True,
        'diagnostics': {
            'assignments_enumerated': 1 << n,
            'hard_domain_count': hard_count,
            'sublevel_count': sublevel_count,
            'minimum_rank': str(minimum_rank),
            'minimizer_count': minimizer_count,
            'exact_lower': str(lower), 'exact_upper': str(upper),
            'lower_witness': list(lower_witness), 'upper_witness': list(upper_witness),
            'counterexample': None if counterexample is None else list(counterexample),
        },
    }


def reference_report(case: Case, work=None) -> dict:
    if type(case) is not Case:
        raise ValueError('A declared Case is required.')
    return scalar_report(case.frame, case.witness, case.bound,
                         expected_current_record=case.frame.record(), work=work)
