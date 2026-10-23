# Three query criteria for a protected summary

Codex (GPT-6), October23,2026. DEVELOPMENT; pass13 formal synthesis/generation.
This is a finite-interface characterization, not a general theorem about
reasoning or a claim that polynomial methods are new.

## Contract and paid representation

Let Q partition the finite cube {0,1}^n into q>=2 nonempty summary cells.
An episode privately queries distinct coordinates and reveals only its
stopping count, at most H. Extra ignored coordinates are available if
padding requires them. Conditional on every public history, the count law
must depend only on Q(x). Every episode has fresh independent private
randomness; no private source-dependent state survives reset. The public
controller may remember counts and choose subsequent declared tests.

All functions, coefficients, partition descriptions and test policies below
must be acquired and stored at their actual cost. The characterization does
not supply them cheaply. It allows no free decoder labels from unresolved
mathematics. It explains which acquired representations can be useful.

Let V_d be the vector space of real degree<=d cube polynomials constant on
each Q-cell. Let K_d be its intersection with the cone of nonnegative
linear combinations of partial-assignment indicators using at most d bits.
The latter is nonnegative literal degree, as in Kaniewski--Lee--de Wolf.
Finite rational constraint matrices permit rational witnesses whenever
the finite strict separations below are feasible.

## Any information and approximate identification

Define d_any as the least d for which V_d contains a nonconstant function.
Define d_sep as the least d for which V_d separates every distinct pair
of Q-cells (different functions may separate different pairs).

The minimum cap for any one-episode information is d_any+1. The minimum
cap permitting arbitrarily accurate full-summary identification with
finitely many fresh episodes is d_sep+1.

Necessity: each count event below H is a depth<=H-1 decision-tree function.
The event of reaching H is already decided after H-1 queries, because it
means no earlier stop occurred. Averaging tapes preserves degree. Thus all
count probabilities belong to V_(H-1). If two cells agree on this space,
induction over public histories shows that their entire transcript laws
agree; no decoder can have error below1/2 on both.

Sufficiency: for any acquired separating F, sample a Fourier monomial with
probability proportional to its absolute coefficient and output its signed
parity. Its mean is F divided by the Fourier absolute sum. This is a bounded
binary channel depending only on Q(x). Padding to d or d+1 reveals it.
Finitely many separating functions give distinct finite probability vectors
for all cells. Independent repetitions estimate those vectors closely
enough to identify the cell at any prescribed positive error bound. Sampling
and concentration are ordinary methods; the thresholds concern this count
interface and retained equivalence relation.

## Zero-error identification with random termination

Define d_zero as the least d such that for every ordered pair of distinct
cells (a,b), some p in K_d satisfies p(a)=0 and p(b)>0. The minimum cap for
zero-error identification that terminates almost surely with finite expected
episodes is d_zero+1, under this finite fresh-reset contract.

For sufficiency, write each selected p as a finite nonnegative sum of
partial-assignment indicators. Divide by the total coefficient, randomly
choose an indicator, query it, and use counts d/d+1 to report its truth.
This preserves zeros and positive separations. Repeatedly cycle through
the finitely many tests, removing candidate a whenever its associated
zero-at-a test accepts. The true candidate is never removed; every wrong
candidate has a strictly positive elimination probability in a fixed finite
cycle. Geometric tails imply almost-sure termination and finite expectation.

For necessity, suppose cells a,b have no such ordered separation. Every
allowed one-episode count event has a nonnegative literal representation
of degree<=H-1. An event with positive probability at b therefore also has
positive probability at a. The same is true for every finite public
transcript by induction over fresh episodes. Any finite transcript that
delivers b with positive probability would then deliver b incorrectly at a.
Hence a zero-error decoder cannot terminate almost surely at b. Independent
public randomness can be conditioned on and integrated without changing
this support argument. Correlated private state and final-only purity are
outside the contract.

The relations are d_any<=d_sep<=d_zero, with possible gaps. The first two
criteria use signed polynomial representations; the third needs positivity
and zeros. A Fourier degree bound alone cannot establish zero-error decoding.

## Instantiation and limits

For the seven-bit Hamming quantizer, all three thresholds equal5:
hamming_degree.md gives the lower bound and coordinate separators, while
symmetric_channel.md supplies the positive zero-separating tests. Thus cap6
is both necessary and sufficient for all three stated duties, with different
cost/error/termination guarantees. Per-tape transcript purity has a different
threshold in s14 and is not covered by this averaged-law characterization.

This connects a fallible complete model Q(x), a protected inference interface,
the form of evidence allowed to leave a bounded computation, and acquisition
cost. Ordinary polynomial/query methods express exactly the same mechanism.
Closest randomized-encoding and zero-error-query comparison remains open;
do not promote the characterization based solely on this derivation.
