# Reproducing W6's first cycle

Codex (GPT-6), November 12, 2026. Read [assessment.md](assessment.md) for
scientific scope and [sources.md](sources.md) for primary comparisons.
The executed environment was Python **3.13.14**, NumPy **2.2.5** and
SymPy **1.14.0** on Windows. Most algebraic checks use standard-library
fractions; numerical and sampled checks use NumPy. SymPy is needed only
for the independent witness checks in `verify_report.py`.

Run these commands from `v4/notebook/P4-R6-C001`. Each program writes its
adjacent JSON. Use a separate checkout/worktree for reproduction, or inspect
the resulting Git diff before replacing saved outputs. No network data is
needed. Seeds, parameters and information contracts are in each program and
output; small floating-point differences across versions are possible.

| Result or check | Command |
| --- | --- |
| R6.1 decision geometry and partitions | `python goal_geometry.py` |
| R6.2 observed representation selection | `python observed_goals.py` |
| R6.2 incomplete price coverage | `python coverage_check.py` |
| R6.3 reusable observation and provision | `python shared_observation.py` |
| R6.4 priority retention and revision | `python plastic_priorities.py` |
| R6.5 purchased-payoff learning | `python payoff_learning.py` |
| R6.6 bounded planning and shaping equivalence | `python bounded_subgoals.py` |
| R6.7 capability geometry | `python capability_geometry.py` |
| R6.8 policy/value reconstruction | `python policy_values.py` |
| R6.8 inverse-value supplement | `python value_queries.py` |
| R6.9 option pressure and goal weights | `python option_pressure.py` |
| R6.10 strategic preference commitment | `python strategic_values.py` |
| R6.11 changing goals and shared histories | `python changing_goals.py` |
| R6.12 survival-filtered values and action cloning | `python unrepresented_values.py` |
| R6.13 exact action-selection improvement | `python selection_learning.py` |
| R6.13 finite-trial supplement | `python selection_sampling.py` |
| R6.14 context-dependent goals | `python goal_context.py` |
| R6.15 continuation values and bonus fixation | `python value_use.py` |
| R6.16 forced-purchase learning | `python learned_concepts.py` |
| R6.16 relevance and outcome-law shifts | `python shift_concepts.py` |
| R6.16 selective purchases (requires `learned_concepts.json`) | `python selective_concepts.py` |
| R6.16 near-tie finite learning | `python boundary_concepts.py` |
| R6.16 one-time-cost reuse, known-law comparison | `python reuse_concepts.py` |
| Saved headline summaries and separate exact algebra implementation | `python verify_report.py` |

Run `learned_concepts.py` before `selective_concepts.py` if regenerating all
outputs. The latter compares paired results from the former. The boundary
panel executes 320 agents with two nested checkpoints up to 2,096,640
opportunities each; it is longer than a small exact check. The survival
sampling diagnostic draws binomial success counts from the exact environment
law instead of simulating every physical step. It does **not** execute the
much larger sufficient schedule proved in its supplement.

Each scientific program was executed successfully in this cycle. The final
summary check independently recomputed 360 statistics/paired differences and
24 exact SymPy equalities. These are checks of the finite evidence, not
independent expert confirmation. Reproducible assertion failures should be
investigated; an isolated apparent hardware failure may be retried, retaining
any scientifically consequential failed attempt.

From the repository root, inspect the closed research balance with:

```powershell
python v4/notebook/clock.py v4/notebook/P4-R6-C001/timing.jsonl --sum
```

The total is **14,412,827,801,100 ns = 240.213796685 minutes**. Do not restart
this completed clock for publication or a new cycle. Repository checks use:

```powershell
python tools/check_repo_paths.py
python tools/evidence_paths.py verify
python v3/checks/math_markdown.py
python -m verification
git diff --cached --check
```

Stage intended changes before checking index paths. The mathematical Markdown
checker validates portable delimiters and conventions, not mathematical truth
or live rendered layout. The cycle record states any platform-specific
repository regression separately from the scientific checks.
