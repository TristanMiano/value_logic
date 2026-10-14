"""Original-source tolerance repair and ordinary knapsack/greedy. Codex (GPT-6)."""
from functools import lru_cache
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import copy
import json
import random
import sys
import graph_audits as ga
g01=ga.g01;Meter=ga.Meter;HERE=Path(__file__).resolve().parent

def coloring(data,meter):
    adj=[[] for _ in range(data['n'])]
    for a,b,w in data['edges']:adj[a].append(b);adj[b].append(a)
    colors=[None]*data['n']
    for root in range(data['n']):
        if colors[root] is not None:continue
        colors[root]=0;todo=[root]
        for a in todo:
            for b in adj[a]:
                meter.pay('geometry','bipartite_color_edge',4)
                if colors[b] is None:colors[b]=1-colors[a];todo.append(b)
                elif colors[b]==colors[a]:raise ValueError('Graph is not bipartite')
    return colors

def check_coloring(data,colors,meter):
    if len(colors)!=data['n'] or any(type(x)is not int or x not in(0,1) for x in colors):raise ValueError('Invalid coloring')
    if any(colors[a]==colors[b] for a,b,w in data['edges']):raise ValueError('Uncut graph edge')
    meter.pay('geometry_check','complete_bipartite_coloring',data['n']+3*len(data['edges']))

def residual(data,known):
    answer=0
    for a,b,w in data['edges']:
        if a not in known and b not in known:answer+=2*w
        elif a not in known and known[b]==1:answer+=w
        elif b not in known and known[a]==1:answer+=w
    return answer

def maxcut_residual(data,known):
    unknown=[i for i in range(data['n']) if i not in known]
    cut=max((sum(w for a,b,w in data['edges'] if a in bits and b in bits and bits[a]!=bits[b])
             for values in product((0,1),repeat=len(unknown)) for bits in [dict(zip(unknown,values))]),default=0)
    boundary=sum(w for a,b,w in data['edges'] if (a not in known and known.get(b)==1) or(b not in known and known.get(a)==1))
    return 2*cut+boundary

def counts(data,known):
    selected=[]
    for a,b,w in data['edges']:
        qa=[known[a]] if a in known else [0,1,2];qb=[known[b]] if b in known else [0,1,2]
        if max(qa)<=min(qb):selected.append(2)
        elif max(qb)<=min(qa):selected.append(0)
        else:selected.append(1)
    return selected

def assignment(data,count):
    out=0
    for e,k in enumerate(count):
        for j in range(2):out|=1<<(4*e+2*j+(0 if j<k else 1))
    return out

def regret(data,count,world):
    return sum(w*(k*world[a]+(2-k)*world[b]-2*min(world[a],world[b])) for(a,b,w),k in zip(data['edges'],count))

def construct(data,known,colors,meter):
    count=counts(data,known);bound=residual(data,known)
    world=[known[i] if i in known else 2*colors[i] for i in range(data['n'])]
    meter.pay('action','balanced_unresolved_and_exact_resolved_components',12*len(data['edges'])+data['n'])
    return dict(source=data['identity'],assignment=assignment(data,count),count=count,regret_bound=bound,attaining_world=world)

