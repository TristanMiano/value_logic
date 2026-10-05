"""Reproducible standalone ND01 scientific figures from checked saved summaries.

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-05. No new experimental data.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
DEST = HERE / "figures_v2"
INPUTS = {
    "core_summary.json": "5f51177477784de4af33796cf519108f044412c11da1ab787c8601ab0fbb9043",
    "mechanism_results.json": "5f351b68d31d22b28e590827816005774e6bc4a61cb423425c6caf1c00080c1f",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    for name, expected in INPUTS.items():
        assert digest(HERE / name) == expected
    summary = json.loads((HERE / "core_summary.json").read_text())
    mechanism = json.loads((HERE / "mechanism_results.json").read_text())
    DEST.mkdir(exist_ok=False)
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False,
                         "axes.spines.right": False, "figure.facecolor": "white",
                         "axes.titleweight": "bold", "pdf.fonttype": 42})
    fig, axes = plt.subplots(2, 2, figsize=(15.5, 11.5))
    fig.subplots_adjust(left=.15, right=.975, bottom=.16, top=.85,
                        hspace=.64, wspace=.58)
    fig.suptitle("Better extraction, with limits on the representation claim",
                 x=.075, y=.975, ha="left", fontsize=19, weight="bold")
    fig.text(.075, .932,
             "F15-ND01 development diagnostic · five unchanged ordinary networks · original F15 complete support remains 0/5",
             ha="left", fontsize=10.5, color="#444444")
    methods = ["frozen_original", "binary_global", "rounded_top8", "fractional_mask"]
    labels = ["Original F15\nsubset", "Exhaustive\nbinary", "Rounded\nfractional", "Fractional\nmask"]
    lookup = {r["method"]: r for r in summary["masks"]["methods"]}
    colors = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#806000"]
    ax = axes[0, 0]
    for model in range(5):
        for role in (0, 1):
            ys = [next(r["mean_mae"] for r in lookup[method]["role_rows"]
                       if r["model_index"] == model and r["role"] == role)
                  for method in methods]
            ax.plot(range(4), ys, color=colors[model], alpha=.50,
                    marker="o" if role == 0 else "^", linewidth=1.1, markersize=4)
    means = [lookup[method]["mean_mae"] for method in methods]
    ax.plot(range(4), means, color="#191919", linewidth=2.3, marker="D",
            markersize=5, label="Mean of ten model/role rows")
    for x, y in enumerate(means):
        ax.annotate(f"{y:.4f}", (x, y), xytext=(0, -16), textcoords="offset points",
                    ha="center", fontsize=9, weight="bold")
    ax.set_xticks(range(4), labels)
    ax.set_ylim(.015, .052)
    ax.set_ylabel("Probability MAE, equal five-stratum average")
    ax.set_title("A  Single-role interventions improve", loc="left", pad=12)
    ax.grid(axis="y", alpha=.18)
    ax.legend(loc="upper right", frameon=False, fontsize=8)

    ax = axes[0, 1]
    families = ["cost_corr", "log_cost_corr", "positive_contribution_cov", "uniform", "permuted_cost_corr"]
    family_labels = ["Cost correlation", "Log-cost correlation", "Head-aware covariance", "Uniform", "Permuted cost"]
    variants = {r["method"]: r for r in summary["search"]["variants"]}
    for y, family in enumerate(families):
        left = variants[f"{family}/budget_1024/frozen_mse"]["mean_mae"]
        right = variants[f"{family}/budget_128/frozen_mse"]["mean_mae"]
        ax.plot([left, right], [y, y], color="#909090", linewidth=2)
        ax.scatter(right, y, s=45, color="#D55E00", label="128 candidates" if y == 0 else None)
        ax.scatter(left, y, s=45, color="#0072B2", label="1,024 candidates" if y == 0 else None)
    ax.set_yticks(range(5), family_labels)
    ax.invert_yaxis()
    ax.set_xlim(.025, .058)
    ax.set_xlabel("Mean validation probability MAE")
    ax.set_title("B  Wider search helps every proposal family", loc="left", pad=12)
    ax.grid(axis="x", alpha=.18)
    ax.legend(frameon=False, fontsize=8, loc="lower right")

    ax = axes[1, 0]
    controls = [r for r in summary["calibration"]["control_status_counts"]
                if r["hypothesis"] == "identity"]
    ctrl_labels = {"random": "Random search", "permuted_concept": "Permuted concept",
                   "shuffled_donor": "Wrong donor", "untrained": "Untrained"}
    for y, row in enumerate(controls):
        ax.barh(y, row["supported"], color="#009E73", height=.60,
                label="Supported advantage" if y == 0 else None)
        ax.barh(y, row["inconclusive"], left=row["supported"], color="#C7CDD3", height=.60,
                label="Inconclusive" if y == 0 else None)
        ax.text(row["supported"] / 2, y, str(row["supported"]), color="white", ha="center", va="center", weight="bold")
        if row["inconclusive"]:
            ax.text(row["supported"] + row["inconclusive"] / 2, y,
                    str(row["inconclusive"]), ha="center", va="center", weight="bold")
    ax.set_yticks(range(4), [ctrl_labels[r["control"]] for r in controls])
    ax.invert_yaxis()
    ax.set_xlim(0, 10)
    ax.set_xlabel("Constructed-layout/role comparisons (ten total)")
    ax.set_title("C  Accurate controls block complete calibration", loc="left", pad=34)
    ax.text(0, 1.025, "Identity adequate: 5/5 layouts · Complete endpoint: 0/5",
            transform=ax.transAxes, fontsize=9, color="#444444")
    ax.legend(frameon=False, fontsize=8, loc="lower center", bbox_to_anchor=(.5, -.27), ncol=2)

    ax = axes[1, 1]
    joint_methods = ["frozen_original", "binary_global", "fractional_mask"]
    joint_labels = ["Original F15\nsubsets", "Exhaustive\nbinary", "Fractional\nmasks"]
    for model in range(5):
        ys = [next(r["order_probability_rms"] for r in mechanism["secondary_composition"]
                   if r["model_index"] == model and r["method"] == method)
              for method in joint_methods]
        ax.plot(range(3), ys, color=colors[model], marker="o", linewidth=1, alpha=.65, markersize=5)
    joint_means = [float(np.mean([r["order_probability_rms"] for r in mechanism["secondary_composition"]
                                 if r["method"] == method])) for method in joint_methods]
    ax.plot(range(3), joint_means, color="#191919", linewidth=2.2, marker="D", markersize=5)
    ax.set_xticks(range(3), joint_labels)
    ax.set_ylim(-.002, .048)
    ax.set_ylabel("Output RMS difference between the two orders")
    ax.set_title("D  Better single edits need not commute", loc="left", pad=34)
    ax.grid(axis="y", alpha=.18)
    ax.text(0, 1.025, "Secondary joint panel from existing validation arrays",
            transform=ax.transAxes, fontsize=9, color="#444444")

    fig.text(.075, .057,
             "A/B: point estimates on common validation arrays; no new complete-support assessment. "
             "C: original 560-row assessment on constructed calibration layouts.", fontsize=8.8, color="#444444")
    fig.text(.075, .033,
             "D: two donor assignments; lower order difference is better. Thin lines reuse the same five networks. "
             "No retraining, new utility identification or technical-superposition claim.", fontsize=8.8, color="#444444")
    png, pdf = DEST / "diagnostic_overview.png", DEST / "diagnostic_overview.pdf"
    fig.savefig(png, dpi=180, metadata={"Software": f"Matplotlib {matplotlib.__version__}"})
    fig.savefig(pdf, metadata={"Title": "F15-ND01 diagnostic overview", "Author": "ChatGPT (GPT-6 Astra Pro)",
                              "CreationDate": None, "ModDate": None})
    plt.close(fig)
    manifest = {"schema": "F15-ND01-figures-v1", "contributor": "ChatGPT (GPT-6 Astra Pro)",
                "inputs": INPUTS, "script_sha256": digest(Path(__file__)),
                "matplotlib": matplotlib.__version__, "numpy": np.__version__,
                "outputs": [{"file": p.name, "sha256": digest(p), "bytes": p.stat().st_size} for p in (png, pdf)],
                "new_scientific_data": False}
    with (DEST / "manifest.json").open("x") as handle:
        json.dump(manifest, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
