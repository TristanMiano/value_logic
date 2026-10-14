"""Ordinary EVBDD compilation for checked policy invoices. DEVELOPMENT."""
from collections import Counter
from itertools import product,combinations
from pathlib import Path
import copy
import json
import random
import sys
import invoice_add as ia
import invoice_completion as ic
import paired_invoices as pi
import continuum_policy as cp
import markov_paths as mk
import g01

HERE=Path(__file__).resolve().parent
Meter=g01.kernel.Meter

class Arena:
    def __init__(self,n):
        self.n=n;self.nodes=[('terminal',)];self.unique={};self.cache={};self.ites={};self.meter=Meter();self.zero=(0,0)
    def leaf(self,value):return value,0
    def var(self,node):return self.n if node==0 else self.nodes[node][0]
    def branch(self,var,low,high):
        lo,a=low;hi,b=high
        if low==high:return low
        assert var<self.var(a) and var<self.var(b)
        record=(var,a,hi-lo,b);self.meter.pay('evbdd','normalize_edge_and_unique_lookup',7)
        if record not in self.unique:
            if len(self.nodes)>=ia.NODE_CAP:raise ia.BudgetExceeded('Created-node cap')
            self.unique[record]=len(self.nodes);self.nodes.append(record)
        return lo,self.unique[record]
    def cofactor(self,edge,var,bit):
        offset,node=edge
        if self.var(node)!=var:return edge
        _,a,delta,b=self.nodes[node]
        return (offset+delta,b) if bit else(offset,a)
    def apply(self,op,left,right):
        oa,a=left;ob,b=right;offset=oa+(ob if op=='add' else -ob)
        if op=='add' and a>b:a,b=b,a
        key=op,a,b
        if key not in self.cache:
            if len(self.cache)+len(self.ites)>=ia.STATE_CAP:raise ia.BudgetExceeded('Apply-state cap')
            self.meter.pay('evbdd','offset_quotient_arithmetic_apply',12)
            if (a==b and op=='sub') or(a==b==0):value=self.zero
            else:
                var=min(self.var(a),self.var(b))
                low=self.apply(op,self.cofactor((0,a),var,0),self.cofactor((0,b),var,0))
                high=self.apply(op,self.cofactor((0,a),var,1),self.cofactor((0,b),var,1))
                value=self.branch(var,low,high)
            assert value[0]==0;self.cache[key]=value
        o,node=self.cache[key];return offset+o,node
    def ite(self,var,low,high):
        offset,a=low;ho,b=high;delta=ho-offset;key=var,a,delta,b
        if key not in self.ites:
            if len(self.cache)+len(self.ites)>=ia.STATE_CAP:raise ia.BudgetExceeded('Apply-state cap')
            self.meter.pay('evbdd','offset_normalized_indicator_ite',11)
            if a==b and delta==0:value=(0,a)
            else:
                top=min(var,self.var(a),self.var(b))
                if top==var:value=self.branch(var,self.cofactor((0,a),var,0),self.cofactor((delta,b),var,1))
                else:value=self.branch(top,self.ite(var,self.cofactor((0,a),top,0),self.cofactor((delta,b),top,0)),
                    self.ite(var,self.cofactor((0,a),top,1),self.cofactor((delta,b),top,1)))
            self.ites[key]=value
        o,node=self.ites[key];return offset+o,node
    def add_many(self,values):
        result=self.zero
        for value in values:result=self.apply('add',result,value)
        return result


def structure(arena,meter):
    nodes=arena.nodes;n=arena.n;seen=set()
    if not nodes or nodes[0]!=('terminal',):raise ValueError('Zero terminal')
    for index,node in enumerate(nodes[1:],1):
        if len(node)!=4 or any(type(v)is not int for v in node):raise ValueError('EVBDD record')
        var,a,delta,b=node
        if not 0<=var<n or not 0<=a<index or not 0<=b<index or(a==b and delta==0):raise ValueError('EVBDD order or reduction')
        if (a and nodes[a][0]<=var) or(b and nodes[b][0]<=var):raise ValueError('Variable order')
        if node in seen:raise ValueError('Duplicate normalized node')
        seen.add(node);meter.pay('check','normalized_edge_node_scope',14)


