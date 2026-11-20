"""Run the W7 mathematical examples and optionally every archived-data comparison."""
import argparse
from pathlib import Path
import subprocess
import sys


NOTEBOOK = Path(__file__).resolve().parent
# Run the small self-contained checks first, then optional public-data replays.
MODELS = (
    "service", "infrastructure", "handover", "advisers", "registry",
    "calibration", "review_panels", "task_selection", "curriculum",
    "participation", "exchange", "default_choice", "grounded_review",
    "frontier", "newton_scope", "swapped_prizes", "translation", "ends",
    "terminal_tests", "first_ends", "changing_premiums",
)
BANDIT = "allBehaviouralData2.csv"
ARCHIVES = {
    "transmission_data": (".",),
    "turnover_data": ("df_solves.Rda", "df_surv.Rda"),
    "reports_data": ("positive_results_in_registered_reports_data.tsv",),
    "bandit_data": (BANDIT,),
    "bandit_monitor": (BANDIT,),
    "unknown_change": (BANDIT,),
    "budget_data": (".",),
    "budget_protection": (".",),
    "shared_outcomes": (BANDIT,),
    "color_data": ("WCS-Data-20110316.zip",),
    "control_data": ("choice_exp2_clean.csv",),
}


def run(name, *inputs):
    print(f"\n--- {name} ---", flush=True)
    subprocess.run([sys.executable, str(NOTEBOOK/(name+".py")), *inputs], check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, help="directory with the files listed in reproduce.md")
    args = parser.parse_args()
    for name in MODELS:
        run(name)
    if args.data is not None:
        for name, files in ARCHIVES.items():
            run(name, *(args.data/filename for filename in files))
    print(f"\nPassed {len(MODELS)} self-contained checks and "
          f"{len(ARCHIVES) if args.data is not None else 0} archive replays.")


if __name__ == "__main__":
    main()
