# Compare computation policies without resolving all mathematical inputs

Codex (GPT-6), October 11, 2026. DEVELOPMENT. New constructive S06 branch,
from S02's failed cheap-replay economics and S01's shared-source comparisons.
No novelty or material-positive confirmation claim; readiness unassessed.

## 1. A more concrete target

The first replay prototype reconstructs an alternate policy only until its
first unavailable bit. Its intervals are often wide, and replaying every
policy is expensive. A narrower but stronger operation is available for
**two fixed-order k-of-n evaluators**: compute the exact range of their cost
difference over *all* completions of the currently purchased truth bits,
without purchasing the remaining bits or enumerating 2^n completions.

Inputs are two permutations A,B of the same n bit computations; threshold
1<=k<=n; nonnegative known acquisition prices c_i; and a partial checked
assignment R. Each policy stops at k ones or n-k+1 zeros. Both policies are
sound on every completion, but their costs differ. Setup fees s_A,s_B and
constant per-probe control fees h_A,h_B may be included if they are known
independently of unresolved bit values. Permutation construction, matching,
receipt validation and producing this comparison have their own costs.

Let C_A(x),C_B(x) be these stipulated complete policy bills. The target is

    [min_(x consistent with R) (C_A(x)-C_B(x)),
     max_(x consistent with R) (C_A(x)-C_B(x))].

This is a conditional, same-request comparison. Using it for future requests
requires a new source or a transfer argument. It is not evidence that the
realized cheap policy's truth prediction is better, nor a free all-policy
feedback oracle. Ordinary combinatorial/robust optimization has the same
inputs and is allowed to use this algorithm.

## 2. Feasibility of a pair of stopping positions

Fix the common output e in {0,1}. The certificate needs K=k occurrences of e
if e=1, otherwise K=n-k+1. Suppose A stops at position i and B at position j,
with positions numbered from zero. Their final coordinates a=A[i], b=B[j]
must both equal e. If either contradicts R, this pair is impossible.

Set X=A[:i], Y=B[:j]. After imposing the final-coordinate values, each prefix
must contain exactly K-1 occurrences of e. This condition also prevents
earlier stopping on either output: K-1 winning bits do not certify e; once
the entire vector has K occurrences of e, the opposite outcome cannot obtain
its required certificate anywhere. More explicitly, the opposite threshold
is n-K+1, while at most n-K opposite bits exist in the full vector.

Let f_X,f_Y count fixed e bits in those prefixes, including either forced
final coordinate that occurs in the *other* policy's prefix. Among remaining
unknown coordinates write I=X intersect Y, P=X minus Y, Q=Y minus X and let
their sizes be u_I,u_P,u_Q. Required unknown e counts are

    r_X=K-1-f_X,   r_Y=K-1-f_Y.

Writing z for the number of e bits in I, a completion exists exactly when

    max(0, r_X-u_P, r_Y-u_Q) <= min(u_I, r_X, r_Y).

All quantities are integers. Necessity follows by counting e bits in the
three disjoint groups. For sufficiency choose an integer z in that interval,
put z e bits in I, r_X-z in P, r_Y-z in Q, keep the forced/fixed bits, and
set every other unknown bit arbitrarily. Both first stop positions follow.
This gives a reconstructable endpoint witness, not merely an LP relaxation.

## 3. Quadratic construction

Precompute each order's cumulative query price, fixed-zero/fixed-one counts,
unknown counts and inverse permutation. Also precompute the n-by-n table

    U[i,j] = number of R-unknown coordinates in A[:i] intersect B[:j].

It is a two-dimensional prefix-sum table over the permutation matrix, with
ones only at coordinates unknown in R. This takes O(n^2) unit arithmetic and
O(n^2) memory in the simple implementation. For each (e,i,j), neither forced
final coordinate belongs to the intersection: a is not in X, b is not in Y.
Only the opposite-prefix fixed and unknown counts need a constant-time
correction. The displayed feasibility test then costs O(1).

For every feasible pair the cost difference is already known:

    s_A-s_B + price_A[i+1]-price_B[j+1]
      + h_A*(i+1)-h_B*(j+1).

Take its minimum and maximum over the at most 2n^2 pairs, retaining their
witnesses. Every completion has one common output and one pair of first
stops, so none is omitted. Every admitted pair has a completion by section 2,
so neither endpoint is spurious. This proves exactness under the input
contract. Arbitrary integers require bit-complexity accounting in addition
to the unit-arithmetic bound; no constant-cost huge-integer claim is made.

### Retrospective bills and remaining bills are different requests

The displayed C_A,C_B are costs of the original stand-alone procedures on the
same request. R is evidence acquired since that original start, used to bound
their counterfactual bills. It is **not** permission to bill again for receipts
already available to a newly deployed procedure. The raw prototype uses the
retrospective contract. Its conditioned examples must not be presented as
live cache savings.

For a live comparison after R is common information, first compute
k'=k-number_of_known_ones and n'=n-|R|. If k'<=0 or k'>n', the threshold is
already resolved and both procedures should stop through the common checker.
Otherwise delete known coordinates from both permutations, keep their
unpaid prices and apply the algorithm with n',k' and no additional fixed
assignment. Original acquisition expense is common sunk cost, retained in the
history. Model/setup fees still needed at this point stay in the new bill;
already incurred fees are not charged again. This O(n) reduction prevents an
artificial advantage from repeatedly charging exact evaluation of known bits.

## 4. Why coupling can matter operationally

