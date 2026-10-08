# P3-05 — joined certificates and edit-stable information

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 8, 2026 UTC.
Continuation S3 of P3-05-R1. **Complete at its stated finite scope; execution and closing
assessment are recorded separately.** This extends, rather than replaces,
[CT05-1–5](05_counterfactual_transport.md). All evidence is DEVELOPMENT.

## 1. The missing quantifier in a proof portfolio

Let the current finite feasible source be $`F\subseteq\{0,1\}^n`$,
with exactly interpreted scalar rational rank $`\rho`$ and a *single fixed*
receiving loss difference $`d`$. A checked feasible incumbent $`z\in F`$
gives $`u=\rho(z)`$. Define

```math
Q_u=\{y\in F:\rho(y)\le u\},\qquad S=\arg\min_{y\in F}\rho(y).
```

Both sets are nonempty and $`S\subseteq Q_u`$. The incumbent need not be
optimal. Its discovery, checking and evaluation are charged. Unknown source
facts are not optimized away: where a request has distinct exogenous cases,
apply the construction separately and cover all cases as in P3-04.

An admitted old certificate i proves $`d_i(x)\le b_i`$ throughout a known
old domain

```math
G_i=\{x\in F_i:\rho_i(x)\le h_i\}.
```

Fix a declared map $`\pi_i`$ from current assignments to old assignments and
positive scale $`\alpha_i`$. A certificate's applicability and its loss
correction can depend on the current case. Correct portfolio coverage is

```math
\forall y\in Q_u\;\exists i:\quad
\pi_i(y)\in G_i\quad\hbox{and}\quad
\alpha_i b_i+d(y)-\alpha_i d_i(\pi_i(y))\le B.
```

The order cannot be replaced by "one proof works everywhere" without losing
valid opportunities. Neither can it be weakened to "every case has a good
*action*" when the receiving action cannot observe that case. Only the proof
of the already fixed comparison may vary.

### CT05-6: joined domain-and-loss certificates

If the displayed coverage condition holds and every old certificate and map
has its stated meaning, then $`d(y)\le B`$ for every $`y\in S`$.
For each y choose a witnessing i. Its old inequality and positive scaling give

```math
d(y)=\alpha_i d_i(\pi_i(y))+
          [d(y)-\alpha_i d_i(\pi_i(y))]
 \le \alpha_i b_i+d(y)-\alpha_i d_i(\pi_i(y))\le B.
```

This is an elementary combination of conditional inequalities. Its constructive
content here is the finite certificate interface below: applicability is
checked over a cover, rather than assumed from the presence of handles in a
cache. The theorem concerns a bound, not exact identification of S or the
sharpest B. Rejecting this sufficient route does not refute the actual selected
comparison. In particular, a bad point in $`Q_u\setminus S`$ may defeat a
weak incumbent even though every true optimum obeys B.

## 2. Conditional numerical side certificates

On a partial Boolean cell C, construct a list of expressions $`g_j`$ that
are known to be nonpositive on $`C\cap Q_u`$. These can include the actual
current hard constraints, equality consequences of those constraints, fixed
cell coordinates, and $`\rho-u`$. Every generated row needs its elementary
semantic justification; a caller's unchecked list is not a source of premises.

**CT05-7: nonnegative-combination certificate with interval remainder.**
To certify $`t\le c`$, supply finitely many $`\lambda_j\ge0`$ and verify

```math
\sup_{y\in C}\left(t(y)-\sum_j\lambda_j g_j(y)\right)\le c.
```

A sound enclosure of that residual suffices. For each current relevant y,
$`\sum_j\lambda_jg_j(y)\le0`$, so adding it back proves the target. A signed
combination of an *equality* is permitted only because both opposite
inequalities are explicitly justified. Negative multipliers on a one-sided
row are not permitted. This direct arithmetic does not rely on LP solver
correctness or on statistical independence of expression features.

For example, from current hard equalities $`p=0`$ and $`q=p`$, the rows
$`p\le0`$ and $`q-p\le0`$ certify $`q\le0`$ with weights (1,1). Merely
looking for the old literal $`q=0`$ among current rows misses this implication.
Discarding $`p=0`$ makes the same certificate invalid. The test case does not
require a theorem-proving oracle.

### Truth and rank obligations

For a mapped old Boolean premise h, certify $`1-h\le0`$. Exact equality
$`a=b`$ can instead be discharged by both directions $`a-b\le0`$ and
$`b-a\le0`$. Conjunction is discharged by its two conjuncts. There is no
corresponding rule that silently treats each disjunct as true.

The old domain obligation is $`\rho_i\circ\pi_i\le h_i`$. The loss obligation
is $`d-\alpha_i(d_i\circ\pi_i)\le B-\alpha_i b_i`$. These may use current
premises conditionally. Rank units and loss units remain distinct: the
external numerical adapter normalizes their explicitly interpreted rows,
with coefficients in the appropriate target/source units. It is not a native
proof introducing an undeclared reverse conversion into the phase-two calculus.
The executable restricts old and current loss reports to the same named unit.

## 3. A finite checked cover, not a list of visited cases

A binary split tree starts at the whole current Boolean box. A split on an
unassigned bit must contain both children, fixing that bit to zero and one.
Every leaf has one of the following independently verified meanings:

1. The current hard constraints make that leaf irrelevant.
2. Its current rank is strictly above u, so it contains no point of $`Q_u`$.
3. A named admitted old certificate is applicable there, and its mapped
   hard, rank and receiving-loss obligations are proved by CT05-7.
