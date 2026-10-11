#!/usr/bin/env python3
"""Assemble a source-only review; no scientific implementation is imported or run."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[6]
HERE = Path(__file__).resolve().parent
OWNER = "ChatGPT (GPT-6 Astra Pro), /root/conformance_reconstruction"
REVIEW_ROOT = "v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction"
FROZEN = "v3/experiments/frozen_v1/source/"

SOURCES = {
    "PI": (FROZEN + "v3/derivations/02_probability_information.md", "frozen theorem statements"),
    "AUD": (FROZEN + "v3/checks/02_finite_information_audit.py", "frozen information implementation"),
    "VER": (FROZEN + "v3/checks/02_finite_information_verify.py", "frozen independent arithmetic verifier"),
    "CF": ("v3/derivations/04_counterfactual_semantics.md", "current theoretical source; separately byte bound"),
    "TR": ("v3/derivations/05_counterfactual_transport.md", "current theoretical source; separately byte bound"),
    "ADD": (FROZEN + "v3/derivations/05_equal_certificate_delivery.md", "frozen separate receiving-service theorem"),
    "S": (FROZEN + "v3/experiments/p308_structural.py", "frozen structural fixture and policy source"),
    "C": (FROZEN + "v3/experiments/p309_conformance.py", "frozen conformance roster and adapter"),
    "O": (REVIEW_ROOT + "/observer_v4.py", "previously executed independent observer source; not rerun"),
    "R": (REVIEW_ROOT + "/REVIEW.md", "previous signed conformance result review; counts cited without reopening final payloads"),
    "D": (REVIEW_ROOT + "/duty_attachment_v1/output/attachment.md", "previous read-only accepted-duty attachment"),
}

INFORMATION = [
    {
        "id": "I1", "hypothesis": "Exact finite request and input identity",
        "checked": "36 requests: exact rational rows, dimensions, mode, requested targets, and certificate-to-request binding. Six named malformed requests are rejected. The independent observer also recomputes summary ranks.",
        "supplied_or_unchecked": "The supplied loss rows really mean those statewise quantities; a numerical type check cannot establish that meaning. The six controls exercise only their named schema boundaries.",
        "sources": "AUD audit; VER verify; C _information_binding; O verify_information; R §§ Evidence, Six invalid-input controls",
    },
    {
        "id": "I2", "hypothesis": "Global linear-target recovery and normalization (PI-1, PI-2)",
        "checked": "Affine row identities and every required law coordinate are checked. Known-scale recovery uses row([1; M]); normalization is retained. Prior results: 20/36 full-law designs and 22/36 complete target families recoverable.",
        "supplied_or_unchecked": "The source is the full normalized real simplex, the target is the declared linear family, and the observation is an exact expectation map. The necessity argument uses the simplex's interior. Twelve one-state designs are forced by normalization; four empty-target flags are vacuous.",
        "sources": "PI §§2, 4, 19; AUD target_certificate; O recoverable, verify_information; R § Information findings",
    },
    {
        "id": "I3", "hypothesis": "Shared nuisance and valid ratio denominator (PI-10)",
        "checked": "Offset differences M and the identities alpha M = 1 and beta M = c are checked for nonconstant unknown-scale targets. Witness scales are positive and known nuisance values remain fixed. An independent-row-scale tag is rejected.",
        "supplied_or_unchecked": "One common positive scale s and, when unknown, one unrestricted common offset b apply to every row; known units were correctly removed. The denominator equals s under that contract. No future numerical observation or empirical shared-unit premise is tested.",
        "sources": "PI §10; AUD module contract; VER verify_target; O verify_target",
    },
    {
        "id": "I4", "hypothesis": "A collision defeats global exact decoding, not every local fiber",
        "checked": "43 negative proof components: 27 target collisions and 16 law obstructions have interior normalized p and q, allowed nuisances, equal raw observations, and unequal targets.",
        "supplied_or_unchecked": "Both witnesses are admissible because the full simplex is declared. A smaller or nonconvex source, bounded nuisance, or a particular boundary observation can identify more. Nonidentification does not mean that a record has no statistical information or that every observation is ambiguous.",
        "sources": "PI PI-1, PI-3, PI-4, PI-10 and §16; VER verify_target; R § What the exact certificates establish",
    },
    {
        "id": "I5", "hypothesis": "Sharp additional-query repair (PI-17)",
        "checked": "The independent rank deficit, raw-row construction, B h_j = 0, q_i h_j = delta_ij, and all repaired target identities are checked. Fourteen designs need positive repair; their minimum counts total 24 additional raw rows.",
        "supplied_or_unchecked": "Additional rows may be any fixed known rational losses, with the same law and nuisance as the old rows. These are proposed measurement designs, not 24 acquired observations. No restricted purchase menu, noisy acquisition, adaptive policy, bit cost, or paid access guarantee is established; exact target recovery need not recover the whole law or offset.",
        "sources": "PI §18; VER verify repair block; O verify_information; R § What the exact certificates establish",
    },
    {
        "id": "I6", "hypothesis": "Expected loss versus observed finite forecast accuracy",
        "checked": "The audit accepts L, C, n and a calibration tag, not a sample or forecast-truth transcript. The 36 accepted certificates check algebraic designs. They contain 138 positive proof components, not 138 independent prediction successes.",
        "supplied_or_unchecked": "Actual values must be exact expectations under one supplied law. A common realized batch has means L p_hat and an inverse recovers that empirical law; population accuracy needs a separate sampling/error argument. The 20/36 fraction is neither an accuracy rate nor evidence of learning, calibration, or broker improvement.",
        "sources": "PI §§2, 16, 19; AUD module contract; C run; R § Information findings",
    },
]

STRUCTURAL = [
    {
        "id": "S1", "hypothesis": "Declared finite hypothetical semantics",
        "checked": "For 9 fixtures under both methods, the previous observer evaluates the original quoted antecedent, paired support or explicit routing, hard commitments, ranks and losses. It reconstructs all 18 complete terminal replies from the fixture definitions.",
        "supplied_or_unchecked": "The finite grammar, baseline, exceptions, weights, hard frames, action menu, loss meanings and copy/predictor routing are supplied. Correct evaluation does not infer the causal graph, justify relevance weights, or make a paired-support case an ordinary world or a truth probability.",
        "sources": "CF §§2–4; S fixtures, candidate_compile, ordinary_compile; O reconstruct_structural; R § Structural findings",
    },
    {
        "id": "S2", "hypothesis": "All ties and all declared unresolved sources",
        "checked": "The completed search/enumerator retains rank equality and the observer reconstructs every finite minimizer and loss image. The tied fixture retains both minima; the external-source fixture retains both sources despite minimum ranks 1 and 2.",
        "supplied_or_unchecked": "The declared domain and source roster exhaust the intended alternatives. Repair rank is minimized separately inside each source. These completions do not newly test interrupted-frontier coverage at arbitrary budgets, or justify discarding ties in another service.",
        "sources": "CF C04-5–6; TR §2; S solve_candidate, solve_ordinary, choose_fixed_action; O reconstruct_structural",
    },
    {
        "id": "S3", "hypothesis": "Established nonempty target before an action warrant",
        "checked": "Seven nonempty fixtures per method give 14 action warrants. Fixed falsity and impossible ordinary conditioning give 4 complete infeasibility replies and no useful action. The choice function refuses an action if any retained source lacks a nonempty target.",
        "supplied_or_unchecked": "This is exhaustive infeasibility in the declared finite domain. An empty implication or an interrupted search without a witness cannot replace nonemptiness. The 60-unit roster does not add low-budget structural failure controls.",
        "sources": "CF §2 and C04-5–6; S choose_fixed_action; C units, default_config; R § Evidence and denominator",
    },
    {
        "id": "S4", "hypothesis": "Fixed minimax choice versus pointwise non-deterioration",
        "checked": "The selected action minimizes its maximum loss over all retained source/minimum pairs. Candidate and ordinary return the same action. The record explicitly refuses the hidden-case action oracle.",
        "supplied_or_unchecked": "Minimax is the supplied consumer policy. Lower maximum absolute loss does not prove a nonpositive same-case loss difference against every alternative. A named baseline and a bound on that difference are needed for uniform non-deterioration; see the concrete example below.",
        "sources": "CF §4 and C04-6; TR CT05-1; S choose_fixed_action; O reconstruct_structural",
    },
    {
        "id": "S5", "hypothesis": "Whole incumbent-sublevel receiving certificate",
        "checked": "No ADD current-bound receipt is produced by these 18 structural conformance calls. Their complete minimizer identities are a separate local service. The source roster calls run_method, not transport_development or the ADD receiving service.",
        "supplied_or_unchecked": "The separate receiving theorem needs a checked feasible incumbent w, the complete current request and D, and a checked bound on every feasible x with rank(x) <= rank(w), including nonoptimal points and ties. When B <= 0 and D is the intended fixed-pair loss difference, this implies non-deterioration on the minima. Minimizer-only answers do not establish the larger sublevel bound.",
        "sources": "ADD §§1–2.3; CF C04-5–6; C run; S run_method, transport_development",
    },
    {
        "id": "S6", "hypothesis": "Reuse or repair after an edit (CT05-1, CT05-2, CT05-5)",
        "checked": "The fixture requests bind their complete current source and routing, and different routing masks give their declared outcomes. These 60 calls do not exercise an old-certificate admission, edit chain, domain-coverage bridge or repaired receipt.",
        "supplied_or_unchecked": "Reuse needs valid old proof domains, a current feasible witness, a checked map into the old domain, the rank-drift/cutoff inequality, and a positive-unit numerical loss bridge covering every new minimum and unresolved source. A repaired allowance must still be <= 0 to warrant non-deterioration. Old winners, source names or a surviving candidate alone do not supply those premises.",
        "sources": "TR §§2–3, 8; CF §7.2; S source_scope, fixtures; C run",
    },
]


def digest(data):
    return sha256(data).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n")


def matrix_md(rows):
    lines = [
        "| ID and hypothesis | Checked in the existing 60-fixture reconstruction | Supplied by construction or outside this evidence | Source |",
        "|---|---|---|---|",
    ]
    for row in rows:
        refs = row["sources"]
        for key in sorted(SOURCES, key=len, reverse=True):
            # Only complete source-label tokens are linked; function/theorem names remain plain text.
            import re
            refs = re.sub(r"(?<![A-Za-z0-9_\[])" + key + r"(?![A-Za-z0-9_\]])", f"[{key}]", refs)
        cells = [f"**{row['id']} — {row['hypothesis']}**", row["checked"], row["supplied_or_unchecked"], refs]
        lines.append("| " + " | ".join(cell.replace("|", "\\|") for cell in cells) + " |")
    return "\n".join(lines)


def main():
    if not (REPO / "v3/experiments/p309_conformance.py").is_file():
        raise RuntimeError("Repository root not found; do not write elsewhere.")
    out = HERE / "output"
    out.mkdir(exist_ok=False)
    snapshot_dir = out / "source_snapshots"
    snapshot_dir.mkdir()
    bindings = {}
    for label, (relative, role) in SOURCES.items():
        source = REPO / relative
        data = source.read_bytes()
        snapshot = snapshot_dir / (label + "__" + source.name)
        snapshot.write_bytes(data)
        bindings[label] = {"path": relative, "role": role, "bytes": len(data), "sha256": digest(data),
                           "snapshot": str(snapshot.relative_to(out))}
    if bindings["O"]["sha256"] != "172aee16c019122fe3feaae12e0601cf41681f070a7ed7761c08fa7bedf227a8":
        raise RuntimeError("Previously reviewed observer changed.")
    if bindings["R"]["sha256"] != "8785d5c4f295930d4e66aba233c1186078f607a72402297668a6c57637545b63":
        raise RuntimeError("Previously signed review changed.")
    now = datetime.now(timezone.utc).isoformat()
    review = {
        "schema": "p310.conformance.assumption-matrix.v1", "signed_by": OWNER,
        "created_at_utc": now, "review_kind": "source-only assumption and implication review",
        "principal_clock_seconds": 0, "new_scientific_executions": 0,
        "new_final_payload_reads": 0, "accepted_status_changes": [], "gate_changes": [],
        "scope": "P3-10-A1 inherited conformance; no P3-11, no author gate, no official/source edits",
        "previous_denominators": {"structural": 18, "valid_information": 36, "invalid_controls": 6, "total": 60},
        "information_matrix": INFORMATION, "structural_matrix": STRUCTURAL,
        "source_bindings": bindings,
    }
    dump(out / "matrix.json", review)
    md = rf"""# P3-10-A1 conformance: assumption and implication matrix

