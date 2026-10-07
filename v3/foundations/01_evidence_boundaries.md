# P3-01 — evidence boundaries for the comparison contract

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 7, 2026 UTC.
Scope: definition reconstruction and elementary separating arguments for
P3-01. These are development evidence, not a new learner, a general
counterpossible semantics, or a novelty claim. Read with the
[main contract](01_problem_contract.md), [duties](01_desiderata.md) and
[source contracts](../literature/01_source_contracts.md).

## 1. Finite checked information is a legitimate comparison object

Logical Induction (S01, Definitions 3.2.1–4) assesses a market against Boolean
worlds compatible with a finite, growing disclosure record `D_t`. This is
different from giving a bounded reasoner the full models of its theory.
At the Boolean layer a quantified sentence can be a prime atom; quantifier
relations require their own admitted axioms or checked derivations.

Let `A` contain every prime atom used by the finite record `D` and the
currently queried formulas. Define

$$
V=\{v\in\{0,1\}^{A}:v\models D\}.
$$

Then `V` is exactly the restriction to `A` of `PC(D)`. Restricting any world
in `PC(D)` gives a satisfying assignment. Conversely, extend any satisfying
assignment on `A` arbitrarily to all other prime atoms and evaluate compounds
by their Boolean rules. No sentence of `D` depends on those other choices,
so this extension is in `PC(D)`. This proves the finite restriction identity.
It neither decides consistency with the entire arithmetic theory nor licenses
unbudgeted computation: enumeration visits up to `2^|A|` assignments before
formula evaluation, storage and projection costs.

The premises matter when a smaller interface is used. Take

$$
D=\{u\lor z,\ u\lor\neg z\}.
$$

Every satisfying assignment has `u=1`. Exact projection onto `u` is therefore
`{1}`. Dropping both clauses because each mentions the omitted variable `z`
leaves `{0,1}`. This is a sound outer approximation, with weaker information;
it is not exact projection. Deriving `u` or eliminating `z` is an operation to
perform and charge.

Also distinguish an outer approximation from found cases. If the true target
family is `V` and a certified set `Vplus` contains `V`, then

$$
\inf_{v\in V^+}\ell(v)\le\inf_{v\in V}\ell(v),\qquad
\sup_{v\in V}\ell(v)\le\sup_{v\in V^+}\ell(v).
$$

These give conservative bounds when the families are nonempty and the bounds
are defined in the stated extended-value domain. A sample `F` contained in
`V` generally gives the reverse optimization inequalities. For example,
`V={0,1}`, `F={0}` and `ell(x)=x` yield sample maximum zero but true maximum
one. Listing some found worlds does not certify an upper task-loss bound.
No numerical confidence label repairs the missing set-containment evidence.

These observations specify O-FINITE's possible services. They do not show
that any particular representation computes them cheaply. The full same-model
reconstruction is in the [finite information review](../work_logs/P3_01_2026-10-07_S1/reviews/li_information_boundary.md).

## 2. Exact finite coherence and eventual fixed-query truth are weaker than LI

A coherent forecast at every finite date can still systematically ignore an
easy pattern among newly arriving sentences. The following direct witness
separates the quantifiers; it is deliberately not a strong practical baseline.

Use atoms `A_1,A_2,...`, a consistent theory containing every `A_k`, and the
finite record

$$
D_n=\{A_k:2^k\le n\}.
$$

This witness uses a propositional comparison language; it does not implement
the full arithmetic reference language. It separates the stated abstract
coherence/convergence duties under that explicit fragment.

Their union is the theory's stated generating set, hence has the same Boolean
assessment worlds. At date `n`, set disclosed atoms to one and treat every
undisclosed atom as an independent fair bit. Evaluate a requested finite
formula by finite averaging over the undisclosed atoms it contains. This is
a computable rational pricing, coherent with `D_n`. Every fixed formula
eventually gets its correct value in the all-true-atom world. Yet

$$
P_n(A_n)=1/2
$$

at every date, because `2^n>n`. Correctness for each fixed query does not give
correctness on this efficiently generated moving sequence.

There is a direct exploiter. Set `t_1=1` and `t_(j+1)=2^(t_j)`. Buy one share
of `A_(t_j)` on day `t_j`. The next purchase occurs only when the previous
claim is disclosed. With `k` purchases made, all but the last holding have
payoff one in every currently plausible world. Wealth is

$$
\frac{k-1}{2}+W(A_{t_k})-\frac12
\in\left\{\frac{k-2}{2},\frac{k}{2}\right\}.
$$

It is uniformly at least `-1/2` and unbounded above as `k` grows. The trader
has constant continuous coefficients and can decide purchase-day membership
in time polynomial in unary `n`: do not construct a next tower value when
its exponent exceeds `floor(log2(n))`. This is within S01's efficient-trader
interface. Thus the pricing fails LI even though it has both exact current
coherence and pointwise eventual correctness. A finite simulation is not the
proof of this unbounded statement; the argument supplies its quantifiers.

## 3. LI does not require exact hard-evidence coherence on every finite day

