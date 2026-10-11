"""Independent exact checks of saved readable certificates and clipped figure."""
from datetime import datetime, timezone
from decimal import Decimal, localcontext
from fractions import Fraction as Q
import hashlib
from itertools import combinations
import json
from pathlib import Path
import time
import traceback

ROOT = Path("/workspace/scratch/095cdac579b7/value_logic")
W = ROOT / "v3/work_logs/P3_10_2026-10-11_S1"
OWN = W / "reviews/certificate_reconstruction/forecast_action_price_review_v1/readable_figure_review_v1"
OUT = OWN / "observation_v1"
checks = []


def q(pair):
    assert len(pair) == 2 and all(type(x) is int for x in pair) and pair[1] > 0
    return Q(*pair)


def eq(label, actual, expected):
    checks.append({"id": label, "pass": actual == expected})
    if actual != expected:
        raise AssertionError(f"{label}: {actual!r} != {expected!r}")


def encode(v):
    if isinstance(v, Q):
        return [v.numerator, v.denominator]
    if isinstance(v, dict):
        return {str(k): encode(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [encode(x) for x in v]
    return v


def save(path, value):
    with path.open("x") as f:
        json.dump(encode(value), f, indent=2, sort_keys=True)
        f.write("\n")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def vec(row):
    return {"W": q(row["means"]["action_loss_mean"]), "C": q(row["mean_cold_units_per_request"]),
            "B": q(row["means"]["brier_mean"])}


def decvec(v):
    return {k: q(v[k]) for k in ["W", "C", "B"]}


def rounded(x):
    with localcontext() as ctx:
        ctx.prec = 100
        return format(Decimal(x.numerator) / Decimal(x.denominator), ".10f")


def cross(o, a, b):
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])


def hull(points):
    pts = sorted(set(points))
    low, up = [], []
    for seq, target in [(pts, low), (list(reversed(pts)), up)]:
        for p in seq:
            while len(target) >= 2 and cross(target[-2], target[-1], p) <= 0:
                target.pop()
            target.append(p)
    return low[:-1] + up[:-1]


def boundary_vertices(rows):
    found = set()
    for (a, b, d), (aa, bb, dd) in combinations(rows, 2):
        det = a*bb-aa*b
        if det:
            x, y = (d*bb-dd*b)/det, (a*dd-aa*d)/det
            if all(A*x+B*y <= D for A, B, D in rows):
                found.add((x, y))
    return found


