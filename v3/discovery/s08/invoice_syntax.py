"""Ordinary arithmetic-circuit invoice simplification. DEVELOPMENT."""
from collections import Counter
from itertools import product
from pathlib import Path
import json
import random
import sys
import g01
import invoice_completion as ic
import markov_paths as mk
import paired_invoices as pi
import continuum_policy as cp

HERE=Path(__file__).resolve().parent
Meter=g01.kernel.Meter

class Arena:
    def __init__(self):self.nodes=[('zero',)];self.unique={};self.meter=Meter()
    def intern(self,node):
        self.meter.pay('syntax','canonical_record_lookup',len(node)+2)
        if node not in self.unique:
            if len(self.nodes)>=250000:raise RuntimeError('Syntax-node cap')
            self.unique[node]=len(self.nodes);self.nodes.append(node)
        return self.unique[node]
    def terms(self,edge):
        offset,node=edge
        if node==0:return offset,Counter()
        if self.nodes[node][0]=='sum':return offset,Counter(dict(self.nodes[node][1]))
        return offset,Counter({node:1})
    def packed(self,offset,terms):
        items=tuple(sorted((node,count) for node,count in terms.items() if count))
        if not items:return offset,0
        if len(items)==1 and items[0][1]==1:return offset,items[0][0]
        return offset,self.intern(('sum',items))
    def add(self,edges):
        offset=0;terms=Counter()
        for edge in edges:
            value,local=self.terms(edge);offset+=value;terms.update(local)
            self.meter.pay('syntax','flatten_collect_sum_terms',3+2*len(local))
        return self.packed(offset,terms)
    def ite(self,var,low,high):
        if low==high:return low
        lo,a=self.terms(low);hi,b=self.terms(high);common=a&b
        a.subtract(common);b.subtract(common)
        # All-zero branch is the normalization anchor; signed residual allowed.
        left=self.packed(0,a);right=self.packed(hi-lo,b)
        node=self.intern(('ite',var,left,right));self.meter.pay('syntax','extract_shared_conditional_summands',5+len(common))
        return self.add([self.packed(lo,common),(0,node)])


def compile_policy(arena,costs,roots):
    tables={m:{} for m in('ordinary','left','right')}
    def rec(mode,a,b):
        if a>b:return(0,0)
        if(a,b) in tables[mode]:return tables[mode][a,b]
        if mode=='ordinary' and a==b:value=(0,0)
        else:
            i,e,m=ic.branches(mode,a,b,roots)
            low=arena.add([rec(k,l,h) for k,l,h in e]);high=arena.add([rec(k,l,h) for k,l,h in m])
            value=arena.add([(costs[i],0),arena.ite(i,low,high)])
        tables[mode][a,b]=value;arena.meter.pay('syntax','retain_reachable_interval',4);return value
    root=rec('ordinary',0,len(costs)-1);return root,tables


def evaluate(arena,edge,bits):
    cache={0:0}
    def go(node):
        if node in cache:return cache[node]
        entry=arena.nodes[node]
        if entry[0]=='sum':value=sum(count*go(child) for child,count in entry[1])
        else:
            _,var,low,high=entry;off,child=high if bits[var] else low;value=off+go(child)
        cache[node]=value;return value
    return edge[0]+go(edge[1])


def run(directory):
    directory.mkdir(exist_ok=False);(directory/'impl.py').write_bytes(Path(__file__).read_bytes())
    cases=json.loads((HERE/'ia01/design.json').read_text())['cases']
    old=json.loads((HERE/'cs01/design.json').read_text())['cases']
    cases +=[dict(name=f"service_n{len(old[i]['costs'])}",costs=old[i]['costs']) for i in(0,3,6)]
    g01.save(directory/'design.json',dict(stage='DEVELOPMENT',contributor='Codex (GPT-6)',cases=cases,
        source_sha256=g01.sha(__file__),declaration_sha256=g01.sha(HERE/'invoice_syntax.md'),physical_audits=0))
    result=[];rng=random.Random(8141503)
    for case in cases:
        costs=case['costs'];arena=Arena();bank={};records={};checks=0
        for r in mk.MENU:
            proposal=mk.plan(costs,r);arena.meter.pay('proposal','same_root_proposal',proposal['invoice']['total'])
            root,tables=compile_policy(arena,costs,proposal['roots']);bank[r]=root;records[r]=dict(roots=proposal['roots'],tables=tables,edge=root)
            worlds=list(product((0,1),repeat=len(costs))) if len(costs)<=10 else[tuple(rng.randrange(2) for _ in costs) for _ in range(256)]
            for bits in worlds:
                fee,_=pi.direct_fee(costs,proposal['roots'],bits);assert evaluate(arena,root,bits)==fee;checks+=1
        groups={}
        for r,root in bank.items():groups.setdefault(root,[]).append(r)
        row=dict(name=case['name'],n=len(costs),syntax_nodes=len(arena.nodes),groups=list(groups.values()),world_checks=checks,
            named_units=arena.meter.total,invoice=arena.meter.record())
        g01.save(directory/f"{case['name']}.json",cp.normalize(dict(case=case,nodes=arena.nodes,policies=records,result=row)))
        result.append(row);g01.save(directory/'results.json',dict(status='running',cases=result));print(json.dumps({k:v for k,v in row.items() if k!='invoice'}),flush=True)
    g01.save(directory/'results.json',dict(status='complete',cases=result,physical_audits=0))

if __name__=='__main__':run(Path(sys.argv[1]))
