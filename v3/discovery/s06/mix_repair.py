#!/usr/bin/env python3
"""Optional expected-action repair mixtures, independently checked in rationals.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. DEVELOPMENT.
Input witnesses/trees must already be admitted; LP statuses prove no bound.
"""
from __future__ import annotations

from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import sys
import time

import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

HERE = Path(__file__).resolve().parent
S05 = HERE.parent / "s05"
sys.path.insert(0, str(S05))
import maxsat_repair as src
import maxsat_reprice as raw

VERSION = "s06-mix-repair-v1"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def bits(mask, size):
    return tuple((mask >> j) & 1 for j in range(size))


def fraction_json(value):
    if isinstance(value, F):
        return str(value)
    raise TypeError(type(value).__name__)


class CohortState:
    """Same exact joint cost-source semantics as joint_repair.CostState.

    No hidden realized modes or probabilities are read by this state.
    A checksum only binds the already observed synthetic-provider receipt.
    """
    representation = "joint"

    def __init__(self, modes, n, source_id, meter):
        self.modes = tuple(tuple(v) for v in modes)
        self.n, self.m = n, len(self.modes[0])
        if n <= 0 or any(len(v) != self.m or any(type(x) is not int or x < 0 for x in v)
                         for v in self.modes):
            raise ValueError("Malformed public cost source")
        self.possible = [tuple(range(len(self.modes))) for _ in range(n)]
        self.source_id, self.meter = source_id, meter
        self.receipts = []
        meter.pay("cost_admission", "public_mode_and_cohort_words", len(modes)*self.m+n+8)

    def observe(self, receipt):
        if (receipt["source_id"] != self.source_id
                or src.digest({k:v for k,v in receipt.items() if k != "receipt_id"}) != receipt["receipt_id"]):
            raise ValueError("Foreign or changed observation")
        i,j,value = receipt["row"],receipt["coordinate"],receipt["value"]
        if not (type(i) is int and 0 <= i < self.n and type(j) is int and 0 <= j < self.m):
            raise ValueError("Bad observation index")
        choices = tuple(k for k in self.possible[i] if self.modes[k][j] == value)
        self.meter.pay("cost_check", "receipt_binding_and_mode_filter",12+len(self.possible[i]))
        if not choices:
            raise ValueError("Empty source is not a certificate")
        self.possible[i] = choices
        self.receipts.append(receipt["receipt_id"])

    def support(self, coefficient):
        if len(coefficient) != self.m:
            raise ValueError("Cost meaning changed")
        total, point = F(0), [0]*self.m
        for choices in self.possible:
            values = [(sum((c*z for c,z in zip(coefficient,self.modes[k])),F(0)),k)
                      for k in choices]
            value,k = max(values)
            total += value
            point = [a+b for a,b in zip(point,self.modes[k])]
            self.meter.pay("exact_support", "rational_products_additions_and_mode_max",(2*self.m+1)*len(choices)+self.m+1)
        return total,point

    def snapshot(self):
        return dict(source_id=self.source_id,cohort_size=self.n,
                    possible_modes=[list(v) for v in self.possible],
                    audit_receipts=self.receipts)


def exact_certificate(profile, costs, price, simplex, tree_index):
    """Check a rational simplex using the admitted witnesses and one proof."""
    if (len(simplex) != len(profile["witnesses"])+1
            or any(type(p) is not F or p < 0 for p in simplex) or sum(simplex) != 1):
        raise ValueError("Require an exact nonnegative rational simplex")
    price = F(price)
    us = [bits(w["violation_mask"],costs.m) for w in profile["witnesses"]]
    d = tuple(sum((p*u[j] for p,u in zip(simplex,us)),F(0)) for j in range(costs.m))
    k = price*simplex[-1]
    tree = (profile["trees"][tree_index] if tree_index is not None
            else dict(leaf_masks=[0],receipt_id="nonnegative_objective"))
    masks = list(dict.fromkeys(tree["leaf_masks"]))
    if not masks:
        raise ValueError("Unadmitted empty proof")
    terms = []
    value,point = costs.support(d)
    terms.append(dict(role="replacement",coefficient=d,constant=k-price,
                      value=k+value-price,attaining_weights=point))
    for mask in masks:
        v = bits(mask,costs.m)
        c = tuple(x-y for x,y in zip(d,v))
        value,point = costs.support(c)
        terms.append(dict(role="proof_leaf",leaf_mask=mask,coefficient=c,
                          constant=k,value=k+value,attaining_weights=point))
    bound = max([F(0)]+[t["value"] for t in terms])
    costs.meter.pay("mixture_check", "simplex_combination_and_certificate",len(simplex)*(2*costs.m+2)+4*len(terms))
    return dict(bound=bound,simplex=simplex,mean_violation=d,
                replacement_constant=k,tree_index=tree_index,
                proof_id=tree.get("receipt_id",tree.get("source_receipt",f"archive-row-{profile['row']}-tree-{tree_index}")),
                terms=terms,
                actions=[dict(model=w["model"],violation_mask=w["violation_mask"],probability=p)
                         for w,p in zip(profile["witnesses"],simplex)]
                        +[dict(model=None,action="replace",probability=simplex[-1])],
                duty="uniform bound on expected regret over randomized output; not every realized action")


