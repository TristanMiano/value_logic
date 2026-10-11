"""Exact halfplane clipping; float rendering only for a fixed-record figure.

ChatGPT (GPT-6 Astra Pro), principal /root, 2026-10-11.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
import os

os.environ.setdefault("MPLCONFIGDIR", "/workspace/scratch/p310_matplotlib_cache")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

W = Path(__file__).resolve().parent
SOURCE = W / "forecast_action_price_observation_A1/results.json"
READABLE = W / "forecast_action_price_readable_A1/results.json"
OUT = W / "forecast_action_price_figure_A1_v2"


def encode(v):
    if isinstance(v, F):
        return [v.numerator, v.denominator]
    if isinstance(v, dict):
        return {k: encode(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [encode(x) for x in v]
    return v


def clip(polygon, constraint):
    a, b, d = [F(*constraint[k]) for k in ["a", "b", "d"]]
    result = []
    for previous, current in zip(polygon[-1:]+polygon[:-1], polygon):
        ps = d-a*previous[0]-b*previous[1]
        cs = d-a*current[0]-b*current[1]
        if (ps >= 0) != (cs >= 0):
            t = ps/(ps-cs)
            crossing = tuple(p+t*(q-p) for p, q in zip(previous, current))
            assert a*crossing[0]+b*crossing[1] == d
            result.append(crossing)
        if cs >= 0:
            result.append(current)
    return result


def main():
    OUT.mkdir(exist_ok=False)
    data, readable = json.loads(SOURCE.read_text()), json.loads(READABLE.read_text())
    assert data["status"] == readable["status"] == "PASS_SCOPED"
    assert readable["source_sha256"] == sha256(SOURCE.read_bytes()).hexdigest()
    rows = {(r["family"], r["candidate_id"]): r for r in data["cases"]}
    points = {(r["family"], r["candidate_id"]): r for r in readable["cases"] if r["kind"] == "strict illustrative point"}
    style = {"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False,
             "axes.spines.right": False, "axes.titleweight": "bold", "svg.fonttype": "none"}
    plt.rcParams.update(style)
    fig, axes = plt.subplots(1, 2, figsize=(11.8, 6.3))
    fig.subplots_adjust(left=.065, right=.99, bottom=.23, top=.82, wspace=.20)
    panels = [("mixed", "Mixed CNF: uniform, cold", F(3,25000), F(60), ["value_uniform_cold"]),
              ("gate_transfer", "Gate CNF: ticketed", F(3,25000), F(420),
               ["value_tickets_cold", "value_tickets_cached_hashed"])]
    records = []
    for ax, (family, title, xmax, ymax, candidates) in zip(axes, panels):
        ax.set_facecolor("#f8fafc")
        ax.set_title(title, loc="left", pad=14)
        for index, name in enumerate(candidates):
            r = rows[(family, name)]
            polygon = [(F(0), F(0)), (xmax,F(0)), (xmax,ymax), (F(0),ymax)]
            for constraint in r["constraints"]:
                polygon = clip(polygon, constraint)
                if not polygon:
                    break
            assert polygon
            for x, y in polygon:
                assert 0 <= x <= xmax and 0 <= y <= ymax
                assert all(F(*c["a"])*x+F(*c["b"])*y <= F(*c["d"]) for c in r["constraints"])
            coords = [(float(x)*100000, float(y)) for x, y in polygon]
            if index == 0:
                patch = Polygon(coords, closed=True, facecolor="#bae6fd", edgecolor="#0369a1",
                                linewidth=1.8, label="Cold: weak minimum region")
            else:
                patch = Polygon(coords, closed=True, facecolor="none", edgecolor="#b45309",
                                linewidth=1.5, linestyle="--", label="Cached: weak minimum boundary")
            ax.add_patch(patch)
            p = points[(family, name)]
            x, y = F(*p["lambda_value"]), F(*p["mu_value"])
            if index == 0:
                ax.scatter([float(x)*100000], [float(y)], s=65, color="#172554", marker="*", zorder=5,
                           label="Checked strict example")
                ax.annotate(f"({float(x)*100000:g}, {float(y):g})", (float(x)*100000,float(y)),
                            xytext=(9, 6), textcoords="offset points", fontsize=9, color="#172554")
            records.append({"family": family, "candidate": name, "viewport": {"lambda_max": xmax, "mu_max": ymax},
                            "exact_clipped_vertices": polygon})
        ax.set_xlim(0, float(xmax)*100000)
        ax.set_ylim(0, float(ymax))
        ax.set_xlabel("Resource price λ (axis units of 10⁻⁵)")
        ax.set_ylabel("Additional issued-Brier weight μ")
        ax.grid(color="#cbd5e1", alpha=.55, linewidth=.6)
        ax.set_axisbelow(True)
        ax.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="#e2e8f0", fontsize=8)
    fig.suptitle("Valuing the issued forecast changes the fixed-record comparison", x=.015, ha="left", fontsize=15, weight="bold")
    fig.text(.065, .035, "Post-outcome K = W + λC + μB. Each region compares with all 19 distinct ordinary configurations.\n"
                  "Regions continue outside the viewport; boundaries include ties. No paid policy was rerun.\n"
                  "All candidates lose the frozen μ = 0 comparison. The unknown outer-cost gate remains false.",
                  fontsize=9, color="#334155", ha="left", va="bottom")
    for suffix in ["svg", "png"]:
        fig.savefig(OUT/("forecast_action_price_regions."+suffix), dpi=160, bbox_inches="tight",
                    metadata={"Creator": "ChatGPT (GPT-6 Astra Pro)"} if suffix=="svg" else {"Software": "ChatGPT (GPT-6 Astra Pro)"})
    plt.close(fig)
    manifest = {"status": "PASS_SCOPED", "contributor": "ChatGPT (GPT-6 Astra Pro), principal /root",
                "signed_utc": datetime.now(timezone.utc).isoformat(), "matplotlib": matplotlib.__version__,
                "source_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
                "readable_sha256": sha256(READABLE.read_bytes()).hexdigest(),
                "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
                "coordinate_policy": "Rational clipping and membership checks; only final rendering uses floats",
                "render_revision": "V2 gives the caption dedicated space; original V1 image, exact geometry and source remain preserved.",
                "panels": records, "new_paid_executions": 0,
                "files": [{"path": p.name, "bytes": p.stat().st_size, "sha256": sha256(p.read_bytes()).hexdigest()}
                          for p in sorted(OUT.iterdir())]}
    (OUT/"manifest.json").write_text(json.dumps(encode(manifest), indent=2)+"\n")
    print(json.dumps({"status": manifest["status"], "panels": 2, "regions": 3}))


if __name__ == "__main__":
    main()
