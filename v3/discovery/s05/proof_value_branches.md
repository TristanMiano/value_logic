# Buying a useful proof before the requested feature

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT; no new research-clock credit from concurrent work.
Motivation: [the paid CNF comparison](cnf_findings.md). Model attribution applies
to the derivations and [threshold planner](threshold_plan.py).

The endpoint-only method initially saved work, then paid more when later
requests exposed the value of a previously unrequested weaker UNSAT proof.
The useful acquisition object is consequently not just a feature boundary.
It is an action whose checked result changes both the statistical evidence
and the cost of obtaining subsequent evidence.

The [portfolio](../candidates.md) already contains proof bundles (S03),
monotone SAT/UNSAT reuse (S07), computation-aware state (S11), and closure
optimization (S13). The branches below refine those mechanisms. They do not
claim that caching, implication, binary search or Bellman planning are new.
The concrete new specialization is a **monotone truth-transition state** that
simultaneously describes calibration features and the available proof work.

## Branch 1: a truth transition replaces unrelated parity parameters

Suppose a public revision chain only adds clauses:

```text
F_0 subset F_1 subset ... subset F_m.
```

Let H in {0,...,m+1} be the first UNSAT position, with H=m+1 when every
formula is SAT. Then SAT(F_j)=1[j<H] and X_j=2*1[j<H]-1. For a<b,

```text
1[X_a*X_b = -1] = 1[a < H <= b].
```

Every pair feature is therefore an interval-membership question about one
transition. For a general even boundary T={t_1<...<t_(2k)}, its parity-error
indicator is membership in the disjoint union

```text
(t_1,t_2] union (t_3,t_4] union ... union (t_(2k-1),t_(2k)].
```

Proof: as H moves from zero to m+1, each selected vertex changes its sign
once. The initially positive product toggles at the listed boundary positions.
With a source CDF G(t)=P(H<=t), the exact error probability is consequently
sum_j [G(t_(2j))-G(t_(2j-1))]. This joint structural information follows from
checked clause inclusion. The numerical CDF still needs paid source evidence.

### One receipt improves information and future computation

For each prospectively sampled row, retain an interval [l,u] containing H,
initially [0,m+1]. A checked SAT answer at j implies H>j and updates
l=max(l,j+1); a checked UNSAT answer updates u=min(u,j). The same receipt
settles all weaker SAT formulas or all stronger UNSAT formulas, after paying
the valid transport checks. Rows and intervals retain their immutable source
identities; a capped unresolved attempt changes no endpoint.

For a target interval A=(a,b], a row already provides exact lower and upper
indicators without always resolving H:

```text
lower = 1[[l,u] is contained in A]
upper = 1[[l,u] intersects A].
```

For a union of target intervals use the same containment/intersection rule.
In particular, a whole feature vector is settled as soon as it is constant
over all H in [l,u]. There is no need to identify the exact transition when
the consumer does not distinguish its remaining positions.

These per-row bounds can feed a valid partial-receipt calibration source.
Retain every sampled identity, including intervals that remain wide. Searching
within a row adaptively does not justify selecting only the easy rows for the
source estimate. The source agent's [notes](sources.md) develop the separate
sampling warrant. The present planner requires no source probabilities in
its minimax mode.

## A small complete-answer planning interface

First use exogenous nonnegative prices c_j for complete checked queries,
including the declared interval-update and transport work. If these prices
are only upper bounds, the result is an upper bound on the bill; it does not
prove that a competing upper bound is attained by an actual solver.

For a fixed requested feature vector g(H), let C(l,u)=0 whenever g is
constant on that entire interval. Otherwise the minimax recurrence is

```text
C(l,u) = min_(l <= j < u) [c_j + max(C(l,j), C(j+1,u))].
```

Its branches correspond to UNSAT and SAT. Every complete decision tree has
some first query j; after that query its two subtrees solve exactly the two
smaller intervals. Induction proves the recurrence's optimality under the
stated interface. Precompute where g changes, so interval constancy takes
constant time. There are O(m^2) interval states and O(m) candidate queries
per state: O(m^3) arithmetic work and O(m^2) value storage, excluding feature
compilation, source acquisition and explicit decision-tree serialization.

For a **known** threshold law q, replace the maximum with the conditional
weighted average of the two continuation values. This gives an expected-cost
benchmark. A fallible proposed q can suggest an order while all returned
truths remain checked, but the resulting cost expectation is not established
until the source law or corresponding policy-cost contrast is warranted.
The prototype's expected mode uses an explicitly supplied positive finite law.

### A useful unrequested pivot, with no source law

To acquire the parity of endpoints a<b, permit an intermediate query j with
a<j<b. If F_j is SAT, F_a is SAT and only F_b needs another answer. If F_j
is UNSAT, F_b is UNSAT and only F_a remains. With prices including transport,

```text
bridge-first worst bill <= c_j + max(c_a,c_b).
endpoint-only worst bill = c_a + c_b,
```

where the equality is for the abstract exact-price observation model: a
transition between a and b forces both endpoint queries. Thus an intermediate
complete answer cheaper than either endpoint gives a strict improvement in
that model. With c_a=c_b=10 and c_j=1, the worst bill is **11 instead of 20**.
If transfer prices t_(j->a) and t_(j->b) are separate, the bridge bound is

```text
c_j + max(t_(j->a)+c_b, t_(j->b)+c_a).
```

The observation is useful in both outcome branches. It narrows the feature
uncertainty and creates exactly the proof knowledge that reduces later work.
The planner must allow unrequested pivots to express this option.

This does not establish a CNF runtime saving. Actual complete-query prices
are outcome- and cache-dependent, and a strong direct policy-bank controller
can use the identical pivot. The comparison to develop is whether a practical
controller can find and pay for these bridge opportunities efficiently.

