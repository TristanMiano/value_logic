#!/usr/bin/env python3
"""Finite joined-domain proof receiver for P3-05, version portfolio-v2.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-08.
Python 3.10+, standard library only. An external rational Boolean adapter,
not a native v2 proof compiler, dependency-learning algorithm, or authenticated
serialization format. The private cache and imported exact-expression semantics
are trusted. Inputs, feasibility witnesses and all proof instructions are checked.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
from typing import Any
import importlib.util
import sys

sys.dont_write_bytecode = True
_NAME = '_p305_portfolio_base'
if _NAME in sys.modules:
    M = sys.modules[_NAME]
else:
    _spec = importlib.util.spec_from_file_location(_NAME, Path(__file__).with_name('05_counterfactual_transport.py'))
    if _spec is None or _spec.loader is None:
        raise ImportError('Pinned P3-05 receiver dependency is missing.')
    M = importlib.util.module_from_spec(_spec)
    sys.modules[_NAME] = M
    _spec.loader.exec_module(M)
K = M.K
Rejected = M.Rejected
VERSION = 'p305-portfolio-v2'
MAX_CHOICES = 16
MAX_EQUALITIES = 512
MAX_WEIGHTS = 1025
MAX_FEATURES = 2048
MAX_SCALE_CANDIDATES = 32
MAX_TREE_NODES = 2047
_CON = '$constant'


def inc(work: dict | None, key: str, count: int = 1) -> None:
    if work is not None:
        work[key] = work.get(key, 0) + count


def _size(q: F, work=None):
    if work is not None:
        work['max_rational_component_bits'] = max(work.get('max_rational_component_bits', 0),
            abs(q.numerator).bit_length(), q.denominator.bit_length())
    return q


def balanced_sum(expressions):
    es = tuple(expressions)
    if not es: return K.lit(0)
    if len(es) == 1: return es[0]
    m = len(es)//2
    return K.add(balanced_sum(es[:m]), balanced_sum(es[m:]))


def rank_expression(frame):
    return balanced_sum(K.scale(s.weight, K.neg(s.formula)) for s in frame.request.soft)


def substitute(expression, replacements, nbits, work=None):
    def go(e):
        inc(work, 'substitution_nodes')
        if e[0] == 'bit': return replacements[e[1]]
        if e[0] == 'lit': return e
        if e[0] == 'scale': return K.scale(e[1], go(e[2]))
        return (e[0],) + tuple(go(x) for x in e[1:])
    out = go(expression)
    K.validate(out, nbits)
    return out


def form(expression, work=None):
    """Linear collection with Boolean negation; nonlinear features stay opaque.

    No independence of features is used. Identical features can cancel exactly.
    Every public expression has been type-checked before collection.
    """
    vec: dict[str, F] = {}
    atoms: dict[str, Any] = {}
    def add(key, value):
        vec[key] = _size(vec.get(key, F(0)) + value, work)
    def walk(e, coefficient):
        inc(work, 'collection_nodes')
        if e[0] == 'lit': add(_CON, coefficient*F(e[1]))
        elif e[0] == 'add':
            walk(e[1], coefficient); walk(e[2], coefficient)
        elif e[0] == 'scale': walk(e[2], coefficient*F(e[1]))
        elif e[0] == 'not':
            add(_CON, coefficient); walk(e[1], -coefficient)
        else:
            key = M._key(e)
            atoms[key] = e
            add(key, coefficient)
    walk(expression, F(1))
    vec = {k:v for k,v in vec.items() if v}
    if len(vec) > MAX_FEATURES: raise Rejected('Collected feature cap.')
    return vec, atoms


def _combine(dst, src, factor, work=None):
    for key, value in src.items():
        inc(work, 'coefficient_operations')
        q = _size(dst.get(key, F(0)) + factor*value, work)
        if q: dst[key] = q
        else: dst.pop(key, None)


def _enclose_form(vec, atoms, cell, work=None):
    lo = hi = vec.get(_CON, F(0))
    for key, coefficient in vec.items():
        if key == _CON: continue
        a,b = K.interval(atoms[key], cell, work)
        lo = _size(lo + min(coefficient*a, coefficient*b), work)
        hi = _size(hi + max(coefficient*a, coefficient*b), work)
    return lo,hi


def truth_goals(expression):
    """Return numerical <= 0 goals sufficient for this Boolean formula's truth."""
    if expression[0] == 'and':
        return truth_goals(expression[1]) + truth_goals(expression[2])
    if expression[0] == 'eq':
        return (K.sub(expression[1], expression[2]), K.sub(expression[2], expression[1]))
    return (K.sub(K.lit(1), expression),)


