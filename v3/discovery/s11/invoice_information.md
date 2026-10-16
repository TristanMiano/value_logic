# Probability information in bounded-query invoices

Codex (GPT-6), DEVELOPMENT. This is a distinct Q5/Q1 connection, applying
the prior [P3-02 rank criterion](../../derivations/02_probability_information.md)
to a concrete paid-query interface. It is not a new general identification
criterion or a claim that every reasoning cost has this form.

## Interface and the one-observation lag

Let X range over {0,1}^n. A policy may stop at will or query an unqueried
coordinate, with at most H distinct queries, 1<=H<=n. Each positive fee is
fixed and known before that query's answer; initially take fee q_i independent
of history. No terminal outcome-dependent reward or charge is included.
An external observer sees only the total invoice and the chosen policy,
not query answers. Policies are selected without private current-world
information. Private randomization is independent of X.

For a fixed deterministic query tree, the total cost is

```math
C_\pi(x)=\sum_{h\text{ internal}}q_{j(h)}\mathbf1\{x\text{ matches }h\}.
```

An internal history has at most H-1 observed bits. Its cylinder indicator is
a multilinear polynomial of degree at most H-1. Consequently C_pi belongs
to the space V_(H-1) of degree-at-most-H-1 functions on the Boolean cube.
The last queried answer cannot affect this invoice: it arrives after the
last permitted purchase. Pruning those last answer branches gives a decision
tree of depth at most H-1 for the invoice itself. Thus every event
1{C_pi in A}, and hence the WHOLE invoice distribution, has the same degree
bound. Mixtures over private coins preserve the span. Predictable
history-dependent fees also preserve the upper bound.

The bound is sharp with fixed positive fees. For any nonempty S with
|S|<=H-1, query all S, then query some j outside S iff the parity character
chi_S(x)=(-1)^(sum_(i in S) x_i) is +1. The invoice is

```math
C_S(x)=\sum_{i\in S}q_i+\frac{q_j}{2}(1+\chi_S(x)).
```

Its expected value determines E chi_S. A one-query fixed bill supplies the
constant function; normalization already gives its expectation. Therefore
the invoice-function span is EXACTLY V_(H-1), of dimension
sum_(k=0)^(H-1) binom(n,k). Invoice data over all permitted policies identify
exactly the source's moments of orders <=H-1, or their restrictions to a
declared support. This is an exact population statement; finite sampling,
query fees and policy preparation remain separate costs.

For an unrestricted source, even H=n leaves the top parity moment invisible.
The uniform distributions on even and odd parity worlds have identical
invoice distributions under EVERY permitted policy, although their full
parity probabilities differ by one. More generally a signed perturbation
along a character of degree >=H is invisible. Repricing predictable fees
cannot repair that missing observation channel.

The indistinguishability also persists across fresh independent requests
when each experiment is chosen using only previous public invoices and
independent coins. It need not persist if a service carries private answers
from the same world across nominally separate runs, changes prices using
the answer being purchased, or adds a terminal outcome-dependent charge.
Those are different information interfaces.

## Logical support can make the missing moments redundant

For ANY proper support F strictly smaller than the full cube, all cap-n
invoice expectations identify the entire law supported on F. The full-cube
kernel at degree n-1 is the one-dimensional span of its top parity character,
whose value is nonzero at every world. A perturbation supported on proper F
cannot be a nonzero multiple of that character. This uses exact known support;
an approximate exclusion does not justify exact identification. The number
of required measurements may still be exponential and conditioning can be poor.

For a known affine binary code F=x0+C, a sharper statement is available.
Two characters chi_S and chi_T restrict to the same character on C iff
their indicator vectors differ by an element of the dual code C_perp.
The offset x0 supplies a known sign. Different dual cosets give independent
orthogonal characters on C. Therefore the rank of degree-D restricted
measurements equals the number of cosets of C_perp having a representative
of Hamming weight <=D. The full invoice family identifies every law on F iff

```math
H-1\ge\rho(C^\perp),\qquad
\rho(C^\perp)=\max_v\min_{u\in C^\perp}|v-u|.
```

This formula concerns 1<=H<=n and a nontrivial support. A known singleton
needs no measurements at all. If C is the full cube, rho=n and no permitted
distinct-query cap suffices, in agreement with the preceding obstruction.
The formula is an elementary combination of character orthogonality and
the definition of covering radius, not a new coding-theory theorem.

Examples:

- A known even-parity source has dual {0,all-ones}. Complementary characters
  agree on that source, giving rho=floor(n/2). The least sufficient invoice
  cap is floor(n/2)+1, despite arbitrary probabilities on its 2^(n-1) worlds.
- A repetition source {all-zero,all-one}, n>=2, needs cap two; a one-query
  invoice is constant, while a conditional second purchase encodes the bit.
- If the interface offers every nonzero parity of k latent bits as a distinct
  coordinate (n=2^k-1, k>=2), every nonconstant source character has a
  one-coordinate representative. Cap-two invoices suffice, but there are
  still 2^k-1 independent moments to learn. This trades query depth for a
  large logically redundant interface; it is not cheap full-law learning.

## Cost and conventional comparison

Different checked parity representations of the same source character yield
the same Bernoulli signal in C_S after subtracting known base fees and dividing
by the marker fee. Their statistical quality is identical in that ideal
interface. A cheaper representation can reduce acquisition cost; finding
minimum-weight representatives is itself a decoding/optimization problem.
Fallible advisers may propose representatives, but the relation must be
checked and proposal/search/checking costs charged. No solver for that
cost optimization has been implemented here.

An ordinary method with the same invoice-only interface has exactly the same
identification limits and constructions. A method allowed to observe the
answers has a stronger interface and may avoid the extra marker purchase.
Thus the positive delta is a precise link between logical source constraints,
query depth and value information, not a claim that billing is the best way
to learn probabilities or that ordinary probability methods cannot do this.

## Prior-art boundary and first screen

[Nisan and Szegedy (1994)](https://web.vu.lt/mif/s.jukna/boolean/Nisan-Szegedy.pdf)
section 1.3.2, Theorem 1.3, is a primary comparison for Boolean polynomial
degree and decision trees, including degree <= decision-tree depth. The general polynomial
and character machinery is established. P3-02 already establishes finite
rank/fiber identification. The proposed adapter here is the predictable-fee
lag and its explicit logical-support consequences.

Screen a few small query caps using fully evaluated random adaptive trees,
the explicit parity-purchase construction, and exact restricted-character
ranks for full-cube, parity, repetition and parity-interface sources. Include
an outcome-dependent terminal fee as a boundary counterexample. These are
finite mathematical checks, not data collection or an application benchmark.

ip01 passes all five declared cases on first attempts. It checks random
adaptive trees for n=2,3,4,6 and all permitted caps, explicit parity-purchase
functions, and exact ranks for full-cube, affine parity, repetition and
seven-coordinate latent-parity sources. The six-bit affine-parity source
has ranks 1,7,22,32,32,32 at caps 1 through 6, so cap four first identifies
all 32 world masses. The seven-coordinate/three-latent-bit interface has
rank eight already at cap two. These finite counts corroborate the proof;
they do not establish acquisition efficiency.

[Introduction to Linear Codes, lecture 7](https://tdalazard.io/infoTheory/S7.pdf),
PDF pages 20-23 (slides 19-22), gives the character-annihilator interpretation
of a dual code and quotient/coset definitions used above. This is primary
teaching material for established background, not evidence that this invoice
adapter is novel. No stronger novelty conclusion is drawn from its absence
in the few sources inspected.
