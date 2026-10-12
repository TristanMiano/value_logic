# S11M: informative probes require a controlled moment hierarchy

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT; continuation of
[the baseline construction](linear_values.md), across Q2/Q3/Q4/Q5.
Ordinary value-directed belief compression is the direct antecedent. The
following finite Boolean specialization makes its retained information and
failure modes explicit; neither novelty nor a material-positive gate is claimed.

## One useful correlation, not a free independence assumption

Let two latent signs have zero means and correlation rho=E[x1*x2]. Terminal
costs are 0 and x1+x2. A paid observation reveals x1 without changing it. Then

    E[x1+x2 | x1=o] = o*(1+rho),  o in {−1,+1}.

Both observations have probability 1/2. The optimal expected terminal cost
after the probe is −(1+rho)/2. At price c, buy it iff rho>2c−1. The perfectly
correlated and anticorrelated priors have identical marginals but probe values
−1 and 0 before price. For c=1/4 they demand different purchase decisions.
Learning or bounding the pair moment resolves the difference; pretending
independence is not an admissible substitute for that evidence.

More generally, after observing xj=o,

    Pr(o)=(1+o*mu_j)/2,
    E[xi | o]=(mu_i+o*mu_ij)/(1+o*mu_j), i!=j.

The denominator may vanish; that branch is impossible and must be skipped,
not repaired by an arbitrary conditional belief. These identities are algebra
of the known observation, not a calibration claim for an estimated model.

## Exact features for a limited observation depth

For each subset A define mu_A=E[product_(i in A) xi], with mu_empty=1.
Write K_jo f(x)=1[xj=o]*f(x). A monomial transforms as

    K_jo chi_A = (chi_A + o*chi_(A symmetric_difference {j}))/2.

Thus, for linear terminal cost vectors and known constant observation prices,
retaining all moments of degree at most H+1 suffices for exact finite-horizon
planning with at most H individual-bit observations. At each observed branch
use the formula above for every remaining needed moment, dropping one degree
of the representation. Coordinate flips multiply a moment by −1 when its
coordinate is in A; they do not increase degree. A finite additional flip
budget with known prices can therefore be included without increasing this
degree bound, though it enlarges the action/planning search.

Proof by backward induction: terminal action values are linear combinations
of degree-one moments. Pulling any continuation cost through one possible
observation multiplies its monomials by the degree-one indicator, increasing
degree by at most one. Each branch may choose a different continuation policy,
but summing their pulled-back cost vectors stays in the same degree bound.
Adding the constant observation price also stays there. Equivalently, use the
degree-indexed conditional-moment updates; at remaining depth h, degree h+1
provides degree h at the successor. The exact minimum over allowed choices is
then the same as explicit-belief planning.

The retained dimension is at most sum_(k=0)^min(m,H+1) binom(m,k), polynomial
in m for fixed H but potentially the full 2^m at larger depth. This is a
sufficient family, not the minimal dimension for every task: terminal sparsity,
limited diagnostic menus or known conditional structure can remove moments.
Feature acquisition and its reliability remain paid. Planning can still branch
exponentially in H, even when storage is smaller than a full probability table.

## Why depth H can really need order H+1

Take m=H+1 and the two uniform distributions p+ and p− on sign assignments with
product_i xi=+1 or −1. Every proper-subset moment is zero in both distributions;
only the full parity moment differs. Allow observations only of the first H
bits. Terminal actions guess the last bit, with 0/1 error loss, a linear
terminal cost for either guess.

If the true prior is known, observing all H permitted bits identifies the last
bit, with opposite guessing rules under the two priors. The entire observed
sequence of the first H bits nevertheless has the same uniform distribution
in both cases. A controller retaining only moments of order <=H starts with
the same representation; if it subsequently receives only those observations,
it cannot distinguish the priors. Couple the first H signs and its private
randomness across the two cases. It outputs the same guess while the correct
last signs are opposite, so its two error probabilities sum to one. At least
one prior therefore has error >=1/2, versus zero for an informed controller.

This remains an obstruction for adaptive ordering or early stopping: the full
unobserved first-H vector can be coupled before the policy selects which bits
to inspect. With positive per-observation price c and H*c<1/2, the informed
optimum is H*c (a proper subset conveys no information about the last bit).
Any controller with the same compressed prior in both cases has worst total
cost at least 1/2, hence regret at least 1/2−H*c. The claim concerns this exact
menu and uniform-parity pair, not every possible approximate value source.

This complements the exponential-baseline example: discard nuisance common
values, but retain the correlations that future observations can turn into
different useful actions. No single current marginal vector answers both duties.

## Next constructive check

