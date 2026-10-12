#!/usr/bin/env python3
"""Reconstruct executed joint-v2 action certificates from their raw evidence.

ChatGPT (GPT-6 Astra Pro), DEVELOPMENT, 2026-10-12.
No native search object is created, and no provider/audit acquisition is called.
Auxiliary-agent time is not added to the principal research clock.
"""
from __future__ import annotations

import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time

import native_repair as native
import native_stream

kernel,raw=native.kernel,native.profile_kernel
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent.parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(condition,message):
    if not condition:
        raise ValueError(message)


def bits(mask,m):
    require(type(mask) is int and 0 <= mask < 1 << m,"Invalid violation mask")
    return tuple((mask >> j)&1 for j in range(m))


class Observations:
    """Independent direct row-state and support replay, without lookup caches."""
    def __init__(self,source,meter):
        self.source=source
        self.modes=source["possible_cost_modes"]
        self.n=source["cohort_size"]
        self.m=len(self.modes[0])
        require(type(self.n) is int and self.n>0,"Invalid cohort size")
        require(all(len(v)==self.m and all(type(x) is int and x>=0 for x in v)
                    for v in self.modes),"Invalid nonnegative cost modes")
        hidden=source["hidden_modes"]
        require(len(hidden)==self.n and all(type(k) is int and 0<=k<len(self.modes) for k in hidden),"Bad committed cohort")
        self.possible=[list(range(len(self.modes))) for _ in range(self.n)]
        self.receipts=[]
        self.meter=meter
        meter.pay("cost_readmission","declared_modes_and_cohort",len(self.modes)*self.m+2*self.n+8)

    def observe(self,receipt):
        require(receipt["source_id"]==self.source["source_identity"],"Foreign audit source")
        require(kernel.digest({k:v for k,v in receipt.items() if k!="receipt_id"})==receipt["receipt_id"],"Changed audit bytes")
        i,j,value=receipt["row"],receipt["coordinate"],receipt["value"]
        require(type(i) is int and 0<=i<self.n and type(j) is int and 0<=j<self.m,"Bad audit index")
        require(receipt["provider_call"]==len(self.receipts),"Audit call order changed")
        # This is an evidence checker, not an acquisition controller. Compare
        # only this already disclosed coordinate with the committed source.
        expected=self.modes[self.source["hidden_modes"][i]][j]
        require(value==expected,"Audit disagrees with the actual committed source")
        candidates=[k for k in self.possible[i] if self.modes[k][j]==value]
        require(bool(candidates),"Empty cost evidence state")
        self.meter.pay("cost_readmission","receipt_binding_committed_value_and_filter",16+len(self.possible[i]))
        self.possible[i]=candidates
        self.receipts.append(receipt)

    def support(self,c):
        require(len(c)==self.m,"Changed feature meanings")
        total=0
        point=[0]*self.m
        for choices in self.possible:
            values=[]
            for mode in choices:
                value=sum(a*b for a,b in zip(c,self.modes[mode]))
                values.append((value,mode))
                self.meter.pay("certificate_reconstruction","direct_mode_dot",2*self.m)
            value,mode=max(values)
            total+=value
            point=[a+b for a,b in zip(point,self.modes[mode])]
            self.meter.pay("certificate_reconstruction","row_maximum_and_sum",len(values)+self.m+1)
        return total,point

    def snapshot(self):
        return dict(source_id=self.source["source_identity"],representation="joint",
                    cohort_size=self.n,possible_modes=self.possible,
                    audit_receipts=[r["receipt_id"] for r in self.receipts])


