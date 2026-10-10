#!/usr/bin/env python3
"""Bounded current dependency pruning for recorded ordinary ADD evidence.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-10.
R-P3-B-B DEVELOPMENT, added after primary exposure. Existing producers,
receivers and measured source closures are unchanged. This module extracts a
dependency-closed full v1 packet; it is not a proof checker or a proof minimizer.
The unchanged independent receiver remains the sole certificate authority.
"""
from __future__ import annotations

from fractions import Fraction as F
from pathlib import Path
import importlib.util
import sys

sys.dont_write_bytecode = True


def _load_evidence():
    name = '_rp3bb_add_evidence_producer'
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(
        name, Path(__file__).with_name('05_add_evidence.py'))
    if spec is None or spec.loader is None:
        raise ImportError('Missing unchanged recorded ADD evidence dependency.')
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


E = _load_evidence()
M, K = E.M, E.K
VERSION = 'rp3bb-add-evidence-prune-v1'
MAX_DEPENDENCY_STEPS = 8_000_000
SOURCE_PATHS = (*E.DEFAULT_SOURCE_PATHS, 'v3/checks/05_add_evidence_prune.py')


class PruneRejected(E.EvidenceRejected):
    """Unsupported scope or absent required structural dependency; no proof."""


class PruneLimit(E.EvidenceLimit):
    """Exhausted finite dependency guard, not falsity of the requested bound."""
    def __init__(self, used, limit, requested):
        self.used, self.limit, self.requested = used, limit, requested
        super().__init__(f'Dependency pruning limit: {used}+{requested}>{limit}.')


class _Budget:
    """Local traversal guard; the outer service must still charge all execution."""
    def __init__(self, work, limit):
        if work is not None and type(work) is not dict:
            raise PruneRejected('A plain diagnostic work dictionary is required.')
        if type(limit) is not int or not 1 <= limit <= MAX_DEPENDENCY_STEPS:
            raise PruneRejected('Exact pruning limit from 1 through 8,000,000 required.')
        self.work, self.limit, self.used = work, limit, 0
        if work is not None:
            work['prune_limit_steps'] = limit

    def tick(self, category, count=1):
        if self.used + count > self.limit:
            E.inc(self.work, 'prune_denied_step_requests', count)
            raise PruneLimit(self.used, self.limit, count)
        self.used += count
        E.inc(self.work, 'prune_steps', count)
        E.inc(self.work, category, count)


