#!/usr/bin/env python3
"""Independent, read-only P3-10 saved-data conformance reconstruction.

Contributor: ChatGPT (GPT-6 Astra Pro), conformance_reconstruction subagent.
Revision 2 corrects lifecycle newline hashing identified by source review before
any final data access or observer run; v1 is preserved.
Written from frozen contracts before final data access. Imports only the standard
library: it never imports a generator, paid worker, private scorer or analyzer.
All reads and proof arithmetic are external audit work with zero principal credit.
Run only after the principal confirms ALL public and evaluation units complete.
Each invocation gets a fresh immutable attempt directory; failures are preserved.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path
import sys
import traceback

sys.dont_write_bytecode = True
AUTHOR = "ChatGPT (GPT-6 Astra Pro), /root/conformance_reconstruction"
SCOPE = "P3-10 saved-result conformance reconstruction; not P3-11 contribution review"
STRUCTURAL_NAMES = (
    "counterpossible_tied_minima", "external_sources_not_repairs",
    "fixed_falsity_constant_infeasible", "conditioning", "occurrence",
    "actor_replacement", "shared_replacement", "shared_and_copy",
    "shared_copy_and_new_predictor",
)
INFORMATION_NAMES = (
    "one_state_empty", "one_state_duplicate", "one_state_no_target",
    "rational_signed", "brier_anchor", "four_state_basis", "zero_reference",
    "partial_target_offset", "larger_exact",
)
CALIBRATIONS = ("known", "unknown_offset", "unknown_scale", "unknown_affine")
REJECTIONS = {
    "boolean_state_count": "n_states must be a positive integer.",
    "floating_loss": "Use integers or rational strings; floats and booleans are not exact inputs.",
    "unshared_scale_contract": "Unsupported calibration contract.",
    "restricted_source_field": "Unsupported input fields; this tool accepts only its declared full-simplex contract.",
    "wrong_row_width": "Every losses row must have n_states entries.",
    "realized_score_tag": "Unsupported input fields; this tool accepts only its declared full-simplex contract.",
}
SOURCE_PATHS = (
    "v3/experiments/p309_conformance.py",
    "v3/experiments/p308_structural.py",
    "v3/checks/02_finite_information_audit.py",
    "v3/checks/02_finite_information_verify.py",
    "v3/checks/02_finite_information_check.py",
    "v3/checks/04_counterfactual_repair.py",
    "v3/checks/05_counterfactual_transport.py",
    "v3/derivations/02_probability_information.md",
    "v3/experiments/protocol.md",
    "v3/experiments/protocol.v1.json",
    "v3/experiments/p309_lifecycle.py",
    "v3/experiments/p309_freeze.py",
    "v3/work_logs/P3_08_2026-10-10_S1/development/structural/tariff_v4_1_scope_note.md",
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def jsonable(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, (tuple, list)):
        return [jsonable(y) for y in x]
    if isinstance(x, dict):
        return {k: jsonable(v) for k, v in x.items()}
    return x


def wire(x):
    return json.dumps(jsonable(x), sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False)


def digest(x):
    return hashlib.sha256(wire(x).encode("ascii")).hexdigest()


def lifecycle_digest(x):
    """Lifecycle JSON bindings include one trailing newline; scientific payloads do not."""
    return hashlib.sha256((wire(x)+"\n").encode("utf-8")).hexdigest()


def utc():
    return datetime.now(timezone.utc).isoformat()


def vector(xs, n):
    require(type(xs) is list and len(xs) == n, "Exact vector dimension mismatch")
    require(all(type(x) in (int, str) for x in xs), "Nonexact vector component")
    return [F(x) for x in xs]


def matrix(xs, n):
    require(type(xs) is list, "Exact matrix required")
    return [vector(row, n) for row in xs]


def dot(a, b):
    require(len(a) == len(b), "Dot product dimension mismatch")
    return sum((x*y for x, y in zip(a, b)), F(0))


def linear(weights, rows, n):
    weights = vector(weights, len(rows))
    return [sum((w*row[i] for w, row in zip(weights, rows)), F(0)) for i in range(n)]


def rank(rows, n):
    """Independent forward elimination; no production row reducer is imported."""
    basis = {}
    for row in rows:
        require(len(row) == n, "Rank row width mismatch")
        residual = [F(x) for x in row]
        for pivot in sorted(basis):
            q = residual[pivot]
            if q:
                residual = [x-q*y for x, y in zip(residual, basis[pivot])]
        lead = next((i for i, x in enumerate(residual) if x), None)
        if lead is not None:
            q = residual[lead]
            basis[lead] = [x/q for x in residual]
    return len(basis)


def in_span(rows, c):
    return rank(rows+[c], len(c)) == rank(rows, len(c))


def effective(losses, offset_unknown):
    if not offset_unknown:
        return losses
    return [[x-y for x, y in zip(row, losses[0])] for row in losses[1:]] if losses else []


def constant(c):
    return all(x == c[0] for x in c)


def recoverable(c, rows, n, scale_unknown):
    if constant(c):
        return True
    if scale_unknown:
        return in_span(rows, [F(1)]*n) and in_span(rows, c)
    return in_span([[F(1)]*n]+rows, c)


def verify_target(target, cert, losses, rows, n, su, ou, counts):
    expected = recoverable(target, rows, n, su)
    require(type(cert["recoverable"]) is bool and cert["recoverable"] == expected,
            "Certificate recoverability differs from independent row-span criterion")
    if expected:
        kind = cert["kind"]
        if kind == "constant":
            require(target == [F(cert["value"])]*n, "False constant identity")
        elif kind == "affine":
            require(not su, "Uncalibrated scale used affine identity")
            got = linear(cert["effective_coefficients"], rows, n)
            require(target == [x+F(cert["constant"]) for x in got], "False affine identity")
        elif kind == "ratio_of_scaled_linear_targets":
            require(su, "Known-scale contract used unknown-scale certificate")
            require(linear(cert["normalizer_coefficients"], rows, n) == [F(1)]*n,
                    "Normalizer does not recover shared positive scale")
            require(linear(cert["numerator_coefficients"], rows, n) == target,
                    "Ratio numerator identity fails")
        else:
            raise AssertionError("Unknown positive certificate kind")
        counts["positive_target_certificates"] += 1
        return
    require(cert["kind"] == "indistinguishable_laws", "No nonidentification witness")
    w = cert["witness"]
    p, q = vector(w["p"], n), vector(w["q"], n)
    require(min(p) > 0 and min(q) > 0 and sum(p) == sum(q) == 1,
            "Collision is not between interior normalized laws")
    sp, sq, bp, bq = map(F, (w["scale_p"], w["scale_q"], w["offset_p"], w["offset_q"]))
    require(sp > 0 and sq > 0, "Nonpositive collision scale")
    require(su or sp == sq == 1, "Collision changed known scale")
    require(ou or bp == bq == 0, "Collision changed known offset")
    yp, yq = [sp*dot(l, p)+bp for l in losses], [sq*dot(l, q)+bq for l in losses]
    require(yp == yq == vector(w["observation"], len(losses)), "Collision observations differ")
    tp, tq = dot(target, p), dot(target, q)
    require(tp != tq and tp == F(w["target_p"]) and tq == F(w["target_q"]),
            "Collision fails to separate target")
    if "hidden_direction" in w:
        h, step = vector(w["hidden_direction"], n), F(w["positive_step"])
        hidden_base = rows if su else [[F(1)]*n]+rows
        require(all(dot(r, h) == 0 for r in hidden_base) and step > 0,
                "Saved collision direction/step is invalid")
        x = [a+step*b for a, b in zip(p, h)]
        require(q == [a/sum(x) for a in x], "Saved collision construction differs")
    counts["negative_target_certificates"] += 1


def verify_information(request, cert):
    n, cal = request["n_states"], request["calibration"]
    require(type(n) is int and n > 0 and cal in CALIBRATIONS, "Unsupported admitted request")
    su, ou = cal in ("unknown_scale", "unknown_affine"), cal in ("unknown_offset", "unknown_affine")
    L = matrix(request["losses"], n)
    C = matrix(request.get("targets", [[int(i == j) for j in range(n)] for i in range(n)]), n)
    M = effective(L, ou)
    require(cert["schema"] == "P3-02-finite-information-audit/v1" and cert["stage"] == "development",
            "Inherited inner proof schema/stage changed")
    require(type(cert["n_states"]) is int and cert["n_states"] == n and cert["calibration"] == cal,
            "Certificate request identity differs")
    require(matrix(cert["losses"], n) == L and matrix(cert["targets"], n) == C,
            "Certificate bound to different rows")
    require(matrix(cert["effective_rows"], n) == M, "Offset quotient rows differ")
    require(cert["effective_rank"] == rank(M, n), "Effective summary rank is incorrect")
    require(cert["normalization_augmented_rank"] == rank([[F(1)]*n]+M, n),
            "Normalization-augmented summary rank is incorrect")
    expected_targets = [recoverable(c, M, n, su) for c in C]
    full = all(recoverable([F(i == j) for j in range(n)], M, n, su) for i in range(n))
    require(type(cert["full_law_recoverable"]) is bool and cert["full_law_recoverable"] == full,
            "Full-law flag differs from independent row-span criterion")
    require(type(cert["all_targets_recoverable"]) is bool and cert["all_targets_recoverable"] == all(expected_targets),
            "Target summary differs from independent row-span criterion")
    counts = Counter(positive_target_certificates=0, negative_target_certificates=0, repair_dual_pairings=0)
    require(len(cert["target_certificates"]) == len(C), "Wrong target certificate count")
    for c, proof in zip(C, cert["target_certificates"]):
        verify_target(c, proof, L, M, n, su, ou, counts)
    law = cert["law_certificate"]
    if full:
        require(law["kind"] == "coordinate_decoders" and len(law["coordinates"]) == n,
                "Missing full-law coordinate decoders")
        for i, proof in enumerate(law["coordinates"]):
            verify_target([F(i == j) for j in range(n)], proof, L, M, n, su, ou, counts)
    else:
        i = law["coordinate"]
        require(law["kind"] == "separating_coordinate" and type(i) is int and 0 <= i < n,
                "Missing separating coordinate")
        require(law["certificate"]["recoverable"] is False, "Law obstruction has positive verdict")
        verify_target([F(i == j) for j in range(n)], law["certificate"], L, M, n, su, ou, counts)
    rep = cert["repair"]
    nonconstant = any(not constant(c) for c in C)
    base = M if su else [[F(1)]*n]+M
    needed = [[F(1)]*n]+C if su else C
    deficit = rank(base+needed, n)-rank(base, n) if nonconstant else 0
    ref = int(ou and not L and nonconstant)
    require(type(rep["effective_rank_deficit"]) is int and rep["effective_rank_deficit"] == deficit,
            "Repair deficit differs from independent rank formula")
    require(rep["new_reference_queries"] == ref and rep["minimum_extra_raw_queries"] == deficit+ref,
            "Sharp raw-query repair count is incorrect")
    Q = matrix(rep.get("added_effective_rows", []), n)
    H = matrix(rep.get("lower_bound_hidden_directions", []), n)
    extra = matrix(rep["extra_loss_rows"], n)
    require(len(Q) == len(H) == deficit and len(extra) == deficit+ref, "Repair witness dimensions differ")
    require(all(q in needed for q in Q), "Repair lower-bound row not required by target contract")
    for j, h in enumerate(H):
        require(all(dot(b, h) == 0 for b in base), "Repair direction visible in old information")
        require([dot(q, h) for q in Q] == [F(i == j) for i in range(deficit)],
                "Repair dual pairing matrix is not the identity")
        counts["repair_dual_pairings"] += deficit
    reference = L[0] if ou and L else [F(0)]*n
    expected_extra = ([[F(0)]*n] if ref else []) + [
        [a+b for a, b in zip(reference, q)] if ou else q for q in Q]
    require(extra == expected_extra, "Raw repair queries do not implement certified effective queries")
    newL, newM = L+extra, effective(L+extra, ou)
    require(len(rep["repaired_target_certificates"]) == len(C), "Repaired target certificate count differs")
    for c, proof in zip(C, rep["repaired_target_certificates"]):
        require(proof["recoverable"] is True, "Proposed repair still has unresolved target")
        verify_target(c, proof, newL, newM, n, su, ou, counts)
    return {
        "full_law_recoverable": full,
        "all_targets_recoverable": all(expected_targets),
        "target_count": len(C), "original_targets_recoverable": sum(expected_targets),
        "original_targets_nonidentified": len(C)-sum(expected_targets),
        "effective_rank": rank(M, n), "normalization_augmented_rank": rank([[F(1)]*n]+M, n),
        "minimum_extra_raw_queries": deficit+ref, "repair_effective_deficit": deficit,
        "counts": dict(counts),
    }


def expr(e, bits):
    op = e[0]
    if op == "lit": return F(e[1])
    if op == "bit": return F(bits[e[1]])
    if op == "not": return 1-expr(e[1], bits)
    if op == "scale": return F(e[1])*expr(e[2], bits)
    a, b = expr(e[1], bits), expr(e[2], bits)
    if op == "add": return a+b
    if op in ("and", "min"): return min(a, b)
    if op in ("or", "max"): return max(a, b)
    if op == "eq": return F(a == b)
    raise AssertionError("Unknown expression operation")


def support(q, atoms, bits):
    op = q[0]
    if op == "atom":
        i = atoms.index(q[1]); return bits[2*i], bits[2*i+1]
    if op == "top": return 1, 0
    if op == "bottom": return 0, 1
    if op == "not":
        p, n = support(q[1], atoms, bits); return n, p
    ap, an = support(q[1], atoms, bits)
    bp, bn = support(q[2], atoms, bits)
    if op == "and": return min(ap, bp), max(an, bn)
    if op == "or": return max(ap, bp), min(an, bn)
    raise AssertionError("Unknown quoted formula")


def classical(q, atoms, bits):
    op = q[0]
    if op == "atom": return bits[atoms.index(q[1])]
    if op == "top": return 1
    if op == "bottom": return 0
    if op == "not": return 1-classical(q[1], atoms, bits)
    a, b = classical(q[1], atoms, bits), classical(q[2], atoms, bits)
    if op == "and": return min(a, b)
    if op == "or": return max(a, b)
    raise AssertionError("Unknown classical quote")


def reconstruct_structural(spec):
    """Direct semantics and truth-table enumeration, without worker compilation."""
    rows = []
    for source in spec["sources"]:
        if spec["kind"] == "routing":
            h, old, new = spec["history"], spec["original_table"], spec["replacement_table"]
            require(new[h] == 1, "Replacement does not meet required action")
            op = source["operation"]
            if op == "conditioning": models = [] if old[h] != 1 else [[1, 1, 0, 0]]
            elif op == "occurrence": models = [[1, old[h], 0, 0]]
            else:
                require(op == "replacement", "Unknown routing operation")
                models = [[(new if follow else old)[h] for _, follow in source["routing"]]]
            best_rank = [F(0)] if models else None
        else:
            require(spec["kind"] == "paired", "Unknown structural request")
            models, best_rank = [], None
            atoms, frame, weights = spec["atoms"], dict(source["frame"]), dict(source["weights"])
            for bits in product((0, 1), repeat=2*len(atoms)):
                if support(spec["quote"], atoms, bits)[0] != 1: continue
                if any(bits[2*i]+bits[2*i+1] != 1 for i, atom in enumerate(atoms)
                       if atom not in spec["exceptions"]): continue
                if any((bits[2*i], bits[2*i+1]) != (frame[atom], 1-frame[atom])
                       for i, atom in enumerate(atoms) if atom in frame): continue
                candidate_rank = [F(sum(weights[atom] for i, atom in enumerate(atoms)
                                        if atom in spec["exceptions"] and bits[2*i]+bits[2*i+1] != 1))]
                if spec["preserve_baseline"]:
                    candidate_rank.append(F(sum(int(bits[2*i] != b)+int(bits[2*i+1] != 1-b)
                                                for i, b in enumerate(spec["baseline"]))))
                if best_rank is None or candidate_rank < best_rank:
                    best_rank, models = candidate_rank, [list(bits)]
                elif candidate_rank == best_rank: models.append(list(bits))
        vals = [{"state": bits, "losses": {name: expr(e, bits) for name, e in spec["actions"]}}
                for bits in models]
        rows.append({
            "source_id": source["id"],
            "scope_record": wire({"version": "p308-structural-v4.1", "request": spec, "source": source,
                                   "source_quantifier": "EXTERNAL_UNRESOLVED_CASE_NOT_A_REPAIR"}),
            "feasibility": "NONEMPTY" if models else "INFEASIBLE", "identities_complete": True,
            "optimal_rank": best_rank, "models": models,
            "loss_images": {name: sorted({v["losses"][name] for v in vals}) for name, _ in spec["actions"]},
            "case_values": vals,
        })
    if any(row["feasibility"] != "NONEMPTY" for row in rows):
        decision = {"status": "INFEASIBLE", "action": None, "useful_action_warrant": False,
                    "reason": "No established nonempty target for every retained source."}
    else:
        names = [name for name, _ in spec["actions"]]
        cases = [case for row in rows for case in row["case_values"]]
        worst = {a: max(case["losses"][a] for case in cases) for a in names}
        chosen = min(names, key=lambda a: (worst[a], names.index(a)))
        lowest = min(row["optimal_rank"] for row in rows)
        wrongly_retained = [row for row in rows if row["optimal_rank"] == lowest]
        wrong_cases = [case for row in wrongly_retained for case in row["case_values"]]
        wrong_worst = {a: max(case["losses"][a] for case in wrong_cases) for a in names}
        decision = {
            "status": "CHECKED_COMPLETE", "action": chosen, "fixed_action_worst_loss": worst[chosen],
            "worst_loss_by_fixed_action": worst, "useful_action_warrant": True,
            "all_ties_preserved": True,
            "selection_order": "ONE_ACTION_THEN_ALL_UNRESOLVED_SOURCES_THEN_ALL_PER_SOURCE_MINIMA",
            "nonimplementable_pointwise_action_oracle": max(min(c["losses"][a] for a in names) for c in cases),
            "oracle_is_policy": False,
            "forbidden_joint_source_repair_minimum": {
                "retained_sources": [row["source_id"] for row in wrongly_retained],
                "minimum_fixed_loss": min(wrong_worst.values()), "is_an_admissible_service": False},
        }
    terminal = {"status": "SUCCESS", "sources": rows, "decision": decision,
                "source_information": "Each named source is unresolved and retained outside minimization.",
                "check_service": "complete local finite report"}
    if spec["kind"] == "paired":
        terminal.update(quoted_antecedent=spec["quote"],
                        ordinary_interpretation="Fixed ordinary Boolean interpretation of the original quote.",
                        ordinary_satisfying_valuations=sum(classical(spec["quote"], spec["atoms"], bits)
                            for bits in product((0, 1), repeat=len(spec["atoms"]))),
                        hypothetical_interpretation="Declared paired-support evaluation; not a truth probability.")
    return jsonable(terminal)


class Observer:
    def __init__(self, repo):
        self.repo = repo
        self.frozen = repo/"v3/experiments/frozen_v1"
        self.final = repo/"v3/experiments/final_v1"
        self.reads = {}
        self.stage_meta = {}

    def read(self, path):
        b = path.read_bytes()
        self.reads[str(path.relative_to(self.repo))] = {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
        return json.loads(b)

    def prepare(self):
        manifest = self.read(self.frozen/"manifest.json")
        schedule = self.read(self.frozen/"schedule.json")
        require(self.reads[str((self.frozen/"schedule.json").relative_to(self.repo))]["sha256"] == manifest["schedule_sha256"],
                "Frozen schedule digest differs from manifest")
        source_rows = {row["path"]: row for row in manifest["sources"]}
        checked = []
        for rel in SOURCE_PATHS:
            row = source_rows[rel]
            for p in (self.frozen/"source"/rel, self.repo/rel):
                b = p.read_bytes()
                got = {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
                self.reads[str(p.relative_to(self.repo))] = got
                require(got == {k: row[k] for k in got}, "Frozen/live source differs: "+str(p))
            checked.append(row)
        self.binding = {"freeze_id": manifest["freeze_id"],
                        "manifest_sha256": self.reads[str((self.frozen/"manifest.json").relative_to(self.repo))]["sha256"],
                        "protocol_sha256": manifest["protocol_sha256"]}
        self.schedule = schedule
        return checked

    def stage(self, name):
        if name in self.stage_meta: return self.stage_meta[name]
        s = self.read(self.final/"stages"/name/"schedule.json")
        c = self.read(self.final/"stages"/name/"complete.json")
        expected = self.schedule["groups"] if name == "inputs" else self.schedule["units"]
        if name == "evaluation": expected = [dict(u, id="score-"+u["id"], public_unit_id=u["id"]) for u in expected]
        identity = {"stage": name, "binding": self.binding, "schedule_sha256": lifecycle_digest(expected)}
        require(s["units"] == expected and all(s[k] == v for k, v in identity.items()), "Stage schedule binding mismatch")
        require(all(c[k] == v for k, v in identity.items()), "Stage completion binding mismatch")
        require(c["expected_units"] == c["completed_units"] == len(expected) == len(c["seals"]),
                "Stage is not fully complete")
        require([x["unit_id"] for x in c["seals"]] == [x["id"] for x in expected],
                "Stage completion seal roster differs")
        self.stage_meta[name] = (identity, {x["unit_id"]: x for x in c["seals"]})
        return self.stage_meta[name]

    def sealed(self, name, unit):
        identity, entries = self.stage(name)
        e = entries[unit["id"]]
        seal_path = self.final/e["path"]
        require(seal_path.parent.parent.name == unit["id"] and seal_path.parent.name.startswith("attempt_"),
                "Completion seal path not owned by unit")
        seal = self.read(seal_path)
        require(self.reads[str(seal_path.relative_to(self.repo))]["sha256"] == e["sha256"], "Seal content hash differs")
        all_seals = list(seal_path.parent.parent.glob("attempt_*/seal.json"))
        require(all_seals == [seal_path], "Unit does not have exactly one completion seal")
        result_path, start_path = seal_path.parent/"result.json", seal_path.parent/"start.json"
        result, start = self.read(result_path), self.read(start_path)
        require(seal["identity"] == identity and seal["unit_sha256"] == lifecycle_digest(unit), "Sealed unit identity mismatch")
        require(self.reads[str(result_path.relative_to(self.repo))]["sha256"] == seal["result_sha256"] and
                self.reads[str(start_path.relative_to(self.repo))]["sha256"] == seal["start_sha256"], "Unit file hash mismatch")
        require(result["identity"] == start["identity"] == identity and result["unit"] == start["unit"] == unit,
                "Unit record binding mismatch")
        require(result["attempt"] == start["attempt"] == seal["attempt"], "Unit attempt mismatch")
        return result["value"], seal["result_sha256"]

    def run(self):
        sources = self.prepare()
        # These indices must show ALL units complete before any final scientific payload is read.
        self.stage("public")
        self.stage("evaluation")
        groups = [g for g in self.schedule["groups"] if g["arm"] == "conformance"]
        units = [u for u in self.schedule["units"] if u["arm"] == "conformance"]
        require(len(groups) == 2 and len(units) == 60, "Wrong conformance schedule size")
        inputs = {g["id"]: self.sealed("inputs", g) for g in groups}
        summary = Counter()
        rows, reconstructions = [], {}
        for unit in units:
            public, input_sha = inputs[unit["group_id"]]
            envelope, public_sha = self.sealed("public", unit)
            scored, score_sha = self.sealed("evaluation", dict(unit, id="score-"+unit["id"], public_unit_id=unit["id"]))
            result, score = envelope["paid_result"], scored["score"]
            require(envelope["input_result_sha256"] == input_sha == scored["input_result_sha256"] and
                    scored["public_result_sha256"] == public_sha, "Cross-stage seal linkage mismatch")
            selected = public["inputs"][unit["case_index"]]
            require(result["unit_id"] == score["unit_id"] == unit["id"] and result["group_id"] == unit["group_id"],
                    "Outer unit binding mismatch")
            for key in ("method", "configuration_id", "evidence_class"):
                require(result[key] == score[key] == unit[key], "Outer method/classification binding mismatch")
            require(result["schema"] == "p309.conformance.result.v1" and result["version"] == "p309-conformance-v1" and
                    result["stage"] == "P3-10-PUBLIC" and public["stage"] == "P3-10-EXPOSED", "Outer stage/schema mismatch")
            require(result["public_input_sha256"] == digest(public) and result["case_sha256"] == digest(selected),
                    "Selected case/public payload binding mismatch")
            require(score["stage"] == "P3-10-SCORED" and score["status"] == "PASS" and score["validity_pass"] is True,
                    "Final score is not a conformance pass")
            row = {"unit_id": unit["id"], "case_name": unit["case_name"], "engine": unit["engine"],
                   "public_result_sha256": public_sha, "score_result_sha256": score_sha, "independent_pass": True}
            if unit["engine"] == "legacy_structural":
                require(selected["name"] == unit["case_name"] in STRUCTURAL_NAMES, "Wrong structural case")
                inner = result["inner_record"]
                expected = reconstruct_structural(selected)
                require(wire(expected) == wire(inner["output"]), "Structural terminal differs from independent exhaustive reconstruction")
                require(inner["input_sha256"] == digest(selected) and inner["method"] == unit["worker_method"],
                        "Structural inner binding mismatch")
                invoice = inner["invoice"]
                require(invoice["tariff"] == "STRUCTURAL-VM-v1" and invoice["budget"] == 50_000_000,
                        "Structural invoice tariff/cap mismatch")
                costs = [v for by_kind in invoice["by_stage"].values() for v in by_kind.values()]
                require(all(type(v) is int and v >= 0 for v in costs), "Invalid structural cost component")
                total = sum(costs)
                require(total == invoice["total_units"] == score["cold_units"] and total <= invoice["budget"],
                        "Structural invoice sum/cap does not reconcile")
                admission_paths = ["v3/experiments/p308_structural.py"]
                if unit["worker_method"] == "candidate":
                    admission_paths += ["v3/checks/04_counterfactual_repair.py", "v3/checks/05_counterfactual_transport.py"]
                expected_admission = [{"path": p, "bytes": next(x["bytes"] for x in sources if x["path"] == p)} for p in admission_paths]
                require(inner["source_admission"] == expected_admission, "Structural source admission roster differs")
                source_bytes = sum(x["bytes"] for x in expected_admission)
                require(invoice["by_stage"]["setup"]["source_admission_bytes"] == source_bytes,
                        "Structural installed source-byte charge differs")
                require(score["local_units"] == total-source_bytes, "Structural local cost differs")
                require(score["output_sha256"] == digest(expected) and score["delivered"] is True,
                        "Structural scored output/delivery mismatch")
                available = expected["decision"]["useful_action_warrant"]
                require(score["semantic_action_available"] == available, "Infeasibility/action status conflated")
                row.update(method=unit["worker_method"], cold_units=total, local_units=total-source_bytes,
                           action=expected["decision"]["action"], decision_status=expected["decision"]["status"],
                           source_count=len(expected["sources"]),
                           per_source_minima=[len(x["models"]) for x in expected["sources"]],
                           fixed_action_worst_loss=expected["decision"].get("fixed_action_worst_loss"),
                           expected_output_sha256=digest(expected))
                reconstructions[unit["case_name"]] = expected
                summary["structural_outputs"] += 1
                summary["structural_action_available"] += int(available)
                summary["structural_infeasible_terminals"] += int(not available)
            elif unit["expected_kind"] == "input_rejection":
                name = unit["case_name"]
                require(selected["name"] == name and selected["expected_error"] == REJECTIONS[name], "Rejection definition differs")
                request = selected["request"]
                # Establish each actual defect directly from JSON, without calling the production validator.
                defects = {
                    "boolean_state_count": type(request.get("n_states")) is bool,
                    "floating_loss": any(type(x) is float for xs in request["losses"] for x in xs),
                    "unshared_scale_contract": request.get("calibration") == "independent_row_scales",
                    "restricted_source_field": request.get("source") == "restricted",
                    "wrong_row_width": any(len(xs) != request["n_states"] for xs in request["losses"]),
                    "realized_score_tag": request.get("observation_kind") == "realized_score",
                }
                require(defects[name], "Named invalid-input defect is absent")
                require(result["status"] == "INPUT_REJECTED" and result["error_type"] == "ValueError" and result["error"] == REJECTIONS[name],
                        "Wrong invalid-input rejection")
                require(score["counts"] == {"input_rejections": 1} and score["delivered"] is False and score["hypothesis_rejection"] is True,
                        "Input rejection misclassified as delivered mathematical service")
                row.update(rejection_name=name, expected_error=REJECTIONS[name], defect_observed=True)
                summary["information_input_rejections"] += 1
            else:
                require(selected["name"] == unit["case_name"] in INFORMATION_NAMES, "Wrong information case")
                require(result["status"] == "CERTIFICATE" and score["delivered"] is True, "Missing information certificate")
                info = verify_information(selected["request"], result["certificate"])
                for key in ("full_law_recoverable", "all_targets_recoverable", "minimum_extra_raw_queries", "counts"):
                    require(score[key] == info[key], "Scored information summary differs: "+key)
                row.update(calibration=unit["calibration"], **info)
                summary["information_certificates"] += 1
                summary["information_full_law_recoverable"] += int(info["full_law_recoverable"])
                summary["information_full_law_nonidentified"] += int(not info["full_law_recoverable"])
                summary["information_all_targets_recoverable"] += int(info["all_targets_recoverable"])
                summary["information_some_targets_nonidentified"] += int(not info["all_targets_recoverable"])
                summary["information_original_target_rows"] += info["target_count"]
                summary["information_original_targets_recoverable"] += info["original_targets_recoverable"]
                summary["information_original_targets_nonidentified"] += info["original_targets_nonidentified"]
                summary["information_positive_repair_units"] += int(info["minimum_extra_raw_queries"] > 0)
                summary["information_minimum_extra_queries_sum"] += info["minimum_extra_raw_queries"]
                for k, v in info["counts"].items(): summary["verifier_"+k] += v
            rows.append(row)
        require(summary["structural_outputs"] == 18 and summary["information_certificates"] == 36 and
                summary["information_input_rejections"] == 6, "Conformance output roster incomplete")
        for name in STRUCTURAL_NAMES:
            paired = [r for r in rows if r["engine"] == "legacy_structural" and r["case_name"] == name]
            require(len(paired) == 2 and len({r["expected_output_sha256"] for r in paired}) == 1,
                    "Structural candidate/ordinary exact replies differ")
        by_mode = {}
        for mode in CALIBRATIONS:
            subset = [r for r in rows if r.get("calibration") == mode]
            by_mode[mode] = {
                "certificates": len(subset), "full_law_recoverable": sum(r["full_law_recoverable"] for r in subset),
                "all_targets_recoverable": sum(r["all_targets_recoverable"] for r in subset),
                "minimum_extra_raw_queries": sum(r["minimum_extra_raw_queries"] for r in subset),
            }
        return {"schema": "value_logic.p310.conformance_independent_observer.v1", "status": "PASS",
                "contributor": AUTHOR, "scope": SCOPE, "finished_utc": utc(),
                "principal_clock_credit_seconds": 0, "frozen_imports": 0, "paid_worker_invocations": 0,
                "generator_invocations": 0, "private_scorer_invocations": 0, "analyzer_invocations": 0,
                "summary": dict(summary), "by_calibration": by_mode, "rows": rows,
                "structural_reconstructed_outputs": reconstructions,
                "limitations": ["All 60 are already exposed regression/conformance definitions, not unseen transfer.",
                                "Information inputs assume exact expected losses under one common full-simplex law and declared shared nuisance.",
                                "Structural arithmetic verifies the exact nine-fixture tariff sums and source charges, not measured CPU or heap cost.",
                                "Complete-stage indices establish the exposure boundary; other-arm scientific outputs are outside this review.",
                                "No novelty or method-superiority judgment is made; P3-N01/P3-11 is separate."],
                "reviewed_frozen_sources": sources, "consumed_file_bindings": self.reads}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--public-and-evaluation-complete", action="store_true", required=True)
    args = parser.parse_args()
    own = Path(__file__).resolve().parent
    attempts = own/"runs"
    attempts.mkdir(exist_ok=True)
    i = 1
    while (attempts/("attempt_%02d" % i)).exists(): i += 1
    out = attempts/("attempt_%02d" % i)
    out.mkdir()
    observer = Observer(args.repo.resolve())
    code = Path(__file__).read_bytes()
    start = {"schema": "value_logic.p310.observer_start.v1", "contributor": AUTHOR, "scope": SCOPE,
             "started_utc": utc(), "public_and_evaluation_completion_authorized": args.public_and_evaluation_complete,
             "observer_sha256": hashlib.sha256(code).hexdigest(), "observer_bytes": len(code),
             "principal_clock_credit_seconds": 0}
    (out/"start.json").write_text(json.dumps(start, indent=2, sort_keys=True)+"\n")
    try:
        result = observer.run()
        (out/"result.json").write_text(json.dumps(jsonable(result), indent=2, sort_keys=True)+"\n")
    except BaseException as exc:
        failure = {"status": "OBSERVER_FAILURE", "finished_utc": utc(), "type": type(exc).__name__,
                   "message": str(exc), "traceback": traceback.format_exc(), "consumed_file_bindings": observer.reads,
                   "frozen_data_modified": False, "paid_or_private_methods_invoked": False,
                   "interpretation": "Failure of this external observer, not a new scientific run or method result."}
        (out/"failure.json").write_text(json.dumps(failure, indent=2, sort_keys=True)+"\n")
        (out/"stderr.txt").write_text(failure["traceback"])
        raise
    print(json.dumps({"status": result["status"], "attempt": str(out), "summary": result["summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
