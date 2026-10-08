#!/usr/bin/env python3
"""P3-05 finite pure-program compiler and independently bound receiver.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-08. Python 3.10+.
The supplied tables/graph are model input, not discovered dependencies. This
compiler neither evaluates arbitrary programs nor authenticates external data.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import sys

sys.dont_write_bytecode = True
_NAME = '_p305_portfolio_receiver_v3'
if _NAME in sys.modules:
    P = sys.modules[_NAME]
else:
    _spec = importlib.util.spec_from_file_location(_NAME, Path(__file__).with_name('05_portfolio_transport.py'))
    if _spec is None or _spec.loader is None: raise ImportError('Missing portfolio dependency.')
    P = importlib.util.module_from_spec(_spec); sys.modules[_NAME] = P; _spec.loader.exec_module(P)
M, K = P.M, P.K
Rejected = P.Rejected
VERSION = 'p305-dependency-v2'
MAX_DEFINITIONS = 64
MAX_TABLES = 16
MAX_OUTPUTS = 16
MAX_AST_NODES = 2048
MAX_AST_DEPTH = 24


def inc(work, key, count=1): P.inc(work, key, count)


def _name(value):
    if type(value) is not str or not value or len(value) > 128:
        raise Rejected('Nonempty capped string identity required.')
    return value


@dataclass(frozen=True)
class Table:
    name: str
    arity: int
    values: tuple[int, ...]

    def validate(self):
        _name(self.name)
        if type(self.arity) is not int or not 0 <= self.arity <= 3:
            raise Rejected('Table arity cap.')
        if type(self.values) is not tuple or len(self.values) != 2**self.arity or any(type(v) is not int or v not in (0,1) for v in self.values):
            raise Rejected('A complete immutable Boolean table is required.')

    def record(self): return {'name':self.name, 'arity':self.arity, 'values':self.values}


@dataclass(frozen=True)
class Program:
    scope: str
    inputs: tuple[str, ...]
    tables: tuple[Table, ...]
    definitions: tuple[tuple[str, tuple], ...]
    outputs: tuple[tuple[str, tuple], ...]

    def record(self):
        validate(self)
        return M.canonical({'version':VERSION, 'scope':self.scope, 'inputs':self.inputs,
            'tables':[t.record() for t in self.tables], 'definitions':self.definitions,'outputs':self.outputs})


def validate(program:Program, work=None):
    if type(program) is not Program: raise Rejected('Program input type.')
    _name(program.scope)
    if type(program.inputs) is not tuple or not 1 <= len(program.inputs) <= M.MAX_BITS:
        raise Rejected('Input tuple/cap.')
    for x in program.inputs: _name(x)
    if len(set(program.inputs)) != len(program.inputs): raise Rejected('Distinct input identities required.')
    if type(program.tables) is not tuple or len(program.tables) > MAX_TABLES: raise Rejected('Table tuple/cap.')
    table={}
    for t in program.tables:
        if type(t) is not Table: raise Rejected('Table type.')
        t.validate(); inc(work,'admitted_table_entries',len(t.values))
        if t.name in table: raise Rejected('Duplicate table identity.')
        table[t.name]=t
    if type(program.definitions) is not tuple or len(program.definitions) > MAX_DEFINITIONS:
        raise Rejected('Definition tuple/cap.')
    if type(program.outputs) is not tuple or not 1 <= len(program.outputs) <= MAX_OUTPUTS:
        raise Rejected('Output tuple/cap.')
    available=set(); count=0
    def expr(e, depth=0):
        nonlocal count
        count+=1; inc(work,'validated_program_nodes')
        if count > MAX_AST_NODES or depth > MAX_AST_DEPTH or type(e) is not tuple or not e or type(e[0]) is not str:
            raise Rejected('Malformed or oversized program expression.')
        op=e[0]
        if op=='const' and len(e)==2 and type(e[1]) is int and e[1] in (0,1): return
        if op=='input' and len(e)==2 and type(e[1]) is int and 0 <= e[1] < len(program.inputs): return
        if op=='ref' and len(e)==2 and type(e[1]) is str and e[1] in available: return
        if op=='not' and len(e)==2: expr(e[1],depth+1);return
        if op in ('and','or','xor') and len(e)==3:
            expr(e[1],depth+1);expr(e[2],depth+1);return
        if op=='call' and len(e)==3 and type(e[1]) is str and e[1] in table and type(e[2]) is tuple and len(e[2])==table[e[1]].arity:
            for x in e[2]:expr(x,depth+1)
            return
        raise Rejected('Unknown operator, forward/cyclic reference, or malformed table call.')
    for entry in program.definitions:
        if type(entry) is not tuple or len(entry)!=2: raise Rejected('Definition entry type.')
        name,e=entry;_name(name)
        if name in available: raise Rejected('Duplicate definition.')
        expr(e);available.add(name)
    outputs=set()
    for entry in program.outputs:
        if type(entry) is not tuple or len(entry)!=2: raise Rejected('Output entry type.')
        name,e=entry;_name(name)
        if name in outputs: raise Rejected('Duplicate output role.')
        expr(e);outputs.add(name)


@dataclass(frozen=True)
class Compilation:
    program_record: str
    outputs: tuple[tuple[str, tuple], ...]
    supports: tuple[tuple[str, tuple[str, ...]], ...]


def compile_program(program:Program, work=None) -> Compilation:
    validate(program,work)
    nbits=len(program.inputs);tables={t.name:t for t in program.tables};definitions={}
    def checked(e):
        if K.validate(e,nbits) != 'bool': raise Rejected('Compiled output must be Boolean.')
        return e
    def meet(es):
        if not es:return K.lit(1)
        if len(es)==1:return es[0]
        k=len(es)//2;return checked(K.AND(meet(es[:k]),meet(es[k:])))
    def join(es):
        if not es:return K.lit(0)
        if len(es)==1:return es[0]
        k=len(es)//2;return checked(K.OR(join(es[:k]),join(es[k:])))
    def go(e):
        inc(work,'compiled_program_nodes');op=e[0]
        if op=='const':return K.lit(e[1]),set()
        if op=='input':return K.bit(e[1]),set()
        if op=='ref':
            inc(work,'compiled_definition_lookups')
            x,s=definitions[e[1]];return x,s|{'D:'+e[1]}
        if op=='not':
            x,s=go(e[1]);return checked(K.neg(x)),s
        if op in ('and','or','xor'):
            a,s=go(e[1]);b,t=go(e[2])
            if op=='and':x=K.AND(a,b)
            elif op=='or':x=K.OR(a,b)
            else:x=K.OR(K.AND(a,K.neg(b)),K.AND(K.neg(a),b))
            return checked(x),s|t
        t=tables[e[1]];args=[go(x) for x in e[2]];clauses=[]
        support={'T:'+t.name}
        for _,s in args:support |= s
        for i,bit in enumerate(t.values):
            inc(work,'compiled_table_rows')
            if bit:
                literals=[a if (i>>(t.arity-j-1))&1 else K.neg(a) for j,(a,_) in enumerate(args)]
                clauses.append(meet(literals))
        return checked(join(clauses)),support
    for name,e in program.definitions: definitions[name]=go(e)
    outputs=[];supports=[]
    for name,e in program.outputs:
        x,s=go(e);outputs.append((name,x));supports.append((name,tuple(sorted(s))))
    return Compilation(program.record(),tuple(outputs),tuple(supports))


def relevant_record(program:Program, role:str, work=None) -> str:
    """Sufficient semantic support, not a minimal slice or a runtime claim."""
    c=compile_program(program,work);outputs=dict(program.outputs)
    if type(role) is not str or role not in outputs: raise Rejected('Unknown output role.')
    support=set(dict(c.supports)[role])
    return M.canonical({'inputs':program.inputs,'root':outputs[role],
        'definitions':[(n,e) for n,e in program.definitions if 'D:'+n in support],
        'tables':[t.record() for t in program.tables if 'T:'+t.name in support]})


@dataclass(frozen=True)
class Comparison:
    scope: str
    old: Program
    new: Program
    weights: tuple[tuple[str,F], ...]
    hard: tuple
    soft: tuple
    unit: str = 'U'

    def record(self):
        _name(self.scope);_name(self.unit)
        if type(self.old) is not Program or type(self.new) is not Program:raise Rejected('Both program records are required.')
        # Use exact strings from validated whole programs; bools cannot be
        # smuggled into integer-valued tables through Python equality.
        old=self.old.record();new=self.new.record()
        if self.old.inputs != self.new.inputs: raise Rejected('Shared input identities must match exactly.')
        if type(self.weights) is not tuple or not self.weights or len(self.weights)>MAX_OUTPUTS:
            raise Rejected('Capped immutable nonempty coefficient table required.')
        roles=set()
        for item in self.weights:
            if type(item) is not tuple or len(item)!=2:raise Rejected('Coefficient entry.')
            name,value=item;_name(name);K.rational(value)
            if name in roles or name not in dict(self.old.outputs) or name not in dict(self.new.outputs):
                raise Rejected('Distinct shared output roles required.')
            roles.add(name)
        if type(self.hard) is not tuple or type(self.soft) is not tuple:raise Rejected('Immutable source constraints required.')
        for h in self.hard:
            if K.validate(h,len(self.old.inputs)) != 'bool':raise Rejected('Boolean source requirement.')
        for s in self.soft:
            if type(s) is not K.Soft:raise Rejected('Soft constraint record type.')
        # K.Request will perform the complete soft/rank checks in compile_comparison.
        return M.canonical({'scope':self.scope,'old':old,'new':new,'weights':self.weights,
            'hard':self.hard,'soft':[{'identity':s.identity,'formula':s.formula,'weight':s.weight,'tier':s.tier} for s in self.soft], 'unit':self.unit})


def compile_comparison(request:Comparison,work=None):
    if type(request) is not Comparison:raise Rejected('Comparison input type.')
    record=request.record();a=compile_program(request.old,work);b=compile_program(request.new,work)
    aa=dict(a.outputs);bb=dict(b.outputs)
    d=P.balanced_sum(K.scale(K.rational(w),K.sub(bb[name],aa[name])) for name,w in request.weights)
    frame=M.Frame(K.Request(len(request.old.inputs),request.hard,request.soft,(('D',d),),
                    request.scope,metadata_json=record),loss='D',unit=request.unit)
    inc(work,'compiled_comparisons')
    return frame


@dataclass(frozen=True)
class DependencyProof:
    comparison_record: str
    portfolio: P.PortfolioProof


def produce(cache:P.PortfolioCache,request:Comparison,choices,witness,bound,*,work=None,**options):
    frame=compile_comparison(request,work)
    return DependencyProof(request.record(),cache.build(frame,choices,witness,bound,work=work,**options))


def receive(cache:P.PortfolioCache,proof:DependencyProof,request:Comparison,expected_record:str,
            requested_bound,work=None):
    if type(proof) is not DependencyProof or type(request) is not Comparison:
        raise Rejected('Dependency proof/request type.')
    record=request.record()
    if type(expected_record) is not str or record != expected_record or proof.comparison_record != record:
        raise Rejected('Program/edit request binding differs.')
    inc(work,'program_record_characters_compared',2*len(record))
    frame=compile_comparison(request,work)
    result=cache.verify(proof.portfolio,frame,frame.record(),work)
    required=K.rational(requested_bound)
    if K.rational(result['bound']) > required:raise Rejected('Certified budget does not meet the independently requested bound.')
    return {'status':'PROGRAM_COMPARISON_CERTIFIED','version':VERSION,'comparison_record':record,
            'requested_bound':str(required),'certificate':result}
