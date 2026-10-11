"""Supplemental independent arithmetic reconstruction of sealed P3-10 paths.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11.
No frozen module, generator, paid method, reporter or private scorer is imported.
The observer reads a completed experiment and produces no replacement result.
Its use of the specified MT seed reconstructs the recorded finite bit string;
it is neither another paid execution nor evidence of independent fair bits.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import argparse
import hashlib
import json
import random
import time
import traceback

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
FINAL = REPO / "v3/experiments/final_v1_amended_A1"
from amended_lineage_reader import Lineage
LINEAGE = None
CHECKS = Counter()


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def require(condition, name, detail):
    CHECKS[name] += 1
    if not condition:
        raise AssertionError(f"{name}: {detail}")


def rat(value):
    return F(*value) if isinstance(value, (list, tuple)) else F(value)


def pair(value):
    value = F(value)
    return [value.numerator, value.denominator]


def sealed(stage, identifier):
    require(LINEAGE is not None, "amended_lineage_barrier", identifier)
    return LINEAGE.record(stage, identifier)

def syntax_advice(query):
    clauses, n = query["clauses"], query["variables"]
    positive = {x for c in clauses for x in c if x > 0}
    negative = {-x for c in clauses for x in c if x < 0}
    pos_units = {c[0] for c in clauses if len(c) == 1 and c[0] > 0}
    neg_units = {-c[0] for c in clauses if len(c) == 1 and c[0] < 0}
    pure = (positive - negative) | {-x for x in negative - positive}
    return [0, 1, int(len(clauses) <= 3 * n), int(not (pos_units & neg_units)),
            int(all(any(x in pure for x in c) for c in clauses)),
            int(sum(x > 0 for c in clauses for x in c) >= sum(x < 0 for c in clauses for x in c))]


def key(query):
    return canonical([query["semantics_version"], query["source_version"],
                      query["variables"], query["clauses"]])


def proxy(query):
    literals = sum(map(len, query["clauses"]))
    words = (4 + max(1, (len(query["semantics_version"]) + 7) // 8)
             + max(1, (len(query["source_version"]) + 7) // 8)
             + len(query["clauses"]) + literals)
    return 128 + words + (1 << query["variables"]) * max(1, literals)


@lru_cache(None)
def coordinate_masks(n):
    return tuple(sum(1 << a for a in range(1 << n) if a & (1 << i)) for i in range(n))


def truth(query):
    """Independent bit-parallel truth table, unlike the scalar private scorer."""
    masks = coordinate_masks(query["variables"])
    full = (1 << (1 << query["variables"])) - 1
    satisfying = full
    for clause in query["clauses"]:
        disjunction = 0
        for literal in clause:
            variable = masks[abs(literal) - 1]
            disjunction |= variable if literal > 0 else full ^ variable
        satisfying &= disjunction
    return int(bool(satisfying))


def fixed_mass(products, n, state_bits):
    mass = n << state_bits
    ideals = [F((mass - n) * value, sum(products)) for value in products]
    result = [1 + value.numerator // value.denominator for value in ideals]
    residual = mass - sum(result)
    require(0 <= residual < n, "rounding_residual_range", residual)
    result = [value + int(index < residual) for index, value in enumerate(result)]
    require(sum(result) == mass and min(result) >= 1, "fixed_positive_mass", result)
    return result


def audit_episode(unit, paid, public, config):
    episode = paid["episode"]
    queries = public["queries"]
    whole = [s for s in unit["segments"] if s["name"] == "whole"]
    require(len(whole) == 1 and whole[0]["start"] == 0, "one_scheduled_whole_horizon", unit["id"])
    require(paid["unit"] == unit and len(queries) == whole[0]["stop"], "scheduled_paid_input_binding", unit["id"])
    if episode["status"] != "success":
        return {"unit_id": unit["id"], "group_id": unit["group_id"],
                "configuration_id": unit["configuration_id"], "status": "unavailable",
                "scheduled_horizon": whole[0]["stop"], "episode_status": episode["status"],
                "failure_detail": episode.get("failure_detail"), "counts": {}, "blocks": [],
                "reason": "No completed numerical trajectory; the scheduled denominator and failed service are retained."}
    rows, blocks = episode["trace"], episode["blocks"]
    contract = episode["contract"]
    expected_contract = {"version": "p308-program-broker-v1.2", "horizon": len(queries),
        "block_size": config["block_size"], "expert_count": 6,
        "action_bits": config["action_bits"], "state_bits": config["state_bits"],
        "selector": unit["parameters"]["selector"], "hard_capacity": config["hard_capacity"],
        "hard_index": "hashed" if unit["parameters"]["hard"] else "linear"}
    require(all(contract[k] == value for k, value in expected_contract.items())
            and episode["hard_enabled"] is unit["parameters"]["hard"], "frozen_numeric_contract", unit["id"])
    expected_scope = [queries[0]["semantics_version"], queries[0]["source_version"], "p309-" + unit["group_id"]]
    require(episode["scope"] == expected_scope and episode["hard_state"]["scope"] == expected_scope,
            "frozen_episode_scope", unit["id"])
    n, b, t = contract["expert_count"], contract["block_size"], contract["horizon"]
    action_bits, state_bits = contract["action_bits"], contract["state_bits"]
    denominator = 1 << action_bits
    mode = contract["selector"]
    selector_bits = (b - 1).bit_length() + int(mode == "tickets")
    bit_count = (t // b) * selector_bits + t * action_bits
    require(episode["status"] == "success" and len(rows) == len(queries) == t
            and len(blocks) == t // b, "complete_numeric_episode", unit["id"])
    rng = random.Random(unit["seed"])
    word_count = (bit_count + 63) // 64
    # One integer representation gives an independent bit-extraction route.
    bit_string = sum(rng.getrandbits(64) << (64 * i) for i in range(word_count))
    position = 0

    def bits(count):
        nonlocal position
        value = (bit_string >> position) & ((1 << count) - 1)
        position += count
        return value

    weights = [1 << state_bits] * n
    known, seen, detail = {}, set(), []
    counts = Counter()
    invoice_ids = [receipt["query_id"] for receipt in episode["invoices"]]
    require(len(invoice_ids) == len(set(invoice_ids)) == t // b, "distinct_complete_invoice_roster", unit["id"])
    require(invoice_ids == [row["query_id"] for row in rows if row["selected"]], "chronological_selected_invoice_roster", unit["id"])
    by_query = {receipt["query_id"]: receipt for receipt in episode["invoices"]}
    expected_provider = ("bounded_cnf_checked", "p308-bounded-cnf-services-v1.1") if unit["parameters"]["provider"] == "cold" else (
                         "owned_cached_cnf_receipt", "p308-selected-receipt-cache-v1.1")
    for block_index, recorded in enumerate(blocks):
        start = block_index * b
        qblock = queries[start:start + b]
        advice = [syntax_advice(q) for q in qblock]
        forecasts = [denominator * sum(w * a for w, a in zip(weights, acts)) // sum(weights)
                     for acts in advice]
        require(recorded["weights_before"] == weights, "block_weights_before", [unit["id"], block_index])
        favorite = 0 if mode == "uniform" else max(range(b), key=lambda j:
            F(forecasts[j] * (denominator - forecasts[j]), proxy(qblock[j])))
        ticket = bits(selector_bits)
        selected = ticket if mode == "uniform" or ticket < b else favorite
        multiplicity = 1 if mode == "uniform" or selected != favorite else b + 1
        propensities = [[1, b] if mode == "uniform" else [b + 1 if j == favorite else 1, 2 * b]
                        for j in range(b)]
        expected = dict(block=block_index, selected=selected, ticket=ticket,
                        favorite=favorite, multiplicity=multiplicity, propensities=propensities)
        require(all(recorded[k] == v for k, v in expected.items()), "selection_and_propensity", unit["id"])
        block_losses = []
        for j, query in enumerate(qblock):
            index, row = start + j, rows[start + j]
            qkey, y = key(query), truth(query)
            require(canonical(row["claim_key"]) == qkey and row["scope"] == expected_scope,
                    "full_row_key_and_scope", [unit["id"], index])
            fresh = qkey not in seen
            prior_known = episode["hard_enabled"] and qkey in known
            emitted = denominator * known[qkey] if prior_known else forecasts[j]
            draw = bits(action_bits)
            base_action, live_action = int(draw < forecasts[j]), int(draw < emitted)
            selected_here = j == selected
            label = None
            if selected_here:
                receipt = by_query[row["query_id"]]
                require(receipt["status"] == "success" and receipt["checked"] is True
                        and receipt["answer"] == y, "selected_checked_label", [unit["id"], index])
                require(canonical(receipt["claim_key"]) == qkey
                        and (receipt["provider"], receipt["provider_version"]) == expected_provider,
                        "full_receipt_key_and_provider", [unit["id"], index])
                label = receipt["answer"]
            base_terminal = label if selected_here else base_action
            terminal = label if selected_here else live_action
            expected_row = dict(index=index, block=block_index, query_id=query["query_id"], advice=advice[j],
                base_q=[forecasts[j], denominator], emitted_q=[emitted, denominator],
                base_action=base_action, prospective_action=live_action, base_terminal=base_terminal,
                terminal_action=terminal, selected=selected_here, propensity=propensities[j], purchased_label=label)
            require(all(row[k] == v for k, v in expected_row.items()), "full_numeric_row", [unit["id"], index])
            require(row["hard_before"] == ("checked" if prior_known else "unresolved"),
                    "prior_hard_chronology", [unit["id"], index])
            require(not fresh or not prior_known, "no_first_occurrence_hard_hit", [unit["id"], index])
            brier_base, brier_live = (F(forecasts[j], denominator) - y) ** 2, (F(emitted, denominator) - y) ** 2
            require(brier_live <= brier_base and int(terminal != y) <= int(base_terminal != y),
                    "pathwise_hardening_nonworsening", [unit["id"], index])
            if label is not None and episode["hard_enabled"]:
                known[qkey] = label
            expected_after = {"status": "checked", "answer": known[qkey], "interval": [known[qkey], known[qkey]]} if qkey in known else {
                              "status": "unresolved", "answer": None, "interval": [0, 1]}
            require(row["hard_after"] == expected_after, "current_hard_after", [unit["id"], index])
            counts.update(positions=1, first_occurrences=int(fresh), prior_known_positions=int(prior_known),
                          purchases=int(selected_here), changed_forecasts=int(emitted != forecasts[j]),
                          changed_prospective_actions=int(base_action != live_action),
                          corrected_terminal_actions=int(base_terminal != terminal))
            block_losses.append({"index": index, "truth": y, "first_occurrence": fresh,
                "prior_known": prior_known, "base_brier": pair(brier_base), "live_brier": pair(brier_live),
                "frozen_equal_brier": pair((F(sum(advice[j]), n) - y) ** 2),
                "base_terminal_error": int(base_terminal != y), "live_terminal_error": int(terminal != y),
                "selected": selected_here})
            seen.add(qkey)
        chosen = rows[start + selected]
        k = max(2, b - 1) if mode == "uniform" else 2 * b - 1
        divisor, scale = (k, 1) if mode == "uniform" else (multiplicity * k * k, 2 * b - multiplicity)
        products = [w * (divisor - scale * int(a != chosen["purchased_label"]))
                    for w, a in zip(weights, advice[selected])]
        after = fixed_mass(products, n, state_bits)
        require(recorded["weights_after"] == after, "block_weights_after", [unit["id"], block_index])
        detail.append({"block": block_index, "weights_before": weights, "weights_after": after,
                       "selected_offset": selected, "favorite": favorite, "rows": block_losses})
        weights = after
    require(position == bit_count == episode["random_bits_consumed"] == contract["random_bits"],
            "complete_bit_chronology", unit["id"])
    require(weights == episode["weights"] and episode["purchases"] == t // b,
            "final_numeric_state", unit["id"])
    require(len(known) <= contract["hard_capacity"], "observed_hard_capacity", unit["id"])
    hard_state = episode["hard_state"]
    require(hard_state["entries_retained"] == hard_state["active_entries"] == len(known)
            and hard_state["conflicts"] == hard_state["withdrawals"] == hard_state["generation"] == 0
            and hard_state["index_kind"] == contract["hard_index"]
            and hard_state["bucket_count"] == (128 if contract["hard_index"] == "hashed" else 0),
            "complete_current_hard_state", unit["id"])
    return {"unit_id": unit["id"], "group_id": unit["group_id"], "status": "audited",
            "configuration_id": unit["configuration_id"], "selector": mode,
            "counts": dict(counts), "final_weight_fractions": [pair(F(w, sum(weights))) for w in weights],
            "blocks": detail}


def main():
    global LINEAGE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=False)
    before = {"utc": datetime.now(timezone.utc).isoformat(), "monotonic_ns": time.monotonic_ns()}
    try:
        LINEAGE = Lineage()
        schedule_path = REPO / "v3/experiments/frozen_v1/schedule.json"
        schedule = read(schedule_path)
        config_path = REPO / "v3/experiments/protocol.v1.json"
        require(sha(config_path) == "dde9fe405ad39e65db3d49cb47d298e3ab6e498d7c5c485ff215ff884466b88f",
                "unchanged_machine_protocol", str(config_path))
        config = read(config_path)["arms"]["broker"]
        inputs = {g["id"]: sealed("inputs", g["id"]) for g in schedule["groups"] if g["arm"] == "broker"}
        audits = []
        bindings = []
        for unit in schedule["units"]:
            if unit["arm"] != "broker" or unit["engine"] not in ("broker", "mirror"):
                continue
            public, public_seal = sealed("public", unit["id"])
            evaluation, score_seal = sealed("evaluation", "score-" + unit["id"])
            require(evaluation["value"]["public_result_sha256"] == public_seal["result_sha256"],
                    "score_public_binding", unit["id"])
            input_record, input_seal = inputs[unit["group_id"]]
            require(public["value"]["input_result_sha256"] == evaluation["value"]["input_result_sha256"] == input_seal["result_sha256"],
                    "public_private_input_binding", unit["id"])
            bindings.append({"unit_id": unit["id"], "input_result_sha256": input_seal["result_sha256"],
                             "public_result_sha256": public_seal["result_sha256"], "score_result_sha256": score_seal["result_sha256"]})
            audits.append(audit_episode(unit, public["value"]["paid_result"], input_record["value"], config))
        result = {"schema": "value_logic.p310.numeric_transcript_observer.v1", "status": "PASS",
            "contributor": "ChatGPT (GPT-6 Astra Pro)", "scope": "Supplemental independent reconstruction of the already sealed broker/mirror numerical transcripts; no new paid run or fair-bit claim.",
            "start": before, "end": {"utc": datetime.now(timezone.utc).isoformat(), "monotonic_ns": time.monotonic_ns()},
            "source_sha256": sha(Path(__file__).resolve()), "schedule_sha256": sha(schedule_path),
            "checks_by_kind": dict(CHECKS), "checks_total": sum(CHECKS.values()),
            "episodes": len(audits), "counts": dict(sum((Counter(a["counts"]) for a in audits), Counter())),
            "audited_episodes": sum(a["status"] == "audited" for a in audits),
            "unavailable_unit_ids": [a["unit_id"] for a in audits if a["status"] != "audited"],
            "sealed_source_bindings": bindings, "amendment_lineage": LINEAGE.receipt,
            "per_episode": audits, "no_frozen_module_imported": True, "no_paid_execution": True}
        (out / "results.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
        print(json.dumps({k: v for k, v in result.items() if k not in ("per_episode", "sealed_source_bindings")}, indent=2))
    except BaseException as error:
        failure = {"status": "OBSERVER_FAILURE", "start": before, "observed_utc": datetime.now(timezone.utc).isoformat(),
                   "source_sha256": sha(Path(__file__).resolve()), "error_type": type(error).__name__,
                   "error": str(error), "traceback": traceback.format_exc(), "checks_completed": dict(CHECKS),
                   "scientific_stage_failure": False}
        (out / "failure.json").write_text(json.dumps(failure, indent=2) + "\n")
        raise


if __name__ == "__main__":
    main()
