#!/usr/bin/env python3
"""Rational lower certificates proposed by a persistent continuous cut LP.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12. LP status is advisory;
weak duality with checked cuts and exact nonnegative rational multipliers
establishes the returned value. This does not enumerate Boolean masks.
"""
from __future__ import annotations

import copy
from fractions import Fraction
import math
import time

import highspy
import numpy as np

import native_repair as native
import rup_bridge_v2 as rup

VERSION='s06-rational-cut-dual-v1'


def rational_dual(cuts,multipliers,source_id,meter):
    if len(cuts)!=len(multipliers):
        raise ValueError('One multiplier per admitted cut required')
    if not cuts:
        raise ValueError('At least one admitted cut required')
    m=len(cuts[0]['weights'])
    lam=[Fraction(x) for x in multipliers]
    if any(x<0 for x in lam):
        raise ValueError('Nonnegative exact multipliers required')
    a=[Fraction(0)]*m
    K=Fraction(0)
    for cut,value in zip(cuts,lam):
        if cut['structural_source_id']!=source_id or len(cut['weights'])!=m:
            raise ValueError('Cut source or feature meanings changed')
        K+=value*(cut['budget']+1)
        a=[x+value*q for x,q in zip(a,cut['weights'])]
        meter.pay('dual_check','exact_cut_linear_combination',2*m+3)
    result=dict(version=VERSION,structural_source_id=source_id,
                cut_dependencies=[c['receipt_id'] for c in cuts],
                multipliers=[str(x) for x in lam],coefficient=[str(x) for x in a],constant=str(K),
                domain='Same source violation features; any real weight vector, with Boolean violations')
    result['receipt_id']=native.kernel.digest(result)
    meter.pay('dual_storage','multiplier_coefficient_and_dependency_words',3*len(cuts)+2*m+8)
    return result


def point_lower(certificate,weights,meter,integral=False):
    a=[Fraction(x) for x in certificate['coefficient']]
    if len(a)!=len(weights):
        raise ValueError('Objective length changed')
    if integral and any(type(w) is not int for w in weights):
        raise ValueError('Ceiling requires an integral objective')
    value=Fraction(certificate['constant'])-sum(max(Fraction(0),x-Fraction(w)) for x,w in zip(a,weights))
    value=max(Fraction(0),value)
    meter.pay('dual_evaluation','exact_column_slack_and_sum',4*len(a)+3)
    return -((-value.numerator)//value.denominator) if integral else value


def fixed_box_bound(certificate,mask,lower,upper,price,meter):
    a=[Fraction(x) for x in certificate['coefficient']]
    lo,hi=list(map(Fraction,lower)),list(map(Fraction,upper))
    if len(a)!=len(lo) or len(lo)!=len(hi) or any(x<0 or y<x for x,y in zip(lo,hi)):
        raise ValueError('Nonnegative warranted coordinate enclosure required')
    K=Fraction(certificate['constant'])
    if mask is None:
        value=Fraction(price)-K+sum(max(Fraction(0),x-l) for x,l in zip(a,lo))
    else:
        if type(mask) is not int or not 0<=mask<(1<<len(a)):
            raise ValueError('Boolean action mask required')
        contrast=-K+sum(max(h,x) if mask&(1<<j) else max(Fraction(0),x-l)
                        for j,(x,l,h) in enumerate(zip(a,lo,hi)))
        replace=sum(h for j,h in enumerate(hi) if mask&(1<<j))-price
        value=max(contrast,replace)
    meter.pay('dual_evaluation','fixed_action_box_regret',5*len(a)+5)
    return max(Fraction(0),value)


class PersistentCutDual:
    """Own raw-proof admission, retained continuous rows, and objective updates."""
    def __init__(self,instance):
        self.instance=copy.deepcopy(instance)
        self.source_id=native.structural_id(instance)
        self.m=len(instance['soft'])
        self.cuts=[]
        self.duals=[]
        self.meter=native.kernel.Meter()
        self.hs=highspy.Highs()
        self.hs.setOptionValue('output_flag',False)
        self.hs.setOptionValue('threads',1)
        self.hs.setOptionValue('random_seed',0)
        for _ in range(self.m):
            self.hs.addCol(0.0,0.0,1.0,0,np.array([],dtype=np.int32),np.array([],dtype=float))
            self.meter.pay('dual_setup','continuous_column',6)
        self.weights=None
        self.calls=[]

    def add_export(self,raw_purchase):
        # Actually check the raw original-source CNF proof. A cached checked
        # flag or multiplier cannot independently create a row of this LP.
        cut=rup.check_export(self.instance,raw_purchase,self.meter)
        if any(c['receipt_id']==cut['receipt_id'] for c in self.cuts):
            return cut
        q=cut['weights']
        indices=[j for j,x in enumerate(q) if x]
        self.hs.addRow(float(cut['budget']+1),highspy.kHighsInf,len(indices),
                       np.array(indices,dtype=np.int32),np.array([q[j] for j in indices],dtype=float))
        self.cuts.append(cut)
        self.meter.pay('dual_setup','admitted_cut_row',2*len(indices)+4)
        return cut

    def propose(self,weights,seconds=1.0,denominator=1_000_000):
        if not self.cuts:
            raise ValueError('No admitted cut to propose from')
        if len(weights)!=self.m or any(type(w) is not int or w<0 for w in weights):
            raise ValueError('Nonnegative integer query objective required')
        if type(denominator) is not int or denominator<1 or not math.isfinite(seconds) or seconds<=0:
            raise ValueError('Positive finite proposal limits required')
        cpu,wall=time.process_time_ns(),time.perf_counter_ns()
        changed=self.weights!=list(weights)
        if changed:
            self.hs.changeColsCost(self.m,np.arange(self.m,dtype=np.int32),np.array(weights,dtype=float))
            self.meter.pay('dual_objective','objective_update',2*self.m+2)
            self.weights=list(weights)
        self.hs.setOptionValue('time_limit',seconds)
        status=self.hs.run()
        native_status=str(self.hs.getModelStatus())
        proposed=self.hs.getSolution().row_dual
        # Every nonnegative rational is safe; status/floating feasibility do
        # not establish the bound. Invalid proposals fall back to zero.
        multipliers=[]
        for i in range(len(self.cuts)):
            x=proposed[i] if i<len(proposed) else 0
            multipliers.append(Fraction(str(max(0.0,x))).limit_denominator(denominator)
                               if math.isfinite(x) else Fraction(0))
            self.meter.pay('dual_proposal','finite_nonnegative_rationalization',5)
        receipt=rational_dual(self.cuts,multipliers,self.source_id,self.meter)
        self.duals.append(receipt)
        call=dict(native_status=native_status,api_status=str(status),objective_changed=changed,
                  rows=len(self.cuts),columns=self.m,weights=list(weights),seconds_cap=seconds,
                  dual_receipt_id=receipt['receipt_id'],native_lp_calls=1,
                  timing=dict(process_ns=time.process_time_ns()-cpu,wall_ns=time.perf_counter_ns()-wall))
        self.calls.append(call)
        return receipt,call
