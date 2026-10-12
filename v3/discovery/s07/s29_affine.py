#!/usr/bin/env python3
"""S29: source-proved affine cost shifts and checked scalar transport.

DEVELOPMENT. ChatGPT (GPT-6 Astra Pro), 2026-10-12. This compact constructor
supports one exactly-one group of atomic soft violations and arbitrary extra
hard constraints. It does not alter the executed S28 service or quotations.
"""
import copy
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
from vertex_probe import jsonable
sys.path.insert(0, str(HERE))
import row_margins

source, raw = cq.source, cq.compilation


def structure_id(instance):
    return source.digest(dict(variables=instance["variables"], hard=instance["hard"],
                              soft_clauses=[s["clause"] for s in instance["soft"]]))


def admit_exactly_one(instance, meter):
    """Verify the exact raw clauses and the polarity of every atomic violation.

    A soft clause [literal] is violated when -literal is true. The checked
    at-least-one hard clause and all pair exclusions prove sum(z)=1. Extra
    hard constraints can restrict this simplex further and remain untouched.
    """
    if instance.get("identity") != source.digest({k: v for k, v in instance.items() if k != "identity"}):
        raise ValueError("Original source identity changed")
    n = instance["variables"]
    if type(n) is not int or n < 1 or not instance["soft"]:
        raise ValueError("Nonempty finite atomic objective required")
    if any(len(s["clause"]) != 1 for s in instance["soft"]):
        raise ValueError("This checker supports atomic soft clauses only")
    violations = [-s["clause"][0] for s in instance["soft"]]
    if any(type(v) is not int or not 1 <= abs(v) <= n for v in violations):
        raise ValueError("Invalid atomic violation literal")
    if len({abs(v) for v in violations}) != len(violations):
        raise ValueError("Distinct atomic variables required by this compact checker")
    clauses = {}
    for i, clause in enumerate(instance["hard"]):
        if any(type(v) is not int or not 1 <= abs(v) <= n for v in clause):
            raise ValueError("Invalid hard source literal")
        clauses.setdefault(tuple(sorted(set(clause))), i)
    needed = [tuple(sorted(violations))]
    needed.extend(tuple(sorted((-a, -b))) for i, a in enumerate(violations) for b in violations[i + 1:])
    meter.pay("source_geometry_check", "raw_clause_index_and_exact_violation_polarities",
              sum(2 + 3 * len(c) for c in instance["hard"]) + 5 * len(violations) + 3 * len(needed) + 12)
    if any(clause not in clauses for clause in needed):
        raise ValueError("Missing source clause for exactly-one violation semantics")
    receipt = dict(kind="checked_atomic_exactly_one_v1", original_source_identity=instance["identity"],
                   structure_identity=structure_id(instance), ordered_violation_literals=violations,
                   raw_clause_indices=[clauses[c] for c in needed],
                   relaxation="z>=0; sum(z)=1 contains every feasible Boolean violation vector")
    receipt["receipt_id"] = source.digest(receipt)
    return receipt


def reconstruct_transport(instance, negative, geometry, target, meter):
    """Reconstruct a scalar certificate from actual source and raw proof bytes.

    No constraint is imposed on the old proof's abstract leaf masks. Its
    checked scalar q-lower and source-feasible simplex imply the new lower.
    """
    expected = admit_exactly_one(instance, meter)
    if expected != geometry:
        raise ValueError("Geometry receipt does not bind the supplied source")
    if negative.get("receipt_id") != source.digest({k: v for k, v in negative.items() if k != "receipt_id"}):
        raise ValueError("Raw negative receipt identity changed")
    if negative["source_id"] != source.digest(instance) or negative["provider_response"]["status"] != "UNSAT":
        raise ValueError("Wrong logical source or no checked negative answer")
    source.check_negative(instance, negative["budget"], negative["provider_response"]["proof"], meter)
    q = [s["weight"] for s in instance["soft"]]
    target = list(map(F, target))
    if len(target) != len(q) or any(v < 0 for v in target):
        raise ValueError("Same ordered nonnegative target objective required")
    lower = negative["budget"] + 1
    difference = [v - w for v, w in zip(target, q)]
    support_minimum = min(difference)
    transported = max(F(0), lower + support_minimum)
    meter.pay("source_scalar_transport", "signed_simplex_minimum_and_nonnegative_lower", 4 * len(q) + 8)
    receipt = dict(kind="source_feasible_simplex_scalar_transport_v1",
                   original_source_identity=instance["identity"], structure_identity=structure_id(instance),
                   original_query=q, target_weights=target, checked_point_lower=lower,
                   signed_displacement=difference, simplex_support_minimum=support_minimum,
                   target_scalar_lower=transported, geometry_receipt_id=geometry["receipt_id"],
                   raw_negative_receipt_id=negative["receipt_id"],
                   justification="For every feasible z, target.z=q.z+(target-q).z >= Lq+min(simplex,(target-q).z). Zero clamp uses nonnegative target weights.")
    # Fractions are serialized exactly before hashing the explanatory receipt.
    receipt = jsonable(receipt)
    receipt["receipt_id"] = source.digest(receipt)
    return transported, receipt


