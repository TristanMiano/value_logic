"""Compositional exact invoice ADDs, independent recurrence checking.
DEVELOPMENT, Codex (GPT-6), 2026-10-14. Natural variable order only.
"""
from collections import Counter
from itertools import product,combinations
from pathlib import Path
import copy
import json
import random
import sys
import g01
import markov_paths as mk
import invoice_completion as ic
import paired_invoices as pi
import continuum_policy as cp

HERE=Path(__file__).resolve().parent
Meter=g01.kernel.Meter
NODE_CAP=250000
STATE_CAP=2000000

class BudgetExceeded(Exception):pass


class Arena:
    def __init__(self,n):
        self.n=n;self.nodes=[];self.unique={};self.cache={};self.ites={};self.meter=Meter();self.zero=self.leaf(0)
    def node(self,record):
        self.meter.pay('add','canonical_record_lookup',len(record)+1)
        if record in self.unique:return self.unique[record]
        if len(self.nodes)>=NODE_CAP:raise BudgetExceeded('Created-node cap')
        i=len(self.nodes);self.nodes.append(record);self.unique[record]=i;return i
    def leaf(self,value):return self.node(('leaf',value))
    def branch(self,var,a,b):
        if a==b:return a
        assert var<self.var(a) and var<self.var(b)
        return self.node(('branch',var,a,b))
    def var(self,node):return self.n if self.nodes[node][0]=='leaf' else self.nodes[node][1]
    def cofactor(self,node,var,bit):
        entry=self.nodes[node];return entry[2+bit] if self.var(node)==var else node
    def apply(self,op,a,b):
        if op=='add' and a>b:a,b=b,a
        key=op,a,b
        if key in self.cache:return self.cache[key]
        if len(self.cache)+len(self.ites)>=STATE_CAP:raise BudgetExceeded('Apply-state cap')
        self.meter.pay('add','arithmetic_apply_state',10)
        if a==b and op=='sub':result=self.zero
        elif self.var(a)==self.n and self.var(b)==self.n:
            x=self.nodes[a][1];y=self.nodes[b][1];result=self.leaf(x+y if op=='add' else x-y)
        else:
            var=min(self.var(a),self.var(b))
            lo=self.apply(op,self.cofactor(a,var,0),self.cofactor(b,var,0))
            hi=self.apply(op,self.cofactor(a,var,1),self.cofactor(b,var,1))
            result=self.branch(var,lo,hi)
        self.cache[key]=result;return result
    def ite(self,var,low,high):
        key=var,low,high
        if key in self.ites:return self.ites[key]
        if len(self.cache)+len(self.ites)>=STATE_CAP:raise BudgetExceeded('Apply-state cap')
        self.meter.pay('add','ordered_indicator_ite_state',9)
        if low==high:result=low
        else:
            top=min(var,self.var(low),self.var(high))
            if top==var:result=self.branch(var,self.cofactor(low,var,0),self.cofactor(high,var,1))
            else:result=self.branch(top,self.ite(var,self.cofactor(low,top,0),self.cofactor(high,top,0)),self.ite(var,self.cofactor(low,top,1),self.cofactor(high,top,1)))
        self.ites[key]=result;return result
    def add_many(self,values):
        result=self.zero
        for value in values:result=self.apply('add',result,value)
        return result


def compile_policy(arena,costs,roots):
    ic.validate(costs,roots,{})
    tables={m:{} for m in ('ordinary','left','right')}
    for length in range(1,len(costs)+1):
        for a in range(len(costs)-length+1):
            b=a+length-1
            for mode in tables:
                if mode=='ordinary' and a==b:node=arena.zero
                else:
                    i,e,m=ic.branches(mode,a,b,roots)
                    low=arena.add_many([tables[k][l,h] for k,l,h in e if l<=h])
                    high=arena.add_many([tables[k][l,h] for k,l,h in m if l<=h])
                    node=arena.apply('add',arena.leaf(costs[i]),arena.ite(i,low,high))
                tables[mode][a,b]=node;arena.meter.pay('compile','retain_invoice_recurrence',4)
    return tables


def check_equation(nodes,n,result,var,cost,extreme,middle,meter):
    """Shannon-zero checker, independent of producer apply/ITE/unique table."""
    visited=set();linear_seen=set()
    def top(node):return n if nodes[node][0]=='leaf' else nodes[node][1]
    def child(node,v,bit):return nodes[node][2+bit] if top(node)==v else node
    def linear(terms,constant):
        counts=Counter()
        for factor,node in terms:
            if top(node)==n:constant+=factor*nodes[node][1]
            else:counts[node]+=factor
        terms=tuple(sorted((factor,node) for node,factor in counts.items() if factor))
        key=terms,constant
        if key in linear_seen:return
        linear_seen.add(key);meter.pay('check','normalize_and_split_linear_identity',5+4*len(terms))
        if not terms:
            if constant:raise ValueError('Invalid invoice recurrence')
            return
        v=min(top(node) for _,node in terms)
        for bit in (0,1):linear([(f,child(node,v,bit)) for f,node in terms],constant)
    def branch(res,e,m):
        key=res,e,m
        if key in visited:return
        visited.add(key);meter.pay('check','conditional_invoice_identity_state',10+len(e)+len(m))
        v=min([var,top(res)]+[top(node) for node in e+m])
        if v==var:
            for bit,items in ((0,e),(1,m)):
                linear([(1,child(res,v,bit))]+[(-1,child(node,v,bit)) for node in items],-cost)
        else:
            for bit in (0,1):branch(child(res,v,bit),tuple(child(node,v,bit) for node in e),tuple(child(node,v,bit) for node in m))
    branch(result,tuple(extreme),tuple(middle))


