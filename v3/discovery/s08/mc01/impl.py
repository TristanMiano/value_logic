"""mc01 finite source checks, Codex (GPT-6), DEVELOPMENT."""
from itertools import combinations,product
from pathlib import Path
import json
import sys
import g01
HERE=Path(__file__).resolve().parent

def independent(subset,bases):return any(subset<=b for b in bases)
def exchange(bases):
    return all(any((a-{i}|{j}) in bases for j in b-a) for a in bases for b in bases for i in a-b)
def greedy(weights,bases,reverse=True):
    answer=set()
    for i in sorted(range(len(weights)),key=lambda i:(-weights[i] if reverse else weights[i],i)):
        if independent(answer|{i},bases):answer.add(i)
    return answer
def graphic(vertices,edges):
    bases=[]
    for chosen in combinations(range(len(edges)),vertices-1):
        parent=list(range(vertices))
        def find(i):
            while parent[i]!=i:i=parent[i]
            return i
        good=True
        for i in chosen:
            a,b=map(find,edges[i])
            if a==b:good=False;break
            parent[a]=b
        if good:bases.append(set(chosen))
    return bases
def cases():
    result=[dict(name=f'u{n}_{r}',n=n,bases=[list(b) for b in combinations(range(n),r)]) for n in range(2,7) for r in range(1,n)]
    for name,v,edges in [('triangle',3,[(0,1),(1,2),(0,2)]),('square',4,[(0,1),(1,2),(2,3),(0,3)]),('k4',4,list(combinations(range(4),2)))]:
        result.append(dict(name=name,n=len(edges),bases=[sorted(b) for b in graphic(v,edges)]))
    return result
def run(root,case):
    n=case['n'];bases=[set(b) for b in case['bases']];assert exchange(bases);r=len(bases[0]);m=len(bases);H=2;coef=[sum(i in b for b in bases) for i in range(n)];tau=H*(m*r-min(sum(coef[i] for i in b) for b in bases));Q=m*r*H-tau
    cnf=[[(-i-1 if mask>>i&1 else i+1) for i in range(n)] for mask in range(1<<n) if {i for i in range(n) if mask>>i&1} not in bases];source_checks=0
    for mask in range(1<<n):
        assert all(any(bool(mask>>(abs(l)-1)&1)==(l>0) for l in clause) for clause in cnf)==({i for i in range(n) if mask>>i&1} in bases);source_checks+=1
    worst=0;corners=0
    for world in product((0,H),repeat=n):
        optimum=m*min(sum(world[i] for i in b) for b in bases);value=sum(c*z for c,z in zip(coef,world));worst=max(worst,value-optimum);corners+=1
    assert worst==tau
    selected=greedy(coef,bases,False);assert sum(coef[i] for i in selected)==min(sum(coef[i] for i in b) for b in bases)
    states=actions=0
    for state in product((None,0,1,2),repeat=n):
        upper=[H if v is None else v for v in state];d=[H-v for v in upper];chosen=greedy(d,bases);rank=sum(d[i] for i in chosen);assert rank==max(sum(d[i] for i in b) for b in bases)
        U=m*sum(upper[i] for i in chosen);assert U==m*(r*H-rank)==m*min(sum(upper[i] for i in b) for b in bases)
        assert (U<=tau)==(min(Q,m*rank)==Q);states+=1
        if U<=tau:
            mask=sum(1<<i for i in chosen);assert all(any(bool(mask>>(abs(l)-1)&1)==(l>0) for l in clause) for clause in cnf);actions+=1
    comparisons=0;weighted_worlds=0
    for scores in product((0,1,2),repeat=n):
        vals=[]
        for mask in range(1<<n):vals.append(min(Q,m*max(sum(scores[i] for i in b if mask>>i&1) for b in bases)))
        for mask,value in enumerate(vals):
            unseen=[i for i in range(n) if not(mask>>i&1)]
            for i,j in combinations(unseen,2):
                assert vals[mask|1<<i]+vals[mask|1<<j]>=value+vals[mask|1<<i|1<<j];comparisons+=1
        weighted_worlds+=1
    g01.save(root/f"{case['name']}.json",dict(status='complete',source=case,one_copy_cnf=cnf,copies=m,rank=r,fallback_coefficients=coef,tolerance=tau,quota=Q,source_bitmask_checks=source_checks,regret_corners=corners,partial_states=states,upper_actions=actions,weighted_worlds=weighted_worlds,submodularity_checks=comparisons,physical_audits=0))
    print(case['name'],states,comparisons,flush=True)
def prepare(root):
    root.mkdir(exist_ok=False);design=dict(stage='DEVELOPMENT',contributor='Codex (GPT-6)',cases=cases(),source_sha256=g01.sha(__file__),physical_audits=0);g01.save(root/'design.json',design);(root/'impl.py').write_bytes(Path(__file__).read_bytes());(root/'declaration.md').write_bytes((HERE/'matroid_cover.md').read_bytes())
    bases=[{0,1},{2,3}];assert not exchange(bases)
    def value(s):return max(len(s&b) for b in bases)
    S={0};T={0,2};i=3;assert value(S|{i})-value(S)==0 and value(T|{i})-value(T)==1
    g01.save(root/'nonmatroid.json',dict(bases=[sorted(b) for b in bases],exchange=False,S=sorted(S),T=sorted(T),added=i,small_gain=0,large_gain=1))
if __name__=='__main__':
    root=HERE/'mc01'
    if sys.argv[1]=='prepare':prepare(root)
    else:run(root,next(c for c in json.loads((root/'design.json').read_text())['cases'] if c['name']==sys.argv[1]))