def run():
    enrollment = json.loads((OWN / "enrollment.json").read_text())
    for f in enrollment["files"]:
        eq("current.hash:" + f["path"], sha(ROOT / f["path"]), f["sha256"])
        eq("snapshot.hash:" + f["path"], sha(ROOT / f["snapshot"]), f["sha256"])
    summary_path = W / "reviews/broker_reconstruction/findings_tables_A1.json"
    original_path = W / "forecast_action_price_observation_A1/results.json"
    readable_path = W / "forecast_action_price_readable_A1/results.json"
    figure_path = W / "forecast_action_price_figure_A1_v2/manifest.json"
    eq("summary.pin", sha(summary_path), "94f41a247f9fade238028608a221fac39d0a8be56af857de5a4c0c1d8640c3ae")
    eq("original.pin", sha(original_path), "0fa171400460af35bfe2839c3493a30fdfab81811357c08838ec92eb4257a751")
    summary = json.loads(summary_path.read_text())
    original = json.loads(original_path.read_text())
    readable = json.loads(readable_path.read_text())
    figure = json.loads(figure_path.read_text())
    eq("readable.original.binding", readable["source_sha256"], sha(original_path))
    eq("readable.script.binding", readable["script_sha256"], sha(W / "forecast_action_price_readable.py"))
    eq("readable.status", readable["status"], "PASS_SCOPED")
    eq("readable.new.paid", readable["new_paid_runs"], 0)
    eq("readable.endpoint.gate.unchanged", readable["fixed_primary_endpoint_or_global_economic_gate_changed"], False)
    eq("figure.original.binding", figure["source_sha256"], sha(original_path))
    eq("figure.readable.binding", figure["readable_sha256"], sha(readable_path))
    eq("figure.script.binding", figure["script_sha256"], sha(W / "plot_forecast_action_price_v2.py"))
    eq("figure.new.paid", figure["new_paid_executions"], 0)
    for f in figure["files"]:
        p = figure_path.parent / f["path"]
        eq("figure.render.hash:" + f["path"], sha(p), f["sha256"])
        eq("figure.render.bytes:" + f["path"], p.stat().st_size, f["bytes"])
    rows = [r for r in summary["all_configuration_summaries"] if r["stakes"] == {"fn": [1, 1], "fp": [1, 1]}]
    by_key = {(r["family"], r["configuration_id"]): r for r in rows}
    ordinary = {family: {r["configuration_id"]: vec(r) for r in rows if r["family"] == family and r["method_kind"] == "ordinary"}
                for family in ["cheap_null", "mixed", "gate_transfer"]}
    orig = {(c["family"], c["candidate_id"]): c for c in original["cases"]}
    rcases = {(c["family"], c["candidate_id"]): c for c in readable["cases"]}
    eq("readable.exact.cell.roster", set(rcases), set(orig))
    eq("readable.no.duplicates", len(rcases), len(readable["cases"]))
    strict, convex = [], []
    for key, r in rcases.items():
        label = ":".join(key)
        candidate = vec(by_key[key])
        eq(label + ":candidate", decvec(r["candidate"]), candidate)
        ov = ordinary[key[0]]
        eq(label + ":full.catalogue", len(ov), 19)
        if r["kind"] == "strict illustrative point":
            eq(label + ":was.feasible", orig[key]["feasible"], True)
            x, y = q(r["lambda_value"]), q(r["mu_value"])
            eq(label + ":nonnegative.prices", x >= 0 and y >= 0, True)
            ck = candidate["W"]+x*candidate["C"]+y*candidate["B"]
            ok = {i: o["W"]+x*o["C"]+y*o["B"] for i, o in ov.items()}
            best = min(ok.values())
            names = sorted(i for i, v in ok.items() if v == best)
            gap = best-ck
            eq(label + ":all.ordinary.K", {i: q(v) for i, v in r["all_19_ordinary_scores"].items()}, ok)
            eq(label + ":candidate.K", q(r["candidate_K"]), ck)
            eq(label + ":minimum.K", q(r["minimum_ordinary_K"]), best)
            eq(label + ":minimum.margin", q(r["minimum_strict_margin"]), gap)
            eq(label + ":all.tied.minimizers", sorted(r["ordinary_minimizers"]), names)
            eq(label + ":strict.gap", gap > 0, True)
            strict.append({"family": key[0], "candidate_id": key[1], "lambda": x, "mu": y,
                           "candidate_K": ck, "minimum_ordinary_K": best, "strict_gap": gap,
                           "ordinary_minimizers": names})
        else:
            eq(label + ":kind", r["kind"], "strict three-coordinate convex certificate")
            eq(label + ":was.empty", orig[key]["feasible"], False)
            weights = {i: q(v) for i, v in r["weights"].items()}
            eq(label + ":positive.weights", all(v > 0 for v in weights.values()), True)
            eq(label + ":weights.sum", sum(weights.values(), Q(0)), Q(1))
            combined = {k: sum((v*ov[i][k] for i, v in weights.items()), Q(0)) for k in candidate}
            gap = {k: candidate[k]-combined[k] for k in candidate}
            eq(label + ":combined", decvec(r["combined_coordinates"]), combined)
            eq(label + ":gaps", decvec(r["candidate_minus_combination"]), gap)
            eq(label + ":all.three.strict", all(v > 0 for v in gap.values()), True)
            eq(label + ":unpaid", r["paid_randomized_controller_executed"], False)
            convex.append({"family": key[0], "candidate_id": key[1], "weights": weights,
                           "candidate_minus_combination": gap, "combined": combined})
    eq("strict.points.count", len(strict), 3)
    eq("convex.certificates.count", len(convex), 9)
    eq("single.ordinary.certificates", sum(len(c["weights"]) == 1 for c in convex), 5)
    eq("two.ordinary.certificates", sum(len(c["weights"]) == 2 for c in convex), 4)
    # Independently check every displayed numerical cell, with decimal rounding.
    text = (W / "forecast_action_price_readable_A1/interpretation.md").read_text()
    lines = [[v.strip() for v in line.strip().strip("|").split("|")] for line in text.splitlines()
             if line.startswith("| cheap_null |") or line.startswith("| mixed |") or line.startswith("| gate_transfer |")]
    eq("readable.table.rows", len(lines), 12)
    for cells in lines:
        key = (cells[0], cells[1])
        r = rcases[key]
        if len(cells) == 8:
            expected = [str(q(r["lambda_value"])), str(q(r["mu_value"])), rounded(q(r["candidate_K"])),
                        rounded(q(r["minimum_ordinary_K"])), rounded(q(r["minimum_strict_margin"])),
                        ", ".join(r["ordinary_minimizers"])]
            eq(":".join(key) + ":displayed.point", cells[2:], expected)
        else:
            eq(":".join(key) + ":convex.table.width", len(cells), 6)
            displayed = {}
            for term in cells[2].split(" + "):
                weight, name = term.split(" ", 1)
                displayed[name] = Q(weight)
            eq(":".join(key) + ":displayed.weights", displayed, {i: q(v) for i, v in r["weights"].items()})
            eq(":".join(key) + ":displayed.gaps", cells[3:], [rounded(q(r["candidate_minus_combination"][k])) for k in ["W", "C", "B"]])
    clipped = []
    for panel in figure["panels"]:
        key = (panel["family"], panel["candidate"])
        cv, ov = vec(by_key[key]), ordinary[key[0]]
        xmax, ymax = q(panel["viewport"]["lambda_max"]), q(panel["viewport"]["mu_max"])
        constraints = [(Q(-1), Q(0), Q(0)), (Q(0), Q(-1), Q(0)),
                       (Q(1), Q(0), xmax), (Q(0), Q(1), ymax)]
        constraints += [(cv["C"]-o["C"], cv["B"]-o["B"], o["W"]-cv["W"]) for o in ov.values()]
        exact = boundary_vertices(constraints)
        saved = [(q(p[0]), q(p[1])) for p in panel["exact_clipped_vertices"]]
        label = ":".join(key)
        eq(label + ":all.clipped.vertices", set(saved), exact)
        eq(label + ":unique.clipped.vertices", len(saved), len(exact))
        poly = hull(exact)
        rotations = [poly[i:]+poly[:i] for i in range(len(poly))]
        eq(label + ":convex.ccw.order", saved in rotations, True)
        area = sum((p[0]*qq[1]-p[1]*qq[0] for p, qq in zip(poly, poly[1:]+poly[:1])), Q(0))/2
        eq(label + ":positive.viewport.area", area > 0, True)
        point = rcases[key]
        x, y = q(point["lambda_value"]), q(point["mu_value"])
        eq(label + ":plotted.point.in.viewport", 0 <= x <= xmax and 0 <= y <= ymax, True)
        eq(label + ":plotted.point.strict.ordinary", all(a*x+b*y < d for a, b, d in constraints[4:]), True)
        clipped.append({"family": key[0], "candidate_id": key[1], "viewport": {"lambda_max": xmax, "mu_max": ymax},
                        "vertices": saved, "exact_area": area})
    eq("figure.region.count", len(clipped), 3)
    eq("figure.vertex.count", sum(len(c["vertices"]) for c in clipped), 15)
    gate_cold = vec(by_key[("gate_transfer", "value_tickets_cold")])
    gate_cached = vec(by_key[("gate_transfer", "value_tickets_cached_hashed")])
    eq("gate.ticketed.WB.identity", (gate_cold["W"], gate_cold["B"]), (gate_cached["W"], gate_cached["B"]))
    eq("gate.ticketed.cold.cost.lower", gate_cold["C"] < gate_cached["C"], True)
    section = (OWN / "results_section_4_4_snapshot.md").read_text()
    eq("section.snapshot.hash", hashlib.sha256(section.encode()).hexdigest(), enrollment["section_4_4_sha256"])
    current = (ROOT / "v3/experiments/results.md").read_text()
    start = current.index("### 4.4 ")
    end = current.index("\n## 5.", start)
    eq("section.unchanged", current[start:end], section)
    mapping = {"Mixed, uniform cold": ("mixed", "value_uniform_cold"),
               "Gate, ticketed cold": ("gate_transfer", "value_tickets_cold"),
               "Gate, ticketed cached": ("gate_transfer", "value_tickets_cached_hashed")}
    section_rows = [[v.strip() for v in line.strip().strip("|").split("|")] for line in section.splitlines()
                    if any(line.startswith("| " + name + " |") for name in mapping)]
    eq("section.illustrative.rows", len(section_rows), 3)
    for cells in section_rows:
        r = rcases[mapping[cells[0]]]
        eq(cells[0] + ":section.numbers", cells[1:], [str(q(r["lambda_value"])), str(q(r["mu_value"])),
           rounded(q(r["candidate_K"])), rounded(q(r["minimum_ordinary_K"])), "+" + rounded(q(r["minimum_strict_margin"]))])
    for f in enrollment["files"]:
        eq("unchanged:" + f["path"], sha(ROOT / f["path"]), f["sha256"])
    return {"status": "PASS", "strict_points": strict, "convex_certificates": convex, "figure_regions": clipped,
            "strict_point_count": 3, "strict_ordinary_score_comparisons": 57,
            "single_ordinary_certificate_count": 5, "two_ordinary_certificate_count": 4,
            "strict_coordinate_gaps": 27, "readable_table_rows_checked": 12, "results_section_rows_checked": 3,
            "figure_clipped_vertices": 15, "results_section_4_4_sha256": enrollment["section_4_4_sha256"],
            "gate_ticketed_cached_minus_cold_C": gate_cached["C"]-gate_cold["C"],
            "new_paid_runs": 0, "new_truth_generations": 0, "principal_script_runs": 0,
            "principal_research_credit_seconds": 0,
            "scope": "Saved fixed-record witnesses, mathematical combinations and exact clipped geometry only; no changed endpoint, practical flag, controller or global gate."}