def common_shift(q, target, meter):
    difference = [F(v) - F(w) for v, w in zip(target, q)]
    meter.pay("source_affine_check", "common_shift_comparison", 3 * len(q) + 2)
    if len(target) != len(q) or not difference or any(v != difference[0] for v in difference):
        raise ValueError("Displacement is not a common affine shift for this exactly-one source")
    return difference[0]


def make_source(m=4, a=3):
    violations = [j + 1 if j % 2 == 0 else -(j + 1) for j in range(m)]
    hard = [violations]
    hard += [[-u, -v] for j, u in enumerate(violations) for v in violations[j + 1:]]
    hard += [[-violations[0]]]  # Additional source constraint removes cheapest simplex vertex.
    selected = 1
    model = sum(1 << j for j, literal in enumerate(violations)
                if ((j == selected) if literal > 0 else (j != selected)))
    instance = dict(row="s29-affine-shift", variables=m, hard=hard,
                    soft=[dict(weight=a + j, clause=[-literal]) for j, literal in enumerate(violations)],
                    public_incumbent=model, objective_max=sum(a + j for j in range(m)))
    instance["identity"] = source.digest(instance)
    return instance


def run(output):
    if output.exists():
        raise FileExistsError("Preserve the actual acquired proof")
    wall, cpu = time.perf_counter_ns(), time.process_time_ns()
    meter = source.Meter()
    instance = make_source()
    q = [s["weight"] for s in instance["soft"]]
    shifts = [-2, 2]
    modes = [[v + theta for v in q] for theta in shifts]
    cost_contract = dict(cohort_size=1, possible_cost_modes=modes, hidden_modes=[1],
                         logical_structure_id=structure_id(instance),
                         interpretation="Fixed synthetic source; no mode law, observations or learned population guarantee")
    cost_contract["source_identity"] = source.digest(cost_contract)
    result = dict(status="prepared", candidate="S29 source-proved affine cost invariance",
                  evidence="DEVELOPMENT separate generative branch from S28-B1",
                  contributor="ChatGPT (GPT-6 Astra Pro)", start_utc=datetime.now(timezone.utc).isoformat(),
                  implementation_sha256=cq.sha(__file__),
                  dependencies={p.name: cq.sha(p) for p in [S06 / "contract_quote.py", S06 / "contract_guard.py",
                                S06 / "source_anchor.py", S06 / "anchor_quotes.py", HERE / "row_margins.py"]},
                  logical_source=instance, cost_source=cost_contract,
                  actual_audits=0, actual_native_or_LP_calls=0, actual_complete_calls=0)

    def save():
        output.write_text(json.dumps(jsonable(result), indent=2) + "\n")

    save()
    code_admission = contract_guard.admit()
    geometry = admit_exactly_one(instance, meter)
    witness = raw.compile_witness(instance, instance["public_incumbent"], meter)
    upper = witness["original_cost"]
    negative = cq.execute_complete(instance, upper - 1)
    assert negative["provider_response"]["status"] == "UNSAT"
    result.update(status="point_proof_acquired", actual_complete_calls=1,
                  actual_paid_point_proof=negative, nominal_checked_witness=witness,
                  source_geometry_receipt=geometry, code_admission=code_admission)
    save()
    lower = negative["checked_lower"]
    assert lower == upper == 4
    transported, receipts = [], []
    for mode, theta in zip(modes, shifts):
        assert common_shift(q, mode, meter) == theta
        ell, receipt = reconstruct_transport(instance, negative, geometry, mode, meter)
        transported.append(ell)
        receipts.append(receipt)
    generic = [max(0, lower - sum(max(0, x - y) for x, y in zip(q, mode))) for mode in modes]
    meter.pay("comparison", "generic_boolean_displacement_lower", 4 * len(q) * len(modes))
    own_tree_lowers = [min(sum(mode[j] for j in range(len(q)) if mask & (1 << j))
                            for mask in negative["leaf_masks"]) for mode in modes]
    meter.pay("comparison", "same_paid_tree_revaluation", len(modes) * len(negative["leaf_masks"]) * (2 * len(q) + 1))
    assert list(transported) == own_tree_lowers == [2, 6]
    geometric_point_lower = min(q)
    assert geometric_point_lower == 3 < lower
    row = row_margins.margins(modes, [[0, 1]], q, meter)
    assert row["alpha"] == row["delta"] == 8
    exact_one_alpha = max(F(0), *(max(F(v) - w for v, w in zip(mode, q)) for mode in modes))
    exact_one_delta = max(F(0), *(max(w - F(v) for v, w in zip(mode, q)) for mode in modes))
    meter.pay("comparison", "simplex_signed_upper_margins", 4 * len(q) * len(modes))
    assert exact_one_alpha == exact_one_delta == 2
    prices = []
    masks = [witness["violation_mask"]]
    for price in (7, 5, 1):
        before = aq.best(masks, modes, [[0, 1]], generic, price, meter)
        after = aq.best(masks, modes, [[0, 1]], transported, price, meter)
        repair = max(0, upper - lower, upper + max(shifts) - price)
        replacement = max(0, price - max(0, lower + min(shifts)))
        assert after["bound"] == min(repair, replacement)
        prices.append(dict(price=price, generic_transport=before,
                           source_aware_transport=after,
                           affine_repair_bound=repair, affine_replacement_bound=replacement))
    assert prices[0]["generic_transport"]["bound"] == 2 and prices[0]["source_aware_transport"]["bound"] == 0
    assert prices[1]["affine_repair_bound"] == 1 and prices[1]["affine_replacement_bound"] == 3
    assert prices[2]["source_aware_transport"]["bound"] == 0
    # Negative examples are cheap checker controls, not new solver exposures.
    controls = []
    changed = copy.deepcopy(instance)
    changed["soft"][2]["clause"][0] *= -1
    changed["identity"] = source.digest({k: v for k, v in changed.items() if k != "identity"})
    missing = copy.deepcopy(instance)
    missing["hard"].remove([2, -3])
    missing["identity"] = source.digest({k: v for k, v in missing.items() if k != "identity"})
    for name, bad in [("wrong_atomic_polarity", changed), ("missing_pair_exclusion", missing)]:
        try:
            admit_exactly_one(bad, meter)
        except ValueError as error:
            controls.append(dict(case=name, rejected=True, reason=str(error)))
        else:
            raise AssertionError("Invalid source geometry was admitted")
    try:
        common_shift(q, [q[0] + 1, q[1] - 1] + q[2:], meter)
    except ValueError as error:
        controls.append(dict(case="nonaffine_cost_change", rejected=True, reason=str(error)))
    else:
        raise AssertionError("Nonaffine shift admitted as common")
    total = meter.total + negative["total_operation_units"] + code_admission["declared_admission_units"]
    result.update(status="complete", scalar_transport_receipts=receipts,
                  checked_point_interval=[lower, upper], nominal_simplex_only_lower=geometric_point_lower,
                  generic_boolean_anchor_lowers=generic, source_aware_anchor_lowers=transported,
                  same_paid_tree_anchor_lowers=own_tree_lowers, row_correlation_margins=row,
                  feasible_simplex_margins=dict(alpha=exact_one_alpha, delta=exact_one_delta),
                  common_shift_range=[min(shifts), max(shifts)], price_cases=prices,
                  negative_controls=controls,
                  summary=dict(generic_anchor_bound_at_price7=2, source_aware_bound_at_price7=0,
                               replacement_sensitive_bound_at_price5=1,
                               row_margin_sum=16, simplex_margin_sum=4,
                               affine_repair_comparison_uncertainty=0,
                               actual_complete_calls=1, actual_observations=0,
                               new_LP_or_native_calls=0, new_logical_model_enumerations=0,
                               matches_same_paid_tree_in_this_example=True),
                  invoice=dict(local_operations=meter.record(), complete_wrapper_units=negative["total_operation_units"],
                               provider_code_admission_units=code_admission["declared_admission_units"],
                               total_declared_units=total,
                               scope="All example checks included. Source support is a declared synthetic contract. CPU/storage/serialization and economic conversions are separately unpriced."),
                  end_utc=datetime.now(timezone.utc).isoformat(),
                  timing=dict(process_ns=time.process_time_ns()-cpu, wall_ns=time.perf_counter_ns()-wall),
                  limitations="The ordinary simplex/robust method receives the same source constraint. Full retained-tree revaluation already matches these bounds on this small family. No advantage over those controls, broad transfer or S28-B1 confirmation is established.")
    save()
    print(json.dumps(jsonable(result["summary"] | dict(total_declared_units=total))))


if __name__ == "__main__":
    run(Path(sys.argv[1]))
