"""Prospective P3-09 adapter over preserved P3-08 bounded-CNF methods.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-11.
Import/default_config/groups/units construct no mathematical populations.
Only generate(..., exposure_token='P3-10-EXPOSED') creates final public inputs.
run has no evaluator-truth access; score is a separately called observer.
The inherited DEVELOPMENT/MT labels remain truthful implementation provenance:
these fixed seeded paths do not establish an independent-fair-bit premise.
"""
from __future__ import annotations

from copy import deepcopy
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random

import p308_broker as B
import p308_cached_service as A
import p308_cnf as S
import p308_mirrors as M
import p308_ordinary as O
import p308_reporting as P
from p308_common import C, REPO, canonical, fraction_record, registry_setup


VERSION = "p309-broker-adapter-v1"
EXPOSURE_TOKEN = "P3-10-EXPOSED"
CORE = (
    "v3/experiments/p308_common.py",
    "v3/experiments/p308_cnf.py",
    "v3/experiments/p308_hashcache.py",
    "v3/experiments/p308_broker.py",
    "v3/experiments/p308_ordinary.py",
    "v3/experiments/p308_mirrors.py",
    "v3/experiments/p308_cached_service.py",
    "v3/checks/07_selective_feedback.py",
    "v3/checks/07_selective_feedback_service.py",
    "v3/checks/07_computation_adapter.py",
    "v3/experiments/p309_broker.py",
)
REPORT_SOURCE = "v3/experiments/p308_reporting.py"


def source_paths():
    """Complete local import closure, including this adapter and reporter."""
    return sorted(set(CORE + (REPORT_SOURCE,)))


def _pair(value):
    value = F(value)
    return [value.numerator, value.denominator]


def _json(value):
    return json.loads(canonical(value))


def _digest(value):
    return hashlib.sha256(canonical(value).encode("ascii")).hexdigest()


def _template(stage, policy_seeds, populations):
    return {
        "schema": "value_logic.p309.broker_config.v1",
        "version": VERSION, "stage": stage,
        "policy_seeds": list(policy_seeds), "populations": populations,
        "block_size": 4, "action_bits": 16, "state_bits": 16,
        "hard_capacity": 128, "cache_capacity": 64,
        "ordinary_prices": ["0", "1/10000", "1/1000"],
        "asymmetric_price": "1/10000",
        "asymmetric_stakes": [["1/2", "3/2"], ["3/2", "1/2"]],
        "proof_cap": 2048, "exact_enumeration_cap": 1 << 32,
        "cold_unit_limit": 1 << 38,
        "report_execution_limit": P.REPORT_FUNDING_CAP,
        "report_source_limit": 1 << 20,
        "report_basis": "snapshot", "report_radius": "grid",
        "source_version": S.SOURCE_VERSION,
        "population_scope": "Two fixed prospective recipe instances per family; no IID population claim.",
        "randomness_scope": "Prespecified finite DEVELOPMENT_MT seed paths; no empirical fair-bit or coverage claim.",
        "receiving_service": "Immutable pre-current-computation forecast and terminal binary action, knowledge status, retained paid word record; unresolved proof attempts retain named fallback.",
        "preparation": "No offline fitting, alignment, representation search or truth prepopulation; every episode starts at equal six-expert weights and empty scientific caches.",
        "cost_scope": {
            "core_sources": list(CORE), "report_source": REPORT_SOURCE,
            "adapter_source_bytes": "This co-located adapter file is installed in full and equally for every method.",
            "charged_execution": "Inherited declared word-operation service, provider/check/cache/acquisition/advice/controller/randomness/output/retention costs.",
            "excluded_execution": "Population supplier, Python orchestration/import/JSON audit encoding, private scoring and analysis; not a physical CPU or process-memory tariff.",
            "optional_reporting": "Separate paid source and execution account; excluded from terminal-only economic comparisons.",
        },
        "configuration_selection": "Whole configurations fixed ex ante. Mirrors are mandatory identity duplicates, not independent observations. No per-seed or per-query best-method oracle.",
    }


def default_config():
    """Pure prospective metadata; the literal seeds are not sampled here."""
    populations = []
    for family, seeds in (
            ("mixed", (3092101, 3092102)),
            ("gate_transfer", (3092201, 3092202)),
            ("cheap_null", (3092301, 3092302))):
        for index, seed in enumerate(seeds):
            populations.append({"family": family, "population_index": index,
                "seed": seed, "horizon": 128 if family == "gate_transfer" else 64,
                "prefix_length": 64 if family == "gate_transfer" else 0})
    result = _template("PROSPECTIVE_FINAL_CHALLENGE", (3091001, 3091002, 3091003), populations)
    result["recipes"] = {
        "mixed": "Frozen P3-08-style width/density/component mixture on4/6/8/10/12 variables; every eighth request repeats the formula seven positions earlier, under a new opaque query ID.",
        "gate_transfer": "64 mixed-prefix requests, followed by64 unique width≤3 gate-CNF circuit-miter requests. Three primary inputs, two four-gate AND/OR/XOR circuits, final XOR miter asserted true; twelve total variables. Second circuit is copied, one-gate-mutated, or independently drawn with equal generator probability. Gate descriptions/construction modes are not delivered to policies. Fixed implementation and paid online state continue across the boundary.",
        "cheap_null": "Equal counts of empty CNF, an empty clause, opposing units, and a complete consistent unit assignment, with bounded public variable counts/signs and a shuffled order. Visible exact shortcuts remain available to every method.",
        "gate_duplicate_rule": "At most64 public canonical-key redraws per gate position, without truth calls. Exhaustion is a preserved generation failure, not a new population attempt.",
    }
    result["expected_counts"] = {"groups": 6, "episodes": 336,
        "identity_duplicate_episodes": 18, "non_mirror_episode_executions": 318,
        "mixed_group_episodes": 64, "other_group_episodes": 52}
    return result