def check(data,receipts,request,colors,action,meter):
    check_coloring(data,colors,meter);known={}
    for r in receipts:
        if r['identity']!=g01.kernel.digest({k:v for k,v in r.items() if k!='identity'}):raise ValueError('Receipt hash')
        i=r['node']
        if type(i)is not int or not 0<=i<data['n'] or i in known or r['sequence']!=len(known):raise ValueError('Receipt coordinate')
        if r['source']!=data['identity'] or r['request']!=request or type(r['value'])is not int or r['value'] not in(0,1,2) or r['base_fee']!=data['audit_costs'][i]:raise ValueError('Receipt binding')
        known[i]=r['value'];meter.pay('receipt_check','bind_ternary_source_request_and_fee',17)
    if action['source']!=data['identity']:raise ValueError('Action source')
    mask=action['assignment']
    for clause in data['hard']:
        if not any(bool(mask>>(abs(lit)-1)&1)==(lit>0) for lit in clause):raise ValueError('Original infeasibility')
        meter.pay('action_check','original_hard_clause',len(clause)+1)
    upper=0;decoded=[]
    for e,(a,b,w) in enumerate(data['edges']):
        k=int(bool(mask>>(4*e)&1))+int(bool(mask>>(4*e+2)&1));decoded.append(k)
        qa=[known[a]] if a in known else [0,1,2];qb=[known[b]] if b in known else [0,1,2]
        # Independent local interval upper; bipartite witness proves joint attainment.
        upper+=w*max(k*u+(2-k)*v-2*min(u,v) for u in qa for v in qb)
        meter.pay('action_check','all_compatible_local_regrets',len(qa)*len(qb)*8)
    if decoded!=action['count'] or upper!=action['regret_bound']:raise ValueError('Incorrect count or upper')
    world=action['attaining_world']
    if len(world)!=data['n'] or any(type(v)is not int or v not in(0,1,2) for v in world) or any(world[i]!=v for i,v in known.items()):raise ValueError('Invalid compatible attaining world')
    if regret(data,decoded,world)!=upper:raise ValueError('Nonattaining bound')
    meter.pay('action_check','joint_attaining_original_objective',data['n']+8*len(data['edges']))
    return upper

def knapsack(data,tau,meter):
    target=max(0,2*len(data['edges'])-tau);degrees=[0]*data['n']
    for a,b,w in data['edges']:degrees[a]+=w;degrees[b]+=w
    states={0:(0,())}
    for i,c in enumerate(data['audit_costs']):
        nxt=dict(states)
        for p,(fee,chosen) in states.items():
            q=min(target,p+degrees[i]);value=(fee+c,chosen+(i,))
            if q not in nxt or value<nxt[q]:nxt[q]=value
            meter.pay('planning','degree_quota_knapsack_transition',7+len(chosen))
        states=nxt
    fee,chosen=states[target]
    meter.pay('planning','degree_quota_and_chosen_plan',data['n']+2*len(data['edges'])+len(chosen))
    return dict(fee=fee,chosen=list(chosen),target=target)

def choose(data,known,tau,meter,probabilities=None):
    remaining=residual(data,known)-tau
    if remaining<=0:return None
    d=[0]*data['n'];b=[0]*data['n']
    for a,j,w in data['edges']:
        if a not in known and j not in known:d[a]+=w;d[j]+=w
        elif a not in known and known[j]==1:b[a]+=w
        elif j not in known and known[a]==1:b[j]+=w
    choices=[]
    for i,c in enumerate(data['audit_costs']):
        if i in known:continue
        low=min(remaining,d[i]+b[i]);high=min(remaining,2*d[i]+b[i])
        gain=low if probabilities is None else probabilities[i]*high+(1-probabilities[i])*low
        if gain>0:choices.append((-F(gain,c),c,i))
    meter.pay('planning','remaining_quota_and_capped_marginal_scan',8*len(data['edges'])+8*data['n'])
    return min(choices)[2]

