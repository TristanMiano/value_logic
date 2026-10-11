# Supplemental P3-10 interpretation: retrospective bounds from paid labels

Reviewer: **ChatGPT (GPT-6 Astra Pro), /root/conformance_reconstruction**.
Status: **Mathematically sound at the stated relaxed uncertainty set**.
This is an independent source-only assessment of the principal's proposed
post-run interpretation. No final input or output was accessed for this note.
It does not change the frozen reporter, endpoint, policy or primary analysis.
Principal-clock credit: **0 seconds**.

## Exact construction

Use the immutable **emitted** forecast `q_t`, actual terminal action `a_t`,
and recorded selected/unselected mask. The frozen targets are

\[
 F=\sum_t(q_t-y_t)^2,\qquad
 V=\sum_{t\text{ unselected}}\{q_t+(1-2q_t)y_t\},\qquad
 Z=\sum_t\mathbf1\{a_t\ne y_t\}.
\]

The full key is `(semantics_version, source_version, variables, clauses)`.
An opaque query ID or a hash alone is not the equality criterion. Retain one
Boolean `y_k` for all occurrences of an exactly equal full key. Collect only
successful, checked, sound, currently applicable paid receipts into `K_known`.
Reject conflicting labels for one key. A later receipt can identify an earlier
unchanged query in the same source epoch; it does not make that answer available
at the earlier issuance time.

Because `y` is Boolean, every contribution is affine:

| Target | Constant term | Coefficient of its key's label |
|---|---:|---:|
| `F_t` | `q_t^2` | `1-2q_t` |
| `V_t`, only if unselected | `q_t` | `1-2q_t` |
| `Z_t` | `a_t` | `1-2a_t` |

For any one target `X`, sum these terms within key `k` to obtain `A_k+B_k y_k`.
Then the exact bounds over the relaxed cube of unresolved labels are

\[
 X_{\min}=\sum_{k\in K_{known}}(A_k+B_k\hat y_k)
          +\sum_{k\notin K_{known}}\left(A_k+\min(0,B_k)\right),
\]
\[
 X_{\max}=\sum_{k\in K_{known}}(A_k+B_k\hat y_k)
          +\sum_{k\notin K_{known}}\left(A_k+\max(0,B_k)\right).
\]

**Proof.** Each true unresolved label is in `{0,1}`. Distinct unresolved keys
are independent optimization coordinates in this *relaxation*, so each summand
attains its smaller/larger alternative independently. The actual label assignment
is one member of that cube. Hence the bounds contain the actual target and each
endpoint is attained in the cube. No stochastic independence assumption or
sampling argument appears in the proof. Exact rational arithmetic suffices.

## Relationship to the frozen report

The frozen reporter uses earlier current hard receipts and the current purchase
while scanning chronology. Its deterministic `F` envelope sums each then-unknown
position's separate two-label extrema; its `V` envelope treats still-unresolved
unselected positions separately; its `Z` envelope is `[0,n_live]`. The proposed
end-of-episode map uses a superset of those known labels and imposes same-key
equality across unresolved repeated positions. Consequently its marginal intervals
are contained in those chronology envelopes for the same valid complete record.
They may be strictly narrower even without an additional purchase.

For example, two unresolved occurrences of one key with forecasts `1/4` and `3/4`
have combined `F=5/8` for either label, while independent coordinatewise extrema
give `[1/8,9/8]`. If both are unselected, their combined `V=1`; opposite terminal
actions likewise give combined `Z=1`. These are hypothetical algebraic examples,
not P3-10 observations.

## Scope that the interpretation must retain

- The report is retrospective. The forecasts, actions, selections, scope versions
  and policy history remain the issued ones. Later evidence must not overwrite
  them or become a claim that the policy anticipated an answer earlier.
- Sharpness is for the **relaxed key-label cube**. Distinct keys can be logically
  related or semantically equivalent, and some assignments may also conflict with
  the recorded update history. Ignoring those extra constraints preserves validity
  but does not make the interval sharp over true CNF worlds or policy-consistent
  alternative histories.
- `F`, `V` and `Z` have separately sharp marginal intervals. Their endpoint choices
  can disagree on a key, so the Cartesian product of all three intervals need not
  be jointly attainable.
- Use matching current source/semantics and accepted receipt provenance. Failed,
  unchecked, stale or conflicting records are not labels; privately scored truths
  are not paid observations. Across withdrawal or source change, full-key equality
  and current applicability must be re-established.
- `V` keeps the frozen conditional-Bernoulli-error target. These deterministic
  bounds create no fairness, frequentist coverage, or unconditional-episode-mean
  claim for the finite DEVELOPMENT_MT seed paths.
- Apply the same observer to all eligible retained methods. This is unbilled audit
  computation with additional map construction, comparisons, arithmetic, storage
  and output. Narrower intervals alone establish neither an economic advantage
  nor a deployed reporting result. Any priced extension needs its own protocol.
- Incomplete records require their declared missing-data treatment; a complete
  episode's denominator cannot be silently replaced by an observed prefix.

The construction is suitable as a separately labelled supplemental P3-10 result
interpretation after the frozen public and evaluation stages have completed.
The conformance observer and frozen primary outcomes remain unchanged.

## Source binding

The accompanying `supplemental_reporting_note_v1.manifest.json` binds this note
and the exact frozen source records reviewed. Relevant locations are
`p308_cnf.py: Query.claim_key`, `p308_reporting.py: report_owned_episode`,
`p309_broker.py: _report_comparison`, and the two named reporting derivations.
