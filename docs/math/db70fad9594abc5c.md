> **Portable math view.** [Preserved source](../../v3/work_logs/P3_10_2026-10-11_S1/decision_service_interpretation.md) · [Formatting and provenance](../math_markdown.md).
> Mathematical delimiters and the repository's operator notation are normalized;
> relative links are rebased. The source's evidence bytes remain unchanged.

# What the tied decision fixture does and does not encode

Contributor: **ChatGPT (GPT-6 Astra Pro), principal /root**, 2026-10-11.
Status: post-outcome mathematical interpretation of the already reconstructed
P3-10 conformance loss tables. No new fixture, paid policy, or endpoint is run.
The conclusions below are elementary implications of the declared service;
they are not a P3-11 contribution or author-gate assessment.

Sources: the [frozen structural worker](../../v3/experiments/frozen_v1/source/v3/experiments/p308_structural.py),
[independent conformance reconstruction](../../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/REVIEW.md),
[assumption matrix](../../v3/work_logs/P3_10_2026-10-11_S1/reviews/conformance_reconstruction/assumption_matrix_v1/output/matrix.md), and
[accepted expected-loss observation theorem](../../v3/derivations/02_probability_information.md).

## 1. A correct pure minimax choice need not be optimal under any one law

The named `counterpossible_tied_minima` fixture retains two states. Its complete
loss table is

| Action | First retained state | Second retained state | Maximum loss |
| --- | --- | --- | --- |
| `take_p` | 4 | 0 | 4 |
| `take_r` | 0 | 4 | 4 |
| `fallback` | 3 | 3 | 3 |

The frozen consumer chooses **one action from this finite deterministic menu**
before resolving the state. Fallback is therefore its unique minimax action.
The independent ordinary implementation chooses the same action. This is a
correct result for the declared consumer policy.

Now suppose one tried to infer a probability law from that choice, while
interpreting it as minimization of expected loss for the same menu. Let p be
the probability of the first state. The three expected losses would be

```math
4p,\quad 4(1-p),\quad 3.
```

For every p in [0,1], at least one specialized action has expected loss at
most 2. Thus fallback is **never** an expected-loss minimizer for any law on
these two states. The observed minimax choice cannot be treated as a hidden
Bayesian estimate whose associated probabilities can simply be recovered.
This is not a contradiction in the implementation: minimax and expected-loss
minimization are different declared policies.

The robust action values `(4,4,3)` themselves also fail the linear identities
of a shared expected-loss observation. The first two loss rows sum to the
constant row `(4,4)`, so any common normalized law must give expected values
summing to 4. The two robust maxima instead sum to 8. The maximum functional
is not a linear expectation functional. Useful costs or risk bounds do not
become probability observations without the exact Q5 observation assumptions.

## 2. A hypothetical lottery changes the objective's quantifiers

A fair independent lottery choosing each specialized action with probability
one half has conditional expected loss 2 in **each** retained state. Therefore
its worst-over-states expected loss is 2, smaller than fallback's 3. This
analytic comparison does not use the true state and needs no learned law over
the two states, but it assumes the indicated independent action randomization.

It does not have realized loss at most 3: its worst loss over the retained
state **and the realized draw** is 4. Thus it does not give uniform realized
non-deterioration relative to fallback. The two relevant quantities are

```math
\max_x\mathbb E_U[\ell(A(U),x)]=2,
\qquad
\max_{x,u}\ell(A(u),x)=4.
```

The frozen structural menu has no lottery action, random-bit contract or paid
implementation of that expanded consumer. No randomized policy is added to the
executed ordinary catalogue or credited with a resource saving here. The
calculation only shows why “best fixed action in the declared menu” must not be
reported as optimality over every randomized or differently risk-constrained
decision service. The broker's separate stochastic-action theorem cannot be
silently imported into the structural tariff and interface.

## 3. Loss units and state-dependent offsets distinguish the services

A common positive affine transformation of all losses,
`ell'_a(x)=alpha*ell_a(x)+beta` with alpha positive and beta constant, preserves
the pure minimax choice. Every maximum and its ordering transforms the same
way. Expected-loss choice under a fixed law has that same invariance.

If instead a common **state-dependent** term h(x) is added to every action,
pairwise same-state loss differences remain unchanged. Expected-loss action
ordering under a fixed law is unchanged as well, since the same E[h] is added
to every action. Pure minimax ordering need not be unchanged: which state
attains each action's maximum can differ.

For the displayed table, adding h=(100,0) gives rows `(104,0)`, `(100,4)` and
`(103,3)`. Their maxima are 104, 100 and 103, so the pure minimax choice becomes
`take_r`. Every same-state pairwise loss difference is identical to its old
value. These transformed numbers are a worked mathematical example, not a
newly executed P3-10 fixture. They show that the absolute-loss minimax policy
uses commensurate loss levels across retained states, beyond just action
ordering within each state.

A bound on the current fixed-pair difference D=ell_a-ell_b behaves differently:
the common state-dependent offset cancels. The uniform non-deterioration
condition `D(x)<=0` at every retained state is invariant to that offset. A
positive common scale multiplies D and its bound without changing the sign.
Thus a minimax action reply, a uniform difference-bound certificate and an
expected-loss observation have distinct mathematical semantics even when all
are colloquially described as “values.”

In the original tied table, fallback minus take_p has differences `(-1,3)`.
Its uniform upper bound is +3. The valid minimax choice is therefore not a
nonpositive difference certificate against take_p. This matches the separate
current-bound arm, whose attained positive bounds 1 and 3/2 are valid bounds
without implying non-deterioration.

## 4. Repair ranks are compared within each retained source

Let each retained source s have feasible domain X_s and rank r_s. Its selected
states are `argmin_{x in X_s} r_s(x)`. Replacing that rank by
`a_s*r_s+b_s`, with a_s positive, preserves all of its minima and ties. Since
the admitted source quantifier retains every unresolved source, the union of
source/minimum pairs and the fixed minimax decision stay unchanged.

Jointly minimizing over source and repair would not have this invariance. In
the recorded two-source fixture, minimum ranks 1 and 2 are both retained.
Adding 1 to every rank of the first source leaves its own minimizers unchanged
but changes a joint rank comparison from a strict preference to a tie. Adding
2 instead reverses the joint source preference. None of these sourcewise
offsets changes which states minimize inside a source. Treating source choice
as repair minimization would therefore add a cross-source scale/offset policy
that the admitted contract did not supply.

The separate incumbent-sublevel service has a related ordinal invariance:
`r(x)<=r(w)` is equivalent to `a*r(x)+b<=a*r(w)+b` for positive a. It includes
every minimizing tie and does not require w to be optimal. The statement is
conditional on the same feasible domain and an admitted transformed encoding.
The deployed formats have rational and grammar caps, and transformed source
bytes change request identity and potentially cost. Mathematical equality of
domains does not automatically make an old receipt current, preserve a paid
invoice, or imply that every transformed encoding is admitted. Fresh binding
or a checked transport argument is still required.

## 5. Consequence for the five-question interpretation

Q2 obtains a concrete finite semantics and the stated pure minimax consumer,
with complete ties and unresolved-source quantifiers. Q3 gets a constructive
ordinary realization of that same service, not an exclusive value-theoretic
decision advantage. Q5 obtains exact probability information only from its
separate shared expected-loss observation map; the robust maxima in this
fixture are an explicit example of values outside that map. Q4's forecast and
lottery bridges retain their own feedback and randomization assumptions.

These distinctions sharpen the interpretation of existing final evidence.
They add no empirical success, new loss observation, paid comparison,
automatic contribution upgrade or next-task selection.
