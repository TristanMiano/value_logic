#!/usr/bin/env python3
"""Ordinary finite rational ADD comparator, independently reconstructed.

P3-05 DEVELOPMENT. Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-08.
Uses fixed-order Shannon decomposition, unique nodes and cached pointwise Apply.
Not CUDD, a new ADD algorithm, or a polynomial-time solver. Private in-process
state is trusted; exported nodes are audit data, not an authenticated proof.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import importlib.util, sys
sys.dont_write_bytecode=True
_NAME='_p305_portfolio_base'
if _NAME in sys.modules:M=sys.modules[_NAME]
else:
    sp=importlib.util.spec_from_file_location(_NAME,Path(__file__).with_name('05_counterfactual_transport.py'))
    if sp is None or sp.loader is None:raise ImportError('Missing frame dependency.')
    M=importlib.util.module_from_spec(sp);sys.modules[_NAME]=M;sp.loader.exec_module(M)
K=M.K
VERSION='p305-ordinary-add-v1'
MAX_DIAGRAM_NODES=100000
MAX_CACHE_ENTRIES=200000


def inc(w,k,n=1):
    if w is not None:w[k]=w.get(k,0)+n


class Manager:
    def __init__(self,nbits,order=None):
        if type(nbits) is not int or not 1<=nbits<=M.MAX_BITS:raise ValueError('Bit cap.')
        order=tuple(range(nbits)) if order is None else order
        M._permutation(order,nbits)
        self.nbits=nbits;self.order=order;self.position={v:i for i,v in enumerate(order)}
        self.nodes=[];self.boolean=[];self.unique={};self.operations={};self.expressions={}

    def _id(self,a):
        if type(a) is not int or not 0<=a<len(self.nodes):raise ValueError('Unknown diagram node.')

    def _level(self,a):
        self._id(a);n=self.nodes[a]
        return self.nbits if n[0]=='terminal' else self.position[n[1]]

    def terminal(self,value,work=None):
        if type(value) not in (int,F):raise ValueError('Exact computed rational required.')
        q=F(value)
        if max(abs(q.numerator).bit_length(),q.denominator.bit_length())>16384:raise ValueError('Computed rational cap.')
        if work is not None:work['max_rational_component_bits']=max(work.get('max_rational_component_bits',0),abs(q.numerator).bit_length(),q.denominator.bit_length())
        return self._intern(('terminal',q),work)

    def _intern(self,node,work=None):
        inc(work,'unique_lookups')
        if node in self.unique:
            inc(work,'unique_hits');return self.unique[node]
        if len(self.nodes)>=MAX_DIAGRAM_NODES:raise ValueError('Diagram node cap reached.')
        i=len(self.nodes);self.nodes.append(node)
        self.boolean.append(node[1] in (0,1) if node[0]=='terminal' else self.boolean[node[2]] and self.boolean[node[3]])
        self.unique[node]=i;inc(work,'nodes_created');return i

    def node(self,var,low,high,work=None):
        self._id(low);self._id(high)
        if type(var) is not int or var not in self.position or self._level(low)<=self.position[var] or self._level(high)<=self.position[var]:
            raise ValueError('Ordered diagram requirement.')
        if low==high:inc(work,'redundant_nodes_removed');return low
        return self._intern(('node',var,low,high),work)

    def apply(self,op,a,b,work=None):
        self._id(a);self._id(b)
        if op not in ('add','mul','min','max','eq','le','gt','and','or','sub'):
            raise ValueError('Unknown ADD operator.')
        if op in ('and','or') and not(self.boolean[a] and self.boolean[b]):raise ValueError('Boolean ADD operands required.')
        inc(work,'apply_calls')
        if op in ('add','mul','min','max','eq','and','or') and a>b:a,b=b,a
        key=(op,a,b)
        if key in self.operations:inc(work,'apply_cache_hits');return self.operations[key]
        inc(work,'apply_cache_misses')
        na,nb=self.nodes[a],self.nodes[b]
        if a==b and op in ('min','max','and','or'):out=a
        elif a==b and op in ('eq','le'):out=self.terminal(1,work)
        elif a==b and op in ('sub','gt'):out=self.terminal(0,work)
        elif na[0]==nb[0]=='terminal':
            x,y=na[1],nb[1];inc(work,'terminal_operations')
            if op=='add':v=x+y
            elif op=='sub':v=x-y
            elif op=='mul':v=x*y
            elif op=='min':v=min(x,y)
            elif op=='max':v=max(x,y)
            elif op=='eq':v=F(x==y)
            elif op=='le':v=F(x<=y)
            elif op=='gt':v=F(x>y)
            else:
                if x not in (0,1) or y not in (0,1):raise ValueError('Boolean ADD operands required.')
                v=F((x==1 and y==1) if op=='and' else (x==1 or y==1))
            out=self.terminal(v,work)
        else:
            # Exact controlling values, not fallible data-dependent shortcuts.
            zeroa=na[0]=='terminal' and na[1]==0;zerob=nb[0]=='terminal' and nb[1]==0
            onea=na[0]=='terminal' and na[1]==1;oneb=nb[0]=='terminal' and nb[1]==1
            if op in ('mul','and') and (zeroa or zerob):out=self.terminal(0,work)
            elif op=='or' and (onea or oneb):out=self.terminal(1,work)
            elif op=='add' and zeroa:out=b
            elif op=='add' and zerob:out=a
            elif op=='mul' and onea:out=b
            elif op=='mul' and oneb:out=a
            elif op=='and' and onea:out=b
            elif op=='and' and oneb:out=a
            elif op=='or' and zeroa:out=b
            elif op=='or' and zerob:out=a
            else:
                level=min(self._level(a),self._level(b));var=self.order[level]
                alo,ahi=(na[2],na[3]) if self._level(a)==level else (a,a)
                blo,bhi=(nb[2],nb[3]) if self._level(b)==level else (b,b)
                out=self.node(var,self.apply(op,alo,blo,work),self.apply(op,ahi,bhi,work),work)
        if len(self.operations)>=MAX_CACHE_ENTRIES:raise ValueError('Apply cache cap reached.')
        self.operations[key]=out
        return out

    def compile(self,expression,work=None):
        K.validate(expression,self.nbits)
        inc(work,'validated_expressions')
        inc(work,'expression_record_characters',len(M._key(expression)))
        def go(e):
            inc(work,'expression_visits')
            if e in self.expressions:inc(work,'expression_cache_hits');return self.expressions[e]
            inc(work,'expression_cache_misses');op=e[0]
            if op=='lit':out=self.terminal(F(e[1]),work)
            elif op=='bit':out=self.node(e[1],self.terminal(0,work),self.terminal(1,work),work)
            elif op=='not':out=self.apply('sub',self.terminal(1,work),go(e[1]),work)
            elif op=='scale':out=self.apply('mul',self.terminal(F(e[1]),work),go(e[2]),work)
            else:out=self.apply(op,go(e[1]),go(e[2]),work)
            if len(self.expressions)>=MAX_CACHE_ENTRIES:raise ValueError('Expression cache cap reached.')
            self.expressions[e]=out;return out
        return go(expression)

    def evaluate(self,node,x,work=None):
        self._id(node);M._point(x,self.nbits)
        while self.nodes[node][0]!='terminal':
            inc(work,'diagram_evaluation_nodes');n=self.nodes[node];node=n[2+x[n[1]]]
        inc(work,'diagram_evaluation_nodes');return self.nodes[node][1]

    def extrema(self,guard,value,work=None):
        """Exact attained extrema under a Boolean guard, or explicit emptiness."""
        self._id(guard);self._id(value)
        if not self.boolean[guard]:raise ValueError('Boolean guard required.')
        cache={};zero=(0,)*self.nbits
        def go(g,v):
            inc(work,'extrema_calls')
            if (g,v) in cache:inc(work,'extrema_cache_hits');return cache[(g,v)]
            ng,nv=self.nodes[g],self.nodes[v]
            if ng[0]=='terminal' and ng[1] not in (0,1):raise ValueError('Boolean guard required.')
            if ng==('terminal',F(0)):out=None
            elif ng[0]==nv[0]=='terminal':out=(nv[1],nv[1],zero,zero)
            else:
                level=min(self._level(g),self._level(v));var=self.order[level]
                branches=[]
                for bit in (0,1):
                    gg=ng[2+bit] if self._level(g)==level else g
                    vv=nv[2+bit] if self._level(v)==level else v
                    r=go(gg,vv)
                    if r is not None:
                        lo,hi,lx,hx=r
                        lx=lx[:var]+(bit,)+lx[var+1:];hx=hx[:var]+(bit,)+hx[var+1:]
                        branches.append((lo,hi,lx,hx))
                if not branches:out=None
                else:
                    low=min(branches,key=lambda t:(t[0],t[2]));high=max(branches,key=lambda t:(t[1],tuple(-i for i in t[3])))
                    out=(low[0],high[1],low[2],high[3])
            cache[(g,v)]=out;return out
        return go(guard,value)

    def query(self,frame,witness,expected_record,work=None):
        if type(frame) is not M.Frame or frame.request.nbits!=self.nbits:raise ValueError('Matching Frame/input count required.')
        frame.__post_init__();record=frame.record()
        if type(expected_record) is not str or record!=expected_record:raise ValueError('Independent current record mismatch.')
        inc(work,'record_characters_compared',len(record))
        M._point(witness,self.nbits)
        for h in frame.request.hard:
            inc(work,'feasibility_checks')
            if K.interval(h,witness,work)!=(F(1),F(1)):raise ValueError('Feasible incumbent required.')
        cutoff=M.rank_bounds(frame,witness,work)[0]
        guard=self.terminal(1,work);rank=self.terminal(0,work)
        for h in frame.request.hard:guard=self.apply('and',guard,self.compile(h,work),work)
        for s in frame.request.soft:
            failure=self.apply('sub',self.terminal(1,work),self.compile(s.formula,work),work)
            term=self.apply('mul',self.terminal(s.weight,work),failure,work)
            rank=self.apply('add',rank,term,work)
        guard=self.apply('and',guard,self.apply('le',rank,self.terminal(cutoff,work),work),work)
        value=self.compile(frame.difference,work);result=self.extrema(guard,value,work)
        if result is None:raise AssertionError('Checked incumbent contradicts computed empty sublevel.')
        lo,hi,lx,hx=result
        return {'status':'EXACT_CURRENT_SUBLEVEL_RANGE','version':VERSION,'current_record':record,
            'incumbent_rank':str(cutoff),'lower':str(lo),'upper':str(hi),'lower_witness':lx,'upper_witness':hx,
            'roots':{'guard':guard,'rank':rank,'difference':value},'storage':self.storage(),
            'meaning':'Exact range on the same incumbent sublevel, not necessarily just the minimum-ranked subset.'}

    def storage(self):
        return {'diagram_nodes':len(self.nodes),'unique_entries':len(self.unique),'apply_cache_entries':len(self.operations),
            'expression_cache_entries':len(self.expressions), 'node_serialization_bytes':len(M.canonical(self.nodes).encode())}

    def export(self):
        return {'version':VERSION,'bits':self.nbits,'order':self.order,'nodes':self.nodes,
            'scope':'Private correctly constructed manager; audit export alone is not a verified imported diagram.'}
