"""Focused independent source-bound review of the v1.1 output contract.

DEVELOPMENT; nonblind; no production edits, private truth or research credit.
"""
from collections import Counter
from datetime import datetime,timezone
from hashlib import sha256
from pathlib import Path
from types import SimpleNamespace
import importlib.util
import json
import sys
import traceback

HERE=Path(__file__).resolve().parent
SOURCE=HERE/"source_snapshot"
sys.path.insert(0,str(SOURCE/"v3/experiments"))
import p308_cached_service as K
import p308_cnf as S
import p308_broker as B
from p308_common import C
spec=importlib.util.spec_from_file_location("paid_receipt_v1_preserved",HERE/"p308_cached_service_v1_preserved.py")
OLD=importlib.util.module_from_spec(spec);spec.loader.exec_module(OLD)

def op(receipt): return Counter({(a,b):n for a,b,n in receipt.resources.operations})
def paid_response(receipt): return op(receipt)[("output","selected_cache_final_receipt_prepaid")]
def query(name,answer=1,source="test-source"):
    return S.Query(name,4,() if answer else ((),(1,)),source)


def no_answer(receipt):
    assert receipt.answer is None and receipt.witness is None and receipt.checked is False and not receipt.successful
    assert receipt.provider==K.PROVIDER and receipt.provider_version==K.VERSION
    assert receipt.resources.total==sum(op(receipt).values())==sum(n for _,n in receipt.resources.by_category)
    assert paid_response(receipt)==576


def boundaries():
    results=[]
    for kind in ("linear","hashed"):
        q=query("boundary")
        for amount in (0,48,575,-1,True,1.5):
            service=K.CachedService(cache_kind=kind)
            try: service.checked_purchase(q,limit_total=amount,solver="dpll")
            except (S.Rejected,C.Rejected) as exc:
                assert service.logical_calls==service.cold_calls==service.hits==0 and service.audit==[]
                results.append({"kind":kind,"limit":amount,"external_rejection":type(exc).__name__})
            else: raise AssertionError("Below-minimum or invalid account was admitted")
        for amount in (576,623,624,625,1024):
            service=K.CachedService(cache_kind=kind)
            r=service.checked_purchase(q,limit_total=amount,solver="dpll")
            no_answer(r)
            assert 576<=r.resources.total<=amount and service.cold_calls==0
            if amount<624: assert r.resources.total==576
            if amount==624: assert r.resources.total==624
            results.append({"kind":kind,"limit":amount,"status":r.status,"units":r.resources.total,"response_units":paid_response(r),"query_id":r.query_id})
        invalid=K.CachedService(cache_kind=kind).checked_purchase(None,limit_total=624,solver="dpll")
        no_answer(invalid);assert invalid.status=="rejected"
        service=K.CachedService(cache_kind=kind)
        service.checked_purchase(q,limit_total=service.service_cap(q,"dpll"),solver="dpll")
        new=query("warm-new-id")
        hit=service.checked_purchase(new,limit_total=service.service_cap(new,"dpll"),solver="dpll")
        assert hit.successful
        other=K.CachedService(cache_kind=kind)
        other.checked_purchase(q,limit_total=other.service_cap(q,"dpll"),solver="dpll")
        denied=other.checked_purchase(new,limit_total=hit.resources.total-1,solver="dpll")
        no_answer(denied)
        assert other.cold_calls==1 and other.cache.entries==1
        results.append({"kind":kind,"late_failure_limit":hit.resources.total-1,"late_failure_units":denied.resources.total,"response_units":paid_response(denied)})
    return results


def exact_delta_and_version():
    results=[]
    for kind in ("linear","hashed"):
        for capacity in (0,2):
            old,new=OLD.CachedService(cache_kind=kind,capacity=capacity),K.CachedService(cache_kind=kind,capacity=capacity)
            qs=[query("first",0,"source-a"),query("first-new-id",0,"source-a"),query("version-miss",0,"source-b"),
                query("third-key",1,"source-c"),query("first-again",0,"source-a")]
            for q in qs:
                a=old.checked_purchase(q,limit_total=old.service_cap(q,"dpll"),solver="dpll")
                b=new.checked_purchase(q,limit_total=new.service_cap(q,"dpll"),solver="dpll")
                assert a.successful and b.successful
                assert (a.query_id,a.claim_key,a.answer,a.checked,a.witness)==(b.query_id,b.claim_key,b.answer,b.checked,b.witness)
                assert a.provider_version==OLD.VERSION and b.provider_version==K.VERSION and OLD.VERSION!=K.VERSION
                ao,bo=op(a),op(b)
                key=("output","selected_cache_final_receipt_prepaid")
                assert ao[key]==64+q.key_words and bo[key]==576
                del ao[key];del bo[key]
                assert ao==bo and b.resources.total-a.resources.total==512-q.key_words
                assert old.service_cap(q,"dpll")==new.service_cap(q,"dpll")
                assert old.cold_calls==new.cold_calls and old.hits==new.hits
                if capacity==0:
                    assert "retention follows cache capacity" in b.detail and new.cache.entries==0
                results.append({"kind":kind,"capacity":capacity,"query_id":q.query_id,"Q":q.key_words,
                    "old_units":a.resources.total,"new_units":b.resources.total,"delta":b.resources.total-a.resources.total,
                    "cache_hit":new.audit[-1]["cache_hit"]})
        # Actual admitted maximum key, with both a cold and new-ID hit.
        q=S.Query("q"*128,12,tuple([(1,2,3,4)]*64),"s"*128)
        old,new=OLD.CachedService(cache_kind=kind),K.CachedService(cache_kind=kind)
        for current in (q,S.Query("r"*128,q.variables,q.clauses,q.source_version)):
            a=old.checked_purchase(current,limit_total=old.service_cap(current,"dpll"),solver="dpll")
            b=new.checked_purchase(current,limit_total=new.service_cap(current,"dpll"),solver="dpll")
            assert current.key_words==343 and a.successful and b.successful and b.resources.total-a.resources.total==169
            results.append({"kind":kind,"Q":343,"old_units":a.resources.total,"new_units":b.resources.total,"delta":169,"cache_hit":new.audit[-1]["cache_hit"]})
    # The old formulas are135Q+3242 and143Q+4921. Replacing64+Q by576
    # adds512-Q, giving monotone134Q+3754 and142Q+5433.
    bound={q:{"linear":134*q+3754,"hashed":142*q+5433} for q in (343,512)}
    assert bound[512]=={"linear":72362,"hashed":78137}
    assert bound[343]=={"linear":49716,"hashed":54139}
    assert max(bound[512].values())<80000<K.CACHE_CONTROL_CAP
    return {"calls":results,"source_based_nonchild_envelopes":bound}


