#!/usr/bin/env python3
"""An actual paid audit/proof bundle with zero-gain singleton purchases.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12. A constructed illustration
of a whole scale family; no empirical transfer or economic-superiority claim.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
S06 = HERE.parent / "s06"
sys.path.insert(0, str(S06))
import anchor_quotes as aq
import contract_guard
import contract_quote as cq
import joint_repair as jr
import native_repair as native
from vertex_probe import jsonable
sys.path.insert(0, str(HERE))
import lattice_quotes as lq


def arithmetic_checks(meter):
    endpoint_cases = interval_cases = equivalence_cases = 0
    # These are objective-only reconstruction cases, never a provider's
    # logical models and never advice used to select the actual acquisition.
    for q in ([0, 2], [2, 0], [2, 4], [3, 6, 9], [1, 2, 3]):
        g = lq.objective_lattice(q, meter)
        for mask in range(1 << len(q)):
            value = sum(weight for j, weight in enumerate(q) if mask & (1 << j))
            assert value % g == 0
            for budget in range(-1, sum(q) + 1):
                if value <= budget:
                    assert value <= g * (budget // g)
                else:
                    assert value >= g * (budget // g + 1)
                endpoint_cases += 1
                meter.pay("construction_check", "objective_lattice_endpoint_case", 6 + len(q))
    for h in (1, 2, 3, 6):
        modes, lowers = [[0, h], [h, 0]], [0, 0]
        for possible in ([[0]], [[1]], [[0, 1]]):
            for q in ([0, h], [h, 0], [h, h], [1, 1]):
                for tau in (F(0), F(1, 2)):
                    answer = lq.closing_query([3], modes, possible, lowers, h + 1,
                                             q, tau, meter, exact_interval=True)
                    direct = [b for b in range(-1, 3 * h + 2)
                              if lq.quote([3], modes, possible, lowers, h + 1,
                                          q, b, meter)["worst_bound"] <= tau]
                    assert answer["closes"] == bool(direct)
                    if direct:
                        assert direct == list(range(answer["integer_budget_low"],
                                                    answer["integer_budget_high"] + 1))
                    interval_cases += 1
                for budget in (-1, 0, h, 2 * h):
                    old = aq.logical_quote([3], modes, possible, lowers, h + 1,
                                           q, budget, meter, complete=True)
                    new = lq.quote([3], modes, possible, lowers, h + 1,
                                   q, budget, meter)
                    assert new["SAT_bound"] <= old["SAT_bound"]
                    assert new["UNSAT_bound"] <= old["UNSAT_bound"]
                    if new["objective_lattice"] == 1:
                        assert new["SAT_bound"] == old["SAT_bound"]
                        assert new["UNSAT_bound"] == old["UNSAT_bound"]
                    equivalence_cases += 1
    return dict(objective_endpoint_cases=endpoint_cases,
                exact_interval_cases=interval_cases,
                monotonic_improvement_and_unit_gcd_cases=equivalence_cases,
                logical_model_or_optimum_enumerations=0,
                use="Reconstruction only; not acquisition advice or empirical confirmation")


def run(output):
    if output.exists():
        raise FileExistsError("Preserve the actual acquired receipts")
    wall, cpu = time.perf_counter_ns(), time.process_time_ns()
    source, raw = cq.source, cq.compilation
    meter = source.Meter()
    h, price, tolerance = 2, 3, 0
    logical = dict(row="s07-zero-singleton-bundle", variables=2, hard=[[1, 2]],
                   soft=[dict(weight=h, clause=[-1]), dict(weight=h, clause=[-2])],
                   public_incumbent=3, objective_max=2 * h)
    logical["identity"] = source.digest(logical)
    data = dict(version="s07-zero-singleton-bundle-v1", possible_cost_modes=[[0, h], [h, 0]],
                cohort_size=1, hidden_modes=[1],
                target="One fixed synthetic row with no distribution over its two possible modes",
                logical_structure_id=native.structural_id(logical))
    data["source_identity"] = source.digest(data)
    result = dict(status="prepared", evidence="DEVELOPMENT constructed complementarity family",
                  contributor="ChatGPT (GPT-6 Astra Pro)", start_utc=datetime.now(timezone.utc).isoformat(),
                  implementation_sha256=native.sha(__file__),
                  dependencies={str(p.relative_to(HERE.parent)): native.sha(p)
                                for p in [HERE / "lattice_quotes.py", S06 / "source_anchor.py",
                                          S06 / "anchor_quotes.py", S06 / "contract_quote.py",
                                          S06 / "contract_guard.py", S06 / "joint_repair.py"]},
                  logical_source=logical, declared_cost_source=data,
                  price=price, tolerance=tolerance,
                  initial_candidate_models=[3], actual_audits=[], actual_logical_calls=[])

    def save():
        output.write_text(json.dumps(jsonable(result), indent=2) + "\n")

    save()  # Source and intended initial evidence fixed before any acquisition.
    oracle = jr.CostOracle(data)
    costs = jr.CostState(data["possible_cost_modes"], 1, data["source_identity"], meter)
    admission = contract_guard.admit()
    # This is new paid initial logical evidence, not a reused historical status.
    # Its q=(2,2), b=0 answer also exercises an actual non-unit-gcd negative cut.
    initial = cq.execute_complete(logical, 0)
    assert initial["provider_response"]["status"] == "UNSAT"
    result["actual_logical_calls"].append(dict(role="initial_lower", checked_call=initial))
    save()
    # Readmit the raw proof and initial feasible witness into this scalar bank.
    source.check_negative(logical, 0, initial["provider_response"]["proof"], meter)
    leaves = raw.compile_tree(initial["provider_response"]["proof"], meter)
    lowers = [min(sum(mode[j] for j in range(costs.m) if mask & (1 << j)) for mask in leaves)
              for mode in costs.modes]
    meter.pay("anchor_admission", "checked_tree_evaluation_at_mode_anchors",
              len(costs.modes) * len(leaves) * (2 * costs.m + 1) + len(lowers))
    witness = raw.compile_witness(logical, 3, meter)
    masks = [witness["violation_mask"]]
    assert masks == [3] and lowers == [0, 0]
    before = aq.best(masks, costs.modes, costs.possible, lowers, price, meter)
    audits = [aq.audit_quote(masks, costs.modes, costs.possible, lowers, price, 0, j, meter)
              for j in range(costs.m)]
    assert before["bound"] == h and all(a["guaranteed_gain"] == 0 for a in audits)
    # Each of these illustrative logical singletons has zero gain. The note's
    # endpoint argument covers every possible logical purchase, not just this menu.
    singles = [lq.quote(masks, costs.modes, costs.possible, lowers, price, q, 0, meter)
               for q in ([0, h], [h, 0], [h, h], [1, 1])]
    assert all(v["guaranteed_gain"] == 0 for v in singles)
    branches = []
    for outcome in audits[0]["outcomes"]:
        possible = [outcome["remaining_modes"]]
        assert len(possible[0]) == 1
        q = list(costs.modes[possible[0][0]])
        plan = lq.closing_query(masks, costs.modes, possible, lowers, price,
                                q, tolerance, meter, exact_interval=True)
        assert plan["closes"] and plan["canonical_budget"] == 0
        legacy = aq.logical_quote(masks, costs.modes, possible, lowers, price,
                                  q, 0, meter, complete=True)
        capped = lq.quote(masks, costs.modes, possible, lowers, price,
                          q, 0, meter, complete=False)
        assert legacy["worst_bound"] == 1
        assert capped["worst_bound"] == h and capped["guaranteed_gain"] == 0
        weighted = native.weighted_instance(logical, q)
        provider_quote = cq.finite_call_quote(weighted)
        meter.pay("bundle_quote", "source_weight_copy_and_finite_tariff_arithmetic", 2 * costs.m + 48)
        branches.append(dict(observed_value=outcome["value"], possible_modes=possible,
                             child_query=plan, old_unit_step_quote=legacy,
                             interrupted_quote=capped, complete_provider_quote=provider_quote))
    assert max(v["child_query"]["quote"]["worst_bound"] for v in branches) == 0
    result.update(status="bundle_quoted", initial_checked_witness=witness,
                  initial_anchor_lowers=lowers, before=before, audit_singletons=audits,
                  illustrative_logical_singletons=singles, bundle_branches=branches,
                  bundle_worst_bound=0, bundle_guaranteed_gain=h,
                  complete_provider_code_admission=admission,
                  nominal_initial_negative_lattice_lower=h,
                  nominal_initial_negative_raw_lower=initial["checked_lower"])
    save()
    observation = oracle.audit(0, 0)
    costs.observe(observation)
    result["actual_audits"].append(observation)
    chosen = next(v for v in branches if v["observed_value"] == observation["value"])
    result["selected_branch_observed_value"] = observation["value"]
    save()
    q = chosen["child_query"]["weights"]
    budget = chosen["child_query"]["canonical_budget"]
    weighted = native.weighted_instance(logical, q)
    meter.pay("objective_update", "weighted_source_copy", 2 * costs.m + 8)
    got = cq.execute_complete(weighted, budget)
    result["actual_logical_calls"].append(dict(role="selected_child", checked_call=got))
    save()
    if got["provider_response"]["status"] == "SAT":
        new = raw.compile_witness(logical, got["provider_response"]["model"], meter)
        masks.append(new["violation_mask"])
        result["new_structurally_bound_witness"] = new
    else:
        # The checked raw cut, plus the proved integer-lattice rounding, now
        # warrants this branch's anchor lower values on the unchanged structure.
        lowers = chosen["child_query"]["quote"]["UNSAT_anchor_lowers"]
    after = aq.best(masks, costs.modes, costs.possible, lowers, price, meter)
    assert after["bound"] == 0
    reconstruction = arithmetic_checks(meter)
    wrapper_units = sum(v["checked_call"]["total_operation_units"] for v in result["actual_logical_calls"])
    declared_total = meter.total + wrapper_units + admission["declared_admission_units"] + 4
    result.update(status="complete", after=after, final_cost_state=costs.snapshot(),
                  reconstruction_checks=reconstruction,
                  summary=dict(initial_bound=h, guaranteed_audit_singleton_gain=0,
                               guaranteed_any_logical_singleton_gain=0,
                               quoted_bundle_bound=0, actual_output_bound=after["bound"],
                               external_audits=1, initial_complete_calls=1,
                               child_complete_calls=1, new_native_or_LP_calls=0,
                               prospective_objective_mask_enumerations=0,
                               prospective_logical_truth_outcome_enumerations=0),
                  invoice=dict(controller_admission_and_reconstruction=meter.record(),
                               complete_call_wrapper_units=wrapper_units,
                               provider_code_admission_units=admission["declared_admission_units"],
                               audit_provider_software_units=4,
                               total_declared_software_units=declared_total,
                               external_audits=1, external_price=None,
                               reconstruction_included=True,
                               pricing="A + sigma*K_declared + rho*T_CPU + eta*S_recorded + R_other; A, conversion coefficients, and other implementation costs remain unassigned. No prospective CPU/wall bound or economic dominance."),
                  guarantee_resource_contract=dict(external_audits_max=1,
                      complete_child_calls_max=1,
                      complete_child_wrapper_units_max=max(v["complete_provider_quote"]["complete_wrapper_units"] for v in branches),
                      limitation="The finite provider's declared operation quote is prospective; full CPU, host, serialization and storage prices are not bounded by that quote."),
                  end_utc=datetime.now(timezone.utc).isoformat(),
                  timing=dict(process_ns=time.process_time_ns()-cpu, wall_ns=time.perf_counter_ns()-wall),
                  limitations="Only the initially supplied both-true action is admitted before purchases. An ordinary controller may propose and check other witnesses cheaply; this illustrative bundle is no advantage over such a stronger shared-access control. Exact source support is supplied, not population-learned.")
    save()
    print(json.dumps(jsonable(result["summary"] | dict(declared_units=declared_total,
                     actual_query_status=got["provider_response"]["status"],
                     actual_child_wrapper_units=got["total_operation_units"],
                     quoted_child_wrapper_max=result["guarantee_resource_contract"]["complete_child_wrapper_units_max"]))))


if __name__ == "__main__":
    run(Path(sys.argv[1]))
