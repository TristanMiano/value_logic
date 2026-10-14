"""General-graph original-source anchor cover. Codex (GPT-6), DEVELOPMENT."""
from itertools import combinations,product
from pathlib import Path
import copy
import json
import random
import sys
import action_audits as aa
import frontier_service as fs
g01=aa.g01;Meter=aa.Meter;HERE=Path(__file__).resolve().parent

def source(case):
    n=case['n'];edges=case['edges'];H=case['H'];W=sum(w for a,b,w in edges);data=aa.original(edges,case.get('fees',[1]*(n+1)));data.pop('identity');h=data['variables']+1;data['variables']=h
    data['hard'] += [[1,h],[-1,h]];data['features'].append(dict(clause=[-h],node=n,scale=1));data['supports']=[[0,H//2,H]]*n+[[0,10*H*W]];data['H']=H;data['nodes']=n;data['bit_source']='finite independent cost coordinates with common mandatory anchor';return g01.seal(data)

def propose_cut(data,meter):
    edges={(a,b):w for a,b,w in data['edges']};n=data['nodes'];cliques=[]
    full=list(range(n));pairs=list(combinations(full,2));meter.pay('cut_acquisition','test_full_clique',2+len(pairs))
    if all(pair in edges for pair in pairs):
        amount=min(edges[pair] for pair in pairs);cliques.append(dict(vertices=full,weight=amount))
        for pair in pairs:edges[pair]-=amount
    for vertices in combinations(range(n),3):
        pairs=list(combinations(vertices,2));meter.pay('cut_acquisition','propose_triangle_residual',8)
        if all(edges.get(pair,0)>0 for pair in pairs):
            amount=min(edges[pair] for pair in pairs);cliques.append(dict(vertices=list(vertices),weight=amount))
            for pair in pairs:edges[pair]-=amount
            meter.pay('cut_acquisition','allocate_triangle_capacity',9)
    K=sum(c['weight']*(len(c['vertices'])**2//4) for c in cliques)+sum(edges.values())
    return g01.seal(dict(source=data['identity'],cliques=cliques,bound=K))

def admit(case,data,cut,geometry,meter):
    if data!=source(case):raise ValueError('Original source changed')
    n=data['nodes'];edges={}
    for a,b,w in data['edges']:
        if type(a)is not int or type(b)is not int or not 0<=a<b<n or (a,b) in edges or type(w)is not int or w<=0:raise ValueError('Malformed weighted graph')
        edges[a,b]=w
    if not edges:raise ValueError('Nonempty graph required')
    if cut['source']!=data['identity'] or cut['identity']!=g01.kernel.digest({k:v for k,v in cut.items() if k!='identity'}):raise ValueError('Unbound cut certificate')
    K=0
    for item in cut['cliques']:
        vertices=item['vertices'];amount=item['weight']
        if len(vertices)<2 or vertices!=sorted(set(vertices)) or any(type(v)is not int or not 0<=v<n for v in vertices) or type(amount)is not int or amount<0:raise ValueError('Malformed clique multiplier')
        for edge in combinations(vertices,2):
            if edge not in edges or edges[edge]<amount:raise ValueError('Non-clique or overallocated source edge')
            edges[edge]-=amount;meter.pay('cut_check','original_edge_capacity_subtraction',7)
        K+=amount*(len(vertices)**2//4);meter.pay('cut_check','clique_crossing_bound',8)
    K+=sum(edges.values());W=sum(w for a,b,w in data['edges'])
    if cut['bound']!=K or not 0<K<=W:raise ValueError('Incorrect cut upper bound')
    r=geometry['receipt'];left,right=r['parents'];pivot=r['pivot'];a,b=data['hard'][left],data['hard'][right]
    if r['source']!=data['identity'] or r['identity']!=g01.kernel.digest({k:v for k,v in r.items() if k!='identity'}) or pivot not in a or -pivot not in b or sorted(set(a)-{pivot}|set(b)-{-pivot})!=[data['variables']] or r['derived']!=[data['variables']]:raise ValueError('Mandatory anchor unproved')
    meter.pay('source','all_original_clauses_and_scaled_features',24+sum(1+len(c) for c in data['hard'])+6*len(data['features']))
    meter.pay('geometry_check','mandatory_resolution',24+len(a)+len(b));return K

def utility(data,state,K,meter):
    H=data['H'];W=sum(w for a,b,w in data['edges']);Q=H*(2*W-K)
    if state[-1] is not None:return Q
    score=0
    for a,b,w in data['edges']:
        da=0 if state[a] is None else H-state[a];db=0 if state[b] is None else H-state[b];score+=2*w*max(da,db);meter.pay('cover','graph_edge_maximum_score',7)
    return min(Q,score)

def model(data,count):
    answer=1<<(data['variables']-1)
    for i,k in enumerate(count):
        for j in range(2):answer|=1<<(4*i+2*j+(0 if j<k else 1))
    return answer

def coefficients(data,count):
    mask=model(data,count)
    for clause in data['hard']:
        if not any(bool(mask>>(abs(l)-1)&1)==(l>0) for l in clause):raise AssertionError('Infeasible original count action')
    result=[0]*len(data['supports'])
    for feature in data['features']:
        if not any(bool(mask>>(abs(l)-1)&1)==(l>0) for l in feature['clause']):result[feature['node']]+=feature['scale']
    return result

def action(data,state,K):
    H=data['H'];W=sum(w for a,b,w in data['edges']);A=10*H*W;tau=H*K
    if state[-1]==A:return dict(kind='replace',count=None,bound=0)
    if state[-1]==0:return dict(kind='repair',count=[1]*len(data['edges']),bound=tau)
    upper=[H if v is None else v for v in state[:-1]];count=[2 if upper[a]<=upper[b] else 0 for a,b,w in data['edges']]
    bound=sum(w*(k*upper[a]+(2-k)*upper[b]) for k,(a,b,w) in zip(count,data['edges']))
    if bound>tau:return None
    return dict(kind='repair',count=count,bound=bound)

def small(case,data,K):
    n=case['n'];H=case['H'];W=sum(w for a,b,w in case['edges']);A=10*H*W;tau=H*K;worlds=list(product((0,H//2,H),repeat=n));counts=list(product((0,1,2),repeat=len(case['edges'])));values=[]
    for count in counts:
        coeff=coefficients(data,count);values.append([sum(c*z for c,z in zip(coeff[:-1],world)) for world in worlds])
    opt=[min(row[h] for row in values) for h in range(len(worlds))]
    for h,world in enumerate(worlds):assert opt[h]==sum(2*w*min(world[a],world[b]) for a,b,w in case['edges'])
    states=action_checks=corner_checks=outputs=0
    for partial in product((None,0,H//2,H),repeat=n):
        corners=[h for h,world in enumerate(worlds) if all((v==world[i]) if v is not None else world[i] in(0,H) for i,v in enumerate(partial))]
        bounds=[(max(row[h]-opt[h] for h in corners),max(row[h] for h in corners)) for row in values];L=min(opt[h] for h in corners)
        for anchor in(None,0,A):
            state=(*partial,anchor);loA,hiA=(0,A) if anchor is None else(anchor,anchor)
            feasible=max(0,A-loA-L)<=tau or any(max(R,U+hiA-A)<=tau for R,U in bounds)
            covered=utility(data,state,K,Meter())==H*(2*W-K);decision=action(data,state,K)
            assert covered==feasible==(decision is not None);states+=1;action_checks+=len(counts);corner_checks+=len(corners)*len(counts)
            if decision:
                outputs+=1
                if decision['kind']=='replace':assert max(0,A-loA-L)<=decision['bound']
                else:
                    index=counts.index(tuple(decision['count']));R,U=bounds[index];assert max(R,U+hiA-A)<=decision['bound']<=tau
    return dict(partial_states=states,action_checks=action_checks,corner_checks=corner_checks,terminal_actions=outputs)

def large(case,data,K):
    n=case['n'];H=case['H'];W=sum(w for a,b,w in case['edges']);A=10*H*W;tau=H*K;checked=0
    for world in product((0,H//2,H),repeat=n):
        opt=sum(2*w*min(world[a],world[b]) for a,b,w in case['edges'])
        balanced=sum(w*(world[a]+world[b]) for a,b,w in case['edges']);assert balanced-opt<=tau
        for selected in [(),*[(i,) for i in range(n)],tuple(range(n))]:
            partial=tuple(world[i] if i in selected else None for i in range(n))
            for observed in(None,0,A):
                decision=action(data,(*partial,observed),K)
                if decision is None:continue
                coeff=coefficients(data,decision['count']) if decision['kind']=='repair' else None
                for anchor in((0,A) if observed is None else(observed,)):
                    cost=A if coeff is None else anchor+sum(c*z for c,z in zip(coeff[:-1],world));assert cost-min(A,anchor+opt)<=decision['bound']<=tau;checked+=1
    return dict(actual_world_action_checks=checked)

def run(root,case):
    directory=root/case['name'];directory.mkdir(exist_ok=False);data=source(case);meter=Meter();cut=propose_cut(data,meter);geometry=fs.acquire_geometry(data);K=admit(case,data,cut,geometry,meter)
    g01.save(directory/'source.json',data);g01.save(directory/'cut.json',cut);g01.save(directory/'geometry.json',geometry)
    cuts=[sum(w for a,b,w in case['edges'] if bool(mask>>a&1)!=bool(mask>>b&1)) for mask in range(1<<case['n'])];assert max(cuts)<=K;negatives=[]
    for label in('source','bound','capacity','non_clique'):
        bad=copy.deepcopy(cut)
        if label=='source':bad['source']='wrong'
        elif label=='bound':bad['bound']-=1
        elif label=='capacity':bad['cliques'].append(dict(vertices=list(case['edges'][0][:2]),weight=sum(w for a,b,w in case['edges'])+1))
        else:bad['cliques'].append(dict(vertices=[0,0,1],weight=1))
        bad=g01.seal({k:v for k,v in bad.items() if k!='identity'})
        try:admit(case,data,bad,geometry,Meter())
        except ValueError:negatives.append(label)
        else:raise AssertionError('Invalid cut proof accepted')
    checked=small(case,data,K) if case['n']<=4 else large(case,data,K)
    g01.save(directory/'results.json',dict(status='complete',cut_upper=K,actual_maxcut=max(cuts),edge_weight=sum(w for a,b,w in case['edges']),cut_checks=len(cuts),negative_controls=negatives,checks=checked,invoice=meter.record(),physical_audits=0,resolution_steps=1));print(case['name'],K,max(cuts),checked,flush=True)

def prepare(root):
    root.mkdir(exist_ok=False);rng=random.Random(8141690);cases=[]
    for n in range(2,7):
        for shape in('path','cycle','clique','sparse'):
            edges={(i,i+1) for i in range(n-1)}
            if shape=='cycle':edges.add((0,n-1))
            if shape=='clique':edges=set(combinations(range(n),2))
            if shape=='sparse':edges.update((a,b) for a,b in combinations(range(n),2) if rng.random()<.35)
            weighted=[[a,b,1 if shape!='sparse' else rng.randrange(1,5)] for a,b in sorted(edges)]
            cases.append(dict(name=f'n{n}_{shape}',n=n,H=4,edges=weighted))
    g01.save(root/'design.json',dict(cases=cases,source_sha256=g01.sha(__file__),stage='DEVELOPMENT',contributor='Codex (GPT-6)',physical_audits=0));(root/'impl.py').write_bytes(Path(__file__).read_bytes());(root/'declaration.md').write_bytes((HERE/'graph_cover.md').read_bytes())

if __name__=='__main__':
    root=Path(sys.argv[2])
    if sys.argv[1]=='prepare':prepare(root)
    else:
        design=json.loads((root/'design.json').read_text());case=next(c for c in design['cases'] if c['name']==sys.argv[3]);run(root,case)