class IdentityChecker:
    def __init__(self,arena):self.nodes=arena.nodes;self.n=arena.n;self.meter=Meter();self.seen=set()
    def top(self,edge):return self.n if edge[1]==0 else self.nodes[edge[1]][0]
    def child(self,edge,var,bit):
        offset,node=edge
        if self.top(edge)!=var:return edge
        _,a,delta,b=self.nodes[node];return(offset+delta,b) if bit else(offset,a)
    def linear(self,terms,constant=0):
        coeff=Counter()
        for factor,(offset,node) in terms:
            constant+=factor*offset
            if node:coeff[node]+=factor
        terms=tuple(sorted((factor,node) for node,factor in coeff.items() if factor));key=terms,constant
        if key in self.seen:return
        self.seen.add(key);self.meter.pay('check','independent_offset_linear_identity',7+4*len(terms))
        if not terms:
            if constant:raise ValueError('False edge-valued identity')
            return
        var=min(self.nodes[node][0] for _,node in terms)
        for bit in(0,1):self.linear([(f,self.child((0,node),var,bit)) for f,node in terms],constant)
    def conditional(self,result,var,cost,extreme,middle):
        visited=set()
        def go(res,e,m):
            key=res,e,m
            if key in visited:return
            visited.add(key);self.meter.pay('check','independent_conditional_invoice_identity',12+len(e)+len(m))
            top=min([var,self.top(res)]+[self.top(edge) for edge in e+m])
            if top==var:
                for bit,children in((0,e),(1,m)):
                    self.linear([(1,self.child(res,var,bit))]+[(-1,self.child(edge,var,bit)) for edge in children],-cost)
            else:
                for bit in(0,1):go(self.child(res,top,bit),tuple(self.child(edge,top,bit) for edge in e),tuple(self.child(edge,top,bit) for edge in m))
        go(result,tuple(extreme),tuple(middle))


def check_policy(arena,costs,roots,tables):
    ic.validate(costs,roots,{});checker=IdentityChecker(arena);structure(arena,checker.meter)
    states={(a,b) for a in range(len(costs)) for b in range(a,len(costs))}
    if set(tables)!={'ordinary','left','right'} or any(set(t)!=states for t in tables.values()):raise ValueError('Invoice recurrence scope')
    def at(m,a,b):return tables[m][a,b] if a<=b else None
    for a,b in states:
        for mode in tables:
            result=tables[mode][a,b]
            if len(result)!=2 or any(type(v)is not int for v in result) or not 0<=result[1]<len(arena.nodes):raise ValueError('Invoice edge type/scope')
            if a==b and mode=='ordinary':checker.linear([(1,result)]);continue
            i=a if mode=='left' else b if mode=='right' else roots[a,b]
            if mode=='left':e=[at('ordinary',a+1,b)];m=[at('left',a+1,b)]
            elif mode=='right':e=[at('ordinary',a,b-1)];m=[at('right',a,b-1)]
            else:e=[at('ordinary',a,i-1),at('ordinary',i+1,b)];m=[at('right',a,i-1),at('left',i+1,b)]
            checker.conditional(result,i,costs[i],[v for v in e if v is not None],[v for v in m if v is not None])
    return checker.meter.record()


def evaluate(arena,edge,bits):
    value,node=edge
    while node:
        var,a,delta,b=arena.nodes[node]
        if bits[var]:value+=delta;node=b
        else:node=a
    return value


