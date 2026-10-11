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
FINAL = REPO / "v3/experiments/final_v1"
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
    seals = list((FINAL / "stages" / stage / "units" / identifier).glob("attempt_*/seal.json"))
    require(len(seals) == 1, "one_seal", [stage, identifier])
    seal_path = seals[0]
    seal = read(seal_path)
    result_path = seal_path.parent / "result.json"
    start_path = seal_path.parent / "start.json"
    require(sha(result_path) == seal["result_sha256"], "result_hash", identifier)
    require(sha(start_path) == seal["start_sha256"], "start_hash", identifier)
    result = read(result_path)
    require(hashlib.sha256(canonical(result["unit"])).hexdigest() == seal["unit_sha256"],
            "unit_hash", identifier)
    return result, seal


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


def audit_episode(unit, paid, public):
    episode = paid["episode"]
    queries = public["queries"]
    rows, blocks = episode["trace"], episode["blocks"]
    contract = episode["contract"]
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
    by_query = {receipt["query_id"]: receipt for receipt in episode["invoices"]}
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
    return {"unit_id": unit["id"], "group_id": unit["group_id"],
            "configuration_id": unit["configuration_id"], "selector": mode,
            "counts": dict(counts), "final_weight_fractions": [pair(F(w, sum(weights))) for w in weights],
            "blocks": detail}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=False)
    before = {"utc": datetime.now(timezone.utc).isoformat(), "monotonic_ns": time.monotonic_ns()}
    try:
        for stage in ("inputs", "public", "evaluation", "analysis"):
            require((FINAL / "stages" / stage / "complete.json").is_file(), "ordered_stages_complete", stage)
        schedule_path = REPO / "v3/experiments/frozen_v1/schedule.json"
        schedule = read(schedule_path)
        inputs = {g["id"]: sealed("inputs", g["id"])[0]["value"] for g in schedule["groups"] if g["arm"] == "broker"}
        audits = []
        for unit in schedule["units"]:
            if unit["arm"] != "broker" or unit["engine"] not in ("broker", "mirror"):
                continue
            public, public_seal = sealed("public", unit["id"])
            evaluation, _ = sealed("evaluation", "score-" + unit["id"])
            require(evaluation["value"]["public_result_sha256"] == public_seal["result_sha256"],
                    "score_public_binding", unit["id"])
            audits.append(audit_episode(unit, public["value"]["paid_result"], inputs[unit["group_id"]]))
        result = {"schema": "value_logic.p310.numeric_transcript_observer.v1", "status": "PASS",
            "contributor": "ChatGPT (GPT-6 Astra Pro)", "scope": "Supplemental independent reconstruction of the already sealed broker/mirror numerical transcripts; no new paid run or fair-bit claim.",
            "start": before, "end": {"utc": datetime.now(timezone.utc).isoformat(), "monotonic_ns": time.monotonic_ns()},
            "source_sha256": sha(Path(__file__).resolve()), "schedule_sha256": sha(schedule_path),
            "checks_by_kind": dict(CHECKS), "checks_total": sum(CHECKS.values()),
            "episodes": len(audits), "counts": dict(sum((Counter(a["counts"]) for a in audits), Counter())),
            "per_episode": audits, "no_frozen_module_imported": True, "no_paid_execution": True}
        (out / "results.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
        print(json.dumps({k: v for k, v in result.items() if k != "per_episode"}, indent=2))
    except BaseException as error:
        failure = {"status": "OBSERVER_FAILURE", "start": before, "observed_utc": datetime.now(timezone.utc).isoformat(),
                   "source_sha256": sha(Path(__file__).resolve()), "error_type": type(error).__name__,
                   "error": str(error), "traceback": traceback.format_exc(), "checks_completed": dict(CHECKS),
                   "scientific_stage_failure": False}
        (out / "failure.json").write_text(json.dumps(failure, indent=2) + "\n")
        raise


if __name__ == "__main__":
    main()