class _Closure:
    """Temporary indexes and marked dependencies; never a retained authority."""
    def __init__(self, proof, budget):
        self.proof, self.budget = proof, budget
        self.position = {var: index for index, var in enumerate(proof.order)}
        self.node_index, self.terminal_index = {}, {}
        self.apply_index, self.expression_index = {}, {}
        self.nodes, self.applies, self.expressions = set(), set(), set()
        for index, node in enumerate(proof.nodes):
            budget.tick('prune_node_index_rows')
            if type(node) is not tuple or not node:
                raise PruneRejected('Immutable node row required.')
            if node[0] == 'T' and len(node) == 3:
                E._rational_pair(node[1:], E.MAX_TERMINAL_BITS)
                self.terminal_index[node[1:]] = index
            elif node[0] == 'N' and len(node) == 4:
                if type(node[1]) is not int or node[1] not in self.position:
                    raise PruneRejected('Declared decision coordinate required.')
                for child in node[2:]:
                    self._id(child, upper=index)
                    child_node = proof.nodes[child]
                    if (child_node[0] == 'N' and self.position[child_node[1]]
                            <= self.position[node[1]]):
                        raise PruneRejected('Ordered node back references required.')
                if node[2] == node[3]:
                    raise PruneRejected('Reduced node required.')
            else:
                raise PruneRejected('Unknown node shape.')
            if node in self.node_index:
                raise PruneRejected('Duplicate diagram node in full input.')
            self.node_index[node] = index
        for index, row in enumerate(proof.applies):
            budget.tick('prune_apply_index_rows')
            if (type(row) is not tuple or len(row) != 4
                    or type(row[0]) is not str or row[0] not in E.OPERATORS):
                raise PruneRejected('Exact existing Apply fact required.')
            for identifier in row[1:]:
                self._id(identifier)
            key = self.key(*row[:3])
            if key != row[:3] or key in self.apply_index:
                raise PruneRejected('Unique canonical Apply keys required.')
            self.apply_index[key] = (index, row[3])
        for index, row in enumerate(proof.expressions):
            budget.tick('prune_expression_index_rows')
            if (type(row) is not tuple or len(row) != 2
                    or type(row[0]) is not str):
                raise PruneRejected('Exact existing expression binding required.')
            budget.tick('prune_expression_index_characters', len(row[0]))
            if len(row[0].encode('utf-8')) > E.MAX_EXPRESSION_BYTES:
                raise PruneRejected('Expression key byte cap.')
            self._id(row[1])
            if row[0] in self.expression_index:
                raise PruneRejected('Unique expression keys required.')
            self.expression_index[row[0]] = (index, row[1])

    def _id(self, identifier, upper=None):
        self.budget.tick('prune_node_reference_checks')
        end = len(self.proof.nodes) if upper is None else upper
        if type(identifier) is not int or not 0 <= identifier < end:
            raise PruneRejected('Existing bounded node identifier required.')
        return identifier

    def key(self, op, left, right):
        if op in E.COMMUTATIVE and left > right:
            left, right = right, left
        return op, left, right

    def node(self, identifier):
        self.budget.tick('prune_node_dependency_visits')
        self._id(identifier)
        if identifier not in self.nodes:
            self.nodes.add(identifier)
            row = self.proof.nodes[identifier]
            if row[0] == 'N':
                self.node(row[2])
                self.node(row[3])
        return identifier

    def terminal(self, value):
        pair = E._pair(F(value))
        self.budget.tick('prune_terminal_dependency_lookups')
        if pair not in self.terminal_index:
            raise PruneRejected('Missing required rational terminal.')
        return self.node(self.terminal_index[pair])

    def level(self, identifier):
        self.budget.tick('prune_level_lookups')
        row = self.proof.nodes[identifier]
        return self.proof.bits if row[0] == 'T' else self.position[row[1]]

    def operation(self, op, left, right, *, before=None):
        """Mark the receiver's required proof premises, not a guessed result."""
        key = self.key(op, left, right)
        self.budget.tick('prune_apply_dependency_lookups')
        if key not in self.apply_index:
            raise PruneRejected('Missing required Apply dependency: ' + str(key))
        index, out = self.apply_index[key]
        if before is not None and index >= before:
            raise PruneRejected('Apply premise must precede its dependent fact.')
        if key in self.applies:
            return out
        self.applies.add(key)
        _, left, right = key
        self.node(left)
        self.node(right)
        self.node(out)
        a, b = self.proof.nodes[left], self.proof.nodes[right]
        # These cases have no recursive Apply premises in receiver v1. The
        # receiver still checks the arithmetic, Boolean flags and exact output.
        if left == right and op in ('min', 'max', 'and', 'or', 'eq', 'le', 'sub', 'gt'):
            return out
        if a[0] == b[0] == 'T':
            return out
        az, bz = a == ('T', 0, 1), b == ('T', 0, 1)
        ao, bo = a == ('T', 1, 1), b == ('T', 1, 1)
        if ((op in ('mul', 'and') and (az or bz))
                or (op == 'or' and (ao or bo))
                or (op in ('add', 'or') and (az or bz))
                or (op in ('mul', 'and') and (ao or bo))):
            return out
        left_level, right_level = self.level(left), self.level(right)
        level = min(left_level, right_level)
        if level >= self.proof.bits:
            raise PruneRejected('Missing terminal Apply case.')
        low_a, high_a = a[2:] if left_level == level else (left, left)
        low_b, high_b = b[2:] if right_level == level else (right, right)
        self.operation(op, low_a, low_b, before=index)
        self.operation(op, high_a, high_b, before=index)
        self.budget.tick('prune_shannon_dependencies_expanded')
        return out

    def expression(self, expression, *, before=None):
        key = M._key(expression)
        self.budget.tick('prune_expression_dependency_characters', len(key))
        self.budget.tick('prune_expression_dependency_lookups')
        if key not in self.expression_index:
            raise PruneRejected('Missing required current expression binding.')
        index, root = self.expression_index[key]
        if before is not None and index >= before:
            raise PruneRejected('Expression child must precede its parent binding.')
        if key in self.expressions:
            return root
        self.expressions.add(key)
        self.node(root)
        op = expression[0]
        if op == 'lit':
            expected = self.terminal(expression[1])
        elif op == 'bit':
            zero, one = self.terminal(0), self.terminal(1)
            self.budget.tick('prune_bit_node_lookups')
            expected = self.node_index.get(('N', expression[1], zero, one))
            if expected is None:
                raise PruneRejected('Missing required bit definition.')
            self.node(expected)
        elif op == 'not':
            expected = self.operation('sub', self.terminal(1),
                                      self.expression(expression[1], before=index))
        elif op == 'scale':
            expected = self.operation('mul', self.terminal(expression[1]),
                                      self.expression(expression[2], before=index))
        else:
            expected = self.operation(op, self.expression(expression[1], before=index),
                                      self.expression(expression[2], before=index))
        if root != expected:
            raise PruneRejected('Expression binding disagrees with its required fact.')
        return root

    def emit(self):
        ordered = sorted(self.nodes)
        self.budget.tick('prune_sorted_node_identifiers', len(ordered))
        remap = {old: new for new, old in enumerate(ordered)}
        nodes = []
        for old in ordered:
            self.budget.tick('prune_emitted_node_rows')
            row = self.proof.nodes[old]
            nodes.append(row if row[0] == 'T' else
                         ('N', row[1], remap[row[2]], remap[row[3]]))
        applies = []
        for row in self.proof.applies:
            self.budget.tick('prune_apply_filter_rows')
            if row[:3] in self.applies:
                self.budget.tick('prune_emitted_apply_rows')
                applies.append((row[0], *(remap[node] for node in row[1:])))
        expressions = []
        for key, root in self.proof.expressions:
            self.budget.tick('prune_expression_filter_rows')
            if key in self.expressions:
                self.budget.tick('prune_emitted_expression_rows')
                expressions.append((key, remap[root]))
        self.budget.tick('prune_immutable_output_constructions')
        return E.AddEvidence(
            self.proof.source_record, self.proof.epoch, self.proof.bits,
            self.proof.order, 'full', (0, 0, 0), tuple(nodes), tuple(applies),
            tuple(expressions), self.proof.current_record, self.proof.witness,
            self.proof.bound, tuple(remap[root] for root in self.proof.roots))


