"""Checked partition reuse after hard/soft clause changes. DEVELOPMENT.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. No solver or exact diagnostic calls.
Three fixed revisions of the already exposed eight-bit repair source.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time

import maxsat_repair as old

INPUT = Path(__file__).with_name("maxsat_repair_results.json")
PRICES = (3, 6, 9)


def frame(instance, name, hard, soft):
    result = dict(row=instance["row"], variables=instance["variables"],
                  original_source=instance["identity"], revision=name, hard=hard, soft=soft)
    result["identity"] = old.digest(result)
    return result


def revisions(instance):
    assert instance["variables"] == len(instance["soft"]) == 8
    assert [s["clause"] for s in instance["soft"]] == [[-j] for j in range(1, 9)]
    hard = [dict(id=f"h{j}", clause=list(c)) for j, c in enumerate(instance["hard"])]
    soft = [dict(id=f"s{j}:v0", clause=list(s["clause"]), weight=s["weight"])
            for j, s in enumerate(instance["soft"])]
    base = frame(instance, "base", hard, soft)
    dropped = hard[1:]
    first = frame(instance, "drop_first_hard", dropped, soft)
    changed = [dict(s) for s in soft]
    for j in (0, 4):
        changed[j] = dict(id=f"s{j}:v1", clause=[j+1], weight=soft[j]["weight"])
    second = frame(instance, "flip_soft_0_4", dropped, changed)
    lit = 8 if instance["public_incumbent"] & (1 << 7) else -8
    third = frame(instance, "pin_public_bit_7", dropped+[dict(id="h:new:7", clause=[lit])], changed)
    return base, first, second, third


def compile_partition(proof, n, meter):
    leaves, hard_dependencies = [], set()
    def visit(node, assigned, ones):
        meter.pay("partition_compile", "node_and_variable_domain_check", 4)
        if not isinstance(node, list) or not node:
            raise ValueError("Malformed partition node")
        if node[0] == "b" and len(node) == 4:
            variable = node[1]
            if type(variable) is not int or not 0 <= variable < n or assigned & (1 << variable):
                raise ValueError("Repeated or invalid split variable")
            bit = 1 << variable
            # Both children are compulsory, disjoint, and cover their parent.
            visit(node[2], assigned | bit, ones)
            visit(node[3], assigned | bit, ones | bit)
        elif node[0] in ("h", "w") and len(node) == 2:
            if node[0] == "h":
                hard_dependencies.add(node[1])
            leaves.append(dict(assigned=assigned, ones=ones, old_kind=node[0]))
            meter.pay("storage", "partition_cube_retained", 4)
        else:
            raise ValueError("Unknown partition node or missing branch")
    visit(proof, 0, 0)
    meter.pay("storage", "partition_domain_and_dependencies", 4+len(hard_dependencies))
    return leaves, sorted(hard_dependencies)


def partial_status(clause, assigned, ones, meter, category):
    meter.pay(category, "clause_header")
    satisfied, unknown = False, False
    for lit in clause:
        meter.pay(category, "complete_literal_inspection", 3)
        bit = 1 << (abs(lit)-1)
        if not assigned & bit:
            unknown = True
        elif bool(ones & bit) == (lit > 0):
            satisfied = True
    return True if satisfied else None if unknown else False


class Transport:
    def __init__(self, data):
        self.meter, self.scalar_meter = old.Meter(), old.Meter()
        self.archive, self.cache, self.last_leaf_states = [], {}, {}
        arm = next(a for a in data["arms"] if a["mode"] == "conventional_requested_value")
        for row, instance in enumerate(data["instances"]):
            assert instance["row"] == row
            if old.digest({k:v for k,v in instance.items() if k != "identity"}) != instance["identity"]:
                raise ValueError("Original source identity changed")
            self.meter.pay("archive", "original_source_identity", 8+sum(1+len(c) for c in instance["hard"]))
            events = [e for e in arm["events"] if e["row"] == row]
            models = {instance["public_incumbent"]}
            partitions = []
            for event in events:
                self.meter.pay("archive", "old_receipt_identity", 5)
                if event["source_identity"] != instance["identity"]:
                    raise ValueError("Old receipt has another source")
                if event["status"] == "SAT":
                    models.add(event["model"])
                elif event["status"] == "UNSAT":
                    old.check_negative(instance, event["budget"], event["proof"], self.meter)
                    leaves, dependencies = compile_partition(event["proof"], instance["variables"], self.meter)
                    partitions.append(dict(id=old.digest([instance["identity"], event["budget"], event["proof"]]),
                                           old_budget=event["budget"], leaves=leaves,
                                           hard_dependencies=dependencies))
            if not partitions:
                partitions = [dict(id="universal-root", old_budget=None, hard_dependencies=[],
                                   leaves=[dict(assigned=0, ones=0, old_kind="root")])]
                self.meter.pay("partition_compile", "universal_root_partition", 5)
            self.meter.pay("storage", "archive_models_and_row", len(models)+8)
            self.archive.append(dict(instance=instance, models=sorted(models), partitions=partitions,
                                     old_lower=arm["final_state"][row]["lower"]))
        self.setup = self.meter.record()

    def validate_frame(self, current):
        meter = self.meter
        meter.pay("current_source", "frame_identity_and_variable_map", 10)
        if old.digest({k:v for k,v in current.items() if k != "identity"}) != current["identity"]:
            raise ValueError("Current clause payload does not match identity")
        archive = self.archive[current["row"]]
        instance = archive["instance"]
        if (current["variables"], current["original_source"]) != (instance["variables"], instance["identity"]):
            raise ValueError("Partition variable map or original source changed")
        for category in ("hard", "soft"):
            seen = set()
            for record in current[category]:
                meter.pay("current_source", "clause_identity_and_header", 3)
                if record["id"] in seen:
                    raise ValueError("Duplicate current clause identity")
                seen.add(record["id"])
                for lit in record["clause"]:
                    meter.pay("current_source", "literal_domain_check")
                    if type(lit) is not int or lit == 0 or abs(lit) > current["variables"]:
                        raise ValueError("Clause literal outside fixed variable universe")
                if category == "soft":
                    meter.pay("current_source", "nonnegative_weight_check")
                    if type(record["weight"]) is not int or record["weight"] < 0:
                        raise ValueError("Negative or noninteger current weight")
        return archive

    def scalar_bound(self, archive, current):
        """Ordinary dependency-filtered scalar transport, not warm IHS."""
        meter = self.scalar_meter
        old_instance = archive["instance"]
        if len(current["soft"]) != len(old_instance["soft"]):
            return 0, []
        delta = 0
        for before, after in zip(old_instance["soft"], current["soft"]):
            meter.pay("scalar", "soft_semantics_and_worst_delta", 4+len(before["clause"])+len(after["clause"]))
            delta += min(0, after["weight"]-before["weight"]) if before["clause"] == after["clause"] else -before["weight"]
        values = []
        for partition in archive["partitions"]:
            if partition["old_budget"] is None:
                continue
            survives = True
            for dep in partition["hard_dependencies"]:
                wanted = old_instance["hard"][dep]
                found = False
                for hard in current["hard"]:
                    meter.pay("scalar", "hard_dependency_content_match", 1+len(wanted)+len(hard["clause"]))
                    if wanted == hard["clause"]:
                        found = True
                        break
                if not found:
                    survives = False
                    break
            bound = max(0, partition["old_budget"]+1+delta) if survives else 0
            meter.pay("scalar", "transported_scalar_and_maximum", 3)
            values.append(dict(partition=partition["id"], dependencies_survive=survives, lower=bound))
        return max((v["lower"] for v in values), default=0), values

    def evaluate(self, current):
        wall, cpu = time.perf_counter_ns(), time.process_time_ns()
        before, scalar_before = self.meter.total, self.scalar_meter.total
        archive = self.validate_frame(current)
        key = current["row"], current["identity"]
        if key in self.cache:
            self.meter.pay("cache", "checked_current_frame_receipt", 8)
            return self.cache[key]
        meter = self.meter
        witness_events = []
        upper, winner = None, None
        n = current["variables"]
        for model in archive["models"]:
            meter.pay("witness", "assignment_domain_check", 3)
            if type(model) is not int or not 0 <= model < 1 << n:
                raise ValueError("Retained assignment outside variable universe")
            failed = [h["id"] for h in current["hard"]
                      if partial_status(h["clause"], (1 << n)-1, model, meter, "witness") is False]
            cost = 0
            for soft in current["soft"]:
                if partial_status(soft["clause"], (1 << n)-1, model, meter, "witness") is False:
                    cost += soft["weight"]
                    meter.pay("witness", "new_objective_add")
            feasible = not failed
            if feasible and (upper is None or cost < upper):
                upper, winner = cost, model
            meter.pay("storage", "current_witness_check", 5+len(failed))
            witness_events.append(dict(model=model, failed_hard=failed, current_cost=cost, feasible=feasible))
        partition_events = []
        old_reopened = newly_reopened = newly_closed = 0
        hard_unsat = False
        lower = 0
        for partition in archive["partitions"]:
            leaf_events, candidate_costs = [], []
            for index, cube in enumerate(partition["leaves"]):
                meter.pay("leaf", "cube_source_and_assignment_words", 5)
                conflicts = [h["id"] for h in current["hard"]
                             if partial_status(h["clause"], cube["assigned"], cube["ones"], meter, "leaf") is False]
                forced, cost = [], 0
                for j, soft in enumerate(current["soft"]):
                    if partial_status(soft["clause"], cube["assigned"], cube["ones"], meter, "leaf") is False:
                        forced.append(j)
                        cost += soft["weight"]
                        meter.pay("leaf", "forced_current_soft_cost", 2)
                excluded = bool(conflicts)
                history_key = current["row"], partition["id"], index
                previous = self.last_leaf_states.get(history_key)
                old_reopened += cube["old_kind"] == "h" and not excluded
                newly_reopened += previous is True and not excluded
                newly_closed += previous is False and excluded
                self.last_leaf_states[history_key] = excluded
                if not excluded:
                    candidate_costs.append(cost)
                meter.pay("storage", "current_leaf_incidence_and_bound", 8+len(conflicts)+len(forced))
                leaf_events.append(dict(cube=index, assigned=cube["assigned"], ones=cube["ones"],
                                        old_kind=cube["old_kind"], excluded=excluded,
                                        current_hard_conflicts=conflicts,
                                        forced_current_soft_indices=forced, current_lower=cost))
            bound = min(candidate_costs) if candidate_costs else None
            meter.pay("assessment", "partition_minimum_and_maximum", len(candidate_costs)+2)
            if bound is None:
                hard_unsat = True
            else:
                lower = max(lower, bound)
            partition_events.append(dict(id=partition["id"], lower=bound,
                                         hard_unsat=bound is None, leaves=leaf_events))
        scalar, scalar_events = self.scalar_bound(archive, current)
        if hard_unsat:
            assert upper is None
            lower = None
        else:
            assert lower >= scalar
            if upper is not None:
                assert lower <= upper
        status = "hard_unsat" if hard_unsat else "no_retained_witness" if upper is None else "exact" if lower == upper else "bounded"
        result = dict(row=current["row"], source_identity=current["identity"], revision=current["revision"],
                      status=status, lower=lower, upper=upper, chosen_witness=winner,
                      scalar_lower=scalar, scalar_transports=scalar_events,
                      old_lower=archive["old_lower"],
                      old_numeric_lower_contradicted_by_current_witness=upper is not None and upper < archive["old_lower"],
                      old_hard_leaf_occurrences_reopened=old_reopened,
                      newly_reopened_leaf_occurrences=newly_reopened,
                      newly_excluded_leaf_occurrences=newly_closed,
                      invalidated_witnesses=sum(not w["feasible"] for w in witness_events),
                      witnesses=witness_events, partitions=partition_events,
                      current_check_units=meter.total-before, scalar_check_units=self.scalar_meter.total-scalar_before,
                      process_ns=time.process_time_ns()-cpu, wall_ns=time.perf_counter_ns()-wall)
        self.cache[key] = result
        return result

    def value(self, row, source_identity, price):
        self.meter.pay("value", "source_bound_receipt_lookup", 5)
        receipt = self.cache[row, source_identity]
        self.meter.pay("value", "replacement_and_witness_action_regret", 8)
        if receipt["status"] == "hard_unsat":
            return dict(price=price, action="replace", action_cost=price, regret_upper=0)
        upper, lower = receipt["upper"], receipt["lower"]
        action_cost = price if upper is None else min(upper, price)
        return dict(price=price, action="repair" if upper is not None and upper < price else "replace",
                    action_cost=action_cost, regret_upper=action_cost-min(lower, price),
                    scalar_regret_upper=action_cost-min(receipt["scalar_lower"], price))


def semantic_smoke():
    instance = dict(row=0, variables=3, hard=[[1], [2, 3]],
                    soft=[dict(clause=[-j], weight=w) for j,w in enumerate((2,3,4),1)],
                    public_incumbent=3, objective_max=9)
    instance["identity"] = old.digest(instance)
    proof = ["b",0,["h",0],["b",1,["b",2,["h",1],["w",[0,2]]],["w",[0,1]]]]
    event = dict(row=0, source_identity=instance["identity"], status="UNSAT", budget=4, proof=proof)
    data = dict(instances=[instance], arms=[dict(mode="conventional_requested_value", events=[event], final_state=[dict(lower=5)])])
    service = Transport(data)
    changed = frame(instance, "smoke_remove_requirement_and_flip_preference",
                    [dict(id="h1", clause=[2,3])],
                    [dict(id=f"s{j}:new", clause=c, weight=w) for j,(c,w) in enumerate((([1],2),([-2],3),([-3],4)))])
    got = service.evaluate(changed)
    assert (got["lower"], got["upper"], got["old_hard_leaf_occurrences_reopened"]) == (2,3,1)
    assert got["old_numeric_lower_contradicted_by_current_witness"]
    before = service.meter.total
    assert service.evaluate(changed) is got
    cache_units = service.meter.total-before
    return dict(instance=instance, original_budget=4, original_proof=proof, current=changed,
                receipt=got, cache_hit_units=cache_units,
                invoice=service.meter.record(), scalar_invoice=service.scalar_meter.record(),
                scope="Three-variable checked illustration; no provider call or assignment enumeration")


def main(destination):
    if destination.exists():
        raise FileExistsError("Preserve prior changed-clause transport exposure")
    start, cpu = time.perf_counter_ns(), time.process_time_ns()
    data = json.loads(INPUT.read_text())
    if data["status"] != "complete" or old.digest(data["instances"]) != data["source_identity"]:
        raise ValueError("Incomplete or changed original source")
    if hashlib.sha256(Path(old.__file__).read_bytes()).hexdigest() != data["implementation_sha256"]:
        raise ValueError("Original checker implementation changed")
    current_frames = [revisions(i) for i in data["instances"]]
    result = dict(status="running", evidence="DEVELOPMENT", contributor="ChatGPT (GPT-6 Astra Pro)",
                  start_utc=datetime.now(timezone.utc).isoformat(), command=sys.argv,
                  implementation_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  input_result_sha256=hashlib.sha256(INPUT.read_bytes()).hexdigest(),
                  original_source_identity=data["source_identity"],
                  recipe="Delete first canonical hard clause; flip unit soft preferences 0 and 4; add hard unit fixing variable index 7 to its already public incumbent bit. Same fixed edits on all 16 exposed rows.",
                  new_solver_calls=0, exact_diagnostic_calls=0,
                  tariff="Named source, clause/literal, proof-node, arithmetic, storage and output operations. Full current hard and soft scans at every leaf and witness. Scalar comparator work separately invoiced. Hashing/JSON harness time is included in process/wall, not a complete machine-instruction tariff.",
                  frames=current_frames, stages=[])
    def save():
        destination.write_text(json.dumps(result, separators=(",", ":"))+"\n")
    save()
    result["semantic_smoke"] = semantic_smoke()
    service = Transport(data)
    result["archive"] = service.archive
    result["archive_setup_invoice"] = service.setup
    previous_lower = [a["old_lower"] for a in service.archive]
    for stage in range(4):
        rows = []
        for row, frames in enumerate(current_frames):
            receipt = service.evaluate(frames[stage])
            receipt["prices"] = [service.value(row, frames[stage]["identity"], p) for p in PRICES]
            # Repeating a value request consumes its checked source-bound cache.
            assert service.value(row, frames[stage]["identity"], 6) == receipt["prices"][1]
            receipt["reported_lower_drop"] = max(0, previous_lower[row]-receipt["lower"])
            previous_lower[row] = receipt["lower"]
            assert receipt["upper"] is not None  # The public witness survives these fixed edits.
            rows.append(receipt)
        summary = dict(positive_lower_rows=sum(r["lower"] > 0 for r in rows),
                       exact_rows=sum(r["status"] == "exact" for r in rows),
                       strict_over_dependency_scalar=sum(r["lower"] > r["scalar_lower"] for r in rows),
                       old_hard_leaf_occurrences_reopened=sum(r["old_hard_leaf_occurrences_reopened"] for r in rows),
                       newly_reopened_leaf_occurrences=sum(r["newly_reopened_leaf_occurrences"] for r in rows),
                       invalidated_witnesses=sum(r["invalidated_witnesses"] for r in rows),
                       old_numerical_lower_contradictions=sum(r["old_numeric_lower_contradicted_by_current_witness"] for r in rows),
                       lower_drops=sum(r["reported_lower_drop"] > 0 for r in rows),
                       cohort_mean_price6_regret=sum(r["prices"][1]["regret_upper"] for r in rows)/len(rows),
                       cumulative_partition_units=service.meter.total,
                       cumulative_scalar_units=service.scalar_meter.total)
        result["stages"].append(dict(stage=stage, revision=current_frames[0][stage]["revision"],
                                     rows=rows, summary=summary, partition_invoice=service.meter.record(),
                                     scalar_invoice=service.scalar_meter.record()))
        save()
        print(json.dumps(dict(stage=stage, revision=current_frames[0][stage]["revision"], **summary)), flush=True)
    result.update(status="complete", end_utc=datetime.now(timezone.utc).isoformat(),
                  process_ns=time.process_time_ns()-cpu, wall_ns=time.perf_counter_ns()-start,
                  checks=dict(all_current_bounds_have_checked_feasible_uppers=True,
                              all_partitions_cover_the_unchanged_boolean_universe=True,
                              current_leaf_bounds_dominate_dependency_scalar=True,
                              repeated_value_requests_match=True,
                              no_solver_or_exact_diagnostic=True))
    save()


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name("partition_transport_results.json"))