def _validate_config(config):
    if (type(config) is not dict or config.get("version") != VERSION
            or config.get("schema") != "value_logic.p309.broker_config.v1"):
        raise ValueError("Use the frozen P3-09 broker adapter configuration.")
    if config.get("stage") not in ("PROSPECTIVE_FINAL_CHALLENGE", "DEVELOPMENT"):
        raise ValueError("Unknown adapter configuration stage.")
    for seed in config["policy_seeds"]:
        C.nat(seed, (1 << 64) - 1, "fixed policy seed")
    if not config["policy_seeds"] or len(set(config["policy_seeds"])) != len(config["policy_seeds"]):
        raise ValueError("Use distinct, nonempty fixed policy seed labels.")
    for field in ("cold_unit_limit", "report_execution_limit", "report_source_limit"):
        C.nat(config[field], C.MAX_UNITS, field, minimum=1)
    C.nat(config["block_size"], 8192, "fixed block size", minimum=2)
    if config["block_size"] & (config["block_size"] - 1):
        raise ValueError("The fixed selector needs a power-of-two block size.")
    if config["source_version"] != S.SOURCE_VERSION:
        raise ValueError("The final recipes use the preserved source version.")
    for field, maximum, minimum in (("action_bits", 32, 1), ("state_bits", 32, 1),
            ("cache_capacity", S.MAX_CACHE, 0), ("hard_capacity", 8192, 0),
            ("proof_cap", C.MAX_UNITS, 0), ("exact_enumeration_cap", C.MAX_UNITS, 1)):
        C.nat(config[field], maximum, field, minimum=minimum)
    if config["exact_enumeration_cap"] < 39069040:
        raise ValueError("The exact-enumeration name requires the universal admitted provider envelope.")
    if type(config["ordinary_prices"]) is not list or not config["ordinary_prices"]:
        raise ValueError("The ordinary acquisition price catalogue is required.")
    for price in config["ordinary_prices"] + [config["asymmetric_price"]]:
        O._price(price, "prospective native price")
    for stakes in config["asymmetric_stakes"]:
        if type(stakes) is not list or len(stakes) != 2 or max(F(value) for value in stakes) <= 0:
            raise ValueError("Known asymmetric stake pairs must have a positive maximum.")
        for value in stakes:
            O._price(value, "prospective known stake")
    if config["asymmetric_stakes"] and config["asymmetric_price"] not in config["ordinary_prices"]:
        raise ValueError("Every asymmetric acquisition price needs its declared symmetric reference.")
    if config["report_basis"] not in ("base", "snapshot") or config["report_radius"] not in ("fixed", "grid"):
        raise ValueError("Unknown frozen report construction.")


def groups(config):
    """Return group recipes only; no Query or random generator is created."""
    _validate_config(config)
    result = []
    for recipe in config["populations"]:
        family, index = recipe["family"], recipe["population_index"]
        if family not in ("mixed", "gate_transfer", "cheap_null") or type(index) is not int or index < 0:
            raise ValueError("Unknown finite population recipe.")
        C.nat(recipe["seed"], (1 << 64) - 1, "fixed population seed")
        B.Contract(recipe["horizon"], config["block_size"], 6,
                   config["action_bits"], config["state_bits"],
                   hard_capacity=config["hard_capacity"])
        prefix = recipe["prefix_length"]
        if type(prefix) is not int or not 0 <= prefix < recipe["horizon"] or prefix % config["block_size"]:
            raise ValueError("Transfer boundary must be a complete block boundary.")
        result.append({"id": f"broker_{family}_p{index:02d}", "arm": "broker",
                       "recipe": deepcopy(recipe)})
    if len({group["id"] for group in result}) != len(result):
        raise ValueError("Duplicate prospective group identity.")
    return result


def _specs(config, asymmetric):
    specs = []

    def add(identity, engine, method, parameters, *, kind="ordinary",
            stochastic=False, stakes=("1", "1"), **pairing):
        specs.append({"configuration_id": identity, "engine": engine,
            "method": method, "method_kind": kind, "parameters": parameters,
            "stochastic": stochastic, "stakes": {"fp": _pair(stakes[0]), "fn": _pair(stakes[1])},
            "pairing_configurations": pairing})

    for selector in ("uniform", "tickets"):
        base = "finite_" + selector + "_cold"
        live = "value_" + selector + "_cold"
        cached = "value_" + selector + "_cached_hashed"
        add(base, "broker", "finite", {"selector": selector, "hard": False,
            "provider": "cold", "solver": "dpll"}, stochastic=True)
        add(live, "broker", "value", {"selector": selector, "hard": True,
            "provider": "cold", "solver": "dpll"}, kind="candidate", stochastic=True,
            base_id=base)
        add(cached, "broker", "value", {"selector": selector, "hard": True,
            "provider": "hashed", "solver": "dpll"}, kind="candidate", stochastic=True,
            base_id=base, cold_id=live)
    add("probability_cost", "ordinary", "probability_cost", {}, stochastic=True)
    for cache_kind in ("linear", "hashed"):
        for price in config["ordinary_prices"]:
            identity = "ordinary_combo_" + cache_kind + "_p" + price.replace("/", "_")
            add(identity, "ordinary", "ordinary_combo", {"cache_kind": cache_kind,
                "unit_price": price}, stochastic=True)
    for solver in ("enumeration", "dpll"):
        for fallback in (0, 1):
            add(f"proof_{solver}_fallback{fallback}", "ordinary", "proof_only",
                {"proof_solver": solver, "proof_cap": config["proof_cap"],
                 "fallback_action": fallback})
    add("exact_enumeration", "ordinary", "proof_only",
        {"proof_solver": "enumeration", "proof_cap": config["exact_enumeration_cap"]})
    add("exact_dpll", "ordinary", "exact_dpll", {})
    for cache_kind in ("linear", "hashed"):
        add("exact_cache_" + cache_kind, "ordinary", "exact_cache", {"cache_kind": cache_kind})
    for fallback in (0, 1):
        add("no_compute_" + str(fallback), "ordinary", "no_compute", {"fallback_action": fallback})
    add("ordinary_kernel_mirror", "mirror", "ordinary_mixture",
        {"selector": "uniform", "hard": True, "provider": "hashed", "solver": "dpll"},
        kind="mirror", stochastic=True, identity_of="value_uniform_cached_hashed")
    if asymmetric:
        price = config["asymmetric_price"]
        for index, stakes in enumerate(config["asymmetric_stakes"]):
            add(f"probability_cost_stakes{index}", "ordinary", "probability_cost", {},
                stochastic=True, stakes=stakes, stakes_reference="probability_cost")
            add(f"ordinary_combo_hashed_p{price.replace('/', '_')}_stakes{index}",
                "ordinary", "ordinary_combo", {"cache_kind": "hashed", "unit_price": price},
                stochastic=True, stakes=stakes,
                stakes_reference="ordinary_combo_hashed_p" + price.replace("/", "_"))
    if len({row["configuration_id"] for row in specs}) != len(specs):
        raise ValueError("Repeated configuration identity.")
    return specs


def _segments(recipe):
    horizon, prefix = recipe["horizon"], recipe["prefix_length"]
    result = [{"name": "whole", "start": 0, "stop": horizon}]
    if prefix:
        result += [{"name": "prefix", "start": 0, "stop": prefix},
                   {"name": "transfer", "start": prefix, "stop": horizon}]
    return result


def _unit(group, spec, seed):
    identity = group["id"] + "__" + spec["configuration_id"] + "__seed" + str(seed)
    pairing = {"population_key": group["id"], "randomization_id": "seed" + str(seed),
        "feedback_path_family": "broker_interleaved_selector_and_action_bits"
        if spec["engine"] in ("broker", "mirror") else
        "ordinary_selector_only" if spec["stochastic"] else "deterministic_no_bits",
        "same_seed_does_not_imply_same_broker_and_ordinary_feedback": True}
    for name, configuration in spec["pairing_configurations"].items():
        pairing[name] = group["id"] + "__" + configuration + "__seed" + str(seed)
    return {"id": identity, "group_id": group["id"], "arm": "broker",
        "configuration_id": spec["configuration_id"], "method_kind": spec["method_kind"],
        "engine": spec["engine"], "method": spec["method"], "seed": seed,
        "stochastic": spec["stochastic"], "parameters": deepcopy(spec["parameters"]),
        "stakes": deepcopy(spec["stakes"]), "pairing": pairing,
        "segments": _segments(group["recipe"]),
        "identity_duplicate": spec["method_kind"] == "mirror"}


