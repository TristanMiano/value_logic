#!/usr/bin/env python3
"""Exact finite coverage margins under coupled linear-rank weights.

P3-05 S3 DEVELOPMENT. Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-08.
The primal/dual receiver checks optimality arithmetically. The small capped
basis search is not a general optimized LP solver or a learned rank model.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations,product
from pathlib import Path
import importlib.util,sys
sys.dont_write_bytecode=True
_NAME='_p305_portfolio_base'
if _NAME in sys.modules:M=sys.modules[_NAME]
else:
    sp=importlib.util.spec_from_file_location(_NAME,Path(__file__).with_name('05_counterfactual_transport.py'))
    if sp is None or sp.loader is None:raise ImportError('Missing prior band verifier.')
    M=importlib.util.module_from_spec(sp);sys.modules[_NAME]=M;sp.loader.exec_module(M)
K=M.K
VERSION='p305-rank-region-v1'
MAX_STATES=16
MAX_DIMENSION=3
MAX_EXTRA_ROWS=16
MAX_TRIALS=20000


def inc(w,k,n=1):
    if w is not None:w[k]=w.get(k,0)+n


def rational(q,work=None):
    if isinstance(q,bool) or not isinstance(q,(str,int,F)):raise ValueError('Exact rational required.')
    value=F(q)
    bits=max(abs(value.numerator).bit_length(),value.denominator.bit_length())
    if bits>4096:raise ValueError('Computed rational component cap.')
    if work is not None:work['max_rational_component_bits']=max(work.get('max_rational_component_bits',0),bits)
    return value


def dot(a,b,work=None):
    if len(a)!=len(b):raise ValueError('Vector dimension mismatch.')
    total=F(0)
    for x,y in zip(a,b):inc(work,'rational_multiply_adds');total=rational(total+x*y,work)
    return total


@dataclass(frozen=True)
class Problem:
    scope: str
    states: tuple[str,...]
    features: tuple[tuple[F,...],...]
    covered: tuple[int,...]
    lower: tuple[F,...]
    upper: tuple[F,...]
    extra_rows: tuple[tuple[tuple[F,...],F],...]
    weight_witness: tuple[F,...]

    def validate(self):
        if type(self.scope) is not str or not self.scope or len(self.scope)>131072:raise ValueError('Scope identity/cap.')
        if type(self.states) is not tuple or not 1<=len(self.states)<=MAX_STATES or any(type(s)is not str or not s for s in self.states) or len(set(self.states))!=len(self.states):raise ValueError('Distinct capped state identities required.')
        if type(self.lower) is not tuple or not 1<=len(self.lower)<=MAX_DIMENSION:raise ValueError('Rank dimension cap.')
        n=len(self.lower)
        def vector(v):
            if type(v)is not tuple or len(v)!=n:raise ValueError('Immutable rational vector required.')
            return tuple(K.rational(x) for x in v)
        lo=vector(self.lower);hi=vector(self.upper);w=vector(self.weight_witness)
        if any(l>u for l,u in zip(lo,hi)):raise ValueError('Reversed weight box.')
        if type(self.features)is not tuple or len(self.features)!=len(self.states):raise ValueError('Feature count.')
        for v in self.features:vector(v)
        if type(self.covered)is not tuple or any(type(i)is not int or not 0<=i<len(self.states) for i in self.covered) or len(set(self.covered))!=len(self.covered):raise ValueError('Covered case index set.')
        if type(self.extra_rows)is not tuple or len(self.extra_rows)>MAX_EXTRA_ROWS:raise ValueError('Extra row cap.')
        for row in self.extra_rows:
            if type(row)is not tuple or len(row)!=2:raise ValueError('Extra row type.')
            a,b=row;vector(a);K.rational(b)
        if not self.feasible(w,validate=False):raise ValueError('Weight witness is infeasible.')

    def feasible(self,w,*,validate=True,work=None):
        if validate:self.validate()
        if type(w)is not tuple or len(w)!=len(self.lower):raise ValueError('Weight vector dimension.')
        w=tuple(rational(x,work) for x in w)
        return (all(F(l)<=x<=F(u) for l,u,x in zip(self.lower,self.upper,w)) and
            all(dot(tuple(F(x) for x in a),w,work)<=F(b) for a,b in self.extra_rows))

    def record(self):
        self.validate()
        return M.canonical({'version':VERSION,**self.__dict__})


def constraints(problem:Problem,outside:int):
    problem.validate();d=len(problem.lower)
    if type(outside)is not int or outside in problem.covered or not 0<=outside<len(problem.states):raise ValueError('Outside-case identity.')
    if not problem.covered:raise ValueError('No certified domain.')
    rows=[]
    for i,(lo,hi) in enumerate(zip(problem.lower,problem.upper)):
        e=tuple(F(int(j==i)) for j in range(d))
        rows.append((e+(F(0),),F(hi)));rows.append((tuple(-x for x in e)+(F(0),),-F(lo)))
    rows.extend((tuple(F(x) for x in a)+(F(0),),F(b)) for a,b in problem.extra_rows)
    diffs=[];radius=F(0)
    for g in problem.covered:
        v=tuple(F(x)-F(y) for x,y in zip(problem.features[outside],problem.features[g]));diffs.append(v)
        lo=sum(min(x*F(a),x*F(b)) for x,a,b in zip(v,problem.lower,problem.upper))
        hi=sum(max(x*F(a),x*F(b)) for x,a,b in zip(v,problem.lower,problem.upper))
        radius=max(radius,abs(lo),abs(hi));rows.append((v+(F(-1),),F(0)))
    e=(F(0),)*d+(F(1),);rows.extend(((e,radius),(tuple(-x for x in e),radius)))
    return tuple(rows),tuple(diffs),radius


def solve(matrix,rhs,work=None):
    """Small exact square elimination, returning None on singularity."""
    n=len(rhs)
    if len(matrix)!=n or any(len(r)!=n for r in matrix):raise ValueError('Square linear system required.')
    a=[list(map(F,r))+[F(b)] for r,b in zip(matrix,rhs)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]),None)
        if pivot is None:return None
        a[j],a[pivot]=a[pivot],a[j];q=a[j][j]
        a[j]=[rational(x/q,work) for x in a[j]];inc(work,'elimination_pivots')
        for i in range(n):
            if i==j:continue
            q=a[i][j]
            if q:
                a[i]=[rational(x-q*y,work) for x,y in zip(a[i],a[j])];inc(work,'elimination_row_updates')
    return tuple(r[-1] for r in a)


@dataclass(frozen=True)
class MarginCertificate:
    outside: int
    point: tuple[F,...]
    multipliers: tuple[F,...]
    margin: F

    def record(self):return self.__dict__


def verify_margin(problem,certificate,work=None):
    if type(certificate)is not MarginCertificate:raise ValueError('Margin certificate type.')
    rows,diffs,_=constraints(problem,certificate.outside);n=len(problem.lower)+1
    if type(certificate.point)is not tuple or len(certificate.point)!=n:raise ValueError('Primal point dimension.')
    if type(certificate.multipliers)is not tuple or len(certificate.multipliers)!=len(rows):raise ValueError('Dual vector dimension.')
    u=tuple(rational(x,work) for x in certificate.point);mu=tuple(rational(x,work) for x in certificate.multipliers)
    if any(x<0 for x in mu):raise ValueError('Dual multipliers must be nonnegative.')
    for a,b in rows:
        inc(work,'primal_constraint_checks')
        if dot(a,u,work)>b:raise ValueError('Infeasible primal witness.')
    expected=(F(0),)*(n-1)+(F(-1),)
    actual=tuple(dot(tuple(a[j] for a,b in rows),mu,work) for j in range(n))
    if actual!=expected:raise ValueError('Dual stationarity does not prove the objective.')
    lower=-dot(tuple(b for a,b in rows),mu,work)
    if u[-1]!=lower or rational(certificate.margin,work)!=lower:raise ValueError('Primal and dual bounds do not match.')
    if u[-1]!=max(dot(v,u[:-1],work) for v in diffs):raise ValueError('Reported attaining point does not attain the selection gap.')
    inc(work,'margin_certificates_verified')
    return lower


def search_margin(problem,outside,*,max_trials=MAX_TRIALS,work=None):
    rows,diffs,radius=constraints(problem,outside);n=len(problem.lower)+1
    if type(max_trials)is not int or not 0<=max_trials<=MAX_TRIALS:raise ValueError('Basis-search budget.')
    c=(F(0),)*(n-1)+(F(-1),);trials=0
    for indices in combinations(range(len(rows)),n):
        if trials>=max_trials:return {'status':'SEARCH_BUDGET_EXHAUSTED','trials':trials,'certificate':None}
        trials+=1;inc(work,'basis_trials');matrix=tuple(rows[i][0] for i in indices)
        u=solve(matrix,tuple(rows[i][1] for i in indices),work)
        if u is None or any(dot(a,u,work)>b for a,b in rows):continue
        mu=solve(tuple(zip(*matrix)),c,work)
        if mu is None or any(x<0 for x in mu):continue
        full=[F(0)]*len(rows)
        for i,q in zip(indices,mu):full[i]=q
        proof=MarginCertificate(outside,u,tuple(full),u[-1]);verify_margin(problem,proof,work)
        return {'status':'CERTIFICATE_FOUND','trials':trials,'certificate':proof}
    # The receiver does not rely on completeness of the basis enumeration.
    return {'status':'NO_CERTIFICATE_FOUND','trials':trials,'certificate':None}


@dataclass(frozen=True)
class CoverageProof:
    problem_record: str
    margins: tuple[MarginCertificate,...]
    def record(self):return {'problem_record':self.problem_record,'margins':[m.record() for m in self.margins]}


def verify(problem,proof,expected_record,work=None):
    if type(problem)is not Problem or type(proof)is not CoverageProof:raise ValueError('Coverage input types.')
    record=problem.record()
    if type(expected_record)is not str or record!=expected_record or proof.problem_record!=record:raise ValueError('Coverage request record mismatch.')
    inc(work,'record_characters_compared',2*len(record))
    if type(proof.margins)is not tuple:raise ValueError('Immutable margin family required.')
    if not problem.covered:raise ValueError('No certified domain to transport.')
    outside=tuple(i for i in range(len(problem.states)) if i not in problem.covered)
    if any(type(m)is not MarginCertificate for m in proof.margins) or tuple(m.outside for m in proof.margins)!=outside:raise ValueError('Every outside case must appear exactly once, in canonical order.')
    if not outside:return {'status':'FULL_DOMAIN_ALREADY_COVERED','margin':None,'coverage':True,'outside_count':0}
    values=[verify_margin(problem,p,work) for p in proof.margins];margin=min(values)
    result={'status':'ROBUST_COVERAGE_CERTIFIED' if margin>0 else 'COVERAGE_REFUTED','margin':str(margin),'coverage':margin>0,'outside_count':len(outside),'meaning':'Coverage by the supplied certified domain, not a general proof/refutation of actual action quality.'}
    if margin<=0:
        worst=proof.margins[values.index(margin)];w=tuple(F(x) for x in worst.point[:-1])
        scores=[dot(tuple(F(x) for x in v),w,work) for v in problem.features];m=min(scores)
        winners=[i for i,x in enumerate(scores) if x==m]
        if not any(i not in problem.covered for i in winners):raise AssertionError('Counterexample does not expose an uncovered winner.')
        result['counterexample']={'weights':tuple(str(x) for x in w),'winners':winners,'ranks':tuple(str(x) for x in scores)}
    return result


def search(problem,*,max_trials_per_case=MAX_TRIALS,work=None):
    problem.validate()
    if not problem.covered:return {'status':'NO_CERTIFIED_DOMAIN','proof':None,'completed':()}
    completed=[]
    for j in range(len(problem.states)):
        if j in problem.covered:continue
        result=search_margin(problem,j,max_trials=max_trials_per_case,work=work)
        if result['certificate'] is None:return {'status':'SEARCH_INCOMPLETE','proof':None,'completed':tuple(completed),'uncompleted_case':j,'search_status':result['status']}
        completed.append(result['certificate'])
    proof=CoverageProof(problem.record(),tuple(completed));report=verify(problem,proof,problem.record(),work)
    return {'status':'VERIFIED','proof':proof,'report':report}


def from_band(band,expected_old_record,lower,upper,extra_rows,weight_witness,work=None):
    """Recompute all profiles from a verified fixed old Boolean/soft-clause source."""
    M.verify_band(band,expected_old_record,work);frame=band.frame;n=frame.request.nbits
    if not 1<=len(frame.request.soft)<=MAX_DIMENSION:raise ValueError('Adapter requires one to three unchanged soft formulas.')
    if type(lower)is not tuple or any(K.rational(x)<=0 for x in lower):raise ValueError('Soft-clause adapter requires a strictly positive lower weight box.')
    states=[];features=[];covered=[]
    for x in product((0,1),repeat=n):
        inc(work,'source_assignments_enumerated')
        if any(K.interval(h,x,work)[0]!=1 for h in frame.request.hard):continue
        v=tuple(F(1)-K.interval(s.formula,x,work)[0] for s in frame.request.soft)
        if sum(s.weight*a for s,a in zip(frame.request.soft,v))<=band.cutoff:covered.append(len(states))
        states.append(''.join(map(str,x)));features.append(v)
        if len(states)>MAX_STATES:raise ValueError('Finite profile adapter state cap.')
    p=Problem(M.canonical({'old_record':expected_old_record,'old_band_cutoff':band.cutoff,'old_loss_bound':band.bound,'meaning':'Only rank weights change; source, clauses and loss remain fixed.'}),tuple(states),tuple(features),tuple(covered),lower,upper,extra_rows,weight_witness)
    p.validate();return p


def receive_band_region(band,expected_old_record,lower,upper,extra_rows,weight_witness,proof,work=None):
    problem=from_band(band,expected_old_record,lower,upper,extra_rows,weight_witness,work)
    result=verify(problem,proof,problem.record(),work)
    result['old_loss_bound']=str(band.bound)
    result['loss_bound_transported']=result['coverage']
    result['loss_scope']='Unchanged independently specified old loss difference, for every new rank minimizer at every admitted weight.'
    return result
