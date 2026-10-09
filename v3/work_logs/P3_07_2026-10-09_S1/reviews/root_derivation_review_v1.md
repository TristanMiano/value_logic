# P3-07 — review of root derivation version 1

Reviewer: **ChatGPT (GPT-6 Astra Pro), same-model internal subagent**.  
Date: October 9, 2026 UTC. Agent research time is **unmeasured**, with **zero
principal-clock credit**. No main derivation, clocks, ledger, plan, gate or
publication was edited.

## Reviewed version and independence

Reviewed source: `v3/derivations/07_paid_reasoning.md`, 13,135 bytes.  
SHA256: `65f28c0852ab61b8201090442d95b460e49d1f135a3632c73b6e088bc3f81b47`.

The exact bytes are retained as
[root_derivation_v1_snapshot.md](proof_agent/root_derivation_v1_snapshot.md),
with a [snapshot manifest](proof_agent/root_derivation_v1_snapshot_manifest.json).
The prior independent reconstruction remains unchanged, with SHA256
`0b2ef3b28434b30be8c5719cb484f179edc4da63107c55dd5ac4a2048f7b665e`.
That reconstruction preceded reading the root derivation, with the
same-model/nonblind-prompt limits recorded in its header. This second review
is explicitly nonblind review of the root's displayed argument and proposed
next refinement, not another independent reconstruction.

**Overall finding:** the displayed linear lower certificate, fixed-sample
concentration formula, integer-checkable conservative radius, repricing
restriction, and staged audit argument are sound at their stated conditional
scope. I found no algebraic error in those constructions. The important work
remaining in this snapshot is to make the continuation rule, screening rule,
sampling quantifiers and comparison baseline operationally exact. The root
has already announced a refinement of the sunk-cost rule and a finite-prefix
confidence construction; those announcements are assessed below as proposals,
not silently attributed to this preserved snapshot.

## 1. Continuation selection and all-in profitability are separate criteria

The inequality in §2,

```math
L_{\pi,b}(\lambda)>h(\lambda),
```

is a valid sufficient all-in comparison when `h` bounds incremental overhead
relative to the specified earlier stopping root. The snapshot also correctly
says that a stopped branch can still have assessment costs. Thus the displayed
inequality is not false.

The operational sentence prescribing stop whenever that inequality fails
nevertheless needs the distinction the root has now proposed. If the work
represented by `h` has already been paid, rejecting a positive continuation
gain merely because it cannot repay `h` can make the remaining decision worse.
For example, a certified continuation gain of `3/100` after assessment cost
`1/20` gives total gain `-1/50`; stopping after the same assessment gives
`-1/20`. Neither beats immediate stop, but continuing improves the available
choice by `3/100`.

An exact formulation is to identify the **current decision root** and write

```math
V_\pi=L_{\pi,b}-h^{\rm remaining}_{\pi,b}.
```

Here the remaining overhead is incremental relative to the current baseline
and has not already been represented in the paired features. Choose a
maximizer of `V_pi`, including `V_b=0`, with stop on a zero tie. Common overhead
that is already sunk is absent from this continuation maximization. Work
still required only for a candidate, such as a candidate-specific final
verification or dispatch, belongs in its remaining overhead. Costs common
to all actions at the current root cancel in the incremental comparison.

Independently report whether the selected branch's certificate repays all
earlier costs. For `H` actual same-law uses and paid setup `S`, this flag may
use `H V_selected > S`, with any other applicable assessed cost included
exactly once. An all-in flag being false does not imply that current
continuation should stop. Conversely, a true flag is only the claimed
conditional expected comparison on the common coverage event; it is not a
promise that each realized execution will be profitable.

**Disposition:** the proposed separate continuation and all-in flags are
mathematically appropriate. They improve the decision specification without
requiring a new probability theorem.

## 2. A cheap paid upper-bound screen is sound under a precise route scope

Let the screen have finished and let `R` be the complete family of routes it
is considering. For each route, separate possible gross task benefit from
the future incremental costs needed to realize that route. A sufficient hard
screening premise is

