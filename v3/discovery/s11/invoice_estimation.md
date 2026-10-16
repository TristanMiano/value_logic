# Paid estimation of a task value from invoices

Codex (GPT-6), DEVELOPMENT. This extends the population identification result
in [invoice information](invoice_information.md) with a concrete sampling bill.
It is a restricted acquisition design, not a new general optimal-design theorem.

## A usable measurement and a finite bill

For a nonempty coordinate set S of size at most H-1, query S and then buy an
unqueried marker j precisely when chi_S=+1. The invoice decodes the single
sample Y_S=chi_S(X) in {-1,+1}. Its worst-case fee is
c_S=sum_(i in S) q_i + q_j; its expected fee is the base plus
q_j*(1+E chi_S)/2. Use the worst-case c_S below, and choose the cheapest allowed
marker. Fresh worlds are independent draws from ONE fixed law. No conditional
sampling oracle or law estimate is assumed.

Suppose the desired value contrast g equals a_0+sum_S a_S*chi_S on a checked
support F. Fix the representation and sample counts before these measurements.
Purchase N_S independent fresh-world observations for each nonzero coefficient,
and estimate Eg by a_0+sum_S a_S*mean(Y_S). For arbitrary dependence AMONG
coordinates within one world, independence across the separate draws yields

```math
\Pr\{|\widehat g-\mathbb E g|\ge t\}
\le 2\exp\left(-\frac{t^2}{2\sum_S a_S^2/N_S}\right).
```

This follows by applying Hoeffding to the independent bounded summands
a_S*Y_(S,k)/N_S, each of range 2*|a_S|/N_S. With
v=t^2/(2 log(2/alpha)), it suffices that sum_S a_S^2/N_S<=v.
For positive real sample sizes the least worst-case fee satisfying that
surrogate precision constraint is exactly

```math
\frac{A^2}{v},\qquad A=\sum_S|a_S|\sqrt{c_S},\qquad
N_S^*=\frac{A|a_S|}{v\sqrt{c_S}}.
```

Cauchy--Schwarz gives the lower bound
(sum c_S*N_S)*(sum a_S^2/N_S)>=A^2, with equality at the displayed allocation.
Ceiling every N_S^* preserves the precision guarantee and adds less than
sum_S c_S to its worst-case bill. If all coefficients vanish, the value is
already known and no samples are required. This optimality concerns the
continuous allocation for THIS Hoeffding surrogate and THIS single-character,
independent-sample experiment menu. It is not minimax optimality over all
invoice policies, joint observations, biased estimators or adaptive designs.

## Checked code relations supply an explicit representation choice

On an affine binary source x0+C, restricted characters belong to dual-code
cosets, with known offset signs. Collect all coefficients in each coset first;
call the resulting coefficient a_bar_K. Distinct nonconstant coset characters
are linearly independent on F, so every exact representation of g has the same
a_bar_K. Let c_K be the least fee among available degree-at-most-H-1
representatives and their allowed markers. Then

```math
\min A=\sum_{K\ne C^\perp}|\overline a_K|\sqrt{c_K}.
```

Proof: for every coset, triangle inequality bounds the sum of signed
coefficient magnitudes below by |a_bar_K|, and each fee weight is at least
sqrt(c_K). Put the whole coefficient on one cheapest representative to attain
that lower bound. The constant coset is known from the source and costs zero.
An unavailable nonzero coset makes exact estimation through this menu
impossible. Finding c_K can itself require costly weighted decoding; a fallible
adviser can propose a representative whose equivalence is checked, but search,
proof, checking and retention are additional costs.

Example: a checked interface has x3=x1 xor x2 and an available fourth marker.
With q1=q2=10 and q3=q4=1, estimating chi_{1,2} by querying 1,2 then marker 4
costs 20+p per draw, where p=Pr(chi_{1,2}=+1). Querying 3 then the same marker
costs 1+p and produces the IDENTICAL Bernoulli signal. Thus it saves exactly
19 fee units per observation, and reduces the required maximum query depth
from three to two. A setup bill K is repaid only when 19*N>K. The costs and
checked relation are explicit constructed premises, not measured application
performance. An ordinary method with this same interface can do the same.

## Fallible support: choose a value error budget, not a fictitious proof

If only P(F^c)<=epsilon is warranted, let g_tilde be the chosen measured
representation and suppose g_tilde=g on F. An independently checked bound
R>=max_(x outside F)|g(x)-g_tilde(x)| gives
|Eg-Eg_tilde|<=epsilon*R. The statistical bound above then yields an interval
of radius t+epsilon*R for Eg. Choose the sign of the action contrast only when
that interval excludes zero; otherwise retain uncertainty or buy a different
representation. If epsilon is itself a confidence bound, include its failure
probability. Adaptive selection from noisy estimates requires simultaneous
bounds or fresh independent data; the fixed-design theorem is not silently
reused after selection.

For example, on an even-parity five-bit support,
chi_{1,2,3}=chi_{4,5}. The cheap two-bit representative differs by magnitude
two on every outside world, so its bias bound is 2*epsilon. The direct
three-bit representation has no support-model bias but requires an extra
query before the marker. The useful tradeoff is therefore observation cost
versus a task-specific error budget. Arbitrary full-law interpolation error
need not enter this decision at all.

## Ordinary antecedents and remaining scope

Cost-weighted allocation and concentration are standard. The original finite
rank/contrast reduction is already in P3-02. [Statistics Canada's research on
optimal allocation](https://www150.statcan.gc.ca/n1/pub/12-001-x/2024002/article/00003-eng.htm)
is a primary comparison for constrained allocation; its abstract describes
variance minimization and KKT conditions, not this invoice interface. No theorem
from it is imported without its hypotheses. The adaptation here combines
the predictable-fee measurement, checked code aliases and a separately charged
support-error allowance. It does not establish a unique Value Logic algorithm,
cheap acquisition in an actual domain, or statistical robustness to arbitrary
nonstationarity. No new empirical stream or probability-law acquisition was run.
