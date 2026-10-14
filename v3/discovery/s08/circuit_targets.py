"""Direct normalized-circuit fee contrast evaluation; DEVELOPMENT."""
from collections import Counter
from itertools import product,permutations
from pathlib import Path
import copy
import json
import sys
import invoice_syntax as sy
import check_invoice_syntax as sc
import paired_invoices as pi
import markov_paths as mk
import g01

HERE=Path(__file__).resolve().parent
Meter=g01.kernel.Meter


class Evaluator:
    def __init__(self,arena,costs):
        self.arena=arena;self.costs=costs;self.meter=Meter();self.cache={};self.supports=[0]
    def support(self,node):
        while len(self.supports)<len(self.arena.nodes):
            entry=self.arena.nodes[len(self.supports)]
            if entry[0]=='sum':value=0
            else:value=1<<entry[1]
            children=[child for child,count in entry[1]] if entry[0]=='sum' else [entry[2][1],entry[3][1]]
            for child in children:value|=self.supports[child]
            self.supports.append(value);self.meter.pay('evaluation','syntactic_support_retention',4+len(children))
        return self.supports[node]
    def restrict(self,edge,observed):
        offset,node=edge;support=self.support(node)
        local=tuple(sorted((i,v) for i,v in observed.items() if support>>i&1));key=node,local
        self.meter.pay('evaluation','receipt_cofactor_key_and_lookup',2+len(observed))
        if key not in self.cache:
            if not local:value=(0,node)
            elif node==0:value=(0,0)
            else:
                entry=self.arena.nodes[node]
                if entry[0]=='sum':
                    items=[]
                    for child,count in entry[1]:
                        o,n=self.restrict((0,child),observed);terms=self.arena.terms((o,n))
                        items.append(self.arena.packed(terms[0]*count,Counter({k:v*count for k,v in terms[1].items()})))
                    value=self.arena.add(items)
                elif entry[1] in observed:value=self.restrict(entry[2+observed[entry[1]]],observed)
                else:value=self.arena.ite(entry[1],self.restrict(entry[2],observed),self.restrict(entry[3],observed))
            self.cache[key]=value;self.meter.pay('evaluation','retain_checked_form_cofactor',4)
        o,n=self.cache[key];return offset+o,n
    def residual(self,left,right,known):
        a=self.restrict(left,known);b=self.restrict(right,known)
        ca,ta=self.arena.terms(a);cb,tb=self.arena.terms(b);ta.subtract(tb)
        terms={node:count for node,count in ta.items() if count};support=0
        for node in terms:support|=self.support(node)
        self.meter.pay('evaluation','cancel_shared_signed_invoice_terms',5+2*(len(ta)+len(tb)))
        return ca-cb,terms,support
    def execute(self,left,right,known,bits):
        observed=dict(known);queries=[]
        while True:
            offset,terms,support=self.residual(left,right,observed)
            if not terms:return offset,queries,observed
            options=[i for i in range(len(self.costs)) if support>>i&1]
            if not options:raise ValueError('Unresolved constant circuit')
            var=min(options,key=lambda i:(self.costs[i],i));assert var not in observed
            queries.append(var);observed[var]=bits[var];self.meter.pay('evaluation','choose_cheapest_remaining_target_variable',3*len(options))