def check_policy(arena,costs,roots,tables,check_structure=True):
    ic.validate(costs,roots,{});meter=Meter();n=len(costs)
    if check_structure:pi.structure(dict(n=n,nodes=arena.nodes,root=tables['ordinary'][0,n-1]),meter)
    states={(a,b) for a in range(n) for b in range(a,n)}
    if set(tables)!={'ordinary','left','right'} or any(set(t)!=states for t in tables.values()):raise ValueError('Invoice-table scope')
    def at(mode,a,b):return tables[mode][a,b] if a<=b else None
    for a,b in states:
        for mode in tables:
            result=tables[mode][a,b]
            if type(result)is not int or not 0<=result<len(arena.nodes):raise ValueError('Invoice root scope')
            if mode=='ordinary' and a==b:
                if arena.nodes[result]!=('leaf',0):raise ValueError('Nonzero isolated-node invoice')
                continue
            # Independently restate the three policy cases.
            i=a if mode=='left' else b if mode=='right' else roots[a,b]
            if mode=='left':e=[at('ordinary',a+1,b)];m=[at('left',a+1,b)]
            elif mode=='right':e=[at('ordinary',a,b-1)];m=[at('right',a,b-1)]
            else:e=[at('ordinary',a,i-1),at('ordinary',i+1,b)];m=[at('right',a,i-1),at('left',i+1,b)]
            check_equation(arena.nodes,n,result,i,costs[i],[x for x in e if x is not None],[x for x in m if x is not None],meter)
    return meter.record()


def reachable(arena,root):
    seen=set();todo=[root]
    while todo:
        node=todo.pop()
        if node in seen:continue
        seen.add(node)
        if arena.nodes[node][0]=='branch':todo.extend(arena.nodes[node][2:])
    return seen


def run(directory,costs):
    directory.mkdir(exist_ok=False);arena=Arena(len(costs));bank={};records={};truth_checks=0
    try:
        for r in mk.MENU:
            proposed=mk.plan(costs,r);arena.meter.pay('proposal','markov_policy_proposal_only',proposed['invoice']['total'])
            roots=proposed['roots'];tables=compile_policy(arena,costs,roots);checking=check_policy(arena,costs,roots,tables)
            arena.meter.pay('admission','independent_invoice_recurrence_check',checking['total']);root=tables['ordinary'][0,len(costs)-1]
            bank[r]=root;records[r]=dict(roots=roots,tables=tables,checking=checking,final_root=root,reachable_nodes=len(reachable(arena,root)))
            if len(costs)<=10:
                diagram=dict(n=len(costs),root=root,nodes=arena.nodes)
                for bits in product((0,1),repeat=len(costs)):
                    fee,_=pi.direct_fee(costs,roots,bits);assert pi.evaluate(diagram,bits,Meter())==fee;truth_checks+=1
            g01.save(directory/'progress.json',dict(completed_policies=list(records),created_nodes=len(arena.nodes),apply_states=len(arena.cache)+len(arena.ites),invoice=arena.meter.record()))
        pairs=[]
        for a,b in combinations(bank,2):
            root=arena.apply('sub',bank[a],bank[b]);diag=dict(n=len(costs),root=root,nodes=arena.nodes)
            interval=pi.bounds(diag,{},arena.meter)
            pairs.append(dict(pair=[a,b],root=root,global_interval=interval,reachable_nodes=len(reachable(arena,root)),identical_invoice=bank[a]==bank[b]))
        negative=[]
        first=next(iter(records.values()));bad=copy.deepcopy(first['tables']);bad['ordinary'][0,len(costs)-1]=arena.leaf(999999)
        try:check_policy(arena,costs,first['roots'],bad)
        except ValueError:negative.append('altered_final_invoice_rejected')
        else:raise AssertionError('Invalid final invoice accepted')
        groups={}
        for r,root in bank.items():groups.setdefault(root,[]).append(r)
        result=dict(status='complete',costs=costs,n=len(costs),created_nodes=len(arena.nodes),apply_states=len(arena.cache)+len(arena.ites),
            root_map_groups=len({str(sorted(v['roots'].items())) for v in records.values()}),invoice_groups=list(groups.values()),pairs=pairs,
            truth_checks=truth_checks,negative_controls=negative,invoice=arena.meter.record(),physical_audits=0)
        g01.save(directory/'certificate.json',cp.normalize(dict(costs=costs,nodes=arena.nodes,policies=records,pairs=pairs)))
    except BudgetExceeded as exc:
        result=dict(status='budget_exceeded',reason=str(exc),costs=costs,n=len(costs),completed_policies=list(records),
            created_nodes=len(arena.nodes),apply_states=len(arena.cache)+len(arena.ites),invoice=arena.meter.record(),physical_audits=0)
    g01.save(directory/'result.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in('pairs','invoice','costs')}))


if __name__=='__main__':run(Path(sys.argv[1]),json.loads(sys.argv[2]))