def hard_equalities(expression):
    """Each returned e is identically zero whenever the input formula is true."""
    out = [K.sub(K.lit(1), expression)]
    if expression[0] == 'eq': out.append(K.sub(expression[1], expression[2]))
    elif expression[0] == 'and':
        out.extend(hard_equalities(expression[1])); out.extend(hard_equalities(expression[2]))
    return out


@dataclass(frozen=True)
class ContextRows:
    expressions: tuple
    equality_positive_indices: tuple[int, ...]
    nbits: int
    one_sided_indices: tuple[int, ...] = (0,)


def clause_inequalities(expression):
    """A true Boolean disjunction has sum of its Boolean leaves at least one.

    Conjunction permits recursion into both children; disjunction does not.
    These are ordinary Boolean linear relaxations, not new independent facts.
    """
    def leaves(e, op):
        if e[0] == op: return leaves(e[1], op) + leaves(e[2], op)
        return [e]
    if expression[0] == "and":
        return clause_inequalities(expression[1]) + clause_inequalities(expression[2])
    if expression[0] == "or":
        return [K.sub(K.lit(1), balanced_sum(leaves(expression, "or")))]
    if expression[0] == "not" and expression[1][0] == "and":
        es = [K.neg(e) for e in leaves(expression[1], "and")]
        return [K.sub(K.lit(1), balanced_sum(es))]
    return []


def context_rows(frame, cell, cutoff, work=None) -> ContextRows:
    """Derive premises from the actual receiving frame/cell, never a claimed list."""
    expressions = [K.sub(rank_expression(frame), K.lit(cutoff))]
    positives = []
    eqs = []
    for h in frame.request.hard: eqs.extend(hard_equalities(h))
    for i,value in enumerate(cell):
        if value is not None: eqs.append(K.sub(K.bit(i), K.lit(value)))
    if len(eqs) > MAX_EQUALITIES: raise Rejected('Conditional equality cap.')
    for e in eqs:
        positives.append(len(expressions))
        expressions.extend((e, K.scale(-1, e)))
    one_sided = [0]
    extra = []
    for h in frame.request.hard: extra.extend(clause_inequalities(h))
    if len(eqs) + len(extra) > MAX_EQUALITIES:
        raise Rejected('Conditional premise cap.')
    for e in extra:
        one_sided.append(len(expressions)); expressions.append(e)
    for e in expressions:
        K.validate(e, frame.request.nbits)
        inc(work, 'premise_rows_built')
    return ContextRows(tuple(expressions), tuple(positives), frame.request.nbits, tuple(one_sided))


def conditional_upper(target, weights, rows: ContextRows, cell, work=None) -> F:
    """Check nonnegative row multipliers and bound the exact residual on the box."""
    K.validate(target, rows.nbits)
    if type(weights) is not tuple or len(weights) > MAX_WEIGHTS:
        raise Rejected('A capped tuple of premise multipliers is required.')
    v, atoms = form(target, work)
    seen = set()
    for item in weights:
        if type(item) is not tuple or len(item) != 2: raise Rejected('Malformed multiplier.')
        j, raw = item
        if type(j) is not int or not 0 <= j < len(rows.expressions) or j in seen:
            raise Rejected('Multiplier row indices must be distinct current rows.')
        seen.add(j)
        q = K.rational(raw)
        if q < 0: raise Rejected('Negative multiplier on a one-sided premise.')
        w, more = form(rows.expressions[j], work)
        atoms.update(more); _combine(v, w, -q, work)
        inc(work, 'multipliers_checked')
    return _enclose_form(v, atoms, cell, work)[1]


