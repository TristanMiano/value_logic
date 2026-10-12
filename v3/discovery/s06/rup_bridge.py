#!/usr/bin/env python3
"""Source-bound weighted SAT export, strict RUP checking, and checked cuts.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12. This separate bounded
provider does not replace or modify the persistent native IHS adapter. RUP
checking here is a small executable checker, not a formally verified kernel.
"""
from __future__ import annotations

import copy
from datetime import datetime, timezone
import importlib.metadata
from pathlib import Path
import sys
import time

import pysat.solvers
from pysat.solvers import Glucose3
import pysolvers

from native_repair import kernel, structural_id, weighted_instance, sha

VERSION = 's06-weighted-rup-v1'
LIMITS = dict(encoding_units=1_000_000, checking_units=5_000_000,
              native_conflicts=100_000, native_propagations=10_000_000,
              max_proof_bytes=2_000_000, projection_units=1_000_000,
              max_projected_features=16)


def neg(lit):
    return not lit if type(lit) is bool else -lit


def emit(cnf, literals, meter):
    """Simplify constants, duplicate literals and tautologies exactly."""
    meter.pay('encoding','clause_input_literals',len(literals)+1)
    if any(type(l) is bool and l for l in literals):
        return
    result = []
    seen = set()
    for lit in literals:
        if type(lit) is bool:
            continue
        if -lit in seen:
            return
        if lit not in seen:
            result.append(lit)
            seen.add(lit)
    cnf.append(result)
    meter.pay('encoding','clause_output_words',len(result)+1)


def encode(instance, weights, budget, meter):
    """Encode the exact original soft violation cost <= integer budget.

    Each z_j is equivalent to all literals of soft clause j being false.
    A recursive threshold node T(i,b) means sum_{j>=i} w_j*z_j <= b.
    T(i,b) = ite(z_i,T(i+1,b-w_i),T(i+1,b)). The four equivalence
    clauses below encode this identity; terminal states use exact constants.
    """
    if type(budget) is not int:
        raise ValueError('Integral budget required')
    if instance.get('identity')!=kernel.digest({k:v for k,v in instance.items() if k!='identity'}):
        raise ValueError('Source identity mismatch')
    n = instance['variables']
    if type(n) is not int or n<1:
        raise ValueError('Positive variable count required')
    clauses = instance['hard']+[s['clause'] for s in instance['soft']]
    if any(not isinstance(c,list) or any(type(l) is not int or not 1<=abs(l)<=n for l in c) for c in clauses):
        raise ValueError('Malformed source clause')
    wi = weighted_instance(instance,weights)
    m = len(weights)
    meter.pay('encoding_admission','source_and_objective_words',8+n+2*m+sum(len(c)+1 for c in clauses))
    cnf = []
    for clause in instance['hard']:
        emit(cnf,clause,meter)
    z = list(range(n+1,n+m+1))
    for indicator,soft in zip(z,instance['soft']):
        clause = soft['clause']
        emit(cnf,[indicator]+clause,meter)
        for lit in clause:
            emit(cnf,[-indicator,-lit],meter)
    suffix = [0]*(m+1)
    for i in range(m-1,-1,-1):
        suffix[i] = suffix[i+1]+weights[i]
        meter.pay('encoding','suffix_weight_sum',2)
    nodes,cache = [],{}
    next_variable = n+m+1
    def threshold(i,b):
        nonlocal next_variable
        meter.pay('encoding','threshold_state_dispatch',4)
        if b<0:
            return False
        if b>=suffix[i]:
            return True
        key=(i,b)
        if key in cache:
            return cache[key]
        # This state cannot be a terminal i=m: 0<=b<suffix[m]=0.
        lo = threshold(i+1,b)
        hi = threshold(i+1,b-weights[i])
        v = next_variable
        next_variable += 1
        nodes.append(dict(variable=v,index=i,budget=b,when_zero=lo,when_one=hi))
        cache[key]=v
        emit(cnf,[-v,z[i],lo],meter)
        emit(cnf,[-v,-z[i],hi],meter)
        emit(cnf,[v,z[i],neg(lo)],meter)
        emit(cnf,[v,-z[i],neg(hi)],meter)
        meter.pay('encoding','node_manifest_storage',6)
        return v
    root = threshold(0,budget)
    emit(cnf,[root],meter)
    return dict(version='explicit-soft-bdd-cnf-v1',structural_source_id=structural_id(instance),
                original_source_id=instance['identity'],weighted_source_id=wi['identity'],
                source_variables=n,violation_variables=z,weights=list(weights),budget=budget,
                root=root,nodes=nodes,max_variable=next_variable-1,clauses=cnf)