For this direction we need only a **finite-coordinate perturbation** result.
The original paper's Theorem 4.6.1 states a broader finite-day result. A known
correction, S16, shows why that unrestricted import is unsafe: a whole pricing
on one early day can contain infinitely many later-queryable quotes, which
can act as computational advice. Finitely many day indices do not imply a
finite table of historical values. The paper's §4 covers general computable
markets, not only its narrower finite-support belief states.

The pinned primary formalization declares preservation when a finite set of
`(day,sentence)` coordinates contains every difference. We inspected its
declarations and correction mechanism; we did not build Lean or audit the
entire refutation. The following direct reconstruction is sufficient here.

Let computable markets `P` and `Q` differ only within a fixed finite set `K`
of dated quotes, and use the same deductive process. For an efficient trader
against `P`, replace each coefficient-expression leaf referring to a quote
in `K` by that quote's original rational value in `P`. Leave other leaves
unchanged. Finite literal matching and substitution add polynomial overhead;
the finitely many rational constants have fixed finite encodings. Structural
induction on expressions shows that the transformed coefficients evaluated
against `Q` equal the original coefficients evaluated against `P`.

The transformed trader therefore buys the same share quantities, at the
actual current prices of `Q`. Its cash account can differ only at `K`.
Writing `a_(i,phi)` for the original quantity, the cumulative wealth difference
has absolute value bounded by the fixed finite constant

$$
C=\sum_{(i,\varphi)\in K}
\left|a_{i,\varphi}(P)
\bigl(P_i(\varphi)-Q_i(\varphi)\bigr)\right|.
$$

Uniform lower boundedness and unbounded upper wealth are preserved by this
bounded difference. Exploitation transfers in both directions by exchanging
`P` and `Q`. The restricted result is a reconstruction of an established
argument, not a priority claim.

Now take an LI over a consistent process with `theta` disclosed at day one.
Change only `P_1(theta)` to `1/2`. This changes at most one coordinate, so
preserves LI. Every world in `PC(D_1)` satisfies `theta`, but its quote that
day is one-half. Exact correction at the next eligible update can still be
our engineering requirement U04; it is not a finite-time consequence of LI.

The earlier review's broad invocation of Theorem 4.6.1 is superseded for this
purpose by the [source-scope correction](../work_logs/P3_01_2026-10-07_S1/reviews/finite_perturbation_scope.md).
That review gives the full cash-account identity and exact pinned declarations.
This preserves the witness while narrowing its support. No other LI property
is declared false merely because this proof import needed correction.

## 4. An exceptional hypothetical rule is additional semantics

The ordinary interpretation of `p and not p` has no Boolean satisfying world.
GC01 keeps that original fact and introduces a separately labeled hypothetical
evaluation on triples `(x,n,z)`: `p` receives `x`, `not p` receives `n`, `q`
receives `z`, and `not q` receives `1-z`. The exceptional hypothetical states
allow `n` to differ from `1-x`; ordinary states keep `n=1-x`.

The antecedent together with the stipulated frame `q=0` selects `(1,1,0)`.
Under that table it supports `p`, `not p` and `not q`, while not supporting `q`.
With continuation loss `4z` and fallback loss one, the stipulated case gives
costs zero and one. Without the frame, continuation costs range over `{0,4}`.
The frame, not the value notation, accounts for that difference.

An ordinary repair of the original Boolean constraints with the antecedent
hard has no feasible case. A reified three-bit representation can reproduce
GC01 by explicitly relaxing the link `n=1-x`. This is a fair reconstruction
of the added hypothetical rule; it does not make the selected state an
ordinary Boolean model of the original contradiction. Neither presentation
has justified the relevance of the chosen exception merely by defining it.

The diagnostic therefore establishes the existence of a specified finite
service with a visible exceptional link, not a satisfactory semantics for
arbitrary mathematical counterpossibles. P3-04 must defend a rule against
relevance, refactoring and transport objections, or say what remains open.
S07 §3.1 is relevant: classically equivalent impossible antecedents can differ
under the selected counterpossible treatment. Invariance must name the maps
it actually preserves; demanding unrestricted classical closure would change
the target.

GC01 was developed with its numerical consequences visible. Its stated frame
is an input, not evidence of preregistration. Any confirmatory comparison
requires a later prospectively fixed selection procedure. See the
[target note](../work_logs/P3_01_2026-10-07_S1/reviews/genuine_counterpossible_target.md)
and [closure review](../work_logs/P3_01_2026-10-07_S1/reviews/counterpossible_closure_review.md).

## 5. What these boundaries require of later work

| Boundary | Contract consequence | Owner |
|---|---|---|
| Checked fragment versus full theory | Name represented constraints, solver service and resource charge | P3-03 / P3-08 |
| Found cases versus conservative bounds | Preserve containment, nonemptiness and completion evidence | P3-03 / P3-04 / P3-05 |
| Fixed-query convergence versus anticipation | State the sequence and feedback quantifiers of any learning claim | P3-06 |
| Finite correction versus asymptotic LI | Keep U04 separate and use exact source hypotheses | P3-03 / P3-06 |
| Historical advice and precision | Charge or explicitly supply quoted information and decoding interfaces | P3-07 / P3-08 |
| Defined counterpossible versus defended semantics | Identify exception/frame and test its justification | P3-04 / P3-05 |

These are stronger questions and comparison controls. They do not award
P3-N01 contribution support or execute the later tasks.