def equality_witness(target, rows, rank_factor=F(0), work=None, *, inequality_index=0):
    """Producer-only exact elimination over equalities, with a rank-row multiplier.

    The verifier does not trust this elimination: it independently recomputes
    the nonnegative-combination residual. This is a modest symbolic baseline,
    not a complete LP or SMT searcher.
    """
    rank_factor = K.rational(rank_factor)
    if rank_factor < 0: raise Rejected('Nonnegative row multiplier required.')
    if type(inequality_index) is not int or inequality_index not in rows.one_sided_indices:
        raise Rejected('An actually derived one-sided row is required.')
    basis = []
    for j in rows.equality_positive_indices:
        v,_ = form(rows.expressions[j], work)
        combo = {j:F(1)}
        for pivot, bv, bc in basis:
            coefficient = v.get(pivot, F(0))
            if coefficient:
                _combine(v, bv, -coefficient, work); _combine(combo, bc, -coefficient, work)
        if not v: continue
        pivot = min(v, key=lambda k:(k == _CON, k))
        coefficient = v[pivot]
        v = {k:_size(q/coefficient, work) for k,q in v.items()}
        combo = {k:_size(q/coefficient, work) for k,q in combo.items()}
        basis.append((pivot,v,combo))
        inc(work, 'equality_pivots')
    v,_ = form(target, work)
    if rank_factor:
        rv,_ = form(rows.expressions[inequality_index], work)
        _combine(v, rv, -rank_factor, work)
    combo = {}
    for pivot,bv,bc in basis:
        coefficient = v.get(pivot, F(0))
        if coefficient:
            _combine(v, bv, -coefficient, work); _combine(combo, bc, coefficient, work)
    weights = {} if not rank_factor else {inequality_index:rank_factor}
    for j,q in combo.items():
        index = j if q >= 0 else j+1
        weights[index] = weights.get(index,F(0)) + abs(q)
    answer = tuple(sorted((j,K.rational(q)) for j,q in weights.items() if q))
    if len(answer) > MAX_WEIGHTS: raise Rejected('Conditional witness cap.')
    return answer


def best_witness(target, bound, rows, cell, *, symbolic=True, rank_hint=False, work=None):
    bound = K.rational(bound)
    # The empty witness is a valid interval certificate and wins cheap cases.
    if conditional_upper(target, (), rows, cell, work) <= bound: return ()
    if not symbolic: return None
    weights = equality_witness(target, rows, F(0), work)
    if conditional_upper(target, weights, rows, cell, work) <= bound: return weights
    target_form,_ = form(target, work)
    # Try one derived inequality at a time, plus the equality span. Completeness
    # of this heuristic is NOT claimed; supplied witnesses can use many rows.
    indices = rows.one_sided_indices if rank_hint else tuple(reversed(rows.one_sided_indices))
    for j in indices:
        row_form,_ = form(rows.expressions[j], work)
        ratios = {F(1)}
        for key,value in row_form.items():
            if key == _CON or not value or not target_form.get(key): continue
            ratio = target_form[key]/value
            if ratio > 0:
                try: ratios.add(K.rational(ratio))
                except ValueError: pass
        for factor in sorted(ratios)[:MAX_SCALE_CANDIDATES]:
            weights = equality_witness(target, rows, factor, work, inequality_index=j)
            if conditional_upper(target, weights, rows, cell, work) <= bound: return weights
    return None


@dataclass(frozen=True)
class Choice:
    handle: str
    expected_old_record: str
    replacements: tuple
    alpha: F = F(1)

    def __post_init__(self):
        object.__setattr__(self, 'alpha', K.rational(self.alpha))

    def record(self):
        return {'handle':self.handle, 'old_record':self.expected_old_record,
                'replacements':self.replacements, 'alpha':self.alpha}


@dataclass(frozen=True)
class DomainCertificate:
    frame: Any
    cutoff: F
    bound: F
    kind: str


@dataclass(frozen=True)
class CompiledChoice:
    choice: Choice
    old: DomainCertificate
    hard_goals: tuple
    rank: tuple
    loss_correction: tuple


@dataclass(frozen=True)
class PortfolioProof:
    current_record: str
    choices: tuple[Choice, ...]
    witness: tuple[int, ...]
    bound: F
    tree: tuple

    def record(self):
        return {'version':VERSION,'current_record':self.current_record,
                'choices':[c.record() for c in self.choices],
                'witness':self.witness,'bound':self.bound,'tree':self.tree}


class Uncertified(ValueError):
    """No proof under this supplied cover/portfolio; not necessarily a bad optimum."""
    def __init__(self, cell, reason):
        self.cell = cell
        self.reason = reason
        super().__init__(reason + ': ' + str(cell))