def units(group, config):
    """Pure scheduling; every configuration is applied to every declared seed."""
    _validate_config(config)
    if canonical(group) not in {canonical(value) for value in groups(config)}:
        raise ValueError("Group differs from its frozen metadata.")
    result = []
    for spec in _specs(config, group["recipe"]["family"] == "mixed"):
        if spec["engine"] == "ordinary" and spec["method"] not in O.METHODS:
            raise ValueError("A scheduled ordinary method is not implemented.")
        if spec["engine"] in ("broker", "mirror"):
            params = spec["parameters"]
            if params["selector"] not in ("uniform", "tickets") or params["provider"] not in ("cold", "hashed") or params["solver"] != "dpll":
                raise ValueError("Unknown selected broker configuration.")
        if "proof_cap" in spec["parameters"]:
            C.nat(spec["parameters"]["proof_cap"], C.MAX_UNITS, "scheduled proof cap")
        seeds = config["policy_seeds"] if spec["stochastic"] else config["policy_seeds"][:1]
        result.extend(_unit(group, spec, seed) for seed in seeds)
    return result


def _mixed_query(rng, index, previous, source_version):
    identity = f"p309-q-{index:05d}"
    if index and index % 8 == 7:
        old = previous[index - 7]
        return S.Query(identity, old.variables, old.clauses, source_version)
    n = (4, 6, 8, 10, 12)[index % 5]
    cohort = index % 4
    count = min(64, (2 + (index // 4) % 4) * n)
    clauses = []
    for j in range(count):
        if cohort == 0:
            width, pool = rng.choice((1, 2)), list(range(1, n + 1))
        elif cohort == 1:
            width, pool = 3, list(range(1, n + 1))
        elif cohort == 2:
            half = j & 1
            width, pool = min(3, n // 2), list(range(1 + half * (n // 2), 1 + (half + 1) * (n // 2)))
        else:
            width, pool = rng.choice((2, 3, 4)), list(range(1, n + 1))
        clauses.append(tuple(v if rng.randrange(2) else -v for v in rng.sample(pool, width)))
    return S.make_query(identity, n, clauses, source_version)


def _gate_clauses(op, a, b, z):
    if op == "and":
        return ((-a, -b, z), (a, -z), (b, -z))
    if op == "or":
        return ((a, b, -z), (-a, z), (-b, z))
    if op == "xor":
        return ((a, b, -z), (a, -b, z), (-a, b, z), (-a, -b, -z))
    raise ValueError("Unknown fixed gate constructor.")


def _gate_query(rng, index, source_version):
    # Construction only. No gate/circuit evaluation or satisfiability call.
    operations = ("and", "or", "xor")

    def draw(start):
        available, result = [1, 2, 3], []
        for z in range(start, start + 4):
            a, b = rng.choice(available), rng.choice(available)
            a *= 1 if rng.randrange(2) else -1
            b *= 1 if rng.randrange(2) else -1
            result.append((rng.choice(operations), a, b, z))
            available.append(z)
        return result

    left = draw(4)
    mode = rng.randrange(3)
    if mode == 2:
        right = draw(8)
    else:
        def remap(value):
            return (1 if value > 0 else -1) * (abs(value) + 4 if abs(value) >= 4 else abs(value))
        right = [(op, remap(a), remap(b), z + 4) for op, a, b, z in left]
        if mode == 1:
            where = rng.randrange(4)
            op, a, b, z = right[where]
            right[where] = (rng.choice(tuple(value for value in operations if value != op)), a, b, z)
    clauses = [clause for gate in left + right + [("xor", 7, 11, 12)]
               for clause in _gate_clauses(*gate)]
    clauses.append((12,))
    return S.make_query(f"p309-q-{index:05d}", 12, clauses, source_version)


def generate(group, config, *, exposure_token=None):
    """Generate final CNFs only after the caller's global preparation barrier."""
    if exposure_token != EXPOSURE_TOKEN:
        raise PermissionError("Final population generation requires P3-10-EXPOSED.")
    if canonical(group) not in {canonical(value) for value in groups(config)}:
        raise ValueError("Group differs from its frozen recipe.")
    recipe = group["recipe"]
    rng = random.Random(recipe["seed"])
    horizon, family = recipe["horizon"], recipe["family"]
    source_version, queries = config["source_version"], []
    if family in ("mixed", "gate_transfer"):
        prefix = horizon if family == "mixed" else recipe["prefix_length"]
        for i in range(prefix):
            queries.append(_mixed_query(rng, i, queries, source_version))
        if family == "gate_transfer":
            seen = {query.claim_key for query in queries}
            for i in range(prefix, horizon):
                for _ in range(64):
                    query = _gate_query(rng, i, source_version)
                    if query.claim_key not in seen:
                        seen.add(query.claim_key)
                        queries.append(query)
                        break
                else:
                    raise RuntimeError("Preserve exhausted public-key gate generation; no replacement population.")
    else:
        kinds = [i % 4 for i in range(horizon)]
        rng.shuffle(kinds)
        for i, kind in enumerate(kinds):
            n = rng.choice((4, 6, 8, 10, 12))
            if kind == 0:
                clauses = ()
            elif kind == 1:
                clauses = ((),)
            elif kind == 2:
                v = rng.randrange(1, n + 1)
                clauses = ((v,), (-v,))
            else:
                clauses = tuple((v if rng.randrange(2) else -v,) for v in range(1, n + 1))
            queries.append(S.make_query(f"p309-q-{i:05d}", n, clauses, source_version))
    return {"schema": "value_logic.p309.broker_public_input.v1", "version": VERSION,
        "stage": "FINAL_EVALUATION_INPUT", "exposure_marker": EXPOSURE_TOKEN,
        "group_id": group["id"], "horizon": horizon,
        "segments": _segments(recipe), "queries": [query.record() for query in queries],
        "policy_fields": "Canonical CNF Query only; no truth labels, construction modes, gate graphs, planted witnesses or evaluator cache.",
        "supplier_truth_computations": 0}


def _read_public(public_input, unit, config):
    if public_input.get("schema") != "value_logic.p309.broker_public_input.v1" or public_input.get("version") != VERSION:
        raise ValueError("Unknown public-input schema.")
    development = config["stage"] == "DEVELOPMENT"
    expected = "DEVELOPMENT" if development else EXPOSURE_TOKEN
    if public_input.get("exposure_marker") != expected or public_input["group_id"] != unit["group_id"]:
        raise ValueError("Public input does not belong to the admitted stage/group.")
    if public_input["segments"] != unit["segments"]:
        raise ValueError("Segment metadata changed between scheduling and delivery.")
    queries = []
    for row in public_input["queries"]:
        if set(row) != {"query_id", "variables", "clauses", "source_version", "semantics_version"}:
            raise ValueError("Only the fixed canonical Query fields may reach a policy.")
        queries.append(S.Query(row["query_id"], row["variables"],
            tuple(tuple(clause) for clause in row["clauses"]), row["source_version"], row["semantics_version"]))
    if len(queries) != public_input["horizon"] or len({q.query_id for q in queries}) != len(queries):
        raise ValueError("Full public horizon and distinct request IDs are required.")
    if not queries or any(q.source_version != config["source_version"] for q in queries):
        raise ValueError("A main episode uses one admitted unchanged source epoch.")
    return tuple(queries)


def run(unit, public_input, config):
    """One paid public execution; private truth and score are never called."""
    _validate_config(config)
    tape = _read_public(public_input, unit, config)
    source_meter = C.CostMeter(config["cold_unit_limit"])
    sources, service_audit, optional = [], None, None
    episode = None
    service = None
    try:
        sources = registry_setup([REPO / path for path in CORE], source_meter)
        remaining = config["cold_unit_limit"] - source_meter.total
        params = unit["parameters"]
        if unit["engine"] in ("broker", "mirror"):
            service = S if params["provider"] == "cold" else A.CachedService(
                cache_kind=params["provider"], capacity=config["cache_capacity"])
            contract = B.Contract(len(tape), config["block_size"], 6,
                config["action_bits"], config["state_bits"], params["selector"],
                config["hard_capacity"], "hashed" if params["hard"] else "linear")
            executor = B.execute if unit["engine"] == "broker" else M.run_ordinary_mixture
            episode = executor(service, tape, contract, seed=unit["seed"], hard=params["hard"],
                purchase_solver=params["solver"], unit_limit=remaining,
                provider_limit=params.get("provider_limit"), scope_epoch="p309-" + unit["group_id"])
            if service is not S:
                service_audit = service.audit_record()
        elif unit["engine"] == "ordinary":
            fp, fn = F(*unit["stakes"]["fp"]), F(*unit["stakes"]["fn"])
            episode = O.run_method(tape, unit["method"], seed=unit["seed"],
                false_positive_price=fp, false_negative_price=fn,
                block_size=config["block_size"], action_bits=config["action_bits"],
                state_bits=config["state_bits"], cache_capacity=config["cache_capacity"],
                unit_limit=remaining, **params)
        else:
            raise ValueError("Unknown prepared execution engine.")
    except (C.Rejected, C.BudgetExceeded, S.Rejected) as error:
        # Source/local preparation denial is observable and never refunded.
        # Normal funded core calls return their own detailed failure records.
        empty = C.CostMeter(0).snapshot()
        episode = {"stage": "DEVELOPMENT", "version": VERSION, "status": "failed",
            "failure_detail": type(error).__name__ + ": " + str(error),
            "trace": [], "blocks": [], "invoices": [], "rounds_closed": 0,
            "purchases": 0, "meter": empty, "failure_origin": "adapter_or_source_admission"}
    if service is not None:
        # Optional report denial cannot erase a completed paid terminal episode.
        report_meter = C.CostMeter(config["report_source_limit"])
        report_sources = []
        try:
            report_sources = registry_setup([REPO / REPORT_SOURCE], report_meter)
            report = P.report_owned_episode(service, episode,
                unit_limit=config["report_execution_limit"],
                basis=config["report_basis"], radius=config["report_radius"])
        except (C.Rejected, C.BudgetExceeded) as error:
            report = {"status": "failed", "failure_detail": type(error).__name__ + ": " + str(error),
                      "meter": C.CostMeter(0).snapshot(), "confidence_eligible": False}
        optional = {"source_invoice": report_meter.snapshot(), "sources": report_sources,
            "report": report, "additional_units": report_meter.total + report["meter"]["total"]}
    return _json({"schema": "value_logic.p309.broker_result.v1", "version": VERSION,
        "stage": "DEVELOPMENT" if config["stage"] == "DEVELOPMENT" else "FINAL_PUBLIC_EXECUTION",
        "unit": unit, "public_input_sha256": _digest(public_input),
        "policy_truth_access": False, "common_source_invoice": source_meter.snapshot(),
        "common_sources": sources, "episode": episode, "service_audit": service_audit,
        "optional_reporting": optional, "inner_development_label_is_source_provenance": True,
        "randomness_claim": "Fixed finite seeded path only; fair-bit and probability-coverage premises are not established by this run.",
        "cost_scope": config["cost_scope"]})


def _independent_truth(record):
    """Private evaluator only: independent complete bit-mask enumeration."""
    masks = []
    for clause in record["clauses"]:
        pos = sum(1 << (x - 1) for x in set(clause) if x > 0)
        neg = sum(1 << (-x - 1) for x in set(clause) if x < 0)
        masks.append((pos, neg))
    for assignment in range(1 << record["variables"]):
        if all((assignment & pos) or ((~assignment) & neg) for pos, neg in masks):
            return 1
    return 0


def _fraction(pair):
    if (type(pair) is not list or len(pair) != 2 or any(type(x) is not int for x in pair)
            or pair[1] <= 0):
        raise ValueError("An exact finite rational pair is required.")
    return F(*pair)


def _invoice(snapshot):
    total = snapshot["total"]
    if type(total) is not int or total < 0 or sum(snapshot["by_category"].values()) != total:
        raise ValueError("Resource categories do not reconcile.")
    if sum(row["units"] for row in snapshot["operations"]) != total:
        raise ValueError("Resource operations do not reconcile.")
    if any(type(row["units"]) is not int or row["units"] < 0 for row in snapshot["operations"]):
        raise ValueError("Invalid paid operation amount.")
    return total


def _metrics(rows, truths, start, stop, fp, fn, action_bits, eligible_indices=None):
    eligible = set(range(start, stop)) if eligible_indices is None else set(eligible_indices)
    if any(type(index) is not int or not start <= index < stop for index in eligible):
        raise ValueError("Metric slice is outside the declared horizon.")
    selected = [row for row in rows if row["index"] in eligible]
    count, expected = len(selected), len(eligible)
    full = count == expected and expected > 0
    brier = base_brier = action_loss = F(0)
    half = equal = dyadic = live_half = live_equal = F(0)
    experts = [F(0)] * 6
    advice_available = all(len(row["advice"]) == 6 for row in selected)
    errors = false_positive = false_negative = 0
    for row in selected:
        y = truths[row["index"]]
        q, base = _fraction(row["emitted_q"]), _fraction(row["base_q"])
        brier += (q - y) ** 2
        base_brier += (base - y) ** 2
        action = row["terminal_action"]
        false_positive += int(action == 1 and y == 0)
        false_negative += int(action == 0 and y == 1)
        errors += int(action != y)
        action_loss += fp * int(action == 1 and y == 0) + fn * int(action == 0 and y == 1)
        if advice_available:
            advice = row["advice"]
            mix = F(sum(advice), 6)
            rounded = F((sum(advice) << action_bits) // 6, 1 << action_bits)
            half += (F(1, 2) - y) ** 2
            equal += (mix - y) ** 2
            dyadic += (rounded - y) ** 2
            if row["hard_before"] != "checked":
                live_half += (F(1, 2) - y) ** 2
                live_equal += (mix - y) ** 2
            for j, prediction in enumerate(advice):
                experts[j] += (prediction - y) ** 2
    maximum = max(fp, fn)
    return {"start": start, "stop": stop, "horizon": expected,
        "rounds_closed": count, "full_horizon": full,
        "brier_mean": _pair(brier / expected) if full else None,
        "base_brier_mean": _pair(base_brier / expected) if full else None,
        "uniform_brier_mean": _pair(equal / expected) if full and advice_available else None,
        "action_loss_mean": _pair(action_loss / (maximum * expected)) if full else None,
        "task_max_loss": _pair(maximum), "weighted_action_loss_sum": _pair(action_loss),
        "issued_brier_sum": _pair(brier), "base_issued_brier_sum": _pair(base_brier),
        "terminal_errors": errors, "false_positives": false_positive, "false_negatives": false_negative,
        "closed_prefix_only_if_incomplete": {"brier_mean": _pair(brier / count) if count else None,
            "action_loss_mean": _pair(action_loss / (maximum * count)) if count else None},
        "forecast_readouts": None if not full or not advice_available else {
            "constant_half_brier_mean": _pair(half / expected),
            "equal_mixture_brier_mean": _pair(equal / expected),
            "dyadic_equal_mixture_brier_mean": _pair(dyadic / expected),
            "same_hard_mask_half_brier_mean": _pair(live_half / expected),
            "same_hard_mask_equal_mixture_brier_mean": _pair(live_equal / expected),
            "expert_brier_means": [_pair(value / expected) for value in experts],
            "meaning": "Evaluator-only readouts of this trajectory's recorded paid advice and chronological hard mask; no free deployed controller or regret against upgraded experts."}}


def _path_digests(episode):
    fields = ("index", "query_id", "claim_key", "advice", "base_q", "base_action",
              "base_terminal", "selected", "propensity", "purchased_label")
    common = {"blocks": episode.get("blocks", []), "weights": episode.get("weights"),
        "random_bits_consumed": episode.get("random_bits_consumed"),
        "randomness": episode.get("randomness")}
    base = {**common, "trace": [{key: row[key] for key in fields} for row in episode["trace"]]}
    delivered = {**common, "trace": episode["trace"]}
    action_fields = ("index", "query_id", "emitted_q", "prospective_action", "terminal_action")
    actions = [{field: row[field] for field in action_fields} for row in episode["trace"]]
    return {"base_path_sha256": _digest(base), "delivered_path_sha256": _digest(delivered),
        "action_path_sha256": _digest(actions),
        "meaning": "Hashes exclude invoices, provider identity, accounting and hard-index configuration. Base path also excludes live-hard forecast/action/status changes; it retains selections, actual propensities, base forecasts/actions, labels, updates and consumed bits."}


def _report_widths(optional, horizon):
    if optional is None or optional["report"]["status"] != "success":
        return None
    result = {}
    for name, interval in optional["report"]["intervals"].items():
        width = _fraction(interval["upper"]) - _fraction(interval["lower"])
        conflict = interval.get("confidence_conflict", False)
        result[name] = {"width": None if conflict else _pair(width),
            "width_per_horizon": None if conflict else _pair(width / horizon),
            "lower": interval["lower"], "upper": interval["upper"],
            "confidence_conflict": conflict}
    return result


def _report_comparison(optional, horizon):
    """A5 observer arithmetic on already paid output; no coverage inference.

    Compare each delivered interval with its own deterministic observable
    envelope, not with a newly computed or deployed reference method. Signed
    gains are never clamped; a conflict supplies no usable width reduction.
    """
    if type(horizon) is not int or horizon <= 0:
        raise ValueError("A report comparison needs its positive scheduled horizon.")
    output = {"status": "not_requested", "report_status": None,
        "horizon": horizon, "additional_units": 0, "endpoints": {},
        "practical_threshold_normalized": [1, 100],
        "empirical_coverage_claim": False,
        "comparison_reference": "The same paid report's deterministic observable envelope.",
        "normalization": "All widths and signed gains divide by the scheduled horizon, not the number of purchased or known labels.",
        "scope": "Exact descriptive endpoint arithmetic. A conflicting interval is not usable service or a positive practical reporting gain."}
    if optional is None:
        return output
    report = optional["report"]
    output.update(status=report["status"], report_status=report["status"],
        additional_units=optional["additional_units"],
        reference_basis=report.get("reference_basis"), radius_rule=report.get("radius_rule"),
        failure_detail=report.get("failure_detail"))
    if report["status"] != "success":
        return output
    for name, interval in report["intervals"].items():
        lower, upper = _fraction(interval["lower"]), _fraction(interval["upper"])
        det = report["deterministic_envelopes"][name]
        det_lower, det_upper = _fraction(det[0]), _fraction(det[1])
        det_width, span = det_upper - det_lower, upper - lower
        lower_gain, upper_gain = lower - det_lower, det_upper - upper
        conflict = bool(interval.get("confidence_conflict", False)) or span < 0
        normalized_reduction = None if conflict else (det_width - span) / horizon
        output["endpoints"][name] = {
            "status": "confidence_conflict" if conflict else "success",
            "confidence_conflict": conflict,
            "lower": interval["lower"], "upper": interval["upper"],
            "width": None if conflict else _pair(span),
            "width_per_horizon": None if conflict else _pair(span / horizon),
            "delivered_signed_span": _pair(span),
            "deterministic_lower": det[0], "deterministic_upper": det[1],
            "deterministic_width": _pair(det_width),
            "deterministic_width_per_horizon": _pair(det_width / horizon),
            "normalized_width_reduction": None if conflict else _pair(normalized_reduction),
            "lower_endpoint_gain": _pair(lower_gain),
            "upper_endpoint_gain": _pair(upper_gain),
            "normalized_lower_endpoint_gain": _pair(lower_gain / horizon),
            "normalized_upper_endpoint_gain": _pair(upper_gain / horizon),
            "practical_width_reduction": not conflict and normalized_reduction >= F(1, 100),
            "practical_lower_endpoint_gain": not conflict and lower_gain / horizon >= F(1, 100),
            "practical_upper_endpoint_gain": not conflict and upper_gain / horizon >= F(1, 100)}
    if any(row["confidence_conflict"] for row in output["endpoints"].values()):
        output["status"] = "confidence_conflict"
    return output


def _semantic_errors(unit, episode, tape, truths):
    """Narrow scientific validity checks; programming exceptions are not caught."""
    errors, rows = [], episode["trace"]
    if [row.get("index") for row in rows] != list(range(len(rows))) or len(rows) > len(tape):
        return [{"kind": "invalid_closed_prefix", "detail": "Closed rows are not the declared sequential prefix."}]
    if episode["rounds_closed"] != len(rows):
        return [{"kind": "invalid_closed_count", "detail": "Closed-row count disagrees with the transcript."}]
    known, bought = {}, {}
    by_id = {query.query_id: (query, y) for query, y in zip(tape, truths)}
    cached_provider = unit["engine"] in ("broker", "mirror") and unit["parameters"]["provider"] != "cold"
    provider, version = (A.PROVIDER, A.VERSION) if cached_provider else (S.PROVIDER, S.VERSION)
    for invoice in episode["invoices"]:
        identity = invoice.get("query_id")
        if identity not in by_id:
            errors.append({"kind": "receipt_unknown_query", "query_id": identity})
            continue
        query, y = by_id[identity]
        if canonical(invoice.get("claim_key")) != canonical(query.claim_key) or invoice.get("provider") != provider or invoice.get("provider_version") != version:
            errors.append({"kind": "receipt_content_or_provider_binding", "query_id": identity})
        if invoice.get("status") == "success":
            if invoice.get("checked") is not True or type(invoice.get("answer")) is not int or invoice["answer"] != y:
                errors.append({"kind": "unsound_paid_receipt", "query_id": identity})
            else:
                bought[identity] = y
        elif invoice.get("answer") is not None or invoice.get("checked") is not False:
            errors.append({"kind": "failed_receipt_claimed_answer", "query_id": identity})
    for row, query, y in zip(rows, tape, truths):
        index = row["index"]
        if row.get("query_id") != query.query_id or canonical(row.get("claim_key")) != canonical(query.claim_key):
            errors.append({"kind": "transcript_query_binding", "index": index})
        fractions = {}
        for name in ("base_q", "emitted_q"):
            try:
                fractions[name] = _fraction(row.get(name))
            except ValueError:
                errors.append({"kind": "invalid_forecast_encoding", "index": index, "field": name})
                continue
            if not 0 <= fractions[name] <= 1:
                errors.append({"kind": "forecast_outside_unit_interval", "index": index, "field": name})
        if type(row.get("terminal_action")) is not int or row["terminal_action"] not in (0, 1):
            errors.append({"kind": "invalid_terminal_action", "index": index})
        advice = row.get("advice")
        if type(advice) is not list or len(advice) not in (0, 6) or any(type(value) is not int or value not in (0, 1) for value in advice):
            errors.append({"kind": "invalid_recorded_advice", "index": index})
        if row.get("hard_before") == "checked" and (known.get(query.claim_key) != y or fractions.get("emitted_q") != y):
            errors.append({"kind": "hard_issuance_without_prior_current_answer", "index": index})
        label = row.get("purchased_label")
        if label is not None:
            if type(label) is not int or label != y or bought.get(query.query_id) != y:
                errors.append({"kind": "row_label_without_bound_paid_receipt", "index": index})
            else:
                known[query.claim_key] = label
        after = row.get("hard_after")
        if type(after) is not dict:
            errors.append({"kind": "invalid_hard_status_record", "index": index})
        elif after.get("status") == "checked" and (type(after.get("answer")) is not int
                or after["answer"] != y or after.get("interval") != [y, y]
                or known.get(query.claim_key) != y):
            errors.append({"kind": "unsound_current_hard_answer", "index": index})
    return errors


def _invalid_score(unit, result, tape, source_units, local_units, optional_units, errors):
    """Preserve invalid delivered semantics as an outcome, never a retry reason."""
    return {"schema": "value_logic.p309.broker_score.v1", "version": VERSION,
        "unit_id": unit["id"], "group_id": unit["group_id"],
        "configuration_id": unit["configuration_id"], "method_kind": unit["method_kind"],
        "method": unit["method"], "engine": unit["engine"], "seed": unit["seed"],
        "stochastic": unit["stochastic"], "identity_duplicate": unit["identity_duplicate"],
        "pairing": deepcopy(unit["pairing"]), "stakes": deepcopy(unit["stakes"]),
        "status": "FAIL", "validity_pass": False, "full_horizon": False, "horizon": len(tape),
        "brier_mean": None, "base_brier_mean": None, "uniform_brier_mean": None,
        "action_loss_mean": None, "cold_units": source_units + local_units,
        "local_units": local_units, "source_units": source_units,
        "optional_reporting_units": optional_units,
        "native_price_normalized": None if unit["engine"] != "ordinary" else
            _pair(F(unit["parameters"].get("unit_price", "0")) / max(F(*unit["stakes"]["fp"]), F(*unit["stakes"]["fn"]))),
        "semantic_failures": errors, "paid_public_output_preserved": True,
        "recorded_query_ids": [row.get("query_id") for row in result["episode"]["trace"]],
        "required_query_ids": [query.query_id for query in tape],
        "optional_reporting_status": None if result["optional_reporting"] is None else
            result["optional_reporting"]["report"]["status"],
        "paid_report_comparison": _report_comparison(result["optional_reporting"], len(tape)),
        "public_result_sha256": _digest(result),
        "scope": "Completed semantic validity failure with paid output retained. No infrastructure retry or complete-service ranking is licensed."}


def score(unit, result, public_input, config):
    """Private observer, called only after the root has sealed all public runs."""
    _validate_config(config)
    if result.get("schema") != "value_logic.p309.broker_result.v1" or result.get("version") != VERSION:
        raise ValueError("Unknown saved public-result schema.")
    if canonical(result["unit"]) != canonical(unit) or result["public_input_sha256"] != _digest(public_input):
        raise ValueError("Saved unit/input binding changed before scoring.")
    tape = _read_public(public_input, unit, config)
    episode, rows = result["episode"], result["episode"]["trace"]
    source_units, local_units = _invoice(result["common_source_invoice"]), _invoice(episode["meter"])
    if source_units + local_units > config["cold_unit_limit"]:
        raise ValueError("A result exceeds its fixed cold account.")
    optional = result["optional_reporting"]
    optional_units = 0 if optional is None else _invoice(optional["source_invoice"]) + _invoice(optional["report"]["meter"])
    if optional is not None and optional_units != optional["additional_units"]:
        raise ValueError("Optional reporting invoice does not reconcile.")
    memo, truths = {}, []
    for query in tape:
        key = query.claim_key
        if key not in memo:
            memo[key] = _independent_truth(query.record())
        truths.append(memo[key])
    semantic_errors = _semantic_errors(unit, episode, tape, truths)
    if semantic_errors:
        return _invalid_score(unit, result, tape, source_units, local_units, optional_units, semantic_errors)
    fp, fn = _fraction(unit["stakes"]["fp"]), _fraction(unit["stakes"]["fn"])
    if min(fp, fn) < 0 or max(fp, fn) <= 0:
        raise ValueError("Known nonnegative stakes with positive maximum required.")
    metrics = _metrics(rows, truths, 0, len(tape), fp, fn, config["action_bits"])
    full = episode["status"] == "success" and metrics["full_horizon"]
    if not full:
        metrics["brier_mean"] = metrics["base_brier_mean"] = metrics["uniform_brier_mean"] = metrics["action_loss_mean"] = None
    first_indices, seen = [], set()
    for i, query in enumerate(tape):
        if query.claim_key not in seen:
            first_indices.append(i)
            seen.add(query.claim_key)
    first = _metrics(rows, truths, 0, len(tape), fp, fn, config["action_bits"], first_indices)
    raw_price = F(unit["parameters"].get("unit_price", "0")) if unit["engine"] == "ordinary" else None
    signatures = _path_digests(episode)
    return {"schema": "value_logic.p309.broker_score.v1", "version": VERSION,
        "unit_id": unit["id"], "group_id": unit["group_id"],
        "configuration_id": unit["configuration_id"], "method_kind": unit["method_kind"],
        "method": unit["method"], "engine": unit["engine"], "seed": unit["seed"],
        "stochastic": unit["stochastic"], "identity_duplicate": unit["identity_duplicate"],
        "pairing": deepcopy(unit["pairing"]), "stakes": deepcopy(unit["stakes"]),
        "coupling_signatures": signatures,
        **{name: signatures[name] for name in ("base_path_sha256", "delivered_path_sha256", "action_path_sha256")},
        **metrics, "status": "success" if full else "failed", "inner_status": episode["status"],
        "validity_pass": True, "semantic_failures": [],
        "full_horizon": full, "horizon": len(tape),
        "cold_units": source_units + local_units, "local_units": local_units,
        "source_units": source_units, "optional_reporting_units": optional_units,
        "optional_reporting_status": None if optional is None else optional["report"]["status"],
        "paid_report_endpoint_widths": _report_widths(optional, len(tape)),
        "paid_report_comparison": _report_comparison(optional, len(tape)),
        "native_price_raw": None if raw_price is None else _pair(raw_price),
        "native_price_normalized": None if raw_price is None else _pair(raw_price / max(fp, fn)),
        "native_normalized_objective_mean": None if not full or raw_price is None else
            _pair((_fraction(metrics["weighted_action_loss_sum"]) + raw_price * (source_units + local_units)) / (max(fp, fn) * len(tape))),
        "native_price_meaning": "Ordinary acquisition price is supplied in raw loss per word unit. Both task loss and raw price divide by the declared maximum loss for normalized objectives; broker policies have no acquisition-price input.",
        "first_occurrence": {"indices": first_indices, "parent_full_horizon": full,
            "definition": "First exact full canonical content+version key within this episode; not a claim of semantic inequivalence.", **first},
        "segments": {segment["name"]: _metrics(rows, truths, segment["start"], segment["stop"], fp, fn,
                     config["action_bits"]) for segment in unit["segments"]},
        "served_query_ids": [row["query_id"] for row in rows],
        "missing_query_ids": [query.query_id for query in tape[len(rows):]],
        "failure_detail": episode.get("failure_detail"),
        "logical_receipts": episode["purchases"] if unit["engine"] in ("broker", "mirror") else None,
        "physical_provider_attempts": episode["purchases"] if result["service_audit"] is None
            else result["service_audit"]["physical_cold_calls"],
        "checked_cache_hits": (episode.get("cache_hits", 0) if result["service_audit"] is None
                               else result["service_audit"]["checked_cache_hits"]),
        "private_truth_unique_programs": len(memo), "known_wrong": 0,
        "ordinary_combo_exploration_floor": unit["method"] == "ordinary_combo",
        "all_path_funded_interface": episode.get("all_path_funded", False),
        "fair_bits_established": False, "empirical_coverage_claim": False,
        "scope": "Finite complete-configuration comparison; incomplete service is retained with all costs and is not a cheap full-horizon winner."}


class SelfcheckFailure(AssertionError):
    """Caller must preserve .record; it contains completed development units."""
    def __init__(self, message, record):
        super().__init__(message)
        self.record = _json(record)


def _selfcheck_impl(state):
    config = _template("DEVELOPMENT", (7,), [])
    group = {"id": "development_broker_toy", "arm": "broker",
        "recipe": {"family": "development_toy", "horizon": 16, "prefix_length": 0}}
    queries = [S.make_query(f"development-only-{i:03d}", 3,
               ((1,),) if i < 8 else ((1,), (-1,))) for i in range(12)]
    for i, right_op in enumerate(("and", "and", "or", "or"), start=12):
        clauses = (_gate_clauses("and", 1, 2, 3) + _gate_clauses(right_op, 1, 2, 4)
                   + _gate_clauses("xor", 3, 4, 5) + ((5,),))
        queries.append(S.make_query(f"development-only-{i:03d}", 5, clauses))
    public = {"schema": "value_logic.p309.broker_public_input.v1", "version": VERSION,
        "stage": "DEVELOPMENT", "exposure_marker": "DEVELOPMENT", "group_id": group["id"],
        "horizon": 16, "segments": _segments(group["recipe"]), "queries": [query.record() for query in queries],
        "policy_fields": "Explicit development fixture only", "supplier_truth_computations": 0}
    scheduled = [_unit(group, spec, 7) for spec in _specs(config, True)]
    # Complete all development public records before this selfcheck calls score.
    records, scores, checks = [], [], []
    state.update({"configuration": config, "development_public_input": public,
                  "public_records": records, "scores": scores, "checks": checks})
    for unit in scheduled:
        state["current_development_unit_id"] = unit["id"]
        records.append(run(unit, public, config))
    for unit, result in zip(scheduled, records):
        scores.append(score(unit, result, public, config))
    by_id = {row["unit"]["id"]: row for row in records}

    def require(name, condition):
        checks.append({"name": name, "passed": bool(condition)})

    for op in ("and", "or", "xor"):
        for a_sign in (1, -1):
            for b_sign in (1, -1):
                for assignment in range(8):
                    def literal(value):
                        answer = bool(assignment & (1 << (abs(value) - 1)))
                        return answer if value > 0 else not answer
                    a, b, z = literal(a_sign), literal(2 * b_sign), literal(3)
                    expected = (a and b) if op == "and" else (a or b) if op == "or" else (a != b)
                    observed = all(any(literal(value) for value in clause)
                                   for clause in _gate_clauses(op, a_sign, 2 * b_sign, 3))
                    require(f"development_gate_equivalence:{op}:{a_sign}:{b_sign}:{assignment}",
                            observed == (z == expected))
    for row in scores:
        require("complete:" + row["configuration_id"], row["status"] == "success" and row["full_horizon"])
    for unit, result in zip(scheduled, records):
        current = result["episode"]
        links = unit["pairing"]
        if "base_id" in links:
            base = by_id[links["base_id"]]["episode"]
            fields = ("base_q", "base_action", "base_terminal", "selected", "purchased_label", "propensity", "advice")
            require("base_live:" + unit["configuration_id"],
                len(base["trace"]) == len(current["trace"])
                and all(all(a[field] == b[field] for field in fields) for a, b in zip(base["trace"], current["trace"]))
                and base["blocks"] == current["blocks"]
                and base["random_bits_consumed"] == current["random_bits_consumed"])
        if "cold_id" in links:
            cold = by_id[links["cold_id"]]["episode"]
            require("logical_receipt_reuse:" + unit["configuration_id"],
                all(cold[field] == current[field] for field in ("trace", "blocks", "weights", "random_bits_consumed")))
        if "identity_of" in links:
            direct = by_id[links["identity_of"]]
            require("ordinary_kernel_identity", current == direct["episode"]
                and result["service_audit"] == direct["service_audit"]
                and result["optional_reporting"] == direct["optional_reporting"]
                and result["common_source_invoice"] == direct["common_source_invoice"])
        if "stakes_reference" in links and unit["method"] == "probability_cost":
            reference = by_id[links["stakes_reference"]]["episode"]
            fields = ("advice", "base_q", "emitted_q", "selected", "purchased_label", "propensity")
            require("same_history_stakes_readout:" + unit["configuration_id"],
                all(all(a[field] == b[field] for field in fields) for a, b in zip(reference["trace"], current["trace"]))
                and reference["blocks"] == current["blocks"])
    # A separately named provider denial preserves its paid failed prefix.
    failed_unit = deepcopy(scheduled[0])
    failed_unit["id"] += "__development_denial"
    failed_unit["configuration_id"] += "__development_denial"
    failed_unit["parameters"]["provider_limit"] = 0
    failed = run(failed_unit, public, config)
    records.append(failed)
    failed_score = score(failed_unit, failed, public, config)
    scores.append(failed_score)
    require("paid_failure_not_full_service", not failed_score["full_horizon"]
        and failed_score["brier_mean"] is None and failed_score["action_loss_mean"] is None
        and failed_score["cold_units"] > 0 and failed["episode"]["status"] == "failed")
    # Separate optional-account denial cannot erase a paid complete episode.
    optional_config = deepcopy(config)
    optional_config["report_source_limit"] = 1
    optional_unit = deepcopy(scheduled[0])
    optional_unit["id"] += "__development_report_denial"
    optional_unit["configuration_id"] += "__development_report_denial"
    report_denied = run(optional_unit, public, optional_config)
    records.append(report_denied)
    report_denied_score = score(optional_unit, report_denied, public, optional_config)
    scores.append(report_denied_score)
    require("optional_denial_preserves_full_terminal_service",
        report_denied_score["full_horizon"] and report_denied_score["validity_pass"]
        and report_denied_score["optional_reporting_status"] == "failed"
        and report_denied["episode"] == records[0]["episode"])
    # Observer-only malformed-output copies are negative controls, not reruns.
    negative_controls = []
    state["observer_negative_controls"] = negative_controls
    for field, value in (("emitted_q", [2, 1]), ("terminal_action", 2)):
        malformed = deepcopy(records[0])
        malformed["episode"]["trace"][0][field] = value
        negative = score(scheduled[0], malformed, public, config)
        negative_controls.append({"mutation": {"row": 0, "field": field, "value": value},
            "public_record": malformed, "score": negative})
        require("semantic_negative_retains_paid_record:" + field,
            negative["status"] == "FAIL" and negative["validity_pass"] is False
            and negative["brier_mean"] is None
            and negative["cold_units"] == scores[0]["cold_units"]
            and negative["paid_public_output_preserved"] is True)
    malformed = deepcopy(records[0])
    malformed["episode"]["invoices"][0]["answer"] ^= 1
    negative = score(scheduled[0], malformed, public, config)
    negative_controls.append({"mutation": {"receipt": 0, "field": "answer", "operation": "flip bit"},
        "public_record": malformed, "score": negative})
    require("semantic_negative_retains_paid_record:receipt",
        negative["status"] == "FAIL" and negative["validity_pass"] is False
        and negative["cold_units"] == scores[0]["cold_units"]
        and any(error["kind"] == "unsound_paid_receipt" for error in negative["semantic_failures"]))
    meter = C.CostMeter(1 << 24)
    old_query = queries[0]
    cache = S.ExactCache(4)
    cap = S.service_cap(old_query, "dpll")
    meter.reserve("development_source_version", cap)
    receipt = S.checked_purchase(old_query, limit_total=cap, solver="dpll")
    meter.absorb(receipt.resources, "development_source_version_provider",
                 reservation="development_source_version", release=cap)
    cache.remember(old_query, receipt, meter)
    renamed = S.Query("development-renamed-id", old_query.variables, old_query.clauses, old_query.source_version)
    changed = S.Query("development-changed-source", old_query.variables, old_query.clauses, "development-source-v2")
    require("query_id_rename_reuses_paid_answer", cache.lookup(renamed, meter).answer == receipt.answer)
    require("source_version_change_is_cache_miss", cache.lookup(changed, meter) is None)
    contract = B.Contract(4)
    bits = C.BitTape.seeded(contract.random_bits, 7, meter)
    scope = (S.SEMANTICS_VERSION, S.SOURCE_VERSION, "development-epoch-1")
    broker = B.Broker(S, contract, meter, bits, scope, hard=True, purchase_solver="dpll")
    broker.begin_block(tuple(queries[:4]))
    for _ in range(4):
        issued = broker.issue()
        broker.close(issued)
        if broker.purchases:
            break
    require("development_live_receipt_before_withdrawal", broker.hard.lookup(old_query)["status"] == "checked")
    broker.withdraw((S.SEMANTICS_VERSION, S.SOURCE_VERSION, "development-epoch-2"))
    rejected = False
    try:
        broker.close(issued)
    except C.Rejected:
        rejected = True
    require("withdrawal_ends_old_broker_authority", rejected and broker.record()["status"] == "failed")
    broker.hard.invalidate(scope)
    require("return_to_old_epoch_label_does_not_revive", broker.hard.lookup(old_query)["status"] == "stale")
    result = {"schema": "value_logic.p309.broker_selfcheck.v1", "stage": "DEVELOPMENT",
        "version": VERSION, "status": "PASS", "principal_clock_credit": 0,
        "final_generation_calls": 0, "final_seed_streams_generated": 0,
        "final_group_scheduling_calls": 0, "explicit_development_seed": 7,
        "development_public_input": public, "configuration": config,
        "public_records": records, "scores": scores,
        "observer_negative_controls": negative_controls,
        "optional_denial_configuration": optional_config,
        "development_boundary_invoice": meter.snapshot(),
        "checks": checks, "assertion_count": len(checks),
        "limits": "Small implementation conformance only; no final population, policy optimization, fair-bit coverage or broad scientific result."}
    if any(not check["passed"] for check in checks):
        result["status"] = "FAIL"
        raise SelfcheckFailure("A declared development conformance assertion failed.", result)
    return result


def selfcheck():
    """Preparation-only toy fixtures; no final groups/generator/seed streams.

    PASS is explicit. Any failed assertion or unexpected exception raises a
    SelfcheckFailure whose .record preserves all returned development units.
    """
    state = {"schema": "value_logic.p309.broker_selfcheck.v1", "stage": "DEVELOPMENT",
        "version": VERSION, "status": "FAIL", "principal_clock_credit": 0,
        "final_generation_calls": 0, "final_seed_streams_generated": 0,
        "final_group_scheduling_calls": 0, "explicit_development_seed": 7}
    try:
        return _selfcheck_impl(state)
    except SelfcheckFailure:
        raise
    except Exception as error:
        state.update({"unexpected_error_type": type(error).__name__, "unexpected_error": str(error)})
        raise SelfcheckFailure("Unexpected development selfcheck failure; preserve its attached record.", state) from error