Implement exact rational depth-indexed moment updates and compare their plans
with explicit belief recursion on small correlated priors. Include impossible
branches, the pair-correlation purchase boundary and both parity priors.
After that, develop paid acquisition or robust moment intervals; do not give
the model exact higher moments without recording that source cost.

## First executed screen and implementation limit

[moment01.json](moment01.json) matches depth-indexed moments to explicit-belief
values and first choices on 60 saved correlated-prior systems, the two
correlation examples, eight parity-prior cases, and a point mass that skips
16 impossible branches. The source is [moment_values.py](../moment_values.py).
These are supplied-table developmental checks; computing features from that
full table is recorded as acquisition, not claimed efficient external learning.

Code inspection found a scaling defect in the first feature enumerator: it
scans all 2^m masks before selecting the required degrees. That implementation
does not realize the polynomial-size construction at fixed H. Preserve the
source-bound first run and replace mask generation in a new version using
combinations of coordinate indices. No failed large run is invented; the
defect was identified before attempting one.

## Sparse policy contrasts can bypass a generic hierarchy

The full degree hierarchy supports arbitrary planning in the stated menu.
After a fallible model proposes a specific policy, its value can require far
fewer moments. Compile a finite policy DAG into a multilinear Walsh polynomial
of its original hidden signs. Terminal costs are linear. At an observation
node j with price c and child polynomials f+ and f−, the cost polynomial is

    c + (f+ + f−)/2 + xj*(f+ − f−)/2.

At a flip node j it is c plus the child's polynomial with every monomial
containing j negated. Multiplication by xj toggles j in a monomial's mask.
Combine identical masks and discard zero coefficients after each operation.
Memoizing DAG nodes can avoid expanding repeated continuation subtrees;
polynomial support itself can still grow exponentially. These are ordinary
decision-diagram/symbolic-evaluation operations, not free semantic validation.

Compile two proposed policies and subtract before acquiring their moments.
All common costs cancel. For a difference d_0+sum_A d_A*mu_A and a warranted
common box [l_A,u_A], its maximum is d_0+sum_A d_A*(u_A if d_A>=0 else l_A).
This is exact for the box and conservative for the realizable joint-moment
set inside it. Do not convert an arbitrary box endpoint into a probability
distribution or a calibrated conditional belief. A fixed common confidence
event permits adaptive choice among covered contrasts without another risk
charge; learning new uncovered moments requires its own evidence/risk account.

For the parity example, a controller with two accumulator states per level
observes H bits and guesses parity-sign times their product. Its cost compiles
to H*c+1/2−(sign/2)*chi_all. Comparing the two sign policies needs only the
full parity moment, despite its degree H+1. Comparing with a fixed immediate
guess also needs the last-bit marginal. Thus necessary high degree does not
imply a need to acquire every lower-degree moment. A model may suggest the
right sparse contrast; the value source must still warrant the moments used.

This supplies a new constructive next step: proposed-policy compilation and
targeted value acquisition, with explicit comparison scope. A two-policy
certificate alone does not certify optimality among all diagnostic policies.
Its strongest ordinary controls are symbolic policy evaluation and direct
estimation of the same policy-cost contrast under equal access and costs.

## Sparse compiler outcome and versioned enumerator disposition

[policy01.json](policy01.json) checks 100 generated observation/flip DAGs on
2,370 explicit Boolean worlds, matching execution to the compiled polynomial.
For a 64-observation parity controller over 65 hidden bits, 130 DAG nodes
compile to two terms. Both sign policies compiled in 4.7020 ms on this run.
Given the specified two moment intervals, the selected policy has zero regret
against the four named policies. Acquisition, semantic validation and global
optimality are not supplied by that fixture.

The feature-enumerator repair preserves version 1 and replaces exhaustive mask
filtering with coordinate combinations in [moment_v2.py](moment_v2.py).
Its first replay raised an unexpected Fraction-construction TypeError; the
single unchanged retry ended with Windows access violation and no result.
[First failure](moment02_failure.json), [retry failure](moment02_retry_failure.json).
The failing replay case and completed prefix were not durably journaled and
remain unknown. No additional unchanged retry is authorized by this record.

A prospectively recorded [environment change](moment03_plan.json) used the
already installed Python 3.12.14 instead of 3.13.14, keeping source and exposed
inputs fixed. [moment03.json](moment03.json) completed: 65 small enumerator
equivalence checks and all 71 old cases replayed. Degree-two features for
m=64,128,256 numbered 2,081, 8,257 and 32,897 and took 0.5510, 1.9942 and
8.0700 ms to enumerate. This is changed-environment development, not independent
confirmation or a diagnosis of the earlier errors. Their root causes remain
unknown. The new feature generation meets the intended subset-count structure;
the planner still pays its branching and source-acquisition costs.
