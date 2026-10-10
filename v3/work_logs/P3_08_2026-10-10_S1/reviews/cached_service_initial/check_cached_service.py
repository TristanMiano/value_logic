"""Independent focused executable checks against a copied source closure.

P3-08 DEVELOPMENT, same-model nonblind, zero principal research credit.
No private evaluator input; expected trivial fixture labels are public.
One explicitly disclosed child-failure fixture changes only this subprocess's
copied adapter module binding; the root-owned source files are never edited.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
from types import SimpleNamespace
import json
import sys
import traceback

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "source_snapshot"
sys.path.insert(0,str(SOURCE/"v3/experiments"))
import p308_cached_service as K
import p308_cnf as S
import p308_hashcache as H
import p308_broker as B
import p308_reporting as P
from p308_common import C

cases = []


def run_case(name, fn):
    started = datetime.now(timezone.utc).isoformat()
    try:
        result = fn()
        cases.append({"name":name,"pass":True,"started_utc":started,"result":result})
    except Exception:
        cases.append({"name":name,"pass":False,"started_utc":started,"exception":traceback.format_exc()})


def operations(resource):
    return Counter({(a,b):n for a,b,n in resource.operations})


def check_receipt(receipt, query, success=True):
    assert type(receipt) is S.Receipt
    assert receipt.query_id == query.query_id and receipt.claim_key == query.claim_key
    assert receipt.provider == K.PROVIDER and receipt.provider_version == K.VERSION
    assert receipt.resources.total == sum(n for _,n in receipt.resources.by_category)
    assert receipt.resources.total == sum(n for _,_,n in receipt.resources.operations)
    assert receipt.successful == success
    if success:
        assert receipt.checked is True and type(receipt.answer) is int and receipt.answer in (0,1)
    else:
        assert receipt.checked is False and receipt.answer is None and receipt.witness is None


def purchase(service, query, solver="dpll", limit=None):
    cap = service.service_cap(query,solver)
    receipt = service.checked_purchase(query,limit_total=cap if limit is None else limit,solver=solver)
    check_receipt(receipt,query)
    assert receipt.resources.total <= cap
    return receipt


def trivial(name, answer, version=S.SOURCE_VERSION):
    return S.make_query(name,4,[] if answer else [[],[1]],source_version=version)


def source_binding():
    manifest = json.loads((HERE/"plan.json").read_text())["sources"]
    for row in manifest:
        assert sha256((SOURCE/row["path"]).read_bytes()).hexdigest() == row["sha256"]
    assert K.CachedService.Query is S.Query and K.CachedService.Receipt is S.Receipt
    assert K.CachedService.expert_predictions is S.expert_predictions
    assert K.CachedService.cost_proxy is S.cost_proxy
    return {"source_count":len(manifest),"adapter_sha256":sha256((SOURCE/"v3/experiments/p308_cached_service.py").read_bytes()).hexdigest()}


def new_id_and_accounting():
    result = []
    for kind in ("linear","hashed"):
        service = K.CachedService(cache_kind=kind)
        q1,q2 = trivial("new-id-first",0),trivial("new-id-second",0)
        first,second = purchase(service,q1),purchase(service,q2)
        check_receipt(first,q1);check_receipt(second,q2)
        assert first.answer == second.answer == 0
        audit = service.audit_record()
        assert (audit["logical_selected_calls"],audit["physical_cold_calls"],audit["checked_cache_hits"]) == (2,1,1)
        cold = audit["requests"][0]["cold_receipt"]
        expected = Counter({(x["category"],x["operation"]):x["units"] for x in cold["resources"]["operations"]})
        prefix = "selected_cache_cold_provider:"
        absorbed = Counter({(a,b[len(prefix):]):n for a,b,n in first.resources.operations if b.startswith(prefix)})
        assert expected == absorbed
        assert not any(b.startswith(prefix) for _,b,_ in second.resources.operations)
        # Reconstruct the exact standalone hit delta in an independently
        # initialized copy of the same existing cache implementation.
        direct = (S.ExactCache if kind == "linear" else H.ExactHashCache)(64)
        setup = C.CostMeter()
        original = S.checked_purchase(q1,limit_total=S.service_cap(q1,"dpll"),solver="dpll")
        direct.remember(q1,original,setup)
        meter = C.CostMeter()
        hit = direct.lookup(q2,meter)
        assert hit is not None and hit.resources.total == meter.total
        # Adapter's paid front/back work is 192+3Q on a hit. Its cache
        # receipt delta already debits the same meter; adding it again fails.
        expected_hit_total = hit.resources.total + 192 + 3*q2.key_words
        assert second.resources.total == expected_hit_total
        result.append({"kind":kind,"first":first.record(),"second":second.record(),
                       "direct_cache_hit_units":hit.resources.total,"expected_adapter_hit_units":expected_hit_total,
                       "audit_counts":{k:audit[k] for k in ["logical_selected_calls","physical_cold_calls","checked_cache_hits"]}})
    return result


def source_version_and_eviction():
    result = []
    for kind in ("linear","hashed"):
        service = K.CachedService(cache_kind=kind,capacity=2)
        a,b = trivial("epoch-a",1,"source-a"),trivial("epoch-b",1,"source-b")
        aa = trivial("epoch-a-again",1,"source-a")
        cc = trivial("epoch-c",0,"source-c")
        bb = trivial("epoch-b-again",1,"source-b")
        aaa = trivial("epoch-a-third",1,"source-a")
        rr = [purchase(service,q) for q in (a,b,aa,cc,bb,aaa)]
        assert [x.answer for x in rr] == [1,1,1,0,1,1]
        audit = service.audit_record()
        assert [x["cache_hit"] for x in audit["requests"]] == [False,False,True,False,True,False]
        assert audit["physical_cold_calls"] == 4 and audit["checked_cache_hits"] == 2
        assert service.cache.entries == 2
        zero = K.CachedService(cache_kind=kind,capacity=0)
        r0,r1 = purchase(zero,a),purchase(zero,aa)
        assert zero.cold_calls == 2 and zero.hits == 0 and zero.cache.entries == 0
        result.append({"kind":kind,"fifo_statuses":[x["cache_hit"] for x in audit["requests"]],
                       "cold_calls":service.cold_calls,"hits":service.hits,"entries":service.cache.entries,
                       "zero_capacity_calls":zero.cold_calls,"zero_capacity_detail":r1.detail})
    return result


def low_budget_and_invalid_inputs():
    result = []
    for kind in ("linear","hashed"):
        query = trivial("limited-valid",1)
        for limit in (0,47,48,100):
            service = K.CachedService(cache_kind=kind)
            receipt = service.checked_purchase(query,limit_total=limit,solver="dpll")
            assert not receipt.successful and receipt.answer is None and receipt.checked is False
            assert receipt.resources.total <= limit and service.cold_calls == service.hits == 0
            result.append({"kind":kind,"limit":limit,"status":receipt.status,"units":receipt.resources.total,"query_id":receipt.query_id})
        # Exact hit boundary: match an already initialized independent cache
        # state, then deny one unit of the complete adapter call.
        warm = K.CachedService(cache_kind=kind)
        purchase(warm,query)
        hit_query = trivial("limited-hit",1)
        paid = purchase(warm,hit_query)
        exact = K.CachedService(cache_kind=kind);purchase(exact,query)
        success = purchase(exact,hit_query,limit=paid.resources.total)
        denied = K.CachedService(cache_kind=kind);purchase(denied,query)
        failed = denied.checked_purchase(hit_query,limit_total=paid.resources.total-1,solver="dpll")
        check_receipt(failed,hit_query,False)
        assert failed.resources.total <= paid.resources.total-1 and denied.cold_calls == 1
        assert denied.cache.entries == 1
        invalid = K.CachedService(cache_kind=kind).checked_purchase(None,limit_total=1000,solver="dpll")
        assert invalid.status == "rejected" and invalid.answer is None and invalid.checked is False
        result.append({"kind":kind,"exact_hit_budget":paid.resources.total,"exact_hit_success":success.successful,
                       "one_less_status":failed.status,"one_less_spent":failed.resources.total,
                       "one_less_checked_cache_hits":denied.hits,"invalid_status":invalid.status})
    for kwargs in ({"capacity":65},{"capacity":-1},{"capacity":True},{"cache_kind":"unrecognized"}):
        try:
            K.CachedService(**kwargs)
        except S.Rejected:
            pass
        else:
            raise AssertionError("Invalid constructor configuration was accepted")
    return result


def failed_child_invoice():
    real = K.S
    outputs = []
    try:
        for kind in ("linear","hashed"):
            queries = []
            def exhausted_child(query,limit_total,solver):
                # Real production CNF failure invoice, with a disclosed local
                # fault fixture replacing only the copied facade's binding.
                queries.append((query.query_id,limit_total,solver))
                return real.checked_purchase(query,limit_total=64,solver=solver)
            K.S = SimpleNamespace(**{k:getattr(real,k) for k in ["Query","Receipt","Rejected","PROVIDER","VERSION","SERVICE_CAP","service_cap","ExactCache"]},checked_purchase=exhausted_child)
            service = K.CachedService(cache_kind=kind)
            q = trivial("injected-honest-child-failure",0)
            r = service.checked_purchase(q,limit_total=service.service_cap(q,"dpll"),solver="dpll")
            check_receipt(r,q,False)
            audit = service.audit_record()
            child = audit["requests"][0]["cold_receipt"]
            assert child["status"] == "budget_exhausted" and child["answer"] is None and child["checked"] is False
            prefix = "selected_cache_cold_provider:"
            expected = Counter({(x["category"],x["operation"]):x["units"] for x in child["resources"]["operations"]})
            actual = Counter({(a,b[len(prefix):]):n for a,b,n in r.resources.operations if b.startswith(prefix)})
            assert expected == actual and service.cache.entries == 0 and service.cold_calls == 1 and service.hits == 0
            outputs.append({"kind":kind,"adapter":r.record(),"child":child,"fixture_invocations":queries})
    finally:
        K.S = real
    return outputs


def maximum_key_full_cache_cap():
    results = []
    for kind in ("linear","hashed"):
        service = K.CachedService(cache_kind=kind,capacity=64)
        maximum = []
        largest = 0
        last = None
        for i in range(65):
            source = (f"source-{i:03d}-" + "s"*128)[:128]
            name = (f"request-{i:03d}-" + "q"*128)[:128]
            q = S.Query(name,12,tuple([(1,2,3,4)]*64),source)
            assert q.key_words == 343
            cap = service.service_cap(q,"dpll")
            r = purchase(service,q,limit=cap)
            assert r.answer == 1
            child_units = service.audit[-1]["cold_receipt"]["resources"]["total"]
            overhead = r.resources.total-child_units
            assert overhead < 60000 and overhead < K.CACHE_CONTROL_CAP
            largest = max(largest,overhead)
            last = r
            maximum.append(q)
        assert service.cache.entries == 64 and service.cold_calls == 65
        # The oldest full key was evicted; an admitted new ID for it is cold.
        old = maximum[0]
        again = S.Query("oldest-new-request",old.variables,old.clauses,old.source_version)
        purchase(service,again)
        assert service.cold_calls == 66 and service.hits == 0
        results.append({"kind":kind,"max_key_words":343,"capacity":64,"calls":service.cold_calls,
                        "largest_observed_nonchild_units":largest,"all_path_overhead_allowance":K.CACHE_CONTROL_CAP,
                        "last_full_cache_miss":last.record()})
    # Independent source-algebra envelope using a deliberately larger Q512.
    Q,A,Hbound,Kmax = 512,512+1377,4*512+16,64
    linear = 200+3*Q + 6+2*A + Kmax*(Q+2) + (16+Q)+Kmax*(Q+1)+(8+Q)+(2+Kmax)
    hashed = 200+3*Q + 204+2*A + 2 + 2*Hbound + 2*(1+Kmax*(Q+13)) + (16+Q) + 4+11 + (7+15+Q+3+3+4)
    assert linear == 72362 and hashed == 78137 and max(linear,hashed) < K.CACHE_CONTROL_CAP
    return {"paths":results,"conservative_Q512_nonchild_bounds":{"linear":linear,"hashed":hashed}}


def broker_coupling_and_reporting():
    outputs = []
    # All requests in each four-position block share one key. Keys alternate
    # SAT/UNSAT across blocks, so exactly two cold admissions suffice and
    # any selected position in a block supplies the same tested public bit.
    tape = tuple(trivial(f"coupled-{i:03d}",(i//4)%2) for i in range(24))
    for selector in ("uniform","tickets"):
        for hard in (False,True):
            contract = B.Contract(24,4,len(S.EXPERT_NAMES),8,8,selector,6,hard_index="hashed")
            ordinary_cap = B.funded_cap(S,tape,contract,hard=hard,solver="dpll")
            cold = B.execute(S,tape,contract,seed=47,hard=hard,unit_limit=ordinary_cap,purchase_solver="dpll")
            assert cold["status"] == "success" and cold["all_path_funded"]
            cold_report = P.report_owned_episode(S,cold,basis="snapshot",radius="grid")
            assert cold_report["status"] == "success"
            for kind in ("linear","hashed"):
                service = K.CachedService(cache_kind=kind)
                cap = B.funded_cap(service,tape,contract,hard=hard,solver="dpll")
                assert cap-ordinary_cap == contract.quota*K.CACHE_CONTROL_CAP
                r = B.execute(service,tape,contract,seed=47,hard=hard,unit_limit=cap,purchase_solver="dpll")
                assert r["status"] == "success" and r["all_path_funded"]
                for key in ["trace","blocks","weights","random_bits_consumed","purchases","hard_state"]:
                    assert r[key] == cold[key], (kind,selector,hard,key)
                assert r["purchases"] == contract.quota == service.logical_calls
                assert service.cold_calls == 2 and service.hits == 4
                for old,new in zip(cold["invoices"],r["invoices"]):
                    for key in ["query_id","claim_key","answer","checked","status"]:
                        assert old[key] == new[key]
                    assert new["provider"] == K.PROVIDER and new["provider_version"] == K.VERSION
                child_ops = Counter()
                for invoice in r["invoices"]:
                    child_ops.update({(x["category"],x["operation"]):x["units"] for x in invoice["resources"]["operations"]})
                prefix = "selected_provider:"
                parent_ops = Counter({(x["category"],x["operation"][len(prefix):]):x["units"] for x in r["meter"]["operations"] if x["operation"].startswith(prefix)})
                assert child_ops == parent_ops
                report = P.report_owned_episode(service,r,basis="snapshot",radius="grid")
                assert report["status"] == "success"
                for key in ["Q","R","n_live","sampling_radius","action_radius","reference_centers","live_centers","reference_corrections","corrections","intervals","deterministic_envelopes","confidence_eligible"]:
                    assert report[key] == cold_report[key],key
                wrong = P.report_owned_episode(S,r,basis="snapshot",radius="grid")
                assert wrong["status"] == "failed" and not wrong["confidence_eligible"]
                # Fresh below-envelope completion has no funded assertion.
                cheap = K.CachedService(cache_kind=kind)
                completed_low = B.execute(cheap,tape,contract,seed=47,hard=hard,unit_limit=cap-1,purchase_solver="dpll")
                assert completed_low["status"] == "success" and not completed_low["all_path_funded"]
                outputs.append({"selector":selector,"hard":hard,"kind":kind,"cold_local_units":cold["meter"]["total"],
                    "cached_local_units":r["meter"]["total"],"cold_cap":ordinary_cap,"cached_cap":cap,
                    "logical_selected_calls":service.logical_calls,"cold_calls":service.cold_calls,"hits":service.hits,
                    "report_units":report["meter"]["total"],"wrong_provider_report_status":wrong["status"],
                    "below_cap_success_not_funded":True})
    return outputs


if __name__ == "__main__":
    started = datetime.now(timezone.utc).isoformat()
    for name,fn in [("source_binding",source_binding),("new_id_and_accounting",new_id_and_accounting),
                    ("source_version_and_eviction",source_version_and_eviction),("low_budget_and_invalid_inputs",low_budget_and_invalid_inputs),
                    ("failed_child_invoice_disclosed_fixture",failed_child_invoice),
                    ("maximum_key_full_cache_cap",maximum_key_full_cache_cap),("broker_coupling_and_reporting",broker_coupling_and_reporting)]:
        run_case(name,fn)
    result = {"stage":"DEVELOPMENT","reviewer":"same-model nonblind independent focused source review",
              "started_utc":started,"finished_utc":datetime.now(timezone.utc).isoformat(),
              "script_sha256":sha256(Path(__file__).read_bytes()).hexdigest(),"research_credit_seconds":0,
              "pass":all(c["pass"] for c in cases),"passed_cases":sum(c["pass"] for c in cases),"cases":cases}
    with (HERE/"results.json").open("x") as f:
        json.dump(result,f,indent=2,sort_keys=True);f.write("\n")
    print(json.dumps({k:v for k,v in result.items() if k != "cases"}|{"case_status":[{"name":x["name"],"pass":x["pass"],"exception":x.get("exception")} for x in cases]},sort_keys=True))
    raise SystemExit(0 if result["pass"] else 1)
