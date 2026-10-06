# F16 implementation probe commands, bounds and failure record

Working directory for every command below:

`/workspace/scratch/8dbd45f3c7ee/value_logic`

Baseline: `6ef27f20e3ac0920953a27dd84d6c91a021ba58f`. Reviewer: separate ChatGPT (GPT-6 Astra Pro) implementation audit agent. Concurrent work contributes **zero principal D/L/E/O minutes**.

## Executed probe commands

```sh
mkdir -p v2/work_logs/F16_2026-10-05_S1/reviews/implementation

PYTHONDONTWRITEBYTECODE=1 python -X faulthandler v2/work_logs/F16_2026-10-05_S1/reviews/implementation/probes.py attempt1 > v2/work_logs/F16_2026-10-05_S1/reviews/implementation/attempt1.stdout.log 2> v2/work_logs/F16_2026-10-05_S1/reviews/implementation/attempt1.stderr.log

PYTHONDONTWRITEBYTECODE=1 python -X faulthandler v2/work_logs/F16_2026-10-05_S1/reviews/implementation/supplement.py > v2/work_logs/F16_2026-10-05_S1/reviews/implementation/supplement1.stdout.log 2> v2/work_logs/F16_2026-10-05_S1/reviews/implementation/supplement1.stderr.log
```

The first command creates the allowed output directory. The next two are the only executing audit probes. Both returned exit code `0` on their first attempt. No retry, patch to old code, or modification of an existing test was needed. Output filenames were checked in the scripts to prevent overwriting an earlier attempt. Bytecode writes were disabled.

The first source manifest runs `git show 6ef27f20e3ac0920953a27dd84d6c91a021ba58f:<path>` for each of its 26 listed files, compares the exact bytes to the working source, and hashes both with SHA-256. No content is fetched from a remote repository. The main probe hashes itself before execution; the supplement records its own SHA-256 in `supplement1.json`.

## Exact attempted bounds

The source of each attempted query and transformed proof is retained in `probes.py`; `attempt1.jsonl` stores every outcome, expected exception class/message and returned numeric detail. The complete small-domain choices are:

| Probe family | Declared choices and limits |
|---|---|
| Receiver | Two cases `x<=0` and `x<=1`; local/global budgets `0`, `1`, `-2^-255`; changed literal pair, equivalent `x+0` pair, unit, case, revision, observation, scope, and source row. |
| Transport | Single rows `x<=0`, `y<=0`, relaxed `x<=2`; complete coordinate swap; omitted key; free local; withdrawn source; two alternatives `x<=0`, `x<=1`; zero-scaled source row. |
| Signed native rules | Exactly 25 instructions, all 16 native tags; `x in [-1,-1/3]`, `y in [-1/2,1/2]`; conversion `3/2`; exactly three points `(-1/3,1/2)`, `(-1,-1/2)`, `(-5/7,2/9)`; 75 independent node evaluations. |
| Scientific direct loss | Exactly four points `(0,0)`, `(-7/13,5/17)`, `(-1,1)`, `(2^-255,-2^-254)`; T1/T2/R/F losses at each. |
| Receipt/reconstruction | Origin evidence `(plus,minus,beta,gamma)=(0,0,0,0)`; current `(None,None,0,3/32)`; T1; current budget `0`, exact root budgets `-3/8192`, `+3/8192`, and stricter differences `2^-240`/`2^-255`. |
| Identity relabeling | Genuine old proof relabeled to current evidence `(1,1,1,1)` and the current fingerprint in every instruction. |
| Scientific asymmetric exact source | `(plus,minus,beta,gamma)=(2^-255,7/19,5/23,3/29)`; action R, requested budget `2`; exact optimum `-17/464`. |
| Resource refusal | Scientific maximum basis checks `0` or proof steps `0`; default finite ceilings otherwise 440 bases and 128 steps. |
| Coefficient cache | Origin `(1/8,1/9,1/7,1/6)`, relaxed `(2,2,1,1)`; T1 budget `3` for successful current emission and `0` for the selected screen; changed action R, one removed joint row, empty catalogue with max bases `0`. |
| Program/reduct | Default allowed program caps `error<=1/20`, `second<=3/10`, `foreign_zero=True`; risk budget `-1/20`, and `alpha=1-2^-255` with budget `0`; mean `second_cap=9/40`, budgets `0` and `-2^-255`. Program max bases 35 and max steps 128. |
| Derived-rational supplement | `beta_cap=0`, `gamma_cap=2^-255`; T1 budget `0`; active bound `255/2^263-3/32`; reduced denominator 264 bits; internal exact-bound receiver and current external receipt checked. |
| Graded supplement | Alternative rows `x<=0`, `x<=1`; withdraw only row 0; point `x=1` accepted with exact penalty/bound 1; point `x=2` rejected because retained row 1 fails. |

No loop over the F11/F12 populations, minimizer candidates, broad suite, or F15/ND01 data-generation/estimation stage was invoked. The three-point native fixture and four explicitly listed loss points are the only direct point collections; reference calls use the existing small geometric algorithm for individual selected sources.

## Result counting

`attempt1_summary.json` contains 65 records, all passing. Remove the manifest and five `*_setup` records to obtain 59 substantive records. Of those, 40 are expected rejection records. The supplement adds three substantive records, one an expected rejection. Total: **62 substantive records, 41 expected rejections, no unexpected probe failures**. Bundle counts are not test-independence claims; for example, the cache refusal record contains six individually checked results.

## All failures and limitations retained

There was **no failed probe run, unexpected exception, crash, retry, or assertion repair**. Both probe stderr logs are empty. Expected adversarial rejections are retained in full in the result journal and are successful observations of the stated contract, not hidden failed runs.

One ordinary read-only inspection command returned exit code `2` because two wildcard patterns had no matching files:

```sh
sed -n '1,75p' v2/derivations/03_soundness.md && sed -n '334,370p' v2/derivations/03_soundness.md && sed -n '850,875p' v2/derivations/03a_soundness_scope_and_use.md && rg -n 'strict|3/8192|3/32|origin' verification/test_v2_f12* v2/verification/mutation_probe.py v2/work_logs/F12_2026-10-03_S1/*minimum* v2/work_logs/F12_2026-10-03_S1/*reuse*
```

The two messages were:

```text
rg: v2/work_logs/F12_2026-10-03_S1/*minimum*: No such file or directory (os error 2)
rg: v2/work_logs/F12_2026-10-03_S1/*reuse*: No such file or directory (os error 2)
```

The preceding document reads and matching test/module results succeeded. The missing patterns were not used as evidence of missing mathematical results. The strict-margin source and published expected values were instead read from `v2/verification/minimize_reuse.py`, `verification/test_v2_f12_revisions.py`, and the public F12 report; the existing minimizer and old tests were not executed.

Some batched read-only tool responses were display-truncated. The actual relevant functions were then read in smaller segments before review. Those display limits did not truncate either saved probe journal.

The first large-denominator fixture had a 9-bit active bound despite its 256-bit input denominator. It therefore did not establish the derived-rational boundary. The separate supplement explicitly resolved that limitation with an active 264-bit denominator; the original probe and its result were retained unchanged.

The known `-3/8192` versus `+3/8192` reconstruction miss is recorded as a limitation of the retained proof strategy. It was not converted into a new defect claim or called a false semantic request. No worldwide minimality, universal soundness proof, empirical validation, external peer review, performance result, or full-repository pass is claimed.