def run(directory,case):
    directory.mkdir(exist_ok=False);costs=case['costs'];n=len(costs);arena=sy.Arena();meter=Meter();bank={};edges={};aliases={};proofs={}
    proposals=[]
    for r in mk.MENU:
        p=mk.plan(costs,r);meter.pay('proposal','same_markov_menu',p['invoice']['total']);proposals.append((f'r{r}',p['roots']))
    for rule in('left','right','middle'):
        roots={(a,b):(a if rule=='left' else b if rule=='right' else(a+b)//2) for a in range(n) for b in range(a+1,n)}
        meter.pay('proposal','simple_interval_root_rule',3*len(roots));proposals.append((rule,roots))
    for name,roots in proposals:
        duplicate=next((a for a,r in bank.items() if r==roots),None)
        if duplicate is not None:aliases[duplicate].append(name);continue
        bank[name]=roots;aliases[name]=[name];edge,tables=sy.compile_policy(arena,costs,roots);checking=sc.check(arena.nodes,costs,roots,tables,edge)
        edges[name]=edge;proofs[name]=dict(roots=roots,tables=tables,edge=edge,checking=checking)
        meter.pay('preparation','local_source_invoice_recurrence_check',checking['total'])
    compile_units=arena.meter.total;meter.pay('preparation','original_syntax_compilation',compile_units)
    evaluator=Evaluator(arena,costs);totals=Counter();subgroups={'model_pair':Counter(),'expanded_pair':Counter()};completion_checks=0;witnesses=[]
    with (directory/'worlds.jsonl').open('w') as out:
        for bits in case['worlds']:
            data={name:pi.direct_fee(costs,roots,bits) for name,roots in bank.items()}
            for a,b in permutations(bank,2):
                fa,queries=data[a];fb,_=data[b];known={i:bits[i] for i in queries}
                value,target,observed=evaluator.execute(edges[a],edges[b],known,bits);assert value==fa-fb
                # Independently establish the reported scalar for every compatible completion.
                missing=[i for i in range(n) if i not in observed]
                for assignment in product((0,1),repeat=len(missing)):
                    completed=[observed.get(i,0) for i in range(n)]
                    for i,v in zip(missing,assignment):completed[i]=v
                    fee_a,_=pi.direct_fee(costs,bank[a],completed);fee_b,_=pi.direct_fee(costs,bank[b],completed)
                    assert fee_a-fee_b==value;completion_checks+=1
                state=[known.get(i,-1) for i in range(n)];replay=[]
                while True:
                    var=mk.pc.next_query(state,bank[b])
                    if var is None:break
                    replay.append(var);state[var]=bits[var]
                target_fee=sum(costs[i] for i in target);replay_fee=sum(costs[i] for i in replay)
                subgroup='model_pair' if any(x.startswith('r') and x!='right' for x in aliases[a]) and any(x.startswith('r') and x!='right' for x in aliases[b]) else'expanded_pair'
                record=dict(bits=bits,logger=a,alternative=b,logger_queries=queries,target_queries=target,replay_queries=replay,
                    target_fee=target_fee,replay_fee=replay_fee,contrast=value,subgroup=subgroup)
                out.write(json.dumps(record,separators=(',',':'))+'\n')
                for counter in(totals,subgroups[subgroup]):
                    counter['cases']+=1;counter['target_fee']+=target_fee;counter['replay_fee']+=replay_fee
                    counter['wins']+=target_fee<replay_fee;counter['losses']+=target_fee>replay_fee;counter['ties']+=target_fee==replay_fee
                    counter['zero_target']+=not target;counter['zero_replay']+=not replay
                if target_fee<replay_fee and len(witnesses)<8:witnesses.append(record)
    meter.pay('evaluation','all_direct_circuit_evaluation',evaluator.meter.total)
    meter.pay('evaluation','retained_cofactor_circuit_construction',arena.meter.total-compile_units)
    result=dict(status='complete',name=case['name'],n=n,costs=costs,policies=list(bank),aliases=aliases,
        totals=totals,subgroups=subgroups,completion_checks=completion_checks,syntax_nodes=len(arena.nodes),cofactor_cache=len(evaluator.cache),
        invoice=meter.record(),physical_audits=0,witnesses=witnesses)
    g01.save(directory/'source.json',ib_normalize(dict(costs=costs,nodes=arena.nodes,policies=proofs)))
    g01.save(directory/'result.json',result);print(json.dumps(dict(name=case['name'],totals=totals,subgroups=subgroups,units=meter.total)),flush=True)


def ib_normalize(data):
    import continuum_policy as cp
    return cp.normalize(data)

if __name__=='__main__':
    design=json.loads(Path(sys.argv[2]).read_text());case=next(c for c in design['cases'] if c['name']==sys.argv[3]);run(Path(sys.argv[1]),case)
