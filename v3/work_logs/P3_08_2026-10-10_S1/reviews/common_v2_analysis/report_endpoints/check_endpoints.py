"""Public-input-only retrospective interval informativeness diagnostic.

Same-model nonblind: this reviewer previously saw private scores in a separate
audit. This executable neither reads private files nor reruns any service.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import gzip
import json
import traceback

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
WORK = HERE.parents[2]
DEV = WORK / "development"


def read(p):
    return json.loads(p.read_text())


def digest(p):
    return sha256(p.read_bytes()).hexdigest()


def pair(v):
    return [v.numerator, v.denominator]


def rows(p):
    with gzip.open(p,"rt") as f:
        for line in f:
            yield json.loads(line)


def caps(episode):
    flo = fhi = vlo = vhi = F()
    n = 0
    for row in episode["trace"]:
        q = F(*row["emitted_q"])
        hard = row["hard_before"] == "checked"
        y = row["prospective_action"] if hard else None
        if row["selected"]:
            y = row["purchased_label"]
            assert type(y) is int and y in (0,1)
        if y is None:
            flo += min(q*q,(1-q)**2)
            fhi += max(q*q,(1-q)**2)
        else:
            flo += (q-y)**2
            fhi += (q-y)**2
        if not row["selected"] and not hard:
            n += 1
            vlo += min(q,1-q)
            vhi += max(q,1-q)
    return {"F":(flo,fhi),"V":(vlo,vhi),"Z":(F(),F(n))}


def inspect_report(rid, report, expected_caps, construction):
    assert report["status"] == "success"
    result = {"run_id":rid,"construction":construction,"n_live":report["n_live"],
              "sampling_radius":report["sampling_radius"],"targets":{}}
    assert report["n_live"] == expected_caps["Z"][1]
    for target in ("F","V","Z"):
        lo,hi = [F(*x) for x in report["deterministic_envelopes"][target]]
        assert (lo,hi) == expected_caps[target]
        interval = report["intervals"][target]
        left,right = F(*interval["lower"]), F(*interval["upper"])
        assert left >= lo and right <= hi
        empty = left > right
        assert interval["confidence_conflict"] == empty
        if report["n_live"] == 0:
            formula = (lo,hi)
        else:
            center = F(*report["live_centers"]["V" if target == "Z" else target])
            radius = F(*report["sampling_radius"]) + (report["action_radius"] if target == "Z" else 0)
            formula = (max(lo,center-radius),min(hi,center+radius))
        assert (left,right) == formula
        result["targets"][target] = {"cap":[pair(lo),pair(hi)],"interval":[pair(left),pair(right)],
            "empty":empty,"conflict":interval["confidence_conflict"],
            "lower_strict_improvement":not empty and left > lo,
            "upper_strict_improvement":not empty and right < hi,
            "either_strict_improvement":not empty and (left > lo or right < hi),
            "both_endpoints_equal_caps":left == lo and right == hi}
    return result


def summarize(items):
    out = {"reports":len(items),"reports_with_any_strict_tightening":sum(any(t["either_strict_improvement"] for t in x["targets"].values()) for x in items),
           "exact_all_remaining_known":sum(x["n_live"] == 0 for x in items),"targets":{}}
    for target in ("F","V","Z"):
        tt = [x["targets"][target] for x in items]
        out["targets"][target] = {k:sum(x[k] for x in tt) for k in ["empty","conflict","lower_strict_improvement","upper_strict_improvement","either_strict_improvement","both_endpoints_equal_caps"]}
    return out


def comparison(left,right):
    # Compare the declared alternative right to left; no posthoc minimum.
    old,new = F(*left["sampling_radius"]),F(*right["sampling_radius"])
    item = {"radius_change":"smaller" if new < old else "larger" if new > old else "equal",
            "old_radius":pair(old),"new_radius":pair(new),"targets":{}}
    for target in ("F","V","Z"):
        a,b = left["targets"][target],right["targets"][target]
        a0,a1 = (F(*x) for x in a["interval"])
        b0,b1 = (F(*x) for x in b["interval"])
        item["targets"][target] = {"old_empty":a["empty"],"new_empty":b["empty"],
            "strict_lower_gain":not b["empty"] and b0>a0,
            "strict_upper_gain":not b["empty"] and b1<a1,
            "either_endpoint_gain":not b["empty"] and (b0>a0 or b1<a1),
            "equal_endpoints":(a0,a1)==(b0,b1),
            "strict_width_reduction":not a["empty"] and not b["empty"] and b1-b0<a1-a0}
    return item


def compare_summary(items):
    return {"pairs":len(items),"radius_changes":dict(Counter(x["radius_change"] for x in items)),
            "targets":{t:{k:sum(x["targets"][t][k] for x in items) for k in ["old_empty","new_empty","strict_lower_gain","strict_upper_gain","either_endpoint_gain","equal_endpoints","strict_width_reduction"]} for t in ("F","V","Z")}}


def run():
    for source in read(HERE/"plan.json")["sources"]:
        assert digest(ROOT/source["path"]) == source["sha256"]
    archives = {}
    for version in ("common_v1","common_v2"):
        directory = DEV/version/"run"
        seal = read(directory/"public_seal.json")
        expected = next(x["sha256"] for x in seal["files"] if x["path"] == "public_records.jsonl.gz")
        assert digest(directory/"public_records.jsonl.gz") == expected
        archives[version] = {x["run_id"]:x for x in rows(directory/"public_records.jsonl.gz") if x["configuration"]["kind"] == "broker"}
    replay_seal = read(DEV/"reporting_v2/run/public_seal.json")
    assert digest(DEV/"reporting_v2/run/public_reports.jsonl.gz") == replay_seal["output_sha256"]
    assert digest(DEV/"common_v1/run/public_records.jsonl.gz") == replay_seal["input_public_archive_sha256"]
    assert digest(DEV/"common_v1/run/public_seal.json") == replay_seal["input_public_seal_sha256"]
    common = []
    common_virtual_fixed = []
    for rid,record in archives["common_v2"].items():
        r = record["optional_reporting"]["report"]
        result = inspect_report(rid,r,caps(record["episode"]),"snapshot/grid")
        common.append(result)
        # Same Q/centers, fixed-rule radius formula. Public diagnostic only;
        # the actual archive contains the prospectively selected grid report.
        fixed_rho = F(*r["Q"])/r["original_fixed_R"] + F(5*r["original_fixed_R"],8)
        virtual = json.loads(json.dumps(result))
        virtual["sampling_radius"] = pair(fixed_rho)
        for target in ("F","V","Z"):
            lo,hi = (F(*x) for x in virtual["targets"][target]["cap"])
            center = F(*r["live_centers"]["V" if target == "Z" else target])
            width = fixed_rho + (r["action_radius"] if target == "Z" else 0)
            low,high = (lo,hi) if r["n_live"] == 0 else (max(lo,center-width),min(hi,center+width))
            virtual["targets"][target]["interval"] = [pair(low),pair(high)]
            virtual["targets"][target]["empty"] = low>high
        common_virtual_fixed.append({"run_id":rid}|comparison(virtual,result))
    replay = []
    groups = defaultdict(dict)
    for row in rows(DEV/"reporting_v2/run/public_reports.jsonl.gz"):
        rid = row["run_id"]
        construction = row["basis"]+"/"+row["radius"]
        result = inspect_report(rid,row["report"],caps(archives["common_v1"][rid]["episode"]),construction)
        replay.append(result)
        groups[rid][construction] = result
    assert len(common) == 63 and len(replay) == 180 and len(groups) == 45
    contrasts = defaultdict(list)
    for rid,group in groups.items():
        for left,right,label in [("base/fixed","base/grid","grid_vs_fixed_base_basis"),
                                 ("snapshot/fixed","snapshot/grid","grid_vs_fixed_snapshot_basis"),
                                 ("base/fixed","snapshot/fixed","snapshot_vs_base_fixed_rule"),
                                 ("base/grid","snapshot/grid","snapshot_vs_base_grid_rule"),
                                 ("base/fixed","snapshot/grid","snapshot_grid_vs_original_base_fixed")]:
            contrasts[label].append({"run_id":rid}|comparison(group[left],group[right]))
    summary = {"common_v2":summarize(common),"replay_v2":summarize(replay),
        "replay_constructions":{name:summarize([x for x in replay if x["construction"] == name]) for name in sorted(groups[next(iter(groups))])},
        "replay_pair_comparisons":{name:compare_summary(items) for name,items in contrasts.items()},
        "common_grid_vs_same_basis_virtual_fixed":compare_summary(common_virtual_fixed)}
    with (HERE/"details.json").open("x") as f:
        json.dump({"common":common,"replay":replay,"replay_pair_comparisons":contrasts,"common_virtual_fixed":common_virtual_fixed},f,indent=2,sort_keys=True);f.write("\n")
    return summary


if __name__ == "__main__":
    outcome = {"stage":"DEVELOPMENT","started_utc":datetime.now(timezone.utc).isoformat(),
               "script_sha256":digest(Path(__file__)),"private_data_read_by_this_executable":False,
               "reviewer_nonblind":True,"research_credit_seconds":0}
    try:
        outcome["summary"] = run()
        outcome["pass"] = True
    except Exception:
        outcome["pass"] = False
        outcome["exception"] = traceback.format_exc()
    outcome["finished_utc"] = datetime.now(timezone.utc).isoformat()
    with (HERE/"results.json").open("x") as f:
        json.dump(outcome,f,indent=2,sort_keys=True);f.write("\n")
    print(json.dumps(outcome,sort_keys=True))
    raise SystemExit(0 if outcome["pass"] else 1)