Subtracting independent cost intervals can claim A might be much more
expensive than B even when their cost difference is identical on all
completions. Identical orders are the simplest null check, but related orders
can also have much tighter coupled differences. A certificate that the upper
difference is nonpositive may eliminate a competing recipe without resolving
the mathematical bits that affect both recipes identically.

The plausible material consequence is *cheaper feedback or comparison for
fallible computation models*, with exact same-source scope and an O(n^2)
construction instead of exponential completion enumeration. This is not a
demonstrated complete-cost saving: direct policy execution might be cheap,
and O(n^2) comparison can cost more than n acquisitions. The useful regime
requires expensive unresolved computations or repeated comparisons that
amortize legitimate preparation. Compare direct analytical threshold methods,
specialized pair-policy optimization, ordinary brute enumeration at small n,
and the identical conventional kernel. A general model library need not
produce static orders, so this does not subsume SBB or adaptive search.

## 5. Next strengthening moves

Cheap finite reconstruction against all consistent completions should precede
larger applications. Then construct nonidentical-policy witnesses where a
coupled comparison is informative while most truth bits remain unresolved.
Measure the complete comparison bill against direct extra evaluation and
against simple swap/exchange arguments, which may be cheaper still.

Outcome-dependent acquisition costs are a useful possible extension. For
each pair of stop positions, shared queried coordinates cancel from the cost
difference; only exclusive-prefix groups remain. Sorting their outcome-cost
deltas and optimizing the feasible intersection count may yield a polynomial
extension. This has not yet been derived or implemented, and the present
theorem assumes known outcome-independent prices.

## 6. First developmental evidence and its limits

Command: `python v3/discovery/s01/compare_probe.py v3/discovery/s01/compare01.json`.
[Output](compare01.json) binds the source SHA-256 and seed. Across 320 varied
fixtures with n=1..8, the construction exactly matched enumeration of all
5,286 compatible truth completions. Endpoint assignments were reconstructed
and evaluated. In 171 fixtures the coupled range was strictly narrower than
subtracting independent ranges. Eighteen saved nonidentical-order fixtures
had upper difference <=0 while the independent upper bound was positive;
many depend on known bits or different setup/control prices. These were
discovered in the development sweep and are not fresh confirmation cases.

Larger n=32,64,128 last-swap examples retained no truth labels and returned
[-200,100], with checked endpoint completions. At n=128 the observed call
took about 8.5 ms in this one process; this is descriptive, not a benchmark
claim. A direct adjacent-exchange argument obtains the same range much more
cheaply, so these large fixtures validate execution scale only. They do not
establish a material speed advantage over the strongest ordinary control.

The surviving constructive lead is the explicit exact pair-stop feasibility
algorithm and a route to cheap cost feedback under unresolved truth. The next
work is to find a meaningful structured application, compare simpler analytic
optimizers, and charge all preparation/checking. No P3-11 promotion is warranted.

## 7. Outcome-dependent evaluator costs: a further derivation

Suppose evaluating coordinate t has known cost c_t(0) or c_t(1), depending
only on its exact bit. Fix a feasible (e,i,j) pair as above. Costs of every
coordinate in both queried prefixes (including their final coordinates)
cancel. Fixed coordinates contribute a known constant. For each remaining
unknown coordinate let d_t be its coefficient in cost(A)-cost(B): +1 if
queried only by A, -1 if only by B, zero otherwise. Express its contribution
relative to setting it to 1-e as

    d_t*c_t(1-e) + 1[x_t=e]*d_t*(c_t(e)-c_t(1-e)).

Within each of I,P,Q, section 2 fixes the number of e bits once z is chosen.
To minimize the difference, choose that many smallest cost-delta coefficients;
to maximize it, choose the largest. Coordinates in neither prefix have zero
cost coefficient, except the forced final coordinates already fixed. Sort
each group's coefficients, form prefix sums and optimize over the feasible
integer z interval. This is an exact finite optimization for that stop pair.

Enumerating all pairs and sorting afresh gives a polynomial (roughly
O(n^3 log n)) constructive bound, not the original quadratic one. Incremental
ordered-count data structures might reduce it. The argument extends only to
known outcome-local bills; arbitrary execution time depending on multiple
hidden bits is outside it. A finite check and a direct independent derivation
of the bookkeeping are still needed before relying on this extension.

### Developmental implementation of the extension

[outcome_probe.py](outcome_probe.py) implements the grouped-coefficient
construction and the live receipt-removal reduction. The [first run](outcome01.json)
matched 420 retrospective/live comparisons against all 5,546 compatible
completions of 210 varied fixtures with n=1..7. Prices were positive integer
outcome-local tariffs. It saves explicit cases in which retrospective and
remaining ranges differ, preventing those services from being silently
interchanged. Exact endpoint assignments were reconstructed and checked.

This supplies finite support for the extension and implementation, not an
independent adversarial reconstruction, solver-runtime experiment or novelty
assessment. The direct proof above and the code are by the same principal.
The prototype eagerly constructs each improving endpoint witness; its worst-
case implementation cost may exceed the stated O(n^3 log n) constructive
bound. Attaining that bound requires retaining endpoint descriptors and
constructing only the final two witnesses. This is a concrete next optimization,
not an assumption that the current code already has the sharper bound.
Next seek specialized conventional cost-comparison algorithms and real bounded
mathematical evaluators with justified tariffs; reduce comparison overhead
before considering confirmation.
