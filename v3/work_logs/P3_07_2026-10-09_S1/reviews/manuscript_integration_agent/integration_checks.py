"""Frozen manuscript integration checks; saved data and exact arithmetic only.

No solver, experiment, old suite, or root source is executed or changed.
Same-model targeted nonblind review; zero principal Research90 credit.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
WORKLOG = HERE.parent.parent
ROOT = WORKLOG.parents[2]
DERIVATIONS = ROOT / "v3/derivations"


def read(path):
    return json.loads(path.read_text())


def filehash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def section(text, start, end):
    return text.split(start,1)[1].split(end,1)[0]


def table_rows(text):
    return [[cell.strip() for cell in line.strip().strip("|").split("|")]
            for line in text.splitlines() if line.startswith("|") and not line.startswith("|---")]


def main():
    snapshots = read(HERE / "input_snapshots.json")
    for name, item in snapshots.items():
        assert filehash(DERIVATIONS/name) == filehash(HERE/item["snapshot"]) == item["sha256"]
    manuscript = (HERE / snapshots["07_paid_reasoning.md"]["snapshot"]).read_text()
    companion = (HERE / snapshots["07_ordinary_analytic_profile.md"]["snapshot"]).read_text()
    checks = []
    evidence = set()
    def data(relative):
        path = WORKLOG/relative
        evidence.add(path)
        return read(path)
    def number(label, exact, displayed, *, present=True):
        q = F(exact)
        text = displayed.replace(",", "").strip()
        d = F(text)
        digits = len(text.split(".")[1]) if "." in text else 0
        tolerance = F(1,2*10**digits) if "." in text else F(0)
        assert abs(q-d) <= tolerance, (label, str(q), displayed)
        if present:
            assert displayed in manuscript or displayed in companion, (label, displayed)
        checks.append({"claim":label,"exact":str(q),"displayed":displayed,"max_rounding_error":str(tolerance),"pass":True})

    selections = data("development/run_v3/selections.json")
    by_selection = {(r["profile_n"],r["price"],r["selection"]["horizon"]):r for r in selections}
    assert len(selections) == 72
    table = table_rows(section(manuscript,"### 6.2 ","### 6.3 "))[1:]
    price_keys = ("low","high","false_positive_expensive","false_negative_expensive","zero_task","storage_expensive")
    policy_labels = {"fallback":"fallback","full_fallback":"full computation","guess0":"guess 0","guess1":"guess 1"}
    assert len(table) == 6
    for row, price in zip(table,price_keys):
        first = by_selection[(1024,price,64)]["selection"]
        assert row[1].startswith(policy_labels[first["policy"]])
        number(f"sampled {price} lower/query",first["lower_gain_per_query"],row[2])
        for horizon,column in ((64,3),(10000,4)):
            selected = by_selection[(1024,price,horizon)]["selection"]
            assert selected["policy"] == first["policy"]
            number(f"sampled {price} H{horizon}",selected["all_in_lower_gain"],row[column])
            assert F(selected["all_in_lower_gain"]) == horizon*F(selected["lower_gain_per_query"])-F(selected["setup_to_recover"])-F(selected["assessment_cost"])
    changed_cases = []
    for price in price_keys:
        choices = [by_selection[(n,price,64)]["selection"]["policy"] for n in (128,256,512,1024)]
        if len(set(choices)) > 1: changed_cases.append({"price":price,"choices":choices})
    assert changed_cases == [{"price":"storage_expensive","choices":["fallback","fallback","fallback","full_fallback"]}]
    high_lower = [F(by_selection[(n,"high",64)]["selection"]["lower_gain_per_query"]) for n in (128,256,512,1024)]
    assert high_lower == sorted(high_lower)
    assert all(by_selection[(1024,price,64)]["exact_best_policy"]=="full_fallback" for price in ("false_positive_expensive","false_negative_expensive"))
    full_run = data("development/run_v3/result.json")
    sample_units = sum(full_run["profile_setup"]["total_resources"].values())
    number("sampled procurement units",sample_units,"1,692,957")
    number("sampled ordinary setup cost",F(sample_units,1000),"1,692.957")
    for price, setup, cost in (("storage_expensive","39,117.036","70.421"),("zero_task","1,692.957","1.297")):
        s=by_selection[(1024,price,64)]["selection"]
        number(price+" setup",s["setup_to_recover"],setup)
        number(price+" assessment",s["assessment_cost"],cost)

    warm = data("development/run_v3/self_audit.json")
    for key, displayed in (("controller","7.9654375"),("fallback","307.437296875"),("charged_exact","4.0724375")):
        number("warm-profile mean "+key,warm["observed_mean_costs_per_batch"][key],displayed)
    assert warm["lower_gain_per_batch"] == "246661639/1024000"
    number("warm-profile lower",warm["lower_gain_per_batch"],"240.880507")
    number("warm-profile extra assessment",F(warm["observed_mean_costs_per_batch"]["controller"])-F(warm["observed_mean_costs_per_batch"]["charged_exact"]),"3.893")
    number("warm audit procurement plus final check",sum(warm["procurement_resources"].values())+warm["final_audit_check_meter"]["total"],"4,057,527")

    whole = data("development/whole_procedure_run_v2/result.json")
    whole_rows = table_rows(section(manuscript,"### 6.3 ","### 6.4 "))[1:]
    whole_keys=("mean_controller_all_in_cost","mean_baseline_cost","mean_charged_exact_cost","mean_all_in_gain","lower_all_in_gain","outer_audit_procurement_cost")
    assert len(whole_rows) == len(whole_keys) == 6
    for row,key in zip(whole_rows,whole_keys):
        exact_cell=row[1].replace("$`","").replace("`$","")
        assert F(exact_cell)==F(whole[key])
        number("whole v2 "+key,whole[key],row[2])
    number("whole resource cap",whole["closure"]["whole_resource_cap"],"628,752")
    number("whole lower range",whole["closure"]["scalar_range"][0],"-5748.752")
    number("whole startup",whole["outer_startup_meter"]["total"],"45,598")

    analytic = data("development/analytic_profile_run_v2/result.json")
    analytic_profile = data("development/analytic_profile_run_v2/analytic_profile.json")
    assert analytic_profile["core_bytes"] == 5680 and analytic["profile_id"] in companion
    number("analytic construction units",analytic["total_procurement_units"],"64,581")
    analytic_by_price={row["price"]:row for row in analytic["selections"]}
    companion_rows=table_rows(section(companion,"## 4. ","## 5. "))[1:]
    assert len(companion_rows)==6
    for row,price in zip(companion_rows,price_keys):
        selected=analytic_by_price[price]
        for horizon,column in ((64,2),(10000,3)):
            exact_cell=row[column].replace("$`","").replace("`$","")
            assert F(exact_cell)==F(selected[f"all_in_gain_H{horizon}"])
            checks.append({"claim":f"analytic table {price} H{horizon}","exact":exact_cell,"pass":True})
    number("analytic high setup",analytic_by_price["high"]["setup_cost"],"64.581")
    number("analytic high assessment",analytic_by_price["high"]["assessment_cost"],"0.740")
    number("analytic high H64",analytic_by_price["high"]["all_in_gain_H64"],"1,149.624548")
    number("analytic storage setup",analytic_by_price["storage_expensive"]["setup_cost"],"1,481.469")
    number("analytic storage assessment",analytic_by_price["storage_expensive"]["assessment_cost"],"25.688")
    number("analytic storage H64",analytic_by_price["storage_expensive"]["all_in_gain_H64"],"-760.973258")
    number("analytic storage H10000",analytic_by_price["storage_expensive"]["all_in_gain_H10000"],"115,084.052677")
    number("analytic low sunk loss",-F(analytic_by_price["low"]["all_in_gain_H64"]),"65.321")
    exact_population=data("development/run_v3/population_exact.json")
    number("exhaustive procurement excluding private checks",sum(exact_population["resources"].values())-248,"359,918")
    assert analytic["checked_query_policy_resource_and_completion_rows"]==1488

    ordinary_counts=[]
    for prime in (17,31,47,61,97):
        n=(prime-1)//2
        positive=n-1-int(n%2==0)
        negative=n-int(n%2==1)
        assert positive+negative==prime-3
        group=next(g for g in analytic_profile["classes"] if g["prime"]==prime and g["kind"]=="ordinary")
        assert (positive,negative)==(group["positive"],group["negative"])
        ordinary_counts.append({"prime":prime,"positive":positive,"negative":negative,"size":prime-3})

    acquisition=data("development/acquisition_boundary_v1_1/result.json")
    acquisition_rows=data("development/acquisition_boundary_v1_1/rows.json")
    assert acquisition["minimum_n_for_optimal_symmetric_three_quarter_accuracy"]==45
    assert acquisition["minimum_n_from_chi_square_necessary_condition"]==18
    assert all(F(row["optimal_symmetric_accuracy"])<F(3,4) for row in acquisition_rows[:45])
    assert F(acquisition_rows[45]["optimal_symmetric_accuracy"])>=F(3,4)
    number("identification n44 accuracy",acquisition_rows[44]["optimal_symmetric_accuracy"],"0.745767")
    number("identification n45 accuracy",acquisition_rows[45]["optimal_symmetric_accuracy"],"0.750561")
    assert acquisition["best_sign_accuracy_at_affordable_n"]=="32415876138437/51200000000000"
    number("affordable sign accuracy",acquisition["best_sign_accuracy_at_affordable_n"],"0.633123")
    assert F(acquisition["bill_at_exact_minimum"])>F(acquisition["maximum_good_law_future_gross_gain"])
    assert (F(103,99)**17 < 2 <= F(103,99)**18)

    optional=data("reviews/proof_agent/policy_proof_checks_result.json")["optional_stopping"]
    q=optional["optional_stopping_false_positive_probability"]
    number("optional-stopping crossing",F(int(q["numerator"]),int(q["denominator"])),"0.11284")
    assert optional["maximum_profile_samples"]==2000

    dependency=data("development/adapter_agent/dependency_probe_v2/results.json")
    components={k:F(v) for k,v in dependency["base_stage_costs"].items()}
    for key,text in (("model_construction","0.085"),("repair_search","1.098"),("independent_check","0.52335"),("retention","0.09004")):
        number("dependency "+key,components[key],text)
    all_cost=sum(components.values(),F(0)); partial=components["independent_check"]+components["retention"]
    for label,value,display in (("dependency check/retain",partial,"0.61339"),("dependency misleading saving",1-partial,"0.38661"),("dependency full cost",all_cost,"1.79639"),("dependency full gain",1-all_cost,"-0.79639")):
        number(label,value,display)
    assert dependency["checkpoints"][-1]["actual_total_pops"]==13
    assert dependency["independent_check"]["best_repairs"]==[[1,0,1,1],[1,1,0,0]]
    assert dependency["independent_check"]["exact_difference_image"]==[0,1]
    assert len(dependency["tariff_grid"])==15

    multi_rows=[]
    for name,display in (("full_root_eight_bits","640.419"),("capped_root_eight_bits","638.761"),("full_root_one_bit","642.014")):
        row=data(f"development/multi_action_run_v2/{name}_result.json")
        number("multi-action deployment excluding setup "+name,row["all_in_cost_excluding_one_time_setup"],display)
        assert F(row["initial_setup_fee"])==F(2,3125)
        assert F(row["always_buy_fee_cost"])==368 and row["rounds"]==32
        all_in=F(row["all_in_cost_excluding_one_time_setup"])+F(row["initial_setup_fee"])
        multi_rows.append({"name":name,"manuscript_display":display,"deployment_excluding_setup":row["all_in_cost_excluding_one_time_setup"],"setup":row["initial_setup_fee"],"including_setup_exact":str(all_in),"including_setup_3dp":format(float(all_in),".3f")})

    # The prior narrow §3.3 review applies to the exact same section text.
    previous_section=WORKLOG/"reviews/whole_audit_agent/section_3_3_reviewed_v2.txt"
    evidence.add(previous_section)
    assert section(manuscript,"### 3.3 ","\n## 4. ").strip()==previous_section.read_text().split("### 3.3 ",1)[1].strip()

    broken_links=[]
    for name,item in snapshots.items():
        text=(HERE/item["snapshot"]).read_text()
        for target in re.findall(r"\]\(([^)]+)\)",text):
            if "://" in target or target.startswith("#"):continue
            base=target.split("#",1)[0]
            if base and not (DERIVATIONS/base).resolve().exists():broken_links.append({"document":name,"target":target})
    assert not broken_links
    for name,item in snapshots.items():
        assert filehash(DERIVATIONS/name)==item["sha256"]
    return {"status":"MATHEMATICS_AND_NUMERICAL_TRANSCRIPTIONS_PASS_WITH_ONE_COST_LABEL_FINDING",
            "review_type":"Same-model targeted nonblind integration review; no new broad tests or solver runs.",
            "snapshots":snapshots,"numeric_checks":checks,"numeric_check_count":len(checks),
            "only_checkpoint_policy_change":changed_cases,"ordinary_class_counts":ordinary_counts,
            "multi_action_cost_label_finding":multi_rows,"missing_local_link_targets":broken_links,
            "source_cards_consistency":"Main section 7 is consistent with the inspected retained primary-source cards; no new primary-source retrieval performed.",
            "unchanged_section_3_3":True,"evidence_sha256":{str(path.relative_to(ROOT)):filehash(path) for path in sorted(evidence)},
            "principal_research90_credit_seconds":0}


if __name__=="__main__":
    result=main()
    with (HERE/"integration_check_results.json").open("x") as stream:
        json.dump(result,stream,indent=2,sort_keys=True);stream.write("\n")
    print(json.dumps({key:value for key,value in result.items() if key not in ("numeric_checks","evidence_sha256")},indent=2,sort_keys=True))
