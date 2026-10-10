# Independent review of the paid live-performance reporter

Contributor: **ChatGPT (GPT-6 Astra Pro)**, integration-review sub-agent,
October 10, 2026 UTC. Task **P3-08**, **DEVELOPMENT**.

**Disposition: PASS for the captured trusted-owned-record interface and
declared bounded word tariff.** I independently reconstructed the formulas
and their finite bounds, then compared the implementation with separate
Fraction calculations on real owned CNF episodes. All six focused case
groups passed. No remaining formula, scope, funding or finite-width blocker
was found in this source revision.

This is **same-model, nonblind independent review** of the principal's
reporter and lemma. The broker's earlier API fixes were authored by this
reviewer under explicit delegation and are separately labeled self-check
in `broker_review_and_repair_disposition.md`. Agent costs and time are
unmeasured; principal-clock credit is zero. This is not P3-09, a final
evaluation, or empirical validation of confidence coverage.

## 1. Sources, prior static issue and execution evidence

The copied source closure and prospective plan are in
`live_performance_review/`. Key SHA-256 bindings are:

| Artifact | SHA-256 |
|---|---|
| `v3/experiments/p308_reporting.py`, version `p308-live-performance-v1.1` | `33ecde23b45ca9696da44ffb925797b52dc450d141e16b79fa17ec937fdb347d` |
| `v3/derivations/08_live_hard_performance.md` | `82108d6b9b70b8c3cadcb667dbcf16b1528396029177d39e6699c32fefb02db5` |
| `v3/experiments/p308_broker.py` | `399080c950a48c1cd935efbee8ed7769a7af54b7afa14859b5671397638e2e4d` |
| `v3/experiments/p308_cnf.py` | `46fd3e82505b9b6af9805836a562f2f78a3436384e0b3476c4f85cec355817a2` |
| `v3/experiments/p308_common.py` | `4928a5b9c80e05b497bd93116957139252c65f393e6e12ea4c7ad4727f300a29` |
| `live_performance_review/check_reporting.py` | `15f905776a407095a254a4ab19f7f65fd573dee243a47875b5a83c7702014ca2` |
| `live_performance_review/results.json` | `e77c1a3b7248ba9f3d6391cdf35254ec47fa05803a342520bb0f1d234a966548` |

In an earlier static read, `_key_words` admitted source/semantics labels
only through length 64, while the CNF source and broker admitted length 128.
I reported that integration mismatch. The principal fixed it before this
snapshot. The captured v1.1 uses 128 and passes the real 128-character source
case. The principal also made the fair-bit premise and development-seed
limitation explicit in report metadata. I did not execute or assign a new
source hash to the earlier unpreserved reporter wording.

The test script was saved, syntax-validated without execution, and hashed
in `script_before_execution.json` before running:

```text
python v3/work_logs/P3_08_2026-10-10_S1/reviews/live_performance_review/check_reporting.py
```

Observed execution ran from 2026-10-10 16:38:28.776232 UTC to
16:38:28.805300 UTC, with **6 pass, 0 fail**. Every owned episode and report
was saved before its separate private truth/Fraction audit. Those saved
records and hashes remain alongside the results. The private evaluator
does not supply information to the paid reporter and its work is not
silently counted as deployment capability.

## 2. Public read and chronology boundary

The service explicitly consumes a completed record from the trusted local
broker. It checks the broker version, success status, quota completion,
contract shape, trace/block/invoice lengths, actual selected ticket and its
implied position, favorite multiplicity and each row's propensity. Every
base/live forecast is an admitted contract dyadic. Action and terminal
values are exact binary integers. Query keys and scope labels agree with
the epoch, and completed rows cannot claim stale or conflicted issuance.

The reporter reconstructs its list of purchased checked keys in chronological
row order. A hard override must cite a matching answer already in that list
before the row is processed. It cannot borrow its own selected receipt or
a later receipt to justify an earlier emitted forecast. A selected invoice
must bind the row's query ID and complete semantic key, the current provider
and version, successful status, exact checked flag and a binary integer
answer. Contradictory selected and prior answers reject. Selected terminal
actions must equal the receipt label in both the base and live paths.

The reporter then reads only labels actually purchased by that episode.
Its reconstruction does not call the truth service. A prior purchased label
may exist even when the broker's hard override is disabled; the reporter
conservatively respects the actual `hard_before` flag rather than inventing
an override that was not emitted.