**Signed:** {OWNER}, {now}. **Source-only review; zero principal clock credit.**

The 60 known fixtures support conditional finite conformance. They do not turn exact information-design recovery into forecast accuracy, or a minimax choice into a uniform non-deterioration certificate. These are boundaries between declared services, not newly found execution defects.

The denominator is unchanged: **18 structural replies (9 fixtures × 2 methods), 36 valid information certificates (9 designs × 4 calibration modes), and 6 expected invalid-input controls**. “Checked” below refers to the completed independent reconstruction reported in [R] and its inspected source [O]; it does not mean this review reran that observer. This pass read source/theorem text and the previous signed reviews, with no final scientific payload reopened and no generator, paid worker, scorer, analyzer, or empirical experiment run. The frozen adapter itself labels these inputs inherited conformance, never unseen transfer. [C]

## Information recovery

{matrix_md(INFORMATION)}

The global statements concern all admitted laws and nuisances, although each numerical certificate is finite. A positive row identity gives that conditional general conclusion algebraically; a verified same-record pair defeats a uniform exact decoder algebraically. The finite fixture tally tests the implementation on known designs and is not a statistical estimate of either theorem. The original verifier checks identities and collisions but does not independently certify its summary rank fields; the completed observer additionally recomputed those ranks. [PI] §19; [VER]; [O]