def main():
    OUT.mkdir(exist_ok=False)
    start, clock = datetime.now(timezone.utc).isoformat(), time.perf_counter_ns()
    failed = False
    try:
        result = run()
    except Exception as exc:
        failed = True
        (OUT / "failure_traceback.txt").write_text(traceback.format_exc())
        result = {"status": "OBSERVER_FAILURE_PRESERVED", "error_type": type(exc).__name__, "error": str(exc)}
    result.update({"reviewer": "ChatGPT (GPT-6 Astra Pro), /root/certificate_reconstruction",
                   "schema": "p310.independent_readable_price_figure_check.v1",
                   "started_utc": start, "finished_utc": datetime.now(timezone.utc).isoformat(),
                   "elapsed_ns": time.perf_counter_ns()-clock, "checks": len(checks),
                   "failed_checks": sum(not c["pass"] for c in checks), "principal_research_credit_seconds": 0})
    save(OUT / "results.json", result)
    save(OUT / "check_log.json", checks)
    save(OUT / "run_manifest.json", {"source_sha256": sha(Path(__file__)),
         "files": [{"path": str(p.relative_to(ROOT)), "sha256": sha(p), "bytes": p.stat().st_size}
                   for p in sorted(OUT.iterdir()) if p.is_file()]})
    print(json.dumps({k: result[k] for k in ["status", "checks", "failed_checks", "elapsed_ns"]}, sort_keys=True))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
