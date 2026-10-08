# P3-05 — Repeated reuse and loss of correction information

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 8, 2026 UTC.
Status: S3 finite derivation and development checks complete. This concerns the existing
[portfolio receiver](05_portfolio_transport.md), not a new learning task.

## 1. A checked chain is a sequence of new conditional theorems

Suppose an admitted certificate proves $`d_0\le b_0`$ on domain G0. A later
receiver checks that its entire nonempty incumbent sublevel G1 maps into G0
under $`\pi_1`$, and checks a correction
$`\delta_1=d_1-\alpha_1 d_0\circ\pi_1`$ with positive scale alpha1.
Its report at bound b1 can be admitted as a certificate on **all of G1**, not
just its unknown minimizing subset. This distinction permits the next reuse
step to have the same domain contract. Repeating this procedure does not
assume that any earlier source point or minimizing case survives literally.

**CT05-17 — sequential admission soundness.** A finite ordered sequence of
successful admissions by the portfolio receiver preserves validity of every
stored bound on its recorded incumbent sublevel. Induct over admissions.
The base entries have independently checked old band proofs. Each subsequent
entry uses only earlier admitted entries, and CT05-8 establishes its current
bound throughout its full sublevel. The receiver then stores that new
conditional theorem under a fresh handle. Its current feasible incumbent
establishes nonemptiness. There is no circular endorsement.

In the executable, an unadmitted handle, a duplicate handle, a changed frame,
or an omitted receiving obligation is rejected. Reconstructing a cache from
untrusted saved data must replay admissions in order. A list of displayed
reports or matching digests is not a replacement for that replay. The private
in-process cache is trusted after admission; this is not a cryptographic
persistence or arbitrary Python-memory security claim.

Where a portfolio uses different ancestors on different proof cells, induction
still applies pointwise. The receiver does not need a globally fixed ancestor,
but it does need the same fixed receiving comparison on every cell. Case-varying
proof choice cannot implement a hidden-case-varying action.

## 2. Exact corrections compose differently from scalar allowances

For one ancestor per step, assume the same well-typed maps and loss semantics.
Writing $`\Pi=\pi_1\circ\pi_2`$, direct algebra gives

```math
d_2-\alpha_2\alpha_1 d_0\circ\Pi
 =\delta_2+\alpha_2\delta_1\circ\pi_2.
```

If separate uniform bounds $`\delta_1\le e_1`$ and $`\delta_2\le e_2`$
apply on their respective mapped domains, their sum yields the valid allowance
$`e_2+\alpha_2e_1`$. It need not be the sharpest allowance on the actual
shared source. The two corrections may cancel. Replacing them by their maxima
loses that relationship. This is ordinary composition of conditional inequalities,
consistent with phase two's shared-source arithmetic; it is not a new generic
error-propagation theorem.

### A strict finite example

Use one unresolved Boolean coordinate x, no rank preference, and an original
source $`G_0=\{0\}`$ with loss difference $`d_0=0`$ and bound zero.
The first new source is $`G_1=\{0,1\}`$, with map $`\pi_1(x)=0`$ and
$`d_1(x)=x`$. Its smallest uniform bound is one. Admit that actual bound.
The second source is the same Boolean set, the next map is identity, and
$`d_2(x)=0`$. The second correction is minus x. Separately maximizing the
first correction x and the second correction minus x gives allowances one
and zero, hence the loose chained result one. Retaining their joint expressions
gives $`x-x=0`$, and the direct root map proves the sharp bound zero.

A chain route restricted to the scalar b1=1 cannot certify the new bound zero
by $`1-x\le0`$ at x=0. The stored d1 expression does not cure the slack in
that old *uniform bound*. The current direct proof $`d_2=0`$ of course also
works, as does reusing the retained original root certificate. The example
therefore separates information/service choices, not the best possible ordinary
algorithm. Reusing only the latest bound is sound but can be unnecessarily weak.

## 3. Repeated source revisions still require real checking

A theorem $`d\le B`$ on a complete earlier feasible set survives restriction
to a nonempty subset. A theorem on an earlier **selected sublevel** survives
only when the newly selected cases are covered by the transported old domain.
Withdrawing a premise, changing rank weights, or altering the program route
can break that containment. Chaining numerical bounds without rechecking it is
not justified by temporal proximity or by unchanged display names.

A changing task price can also turn a previously sufficient scalar into an
insufficient summary. The original expressions and supporting hypotheses can
permit a new proof; their availability and checking cost must be counted.
The [edit-information analysis](05_edit_information.md) characterizes exact
future services under a supplied finite edit graph. It does not grant that
whole graph or future comparison answers to the online receiver for free.

## 4. Intended development checks and scope

The chain diagnostic exercises ordered cache admission, reuse of a reused
certificate, replay from complete original proof inputs, competing ancestors,
positive scaling, repeated value changes, and rejection of stale or circular
metadata. A separate finite reference enumerates each actually requested
sublevel after each accepted step. That enumeration is development validation,
not a feature handed to the agent. A failed restricted chain route is retained
as a failure of that route, not evidence that the new comparison is false.

This result contributes to R01/I01 and the P3-05 repeated-edit requirement.
It supplies no anticipation, calibration, feedback-learning or counterfactual
structure-discovery guarantee. P3-N01 retains its separate contribution review.
