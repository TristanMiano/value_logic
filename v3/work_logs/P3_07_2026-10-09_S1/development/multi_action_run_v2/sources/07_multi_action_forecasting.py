"""P3-07 multi-action defensive forecasting: bounded DEVELOPMENT prototype.

The P3-06 potential identity is reused with new continuous action features.
This file does not alter P3-06 code/evidence. Each paid exact action row names
a guaranteed checked service with a known flat fee. Later full feedback is
charged too; it is never a free truth oracle. The operation ledger is a
declared bounded rational-primitive model, not Python CPU instructions.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt

VERSION = "p307-multi-action-potential-v2"
MAX_ACTIONS, MAX_ROUNDS, MAX_ROOT_STEPS = 8, 128, 64
MAX_RATIONAL_BITS, MAX_QUERY_CHARS = 8192, 128


class Rejected(ValueError):
    pass


class Exhausted(RuntimeError):
    pass


def rational(x):
    if type(x) not in (int, F):
        raise Rejected("Bounded exact int/Fraction required.")
    x = F(x)
    if max(x.numerator.bit_length(), x.denominator.bit_length()) > MAX_RATIONAL_BITS:
        raise Rejected("Bounded rational primitive component cap exceeded.")
    return x


class Work:
    """Counts prepaid bounded arithmetic/read/write bundles and hard-caps them.

    A rational arithmetic primitive accepts components of at most 8192 bits;
    its temporary exact arithmetic is bounded accordingly. This abstraction
    deliberately does not equate rational operations with machine cycles.
    Fixed-size loop bundles overpay some branches rather than omitting them.
    """
    def __init__(self, limit=2_000_000):
        if type(limit) is not int or not 0 <= limit <= 10_000_000:
            raise Rejected("Work cap required.")
        self.limit, self.total, self.counts, self.peak_bits = limit, 0, {}, 0

    def pay(self, name, count):
        if type(count) is not int or count < 0:
            raise Rejected("Nonnegative primitive bundle required.")
        if self.total + count > self.limit:
            raise Exhausted("No remaining budget for " + name)
        self.total += count
        self.counts[name] = self.counts.get(name, 0) + count

    def observe(self, values):
        for x in values:
            x = rational(x)
            self.peak_bits = max(self.peak_bits, abs(x.numerator).bit_length(), x.denominator.bit_length())

    def record(self):
        return {"limit":self.limit,"total":self.total,"counts":dict(self.counts),
                "peak_component_bits":self.peak_bits}


def projection(costs, eta, work):
    """Exact sorting-and-threshold simplex projection; deterministic ties."""
    if type(costs) is not tuple or not 2 <= len(costs) <= MAX_ACTIONS:
        raise Rejected("Finite immutable action costs required.")
    cc, eta = tuple(rational(x) for x in costs), rational(eta)
    if eta <= 0:
        raise Rejected("Positive smoothing required.")
    a = len(cc)
    work.pay("projection_arithmetic_sort_read_write", a*a + 14*a + 8)
    v = tuple(-c / eta for c in cc)
    ordered = sorted(v, reverse=True)
    total, threshold, active = F(0), None, 0
    for k, value in enumerate(ordered, 1):
        total += value
        tau = (total - 1) / k
        if value > tau:
            threshold, active = tau, k
    if threshold is None:
        raise AssertionError("Simplex projection has no active coordinate.")
    q = tuple(max(F(0), x - threshold) for x in v)
    if sum(q) != 1:
        raise AssertionError("Projection mass differs from one.")
    work.observe(v + q + (threshold,))
    return q, active


def dyadic_round(q, bits, work):
    if type(q) is not tuple or not 2 <= len(q) <= MAX_ACTIONS or type(bits) is not int or not 0 <= bits <= 32:
        raise Rejected("Bounded mixture and fair-bit count required.")
    qq = tuple(rational(x) for x in q)
    if any(x < 0 for x in qq) or sum(qq) != 1:
        raise Rejected("A probability simplex point is required.")
    a, d = len(qq), 1 << bits
    work.pay("dyadic_rounding_arithmetic_sort", a*a + 12*a + 8)
    raw = [d*x for x in qq]
    slots = [x.numerator // x.denominator for x in raw]
    fractions = [x-n for x,n in zip(raw,slots)]
    remaining = d-sum(slots)
    order = sorted(range(a), key=lambda i:(-fractions[i],i))
    for i in order[:remaining]:
        slots[i] += 1
    nu = tuple(F(n,d) for n in slots)
    tv = sum((abs(x-y) for x,y in zip(nu,qq)),F(0))/2
    bound = max((F(r*(a-r),a*d) for r in range(min(a-1,d)+1)),default=F(0))
    if tv > bound or sum(slots) != d:
        raise AssertionError("Dyadic mass/TV bound failed.")
    work.observe(nu+(tv,bound))
    return tuple(slots), nu, tv, bound


def choose_slots(slots, bits, draw, work):
    """Paid bounded lookup. The caller funds random bits before producing draw."""
    if type(bits) is not int or not 0 <= bits <= 32 or type(slots) is not tuple or not 2 <= len(slots) <= MAX_ACTIONS:
        raise Rejected("The public lookup requires bounded action and bit counts.")
    work.pay("cumulative_selection", 2*len(slots) + 2)
    if any(type(x) is not int or not 0 <= x <= 1 << bits for x in slots) or sum(slots) != 1 << bits:
        raise Rejected("Exact dyadic slots required.")
    if type(draw) is not int or not 0 <= draw < 1 << bits:
        raise Rejected("An admitted bounded fair-bit draw is required.")
    total = 0
    for i, count in enumerate(slots):
        total += count
        if draw < total:
            return i
    raise AssertionError("Categorical lookup failed.")


@dataclass(frozen=True)
class Table:
    rows: tuple[tuple[F,F], ...]
    eta: F

    def __post_init__(self):
        if type(self.rows) is not tuple or not 2 <= len(self.rows) <= MAX_ACTIONS:
            raise Rejected("Bounded complete cost rows required.")
        for row in self.rows:
            if type(row) is not tuple or len(row) != 2:
                raise Rejected("Two outcome costs per fixed action required.")
            for x in row:
                rational(x)
        if rational(self.eta) <= 0:
            raise Rejected("Positive eta required.")

    @property
    def slopes(self):
        return tuple(r[1]-r[0] for r in self.rows)

    def costs(self,p):
        return tuple(r[0]+(r[1]-r[0])*p for r in self.rows)


@dataclass(frozen=True)
class Issue:
    query: str
    scope: str
    p: F
    weight: F
    expert: F
    table: Table
    mixture: tuple[F,...]
    feature: tuple[F,...]
    score: F
    allowance: F
    tolerance: F
    tolerance_met: bool
    root_steps: int
    evaluations: int
    lipschitz: F


def sqrt_upper(x, bits=32):
    x = rational(x)
    if x < 0:
        raise Rejected("Nonnegative square-root target required.")
    v = x.numerator << (2*bits)
    z = isqrt(v // x.denominator)
    if z*z*x.denominator < v:
        z += 1
    return F(z,1 << bits)


class Forecaster:
    """One pending prediction, fixed identities/scales, all-settled prototype."""
    def __init__(self, actions=4, bins=4, gamma=F(1,100), scope="p307-four-actions-v1", work=None):
        if type(actions) is not int or not 2 <= actions <= MAX_ACTIONS or type(bins) is not int or not 1 <= bins <= 16:
            raise Rejected("Fixed action/grid dimensions required.")
        if rational(gamma) <= 0 or type(scope) is not str or not scope or len(scope)>256 or not scope.isascii():
            raise Rejected("Positive fixed scale and bounded scope required.")
        self.actions,self.bins,self.gamma,self.scope=actions,bins,F(gamma),scope
        self.work=work if type(work) is Work else Work()
        self.dimension=1+bins+1+actions
        self.residual=(F(0),)*self.dimension
        self.variance=self.allowances=self.slack=self.mixed=F(0)
        self.fixed=(F(0),)*actions
        self.gaps=(F(0),)*actions
        self.pending=None
        self.used=set()
        self.settled=0

    def _features(self,p,expert,w,table):
        self.work.pay("feature_arithmetic_read_write",10*self.dimension+6*self.actions)
        costs=table.costs(p)
        q,_=projection(costs,table.eta,self.work)
        slopes=table.slopes
        mean=sum((x*d for x,d in zip(q,slopes)),F(0))
        phi=(w*(expert-p),)+tuple(w*max(F(0),1-abs(self.bins*p-j)) for j in range(self.bins+1))
        phi+=tuple(self.gamma*w*(mean-d) for d in slopes)
        self.work.observe(costs+phi)
        return phi,q

    def _score(self,p,expert,w,table):
        phi,q=self._features(p,expert,w,table)
        self.work.pay("score_arithmetic_read_write",5*self.dimension+8)
        score=sum((r*f for r,f in zip(self.residual,phi)),F(0))+(1-2*p)*sum((f*f for f in phi),F(0))/2
        self.work.observe((score,))
        return score,phi,q

    def _lipschitz(self,w,table):
        self.work.pay("lipschitz_bound_arithmetic",12*self.actions+8*self.dimension)
        slopes=table.slopes
        delta=max(slopes)-min(slopes)
        mean=sum(slopes,F(0))/self.actions
        centered=sum(((d-mean)**2 for d in slopes),F(0))
        bounds=[(w,w)]+[(w,w*self.bins)]*(self.bins+1)
        bounds += [(self.gamma*w*delta,self.gamma*w*centered/table.eta)]*self.actions
        value=sum((abs(r)*lip+bound*bound+bound*lip for r,(bound,lip) in zip(self.residual,bounds)),F(0))
        self.work.observe((value,))
        return value

    def issue(self,query,table,expert=F(1,2),weight=F(1),tolerance=F(1,1024),root_cap=32):
        if self.pending is not None or self.settled >= MAX_ROUNDS:
            raise Rejected("Pending feedback or finite run cap.")
        if type(query) is not str or not query or len(query)>MAX_QUERY_CHARS or not query.isascii() or query in self.used:
            raise Rejected("New bounded ASCII query identity required.")
        if type(table) is not Table or len(table.rows)!=self.actions:
            raise Rejected("Cost table identity count differs.")
        expert,w,tol=rational(expert),rational(weight),rational(tolerance)
        if not 0 <= expert <= 1 or w < 0 or tol <= 0 or type(root_cap) is not int or not 0 <= root_cap <= MAX_ROOT_STEPS:
            raise Rejected("Invalid forecast/root parameters.")
        self.work.pay("issue_validation_and_identity_words",64+(len(query)+7)//8)
        lip=self._lipschitz(w,table)
        score,phi,q=self._score(F(0),expert,w,table)
        evaluations,steps=1,0
        if score<=0:
            p=F(0)
        else:
            score,phi,q=self._score(F(1),expert,w,table)
            evaluations+=1
            if score>=0:
                p=F(1)
            else:
                lo,hi,p=F(0),F(1),F(1,2)
                score,phi,q=self._score(p,expert,w,table)
                evaluations+=1
                while abs(score)>tol and steps<root_cap:
                    self.work.pay("root_bracket_update",6)
                    if score>0:lo=p
                    else:hi=p
                    p=(lo+hi)/2
                    score,phi,q=self._score(p,expert,w,table)
                    evaluations+=1;steps+=1
        self.work.pay("allowance_and_immutable_issue_write",12+3*self.dimension+4*self.actions)
        allowance=2*max(F(0),(1-p)*score,-p*score)
        met=(p==0 and score<=0) or (p==1 and score>=0) or abs(score)<=tol
        issue=Issue(query,self.scope,p,w,expert,table,q,phi,score,allowance,tol,met,steps,evaluations,lip)
        self.used.add(query);self.pending=issue
        return issue

    def settle(self,query,outcome,scope):
        p=self.pending
        if p is None or query!=p.query or scope!=p.scope or type(outcome) is not int or outcome not in (0,1):
            raise Rejected("Only the matching admitted binary answer may settle.")
        self.work.pay("settlement_update_and_bound_checks",30*self.dimension+20*self.actions+32)
        error=outcome-p.p
        residual=tuple(r+error*f for r,f in zip(self.residual,p.feature))
        variance=self.variance+p.p*(1-p.p)*sum((f*f for f in p.feature),F(0))
        allowances=self.allowances+p.allowance
        norm=sum((r*r for r in residual),F(0))
        if norm>variance+allowances:
            raise AssertionError("Enlarged-feature potential bound failed.")
        costs=p.table.costs(F(outcome));predicted=p.table.costs(p.p)
        mix=sum((q*c for q,c in zip(p.mixture,costs)),F(0))
        predicted_mix=sum((q*c for q,c in zip(p.mixture,predicted)),F(0))
        mixed=self.mixed+p.weight*mix
        fixed=tuple(x+p.weight*c for x,c in zip(self.fixed,costs))
        gaps=tuple(x+p.weight*(predicted_mix-c) for x,c in zip(self.gaps,predicted))
        slack=self.slack+p.weight*p.table.eta*F(self.actions-1,4*self.actions)
        for a in range(self.actions):
            if mixed-fixed[a]!=gaps[a]+residual[-self.actions+a]/self.gamma or gaps[a]>slack:
                raise AssertionError("Multi-action regret decomposition/allowance failed.")
        # The returned certificate is part of this transaction. In particular,
        # individually bounded variance and allowances can have an over-cap sum.
        # Validate that sum and every derived readout before consuming pending.
        prepared=self._report_for(residual,variance,allowances,slack,mixed,fixed,gaps,
                                  self.settled+1,False)
        derived=(prepared['B'],prepared['generic_action_bound'])+prepared['action_regrets']+prepared['retained_gap_bounds']
        self.work.observe(residual+(variance,allowances,slack,mixed,norm)+fixed+gaps+derived)
        prepared['work']=self.work.record()
        self.residual,self.variance,self.allowances=residual,variance,allowances
        self.mixed,self.fixed,self.gaps,self.slack=mixed,fixed,gaps,slack
        self.pending=None;self.settled+=1
        return prepared

    def report(self):
        """Harness export; paid settlement already validated the retained state."""
        return self._report_for(self.residual,self.variance,self.allowances,self.slack,
                    self.mixed,self.fixed,self.gaps,self.settled,self.pending is not None)

    def _report_for(self,residual,variance,allowances,slack,mixed,fixed,gaps,settled,pending):
        bound=rational(variance+allowances)
        root=rational(sqrt_upper(bound)/self.gamma)
        return {"version":VERSION,"settled":settled,"pending":pending,
                "residual":residual,"variance":variance,"allowances":allowances,
                "B":bound,"mixed_cost":mixed,"fixed_costs":fixed,
                "action_regrets":tuple(rational(mixed-x) for x in fixed),
                "predicted_gaps":gaps,"smoothing_slack":slack,
                "generic_action_bound":rational(slack+root),
                "retained_gap_bounds":tuple(rational(g+root) for g in gaps),
                "work":self.work.record(),
                "scope":"Mixed action costs on admitted labels; all-in and sampling corrections are separate."}