def finite(directory):
    directory.mkdir(exist_ok=False);(directory/'impl.py').write_bytes(Path(__file__).read_bytes());(directory/'declaration.md').write_bytes((HERE/'tolerance_graph.md').read_bytes())
    rng=random.Random(8141595);cases=[]
    for n in range(2,7):
        options=dict(path=[(i,i+1) for i in range(n-1)],star=[(0,i) for i in range(1,n)])
        if n%2==0 and n>=4:options['cycle']=[(i,i+1) for i in range(n-1)]+[(0,n-1)]
        for shape,edges in options.items():cases.append(dict(name=f'n{n}_{shape}',costs=[rng.randrange(1,8) for i in range(n)],edges=edges,bipartite=True))
    cases.append(dict(name='triangle',costs=[2,3,4],edges=[(0,1),(0,2),(1,2)],bipartite=False))
    g01.save(directory/'design.json',dict(cases=cases,contributor='Codex (GPT-6)',stage='DEVELOPMENT',source_sha256=g01.sha(__file__),physical_audits=0));results=[]
    for case in cases:
        data=ga.source(case['costs'],case['edges']);n=data['n'];m=len(data['edges']);meter=Meter();ga.admit(data,meter)
        colors=coloring(data,meter) if case['bipartite'] else None;states=world_checks=action_checks=0;strict=0
        for state in product((-1,0,1,2),repeat=n):
            known={i:v for i,v in enumerate(state) if v!=-1};unknown=[i for i in range(n) if i not in known]
            worlds=[]
            for values in product((0,1,2),repeat=len(unknown)):
                world=[known.get(i,0) for i in range(n)]
                for i,v in zip(unknown,values):world[i]=v
                worlds.append(world)
            count=counts(data,known);actual=max(regret(data,count,w) for w in worlds);formula=maxcut_residual(data,known)
            assert actual==formula;world_checks+=len(worlds);strict+=actual<residual(data,known)
            if n<=4:
                all_values=[max(regret(data,k,w) for w in worlds) for k in product((0,1,2),repeat=m)]
                assert actual==min(all_values);action_checks+=len(all_values)
            if colors is not None:
                assert formula==residual(data,known)
                receipts=[g01.seal(dict(source=data['identity'],request='conditional',node=i,value=v,base_fee=case['costs'][i],sequence=j)) for j,(i,v) in enumerate(known.items())]
                action=construct(data,known,colors,meter);assert check(data,receipts,'conditional',colors,action,meter)==formula
            states+=1
        policies=[]
        if colors is not None:
            for tau in sorted(set((0,m//2,m,2*m))):
                plan=knapsack(data,tau,meter)
                @lru_cache(None)
                def bellman(state):
                    known={i:v for i,v in enumerate(state) if v!=-1}
                    if residual(data,known)<=tau:return 0
                    return min(case['costs'][i]+max(bellman(state[:i]+(v,)+state[i+1:]) for v in(0,1)) for i,v in enumerate(state) if v==-1)
                optimum=bellman((-1,)*n);assert optimum==plan['fee']
                ratios=[]
                for bits in product((0,1),repeat=n):
                    known={}
                    while residual(data,known)>tau:
                        i=choose(data,known,tau,Meter());known[i]=bits[i]
                    fee=sum(case['costs'][i] for i in known)
                    offline=min(sum(c for i,c in enumerate(case['costs']) if mask>>i&1) for mask in range(1<<n)
                        if residual(data,{i:bits[i] for i in range(n) if mask>>i&1})<=tau)
                    Q=max(0,2*m-tau);harmonic=sum((F(1,i) for i in range(1,Q+1)),F(0))
                    assert fee<=2*harmonic*offline if Q else fee==0
                    ratios.append(F(fee,offline) if offline else F(1))
                policies.append(dict(tau=tau,minimax_fee=optimum,knapsack=plan,bellman_states=bellman.cache_info().currsize,max_greedy_ratio=max(ratios)))
            bad=list(colors);bad[case['edges'][0][1]]=bad[case['edges'][0][0]]
            try:check_coloring(data,bad,Meter())
            except ValueError:pass
            else:raise AssertionError('Invalid coloring accepted')
            wrong=dict(action,source='wrong')
            try:check(data,receipts,'conditional',colors,wrong,Meter())
            except ValueError:pass
            else:raise AssertionError('Wrong action source accepted')
        result=dict(name=case['name'],states=states,compatible_world_checks=world_checks,action_checks=action_checks,
            strict_edgewise_gap= strict,policies=policies,invoice=meter.record(),physical_audits=0)
        g01.save(directory/f"{case['name']}.json",result);results.append(result);print(case['name'],states,world_checks,flush=True)
    g01.save(directory/'results.json',dict(status='complete',cases=results,physical_audits=0))

if __name__=='__main__':finite(Path(sys.argv[1]))
