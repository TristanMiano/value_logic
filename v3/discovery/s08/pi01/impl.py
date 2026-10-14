"""Finite shared-world invoice contrasts. DEVELOPMENT, Codex (GPT-6)."""
from itertools import product,combinations
from pathlib import Path
import copy
import json
import random
import sys
import g01
import markov_paths as mk
import invoice_completion as ic
import continuum_policy as cp

HERE=Path(__file__).resolve().parent
VERSION='s08-paired-add-v1'
Meter=g01.kernel.Meter


def produce(n,values,meter):
    if len(values)!=2**n or any(type(v)is not int for v in values):raise ValueError('Truth-table scope')
    nodes=[];unique={}
    def intern(node):
        meter.pay('diagram','canonical_node_lookup',len(node)+1)
        if node not in unique:unique[node]=len(nodes);nodes.append(node)
        return unique[node]
    def go(i,lo,hi):
        if i==n:return intern(('leaf',values[lo]))
        mid=(lo+hi)//2;a=go(i+1,lo,mid);b=go(i+1,mid,hi)
        meter.pay('diagram','shannon_split_and_equal_child_reduction',5)
        return a if a==b else intern(('branch',i,a,b))
    root=go(0,0,len(values));return dict(n=n,root=root,nodes=nodes)


def evaluate(diagram,bits,meter):
    node=diagram['root']
    while diagram['nodes'][node][0]=='branch':
        _,i,a,b=diagram['nodes'][node];node=b if bits[i] else a
        meter.pay('diagram_check','follow_world_edge',3)
    return diagram['nodes'][node][1]


def structure(diagram,meter):
    n=diagram['n'];nodes=diagram['nodes'];unique=set()
    if type(n)is not int or n<1 or type(diagram['root'])is not int or not 0<=diagram['root']<len(nodes):raise ValueError('Diagram source dimensions')
    for index,node in enumerate(nodes):
        node=tuple(node)
        if node in unique:raise ValueError('Noncanonical duplicate')
        unique.add(node)
        if node[0]=='leaf':
            if len(node)!=2 or type(node[1])is not int:raise ValueError('Terminal fee type')
        elif node[0]=='branch':
            if len(node)!=4:raise ValueError('Branch arity')
            _,i,a,b=node
            if any(type(v)is not int for v in (i,a,b)) or not 0<=i<n or not 0<=a<index or not 0<=b<index or a==b:raise ValueError('Nonordered or unreduced branch')
            for child in (nodes[a],nodes[b]):
                if child[0]=='branch' and child[1]<=i:raise ValueError('Variable order')
        else:raise ValueError('Unknown diagram node')
        meter.pay('diagram_check','node_scope_order_and_uniqueness',12)


def bounds(diagram,observed,meter):
    if any(type(i)is not int or not 0<=i<diagram['n'] or type(v)is not int or v not in(0,1) for i,v in observed.items()):raise ValueError('Receipt scope')
    result=[]
    for node in diagram['nodes']:
        if node[0]=='leaf':result.append((node[1],node[1]));meter.pay('restriction','terminal_range',2)
        else:
            _,i,a,b=node
            if i in observed:result.append(result[b if observed[i] else a]);meter.pay('restriction','known_receipt_cofactor',3)
            else:result.append((min(result[a][0],result[b][0]),max(result[a][1],result[b][1])));meter.pay('restriction','joint_extremum',5)
    return result[diagram['root']]


def direct_fee(costs,roots,bits):
    # Independent recursive policy interpreter, distinct from next_query replay.
    visited=[]
    def rec(a,b,mode):
        if a>b or(mode=='ordinary' and a==b):return 0
        i=a if mode=='left' else b if mode=='right' else roots[a,b]
        visited.append(i);middle=bits[i]
        if mode=='left':tail=rec(a+1,b,'left' if middle else 'ordinary')
        elif mode=='right':tail=rec(a,b-1,'right' if middle else 'ordinary')
        else:tail=rec(a,i-1,'right' if middle else 'ordinary')+rec(i+1,b,'left' if middle else 'ordinary')
        return costs[i]+tail
    fee=rec(0,len(costs)-1,'ordinary');assert len(set(visited))==len(visited)
    return fee,visited


