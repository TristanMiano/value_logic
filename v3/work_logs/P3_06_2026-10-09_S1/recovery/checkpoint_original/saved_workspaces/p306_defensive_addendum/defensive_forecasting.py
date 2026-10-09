"""Standalone P3-06 continuation: one scalar forecast for finite expert/calibration duties.

New supplementary code, NOT a reconstruction of an unavailable prior run.
Exact rational arithmetic; Python 3.10+, standard library only.
No default scores for pending labels. No general LI or optimal reasoning claim.
Contributor: ChatGPT (GPT-6 Astra Pro).
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from typing import Mapping


def rational(x) -> F:
    if isinstance(x, bool) or not isinstance(x, (int, str, F)):
        raise ValueError('Use integers, rational strings or Fraction, never floats/bools.')
    return F(x)


def squared_norm(xs) -> F:
    return sum((x*x for x in xs), F(0))


@dataclass(frozen=True)
class Prediction:
    query: str
    scope: str
    probability: F
    expert_values: tuple[F, ...]
    weight: F
    features: tuple[F, ...]
    score: F
    allowance: F
    tolerance_met: bool
    bisections: int
    score_evaluations: int


class Forecaster:
    """One outstanding request per instance; use DelayedPool for delayed feedback.

    A exhausted root-search budget returns the actual, charged potential allowance,
    not a fictitious successful root. Storage and rational bit growth are not capped.
    """
    def __init__(self, experts: tuple[str, ...], bins: int = 4,
                 alpha=1, beta=1, scope: str = 'P3-06-defensive-addendum-v1'):
        if not experts or len(set(experts)) != len(experts):
            raise ValueError('Supply distinct nonempty expert names.')
        if any(not isinstance(e, str) or not e for e in experts):
            raise ValueError('Invalid expert name.')
        if isinstance(bins, bool) or not isinstance(bins, int) or not 1 <= bins <= 64:
            raise ValueError('bins must be an integer between 1 and 64.')
        self.alpha, self.beta = rational(alpha), rational(beta)
        if self.alpha <= 0 or self.beta <= 0 or not scope:
            raise ValueError('Positive feature scales and a nonempty scope are required.')
        self.experts, self.bins, self.scope = experts, bins, scope
        self.residual = [F(0)] * (len(experts)+bins+1)
        self.variance = F(0)
        self.allowance = F(0)
        self.own_loss = F(0)
        self.expert_losses = [F(0)] * len(experts)
        self.expert_distances = [F(0)] * len(experts)
        self.pending: Prediction | None = None
        self.used: set[str] = set()
        self.history: list[tuple[Prediction, int]] = []

    def _features(self, p: F, qs: tuple[F, ...], w: F) -> tuple[F, ...]:
        expert = tuple(w*self.alpha*(q-p) for q in qs)
        tent = tuple(w*self.beta*max(F(0), 1-self.bins*abs(p-F(j,self.bins)))
                     for j in range(self.bins+1))
        return expert+tent

    def _score(self, p: F, qs: tuple[F, ...], w: F):
        phi = self._features(p, qs, w)
        s = sum((r*f for r,f in zip(self.residual,phi)), F(0))
        s += F(1,2)*(1-2*p)*squared_norm(phi)
        return s, phi

    def issue(self, query: str, experts: Mapping[str, object], weight=1,
              tolerance=F(1,1024), max_bisections: int=40) -> Prediction:
        if self.pending is not None:
            raise ValueError('This copy already has outstanding feedback.')
        if not isinstance(query,str) or not query or query in self.used:
            raise ValueError('Query identity must be new and nonempty.')
        if set(experts) != set(self.experts):
            raise ValueError('The forecast must give exactly the declared experts.')
        qs = tuple(rational(experts[i]) for i in self.experts)
        if any(q < 0 or q > 1 for q in qs):
            raise ValueError('Expert probabilities must lie in [0,1].')
        w, tol = rational(weight), rational(tolerance)
        if w < 0 or tol <= 0:
            raise ValueError('Nonnegative weight and positive tolerance required.')
        if (isinstance(max_bisections,bool) or not isinstance(max_bisections,int)
                or max_bisections < 0):
            raise ValueError('Root-search budget must be a nonnegative integer.')
        s0, phi0 = self._score(F(0),qs,w)
        evaluations, steps = 1, 0
        if s0 <= 0:
            p,s,phi = F(0),s0,phi0
            boundary=True
        else:
            s1,phi1 = self._score(F(1),qs,w)
            evaluations += 1
            if s1 >= 0:
                p,s,phi = F(1),s1,phi1
                boundary=True
            else:
                boundary=False
                lo,hi = F(0),F(1)
                p = F(1,2)
                s,phi = self._score(p,qs,w)
                evaluations += 1
                while abs(s) > tol and steps < max_bisections:
                    if s > 0:
                        lo=p
                    else:
                        hi=p
                    p=(lo+hi)/2
                    s,phi=self._score(p,qs,w)
                    evaluations += 1
                    steps += 1
        # Exact worst-case increment of the corrected potential over y in {0,1}.
        allowance=2*max(F(0),(1-p)*s,-p*s)
        pred=Prediction(query,self.scope,p,qs,w,phi,s,allowance,
                        boundary or abs(s)<=tol,steps,evaluations)
        self.pending=pred
        self.used.add(query)
        return pred

    def reveal(self, query: str, outcome: int) -> Prediction:
        if isinstance(outcome,bool) or not isinstance(outcome,int) or outcome not in (0,1):
            raise ValueError('Outcome must be integer 0 or 1, not an unresolved label.')
        pred=self.pending
        if pred is None or pred.query != query:
            raise ValueError('Feedback must match the outstanding query.')
        p=pred.probability
        e=F(outcome)-p
        self.residual=[r+e*f for r,f in zip(self.residual,pred.features)]
        self.variance += p*(1-p)*squared_norm(pred.features)
        self.allowance += pred.allowance
        self.own_loss += pred.weight*e*e
        for i,q in enumerate(pred.expert_values):
            self.expert_losses[i] += pred.weight*(q-outcome)**2
            self.expert_distances[i] += pred.weight*(q-p)**2
        self.history.append((pred,outcome))
        self.pending=None
        if squared_norm(self.residual) > self.variance+self.allowance:
            raise AssertionError('Potential bound violated.')
        for i in range(len(self.experts)):
            exact=2*self.residual[i]/self.alpha-self.expert_distances[i]
            if self.own_loss-self.expert_losses[i] != exact:
                raise AssertionError('Weighted regret identity violated.')
        return pred


class DelayedPool:
    """Ordinary free-copy reduction; scores only revealed outcomes.

    The number of live copies is charged. No theorem on an unseen suffix is
    manufactured from a good score on only the already resolved subset.
    """
    def __init__(self, experts: tuple[str,...], bins=4, alpha=1, beta=1,
                 scope='P3-06-defensive-addendum-v1'):
        self.args=(experts,bins,alpha,beta,scope)
        self.copies: list[Forecaster]=[]
        self.pending: dict[str,int]={}
        self.used: set[str]=set()

    def issue(self, query, experts, weight=1, tolerance=F(1,1024), max_bisections=40):
        if query in self.used:
            raise ValueError('Query already used in this pool.')
        index=next((i for i,c in enumerate(self.copies) if c.pending is None),None)
        if index is None:
            index=len(self.copies)
            self.copies.append(Forecaster(*self.args))
        pred=self.copies[index].issue(query,experts,weight,tolerance,max_bisections)
        self.pending[query]=index
        self.used.add(query)
        return pred

    def reveal(self, query, outcome):
        if query not in self.pending:
            raise ValueError('Unknown or already resolved query.')
        index=self.pending[query]
        pred=self.copies[index].reveal(query,outcome)
        del self.pending[query]
        return pred

    def audit(self):
        if not self.copies:
            return {'copies':0,'settled':0,'pending':0,'bound_squared':F(0)}
        k=len(self.copies)
        R=[sum((c.residual[j] for c in self.copies),F(0))
           for j in range(len(self.copies[0].residual))]
        B=k*sum((c.variance+c.allowance for c in self.copies),F(0))
        if squared_norm(R)>B:
            raise AssertionError('Delayed-copy bound violated.')
        own=sum((c.own_loss for c in self.copies),F(0))
        for i in range(len(self.args[0])):
            other=sum((c.expert_losses[i] for c in self.copies),F(0))
            regret=own-other
            if regret>0 and regret**2*self.copies[0].alpha**2>4*B:
                raise AssertionError('Aggregated expert-regret bound violated.')
        return {'copies':k,'settled':sum(len(c.history) for c in self.copies),
                'pending':len(self.pending),'bound_squared':B,'residual':tuple(R)}
