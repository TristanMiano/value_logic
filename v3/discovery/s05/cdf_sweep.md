# Exact value bounds by a quantile sweep

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT. [Implementation](cdf_sweep.py), [development probe](cdf_sweep_probe.py),
[source-bound results](cdf_sweep_results.json).

## Construction and attribution

The interval-distribution representation is established probability-box
inference. Utkin and Destercke, *Computing Expectations with Continuous
P-Boxes: Univariate Case* (2009), §2.2, equations (5)–(6), express expectation
bounds as integrals of payoff extrema over quantile intervals
([primary paper](https://arxiv.org/pdf/0906.1260)). Here we specialize it to
the finite threshold source and implement an exact sliding-window sweep.
Neither the representation nor its lower-expectation formula is claimed as
a new probability theorem.

Let H have ordered support 0,...,m, with only the constraints
`L(j) <= Pr(H<=j) <= U(j)`. Append `L(m)=U(m)=1`. At probability level u,
the allowable quantile interval is

```text
a(u) = min{j : U(j) >= u},
b(u) = min{j : L(j) >= u}.
```

Both endpoints are nondecreasing. Choose the leftmost minimizer of g on
`[a(u),b(u)]`. These choices are nondecreasing: a later strictly smaller
choice would have been feasible earlier and no worse, contradicting the
earlier leftmost minimum. They therefore define an admissible quantile
function and an attaining probability distribution. Every admissible
quantile has pointwise payoff at least this range minimum. Integrating
establishes both the bound and attainment. Ties and CDF jumps affect only
zero-measure boundary levels, which the implementation handles explicitly.

## Linear arithmetic and a separate simple checker

Merge the sorted lower/upper CDF values with 0 and 1. There are at most
`2m+1` positive-width probability intervals. Sweep them in increasing order,
moving the two support endpoints forward. A monotone deque retains the
leftmost payoff minimum in the current support interval. Each support point
enters once and leaves at most once. Preparation, one expectation bound and
the emitted mass/selection trace use O(m) arithmetic operations and storage.
Rational bit lengths still matter; this is not a constant-bit complexity claim.

The implementation also emits an exact attaining distribution. Its deliberately
simple independent range checker scans the selected ranges directly, verifies
their minima, reconstructs the mass distribution and checks every CDF bound.
That checker can take O(m²); its cost is reported separately. No floating
LP residual or rounded dual is needed for the sweep's value.

This source supports arbitrary finite payoff vectors, including nonmonotone
unions, action contrasts and compiled complete policies whose payoffs really
are functions of H. Additional moment, dependence or source-family constraints
need a richer optimizer; this sweep does not make them disappear.

## Development evidence

The probe reuses the paid nested-CNF source. All **126 expectation endpoints**
agree exactly with both the preserved results and a newly executed SciPy LP
plus rational-certificate adapter. Another **84 endpoints** cover full
uncertainty, exact distributions, ties, one-point support and nonmonotone
rational payoffs. No new truth calls occur.

For the 126 paid-source endpoints in this run:

| Work | Observed time |
|---|---:|
| Reusable sweep preparation | 1.05 ms |
| Exact value sweeps | 10.94 ms |
| Separate direct range checks | 15.23 ms |
| Existing LP and rational-check adapter | 249.45 ms |

These are local implementation observations, not a comparison against an
optimized existing probability-box package. Larger constructed sources of
128, 512 and 2,048 support points retain the stated linear operation counts;
their nonuniform runtimes are recorded without extrapolating a speed law.

The practical gain is an inexpensive exact query layer over the common paid
source. It does not pay the earlier calibration bill or improve its statistical
precision. Retaining individual censored rows may also carry information that
pointwise CDF envelopes omit; that is a separate promising representation.
