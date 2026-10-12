# S10/S11 bridge: partial computation can warrant a bounded policy value

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT. This combines the
[positive-production source](positive_bets.md), [delayed refinement](delayed_proofs.md)
and [sparse policy costs](value_moments.md). The confidence mechanism is an
adaptation of conventional bounded-value betting, not a new general statistical
principle. Material usefulness and comparison remain open.

## Fixed policy source and graded receipts

Fix a finite population of N contexts and two policy versions before starting
a fresh sampling lottery. Their true cost difference g_i=cost(reference,i)−
cost(candidate,i) is deterministic and lies in known rational bounds [a,b],
a<b. Put y_i=(g_i−a)/(b−a) in [0,1]. The null that average gain is at most
gamma has total threshold T=N*(gamma−a)/(b−a); handle gamma outside [a,b]
directly from the deterministic range. Later statements keep 0<=T<=N.

A checked partial computation yields l_i<=y_i<=u_i. Missing bits, failed
calls or unsupported predictions cannot tighten that interval. Select each
sampled identity uniformly from the remaining population using fresh randomness
before its computation is exposed. The compute budget may then adapt to its
observed progress. The proof below allows a lower receipt z_j=l_i between 0
and 1, not just a binary proof-produced indicator.

After j sampled identities, let k_j be the sum of their currently recorded
lower receipts. If k_j>T, the null is already inconsistent with hard lower
bounds. Otherwise define, before the next uniform draw,

    mu_j(T)=min(1,(T−k_j)/(N−j)).

Under the null, the actual remaining mean is at most this quantity: subtract
the true sampled sum from the total, and use true sampled sum >=k_j. Since
z_(j+1)<=y_(j+1), its conditional expected value is also at most mu_j(T), even
if computational censoring depends on the actual result. For any predictable
eta_j>=0, the factor

    (1+eta_j*z_(j+1))/(1+eta_j*mu_j(T))

has conditional expectation at most one. Its nonnegative product is therefore
a supermartingale under the null. Rejecting when it reaches 1/alpha gives
an anytime error bound alpha by the ordinary nonnegative-supermartingale
maximal inequality. A fixed mixture of such products is also valid. Prediction
of computational yield can advise eta or effort; it is not a truth probability.
No independence of the contexts' mathematical truths is assumed.

## Delayed interval refinement

Freeze the historical bet choices as actually made. A later checked improvement
of an old lower receipt changes its existing factor and all later lower-prefix
sums, without adding a draw. Compare with an oracle product using the full true
y values on the same sampled identities and those historical predictable bets.
Every partial numerator is no larger; every partial denominator is no smaller,
because its lower-prefix sum is no greater. Thus every refined partial product
is pointwise bounded by the corresponding full-truth product.

The full-truth product is a null supermartingale. Consequently arbitrary sound
delayed refinements retain the same anytime rejection guarantee by domination.
The partially revised process itself need not be a supermartingale in revision
time. Increasing a lower receipt weakly increases its product: its numerator
rises and later denominators weakly fall. Do not retroactively retune historical
bets using newly revealed values. Unsampled bounds may support a separate hard
sum warrant but create no lottery factor until their identities are sampled.

This is a fixed-source guarantee. A policy learned or changed using exposed
samples is a different source. Either use an already warranted common feature
event covering its contrast, or register a new source and fresh lottery with
an explicit new risk allocation. Fresh sampling may reuse previously checked
bit receipts when selected, with lookup/checking costs charged. It does not
erase the older sampling exposure or give unlimited repeated tests one alpha.

## Cheap checked intervals from a compiled cost contrast

For a sparse Walsh polynomial g(x), substitute all checked bit values, combine
equal remaining monomials, and write g=c+sum_(A nonempty) d_A*chi_A. The interval

    [c−sum_A |d_A|, c+sum_A |d_A|]

is sound for every remaining assignment. Substituting one more bit can only
tighten it: the substitution groups old terms, and the triangle inequality
bounds each new coefficient and changed constant by their old absolute sums.
Intersect with other warranted bounds. The range is generally conservative
because monomials can be dependent. Exact SAT/optimization bounds remain an
optional, paid stronger source.

This lets useful lower receipts arrive before full evaluation. For a parity
contrast, however, every unknown bit keeps the full range: all participating
bits must be computed before any improvement. For an additive contrast,
each resolved bit removes its coefficient's contribution to width. A fallible
acquisition model must distinguish such complementarities; single-bit myopic
width reduction can overlook a useful parity bundle. Compilation and source
binding are paid parts of the service, as are failed computations.

## Next development and fair comparison

Implement exact rational graded factors and partial-polynomial bounds; check
small finite populations and sound refinement masks cheaply. Then compare
direct complete policy evaluation, ordinary partial evaluation, and cached
contrast evaluation under the same access, sampling rule and full cost bill.
The identical kernels are valid conventional comparators. A supplied interval
or selected four-policy bank alone does not establish global policy optimality,
external calibration, solver soundness or a materially useful positive result.

Executed [interval01.json](interval01.json), using recorded Python 3.12.14:
exact small finite-population crossing probabilities satisfy the specified
alpha bounds; 2,187 partial/full domination checks, 4,374 delayed-refinement
checks and 12,422 partial-polynomial containment/monotonicity checks passed.
The parity-prefix example preserves its all-bits complementarity. These are
cheap same-model development checks, not external certification.

Next extension: a fixed finite policy bank with a prior weight per policy,
with-replacement context sampling, and a PAC-Bayes bound can permit a posterior
mixture chosen after seeing partial computations. This would replace repeated
source selection by an explicit information penalty. Derive that common event
before claiming adaptive policy selection can reuse a single confidence budget.