4. Optionally, a *fresh current* proof establishes $`d\le B`$ on that leaf.
   This is reported as direct proof, not credited as old-proof reuse.

**CT05-8: receiver soundness.** A verified exhaustive tree, a valid current
feasibility witness and exact independent binding of the receiving frame imply
$`d\le B`$ on every current minimizer. Induct on tree structure. Every relevant
point follows one branch at each split; it cannot terminate at a justified
exclusion; a reuse leaf supplies CT05-6 and a direct leaf supplies its checked
current inequality. Current nonemptiness is established separately by z.

An old tree may certify an empty old band: that alone is not a useful result.
The new witness and complete mapped coverage prevent an empty band from being
used to invent a favorable current action. A missing sibling, changed current
record, forged cutoff, wrong unit or unverified cache entry is a rejection,
not a negative conclusion about the mathematical task.

### Relative completeness and the obstruction it actually proves

Fix the old certificates, maps, positive scales, target B and incumbent u.
If every point of $`Q_u`$ has at least one witnessing portfolio member as in
section 1, exhaustive splitting into single points produces a valid tree:
all mapped formulas and corrections are exactly evaluable at each point.
If direct proof is allowed, the corresponding sufficient condition can also
be met by $`d(y)\le B`$ itself. This is a finite relative-completeness argument,
not an efficiency theorem or completeness of the capped implementation on
arbitrary input sizes. The supported finite shape must fit its caps.

When the per-point retained allowance is too loose, a better theorem may still
exist: old proof alternatives, a tighter old bound, another map, a better
incumbent, different lemmas, or fresh direct reasoning can change the outcome.
A receiver must not call an uncovered point a new optimum without separately
establishing its optimality.

## 4. Complementary domains without hidden action selection

Take p,q,r Boolean. The current source has hard $`p=q`$ and $`r=1`$;
rank is zero. The receiving difference is

```math
d(p,q,r)=\max(p-q,q-p)-1.
```

Old certificate 0 has hard $`p=q=r=0`$; certificate 1 has hard
$`p=q=1,r=0`$. Both prove the same difference at most -1 on their rank-zero
bands. Map old coordinates to $`(p,q,0)`$. Neither old domain covers the
entire current source under this fixed map, but they jointly cover it. Split
only on p; the current equality discharges q's corresponding old literal.
Every old feasible state has r=0 whereas every current feasible state has r=1:
no old state survives literally. The common receiving comparison still holds.

A strong ordinary symbolic method can also simplify the current expression
using $`p=q`$. Thus this is a coverage/conditional-discharge separator, **not**
a speedup against the best ordinary method. The cache, proof discovery and
per-edit checks have distinct costs.

For contrast, let actual actions have losses $`\ell_A(p)=p`$ and
$`\ell_B(p)=1-p`$. A is good at p=0 and B is good at p=1. Combining those
local choices does not certify one unobserving action as always good.
For the fixed receiving difference $`\ell_A-\ell_B=2p-1`$, the p=1
correction defeats a target of zero. A shared display label or proof name
cannot override the independently bound receiving expression.

## 5. Status and research relevance

These proofs supply a conditional finite extension of the existing static
transport service. No probability learner, LI anticipation, calibration or
self-trust result is supplied. The relevant duties remain C01–C03, R01, I01
and V03/V04. The strongest ordinary comparisons include incremental checking,
optimization reuse and symbolic premise reasoning. Their interfaces and
limits are recorded in [the S3 source cards](../literature/05_portfolio_sources.md).

P3-N01 remains NOT YET SUPPORTED. The exact candidate delta is a joined
*selection-coverage and current-loss* receiver, not the generic fact that
proofs can be cached. Execution coverage, actual resource comparisons and
current task timing must be recorded before closing P3-05.

## 7. What guarantee the consumer actually obtains

There are three distinct acceptance targets. First, a checked old inequality
is a conditional theorem on its recorded domain. Second, the new cover proves
that the current selected alternatives lie in domains where the corrected
*one receiving comparison* holds. Third, a policy may decide what to do with
that comparison. These do not require recovering the exact current minimizing
family, its probability law, or every absolute action cost. Conversely, a
selected point or a stored small scalar cannot replace the cover obligation.

For a fixed supplied action a and finite comparison catalogue B, one can compile

```math
 d_a(y)=\ell_a(y)-\min_{b\in B}\ell_b(y)
       =\max_{b\in B}\bigl(\ell_a(y)-\ell_b(y)\bigr).
```

If all expressions fit the admitted grammar and the receiving procedure binds
this actual construction to the request, a certified upper bound epsilon on
this difference is a uniform regret guarantee for a. It remains a fixed-action
service: the benchmark's pointwise minimum is not an agent action that sees the
hidden case. This is a specialization of P3-03's existing named-action result,
not a new online regret theorem. The current P3-05 frontend directly binds a
pair; it does not automatically authenticate an arbitrary user term named
`regret` against an unprovided action catalogue.

This distinction puts the new results on the decision-directed reasoning side
of the Logical Induction comparison. They preserve justified conditional
comparisons while evidence, costs or a stipulated hypothetical change; they do
not establish better pre-resolution forecasts. Actual computation purchase,
calibration, predictor regret and source-model adequacy still require their
separate later analyses. A positive conditional regret bound is not a proof
that paying to obtain it was worthwhile. The saved ordinary-ADD comparison
shows why construction and checking cost must remain separate endpoints.
