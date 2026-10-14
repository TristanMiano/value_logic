#!/usr/bin/env python3
"""Exact model-bank values and first compulsory-pair checks. DEVELOPMENT.
Codex (GPT-6), 2026-10-14.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import copy
import json
import sys
import g01
import markov_paths as mk
import markov_service as ms

HERE=Path(__file__).resolve().parent
Meter=g01.kernel.Meter


def check_exact(data,r,policy):
    """Independent matrix recurrence and Bellman EQUALITIES, not upper bounds."""
    meter=Meter();costs=data['audit_costs'];n=data['n']
    if r not in data['repeat_numerators'] or policy['n']!=n or policy['r']!=r:raise ValueError('Policy/model binding')
    matrix=[[r,10-r],[10-r,r]];powers=[[[1,0],[0,1]]]
    for d in range(1,n+1):
        prior=powers[-1]
        powers.append([[sum(prior[a][k]*matrix[k][b] for k in range(2)) for b in range(2)] for a in range(2)])
        meter.pay('exact_check','transition_matrix_multiplication',12)
    def probability(a,b,mode,i):
        left=[1,1] if a==0 else powers[i-a+1][int(mode=='left')]
        right=[1,1] if b==n-1 else [powers[b-i+1][v][int(mode=='right')] for v in range(2)]
        numerator=left[0]*right[0];denominator=numerator+left[1]*right[1]
        meter.pay('exact_check','boundary_message_normalization',7)
        return F(numerator,denominator)
    states={(a,b) for a in range(n) for b in range(a,n)};tables=policy['tables']
    if set(tables)!= {'ordinary','left','right'} or set(policy['roots'])!={(a,b) for a,b in states if a<b}:raise ValueError('Policy state scope')
    for table in tables.values():
        if set(table)!=states or any(type(x) not in (int,F) or x<0 for x in table.values()):raise ValueError('Invalid certificate entries')
    def at(kind,a,b):return tables[kind][a,b] if a<=b else F(0)
    for a,b in states:
        terms=[('left',a,at('ordinary',a+1,b),at('left',a+1,b)),('right',b,at('ordinary',a,b-1),at('right',a,b-1))]
        if a==b:
            if tables['ordinary'][a,b]!=0:raise ValueError('Ordinary singleton must stop')
        else:
            i=policy['roots'][a,b]
            if type(i)is not int or not a<=i<=b:raise ValueError('Invalid root')
            terms.append(('ordinary',i,at('ordinary',a,i-1)+at('ordinary',i+1,b),at('right',a,i-1)+at('left',i+1,b)))
        for mode,i,extreme,middle in terms:
            p=probability(a,b,mode,i)
            if tables[mode][a,b]!=costs[i]+p*extreme+(1-p)*middle:raise ValueError('Inexact selected-policy value')
            meter.pay('exact_check','selected_policy_value_equality',7)
    if policy['bound']!=tables['ordinary'][0,n-1]:raise ValueError('Root invoice mismatch')
    return meter.record()


def prepare(directory,label,data,meter):
    bank={};values={};certificates={}
    for r in mk.MENU:
        bank[r]=mk.plan(data['audit_costs'],r)
        meter.pay('preparation','optimal_model_root_policy',bank[r]['invoice']['total'])
        values[r]={};certificates[r]={}
        for q in mk.MENU:
            evaluated=mk.plan(data['audit_costs'],q,bank[r]['roots'])
            checked=check_exact(data,q,evaluated)
            meter.pay('preparation','cross_model_policy_evaluation',evaluated['invoice']['total'])
            meter.pay('preparation','independent_exact_certificate_check',checked['total'])
            values[r][q]=evaluated['bound'];certificates[r][q]=dict(policy=mk.export(evaluated),checking=checked)
    minima={q:min(values[r][q] for r in bank) for q in mk.MENU}
    supports={r:{q for q in mk.MENU if values[r][q]==minima[q]} for r in bank}
    meter.pay('preparation','compile_common_minimizing_policy_cells',2*len(bank)*len(mk.MENU))
    record=dict(source=data['identity'],values=values,certificates=certificates,supports={r:sorted(v) for r,v in supports.items()})
    g01.save(directory/f'{label}_bank.json',record)
    return bank,values,supports,g01.sha(directory/f'{label}_bank.json')


def run(directory):
    directory.mkdir(exist_ok=False);(directory/'impl.py').write_bytes(Path(__file__).read_bytes())
    checks=[]
    for n in range(2,8):
        for r in mk.MENU:
            for first in range(n):
                neighbor=first-1 if first else 1
                middle=repeat=F(0)
                for bits in product((0,1),repeat=n):
                    probability=mk.world_probability(bits,r)
                    if bits[first]:
                        middle+=probability
                        if bits[neighbor]:repeat+=probability
                assert middle==F(1,2) and repeat==F(r,20)
                checks.append(dict(n=n,r=r,first=first,neighbor=neighbor,middle=middle,repeat=repeat))
    data=ms.source([2,7,3,1,6]);policy=mk.plan(data['audit_costs'],3)
    check_exact(data,3,policy);bad=copy.deepcopy(policy)
    # A loose but valid upper-bound certificate cannot certify a decision cell.
    for kind in bad['tables']:
        for a,b in bad['tables'][kind]:
            if not(a==b and kind=='ordinary'):bad['tables'][kind][a,b]+=100*(b-a+1)
    bad['bound']=bad['tables']['ordinary'][0,4]
    ms.check_policy(data,3,bad)
    rejected=False
    try:check_exact(data,3,bad)
    except ValueError:rejected=True
    assert rejected
    g01.save(directory/'results.json',dict(status='complete',stage='DEVELOPMENT',checks=checks,
        first_pair_law_checks=len(checks),loose_upper_rejected_by_exact_checker=rejected,physical_audits=0,
        source_sha256=g01.sha(__file__),declaration_sha256=g01.sha(HERE/'forced_calibration.md')))
    print(json.dumps(dict(status='complete',first_pair_law_checks=len(checks),loose_upper_rejected=True)))


if __name__=='__main__':run(Path(sys.argv[1]))
