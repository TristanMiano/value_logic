"""Reproducible figures from F15's saved descriptive summaries only.

Contributor: ChatGPT (GPT-6 Astra Pro). This reporting module is outside the
F14-v1 frozen dependency closure. It never generates experimental data or
changes a confidence interval. Numerical sources remain the saved JSON files.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "v2/experiments/F15_v1_analysis"
METHODS = ("fresh", "cached_proof", "full_joint", "tailored", "exact_intervals", "marginal_diagnostic")
METHOD_LABELS = ("Fresh full law", "Cached proof + full law", "Full joint moments",
                 "Tailored summary", "Ordinary exact intervals", "Marginals diagnostic")
STRATA = ("mixed_near", "mixed_far", "preserve_other", "equal_target", "scale_separating")
STRATUM_LABELS = ("Mixed, near", "Mixed, far", "Preserve other", "Equal target", "Scale separating")
COLORS = {"supported": "#167b64", "inconclusive": "#9a6900", "violated": "#b23748"}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read(name):
    raw = (DATA / name).read_bytes()
    return json.loads(raw), {"path": str((DATA / name).relative_to(ROOT)), "sha256": digest(raw), "bytes": len(raw)}


def style():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.edgecolor": "#c6ced4", "axes.labelcolor": "#28333d",
                         "xtick.color": "#44535e", "ytick.color": "#44535e",
                         "axes.titleweight": "bold", "svg.hashsalt": "F15-v1-saved-results",
                         "figure.facecolor": "white", "savefig.facecolor": "white"})


def retention_outcomes(method_rows):
    fig, axes = plt.subplots(2, 2, figsize=(12.6, 8.6), gridspec_kw={"wspace": .18, "hspace": .42})
    for panel, access in enumerate(("no_reacquisition", "adaptive_reacquisition")):
        rows = [next(r for r in method_rows if r["method"] == m and r["access"] == access) for m in METHODS]
        assert all(r["method_rows"] == 160 and r["numeric_queries"] == 960 for r in rows)
        for column, (key, fields, labels, colors, xmax) in enumerate((
            ("numeric", ("exact", "approximate", "refused"), ("Exact", "Approximate", "Refused"),
             ("#226b96", "#dfad44", "#cad0d5"), 960),
            ("decisions", ("certified_order", "certified_fallback", "refusal_to_fallback"),
             ("Certified order", "Certified fallback", "Refusal to fallback"),
             ("#238470", "#6683a0", "#cad0d5"), 160),
        )):
            ax = axes[panel, column]
            left = [0] * len(rows)
            for field, label, color in zip(fields, labels, colors):
                widths = [r[key].get(field, 0) for r in rows]
                ax.barh(range(len(rows)), widths, left=left, height=.66, color=color, label=label)
                for y, (start, width) in enumerate(zip(left, widths)):
                    if width:
                        ax.text(start + width / 2, y, str(width), ha="center", va="center", fontsize=8.7,
                                color="white" if field in ("exact", "certified_order", "certified_fallback") else "#27343d")
                left = [a + b for a, b in zip(left, widths)]
            assert left == [xmax] * 6
            ax.set_xlim(0, xmax)
            ax.set_ylim(5.6, -.6)
            ax.set_yticks(range(6), METHOD_LABELS if column == 0 else [""] * 6)
            ax.tick_params(axis="y", length=0, pad=7)
            ax.set_xticks([0, xmax / 4, xmax / 2, 3 * xmax / 4, xmax])
            ax.grid(axis="x", color="#e1e6ea", linewidth=.5)
            ax.set_axisbelow(True)
            ax.set_xlabel("Scalar query dispositions (six per episode)" if column == 0 else "Episode decisions")
            ax.set_title(("No reacquisition" if panel == 0 else "Adaptive reacquisition")
                         + (" · numerical answers" if column == 0 else " · actions"), loc="left", fontsize=11)
            if panel == 0:
                ax.legend(loc="upper left", bbox_to_anchor=(0, 1.25), ncol=3, frameon=False, fontsize=8.7,
                          handlelength=1, columnspacing=1)
    fig.subplots_adjust(left=.195, right=.985, top=.82, bottom=.17)
    fig.suptitle("F15 retention: admissions, approximations and refusals", x=.195, y=.965,
                 ha="left", fontsize=16, fontweight="bold")
    fig.text(.195, .922, "All 1,920 saved method/access rows; 160 episodes per bar from 16 population seeds.", fontsize=10)
    fig.text(.195, .036, "Variants share their seed's law. Refusal is reported separately from a certified fallback.\n"
             "Adaptive repair uses the same priced source capability for every method; its costs are reported separately.",
             color="#52616b", fontsize=9)
    return fig


def identity_intervals(intervals):
    rows = {r["id"]: r for r in intervals}
    fig, axes = plt.subplots(5, 2, figsize=(11.5, 13), sharex=True)
    count = {key: 0 for key in COLORS}
    for model in range(5):
        for role in range(2):
            ax = axes[model, role]
            for y, stratum in enumerate(STRATA):
                row = rows[f"model{model}/identity/{role}/{stratum}/mae"]
                assert row["n"] == 8192 and row["threshold"] == .05
                count[row["disposition"]] += 1
                ax.errorbar(row["mean"], y, xerr=[[row["mean"]-row["lower"]], [row["upper"]-row["mean"]]],
                            fmt="o", markersize=4, capsize=2.5, color=COLORS[row["disposition"]], linewidth=1.4)
            ax.axvline(.05, color="#28333d", linestyle="--", linewidth=1)
            ax.set_xlim(0, .1)
            ax.set_ylim(4.7, -.7)
            ax.set_yticks(range(5), STRATUM_LABELS if role == 0 else [""] * 5)
            ax.tick_params(axis="y", length=0)
            ax.set_title(f"Model {model + 1} · role {role} · evaluation seed {1500491 + model}",
                         fontsize=10, loc="left")
            ax.grid(axis="x", color="#e1e6ea", linewidth=.5)
    assert count == {"supported": 2, "inconclusive": 48, "violated": 0}
    for ax in axes[-1]:
        ax.set_xlabel("Identity intervention probability MAE")
    fig.subplots_adjust(left=.17, right=.975, top=.86, bottom=.135, wspace=.09, hspace=.55)
    fig.suptitle("F15 neural probe: all 50 identity MAE intervals", x=.17, y=.963,
                 ha="left", fontsize=16, fontweight="bold")
    fig.text(.17, .922, "2 supported · 48 inconclusive · 0 MAE tolerance violations", fontsize=12)
    fig.text(.17, .897, "Original simultaneous Hoeffding intervals: family K=560, alpha=.05; 8,192 pairs per cell.", fontsize=9.5)
    fig.legend(handles=[Line2D([0], [0], marker="o", color=COLORS[key], label=key.capitalize(), linewidth=1)
                        for key in ("supported", "inconclusive")], loc="upper right", bbox_to_anchor=(.977, .93),
               frameon=False, fontsize=9)
    fig.text(.17, .036, "Dashed line: frozen MAE tolerance .05. Support requires the upper endpoint at or below it.\n"
             "Complete pilot support is 0/5; decision and matched-control criteria include separate violations.\n"
             "These are conditional results for the five saved models and selected subsets, not all learned representations.",
             color="#52616b", fontsize=9)
    return fig


def control_advantages(intervals):
    rows = {r["id"]: r for r in intervals}
    controls = ("random", "permuted_concept", "shuffled_donor", "untrained")
    names = ("Random subset search", "Permuted-concept search", "Independent wrong donor", "Untrained network")
    fig, axes = plt.subplots(1, 4, figsize=(13, 6.8), sharey=True, sharex=True)
    selected = [rows[f"model{m}/identity/{r}/{control}/advantage"]
                for control in controls for m in range(5) for r in range(2)]
    xmin = min(-.05, min(r["lower"] for r in selected) - .005)
    xmax = max(r["upper"] for r in selected) + .008
    for ax, control, name in zip(axes, controls, names):
        for y, (model, role) in enumerate((m, r) for m in range(5) for r in range(2)):
            row = rows[f"model{model}/identity/{role}/{control}/advantage"]
            assert row["n"] == 40960 and row["threshold"] == .01
            ax.errorbar(row["mean"], y, xerr=[[row["mean"]-row["lower"]], [row["upper"]-row["mean"]]],
                        fmt="o", markersize=4, capsize=2, color=COLORS[row["disposition"]], linewidth=1.3)
        ax.axvline(0, color="#bbc4cb", linewidth=.8)
        ax.axvline(.01, color="#28333d", linestyle="--", linewidth=1)
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(9.7, -.7)
        ax.set_title(name, loc="left", fontsize=10)
        ax.set_xlabel("Control MAE − aligned MAE", fontsize=9)
        ax.grid(axis="x", color="#e1e6ea", linewidth=.5)
        ax.set_yticks(range(10), [f"Model {m + 1} · role {r}" for m in range(5) for r in range(2)])
        ax.tick_params(axis="y", length=0)
    fig.subplots_adjust(left=.12, right=.985, top=.75, bottom=.25, wspace=.13)
    fig.suptitle("F15 neural probe: identity advantage over matched controls", x=.12, y=.95,
                 ha="left", fontsize=15, fontweight="bold")
    fig.text(.12, .90, "Same eight-coordinate capacity and 128-candidate budget; each point pools five equal strata.", fontsize=10)
    fig.legend(handles=[Line2D([0], [0], marker="o", color=COLORS[key], label=key.capitalize(), linewidth=1)
                        for key in COLORS], loc="upper left", bbox_to_anchor=(.115, .87),
               ncol=3, frameon=False, fontsize=9)
    fig.text(.12, .06, "Dashed line: required advantage .01. Support needs a lower endpoint at or above the line.\n"
             "Original K=560 intervals; 40,960 independent pair records per pooled comparison. A red interval's upper endpoint is below .01.\n"
             "The controls test specificity of this selected relation. They do not identify a unique utility representation.",
             color="#52616b", fontsize=9)
    return fig


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    style()
    methods, method_meta = read("retention_by_method.json")
    intervals, interval_meta = read("neural_interval_rows.json")
    assert len(methods) == 12 and len(intervals) == 560
    output = DATA / "figures"
    output.mkdir(exist_ok=True)
    records = []
    for name, fig in (("retention_outcomes", retention_outcomes(methods)),
                      ("neural_identity_intervals", identity_intervals(intervals)),
                      ("neural_control_advantages", control_advantages(intervals))):
        for kind in ("png", "svg"):
            buffer = io.BytesIO()
            metadata = {"Software": "Value Logic F15 saved-results reporting"} if kind == "png" else {
                "Creator": "Value Logic F15 saved-results reporting", "Date": None}
            fig.savefig(buffer, format=kind, dpi=180, metadata=metadata)
            raw = buffer.getvalue()
            path = output / f"{name}.{kind}"
            if args.check:
                assert path.read_bytes() == raw, f"Figure differs: {path}"
            else:
                with path.open("xb") as handle:
                    handle.write(raw)
            records.append({"path": str(path.relative_to(ROOT)), "bytes": len(raw), "sha256": digest(raw)})
        plt.close(fig)
    manifest = {"schema": "F15-saved-figure-manifest-v1", "new_generation": False,
                "new_intervals": 0, "matplotlib_version": matplotlib.__version__,
                "script_sha256": digest(Path(__file__).read_bytes()),
                "inputs": [method_meta, interval_meta], "figures": records}
    raw = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    path = output / "manifest.json"
    if args.check:
        assert path.read_bytes() == raw
    else:
        with path.open("xb") as handle:
            handle.write(raw)
    print(json.dumps({"figures": len(records), "manifest_sha256": digest(raw), "check": args.check}))


if __name__ == "__main__":
    main()