def unit_conflict(clauses, assumptions, meter):
    """Independent forward propagation; native solver is never called here."""
    assigned = {}
    for lit in assumptions:
        variable,value = abs(lit),lit>0
        meter.pay('rup_check','assumption_assignment',2)
        if variable in assigned and assigned[variable]!=value:
            return True
        assigned[variable]=value
    while True:
        changed=False
        for clause in clauses:
            meter.pay('rup_check','clause_visit')
            open_literals=[]
            satisfied=False
            for lit in clause:
                meter.pay('rup_check','literal_inspection')
                value=assigned.get(abs(lit))
                if value is None:
                    open_literals.append(lit)
                elif value==(lit>0):
                    satisfied=True
                    break
            if satisfied:
                continue
            if not open_literals:
                return True
            if len(open_literals)==1:
                lit=open_literals[0]
                assigned[abs(lit)]=lit>0
                changed=True
                meter.pay('rup_check','unit_assignment',2)
        if not changed:
            return False


def check_rup(clauses, proof, max_variable, meter):
    """Admit only RUP additions and a checked empty clause.

    Deletions are parsed/charged but ignored. Every retained addition is an
    implicate of the original CNF, so retaining it preserves soundness. This
    is intentionally not a general RAT checker: unsupported additions fail.
    """
    current=[]
    for clause in clauses:
        if any(type(l) is not int or not 1<=abs(l)<=max_variable for l in clause):
            raise ValueError('Malformed admitted CNF')
        if len(set(clause))!=len(clause) or any(-l in clause for l in clause):
            raise ValueError('Normalize source CNF before RUP admission')
        current.append(list(clause))
        meter.pay('rup_admission','source_clause_words',len(clause)+1)
    additions=deletions=0
    for line_number,line in enumerate(proof):
        if not isinstance(line,str):
            raise ValueError('ASCII proof line required')
        fields=line.split()
        meter.pay('rup_parse','proof_bytes_and_words',len(line)+len(fields))
        if not fields or fields[0]=='c':
            continue
        delete=fields[0]=='d'
        if delete:
            fields=fields[1:]
        try:
            literals=[int(x) for x in fields]
        except (ValueError, RecursionError) as exc:
            raise ValueError('Noninteger proof token') from exc
        if not literals or literals[-1]!=0 or any(l==0 for l in literals[:-1]):
            raise ValueError('Each ASCII proof line must contain one terminated clause')
        clause=literals[:-1]
        if any(not 1<=abs(l)<=max_variable for l in clause):
            raise ValueError('Proof variable outside admitted CNF universe')
        if len(set(clause))!=len(clause) or any(-l in clause for l in clause):
            raise ValueError('Unsupported duplicate or tautological proof clause')
        if delete:
            deletions+=1
            continue
        if not unit_conflict(current,[-l for l in clause],meter):
            raise ValueError(f'Addition {line_number} is not RUP; no lower receipt admitted')
        additions+=1
        current.append(clause)
        meter.pay('rup_check','admitted_clause_storage',len(clause)+1)
        if not clause:
            return dict(checked=True,kind='strict_rup',additions=additions,
                        ignored_deletions=deletions,empty_clause_line=line_number,
                        proof_lines=len(proof),checker_sha256=sha(__file__))
    raise ValueError('No checked empty clause')


def check_export(instance, receipt, meter):
    """New consumers establish translation and raw proof admission anew."""
    if receipt['structural_source_id']!=structural_id(instance) or receipt['original_source_id']!=instance['identity']:
        raise ValueError('Foreign source-bound proof')
    translated=encode(instance,receipt['weights'],receipt['budget'],meter)
    if translated!=receipt['encoding']:
        raise ValueError('Unbound or changed weighted-budget translation')
    # No checksum substitutes for the following raw clause proof check.
    checked=check_rup(translated['clauses'],receipt['raw_proof'],translated['max_variable'],meter)
    lower=dict(checked=True,kind='weighted_bound_rup_cut',structural_source_id=structural_id(instance),
               original_source_id=instance['identity'],weights=list(receipt['weights']),budget=receipt['budget'],
               checked_lower=receipt['budget']+1,encoding_sha256=kernel.digest(translated),
               raw_proof_sha256=kernel.digest(receipt['raw_proof']),checker=checked,
               dependency='This purchase raw encoding and exported proof')
    lower['receipt_id']=kernel.digest(lower)
    return lower


def compile_cut_supports(instance, checked_receipts, meter, max_features=16):
    """Paid Boolean objective relaxation, not enumeration of logical models.

    Every feasible source violation mask satisfies each independently checked
    cut q.z>=b+1. Minimize w.z over the relaxed mask set to obtain a reusable
    lower function. Componentwise dominated masks are removable for w>=0.
    """
    m=len(instance['soft'])
    if m>max_features:
        raise ValueError('Objective projection feature cap')
    for r in checked_receipts:
        if r.get('checked') is not True or r['structural_source_id']!=structural_id(instance):
            raise ValueError('Admitted same-source cuts required')
        if len(r['weights'])!=m:
            raise ValueError('Cut objective meanings changed')
    candidates=[]
    for mask in range(1<<m):
        accepted=True
        for r in checked_receipts:
            value=sum(w for j,w in enumerate(r['weights']) if mask&(1<<j))
            meter.pay('cut_projection','objective_mask_and_cut',m+2)
            if value<r['budget']+1:
                accepted=False
                break
        meter.pay('cut_projection','mask_visit')
        if accepted:
            candidates.append(mask)
    # Ascending population count makes every possible dominator available.
    minimal=[]
    for mask in sorted(candidates,key=lambda z:(z.bit_count(),z)):
        dominated=False
        for other in minimal:
            meter.pay('cut_projection','nonnegative_dominance_comparison',2)
            if other&mask==other:
                dominated=True
                break
        if not dominated:
            minimal.append(mask)
            meter.pay('cut_projection','support_storage')
    if not minimal:
        raise ValueError('Cuts exclude all objective masks; source infeasible or admission inconsistent. No ordinary repair lower function.')
    dependencies=[r['receipt_id'] for r in checked_receipts]
    result=dict(leaf_masks=minimal,structural_source_id=structural_id(instance),
                dependencies=dependencies,kind='checked_cut_objective_relaxation',
                objective_masks_examined=1<<m,compatible_masks=len(candidates),
                domain='Any nonnegative weights on the same ordered soft clauses')
    result['receipt_id']=kernel.digest(result)
    return result


