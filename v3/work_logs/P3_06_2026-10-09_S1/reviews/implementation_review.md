# P3-06 independent implementation review

Contributor: **ChatGPT (GPT-6 Astra Pro), independent implementation reviewer**.
October 9, 2026 UTC. Review target: the preserved defensive-forecasting
supplement and its exact-rational implementation. The principal owns the
integrated implementation and task decision.

**Disposition:** the preserved evidence reproduces, and the independently
reconstructed finite potential checks pass. Four API hardening points must be
addressed before treating the supplementary module as the integrated interface.
The supplementary result remains valid for its tested valid inputs. This review
does not supply historical time, principal Research90 credit, general Logical
Induction, or a final evaluation.

## 1. Preservation and replay

The original scripts were inspected before execution. Their hashes match the
source hashes recorded in the original `development_result.json`:

| Preserved artifact | SHA-256 |
| --- | --- |
| `defensive_forecasting.py` | `cbe6565492f3083c55bc966e1b31ae55f95aa026d87af378b1e2673f7e944be2` |
| `check_defensive_forecasting.py` | `5299bd921e452403df13e95447cbeb9f5c8144146ccbf5c33f4a324df20fc9e5` |
| Original `development_result.json` | `dead832e91d7327fd826fc9f8b1c11f4cd6a1ae52ae01aefaa1162919f4a9db3` |

The two scripts were copied byte-for-byte to
[`preserved_rerun_v1`](../development/preserved_rerun_v1/). The fresh run passed
all **1,510** original assertions. Its complete deterministic result payload is
identical to the saved payload after excluding only start/end UTC, execution
duration and interpreter version. The
[`rerun_receipt.json`](../development/preserved_rerun_v1/rerun_receipt.json)
records that comparison and verifies the original directory remained unchanged.

This is a fresh development replay, not recovered evidence of engaged time in
the interrupted session. No original file, old result or old clock was edited.

## 2. Independent finite reconstruction

The distinct review script
[`audit_preserved.py`](../development/independent_audit_v1/audit_preserved.py)
does not call the implementation's `_features`, `_score`, or `squared_norm` to
reconstruct the potential increment. It rebuilds the residual from admitted
history, recomputes the declared features, and evaluates both binary outcomes
before settling the actual outcome.

Its [`audit_result.json`](../development/independent_audit_v1/audit_result.json)
records **2,413** checks, with **44 failed API checks** and **zero mathematical,
delay or arithmetic-resolution failures**. The API failures are repeated
witnesses of the four issues in section 3, not 44 independent scientific bugs.

The mathematical cases cover all 64 binary strings of length six, with
nontrivial feature scales $`\alpha=2/3`$, $`\beta=5/4`$, weights
$`(0,1,1/17,19,1/2,3)`$, non-dyadic expert forecasts and mixed root budgets.
Across **384 issuances**, the script checked **768 hypothetical binary
increments**, including 112 exhausted searches and 128 positive allowances.
The declared allowance equals the maximum actual corrected-potential increment
over the two outcomes in every case.

The reconstruction is direct: with pre-issue residual $`R`$, issued feature
vector $`\Phi`$, and hypothetical $`e=y-p`$, compute

```math
\Delta_y=\|R+e\Phi\|^2-\|R\|^2-p(1-p)\|\Phi\|^2.
```

Because $`e^2-p(1-p)=(1-2p)e`$ for binary outcomes,
$`\Delta_y=2eS(p)`$. The recorded allowance is exactly the larger of the two
increments. This check includes unfavorable outcomes; it is not an assertion
only about the outcome selected for each trace.

The source also returns `tolerance_met=True` at valid endpoint solutions even
when the absolute score exceeds the requested root residual tolerance. There
were 96 such endpoint cases. This behavior is mathematically correct because
the endpoint allowance is zero. The field must be documented as “endpoint
condition or residual tolerance met”; it is not literally a claim that every
returned score has small absolute magnitude.

The identity tests found that issued expert-value tuples are detached from the
caller mapping; old predictions remain unchanged; stale feedback, duplicate
feedback, reused query IDs and issuing over an outstanding prediction are
rejected without losing the pending prediction. The delay metamorphism keeps
two environments identical until a previously hidden label is admitted, then
permits their newly issued predictions to differ. Audit dictionaries are
detached snapshots, not live reports.

## 3. Reproduced API defects and requested repairs

### I-1. Allocation before issue validation

`DelayedPool.issue` appends a newly constructed copy before delegating query,
expert, weight, tolerance and work-budget validation. A rejected issue can
therefore change the pool's copy count and its reported resource/certificate
state. Eighteen invalid issue forms were reproduced both in a fresh pool and
while its existing copy was busy, producing 36 state-atomicity failures.

For example, issuing a negative weight to a fresh pool raises `ValueError`, but
`len(pool.copies)` changes from zero to one. This does not make the mathematical
bound unsound: adding an unused copy only weakens the displayed Cauchy--Schwarz
bound. It does make rejection nontransactional and charges a copy that never
issued a valid prediction.

**Repair:** validate and normalize the complete issue before appending a new
copy, or construct an unregistered candidate and register it only after issue
succeeds. Failure must preserve the pool's entire observable state.

### I-2. Mutable expert-name alias

Although annotated as a tuple, `Forecaster` accepts a list of names and stores
the same object. Appending a name externally after issuance causes `reveal` to
raise `IndexError` after loss/residual updates and after clearing the pending
prediction. The saved witness records one settled history entry and
`pending=None` despite the exception.

This requires a caller to use an accepted mutable sequence; it does not occur
with the intended immutable tuple input. It still warrants repair because the
constructor accepted the sequence and a later caller edit changes the expert
index contract.

