#!/usr/bin/env python3
"""P3-04 replacement implementation, not recovered S1 source.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-08.
Standard library, Python 3.10+. Trusted in-process state, finite Boolean source,
known rational losses and fixed positive rational tier weights. No native proof
checker, general arithmetic oracle, external report authenticator, learning
algorithm, or total CPU/memory budget is provided.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from fractions import Fraction as F
from itertools import product
import json
from math import lcm
from typing import Any

VERSION = 'p304-reconstructed-v1'
MAX_BITS, MAX_NODES, MAX_DEPTH, MAX_ROWS, MAX_TIERS = 12, 1024, 32, 128, 8
Expr = tuple
Cell = tuple[int | None, ...]


def rational(v: Any) -> F:
    if isinstance(v, bool) or not isinstance(v, (int, str, F)):
        raise ValueError('Rationals must be integers, strings or Fraction; no float/bool.')
    q = F(v)
    if max(abs(q.numerator).bit_length(), q.denominator.bit_length()) > 128:
        raise ValueError('Input rational exceeds 128-bit component cap.')
    return q


def lit(q: Any) -> Expr: return ('lit', rational(q))
def bit(i: int) -> Expr: return ('bit', i)
def neg(a: Expr) -> Expr: return ('not', a)
def AND(a: Expr, b: Expr) -> Expr: return ('and', a, b)
def OR(a: Expr, b: Expr) -> Expr: return ('or', a, b)
def eq(a: Expr, b: Expr) -> Expr: return ('eq', a, b)
def add(a: Expr, b: Expr) -> Expr: return ('add', a, b)
def scale(q: Any, a: Expr) -> Expr: return ('scale', rational(q), a)
def sub(a: Expr, b: Expr) -> Expr: return add(a, scale(-1, b))


def validate(e: Expr, n: int, depth: int = 0, count: list[int] | None = None) -> str:
    if count is None: count = [0]
    count[0] += 1
    if count[0] > MAX_NODES or depth > MAX_DEPTH:
        raise ValueError('Expression size/depth cap exceeded.')
    if not isinstance(e, tuple) or not e or not isinstance(e[0], str):
        raise ValueError('An expression must be an immutable tagged tuple.')
    op = e[0]
    if op == 'lit' and len(e) == 2:
        q = rational(e[1]); return 'bool' if q in (0, 1) else 'number'
    if op == 'bit' and len(e) == 2:
        if type(e[1]) is not int or not 0 <= e[1] < n: raise ValueError('Bad bit index.')
        return 'bool'
    if op == 'not' and len(e) == 2:
        if validate(e[1], n, depth+1, count) != 'bool': raise ValueError('Boolean not required.')
        return 'bool'
    if op == 'scale' and len(e) == 3:
        rational(e[1]); validate(e[2], n, depth+1, count); return 'number'
    if op in ('and', 'or', 'eq', 'add', 'min', 'max') and len(e) == 3:
        kinds = [validate(a, n, depth+1, count) for a in e[1:]]
        if op in ('and','or') and kinds != ['bool','bool']: raise ValueError('Boolean operands required.')
        return 'bool' if op in ('and','or','eq') else 'number'
    raise ValueError('Unknown operation or incorrect arity.')


def interval(e: Expr, c: Cell, work: dict[str,int] | None = None) -> tuple[F,F]:
    if work is not None: work['expression_nodes'] = work.get('expression_nodes',0)+1
    op = e[0]
    if op == 'lit': return F(e[1]), F(e[1])
    if op == 'bit': return (F(0),F(1)) if c[e[1]] is None else (F(c[e[1]]),)*2
    if op == 'not':
        lo,hi=interval(e[1],c,work); return 1-hi,1-lo
    if op == 'scale':
        lo,hi=interval(e[2],c,work); q=F(e[1]); return min(q*lo,q*hi),max(q*lo,q*hi)
    a,b=interval(e[1],c,work),interval(e[2],c,work)
    if op == 'add': return a[0]+b[0],a[1]+b[1]
    if op in ('and','min'): return min(a[0],b[0]),min(a[1],b[1])
    if op in ('or','max'): return max(a[0],b[0]),max(a[1],b[1])
    if op == 'eq':
        if a[1]<b[0] or b[1]<a[0]: return F(0),F(0)
        if a[0]==a[1]==b[0]==b[1]: return F(1),F(1)
        return F(0),F(1)
    raise ValueError('Unknown operation.')


@dataclass(frozen=True)
class Soft:
    identity: str
    formula: Expr
    weight: F = F(1)
    tier: int = 0


@dataclass(frozen=True)
class Request:
    nbits: int
    hard: tuple[Expr,...]
    soft: tuple[Soft,...]
    losses: tuple[tuple[str,Expr],...]
    scope: str
    # Full interpretation/reference metadata, not just a digest or display ID.
    metadata_json: str = '{}'
    def __post_init__(self):
        if type(self.nbits) is not int or not 0<=self.nbits<=MAX_BITS: raise ValueError('Bit cap.')
        if not self.scope or not isinstance(self.scope,str): raise ValueError('Scope required.')
        if any(not isinstance(x,tuple) for x in (self.hard,self.soft,self.losses)): raise ValueError('Immutable input required.')
        if len(self.hard)>MAX_ROWS or len(self.soft)>MAX_ROWS or len(self.losses)>32: raise ValueError('Row cap.')
        if len(self.metadata_json)>65536 or not isinstance(json.loads(self.metadata_json),dict): raise ValueError('Metadata must be a capped JSON object.')
        for h in self.hard:
            if validate(h,self.nbits)!='bool': raise ValueError('Hard constraint must be Boolean.')
        seen=set()
        for s in self.soft:
            if not isinstance(s,Soft) or not isinstance(s.identity,str) or not s.identity or s.identity in seen: raise ValueError('Unique nonempty soft identity required.')
            seen.add(s.identity)
            if rational(s.weight)<=0 or type(s.tier) is not int or not 0<=s.tier<MAX_TIERS: raise ValueError('Positive weight and valid tier required.')
            if validate(s.formula,self.nbits)!='bool': raise ValueError('Soft constraint must be Boolean.')
        names=set()
        for name,e in self.losses:
            if not isinstance(name,str) or not name or name in names: raise ValueError('Unique loss label required.')
            names.add(name);validate(e,self.nbits)
    @property
    def tiers(self) -> int: return max((s.tier for s in self.soft),default=0)+1
    def record(self) -> dict:
        def enc(x):
            if isinstance(x,F): return str(x)
            if isinstance(x,tuple):return [enc(v) for v in x]
            return x
        return {'version':VERSION,'scope':self.scope,'nbits':self.nbits,'metadata':json.loads(self.metadata_json),
                'hard':enc(self.hard),'soft':[{'id':s.identity,'formula':enc(s.formula),'weight':str(s.weight),'tier':s.tier} for s in self.soft],
                'losses':enc(self.losses)}


@dataclass
class Search:
    request: Request
    frontier: list[Cell] = field(init=False)
    best: set[tuple[int,...]] = field(default_factory=set,init=False)
    incumbent: tuple[F,...] | None = field(default=None,init=False)
    work: dict[str,int] = field(default_factory=lambda:{'cells_popped':0,'expression_nodes':0,'reports':0,'seed_checks':0},init=False)
    _record: dict = field(init=False,repr=False)
    def __post_init__(self):
        self.frontier=[(None,)*self.request.nbits];self._record=self.request.record()
    def _check(self):
        if self.request.record()!=self._record:raise ValueError('Changed request requires a fresh search.')
    def bound(self,c:Cell) -> tuple[bool,tuple[F,...]]:
        ok=all(interval(e,c,self.work)[1]==1 for e in self.request.hard)
        rank=[F(0)]*self.request.tiers
        for s in self.request.soft:rank[s.tier]+=F(s.weight)*(1-interval(s.formula,c,self.work)[1])
        return ok,tuple(rank)
    def _accept(self,x:tuple[int,...],rank:tuple[F,...]):
        if self.incumbent is None or rank<self.incumbent:self.incumbent=rank;self.best={x}
        elif rank==self.incumbent:self.best.add(x)
    def seed(self,x:tuple[int,...]):
        self._check();self.work['seed_checks']+=1
        if not isinstance(x,tuple) or len(x)!=self.request.nbits or any(type(v) is not int or v not in (0,1) for v in x):raise ValueError('Invalid seed.')
        ok,r=self.bound(x)
        if not ok:raise ValueError('Infeasible seed.')
        self._accept(x,r)
    def advance(self,pops:int=1):
        self._check()
        if type(pops) is not int or not 0<=pops<=100000:raise ValueError('Invalid frontier-pop allowance.')
        for _ in range(pops):
            if not self.frontier:break
            c=self.frontier.pop();self.work['cells_popped']+=1
            ok,low=self.bound(c)
            if not ok or self.incumbent is not None and low>self.incumbent:continue
            if None not in c:self._accept(c,low);continue
            i=c.index(None)
            for v in (1,0):self.frontier.append(c[:i]+(v,)+c[i+1:])
    def cover(self) -> list[Cell]:
        self._check();out=list(sorted(self.best))
        for c in self.frontier:
            ok,low=self.bound(c)
            if ok and (self.incumbent is None or low<=self.incumbent):out.append(c)
        return out
    def report(self) -> dict:
        self._check();self.work['reports']+=1
        eligible=[]
        for c in self.frontier:
            ok,low=self.bound(c)
            if ok and (self.incumbent is None or low<=self.incumbent):eligible.append((c,low))
        witness=self.incumbent is not None
        complete=not eligible
        rank_exact=witness and all(low>=self.incumbent for _,low in eligible)
        cover=list(sorted(self.best))+[c for c,_ in eligible]
        out={'version':VERSION,'request':self._record,'feasibility':'NONEMPTY' if witness else 'INFEASIBLE' if complete else 'UNKNOWN',
             'identities_complete':complete,'rank_exact':bool(rank_exact),'incumbent_rank':self.incumbent,
             'best_witnesses':sorted(self.best),'eligible_frontier':len(eligible),'losses':{}}
        for name,e in self.request.losses:
            ranges=[interval(e,c,self.work) for c in cover]
            bounds=(min(v[0] for v in ranges),max(v[1] for v in ranges)) if ranges else None
            vals=sorted({interval(e,c,self.work)[0] for c in self.best})
            hull_exact=witness and (bounds[0]==bounds[1] or rank_exact and vals and vals[0]==bounds[0] and vals[-1]==bounds[1])
            # A cover can be bounded with unknown feasibility: never call that a useful certificate.
            out['losses'][name]={'outer':bounds,'value_exact':bool(witness and bounds[0]==bounds[1]),
                                 'hull_exact':bool(hull_exact),'image':vals if complete and witness else None}
        out['work']=dict(self.work)
        return out
    def support_report(self, positive:Expr, negative:Expr) -> dict:
        for e in (positive,negative):
            if validate(e,self.request.nbits)!='bool':raise ValueError('Boolean support required.')
        r=self.report()
        if r['feasibility']!='NONEMPTY':return {'positive':r['feasibility'],'negative':r['feasibility']}
        cover=self.cover();out={}
        for label,e in [('positive',positive),('negative',negative)]:
            ranges=[interval(e,c,self.work) for c in cover]
            if min(x[0] for x in ranges)==1:status='YES'
            elif max(x[1] for x in ranges)==0:status='NO'
            elif r['rank_exact'] and any(interval(e,x,self.work)[0]==0 for x in self.best):status='NO'
            else:status='UNRESOLVED'
            out[label]=status
        return out


def paired(e:Expr, atoms:tuple[str,...]) -> tuple[Expr,Expr]:
    """Compile quoted propositional syntax. Constants are ('top',), ('bottom',)."""
    visited = [0]
    def walk(f,depth=0):
        visited[0] += 1
        if visited[0] > MAX_NODES: raise ValueError('Quoted formula node cap.')
        if depth>MAX_DEPTH:raise ValueError('Quoted formula depth cap.')
        if not isinstance(f,tuple) or not f:raise ValueError('Invalid quoted syntax.')
        if f[0]=='atom' and len(f)==2:
            if f[1] not in atoms:raise ValueError('Undeclared atom.')
            i=atoms.index(f[1]);return bit(2*i),bit(2*i+1)
        if f==('top',):return lit(1),lit(0)
        if f==('bottom',):return lit(0),lit(1)
        if f[0]=='not' and len(f)==2:
            t,n=walk(f[1],depth+1);return n,t
        if f[0] in ('and','or') and len(f)==3:
            a,b=walk(f[1],depth+1),walk(f[2],depth+1)
            return (AND(a[0],b[0]),OR(a[1],b[1])) if f[0]=='and' else (OR(a[0],b[0]),AND(a[1],b[1]))
        raise ValueError('Unsupported quoted connective.')
    if not atoms or len(set(atoms))!=len(atoms) or len(atoms)>MAX_BITS//2 or any(not isinstance(a,str) or not a for a in atoms):raise ValueError('Invalid finite atom list.')
    answer=walk(e)
    for f in answer:validate(f,2*len(atoms))
    return answer


def paired_request(atoms:tuple[str,...], antecedent:Expr, baseline:tuple[int,...], exceptions:tuple[str,...],
                   frame:tuple[str,...]=(), background:tuple[Expr,...]=(), preserve_baseline:bool=False,
                   losses:tuple[tuple[str,Expr],...]=()) -> Request:
    t,_=paired(antecedent,atoms)
    if len(baseline)!=len(atoms) or any(type(b) is not int or b not in (0,1) for b in baseline):raise ValueError('Reference must supply ordinary bits.')
    for names in (exceptions,frame):
        if len(set(names))!=len(names) or any(a not in atoms for a in names):raise ValueError('Invalid exception/frame identities.')
    hard=[t]+[paired(f,atoms)[0] for f in background];soft=[]
    for i,a in enumerate(atoms):
        normal=eq(add(bit(2*i),bit(2*i+1)),lit(1))
        if a in exceptions:soft.append(Soft('normal:'+a,normal))
        else:hard.append(normal)
        if a in frame:hard.extend([eq(bit(2*i),lit(baseline[i])),eq(bit(2*i+1),lit(1-baseline[i]))])
        if preserve_baseline:
            soft.extend([Soft('reference:'+a+':t',eq(bit(2*i),lit(baseline[i])),F(1),1),Soft('reference:'+a+':f',eq(bit(2*i+1),lit(1-baseline[i])),F(1),1)])
    meta={'operation':'counterpossible','atoms':atoms,'quoted_antecedent':antecedent,'ordinary_baseline':baseline,'exceptions':exceptions,'frame':frame,'background':background,'preserve_baseline':preserve_baseline,'interpretation':'ordinary Boolean reference; paired support only in the hypothetical evaluation'}
    return Request(2*len(atoms),tuple(hard),tuple(soft),losses,'paired-support-reconstruction',json.dumps(meta,sort_keys=True))


def horn_closure(reference:tuple[int,...], seeds:tuple[int,...], rules:tuple[tuple[tuple[int,...],int],...], allowed:tuple[int,...]) -> dict:
    n=len(reference)
    if not 1<=n<=MAX_BITS//2 or any(type(b) is not int or b not in (0,1) for b in reference):raise ValueError('Reference cap/type.')
    if len(rules)>MAX_ROWS or len(seeds)>2*n or len(set(allowed))!=len(allowed):raise ValueError('Policy cap/identities.')
    if any(type(i) is not int or not 0<=i<n for i in allowed):raise ValueError('Exception index.')
    indices=list(seeds)
    for body,head in rules:indices+=list(body)+[head]
    if any(type(i) is not int or not 0<=i<2*n for i in indices):raise ValueError('Rule support index.')
    ref={2*i if b else 2*i+1 for i,b in enumerate(reference)}
    state=ref|set(seeds);passes=tests=insertions=0
    while True:
        changed=False;passes+=1
        for body,head in rules:
            tests+=len(body)
            if set(body)<=state and head not in state:state.add(head);insertions+=1;changed=True
        if not changed:break
    conflicts=[i for i in range(n) if 2*i in state and 2*i+1 in state and i not in allowed]
    return {'status':'INFEASIBLE' if conflicts else 'NONEMPTY_UNIQUE_MINIMUM','bits':tuple(int(i in state) for i in range(2*n)),
            'forbidden_conflicts':conflicts,'reference_satisfies_rule_policy':all(not set(b)<=ref or h in ref for b,h in rules),
            'rule_body_checks':tests,'passes':passes,'new_rule_bits':insertions}


@dataclass(frozen=True)
class Equation:
    name: str
    domain: tuple[int,...]
    parents: tuple[str,...]
    table: tuple[tuple[tuple[int,...],int],...]


def structural(equations:tuple[Equation,...], context:dict[str,int], intervene:dict[str,int]|None=None) -> dict[str,int]:
    """Total finite acyclic tables in topological order; intervention severs one equation."""
    if len(equations)>32 or len(context)>32:raise ValueError('Graph cap.')
    if any(not isinstance(k,str) or type(v)is not int for k,v in context.items()):raise ValueError('Exogenous context type.')
    state=dict(context);domains={k:(v,) for k,v in context.items()};change=intervene or {}
    names={e.name for e in equations}
    if not set(change)<=names:raise ValueError('Unknown intervention target.')
    for e in equations:
        if not e.name or e.name in state or not 1<=len(e.domain)<=16 or len(set(e.domain))!=len(e.domain) or any(type(v)is not int for v in e.domain):raise ValueError('Variable name/domain.')
        if len(set(e.parents))!=len(e.parents) or any(p not in state for p in e.parents):raise ValueError('Requires acyclic ordered parents.')
        if len(e.table)>4096:raise ValueError('Table cap.')
        table=dict(e.table)
        if len(table)!=len(e.table):raise ValueError('Repeated input row.')
        entries=1
        for p in e.parents:
            entries*=len(domains[p])
            if entries>4096: raise ValueError('Cartesian table construction cap.')
        required=set(product(*(domains[p] for p in e.parents)))
        if not required<=set(table) or any(type(v)is not int or v not in e.domain for v in table.values()):raise ValueError('Partial/invalid table.')
        if e.name in change:
            if type(change[e.name])is not int or change[e.name] not in e.domain:raise ValueError('Bad intervention value.')
            state[e.name]=change[e.name]
        else:state[e.name]=table[tuple(state[p] for p in e.parents)]
        domains[e.name]=e.domain
    return state


def route_replacement(original:tuple[int,...],replacement:tuple[int,...],history:int,calls:tuple[tuple[str,bool],...],required:int=1) -> dict:
    if not original or len(original)!=len(replacement) or len(original)>4096:raise ValueError('Finite table cap.')
    if type(history)is not int or not 0<=history<len(original) or type(required)is not int:raise ValueError('History/required output.')
    if any(type(v)is not int for v in original+replacement) or replacement[history]!=required:raise ValueError('Replacement does not meet the requested output.')
    if len(calls)>32 or len({n for n,_ in calls})!=len(calls) or any(not isinstance(n,str) or not n or type(b)is not bool for n,b in calls):raise ValueError('Routing identities.')
    return {'original':original,'replacement':replacement,'history':history,'routing':calls,'hamming_distance':sum(a!=b for a,b in zip(original,replacement)),
            'outputs':{name:(replacement if follow else original)[history] for name,follow in calls}}


def scalar_weights(req:Request) -> tuple[int,...]:
    den=[1]*req.tiers
    for s in req.soft:den[s.tier]=lcm(den[s.tier],F(s.weight).denominator)
    bounds=[sum((int(den[k]*F(s.weight)) for s in req.soft if s.tier==k),0) for k in range(req.tiers)]
    mult=[1]*req.tiers
    for k in reversed(range(req.tiers)):mult[k]=1+sum(mult[j]*bounds[j] for j in range(k+1,req.tiers))
    return tuple(mult[s.tier]*int(den[s.tier]*F(s.weight)) for s in req.soft)


def compile_cnf(req:Request) -> dict:
    """Full gate equivalences, one weighted root per soft identity. Boolean subgrammar only."""
    clauses=[];gates=[];cache={};nextvar=req.nbits+1
    def root(e):
        nonlocal nextvar
        if e in cache:return cache[e]
        if e[0]=='bit':return e[1]+1
        if e[0]=='lit' and F(e[1]) in (0,1):
            y=nextvar;nextvar+=1;clauses.append((y if F(e[1]) else -y,));gates.append((y,'const',int(F(e[1]))));cache[e]=y;return y
        if e[0] not in ('not','and','or','eq'):raise ValueError('CNF adapter only supports Boolean gates, not arithmetic equality.')
        children=e[1:]
        if any(validate(c,req.nbits)!='bool' for c in children):raise ValueError('CNF operands must be Boolean.')
        args=tuple(root(c) for c in children);y=nextvar;nextvar+=1;cache[e]=y;gates.append((y,e[0],*args))
        if e[0]=='not':
            a=args[0];clauses.extend([(-y,-a),(y,a)])
        else:
            a,b=args
            if e[0]=='and':clauses.extend([(-y,a),(-y,b),(y,-a,-b)])
            elif e[0]=='or':clauses.extend([(y,-a),(y,-b),(-y,a,b)])
            else:clauses.extend([(-y,-a,b),(-y,a,-b),(y,a,b),(y,-a,-b)])
        return y
    for e in req.hard:clauses.append((root(e),))
    soft=[{'id':s.identity,'root':root(s.formula),'weight':str(s.weight),'tier':s.tier} for s in req.soft]
    return {'variables':nextvar-1,'original_bits':req.nbits,'hard_clauses':clauses,'gates':gates,'soft_roots':soft}


def line_regions(lines:tuple[tuple[F,F],...], domain:tuple[F,F]) -> list[tuple[F,F]|None]:
    if not lines or len(lines)>128:raise ValueError('Nonempty capped line family.')
    lines=tuple((rational(a),rational(b)) for a,b in lines);left,right=map(rational,domain)
    if left>right:raise ValueError('Empty parameter interval.')
    out=[]
    for a,b in lines:
        lo,hi=left,right;bad=False
        for c,d in lines:
            m,z=a-c,b-d
            if m==0:
                if z>0:bad=True;break
            elif m>0:hi=min(hi,-z/m)
            else:lo=max(lo,-z/m)
        out.append(None if bad or lo>hi else (lo,hi))
    return out


def envelope_gap(lower:tuple[F,F],lines:tuple[tuple[F,F],...],domain:tuple[F,F]) -> F:
    if not lines or len(lines)>128:raise ValueError('Feasible incumbent lines required.')
    lo,hi=map(rational,domain)
    if lo>hi:raise ValueError('Empty interval.')
    a,b=map(rational,lower);lines=tuple((rational(c),rational(d)) for c,d in lines);points={lo,hi}
    for c,d in lines:
        for e,f in lines:
            if c!=e:
                p=(f-d)/(c-e)
                if lo<=p<=hi:points.add(p)
    return min(a*t+b-min(c*t+d for c,d in lines) for t in points)


def independent_rank_box(bounds:tuple[tuple[F,F],...]) -> dict:
    if not bounds or len(bounds)>4096:raise ValueError('Nonempty finite intervals required.')
    bounds=tuple((rational(lo),rational(hi)) for lo,hi in bounds)
    if any(lo>hi for lo,hi in bounds):raise ValueError('Reversed interval.')
    u=min(hi for lo,hi in bounds);winners=tuple(i for i,(lo,hi) in enumerate(bounds) if lo<=u)
    return {'possible_winners':winners,'simultaneous_witness':tuple(u if i in winners else lo for i,(lo,hi) in enumerate(bounds)),
            'selected_rank_range':(min(lo for lo,hi in bounds),u)}


def gate_term(lower:Any,upper:Any,w:Expr,b:Expr) -> Expr:
    lo,hi=rational(lower),rational(upper)
    if lo>hi:raise ValueError('Reversed weight bounds.')
    # lo*b + min(w-lo,(hi-lo)*b), on b in {0,1} and lo<=w<=hi.
    return add(scale(lo,b),('min',sub(w,lit(lo)),scale(hi-lo,b)))


def gate_source() -> tuple[dict,...]:
    """Ax<=b in coordinates (w,b,g). Numerical rows; units remain declared metadata."""
    return ({'unit_groups':(('w','g'),('b',)), 'A':((0,1,0),(0,-1,0),(0,0,1),(0,0,-1)), 'b':(0,0,0,0),'witness':(0,0,0)},
            {'unit_groups':(('w','g'),('b',)), 'A':((0,1,0),(0,-1,0),(-1,0,1),(1,0,-1)), 'b':(1,-1,0,0),'witness':(0,1,0)})