def prune_full(evidence, current, witness, bound, expected_record, *,
               work=None, limit_steps=MAX_DEPENDENCY_STEPS):
    """Return a dependency-pruned full v1 proof for a fresh receiver.

    Input is an immutable full/zero-base evidence object. No previous receiver
    facts, successful report or truth labels enter this function. The source
    record is preserved and must independently bind the actual closure including
    this module. The function does not authenticate source bytes or certify its
    own result. Its temporary indexes are discarded on return or failure.

    All input scanning, exact goal construction, dependency traversal, remapping
    and output validation occur in this call and must be charged by the outer
    service. Diagnostic dependency steps are only a separate finite local guard.
    The caller retains the unchanged full warm manager and pays its full state.
    """
    budget = _Budget(work, limit_steps)
    budget.tick('prune_entry_checks')
    if type(evidence) is not E.AddEvidence:
        raise PruneRejected('Exact immutable existing AddEvidence required.')
    if evidence.mode != 'full' or evidence.base != (0, 0, 0):
        raise PruneRejected('Pruning requires full evidence with zero base counts.')
    E._header(evidence.source_record, evidence.epoch, evidence.bits, evidence.order)
    for rows, cap in ((evidence.nodes, E.MAX_NODES),
                      (evidence.applies, E.MAX_APPLIES),
                      (evidence.expressions, E.MAX_EXPRESSIONS)):
        if type(rows) is not tuple or len(rows) > cap:
            raise PruneRejected('Capped immutable full evidence tables required.')
    if type(current) is not M.Frame or current.request.nbits != evidence.bits:
        raise PruneRejected('Matching independently supplied current Frame required.')
    current.__post_init__()
    record = current.record()
    budget.tick('prune_current_record_characters', len(record))
    if (type(expected_record) is not str or record != expected_record
            or record != evidence.current_record):
        raise PruneRejected('Independent current record mismatch.')
    M._point(witness, evidence.bits)
    if evidence.witness != witness:
        raise PruneRejected('Pruning may not replace the supplied incumbent.')
    rational_bound = K.rational(bound)
    if E._pair(rational_bound, E.MAX_BOUND_BITS) != evidence.bound:
        raise PruneRejected('Pruning may not replace the requested bound.')
    for hard in current.request.hard:
        budget.tick('prune_feasibility_rows')
        if K.interval(hard, witness, work) != (F(1), F(1)):
            raise PruneRejected('The supplied incumbent is not feasible.')
    cutoff = M.rank_bounds(current, witness, work)[0]
    for key, count in (('prune_input_nodes', len(evidence.nodes)),
                       ('prune_input_applies', len(evidence.applies)),
                       ('prune_input_expressions', len(evidence.expressions))):
        E.inc(work, key, count)
    closure = _Closure(evidence, budget)
    zero, one = closure.terminal(0), closure.terminal(1)
    guard, rank = one, zero
    for hard in current.request.hard:
        guard = closure.operation('and', guard, closure.expression(hard))
    for soft in current.request.soft:
        failure = closure.operation('sub', one, closure.expression(soft.formula))
        weighted = closure.operation('mul', closure.terminal(soft.weight), failure)
        rank = closure.operation('add', rank, weighted)
    rank_test = closure.operation('le', rank, closure.terminal(cutoff))
    guard = closure.operation('and', guard, rank_test)
    difference = closure.expression(current.difference)
    loss_test = closure.operation('gt', difference, closure.terminal(rational_bound))
    bad = closure.operation('and', guard, loss_test)
    if evidence.roots != (guard, rank, difference, bad):
        raise PruneRejected('Current roots disagree with the required request facts.')
    if bad != zero:
        raise PruneRejected('The supplied bad-set root is not the zero terminal.')
    result = closure.emit()
    E.inc(work, 'prune_output_nodes', len(result.nodes))
    E.inc(work, 'prune_output_applies', len(result.applies))
    E.inc(work, 'prune_output_expressions', len(result.expressions))
    return result


def export_pruned(manager, current, witness, bound, expected_record, *,
                  work=None, limit_steps=MAX_DEPENDENCY_STEPS):
    """Pay full ordinary export and pruning; never call an independent receiver."""
    full = E.export_dag(manager, current, witness, bound, expected_record, work=work)
    return prune_full(full, current, witness, bound, expected_record,
                      work=work, limit_steps=limit_steps)
