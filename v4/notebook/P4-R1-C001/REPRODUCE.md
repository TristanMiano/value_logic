# Reproducing the W1 continuation

Codex (GPT-6), November 11, 2026. These checks accompany
[the cycle assessment](assessment.md); they are not independent confirmation.
Fable's earlier scripts and saved outputs retain their original authorship.

S6 used Python 3.13, NumPy 2.2.5 and SciPy 1.15.3 on Windows. The rational
checkers use the standard library; ODE and sampled checks use NumPy/SciPy.
Run the following from this notebook directory. Commands with `--output`
write the named small result record; the last four write their adjacent JSON
automatically. Inspect differences before replacing a historical saved output.
Floating-point trajectories can differ slightly across library versions.

| Claim/check | Command |
| --- | --- |
| Central proof review and R1.8 bounds | `python audit_s6.py --output audit_s6.json` |
| R1.9 potential, allocation and population convergence | `python coupled_reappearance.py --output coupled_reappearance.json` |
| Sufficient versus incompatible concept catalogues | `python catalogue_geometry.py --output catalogue_geometry.json` |
| R1.10 sharp history threshold and support cases | `python unflagged_assignment.py --output unflagged_assignment.json` |
| Exact comparison with the established HSIC statistic | `python transfer_witness.py --output transfer_witness.json` |
| Witness-to-value bound and sharp-order family | `python selected_bounds.py --output selected_bounds.json` |
| Observed transfer partition | `python learn_transfer.py --output learn_transfer.json` |
| Discovery, validation, prediction and mixture comparator | `python observed_judgment.py --output observed_judgment.json` |
| R1.11 evidence correction, probe costs and decisions | `python finite_reappearance.py --output finite_reappearance.json` |
| R1.12 decreasing exposure and imperfect control | `python weak_exposure.py --output weak_exposure.json` |
| R1.13 actual stochastic learner and always-fine comparison | `python stochastic_judgment.py --output stochastic_judgment.json` |
| Analytic sufficient observation budgets, not simulations | `python stochastic_bounds.py --output stochastic_bounds.json` |
| R1.14 coalition fixed points, parity and approximation | `python coalition_recovery.py` |
| R1.14 finite observed recovery | `python coalition_observed.py` |
| Probe, adoption and calibration composition | `python probe_adoption.py` |
| R1.15 directed concepts, decision accuracy and goal menus | `python directed_reappearance.py` |

The stochastic learner executes one million steps for each of twelve paths
in five settings; it is longer than the small exact checks. The decreasing-
exposure probe calculation uses event-driven thinning and does **not** execute
its trillion-trial hypothetical horizon. Seeds, parameters, comparison scopes
and counts are recorded in the programs and outputs. A failed assertion is
evidence to investigate; rerunning a suspected stochastic hardware failure
does not justify discarding a reproducible scientific failure.

From the repository root, recompute the completed research floor with:

```powershell
python v4/notebook/clock.py v4/notebook/P4-R1-C001/timing.jsonl --sum
```

The research total is **14,426,654,567,148 ns**. Do not restart or extend
this closed clock for administrative work or a newly authorized cycle.

For repository hygiene, stage intended changes before the path check:

```powershell
python tools/check_repo_paths.py
python tools/evidence_paths.py verify
python v3/checks/math_markdown.py --path v4/notebook/P4-R1-C001/assessment.md
git diff --cached --check
```

Run the Markdown guard on each changed Markdown file. It checks delimiter
and macro conventions, not mathematical truth or rendered-page layout. Source
read scopes and scientific corrections are in [review_s6.md](review_s6.md).