def certificate(profile,costs,price):
    """Fresh signed-support computation for every retained action/proof pair."""
    trees=profile["trees"] or [dict(leaf_masks=[0],receipt_id="nonnegative_objective")]
    actions=[(w["model"],w["violation_mask"]) for w in profile["witnesses"]]+[(None,None)]
    records=[]
    for model,mask in actions:
        u=bits(mask,costs.m) if mask is not None else (0,)*costs.m
        for ti,tree in enumerate(trees):
            require(bool(tree["leaf_masks"]),"Unadmitted empty tree profile")
            constraints=[]
            if mask is not None:
                value,point=costs.support(u)
                constraints.append((value-price,u,-price,point,"replacement"))
            for leaf in tree["leaf_masks"]:
                v=bits(leaf,costs.m)
                c=tuple(x-y for x,y in zip(u,v))
                value,point=costs.support(c)
                constant=price if mask is None else 0
                constraints.append((value+constant,c,constant,point,"proof_leaf"))
            worst=max(constraints,key=lambda x:x[0])
            records.append(dict(bound=max(0,worst[0]),model=model,mask=mask,
                                action="replace" if mask is None else "repair",
                                tree_index=ti if profile["trees"] else None,
                                proof_id=tree["receipt_id"],critical_coefficient=list(worst[1]),
                                critical_constant=worst[2],critical_weights=worst[3],critical_role=worst[4]))
            costs.meter.pay("certificate_reconstruction","pair_constraints_and_minimum",len(constraints)+12)
    require(bool(records),"No admitted action")
    return min(records,key=lambda r:(r["bound"],r["model"] is None,-1 if r["model"] is None else r["model"]))


def check_purchase(instance,event,meter,event_id,profile):
    response=event["response"]
    proposal=event["proposal"]
    require(event["row"]==instance["row"],"Logical purchase row changed")
    require(response["weights"]==proposal["weights"] and response["requested_budget"]==proposal["budget"],"Logical query changed")
    require(response["exact_requested"] is False,"This joint run used bounded requests")
    wi=native.weighted_instance(instance,response["weights"])
    require(response["source_identity"]==wi["identity"],"Weighted source identity changed")
    require(response["structural_source_id"]==native.structural_id(instance),"Logical structure changed")
    require(response["weight_id"]==kernel.digest(response["weights"]),"Weight identity changed")
    meter.pay("new_receipt_readmission","source_objective_and_budget_binding",len(response["weights"])+12)
    witness_count=proof_count=0
    w=response.get("witness")
    if w is not None:
        checked=raw.compile_witness(wi,w["model"],meter)
        require(checked==w,"Witness fields differ from original-clause check")
        require(response["model"]==w["model"],"Returned model/witness disagreement")
        if response["status"]=="SAT":
            require(w["original_cost"]<=response["requested_budget"],"SAT receipt exceeds query budget")
        witness_count=1
        if not any(old["model"]==w["model"] for old in profile["witnesses"]):
            rid=kernel.digest(dict(source=instance["identity"],model=w["model"],violation_mask=w["violation_mask"]))
            profile["witnesses"].append(dict(model=w["model"],violation_mask=w["violation_mask"],
                                             receipt_id=rid,dependency=dict(purchase=event_id)))
            meter.pay("checked_retention","new_witness",instance["variables"]+8)
    lower=response.get("checked_lower_receipt")
    if lower is not None:
        require(lower["kind"]=="separate_bounded_proof_provider" and lower["status"]=="UNSAT", "Wrong negative receipt kind")
        require(lower["source_identity"]==wi["identity"] and lower["structural_source_id"]==native.structural_id(instance),"Foreign lower proof")
        require(lower["weights"]==response["weights"] and lower["budget"]==response["requested_budget"],"Lower objective/budget changed")
        require(lower in response["events"],"Missing raw proof event")
        require(lower["proof"]==response["proof"],"Raw negative bytes disagree")
        # Neither native statuses nor checked=True enters the proof bank.
        kernel.check_negative(wi,lower["budget"],lower["proof"],meter)
        leaves=raw.compile_tree(lower["proof"],meter)
        require(leaves==lower["leaf_masks"],"Compiled lower supports changed")
        rid=kernel.digest(dict(source=wi["identity"],budget=lower["budget"],proof=lower["proof"]))
        require(rid==lower["receipt_id"],"Raw proof identity changed")
        require(response["checked_lower"]==lower["budget"]+1,"Scalar lower summary changed")
        profile["trees"].append(dict(leaf_masks=leaves,receipt_id=rid,original_budget=lower["budget"],
                                     dependency=dict(purchase=event_id)))
        meter.pay("checked_retention","new_lower_proof",len(leaves)+10)
        proof_count=1
    require(response["status"]!="UNSAT" or lower is not None,"UNSAT outcome lacks admitted lower proof")
    require(response["status"]!="SAT" or w is not None,"SAT outcome lacks feasible witness")
    return witness_count,proof_count