def purchase(instance,weights,budget,limits=None):
    """One actual fresh Glucose call, full CNF proof export, independent check."""
    if set(limits or {})-set(LIMITS):
        raise ValueError('Unknown resource cap')
    limits=LIMITS|dict(limits or {})
    if any(type(v) is not int or v<0 for v in limits.values()):
        raise ValueError('Nonnegative integral resource caps required')
    if limits['native_conflicts']==0 or limits['native_propagations']==0:
        raise ValueError('Positive native budgets required; zero can mean unlimited to a backend')
    wall,cpu=time.perf_counter_ns(),time.process_time_ns()
    encoding_meter=kernel.Meter(limits['encoding_units'])
    checking_meter=kernel.Meter(limits['checking_units'])
    record=dict(version=VERSION,status='UNRESOLVED',contributor='ChatGPT (GPT-6 Astra Pro)',
                start_utc=datetime.now(timezone.utc).isoformat(),structural_source_id=structural_id(instance),
                original_source_id=instance['identity'],weights=list(weights),budget=budget,limits=limits,
                native_calls=0,native_status=None,raw_proof=None,checked_lower_receipt=None,witness=None,
                implementation_sha256=sha(__file__),dependencies=dict(python_sat=importlib.metadata.version('python-sat'),
                    wrapper_sha256=sha(pysat.solvers.__file__),native_sha256=sha(pysolvers.__file__)))
    try:
        encoding=encode(instance,weights,budget,encoding_meter)
        record['encoding']=encoding
        # Trace before adding any source clauses. No assumption-relative proof.
        nwall,ncpu=time.perf_counter_ns(),time.process_time_ns()
        with Glucose3(with_proof=True,use_timer=True) as solver:
            solver.append_formula(encoding['clauses'])
            solver.conf_budget(limits['native_conflicts'])
            solver.prop_budget(limits['native_propagations'])
            result=solver.solve_limited()
            record['native_calls']=1
            record['native_status']=result
            record['native_stats']=solver.accum_stats()
            model=solver.get_model() if result is True else None
            proof=solver.get_proof() if result is False else None
        record['native_timing']=dict(wall_ns=time.perf_counter_ns()-nwall,process_ns=time.process_time_ns()-ncpu)
        if result is None:
            record['reason']='native_cap_or_interruption'
        elif result is True:
            signs=set(model or [])
            original_model=sum(1<<j for j in range(instance['variables']) if j+1 in signs)
            wi=weighted_instance(instance,weights)
            value=kernel.checked_objective(wi,original_model,checking_meter)
            if value>budget:
                raise ValueError('Native witness violates the actual weighted bound')
            from native_repair import profile_kernel
            witness=profile_kernel.compile_witness(wi,original_model,checking_meter)
            record['witness']=witness
            record['status']='SAT'
        else:
            record['raw_proof']=proof
            if proof is None:
                raise ValueError('No supported proof export')
            size=sum(len(s.encode())+1 for s in proof)
            record['raw_proof_bytes']=size
            if size>limits['max_proof_bytes']:
                raise ValueError('Export exceeds admission byte cap')
            lower=check_export(instance,record,checking_meter)
            record['checked_lower_receipt']=lower
            record['status']='UNSAT'
    except kernel.CapReached:
        record['reason']='encoding_or_checking_operation_cap'
    except (ValueError, RecursionError) as exc:
        record['reason']=str(exc)
    record['invoice']=dict(encoding=encoding_meter.record(),checking=checking_meter.record(),
                           declared_units_excluding_native_search=encoding_meter.total+checking_meter.total,
                           native_search_units=None)
    record['timing']=dict(wall_ns=time.perf_counter_ns()-wall,process_ns=time.process_time_ns()-cpu)
    record['end_utc']=datetime.now(timezone.utc).isoformat()
    record['accounting']='Includes named encoding, re-encoding admission and proof/witness-check work; native creation/solve/export and all Python execution measured. Serialization, allocator and host memory are not separately tariffed; no total economic or hard wall-time guarantee.'
    return record