def bounds(arena,edge,observed,meter):
    if any(type(i)is not int or not 0<=i<arena.n or type(v)is not int or v not in(0,1) for i,v in observed.items()):raise ValueError('Receipt indicator scope')
    cache={0:(0,0)}
    def visit(node):
        if node in cache:return cache[node]
        var,a,delta,b=arena.nodes[node];meter.pay('restriction','reachable_edge_extrema',8)
        if var in observed:
            lo,hi=visit(b if observed[var] else a);shift=delta if observed[var] else 0;answer=(lo+shift,hi+shift)
        else:
            l,h=visit(a);p,q=visit(b);answer=(min(l,delta+p),max(h,delta+q))
        cache[node]=answer;return answer
    lo,hi=visit(edge[1]);return lo+edge[0],hi+edge[0]


def run(directory,costs):
    directory.mkdir(exist_ok=False);arena=Arena(len(costs));records={};bank={};checks=0;rng=random.Random(8141502+len(costs))
    try:
        for r in mk.MENU:
            proposal=mk.plan(costs,r);arena.meter.pay('proposal','same_markov_root_proposal',proposal['invoice']['total'])
            roots=proposal['roots'];tables=ia.compile_policy(arena,costs,roots);checking=check_policy(arena,costs,roots,tables)
            arena.meter.pay('admission','independent_edge_invoice_check',checking['total']);edge=tables['ordinary'][0,len(costs)-1]
            bank[r]=edge;records[r]=dict(roots=roots,tables=tables,checking=checking,final_edge=edge)
            worlds=list(product((0,1),repeat=len(costs))) if len(costs)<=10 else [tuple(rng.randrange(2) for _ in costs) for _ in range(256)]
            for bits in worlds:
                fee,_=pi.direct_fee(costs,roots,bits);assert evaluate(arena,edge,bits)==fee;checks+=1
            g01.save(directory/'progress.json',dict(completed_policies=list(records),created_nodes=len(arena.nodes),apply_states=len(arena.cache)+len(arena.ites),invoice=arena.meter.record()))
        pairs=[];checker=IdentityChecker(arena)
        for a,b in combinations(bank,2):
            edge=arena.apply('sub',bank[a],bank[b]);checker.linear([(1,edge),(-1,bank[a]),(1,bank[b])])
            interval=bounds(arena,edge,{},arena.meter)
            pairs.append(dict(pair=[a,b],edge=edge,global_interval=interval,identical_invoice=bank[a]==bank[b]))
        arena.meter.pay('admission','independent_pair_subtraction_check',checker.meter.total)
        negatives=[];first=next(iter(records.values()));bad=copy.deepcopy(first['tables']);off,node=bad['ordinary'][0,len(costs)-1];bad['ordinary'][0,len(costs)-1]=(off+1,node)
        try:check_policy(arena,costs,first['roots'],bad)
        except ValueError:negatives.append('changed_root_offset_rejected')
        else:raise AssertionError('Changed invoice accepted')
        old=arena.nodes[-1];arena.nodes[-1]=(len(costs),0,1,0)
        try:structure(arena,Meter())
        except ValueError:negatives.append('outside_variable_rejected')
        else:raise AssertionError('Outside variable accepted')
        finally:arena.nodes[-1]=old
        groups={}
        for r,edge in bank.items():groups.setdefault(edge,[]).append(r)
        result=dict(status='complete',n=len(costs),costs=costs,created_nodes=len(arena.nodes),apply_states=len(arena.cache)+len(arena.ites),
            invoice_groups=list(groups.values()),world_checks=checks,pairs=pairs,negative_controls=negatives,
            invoice=arena.meter.record(),physical_audits=0)
        g01.save(directory/'certificate.json',cp.normalize(dict(costs=costs,nodes=arena.nodes,policies=records,pairs=pairs)))
    except ia.BudgetExceeded as exc:
        result=dict(status='budget_exceeded',reason=str(exc),n=len(costs),costs=costs,completed_policies=list(records),created_nodes=len(arena.nodes),
            apply_states=len(arena.cache)+len(arena.ites),invoice=arena.meter.record(),physical_audits=0)
    g01.save(directory/'result.json',result);print(json.dumps({k:v for k,v in result.items() if k not in('pairs','invoice','costs')}))

if __name__=='__main__':run(Path(sys.argv[1]),json.loads(sys.argv[2]))