def check_arm(source,instances,initial,arm):
    wall,cpu=time.perf_counter_ns(),time.process_time_ns()
    meter=kernel.Meter()
    costs=Observations(source,meter)
    profiles=copy.deepcopy(initial)
    cursor=0
    witnesses=proofs=logical=0
    rows=[]
    require(len(arm["requests"])==len(source["schedule"]),"Incomplete request stream")
    for index,(request,duty) in enumerate(zip(arm["requests"],source["schedule"])):
        row,price,tau=duty["row"],duty["price"],duty["tolerance"]
        require(request["request"]==index and request["row"]==row,"Request order changed")
        require(request["price"]==price and request["tolerance"]==tau,"Requested duty changed")
        require(request["logical_source_id"]==instances[row]["identity"] and request["cost_source_id"]==costs.source["source_identity"],"Request source changed")
        chosen=certificate(profiles[row],costs,price)
        require(chosen==request["before"],f"Initial certificate mismatch at {arm['policy']}/{index}")
        hit=chosen["bound"]<=tau
        require(hit==request["closed_from_cache"],"Cache gate changed")
        for event_id in request["event_indices"]:
            require(event_id==cursor,"Event reuse, omission, or reordering")
            event=arm["events"][event_id]
            require(event["request"]==index and event["certificate_before"]==chosen,"Event source certificate changed")
            if event["kind"]=="cost_audit":
                receipt=event["receipt"]
                require(event["proposal"]["row"]==receipt["row"] and event["proposal"]["coordinate"]==receipt["coordinate"],"Audit proposal/receipt mismatch")
                costs.observe(receipt)
            elif event["kind"]=="logical_purchase":
                wc,pc=check_purchase(instances[row],event,meter,event_id,profiles[row])
                witnesses+=wc;proofs+=pc;logical+=1
            else:
                raise ValueError("Unknown acquisition event")
            chosen=certificate(profiles[row],costs,price)
            require(chosen==event["certificate_after"],f"Post-purchase certificate mismatch at {arm['policy']}/{event_id}")
            require(costs.snapshot()==event["cost_state_after"],"Post-purchase observation state changed")
            cursor+=1
        require(chosen==request["answer"],"Final action certificate changed")
        require(costs.snapshot()==request["cost_state"],"Final request cost state changed")
        status="checked_action" if chosen["bound"]<=tau else "unresolved"
        require(request["status"]==status,"Final regret gate changed")
        rows.append(dict(request=index,row=row,status=status,bound=chosen["bound"],tolerance=tau,
                         action=chosen["action"],model=chosen["model"],proof_id=chosen["proof_id"],closed_from_cache=hit))
        meter.pay("output_reconstruction","request_source_gate_and_response",24)
    require(cursor==len(arm["events"]),"Unreferenced paid event")
    require(costs.receipts==arm["audit_receipts"],"Audit event/list disagreement")
    require(costs.snapshot()==arm["final_cost_state"],"Final cost source state changed")
    require(profiles==arm["final_profiles"],"Retained evidence differs from checked replay")
    summary=dict(requests=len(rows),checked=sum(r["status"]=="checked_action" for r in rows),
                 cache_hits=sum(r["closed_from_cache"] for r in rows),cost_observations=len(costs.receipts),
                 logical_purchases=logical,unresolved=sum(r["status"]=="unresolved" for r in rows))
    require(summary==arm["summary"],"Final summary disagreement")
    return dict(policy=arm["policy"],summary=summary,new_witness_receipts_readmitted=witnesses,
                new_branching_receipts_readmitted=proofs,final_gates=rows,
                invoice=meter.record(),timing=dict(wall_ns=time.perf_counter_ns()-wall,process_ns=time.process_time_ns()-cpu))


