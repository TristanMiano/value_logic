#!/usr/bin/env python3
"""Exact continuum expected-fee polynomials for supplied path policies.
DEVELOPMENT, Codex (GPT-6), 2026-10-14. No hidden labels in a deployed learner.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from math import comb
import copy
import json
import random
import sys
import time
import g01
import markov_paths as mk

HERE=Path(__file__).resolve().parent
VERSION='s08-continuum-policy-v1'
Meter=g01.kernel.Meter


def normalize(value):
    if isinstance(value,F):return str(value)
    if isinstance(value,dict):return {str(k):normalize(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)):return [normalize(v) for v in value]
    return value


def binding(costs,roots):
    return g01.kernel.digest(normalize(dict(costs=costs,roots=roots,
        source='fresh stationary symmetric homogeneous binary Markov indicators',
        policy='ordinary interval roots with mandatory middle-neighbor continuation')))


def value_certificate(costs,rho,roots):
    n=len(costs);rho=F(rho);meter=Meter();tables={k:{} for k in ('ordinary','left','right')}
    if not 0<rho<1:raise ValueError('Interior evaluation required')
    def probability(a,b,mode,i):
        def potential(distance,label):
            if label is None:return (F(1),F(1))
            same=(1+(2*rho-1)**distance)/2
            return (same,1-same) if label==0 else (1-same,same)
        left=potential(i-a+1,None if a==0 else int(mode=='left'))
        right=potential(b-i+1,None if b==n-1 else int(mode=='right'))
        weights=[left[k]*right[k] for k in (0,1)]
        meter.pay('evaluation','closed_form_bridge_rational_arithmetic',18)
        return weights[0]/sum(weights)
    def at(kind,a,b):return tables[kind][a,b] if a<=b else F(0)
    for length in range(1,n+1):
        for a in range(n-length+1):
            b=a+length-1
            for mode,i,e,m in [('left',a,at('ordinary',a+1,b),at('left',a+1,b)),
                               ('right',b,at('ordinary',a,b-1),at('right',a,b-1))]:
                p=probability(a,b,mode,i);tables[mode][a,b]=costs[i]+p*e+(1-p)*m
                meter.pay('evaluation','forced_value',6)
            if a==b:tables['ordinary'][a,b]=F(0)
            else:
                i=roots[a,b];p=probability(a,b,'ordinary',i)
                tables['ordinary'][a,b]=costs[i]+p*(at('ordinary',a,i-1)+at('ordinary',i+1,b))
                tables['ordinary'][a,b]+=(1-p)*(at('right',a,i-1)+at('left',i+1,b))
                meter.pay('evaluation','supplied_root_value',10)
            meter.pay('evaluation','retain_three_values',3)
    return dict(binding=binding(costs,roots),rho=rho,tables=tables,bound=tables['ordinary'][0,n-1],invoice=meter.record())


def check_value(costs,roots,cert):
    n=len(costs);rho=cert['rho'];meter=Meter()
    if cert['binding']!=binding(costs,roots) or type(rho)is not F or not 0<rho<1:raise ValueError('Value/source binding')
    states={(a,b) for a in range(n) for b in range(a,n)}
    if set(roots)!={(a,b) for a,b in states if a<b}:raise ValueError('Policy state scope')
    if any(type(i)is not int or not a<=i<=b for (a,b),i in roots.items()):raise ValueError('Policy root range')
    if set(cert['tables'])!={'ordinary','left','right'}:raise ValueError('Certificate tables')
    for table in cert['tables'].values():
        if set(table)!=states or any(type(v)not in (int,F) or v<0 for v in table.values()):raise ValueError('Certificate state scope')
    matrix=[[rho,1-rho],[1-rho,rho]];powers=[[[F(1),F(0)],[F(0),F(1)]]]
    for d in range(n):
        prior=powers[-1];powers.append([[sum(prior[i][k]*matrix[k][j] for k in (0,1)) for j in (0,1)] for i in (0,1)])
        meter.pay('checking','independent_transition_matrix_product',12)
    def p(a,b,mode,i):
        left=[1,1] if a==0 else powers[i-a+1][int(mode=='left')]
        right=[1,1] if b==n-1 else [powers[b-i+1][k][int(mode=='right')] for k in (0,1)]
        numerator=left[0]*right[0];meter.pay('checking','boundary_probability_normalization',7)
        return numerator/(numerator+left[1]*right[1])
    # The physical-endpoint case uses integer 1s; force exact arithmetic.
    def at(kind,a,b):return cert['tables'][kind][a,b] if a<=b else F(0)
    for a,b in states:
        terms=[('left',a,at('ordinary',a+1,b),at('left',a+1,b)),('right',b,at('ordinary',a,b-1),at('right',a,b-1))]
        if a==b:
            if at('ordinary',a,b)!=0:raise ValueError('Singleton stop')
        else:
            i=roots[a,b]
            terms.append(('ordinary',i,at('ordinary',a,i-1)+at('ordinary',i+1,b),at('right',a,i-1)+at('left',i+1,b)))
        for kind,i,e,m in terms:
            probability=F(p(a,b,kind,i))
            if at(kind,a,b)!=costs[i]+probability*e+(1-probability)*m:raise ValueError('Selected policy equality')
            meter.pay('checking','exact_selected_policy_equality',7)
    if cert['bound']!=at('ordinary',0,n-1):raise ValueError('Root bound mismatch')
    return meter.record()


def interpolate(nodes,values,meter):
    n=len(nodes);dd=list(map(F,values))
    for order in range(1,n):
        for i in range(n-1,order-1,-1):
            dd[i]=(dd[i]-dd[i-1])/(nodes[i]-nodes[i-order]);meter.pay('interpolation','divided_difference',3)
    power=[F(0)]*n;basis=[F(1)]
    for i in range(n):
        for j,c in enumerate(basis):power[j]+=dd[i]*c;meter.pay('interpolation','newton_power_expansion',2)
        if i<n-1:
            updated=[F(0)]*(len(basis)+1)
            for j,c in enumerate(basis):updated[j]-=nodes[i]*c;updated[j+1]+=c;meter.pay('interpolation','multiply_linear_basis',3)
            basis=updated
    bernstein=[]
    for k in range(n):
        bernstein.append(sum(power[j]*F(comb(k,j),comb(n-1,j)) for j in range(k+1)))
        meter.pay('interpolation','power_to_bernstein',3*(k+1))
    return bernstein


def evaluate(coeff,rho):
    rho=F(rho);d=len(coeff)-1
    return sum(c*comb(d,k)*rho**k*(1-rho)**(d-k) for k,c in enumerate(coeff))


def produce(costs,roots):
    meter=Meter();n=len(costs);nodes=[F(j,n+1) for j in range(1,n+1)];certs=[]
    for rho in nodes:
        cert=value_certificate(costs,rho,roots);certs.append(cert)
        meter.pay('production','supplied_policy_rational_evaluation',cert['invoice']['total'])
    coeff=interpolate(nodes,[c['bound'] for c in certs],meter)
    return dict(binding=binding(costs,roots),coefficients=coeff,evaluations=certs,invoice=meter.record())


def check_polynomial(costs,roots,proof):
    n=len(costs);coeff=proof['coefficients'];meter=Meter()
    if proof['binding']!=binding(costs,roots) or len(coeff)!=n:raise ValueError('Polynomial binding/degree')
    if any(type(v)not in (int,F) or not 0<=v<=sum(costs) for v in coeff):raise ValueError('Invalid fee coefficients')
    certs=proof['evaluations'];nodes=[F(j,n+1) for j in range(1,n+1)]
    if len(certs)!=n or [c['rho'] for c in certs]!=nodes:raise ValueError('Interpolation scope')
    for cert in certs:
        checked=check_value(costs,roots,cert);meter.pay('checking','independent_selected_policy_check',checked['total'])
        if evaluate(coeff,cert['rho'])!=cert['bound']:raise ValueError('Polynomial identity')
        meter.pay('checking','bernstein_point_identity',6*n)
    return meter.record()


def split(coeff,t,meter):
    if not 0<=t<=1:raise ValueError('Invalid subdivision')
    work=list(coeff);left=[work[0]];right=[work[-1]]
    while len(work)>1:
        work=[(1-t)*a+t*b for a,b in zip(work,work[1:])]
        meter.pay('restriction','de_casteljau_convex_combination',3*len(work))
        left.append(work[0]);right.append(work[-1])
    return left,list(reversed(right))


def restrict(coeff,lo,hi,meter):
    lo,hi=F(lo),F(hi)
    if not 0<=lo<=hi<=1:raise ValueError('Invalid source region')
    if lo==hi:
        value=evaluate(coeff,lo);meter.pay('restriction','point_evaluation',6*len(coeff));return [value]*len(coeff)
    left=list(coeff) if hi==1 else split(coeff,hi,meter)[0]
    return left if lo==0 else split(left,lo/hi,meter)[1]


def regret_certificate(bank,chosen,lo,hi,epsilon,meter):
    diffs={other:[a-b for a,b in zip(bank[chosen],coeff)] for other,coeff in bank.items()}
    local={other:restrict(diff,lo,hi,meter) for other,diff in diffs.items()}
    return dict(chosen=chosen,interval=[lo,hi],epsilon=epsilon,coefficients=local,
        bound=max(max(c) for c in local.values()),accepted=all(max(c)<=epsilon for c in local.values()))


def run(directory):
    directory.mkdir(exist_ok=False);(directory/'impl.py').write_bytes(Path(__file__).read_bytes())
    rng=random.Random(8141460);cases=[];identities=restrictions=worlds=0;meter=Meter();cpu=time.process_time_ns();wall=time.perf_counter_ns()
    g01.save(directory/'design.json',dict(version=VERSION,stage='DEVELOPMENT',contributor='Codex (GPT-6)',
        source_sha256=g01.sha(__file__),declaration_sha256=g01.sha(HERE/'continuum_policy.md'),
        sizes=list(range(2,9)),repeats=3,menu=list(mk.MENU),seed=8141460,physical_audits=0))
    for n in range(2,9):
        for repeat in range(3):
            costs=[rng.randrange(1,10) for _ in range(n)];record=dict(n=n,costs=costs,policies=[])
            for r in mk.MENU:
                roots=mk.plan(costs,r)['roots'];proof=produce(costs,roots);checked=check_polynomial(costs,roots,proof)
                sums=[0]*n;counts=[0]*n
                for bits in product((0,1),repeat=n):
                    _,queries=mk.conditional_trace(bits,roots);s=sum(x==y for x,y in zip(bits,bits[1:]))
                    sums[s]+=sum(costs[i] for i in queries);counts[s]+=1;worlds+=1
                enumerated=[F(s,2*comb(n-1,k)) for k,s in enumerate(sums)]
                assert enumerated==proof['coefficients'] and counts==[2*comb(n-1,k) for k in range(n)]
                identities+=1
                for lo,hi in [(F(0),F(1)),(F(1,7),F(5,6)),(F(3,8),F(3,8)),(F(0),F(2,9)),(F(7,8),F(1))]:
                    restricted=restrict(proof['coefficients'],lo,hi,meter)
                    for j in range(11):
                        t=F(j,10);original=evaluate(proof['coefficients'],lo+(hi-lo)*t)
                        assert evaluate(restricted,t)==original and min(restricted)<=original<=max(restricted)
                        restrictions+=1
                record['policies'].append(dict(r=r,coefficients=proof['coefficients'],production=proof['invoice'],checking=checked))
                if n==2 and repeat==0 and r==1:
                    g01.save(directory/'example_certificate.json',normalize(dict(costs=costs,roots=roots,proof=proof)))
            cases.append(record)
    negatives=[]
    costs=[3,2,7,4];roots=mk.plan(costs,3)['roots'];proof=produce(costs,roots)
    bad=copy.deepcopy(proof);bad['coefficients'][0]+=1
    for name,cc,rr,pp in [('coefficient',costs,roots,bad),('fee',[4,2,7,4],roots,proof),
                         ('root',costs,{**roots,(0,3):(roots[0,3]+1)%4},proof),
                         ('missing_evaluation',costs,roots,{**proof,'evaluations':proof['evaluations'][:-1]})]:
        rejected=False
        try:check_polynomial(cc,rr,pp)
        except ValueError:rejected=True
        assert rejected;negatives.append(dict(kind=name,rejected=True))
    g01.save(directory/'results.json',dict(status='complete',cases=cases,polynomial_identities=identities,
        exact_restriction_checks=restrictions,enumerated_policy_worlds=worlds,negative_controls=negatives,
        restriction_invoice=meter.record(),physical_audits=0,cpu_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-wall))
    print(json.dumps(dict(status='complete',polynomial_identities=identities,restriction_checks=restrictions,
        worlds=worlds,negative_controls=len(negatives))))


if __name__=='__main__':run(Path(sys.argv[1]))