```math
V_r(\omega)\le U\quad\hbox{and}\quad C_r(\omega)\ge c_{\rm rem}
\qquad\hbox{for every }r\in R\hbox{ and every admitted }\omega.
```

Then

```math
V_r(\omega)-C_r(\omega)\le U-c_{\rm rem}.
```

If `U<=c_rem`, no considered route has positive gain from the current root;
stopping that route search is sound. A structural upper bound such as a
known fallback loss minus a known lower bound on all terminal task losses
can be available without profiling a future computation law. All arithmetic,
input admission and screening work must still be charged.

The following qualifiers prevent a new hidden oracle or a sunk-cost error:

- `U` covers every action and contingent continuation that the rejected route
  could realize. A maximum of uncovered fixed-action point estimates is not
  a hard upper bound on an observation-adaptive complete route.
- `c_rem` includes only still-unpaid mandatory costs. Already-paid profile
  setup or the screen itself must not cause a post-sunk screen to reject an
  otherwise useful continuation.
- If all candidates in this route must undergo an expensive assessment, that
  assessment can supply a common future cost lower bound. A failed screen for
  this route does not rule out a cheaper unassessed policy, already-certified
  computation, or legitimate ordinary shortcut outside it.
- A lower bound on resource expense needs the declared nonnegative resource
  prices or another valid signed-objective argument. Mathematical permission
  to use signed feature coefficients does not by itself make an execution
  cost a positive lower bound.
- A data-derived upper bound needs its own simultaneous/selection-valid
  coverage and a place in the total failure-probability budget. Calling it
  hard does not establish that premise.

The screen's own cost survives on a rejected branch. The construction avoids
larger unnecessary expenses; it does not make the screen-then-stop procedure
free or universally better than immediate stop. A per-request screen and a
screen for a reusable `H`-episode preparation service are different cost
comparisons and must use their respective benefit and resource horizons.

**Disposition:** the announced hard-upper-value screen is sound with these
conditions. It is a sufficient pruning test, not a general theorem that
passing it makes further assessment worthwhile.

## 3. The integer radius is valid; its full domain must be stated

For positive integers `K,n`, a predeclared `0<delta<1`, an integer `k`
satisfying `2K 2^{-k}<=delta`, and rational `r>=0` satisfying `2nr^2>=k`,

```math
2K\exp(-2nr^2)\le 2K\exp(-k)\le 2K2^{-k}\le\delta.
```

The analytic step `exp(-k)<=2^{-k}` is justified by `e>=2`; the two input
inequalities can be checked exactly with integers/rationals. Under the
stated domain the first condition necessarily makes `k` positive. A
coordinate of known zero width has zero radius and can simply be excluded
from the count if the count convention is fixed prospectively.

The snapshot correctly notes that a paired difference in `[-R,R]` has width
`2R`. It also correctly applies the concentration bound to paired differences
rather than separately treating the two mean estimates as if the pair had
the range of one constituent.

For common IID profile prefixes up to a **prospectively fixed** cap `Nmax`,
the same integer construction works with

```math
2K N_{\max}2^{-k}\le\delta,\qquad
2nr_n^2\ge k\quad(1\le n\le N_{\max}).
```

A union bound over the cells and prefixes then supports a data-selected
stopping time within the cap. Choosing the cap after inspecting the data,
or substituting the final random sample size into the uncorrected fixed-time
bound, is not covered. Zero samples need a supplied structural range rather
than an empirical certificate.

The sample independence premise applies to the full acquired episode vectors,
including any stochastic execution and state-reset behavior, not merely to
the bare mathematical query identifiers. Adaptive allocation of different
sample counts to different policies would require an additional condition:
each acquired observation must retain the target policy's fixed conditional
mean, with its valid prefix bound. Context-selected or success-only data do
not obtain that property merely because the original request generator was
IID. The displayed full-row rollout protocol avoids this additional issue.