def main():
    output=HERE/"joint_check_results.json"
    if output.exists():
        raise FileExistsError("Preserve existing reconstruction")
    wall,cpu=time.perf_counter_ns(),time.process_time_ns()
    readmeter=kernel.Meter()
    paths=[HERE/name for name in ("joint_v2_results.json","joint_source.json","joint_repair_v2.py",
                                  "joint_repair.py","native_repair.py","native_stream.py","joint_check.py")]
    blobs={p.name:p.read_bytes() for p in paths}
    for name,blob in blobs.items():
        readmeter.pay("input_read_hash","eight_byte_words",(len(blob)+7)//8)
        readmeter.pay("input_read_hash","sha256_blocks",(len(blob)+72)//64)
    hashes={name:hashlib.sha256(blob).hexdigest() for name,blob in blobs.items()}
    source=json.loads(blobs["joint_source.json"])
    result=json.loads(blobs["joint_v2_results.json"])
    require(result["status"]=="complete","Executed result is incomplete")
    require(result["source_sha256"]==hashes["joint_source.json"],"Committed source bytes changed")
    require(result["source_identity"]==source["source_identity"]==kernel.digest({k:v for k,v in source.items() if k!="source_identity"}),"Cost source identity changed")
    require(result["implementation_sha256"]==hashes["joint_repair_v2.py"],"Execution implementation differs")
    require(all(hashes[name]==value for name,value in result["dependencies"].items()),"Execution dependency differs")
    archive,initial,admission=native_stream.admit_existing_cache()
    require(admission["hashes"]==result["initial_admission"]["hashes"],"Initial admitted evidence differs")
    require(admission["hashes"]["maxsat_repair_results.json"]==source["logical_archive_sha256"],"Cost/logical source binding changed")
    require([a["policy"] for a in result["arms"]]==["shared_deficit","audit_first","logic_first","certificate_directed"],"Four-arm execution order changed")
    checked=dict(status="running",evidence="DEVELOPMENT same-model focused reconstruction",
                 contributor="ChatGPT (GPT-6 Astra Pro)",created_utc=datetime.now(timezone.utc).isoformat(),
                 implementation_sha256=hashes["joint_check.py"],input_hashes=hashes,
                 input_bytes={name:len(blob) for name,blob in blobs.items()},
                 initial_raw_and_compact_readmission=admission,input_read_hash_invoice=readmeter.record(),
                 new_native_calls=0,new_provider_calls=0,new_cost_observations=0,agent_clock_credit=0,
                 scope="Recheck admitted compact projection, observed source values, new witnesses and raw branching proofs; independently reconstruct all request/event certificates and final gates.",
                 exclusions="No portfolio-quote or policy-optimality audit; no independent calibration of runtime prices; no new diagnostic optimum or validation population.",arms=[])
    def save():
        output.write_text(json.dumps(checked,indent=2)+"\n")
    save()
    try:
        for arm in result["arms"]:
            verified=check_arm(source,archive["instances"],initial,arm)
            checked["arms"].append(verified)
            save()
            print(json.dumps(dict(policy=verified["policy"],**verified["summary"])),flush=True)
        checked["status"]="passed"
    except Exception as exc:
        checked["status"]="failed"
        checked["failure"]=dict(type=type(exc).__name__,message=str(exc))
        raise
    finally:
        checked["timing"]=dict(wall_ns=time.perf_counter_ns()-wall,process_ns=time.process_time_ns()-cpu)
        checked["total_declared_units"]=readmeter.total+admission["total_declared_units"]+sum(a["invoice"]["total"] for a in checked["arms"])
        checked["accounting"]="Read/hash, raw proof and witness readmission, direct exact support and retention tariffs are explicit. Python/JSON execution is timed; serialization/allocation/storage bytes are not a full economic price. Historical acquisition is not rebilled as new calls. No helper time is credited."
        save()


if __name__=="__main__":
    main()