**Repair:** validate expert names and retain a detached tuple. Do not let
caller-owned sequences define the future length or interpretation of state.

### I-3. Delayed constructor validation is deferred

`DelayedPool` accepts empty experts, zero bins, zero feature scales and an empty
scope, then fails on its first issue. Four probes reproduce that delayed error.

**Repair:** validate configuration at construction, before representing a valid
pool. Validation should not itself create or charge a live forecasting copy.

### I-4. Scope type is unchecked

Both classes accept a nonempty integer as `scope`, despite the string/type
contract used for versioned reports. Two probes reproduce this issue.

**Repair:** require a nonempty string and detach all configuration inputs.

Malformed rational strings such as `"1/0"` raise `ZeroDivisionError` rather than
the usual `ValueError`. In a standalone forecaster they preserve state. A
uniform input-error type would simplify consumers, but this is not a separate
mathematical defect.

## 4. Exact witnesses for conditions that cannot be omitted

[`boundary_witnesses.py`](../development/independent_audit_v1/boundary_witnesses.py)
and its
[`result`](../development/independent_audit_v1/boundary_witnesses_result.json)
preserve two deterministic limitation witnesses at 64 rounds. Both pass.

**Root work alone does not give calibration.** With one constant-half expert,
two tent intervals, unit weights, zero bisections and every label zero, both
endpoint signs stay bracketed while every issued forecast remains $`p=1/2`$.
Before round $`t`$, the middle calibration residual is $`-(t-1)/2`$, so

```math
S_t(1/2)=-(t-1)/2,\quad A_t=(t-1)/2,\quad
\sum_{t\le T} A_t=T(T-1)/4.
```

The variance term is $`T/4`$ and the squared norm bound is exactly $`T^2/4`$.
The normalized middle-bin residual remains $`1/2`$. Expert regret is zero
because the supplied expert also predicts half. At $`T=64`$, the allowance is
1,008. The potential certificate remains true and explicitly reveals why a
vanishing calibration conclusion is unavailable.

**Eventual feedback without a copy-count condition does not ensure a useful
uniform rate.** Issue $`T`$ queries with constant-zero and constant-one experts
before revealing any labels. The wrapper uses $`K=T`$ fresh copies, each issuing
half. Reveal all labels as zero afterward. Learner loss is $`T/4`$ and the zero
expert loss is zero, while the aggregated squared norm bound is
$`3T^2/8`$. At 64 rounds these are loss 16 and bound 1,536. This finite family
rules out a uniform sublinear worst-case guarantee over unrestricted delay
schedules.

Before any labels arrive, the audit correctly returns settled count zero,
pending count 64 and a zero bound for the empty settled set. That zero says
nothing about the pending population. An integrated report should keep these
coverage distinctions explicit.

## 5. Arithmetic growth is measurable and input dependent

The main audit compares three declared rational-input profiles over 128 rounds
with `max_bisections=12`. The latest issued probability denominator always fits
in 14 bits. Exact accumulated certificate values can nevertheless be much
larger:

| Input profile | Largest certificate numerator, bits | Largest certificate denominator, bits | Sum of stored history fraction component bits |
| --- | ---: | ---: | ---: |
| Dyadic inputs at fixed resolution | 61 | 55 | 41,955 |
| Fixed non-dyadic denominators | 80 | 80 | 53,337 |
| Fresh prime denominators each round | 10,789 | 10,784 | 1,380,421 |

For the fresh-prime profile, certificate denominator size grows from 1,071 bits
at 16 rounds to 2,271 at 32, 4,926 at 64, and 10,784 at 128. All measurements
are saved with score evaluations, bisections, tolerance failures and observed
execution durations. They count exposed rational values and retained report
fields, not every transient multiplication result or Python heap byte. They
are finite development measurements, not a universal asymptotic benchmark.

There is also a useful restricted denominator guarantee. Suppose expert
probabilities, weights and scales are dyadic at fixed resolutions, and the
search cap is $`K`$. Every issued probability denominator divides $`2^P`$ for
$`P=K+1`$. The tent function can be rewritten as

```math
b_j(p)=\max(0,1-|mp-j|),
```

so it is dyadic whenever $`p`$ is, even when $`m`$ is not a power of two. If
every feature denominator divides $`2^M`$, residual denominators divide
$`2^{P+M}`$, and variance/allowance denominators divide $`2^{2(P+M)}`$.
Summing rounds does not introduce new prime factors or increase those fixed
exponents. With bounded input magnitudes, numerators still grow with the
accumulated sums, and retaining every report still consumes increasing memory.

This restricted profile provides an honest way to keep exact denominators
manageable. Rounding arbitrary supplied experts into that profile would alter
the comparator unless the rounding error is charged explicitly. Increasing
the search cap changes the resolution bound; fixed iteration counts alone do
not imply a fixed-bit CPU or memory guarantee.

## 6. Evidence scope and integration handoff

The tests establish only their enumerated finite claims. The algebra above
supports the exact potential identity, with the binary-label and predictable
feature assumptions stated explicitly. Direct external mutation of internal
state is outside the mathematical protocol; accepted caller configuration
aliases should nevertheless be detached as described.

The principal should preserve the original module and outputs, implement the
repairs in a new version, and rerun these targeted cases against that version.
The integrated task adapter must bind the immutable report to the mathematical
query, its issue-time prices, and the actual admitted answer. The scalar module
does not itself retain arbitrary action-loss coefficients, acquire proofs,
price its expert library, or give a theorem under arbitrary retrospective
repricing.

All review outputs are development evidence. Observed script runtimes are
recorded with zero research-time credit; total reviewer effort is unmeasured
and is not added to the principal clock. P3-06 completion, contribution support
and any subsequent work-item selection remain the principal's separate
integration decisions.