Exact radius checking does not remove the representation contract for the
sample means, price vector, resource counters, paired-feature identities and
overhead bound. They must also be exact in the implemented fragment or have
checked conservative enclosures. The snapshot mentions validation and exact
measurement assumptions; the implementation should preserve that scope rather
than label arbitrary finite floating-point payloads certified.

**Disposition:** no error in the integer inequality. Add the parameter domain
and the planned finite-prefix quantifiers before using adaptive stopping.

## 4. The baseline and credal comparison need explicit quantifiers

### 4.1 Choosing among stopping policies

The snapshot fixes a stopping catalogue and covers every retained comparison,
so selecting a baseline from a fully covered family does not in itself cause
a multiple-comparisons error. The selected-baseline rule is nevertheless not
specified. A candidate can beat a poor stopping action while losing to a
better available immediate action.

The text should state one of the intended services: comparison with a fixed
declared baseline; comparison with the stopping policy chosen by a specified
covered rule; or dominance over every feasible member of the stopping
catalogue. For the last service, a sufficient certificate is
`min_b L_pi,b > appropriate overhead`, with all those pairs covered.
The other services are legitimate, but they do not imply best-stop dominance.
This is an algorithm/comparator specification issue, not a defect in the
componentwise inequality already proved.

### 4.2 Nonempty credal coverage and the correct optimization direction

The credal paragraph should explicitly require a nonempty joint-law family
that contains the actual target law on the stated event. An infimum over an
empty set must lead to an invalid/conflict status rather than a favorable
certificate. If the lower expectation is obtained through a capped solver,
the returned numerical object must be a sound **lower bound on the infimum**.
A found feasible law or sample of laws supplies the opposite optimization
direction and is insufficient for this certificate.

The paragraph's discussion of shared dependence and the root decision
criterion is correct. Complete-policy evaluation itself requires no
rectangularity assumption. If deployment later substitutes conditional
worst-case continuations for the certified complete policy, it has changed
the policy and must validate the new map. The snapshot explains the
joint-versus-branchwise distinction but can state this execution consequence
more directly.

## 5. Remaining displayed claims checked

- **Repricing (§3.2): sound.** The all-constant-price claim follows from one
  simultaneous coordinate event. The text correctly excludes arbitrary
  `lambda(X)`, changed maps and selected individual queries. The guarantee
  concerns the same deployment feature law, including the fixed initial state.
- **Setup inequality (§4): sound with its horizon convention.**
  `H[L-h]>S` uses per-episode overhead `h`, one-time setup `S`, the same
  future law, and actual or explicitly hypothetical `H`. The text already
  warns that successful-branch profitability did not justify the original
  purchase. Preserve those qualifications in the implementation report.
- **Own-procedure audit (§4): sound.** Conditioning on earlier design data
  and auditing a frozen closure on fresh independent bounded episodes is
  valid. Frozen existing profile/cache contents mean an audit of that warm
  initial state. An audit of a cold profile-building procedure must instead
  include that acquisition inside every sampled complete episode. The
  snapshot appropriately distinguishes changing the procedure during the
  audit from fixed within-episode adaptation.
- **Signal witness (§5): arithmetic correct.** Signal A leaves posterior
  `1/2` with probability `21/25`, so Brier loss is `(21/25)(1/4)=21/100`.
  Signal B has posterior losses `(3/10)(7/10)=21/100` on either branch.
  Both improve Brier loss by `1/25`. At threshold `9/10`, A lowers task loss
  from `1/2` to `21/50`, a gain of `2/25`; B changes no action and has gain
  zero. At purchase cost `1/25`, only A has positive net gain. For precision,
  the conclusion is about a Brier-only or proper-score-only profile; the
  two experiments do not have equal hard-classification accuracy.

## Review disposition

The preserved draft supports its elementary finite certificate and profile
construction. The announced continuation/all-in split, hard upper screen and
finite-prefix radius are valid refinements under the conditions above. The
remaining missing quantifiers concern the selected baseline, nonempty credal
coverage, complete execution-level sampling, and the exact timing/scope of
assessment costs. This review does not assert P3-07 completion, contribution
support, implementation validation, or passage of a later gate.