class PortfolioCache:
    """Only verified immutable domains are admitted; private memory is trusted.

    A chain admission can refer only to older admitted handles. To reconstruct
    a cache from files, reverify the chain; a report's JSON or digest is not an
    admission. No claim of protection against arbitrary Python memory mutation.
    """
    def __init__(self):
        self._domains: dict[str, DomainCertificate] = {}

    def _fresh(self, handle):
        if type(handle) is not str or not handle or handle in self._domains or len(self._domains) >= M.MAX_CACHE:
            raise Rejected('Fresh nonempty cache handle and available capacity required.')

    def admit_band(self, handle, proof, expected_old_record, work=None):
        self._fresh(handle)
        M.verify_band(proof, expected_old_record, work)
        self._domains[handle] = DomainCertificate(proof.frame, proof.cutoff, proof.bound, 'band')
        inc(work, 'domains_admitted')

    def _prepare(self, current, choices, witness, bound, work=None):
        if type(current) is not M.Frame: raise Rejected('Current Frame type.')
        current.__post_init__()
        bound = K.rational(bound)
        if type(choices) is not tuple or len(choices) > MAX_CHOICES:
            raise Rejected('Capped immutable portfolio choices required.')
        M._point(witness, current.request.nbits)
        for h in current.request.hard:
            inc(work, 'feasibility_checks')
            if K.interval(h, witness, work) != (F(1),F(1)):
                raise Rejected('The independently checked incumbent is not feasible.')
        cutoff = M.rank_bounds(current,witness,work)[0]
        compiled = []
        for choice in choices:
            if type(choice) is not Choice or type(choice.handle) is not str or choice.handle not in self._domains:
                raise Rejected('Unadmitted portfolio handle or malformed choice.')
            old = self._domains[choice.handle]
            old_record = old.frame.record()
            if type(choice.expected_old_record) is not str or choice.expected_old_record != old_record:
                raise Rejected('Old certificate record does not match the selected input.')
            inc(work, 'record_characters_compared', len(old_record))
            if old.frame.unit != current.unit: raise Rejected('Explicit loss units do not match.')
            alpha = K.rational(choice.alpha)
            if alpha <= 0: raise Rejected('Positive loss scaling required.')
            rs = choice.replacements
            if type(rs) is not tuple or len(rs) != old.frame.request.nbits:
                raise Rejected('Exactly one Boolean map per old bit is required.')
            for e in rs:
                if K.validate(e,current.request.nbits) != 'bool':
                    raise Rejected('Map does not produce an old Boolean coordinate.')
            goals = []
            for h in old.frame.request.hard:
                goals.extend(truth_goals(substitute(h,rs,current.request.nbits,work)))
            rank = substitute(rank_expression(old.frame),rs,current.request.nbits,work)
            mapped_d = substitute(old.frame.difference,rs,current.request.nbits,work)
            drift = K.sub(current.difference,K.scale(alpha,mapped_d))
            for e in (*goals,rank,drift): K.validate(e,current.request.nbits)
            compiled.append(CompiledChoice(choice,old,tuple(goals),rank,drift))
        # Enforce row-cap/expanded-expression obligations before traversing.
        context_rows(current,(None,)*current.request.nbits,cutoff,work)
        return cutoff,tuple(compiled)

    def build(self, current, choices, witness, bound, *, symbolic=True,
              allow_direct=True, order=None, work=None):
        bound = K.rational(bound)
        cutoff, compiled = self._prepare(current,choices,witness,bound,work)
        if type(symbolic) is not bool or type(allow_direct) is not bool:
            raise Rejected('Producer option flags must be Boolean.')
        order = tuple(range(current.request.nbits)) if order is None else order
        M._permutation(order,current.request.nbits)
        visited = 0
        def go(cell):
            nonlocal visited
            visited += 1; inc(work, 'producer_cover_nodes')
            if visited > MAX_TREE_NODES: raise Rejected('Portfolio tree construction cap.')
            for j,h in enumerate(current.request.hard):
                if K.interval(h,cell,work)[1] == 0: return ('hard',j)
            if M.rank_bounds(current,cell,work)[0] > cutoff: return ('rank',)
            rows = context_rows(current,cell,cutoff,work)
            for i,c in enumerate(compiled):
                ws=[]
                for g in c.hard_goals:
                    w=best_witness(g,0,rows,cell,symbolic=symbolic,work=work)
                    if w is None: break
                    ws.append(w)
                if len(ws) != len(c.hard_goals): continue
                rank_w=best_witness(c.rank,c.old.cutoff,rows,cell,symbolic=symbolic,rank_hint=True,work=work)
                if rank_w is None: continue
                loss_w=best_witness(c.loss_correction,bound-c.choice.alpha*c.old.bound,
                                    rows,cell,symbolic=symbolic,work=work)
                if loss_w is None: continue
                return ('reuse',i,tuple(ws),rank_w,loss_w)
            if allow_direct:
                w=best_witness(current.difference,bound,rows,cell,symbolic=symbolic,work=work)
                if w is not None: return ('direct',w)
            free=[i for i in order if cell[i] is None]
            if not free:
                raise Uncertified(cell,'Incumbent sublevel is not covered by the allowed proof vocabulary')
            i=free[0]
            return ('split',i,go(cell[:i]+(0,)+cell[i+1:]),go(cell[:i]+(1,)+cell[i+1:]))
        return PortfolioProof(current.record(),choices,witness,bound,go((None,)*current.request.nbits))

    def verify(self, proof, current, expected_current_record, work=None):
        if type(proof) is not PortfolioProof: raise Rejected('Portfolio proof type.')
        if type(current) is not M.Frame: raise Rejected('Current Frame type.')
        current.__post_init__()
        record=current.record()
        if type(expected_current_record) is not str or record != expected_current_record or proof.current_record != record:
            raise Rejected('The proof does not bind the independently supplied current request.')
        inc(work,'record_characters_compared',2*len(record))
        bound = K.rational(proof.bound)
        cutoff,compiled=self._prepare(current,proof.choices,proof.witness,bound,work)
        counts={'reuse_leaves':0,'direct_leaves':0,'hard_exclusions':0,'rank_exclusions':0,'splits':0}
        visited=0
        def check(tree,cell):
            nonlocal visited
            visited+=1;inc(work,'verified_cover_nodes')
            if visited>MAX_TREE_NODES or type(tree) is not tuple or not tree:
                raise Rejected('Malformed or oversized cover tree.')
            op=tree[0]
            if op=='split' and len(tree)==4:
                i=tree[1]
                if type(i) is not int or not 0<=i<len(cell) or cell[i] is not None:
                    raise Rejected('A split must cover both values of an unassigned bit.')
                counts['splits']+=1
                check(tree[2],cell[:i]+(0,)+cell[i+1:]);check(tree[3],cell[:i]+(1,)+cell[i+1:]);return
            if op=='hard' and len(tree)==2:
                j=tree[1]
                if type(j) is int and 0<=j<len(current.request.hard) and K.interval(current.request.hard[j],cell,work)[1]==0:
                    counts['hard_exclusions']+=1;return
                raise Rejected('Unjustified current hard exclusion.')
            if op=='rank' and len(tree)==1:
                if M.rank_bounds(current,cell,work)[0]>cutoff:
                    counts['rank_exclusions']+=1;return
                raise Rejected('Unjustified rank exclusion; equality cannot remove a tie.')
            rows=context_rows(current,cell,cutoff,work)
            if op=='direct' and len(tree)==2:
                if conditional_upper(current.difference,tree[1],rows,cell,work)<=bound:
                    counts['direct_leaves']+=1;return
                raise Rejected('Unjustified fresh-current inequality.')
            if op=='reuse' and len(tree)==5:
                i,ws,rw,lw=tree[1:]
                if type(i) is not int or not 0<=i<len(compiled): raise Rejected('Unknown portfolio member.')
                c=compiled[i]
                if type(ws) is not tuple or len(ws)!=len(c.hard_goals): raise Rejected('Mapped premise obligations are incomplete.')
                for g,w in zip(c.hard_goals,ws):
                    if conditional_upper(g,w,rows,cell,work)>0: raise Rejected('Mapped old premise not discharged.')
                if conditional_upper(c.rank,rw,rows,cell,work)>c.old.cutoff:
                    raise Rejected('Mapped case lies outside the certified old rank sublevel.')
                if conditional_upper(c.loss_correction,lw,rows,cell,work)>bound-c.choice.alpha*c.old.bound:
                    raise Rejected('Receiving loss correction is insufficient.')
                counts['reuse_leaves']+=1;return
            raise Rejected('Unknown or malformed portfolio instruction.')
        check(proof.tree,(None,)*current.request.nbits)
        return {'status':'CURRENT_BOUND_CERTIFIED','version':VERSION,'current_record':record,
                'bound':str(bound),'non_deterioration':bound<=0,
                'feasibility':'NONEMPTY','incumbent_rank':str(cutoff),
                'coverage':'ENTIRE_CURRENT_INCUMBENT_SUBLEVEL_INCLUDING_ALL_MINIMIZERS',
                'selected_identities_claimed':False, 'counts':counts,
                'meaning':'uniform bound for the independently fixed receiving loss difference',
                'trusted_cache':True}

    def receive(self, advertised, proof, current, expected_current_record, work=None):
        actual=self.verify(proof,current,expected_current_record,work)
        if type(advertised) is not dict or M.canonical(advertised)!=M.canonical(actual):
            raise Rejected('Advertised report differs from the independently verified report.')
        return actual

    def admit_portfolio(self, handle, proof, current, expected_current_record, work=None):
        self._fresh(handle)
        report=self.verify(proof,current,expected_current_record,work)
        self._domains[handle]=DomainCertificate(current,F(report['incumbent_rank']),K.rational(proof.bound),'portfolio')
        inc(work,'domains_admitted')
        return report