This validation does not authenticate an adversarially manufactured record
or prove that an arbitrary transcript was produced by fair randomness. In
particular, the stored base action is trusted as the owned broker's draw;
the reporter does not recreate private random bits from an external claim.
That is consistent with the stated local ownership boundary and the explicit
fair-bit mathematical premise. It would be insufficient for a public
untrusted-receipt API without a new authentication/ownership mechanism.

## 3. Independent exact-arithmetic reconstruction

Put d=2^h, p=B for uniform selection or p=2B for tickets, and M=1 for
uniform selection or M=B+1 for tickets. The actual multiplicity mu is 1 or
M and pi=mu/p. Let a row's base numerator be x, so q=x/d.

The selected centered-loss numerator is

```math
r_{\mathrm{num}}=(x-d/2)(1-2y)=d(d_t-1/2).
```

The sign is correct for both binary labels. The reporter retains U_c with
denominator dM and A_c with denominator d^2 M. Its updates are exactly

```math
U_{\mathrm{num}}\mathrel{+}=(p-\mu)r_{\mathrm{num}}(M/\mu),
\qquad
A_{\mathrm{num}}\mathrel{+}=p r_{\mathrm{num}}d(M/\mu).
```

The initial terms are (T-m)dM/2 and Td^2M/2 respectively. Subtracting
x(d-x)M from the latter for every row gives the public variance subtraction
in A_c. All these divisions are exact: d is even and mu divides M. No
floating-point approximation is hidden in the estimator.

Delta_F accumulates `(x-d*y)^2` with denominator d^2 over prior hard rows.
Delta_V accumulates `x+(d-2*x)*y` with denominator d over prior hard,
unselected rows. Delta_Z counts the corresponding retained base errors.
The selected position is excluded from Delta_V and Delta_Z and included
in Delta_F only if its warrant was prior to its own issuance, as required.

For the base width, the row's scaled quantity is

```math
w_t=|d-2x_t|p(M/\mu_t),\qquad
C_k=\max_{t\in k} w_t/(dM).
```

The squared-width numerator sums the squared block maxima, with common
denominator d^2 M^2. The code correctly uses the complete base forecasts
and their actual propensities here, including hard-corrected live rows.
It does not substitute selection-dependent live widths.

The final common denominator is

```math
D=8R d^2M^2.
```

The stored radius numerator `8*Q_num + 5*R*R*Q_den` is therefore exactly
Q/R+5R/8. Rescaling U and A to D and subtracting the correctly rescaled
Delta_V and Delta_F gives the translated centers. The action radius is
the exact integer `ceil_sqrt((5*n_live+1)//2)`. This is the required
ceil(sqrt(ceil(5n_live/2))) for nonnegative integer n_live.

The terminal interval uses that live action radius plus the single base
sampling radius. Delta_Z is exported as an exact audit quantity and is not
used to select a favorable second terminal confidence construction. The
minima/maxima for deterministic V and F envelopes agree with the binary
possibilities. All interval intersections retain an explicit conflict flag.

When n_live=0, the implementation exports V=Z=0 exactly and uses the known
issued Brier sum as an exact F interval. The two-query test obtains
F=25/64, V=Z=0. This verifies that the current purchased forecast loss is not
retroactively set to zero. The generic centers remain available separately
for audit; exact intervals need not be centered on them.

## 4. Finite integer width has a large explicit margin

The reporter admits MAX_BITS=256 and prepays its abstract integer operations
using their bounded word widths. A conservative algebraic bound does not
need the observed sample to justify that limit. The inherited finite contract
has T<=2^13, m<=2^12, h<=32 and B<=2^10. Consequently d<=2^32, p<=2^11 and
M<2^11. Simultaneously using all those maxima is conservative even when they
cannot occur in the same contract.

| Intermediate quantity | Conservative magnitude bound |
|---|---:|
| One scaled width w_t | <=2^54 |
| Squared-width numerator Q_num | <=2^120 |
| Squared-width denominator d^2 M^2 | <=2^86 |
| R=p ceil(sqrt(2m)) | <2^18 |
| Final denominator D | <2^107 |
| Absolute raw U numerator | <2^66 |
| Absolute raw A numerator | <2^98 |
| Absolute rescaled base center | <2^130 |
| Either rescaled exact correction | <2^120 |
| Absolute live center | <2^131 |
| Rescaled sampling-radius numerator | <2^126 |
| Absolute final interval/envelope intermediate | <2^132 |