## Structural actions, ties and repair

{matrix_md(STRUCTURAL)}

### The minimax distinction is material in a named fixture

Let U contain every declared source together with each of its minimum-ranked cases. The implemented policy chooses one action a* before resolving U and ensures

```math
M(a^*)=\min_{{a\in A}} M(a),\qquad M(a)=\max_{{(s,x)\in U}}\ell_a(s,x).
```

For a named baseline b, pointwise non-deterioration instead requires

```math
\max_{{(s,x)\in U}}\bigl(\ell_{{a^*}}(s,x)-\ell_b(s,x)\bigr)\le0.
```

In `counterpossible_tied_minima`, the two complete minima have losses `(4,0,3)` and `(0,4,3)` for `(take_p,take_r,fallback)`. Fallback minimizes the maximum at 3 rather than 4. Against `take_p`, however, its two differences are -1 and 3, so the uniform difference bound is **+3**, not nonpositive. The minimax result is correct for its declared policy; `useful_action_warrant` does not assert that fallback dominates every alternative in each case. Equality of the candidate and ordinary actions also gives no decision-quality gain between them. [S] `fixtures`, `choose_fixed_action`; [O] `reconstruct_structural`; [R] § Structural findings

For the separate incumbent-sublevel service, a feasible w gives nonempty Q_F(w) and includes every true minimum. A bound D <= B on all of Q_F(w) therefore transfers to every minimum; B <= 0 yields non-deterioration only when D is the intended, current, fixed-pair loss difference. It does not require w to be optimal or enumerate all minimizing identities. After an edit, the old sublevel implication needs a valid current domain/quantity bridge; a repaired positive upper bound is still a bound but no longer certifies non-deterioration. These statements are the explicit hypotheses of [ADD] §§1–2.3 and [TR] CT05-1–2, not new observations in the 60-fixture arm.