def broker_failure_footer():
    tape=tuple(query(f"broker-{i}") for i in range(4))
    contract=B.Contract(4,4,len(S.EXPERT_NAMES),8,8,"uniform",1)
    results=[]
    for amount in (575,576,624):
        service=K.CachedService()
        record=B.execute(service,tape,contract,seed=11,hard=True,purchase_solver="dpll",provider_limit=amount)
        assert record["status"]=="failed" and not record["all_path_funded"] and not record["expectation_theorem_eligible"]
        costs=Counter({(x["category"],x["operation"]):x["units"] for x in record["meter"]["operations"]})
        assert costs[("output","reserved_final_status_words")]==64
        assert costs[("output","broker_prepaid_failure_status_words")]==8
        assert record["purchases"]==0
        if amount<576:
            assert record["invoices"]==[] and service.logical_calls==0
            # Reservation is a retained abort-state commitment, not spent
            # provider work; the failed broker is not resumed as a service.
            assert record["meter"]["reservations"].get("selected_provider")==amount
        else:
            assert len(record["invoices"])==1 and record["invoices"][0]["answer"] is None
            assert costs[("output","selected_provider:selected_cache_final_receipt_prepaid")]==576
        results.append({"provider_limit":amount,"status":record["status"],"paid_broker_status_words":72,
                        "service_logical_calls":service.logical_calls,"failed_receipts":len(record["invoices"]),
                        "retained_abort_reservations":record["meter"]["reservations"],"spent":record["meter"]["total"]})
    return results


def failed_child_paid_outer_response():
    real=K.S
    result=[]
    try:
        def failed(q,limit_total,solver):return real.checked_purchase(q,limit_total=64,solver=solver)
        K.S=SimpleNamespace(**{name:getattr(real,name) for name in ["Query","Receipt","Rejected","PROVIDER","VERSION","SERVICE_CAP","service_cap","ExactCache"]},checked_purchase=failed)
        for kind in ("linear","hashed"):
            service=K.CachedService(cache_kind=kind)
            q=query("fault-child",0)
            r=service.checked_purchase(q,limit_total=service.service_cap(q,"dpll"),solver="dpll")
            no_answer(r)
            child=service.audit[-1]["cold_receipt"]
            assert child["status"]=="budget_exhausted" and child["answer"] is None and service.cache.entries==0
            expected=Counter({(x["category"],x["operation"]):x["units"] for x in child["resources"]["operations"]})
            prefix="selected_cache_cold_provider:"
            actual=Counter({(a,b[len(prefix):]):n for a,b,n in r.resources.operations if b.startswith(prefix)})
            assert actual==expected
            result.append({"kind":kind,"child_units":child["resources"]["total"],"outer_units":r.resources.total,"outer_response_units":paid_response(r)})
    finally:K.S=real
    return result


if __name__=="__main__":
    result={"stage":"DEVELOPMENT","started_utc":datetime.now(timezone.utc).isoformat(),"script_sha256":sha256(Path(__file__).read_bytes()).hexdigest(),"research_credit_seconds":0,"cases":[]}
    for source in json.loads((HERE/"plan.json").read_text())["sources"]:
        assert sha256((SOURCE/source["path"]).read_bytes()).hexdigest()==source["sha256"]
    for name,fn in [("minimum_account_and_paid_denial",boundaries),("exact_v1_delta_and_version",exact_delta_and_version),
                    ("broker_failure_footer",broker_failure_footer),("failed_child_paid_outer_response",failed_child_paid_outer_response)]:
        try:row={"name":name,"pass":True,"result":fn()}
        except Exception:row={"name":name,"pass":False,"exception":traceback.format_exc()}
        result["cases"].append(row)
    result["pass"]=all(x["pass"] for x in result["cases"])
    result["finished_utc"]=datetime.now(timezone.utc).isoformat()
    with (HERE/"results.json").open("x") as f:json.dump(result,f,indent=2,sort_keys=True);f.write("\n")
    print(json.dumps({k:v for k,v in result.items() if k!="cases"}|{"case_status":[{"name":x["name"],"pass":x["pass"],"exception":x.get("exception")} for x in result["cases"]]},sort_keys=True))
    raise SystemExit(0 if result["pass"] else 1)