def rational_simplex(values, denominator, meter):
    if type(denominator) is not int or denominator <= 0:
        raise ValueError("Positive integral rounding denominator required")
    if any(not math.isfinite(float(x)) for x in values):
        raise ValueError("Nonfinite LP proposal")
    positive = [max(F(0),F.from_float(float(x))) for x in values]
    total = sum(positive)
    if not total:
        raise ValueError("Zero proposal")
    scaled = [x*denominator/total for x in positive]
    numerators = [x.numerator//x.denominator for x in scaled]
    order = sorted(range(len(values)),key=lambda i:(-(scaled[i]-numerators[i]),i))
    for i in order[:denominator-sum(numerators)]:
        numerators[i] += 1
    meter.pay("rounding", "positive_normalization_largest_remainders",12*len(values))
    return [F(x,denominator) for x in numerators]


def propose(profile, costs, price, tree_index, lp_seconds):
    start,cpu = time.perf_counter_ns(),time.process_time_ns()
    witnesses = profile["witnesses"]
    us = [bits(w["violation_mask"],costs.m) for w in witnesses]
    kpi = len(witnesses)+1
    tree = profile["trees"][tree_index] if tree_index is not None else dict(leaf_masks=[0])
    # First support is against replacement, followed by proof supports.
    masks = [0]+list(dict.fromkeys(tree["leaf_masks"]))
    ns = len(masks)*costs.n
    t_index = kpi+ns
    nvars = t_index+1
    rr,cc,vv,rhs = [],[],[],[]
    def coefficient(row,column,value):
        if value:
            rr.append(row);cc.append(column);vv.append(float(value))
    for ell,mask in enumerate(masks):
        v = bits(mask,costs.m)
        for i,choices in enumerate(costs.possible):
            s_index = kpi+ell*costs.n+i
            for mode in choices:
                z = costs.modes[mode]
                row = len(rhs)
                for a,u in enumerate(us):
                    coefficient(row,a,sum(x*y for x,y in zip(u,z)))
                coefficient(row,s_index,-1)
                rhs.append(sum(x*y for x,y in zip(v,z)))
                costs.meter.pay("lp_compile", "mode_action_products_and_epigraph_coefficients",2*costs.m*(len(us)+1)+len(us)+2)
        row = len(rhs)
        coefficient(row,kpi-1,price)
        for i in range(costs.n):
            coefficient(row,kpi+ell*costs.n+i,1)
        coefficient(row,t_index,-1)
        rhs.append(price if ell == 0 else 0)
    matrix = coo_matrix((vv,(rr,cc)),shape=(len(rhs),nvars)).tocsr()
    objective = np.zeros(nvars)
    objective[t_index] = 1
    equality = np.zeros((1,nvars));equality[0,:kpi] = 1
    bounds = [(0,1)]*kpi+[(None,None)]*ns+[(0,None)]
    costs.meter.pay("lp_compile", "sparse_storage_equality_and_bounds",len(vv)*3+len(rhs)+3*nvars)
    compile_timing = dict(wall_ns=time.perf_counter_ns()-start,process_ns=time.process_time_ns()-cpu)
    start,cpu = time.perf_counter_ns(),time.process_time_ns()
    result = linprog(objective,A_ub=matrix,b_ub=np.array(rhs),
                     A_eq=equality,b_eq=[1],bounds=bounds,method="highs",
                     options={"time_limit":lp_seconds})
    lp_timing = dict(wall_ns=time.perf_counter_ns()-start,process_ns=time.process_time_ns()-cpu)
    record = dict(tree_index=tree_index,status=int(result.status),message=str(result.message),
                  iterations=int(result.nit),objective=None if result.fun is None else float(result.fun),
                  variables=nvars,inequalities=len(rhs),nonzero_coefficients=len(vv),
                  compile_timing=compile_timing,lp_timing=lp_timing,
                  native_operation_units=None,scope="floating LP proposal only; no independently checked LP optimum")
    values = None if result.x is None else list(result.x[:kpi])
    return values,record


def mix_certificate(profile, costs, price, denominator=1_000_000, lp_seconds=2):
    """Return checked best of pure fallbacks and rationalized LP proposals.

    `costs` may be joint_repair.CostState: it must expose modes, possible, n,
    m, meter, and exact support(coefficient). Admitted raw proofs remain the
    caller's prerequisite. Ordinary controllers may call this same function.
    """
    if getattr(costs,"representation","joint") != "joint":
        raise ValueError("This proposer uses joint row modes; supply a matching exact source")
    start,cpu = time.perf_counter_ns(),time.process_time_ns()
    tree_ids = list(range(len(profile["trees"]))) or [None]
    pure=[]
    for ti in tree_ids:
        for i in range(len(profile["witnesses"])+1):
            simplex = [F(int(i==j)) for j in range(len(profile["witnesses"])+1)]
            pure.append(exact_certificate(profile,costs,price,simplex,ti))
    fixed = min(pure,key=lambda p:p["bound"])
    best = fixed
    lp_records=[]
    for ti in tree_ids:
        values,record=propose(profile,costs,price,ti,lp_seconds)
        if values is not None:
            try:
                simplex=rational_simplex(values,denominator,costs.meter)
                cstart,ccpu=time.perf_counter_ns(),time.process_time_ns()
                checked=exact_certificate(profile,costs,price,simplex,ti)
                record["exact_check_timing"] = dict(wall_ns=time.perf_counter_ns()-cstart,process_ns=time.process_time_ns()-ccpu)
                record["rounded_simplex"]=simplex
                record["rounded_checked_bound"]=checked["bound"]
                if checked["bound"] < best["bound"]:
                    best=checked
            except ValueError as error:
                record["proposal_rejected"]=str(error)
        lp_records.append(record)
    costs.meter.pay("mixture_selection", "retain_best_checked_candidate",len(pure)+len(lp_records))
    return dict(bound=best["bound"],answer=best,fixed_answer=fixed,
                strict_bound_improvement=best["bound"]<fixed["bound"],
                lp_records=lp_records,
                timing=dict(wall_ns=time.perf_counter_ns()-start,process_ns=time.process_time_ns()-cpu))


def execute(source_path, trace_path, output_path):
    source_path,trace_path,output_path=(p.resolve() for p in (source_path,trace_path,output_path))
    if output_path.exists():
        raise FileExistsError("Preserve prior developmental results")
    begin,cpu=time.perf_counter_ns(),time.process_time_ns()
    source=json.loads(source_path.read_text())
    trace=json.loads(trace_path.read_text())
    if (src.digest({k:v for k,v in source.items() if k != "source_identity"}) != source["source_identity"]
            or trace["source_identity"] != source["source_identity"] or trace["status"] != "complete"):
        raise ValueError("Cost source or executed trace changed")
    archive_path=S05/"maxsat_repair_results.json"
    archive=json.loads(archive_path.read_text())
    if (sha(archive_path) != source["logical_archive_sha256"]
            or src.digest(archive["instances"]) != archive["source_identity"]
            or sha(src.__file__) != archive["implementation_sha256"]):
        raise ValueError("Logical archive/checker binding failed")
    astart,acpu=time.perf_counter_ns(),time.process_time_ns()
    profiles,admission,proofs=raw.acquire_profiles(archive)
    admission_timing=dict(wall_ns=time.perf_counter_ns()-astart,process_ns=time.process_time_ns()-acpu)
    arm=next(a for a in trace["arms"] if a["policy"]=="certificate_directed")
    receipts=arm["audit_receipts"]
    prefixes=list(dict.fromkeys([0,4,8,len(receipts)]))
    if len(receipts)<8:
        raise ValueError("This declared prefix scope requires at least eight prior audits")
    result=dict(version=VERSION,status="running",evidence="DEVELOPMENT",
                contributor="ChatGPT (GPT-6 Astra Pro)",created_utc=datetime.now(timezone.utc).isoformat(),
                duty="expected regret over randomized output; distinct from fixed-action duty",
                implementation_sha256=sha(__file__),python=sys.version,scipy_version=scipy.__version__,
                input_sha256={str(p.relative_to(HERE.parent.parent.parent)):sha(p) for p in
                              [source_path,trace_path,archive_path,Path(src.__file__),Path(raw.__file__)]},
                observation_scope="Only previously executed audit receipts; no new cost observations; original logical bank only at every prefix.",
                prefixes=prefixes,cohort_size=source["cohort_size"],
                units="Cost, price and regret are cohort sums; divide by cohort_size for means.",
                admission=dict(raw_witness_and_source=admission.record(),raw_tree_check_and_compile=proofs.record(),
                               timing=admission_timing,raw_archive_bytes=archive_path.stat().st_size,
                               read_hash_units=(archive_path.stat().st_size+7)//8+(archive_path.stat().st_size+72)//64),
                historical_acquisition=dict(original_logical_units=next(a["final"]["total_units"] for a in archive["arms"] if a["mode"]=="conventional_requested_value"),
                                            unique_prior_audits=len(receipts),prior_trace_invoice=arm["invoice"]),
                new_logical_provider_calls=0,new_cost_observations=0,
                preflight=dict(raw_profile_inspections=1,operation_totals_not_retained=True,timing_ns=None,
                               note="Preflight printed profile sizes before this measured run; its bill is not included in the saved run total."),
                rounds=[])
    def save():
        output_path.write_text(json.dumps(result,indent=2,default=fraction_json)+"\n")
    save()
    for prefix in prefixes:
        meter=src.Meter()
        state=CohortState(source["possible_cost_modes"],source["cohort_size"],source["source_identity"],meter)
        for receipt in receipts[:prefix]:
            state.observe(receipt)
        records=[]
        for profile,duty in zip(profiles,source["schedule"]):
            if profile["row"] != duty["row"]:
                raise ValueError("Row schedule mismatch")
            before=meter.total
            answer=mix_certificate(profile,state,duty["price"])
            answer.update(row=profile["row"],price=duty["price"],tolerance=duty["tolerance"],
                          logical_source_id=profile["source_identity"],
                          checked_expected_action=answer["bound"]<=duty["tolerance"],
                          checked_fixed_action=answer["fixed_answer"]["bound"]<=duty["tolerance"],
                          software_units=meter.total-before)
            records.append(answer)
        summary=dict(audit_prefix=prefix,rows=len(records),
                     fixed_closures=sum(r["checked_fixed_action"] for r in records),
                     expected_closures=sum(r["checked_expected_action"] for r in records),
                     strict_bound_improvements=sum(r["strict_bound_improvement"] for r in records),
                     summed_fixed_bound=sum((r["fixed_answer"]["bound"] for r in records),F(0)),
                     summed_expected_bound=sum((r["bound"] for r in records),F(0)),
                     lp_calls=sum(len(r["lp_records"]) for r in records))
        result["rounds"].append(dict(summary=summary,cost_state=state.snapshot(),software_invoice=meter.record(),rows=records))
        save()
        print(json.dumps(summary,default=fraction_json),flush=True)
    result["status"]="complete"
    result["timing"]=dict(wall_ns=time.perf_counter_ns()-begin,process_ns=time.process_time_ns()-cpu)
    result["checks"]=dict(all_exact_simplexes=True,all_supports_recomputed=True,
                          pure_fallback_retained=True,no_optimality_claim_from_lp=True)
    save()


if __name__ == "__main__":
    source,trace,output=map(Path,sys.argv[1:])
    execute(source,trace,output)