def run(directory,n,repeat):
    directory.mkdir(exist_ok=False);rng=random.Random(8141490+10*n+repeat)
    costs=[rng.randrange(1,10) for _ in range(n)];meter=Meter();bank={};proposals={}
    for r in mk.MENU:
        policy=mk.plan(costs,r);meter.pay('preparation','model_policy_proposal',policy['invoice']['total'])
        if policy['roots']not in bank.values():bank[r]=policy['roots'];proposals[r]=policy['invoice']
    worlds=list(product((0,1),repeat=n));truths={};diagrams={};policy_worlds=0
    for r,roots in bank.items():
        values=[]
        for bits in worlds:
            _,queries=mk.conditional_trace(bits,roots);fee=sum(costs[i] for i in queries)
            checked,visited=direct_fee(costs,roots,bits);assert checked==fee and visited==queries
            meter.pay('truth_table','two_policy_world_interpreters',10*n+8*len(queries));policy_worlds+=1;values.append(fee)
        truths[r]=values;diagrams[r]=produce(n,values,meter);structure(diagrams[r],meter)
        assert all(evaluate(diagrams[r],bits,meter)==v for bits,v in zip(worlds,values))
    pairs=[];artifacts={};partial_checks=0;strict=collapsed=0
    for a,b in combinations(bank,2):
        values=[x-y for x,y in zip(truths[a],truths[b])];diagram=produce(n,values,meter);structure(diagram,meter)
        for bits,value in zip(worlds,values):assert evaluate(diagram,bits,meter)==value
        global_joint=bounds(diagram,{},meter);global_separate=(min(truths[a])-max(truths[b]),max(truths[a])-min(truths[b]))
        patterns=list(product((-1,0,1),repeat=n)) if n<=6 else [tuple(rng.choice((-1,0,1)) for _ in range(n)) for _ in range(128)]
        local=[];local_strict=local_collapse=0
        for pattern in patterns:
            observed={i:v for i,v in enumerate(pattern) if v>=0};joint=bounds(diagram,observed,meter)
            ca=bounds(diagrams[a],observed,meter);cb=bounds(diagrams[b],observed,meter);separate=(ca[0]-cb[1],ca[1]-cb[0])
            compatible=[value for bits,value in zip(worlds,values) if all(bits[i]==v for i,v in observed.items())]
            assert joint==(min(compatible),max(compatible))
            assert separate[0]<=joint[0]<=joint[1]<=separate[1]
            gain=(separate[1]-separate[0])-(joint[1]-joint[0]);local_strict+=gain>0
            local_collapse+=joint[0]==joint[1] and separate[0]!=separate[1]
            local.append(dict(pattern=pattern,joint=joint,separate=separate));partial_checks+=1
        strict+=local_strict;collapsed+=local_collapse
        pairs.append(dict(pair=[a,b],joint=global_joint,separate=global_separate,diagram_nodes=len(diagram['nodes']),
            separate_diagram_nodes=len(diagrams[a]['nodes'])+len(diagrams[b]['nodes']),partial_patterns=len(patterns),
            strict_partial_contractions=local_strict,extra_exact_contrasts=local_collapse))
        artifacts[f'{a}_{b}']=dict(diagram=diagram,partial_checks=local)
    negative=[]
    if diagrams:
        diagram=copy.deepcopy(next(iter(diagrams.values())));diagram['nodes'][0]=('leaf',FRAUD:=999999)
        rejected=False
        try:
            structure(diagram,Meter())
            for bits,value in zip(worlds,next(iter(truths.values()))):
                if evaluate(diagram,bits,Meter())!=value:raise ValueError('Wrong invoice function')
        except ValueError:rejected=True
        assert rejected;negative.append('altered_terminal_rejected_by_original_policy_identity')
        changed=copy.deepcopy(next(iter(diagrams.values())));changed['root']=len(changed['nodes'])
        try:structure(changed,Meter())
        except ValueError:negative.append('outside_root_rejected')
        else:raise AssertionError('Outside root accepted')
    g01.save(directory/'artifacts.json',cp.normalize(dict(costs=costs,roots=bank,invoice_diagrams=diagrams,pairs=artifacts)))
    result=dict(status='complete',n=n,repeat=repeat,costs=costs,policies=list(bank),policy_world_executions=policy_worlds,
        pairs=pairs,partial_checks=partial_checks,strict_partial_contractions=strict,extra_exact_contrasts=collapsed,
        negative_controls=negative,named_units=meter.total,invoice=meter.record(),physical_audits=0,
        source_sha256=g01.sha(__file__),declaration_sha256=g01.sha(HERE/'paired_invoices.md'))
    g01.save(directory/'result.json',result)
    print(json.dumps({k:result[k] for k in ('n','repeat','partial_checks','strict_partial_contractions','extra_exact_contrasts','named_units')}))

if __name__=='__main__':run(Path(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))