For example, scaling U multiplies by `8*R*d*M`, less than 2^64, while
scaling A multiplies by `8*R*M`, less than 2^32. These divisibilities are why
the implementation does not recursively multiply growing Fraction
denominators. The conservative pre-operation add/multiply bit allowances
remain below 140 bits throughout, well below the 256-bit cap. Integer-square-
root inputs and its bounded envelope are smaller still. The tests observe
peak reporting widths 19/25 bits at precision 4 and 75/81 bits at precision
32 for uniform/ticket examples; those observations are checks, not the proof
of the global bound.

## 5. Reporting cap and costs

The reporter declares `REPORT_FUNDING_CAP=2^48`. It is intentionally very
conservative. The successful owned input has at most 8192 rows and at most
4096 distinct purchased keys. Each validated key is bounded by 1024 words
in the reporter's own admission, a weaker bound than the current CNF key's
maximum. Therefore a full reverse scan costs at most 2^25 key comparisons.
Each comparison is charged at most `2*(1024+1024)+4=4100` units, so all scans
cost less than 2^38.

All remaining loops are linear in the bounded rows, blocks, clauses and
literals. A 256-bit arithmetic operand occupies at most four words. The
largest single declared binary integer operation costs at most 52 units;
even allowing 256 such operations per row yields less than 2^27. Public
row/key reads and binding checks, storage, selector headers, the bounded
square-root envelopes and terminal rational/metadata output remain far
below 2^38 in total. Thus a generous total below 2^39 is still more than a
factor of 512 below the advertised cap. The finite-width reconstruction
above also prevents a valid owned episode from failing through an integer
width rejection before the cap is reached.

The amended row reading charges actual bounded key size after its shape
validation, rather than debiting 1024 words for every short key. The scanner,
arithmetic, retained answers and output are paid deployment operations. The
source registry and broker have separate bills and completion premises;
they must be included in a combined all-in report. JSON evidence hashing,
the private audit and CPU/heap use are not silently identified with the
declared abstract word tariff.

The focused algebra cases illustrate the size of the actual extra service:

| Selector | Precision | Broker units | Reporter units | Reporting peak bits |
|---|---:|---:|---:|---:|
| Uniform | 4 | 6850 | 7785 | 19 |
| Uniform | 32 | 7054 | 11727 | 75 |
| Tickets | 4 | 7524 | 8168 | 25 |
| Tickets | 32 | 7836 | 12151 | 81 |

These are eight-query development tapes, not averages or claims of economic
advantage. Reporting is a material additional charge on these small cases.

## 6. Funding and failure tests

The confidence flag checks the broker's all-path funding premise and a
reporting limit at least the reporting cap. A successful calculation with a
smaller limit does not acquire that premise merely by completing. The fair
independent-bit assumption remains explicit in metadata even when the
interface/funding flag is true; a deterministic development seed does not
establish coverage.

The restricted-report test completes at its exact observed bill of 5163
units, well below 2^48. Its exact results remain available, but both
`all_path_reporting_funded` and `confidence_eligible` are false. Reporting
with limit zero instead returns a failed audit record with zero spent units,
a denied tariff bundle and confidence eligibility false. These are funding
dispositions, not silent missing observations.

The restricted-broker test completes the chosen four-query realization at
limit 9526 below its advertised all-path cap 99604, with actual broker bill
4566. A fully funded reporter still withholds confidence eligibility. Its
funding cannot retroactively supply the broker's missing all-path premise.
The unrestricted statistical statement is not being conditioned on a
budget-selected subset of successful episodes.

The chronology test perturbs an otherwise real owned record to mark its
first forecast hard-known before any earlier receipt. The reporter rejects
it after 718 paid units with `A hard override lacks an earlier current owned
receipt.` The failed perturbed record is preserved. This tests the declared
validation boundary and makes no external-authentication claim.

## 7. Mathematical acceptance and limits

The companion `live_hard_lemma_acceptance.md` independently reconstructs the
exact correction identities, the unchanged base sampling residual, the
conditioning argument for random n_live, the fixed-end error allocation,
the exact all-known exception and the corrected all-path funding premise.
The current implementation agrees with those formulas on the inspected
source and focused exact calculations.

No further blocker was found. The forthcoming main development run still
needs a frozen complete source closure and billing that adds procurement,
broker execution and reporting. Scope withdrawal must end current report
authority, and any failed or selectively completed episode must retain its
proper status. The result supplies one declared episode's finite paid
performance report. It does not establish joint coverage over development
arms, future-policy value, calibration, coherence, worldwide novelty or a
final contribution/evaluation gate.
