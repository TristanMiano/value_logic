"""Exact two-component analysis of already completed development observations."""
from pathlib import Path
import json
from fractions import Fraction as F

ROOT = Path(__file__).resolve().parent
def read(path):
    return json.loads(path.read_text(encoding="utf-8"))
def rational(x):
    return {"numerator": x.numerator, "denominator": x.denominator, "decimal": float(x)}
def feasible(rows, arm, factor=F(1), controls=None):
    """lambda>=0 for cost(arm)<=factor*cost(each control), exact inclusive bounds."""
    lo, hi, reasons = F(0), None, []
    a = rows[arm]
    for name in controls or rows:
        b = rows[name]
        slope = F(a["named_units"]) - factor*b["named_units"]
        intercept = factor*b["physical_fee"] - a["physical_fee"]
        if slope == 0:
            if intercept < 0:
                return {"empty": True, "obstruction": name}
        elif slope > 0:
            bound = intercept/slope
            hi = bound if hi is None else min(hi,bound)
        else:
            lo = max(lo,intercept/slope)
        reasons.append(name)
    if hi is not None and (hi < lo or hi < 0):
        return {"empty": True, "lower": rational(lo), "upper": rational(hi)}
    return {"empty": False, "lower": rational(lo), "upper": None if hi is None else rational(hi)}

sf = read(ROOT/"sf01/checked.json")["strata"]
result={"contributor":"Codex (GPT-6)","scope":"DEVELOPMENT; cost = physical fee + lambda * named semantic units; all unpriced costs excluded, hence not a complete-cost region.","scalar":{}}
for stratum, rows in sf.items():
    result["scalar"][stratum] = {
        "observed": rows,
        "ordinary_menu_envelope": {arm: feasible(rows,arm) for arm in rows},
        "prefix_10pct_vs_full": feasible(rows,"scalar_prefix",F(9,10),["relevant_audit"]),
        "prefix_10pct_vs_all_ordinary": feasible(rows,"scalar_prefix",F(9,10),[x for x in rows if x != "scalar_prefix"]),
    }
patches=[]
for source in read(ROOT/"patch01/design.json")["sources"]:
    row=read(ROOT/"patch01"/source["name"]/"results.json")
    base=row["base"]["named_units"]
    partial=[]; inc=base; fresh=0
    for patch in row["rows"]:
        inc+=patch["incremental"]["named_units"]
        fresh+=patch["fresh"]["named_units"]
        partial.append({"variable":patch["variable"],"value":patch["value"],"incremental_with_base":inc,"fresh":fresh,"incremental_wins":inc<fresh})
    patches.append({"source":source["name"],"base":base,"incremental":row["incremental_total"],"fresh":row["fresh_total"],"prefixes":partial,"models":[r["models"] for r in row["rows"]],"negative_controls":row["negatives"]})
result["patches"]={"sources":patches,"incremental":sum(x["incremental"] for x in patches),"fresh":sum(x["fresh"] for x in patches),"patches":sum(len(x["prefixes"]) for x in patches),"negative_controls":sum(x["negative_controls"] for x in patches),"unsatisfiable_patches":sum(n==0 for x in patches for n in x["models"]),"single_patch_wins":sum(x["prefixes"][0]["incremental_wins"] for x in patches),"six_patch_wins":sum(x["incremental"]<x["fresh"] for x in patches)}
rl=read(ROOT/"rl01/checked.json")
result["learning"]={"observed":rl["strata"],"coverage_violations":rl["coverageViolations"],"violations_under_stated_assumptions":sum(x["assumptions_hold"] for x in rl["coverage"]),"violations_by_law":{law:sum(x["law"]==law for x in rl["coverage"]) for law in {x["law"] for x in rl["coverage"]}}}
(ROOT/"component_analysis.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"scalar":{s:{k:v for k,v in x.items() if k!="observed"} for s,x in result["scalar"].items()},"patches":{k:v for k,v in result["patches"].items() if k!="sources"},"learning":{k:v for k,v in result["learning"].items() if k!="observed"}},indent=2))