## Reporting consequence and unchanged status

Report the information numbers as conditional design-level recovery/nonidentification and minimum freely chosen query repairs. Report the structural numbers as complete finite answers and fixed minimax decisions on supplied hypothetical semantics. The 18 invoices remain measurements of the declared fixture worker tariff; no general runtime, total experimental economy or action-learning theorem follows. This note supplements the read-only duty attachment [D], preserving every accepted status and residual. It makes no author-gate, novelty or P3-11 judgment.

## Source binding

`manifest.json` binds this note, the structured matrix, the assembly source and all reviewed source snapshots by SHA-256. CF and TR are current theoretical files, separately preserved here; the other theorem/worker sources cited as frozen are the exact frozen copies. R supplies only the already signed reconstruction findings. The assembly script performs file copying, hashing and document generation only.

"""
    for label, binding in bindings.items():
        md += f"[{label}]: sandbox:{REPO / binding['path']}\n"
    (out / "matrix.md").write_text(md)
    artifacts = []
    for path in sorted(out.rglob("*")):
        if path.is_file():
            data = path.read_bytes()
            artifacts.append({"path": str(path.relative_to(out)), "bytes": len(data), "sha256": digest(data)})
    builder = Path(__file__).resolve().read_bytes()
    manifest = {"schema": "p310.conformance.assumption-matrix.manifest.v1", "signed_by": OWNER,
                "created_at_utc": now, "principal_clock_seconds": 0,
                "assembly_source": {"path": str(Path(__file__).resolve().relative_to(REPO)),
                                    "bytes": len(builder), "sha256": digest(builder)},
                "artifacts": artifacts, "source_bindings": bindings,
                "official_mutations": [], "new_scientific_executions": 0}
    dump(out / "manifest.json", manifest)
    for name in ("matrix.md", "matrix.json", "manifest.json"):
        data = (out / name).read_bytes()
        print(json.dumps({"artifact": str((out / name).relative_to(REPO)), "bytes": len(data), "sha256": digest(data)}))


if __name__ == "__main__":
    main()