### What a solver cap does and does not supply

A cap that may return unresolved is not c_j in the complete-answer recurrence.
Its unresolved branch leaves [l,u] unchanged. Exact completion then needs a
separately priced complete fallback or retained solver-progress state; repeated
uninformative capped calls do not supply a finite completion guarantee.
The current prototype does not hide an unresolved branch or assume success.

Even after complete answers, [l,u] alone may not determine future CNF work.
Two checked SAT witnesses can agree on every chain label already known but
behave differently under later clause additions. Different UNSAT cores or
retained solver searches can likewise change what is cheap. The real cost
state must be at least

```text
(threshold interval, witness/support identities, solver progress,
 receipt index, remaining requested feature vector).
```

A state-dependent c_j may be used only if it is a valid function or bound for
that retained state. Treating two such states as equal because they have the
same statistical interval repeats the common-baseline problem identified by
S11. A small first implementation can retain interval logic plus an explicit
receipt cache and use upper prices for robust advice, then charge its actual
outcome-conditioned bills.

## Branch 2: a capped bridge with a protected fallback

For general revision graphs, an unrequested weaker formula may help only on
UNSAT. Let pi_0 be a specified strong continuation with the current receipt
cache, and let pi_b first try bridge b. On a successful useful proof, complete
the same current calibration duty by checked transfer; otherwise return to
pi_0. Write S for useful bridge success, W_0 for pi_0's remaining work, T_b
for successful transfer/completion work, and C_b for the extra bridge bill,
including unsuccessful attempts and cache-copy/registry work. For a protected
fallback that reproduces pi_0's old state when the bridge is unhelpful,

```text
E[W_0-W_b] = E[1_S*(W_0-T_b)] - E[C_b].
```

The success event and saved baseline work are generally dependent. Learning
their separate averages and multiplying them can misprice the bridge.
A usable lower purchase rule is

```text
g_lower > c_upper,
```

where g_lower warrants E[1_S*(W_0-T_b)] under the declared source and
c_upper bounds the bridge bill. A weaker sufficient condition is
p_lower*s_lower>c_upper when the conditional saving is at least s_lower
whenever S occurs. These are explicit paid or structurally supplied premises;
the current row's hidden diagnostic labels cannot select b.

For illustration, let H be uniform on 0,...,3, request pair (1,2), and use
prices (1,10,10). Querying endpoint 1 then endpoint 2 when necessary costs
15 on average. Trying weak vertex 0 first costs 13.5. Success occurs with
probability 1/4, but that is precisely the branch where the baseline costs
only 10. The correct saving is (1/4)*10-1=1.5, not (1/4)*15-1. A bridge-first
policy costs 21 in its worst case, so the minimax planner retains the
endpoint-only value 20. The source law is supplied only for this illustration.

If no source expectation is warranted, a fixed extra-work budget B still
limits the bridge's additive downside to B plus explicitly bounded restoration
overhead. This is an operational exploration budget, not proof of positive
expected value. Keep a strong fixed structural ordering and ordinary
incremental solving as controls.

### Avoid crediting the same statistical improvement twice

If both continuations finish the same feature observations, those observations
have the same final statistical value. Their acquisition-cost saving is the
relevant difference. A bridge must not earn both that full saving and a second
bonus for evidence the baseline would also obtain. Additional retained labels
can have future value only relative to stated later requests or a warranted
request model. Unknown repetition counts cannot make setup work disappear.

For a confidence-width or action-warrant objective, use a continuation state
containing both partial calibration evidence and the receipt cache. Precision
reduces the remaining number of observations; proofs reduce their remaining
cost. A generic Bellman equation then values both through remaining work to
the same stated decision duty. This is an interface prescription; the chain
DP above supplies a concrete tractable part of it.

## Branch 3: implication frontiers in a partial order

In a clause-inclusion partial order, keep maximal known-SAT elements and
minimal known-UNSAT elements. They represent respectively the SAT downset
and UNSAT upset. Removing a redundant frontier element must preserve its
historical proof and any distinct useful witness, not erase that evidence.

An unrequested bridge can cover many currently needed endpoints in either
outcome direction. Generate candidates near the unresolved frontier, then
score a small menu using its coupled completion-work contrast. A cache-aware
conventional controller receives the same bridges, witnesses and implication
checks. Summing per-endpoint saved costs is only a heuristic when those costs
share proof work; use disjoint primitive-cost lower bounds or a paired
continuation comparison for an actual guarantee.

This generalizes the chain's single transition to a moving antichain boundary.
It may support branching edits while retaining compact structural information,
but a polynomial-size frontier or optimal planner is not asserted for an
arbitrary poset. Start with a few chains sharing ancestors, and keep ordinary
cost-aware frontier search alongside a proposed statistical acquisition rule.

## Executed developmental screen and next useful step

Run: `python v3/discovery/s05/threshold_plan.py`.
[Source-bound output](threshold_plan_results.json) records **36 systems**,
**72 mode comparisons**, and **3,600 explicit threshold rollouts**. For
2,3,4 vertices, all single-pair targets and the all-pair vector were checked
under three positive price vectors. The DP values agree with enumeration of
every feature-stopping ordered query tree and explicit execution on every H.
The expected-mode law is positive and specified; minimax mode uses no law.
The two bridge examples above also match their exact arithmetic.

This is one small semantic/cost-model screen. It does not measure a CNF
speedup, source-calibration coverage, or a contribution gate. The next useful
step is an actual monotone CNF-revision chain with paid interval receipts,
source-safe partial calibration, and an explicit cache-aware query bill.
Compare endpoint-only, fixed structural bridge order, and the identical
ordinary interval/frontier planner. Broader mixed-edit posets remain open.
