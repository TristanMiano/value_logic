#!/usr/bin/env python3
"""Recompile a declared P3-04 hypothetical source before receiving a P3-05 proof.

The support labels are ordinary bits; quoted negation is compiled by the
paired-support semantics, not silently replaced by flag complementation.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import importlib.util,sys
sys.dont_write_bytecode=True
NAME='_p305_portfolio_receiver_v3'
if NAME in sys.modules:P=sys.modules[NAME]
else:
    sp=importlib.util.spec_from_file_location(NAME,Path(__file__).with_name('05_portfolio_transport.py'))
    if sp is None or sp.loader is None:raise ImportError('Portfolio dependency missing.')
    P=importlib.util.module_from_spec(sp);sys.modules[NAME]=P;sp.loader.exec_module(P)
M,K=P.M,P.K
VERSION='p305-counterpossible-bridge-v2'

@dataclass(frozen=True)
class Query:
    atoms: tuple[str,...]
    antecedent: tuple
    baseline: tuple[int,...]
    exceptions: tuple[str,...]
    frame: tuple[str,...]
    background: tuple[tuple,...]
    difference: tuple
    unit: str='U'

    def compile(self,work=None):
        for x in (self.atoms,self.antecedent,self.baseline,self.exceptions,self.frame,self.background,self.difference):
            if type(x)is not tuple:raise ValueError('Immutable hypothetical input tuples required.')
        if not 1<=len(self.atoms)<=M.MAX_BITS//2:raise ValueError('Hypothetical atom cap.')
        req=K.paired_request(self.atoms,self.antecedent,self.baseline,self.exceptions,self.frame,self.background,False,(('fixed-difference',self.difference),))
        P.inc(work,'paired_sources_recompiled');P.inc(work,'quoted_background_formulas',1+len(self.background))
        return M.Frame(req,'fixed-difference',self.unit)

    def record(self):return self.compile().record()


def receive(cache,proof,query,expected_query_record,requested_bound,work=None):
    if type(query)is not Query or type(cache)is not P.PortfolioCache:raise ValueError('Explicit source request and admitted portfolio cache required.')
    f=query.compile(work);record=f.record()
    if type(expected_query_record)is not str or record!=expected_query_record:raise ValueError('The independently supplied hypothetical request differs.')
    r=cache.verify(proof,f,record,work)
    if K.rational(r['bound'])>K.rational(requested_bound):raise ValueError('The hypothetical proof is weaker than the requested bound.')
    return {**r,'front_end_version':VERSION,'semantic_scope':'P3-04 declared paired support; original quoted formula and ordinary reference interpretation retained in the independently rebuilt record.','philosophical_uniqueness_claimed':False}
