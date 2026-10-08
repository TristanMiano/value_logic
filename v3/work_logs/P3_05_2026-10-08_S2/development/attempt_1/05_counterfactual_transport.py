#!/usr/bin/env python3
"""P3-05 reconstructed-v1: conditional reuse of a finite rank-band certificate.

Python 3.10+, standard library only. Trusted in-process cache; no cryptographic
or empirical authentication. This is not the lost P3-05 implementation, a native
v2 proof compiler, a general program-equivalence solver or a learning algorithm.
Construction, admission and per-edit checking costs must be reported separately.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any

sys.dont_write_bytecode = True
# Import by file name because the inherited module name starts with a digit.
_name = '_p305_inherited_p304'
if _name in sys.modules:
    K = sys.modules[_name]
else:
    _spec = importlib.util.spec_from_file_location(_name, Path(__file__).with_name('04_counterfactual_repair.py'))
    if _spec is None or _spec.loader is None:
        raise ImportError('The unchanged P3-04 dependency is missing.')
    K = importlib.util.module_from_spec(_spec)
    sys.modules[_name] = K
    _spec.loader.exec_module(K)

VERSION = 'p305-reconstructed-v1'
MAX_BITS, MAX_PROOF_NODES, MAX_CACHE = 10, 2047, 64


class Rejected(ValueError):
    """Malformed, mismatched or invalid evidence, not falsity of a comparison."""


class NoBandProof(ValueError):
    """The specified band comparison fails at a complete finite witness."""


def _inc(work: dict | None, name: str, n: int = 1) -> None:
    if work is not None:
        work[name] = work.get(name, 0) + n


def _q(x: Any) -> F:
    return K.rational(x)


def _unique_pairs(pairs):
    result = {}
    for k, v in pairs:
        if k in result:
            raise Rejected('Duplicate metadata key.')
        result[k] = v
    return result


def _bad_constant(x):
    raise Rejected('Nonfinite JSON constant.')


def canonical(value: Any) -> str:
    """An exact JSON record comparison, distinguishing true, 1 and "1".

    Metadata floats are deliberately unsupported, not silently rounded.
    Keys must be strings; depth and total metadata size are capped by Frame.
    """
    def walk(x, depth=0):
        if depth > 64:
            raise Rejected('Record depth cap.')
        if x is None or type(x) in (bool, int, str):
            return x
        if type(x) is F:
            return {'rational': str(x)}
        if type(x) in (tuple, list):
            return [walk(v, depth+1) for v in x]
        if type(x) is dict and all(type(k) is str for k in x):
            return {k: walk(v, depth+1) for k, v in x.items()}
        raise Rejected('Unsupported exact-record value.')
    return json.dumps(walk(value), ensure_ascii=True, sort_keys=True, separators=(',', ':'), allow_nan=False)


@dataclass(frozen=True)
class Frame:
    request: Any
    loss: str
    unit: str

    def __post_init__(self):
        if type(self.request) is not K.Request:
            raise Rejected('Use the declared inherited Request type.')
        self.request.__post_init__()
        if self.request.nbits > MAX_BITS or self.request.tiers != 1:
            raise Rejected('Receiver supports at most ten bits and one rank tier.')
        if type(self.loss) is not str or self.loss not in dict(self.request.losses):
            raise Rejected('Missing requested difference expression.')
        if type(self.unit) is not str or not self.unit:
            raise Rejected('Declared loss unit required.')
        meta = json.loads(self.request.metadata_json, object_pairs_hook=_unique_pairs,
                          parse_constant=_bad_constant)
        canonical(meta)

    @property
    def difference(self):
        return dict(self.request.losses)[self.loss]

    def record(self) -> str:
        return canonical({'receiver': VERSION, 'request': self.request.record(),
                          'loss': self.loss, 'unit': self.unit})


def _key(e) -> str:
    # Mathematical literal equality is exact-rational; metadata is handled separately.
    def enc(x):
        if x[0] == 'lit':
            return ['lit', str(F(x[1]))]
        if x[0] == 'bit':
            return ['bit', x[1]]
        if x[0] == 'scale':
            return ['scale', str(F(x[1])), enc(x[2])]
        return [x[0]]+[enc(c) for c in x[1:]]
    return json.dumps(enc(e), separators=(',', ':'))


def rename(e, permutation: tuple[int, ...], work=None):
    """old bit i becomes new bit permutation[i]; this is not inferred causality."""
    _inc(work, 'rename_nodes')
    if e[0] == 'lit':
        return e
    if e[0] == 'bit':
        return K.bit(permutation[e[1]])
    if e[0] == 'scale':
        return K.scale(e[1], rename(e[2], permutation, work))
    return (e[0],)+(tuple(rename(c, permutation, work) for c in e[1:]))


def collect(e, work=None):
    """Exact additive collection; nonlinear subexpressions stay opaque atoms."""
    out: dict[str, tuple[Any, F]] = {}
    constant = F(0)
    def go(x, k):
        nonlocal constant
        _inc(work, 'collection_nodes')
        if x[0] == 'lit':
            constant += k*F(x[1])
        elif x[0] == 'add':
            go(x[1], k); go(x[2], k)
        elif x[0] == 'scale':
            go(x[2], k*F(x[1]))
        else:
            key = _key(x)
            old = out.get(key, (x, F(0)))
            out[key] = (x, old[1]+k)
    go(e, F(1))
    return constant, [(x,k) for x,k in out.values() if k]


def enclosure(e, cell, work=None):
    """Sound rational enclosure with exact cancellation of identical atoms."""
    lo, atoms = collect(e, work)
    hi = lo
    for x,k in atoms:
        a,b = K.interval(x, cell, work)
        lo += min(k*a,k*b); hi += max(k*a,k*b)
    return lo, hi


def rank_bounds(frame: Frame, cell, work=None):
    lo = hi = F(0)
    for soft in frame.request.soft:
        a,b = K.interval(soft.formula, cell, work)
        lo += F(soft.weight)*(1-b); hi += F(soft.weight)*(1-a)
    return lo,hi


def impossible(frame: Frame, cell, work=None):
    return any(K.interval(e, cell, work)[1] == 0 for e in frame.request.hard)


@dataclass(frozen=True)
class BandProof:
    frame: Frame
    cutoff: F
    bound: F
    tree: tuple

    def record(self) -> dict:
        return {'frame_record': self.frame.record(), 'cutoff': str(self.cutoff),
                'bound': str(self.bound), 'tree': self.tree}


def build_band(frame: Frame, cutoff, bound, work=None) -> BandProof:
    """Producer only: a bounded binary split proof, or a real violating leaf.

    A returned proof may cover an empty band. Application must establish
    current feasibility and sublevel containment separately.
    """
    cutoff,bound = _q(cutoff),_q(bound)
    visited = 0
    def go(cell):
        nonlocal visited
        visited += 1; _inc(work, 'producer_cells')
        if visited > MAX_PROOF_NODES:
            raise Rejected('Proof construction cap.')
        if impossible(frame, cell, work):
            return ('leaf','hard')
        if rank_bounds(frame, cell, work)[0] > cutoff:
            return ('leaf','rank')
        if enclosure(frame.difference, cell, work)[1] <= bound:
            return ('leaf','loss')
        if None not in cell:
            raise NoBandProof(f'Comparison fails at {cell}.')
        i = cell.index(None)
        return ('split', i, go(cell[:i]+(0,)+cell[i+1:]),
                            go(cell[:i]+(1,)+cell[i+1:]))
    return BandProof(frame, cutoff, bound, go((None,)*frame.request.nbits))


def verify_band(proof: BandProof, expected_frame: str, work=None) -> None:
    """Receiver traversal, not a call back to the producer or point sampling."""
    if type(proof) is not BandProof or type(proof.frame) is not Frame:
        raise Rejected('Band proof type.')
    proof.frame.__post_init__()
    if type(expected_frame) is not str or proof.frame.record() != expected_frame:
        raise Rejected('Old frame does not match independently supplied request.')
    _q(proof.cutoff); _q(proof.bound)
    visited = 0
    def check(tree,cell):
        nonlocal visited
        visited += 1; _inc(work, 'verified_proof_nodes')
        if visited > MAX_PROOF_NODES or type(tree) is not tuple or not tree:
            raise Rejected('Malformed proof or node cap.')
        if tree[0] == 'leaf' and len(tree) == 2:
            if tree[1] == 'hard' and impossible(proof.frame, cell, work):
                return
            if tree[1] == 'rank' and rank_bounds(proof.frame, cell, work)[0] > proof.cutoff:
                return
            if tree[1] == 'loss' and enclosure(proof.frame.difference, cell, work)[1] <= proof.bound:
                return
            raise Rejected('Unjustified certificate leaf.')
        if tree[0] != 'split' or len(tree) != 4:
            raise Rejected('Unknown proof instruction.')
        i = tree[1]
        if type(i) is not int or not 0 <= i < len(cell) or cell[i] is not None:
            raise Rejected('Split must exhaustively partition one unassigned bit.')
        check(tree[2], cell[:i]+(0,)+cell[i+1:])
        check(tree[3], cell[:i]+(1,)+cell[i+1:])
    check(proof.tree, (None,)*proof.frame.request.nbits)


def _permutation(value, n):
    if type(value) is not tuple or len(value) != n or any(type(v) is not int for v in value) or set(value) != set(range(n)):
        raise Rejected('A total bijective coordinate permutation is required.')


def _point(value, n):
    if type(value) is not tuple or len(value) != n or any(type(v) is not int or v not in (0,1) for v in value):
        raise Rejected('A complete Boolean feasible witness is required.')


def rank_drift(old: Frame, new: Frame, permutation, work=None) -> F:
    weights = Counter()
    for soft in old.request.soft:
        weights[_key(rename(soft.formula, permutation, work))] += F(soft.weight)
    for soft in new.request.soft:
        weights[_key(soft.formula)] -= F(soft.weight)
    _inc(work, 'rank_formula_groups', len(weights))
    return sum((max(v,F(0)) for v in weights.values()), F(0))


class CertificateCache:
    """Only locally verified immutable proof objects enter this cache.

    Its private memory is trusted. Rehydrating a cache must call admit again;
    a JSON report or hash never grants admission by itself. No cache eviction
    optimization is supplied, and matching/serialization costs are not free.
    """
    def __init__(self):
        self._entries: dict[str, tuple[BandProof,str]] = {}

    def admit(self, handle: str, proof: BandProof, expected_frame: str, work=None):
        if type(handle) is not str or not handle or handle in self._entries or len(self._entries) >= MAX_CACHE:
            raise Rejected('Fresh cache handle required; cap is 64 entries.')
        verify_band(proof, expected_frame, work)
        self._entries[handle] = (proof, expected_frame)

    def derive(self, handle: str, expected_old: str, new: Frame, permutation,
               witness, *, alpha=F(1), work=None) -> dict:
        if type(handle) is not str or handle not in self._entries:
            raise Rejected('Unknown verified cache entry.')
        proof, old_record = self._entries[handle]
        if type(expected_old) is not str or old_record != expected_old:
            raise Rejected('Stale or different old request record.')
        if type(new) is not Frame:
            raise Rejected('New request type.')
        new.__post_init__()
        new_record = new.record()
        _inc(work, 'record_characters_compared', len(old_record)+len(new_record))
        old = proof.frame
        if old.request.nbits != new.request.nbits or old.unit != new.unit:
            raise Rejected('Domain dimension/unit bridge is not supported here.')
        _permutation(permutation, new.request.nbits)
        _point(witness, new.request.nbits)
        alpha = _q(alpha)
        if alpha <= 0:
            raise Rejected('Positive loss scaling required.')
        # A deliberately sufficient syntactic entailment check. We never
        # assume a removed old hard premise still follows merely by its name.
        new_rows = {_key(e) for e in new.request.hard}
        for e in old.request.hard:
            _inc(work, 'hard_row_checks')
            if _key(rename(e, permutation, work)) not in new_rows:
                return {'status':'NO_REUSE_CERTIFICATE','reason':'old hard premise not syntactically retained'}
        for e in new.request.hard:
            _inc(work, 'witness_row_checks')
            if K.interval(e, witness, work) != (F(1),F(1)):
                raise Rejected('Current feasible witness violates a hard premise.')
        w_rank = rank_bounds(new, witness, work)[0]
        eta = rank_drift(old, new, permutation, work)
        threshold = w_rank+eta
        if threshold > proof.cutoff:
            return {'status':'NO_REUSE_CERTIFICATE','reason':'certified rank band too narrow',
                    'needed_cutoff':str(threshold),'available_cutoff':str(proof.cutoff)}
        old_d = rename(old.difference, permutation, work)
        delta = enclosure(K.sub(new.difference, K.scale(alpha, old_d)),
                          (None,)*new.request.nbits, work)[1]
        allowance = alpha*proof.bound+delta
        return {'status':'REUSE_CERTIFIED','version':VERSION,'old_frame_record':old_record,
                'new_frame_record':new_record,'permutation':list(permutation),'witness':list(witness),
                'feasibility':'NONEMPTY','coverage':'ALL_NEW_MINIMIZERS_WITHIN_OLD_CERTIFIED_SUBLEVEL',
                'rank_upper_from_witness':str(w_rank),'rank_drift_upper':str(eta),
                'needed_cutoff':str(threshold),'certified_cutoff':str(proof.cutoff),
                'old_bound':str(proof.bound),'positive_scale':str(alpha),'loss_drift_upper':str(delta),
                'bound':str(allowance),'non_deterioration':allowance<=0,
                'meaning':'conditional bound on the independently specified current difference, not an exact optimum value'}

    def receive(self, advertised: dict, *args, work=None, **kwargs) -> dict:
        """Recompute the requested report; no advertised numeric field is trusted."""
        actual = self.derive(*args,work=work,**kwargs)
        if type(advertised) is not dict or canonical(advertised) != canonical(actual):
            raise Rejected('Advertised report differs from recomputed current request.')
        return actual
