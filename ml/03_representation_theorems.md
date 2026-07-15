# Representation Theorems for the Hybrid Value-Logic Architecture

Created: 2026-07-14
Task: TODO Task 17
Status: seven frozen targets adjudicated; training and calibration remain Task 18

## Executive result

The representation program succeeds, but only for the hybrid boundary fixed in
Tasks 15–16. A finite ReLU network can compute the required **continuous
piecewise-affine statistics, payloads, and grades** exactly. A deterministic
external layer must still check exact evidence, decode inclusive boundaries,
form direct `K_3` values, aggregate profiles, apply the active mask, and return
fallback on a gap.

The seven frozen targets have the following dispositions.

| target | result | status |
|---|---|---|
| exact factorization | exact kernel/quotient characterization for status and a finer diagnostic version | proved |
| robust approximation | conservative interval decoder is sound; exact recovery is guaranteed outside the explicit doubled error band | proved with the factor-of-two boundary made explicit |
| finite ReLU statistics | global finite CPWL statistic maps have exact finite ReLU realizations with affine outputs | proved from exact CPWL representation, with source conventions audited |
| hard seams | affine hard assembly is continuous iff traces agree on all relevant common faces; discontinuous seams cannot be one ordinary ReLU output | proved |
| expandable libraries | fixed indexed outputs are registry-bound; shared candidate scoring is permutation-equivariant but finite evaluation is not global closure | proved as an interface result plus an indistinguishability obstruction |
| dual-use activation | named normalized positive margins can be both grades and downstream features; the state-plus-surplus code is minimal for a coordinate-complete consumer family | proved conditionally; scalar, boundary, and scale obstructions proved |
| annotated finite plans | a fixed proof-erased plan with CPWL primitives and conforming branches has a joint CPWL payload/grade map and exact finite ReLU realization | proved; certificates remain external |

None of these results says that SGD will learn the representation, that a
calibration claim is valid, that hidden units align with scientific concepts, or
that ReLU is the unique or best architecture.

## 1. Conventions and system boundary

### 1.1 Input class and consumers

Fix a declared input class `Omega`. An element `omega in Omega` contains the
Task 15 atom address or finite plan address, its dependency-scoped record
projection, and the exact side packet needed by the relevant decoder. A finite
numerical view lies in `R^d`; exact identities and proof objects need not.

Fix a finite profile/query family `F`. Let

```text
w_F : Omega -> WFObs_F
```

be the required well-formedness observation. On the well-formed fiber, let
`v(omega) in V` be the complete finite atom valuation and let `~_F` identify
exactly those valuations that answer every requested public status query in
`F` identically.

The canonical public observation is

```text
N_F(omega) = Ill(w_F(omega))                 if WF fails,
             Well([v(omega)]_F)              otherwise.
```

`Ill/Well` is a **canonical decoded normal form**. A representation need not
literally store that sum type. It need only admit a deterministic decoder to
the same observation.

For an audit consumer family `A`, replace `N_F` by the finer observation
`N_A` containing every requested address-indexed diagnostic, safety role,
statistic/envelope, checker/certificate reference, and provenance item. In
general,

```text
ker(N_A) subseteq ker(N_F).
```

### 1.2 ReLU convention

Throughout,

```text
rho(t)=max(0,t).
```

A ReLU network has affine maps into each hidden layer, coordinatewise ReLU at
each hidden layer, and an affine final output. Under the convention of
`AroraEtAl2018`, `k` hidden layers give total depth `k+1`, and network size is
the sum of hidden-layer widths. Biases are permitted on hidden affine maps;
the final map is linear in that paper's displayed convention, with constants
carried by preceding affine coordinates when needed.

The word **CPWL** below means a globally continuous map that is affine on each
cell of a finite polyhedral decomposition. Some cited sources call the same
class continuous piecewise linear even though affine offsets are allowed.

### 1.3 What is not a neural output

Unless a later task explicitly changes the interface, the following remain
exact or external:

- `WF` and its diagnostic;
- evidence presence, currentness, conflict, scope, mode, checker, calibration,
  provenance, and registry identity;
- proof/certificate checking;
- inclusive support and strict refutation comparisons;
- direct `K_3` atom construction and profile meet;
- the exact active set, tie policy, selection restriction, and fallback; and
- complete audit traces.

The network may compute the real quantities consumed by this layer. It does
not thereby compute a proof or self-authorize its use.

## 2. Exact factorization

### Theorem 1 (status factorization and minimal quotient)

Let `c:Omega -> Z` be any representation and let `N_F` be the canonical public
observation above. The following are equivalent:

1. there is a deterministic decoder `d:Z -> im(N_F)` such that
   `d(c(omega))=N_F(omega)` for every `omega`;
2. `ker(c) subseteq ker(N_F)`;
3. whenever `c(omega)=c(omega')`, the inputs have the same required `WF`
   observation and, when well formed, their valuations lie in the same
   `V/~_F` class.

Moreover, `N_F` is the coarsest exact code up to relabeling: every exact code
`c` admits a unique map on `im(c)` to `im(N_F)`.

#### Proof

If a decoder exists and `c(omega)=c(omega')`, applying it gives
`N_F(omega)=N_F(omega')`; hence (1) implies (2). Expanding equality of the
disjoint invalid/well-formed observations gives (3).

Conversely, assume (2). Define

```text
d(z)=N_F(omega) for any omega with c(omega)=z.
```

The kernel inclusion makes this independent of the representative. Thus `d`
is well defined on `im(c)` and is an exact decoder. The same definition also
shows uniqueness. ∎

### Corollary 1 (diagnostic-preserving factorization)

Replacing `N_F` by any declared audit observation `N_A` yields the identical
characterization. A status-sufficient code is audit-sufficient iff

```text
ker(c) subseteq ker(N_A).
```

Consequently a status quotient may discard distinctions—such as missing
versus expired evidence—that a diagnostic client must retain even when the
public outcome is the same.

### Corollary 2 (no real-width conclusion from finite code counts)

If `im(N_F)` is finite, then a fixed-length discrete code with distinguishable
symbols needs at least

```text
ceil(log_2 |im(N_F)|)
```

bits. This is a statement about a finite discrete alphabet. It is **not** a
lower bound on the number of real neural outputs: without a precision,
robustness, noise, or decoder-regularity restriction, one real number can name
arbitrarily many finite states.

### Project role

The theorem is architecture-neutral. It says exactly what any ReLU, lattice,
maxout, graph, symbolic, or other scorer must preserve for the declared
consumer. It does not say that `N_F` is sufficient for an undeclared future
profile; changing `F` changes the quotient.

## 3. Robust realization by approximate statistics

### 3.1 Affine boundary propagation

Let the ideal continuous statistic vector be

```text
s(omega)=(s_1,...,s_k),
```

and suppose an accepted external envelope establishes

```text
|s_j-hat_s_j| <= delta_j.
```

For a decoder boundary

```text
b(s)=alpha_0 + sum_j alpha_j s_j,
```

define the propagated margin radius

```text
r_b = sum_j |alpha_j| delta_j.
```

Then `|b(s)-b(hat_s)|<=r_b`. More generally, if `b` is `L_b`-Lipschitz under a
declared norm and the statistic error is at most `delta`, use
`r_b=L_b delta`.

Consider an ideal relation `b(s)<=0`, with equality included on the supported
side. The conservative decoder uses the interval

```text
B_hat=[b(hat_s)-r_b,b(hat_s)+r_b]
```

and returns:

```text
supported  if upper(B_hat) <= 0 and the mode can support,
refuted    if lower(B_hat) >  0 and the mode can refute,
open       otherwise.
```

### Theorem 2 (sound conservative decoding and exact separated recovery)

Assume the accepted statistic bounds hold.

1. Every supported output satisfies the ideal relation `b(s)<=0`.
2. Every refuted output satisfies `b(s)>0`.
3. If `b(s)<=-2r_b`, the two-sided decoder returns supported.
4. If `b(s)>2r_b`, the two-sided decoder returns refuted.
5. In a two-sided mode, if the decoder is open, then
   `-2r_b < b(s) <= 2r_b`.

Thus the raw margin approximation error is `r_b`, while the guaranteed
conservative **decision band in ideal-margin space** has half-width `2r_b`.

#### Proof

The true value lies in `B_hat`, proving (1) and (2). If
`b(s)<=-2r_b`, then `b(hat_s)<=b(s)+r_b<=-r_b`, so the interval upper endpoint
is nonpositive. If `b(s)>2r_b`, then
`b(hat_s)>=b(s)-r_b>r_b`, so the lower endpoint is positive. The contrapositive
of these two implications gives (5). ∎

The factor two is necessary for a decoder that is both conservative everywhere
the envelope holds and complete away from the boundary. A raw sign decoder
recovers the ideal sign whenever `|b(s)|>r_b`, but it may issue an unsupported
grant inside its error interval; it is not the production decoder.

### 3.2 Scalar risk specialization

For ideal risk `J` and tolerance `epsilon`, take `b(J)=J-epsilon`. With
`|hat_J-J|<=delta`, the reference decoder is

```text
hat_J+delta <= epsilon  -> supported,
hat_J-delta >  epsilon  -> refuted,
otherwise               -> open.
```

It is always sound relative to the accepted bound. It is guaranteed to match
the ideal two-valued threshold result when

```text
J <= epsilon-2delta
```

or

```text
J > epsilon+2delta.
```

At or near the ideal boundary, opening is intentional. With `delta=0`, the
inclusive equality `J=epsilon` is supported exactly.

### 3.3 Multiple atoms, profiles, and modes

For finitely many relevant boundaries `b_a`, compute a separate propagated
radius `r_a`. An atom whose definition has several required inequalities is
supported only when every required conservative interval lies on its supported
side. A valid countercondition may refute it only when the certificate mode
permits that polarity. Otherwise the atom remains open.

Let `A(P)` be all required and safety atoms read by a finite profile `P`.
If:

1. exact `WF` and evidence gates are unchanged;
2. every `a in A(P)` lies outside its mode-relative decision band; and
3. every statistic bound is valid on the same scope,

then every atom's `K_3` value and mode-relative boundary outcome equal the
ideal result, and the external direct `K_3` meet, safety projection, four-way
public result, active set, and fallback decision are exact. Complete audit
diagnostics still retain the actual estimate and envelope rather than
pretending they are the ideal statistic. The public maps are deterministic
functions of the exact atom values and gates; no neural aggregate-status head
is needed.

If any required atom remains in its band, the profile result need not equal the
ideal two-valued result. The supported production behavior is to retain that
atom as open and let the exact profile semantics decide whether reliance is
withheld.

## 4. Exact finite ReLU realization of CPWL statistics

### 4.1 Primary-source audit and architecture count

`AroraEtAl2018`, Theorem 2.1, uses exactly the convention in §1.2 and proves
that a scalar map `R^d -> R` is representable by a finite ReLU network iff it
is CPWL. Its positive direction gives total depth at most

```text
ceil(log_2(d+1))+1,
```

that is, at most `ceil(log_2(d+1))` hidden layers. The proof uses the
`WangSun2005` representation

```text
f(x)=sum_{j=1}^p sign_j max_{i in S_j} ell_i(x),
|S_j|<=d+1,
```

and a balanced exact ReLU max construction. The theorem supplies finite
existence and the depth bound, not a tight general neuron bound.

`HeEtAl2020`, Theorem 5.2, independently details the construction and supplies
a rough size estimate. If a scalar CPWL function has `m` distinct affine
pieces and `M` unique-order regions, where `m<=M<=m!`, their bound has the
form

```text
O(d 2^(m M + (d+1)(m-d-1)))    if m>=d+1,
O(d 2^(m M))                    if m< d+1,
```

under their size convention. The estimate is deliberately loose and can be
enormous. This project therefore claims a finite exact construction and the
audited depth convention, not an efficient representation for arbitrary
CPWL inputs.

The elementary identities used by the construction include

```text
max(u,v)=ReLU(u-v)+v,
min(u,v)=-max(-u,-v).
```

### Theorem 3 (fixed-dimensional vector statistic realization)

Let

```text
S:R^d -> R^p
```

have finitely many coordinates, each a global finite CPWL function. Then a
finite ReLU network with affine output computes `S` exactly on all of `R^d`.
It can be chosen with at most `ceil(log_2(d+1))` hidden layers. Its size is at
most the sum of finite scalar-coordinate construction sizes after shallower
coordinates are padded or carried to the common output.

#### Proof

Apply the scalar exact-representation theorem to every coordinate. Put the
coordinate subnetworks in parallel, pad them to a common depth by exact signed
identity transport if necessary, and concatenate their affine outputs. The
result remains finite and computes every coordinate exactly. ∎

### Corollary 3 (hybrid atom realization)

On a fixed finite numerical view, if all learned atom centers, endpoints,
half-widths, signed margins, payload coordinates, and quantitative-grade
coordinates requested by a module are global CPWL, one finite ReLU network
can compute them exactly. A fixed external decoder then combines them with
exact `WF`, evidence gates, side-packet identities, and boundary conventions
to recover the selected finite profile queries.

This corollary does **not** say that the ReLU network directly outputs `K_3`.
The direct label-valued threshold map is generally discontinuous on any
connected neighborhood crossing a boundary, whereas an ordinary ReLU network
has continuous real outputs. The exact comparison—including equality on the
supported side—is external.

### 4.2 Domain and schema conventions

The theorem is global. If a statistic is specified only on a domain `D`, the
claim must provide a global CPWL extension `S_ext:R^d->R^p` and applies to
`S_ext|D`. Merely saying “piecewise affine on an arbitrary subset” does not
supply such an extension.

Finite categorical schemas may be represented by exact external dispatch or
by a fixed numerical encoding for which one global CPWL map is explicitly
defined. The theorem does not turn opaque checker IDs, variable-size evidence
records, or an unbounded registry into a fixed Euclidean vector.

## 5. Conforming hard seams

### 5.1 Setup

Let `X` be covered by the maximal cells of a finite conforming polyhedral
complex `P`. Each closed maximal cell `C` has an affine expert

```text
f_C(x)=A_C x+b_C.
```

The router uses `f_C` on the relative interior of `C`. Every point of a
relevant common face is assumed to be an accumulation point of the relative
interiors on both sides. A tie rule may choose either expert on the face.

### Theorem 4 (hard-seam characterization)

The hard assembly has a well-defined continuous extension `H:X->R^p` agreeing
with every cell expert iff

```text
f_C(x)=f_D(x)
```

for every pair of maximal cells and every point in their nonempty relevant
intersection. Under this condition `H` is CPWL and, when extended globally as
in §4.2, has an exact finite ReLU representation.

If two traces disagree at an accumulation point of a common face, no ordinary
continuous ReLU output can equal both hard expert limits there. An external
discrete router or hard mixture of experts can still represent the
discontinuity, but it is a different architecture and retains route, scope,
risk, and fallback obligations.

#### Proof

For sufficiency, the finite cells form a closed cover. Pairwise trace agreement
makes the affine definitions well defined on intersections. The finite gluing
lemma yields continuity, and the result is affine on each cell, hence CPWL.

For necessity, approach a common-face point through the relative interiors of
the two cells. Continuity forces both affine limits to equal the value at the
face point, so the traces agree. If they do not, the two sequences have
different limits; no choice of the face value repairs continuity. ∎

### Corollary 4 (rank-one codimension-one seam)

Suppose adjacent affine maps agree on the hyperplane

```text
H={x:n^T x=c},  n!=0.
```

Then for some `a in R^p`,

```text
A_C-A_D = a n^T,
b_C-b_D = -a c.
```

Thus the Jacobian change has rank at most one. Indeed, the linear difference
vanishes on every tangent vector in `n^perp`, so each row is proportional to
`n^T`; evaluating at one point of `H` gives the bias relation.

This is a seam statement about affine traces. The familiar one-switch ReLU
activation-facet formula is a special case. If several units switch, cells are
degenerate, or the router joins independently trained experts, the rank-one
conclusion need not hold.

### 5.2 Relation to the scientific cover

This theorem does not identify neural activation cells, router selection
cells, and scientific model domains. Several scientific models may be licensed
on one neural cell; many activation cells may refine one scientific domain;
and a router seam may lie inside a thick overlap. Approximate bridge agreement
can be useful without satisfying exact CPWL gluing. In that case the system
must either accept a new blended plan with its own error analysis or keep the
hard discontinuity external.

## 6. Fixed and expandable libraries

### Proposition 5 (fixed-index interface limitation)

A fixed model-indexed output

```text
T_K(x)=(t_e(x))_(e in K) in R^(|K| p)
```

is defined only for its declared finite registry `K`. A candidate
`e_star notin K` has no output coordinate. Producing one requires changing the
interface, replacing a coordinate by convention, or invoking an external
candidate-conditioned scorer. This is a type/interface fact, not a
finite-precision parameter lower bound.

### Proposition 6 (candidate-conditioned equivariance)

Let

```text
f_theta(x,phi(e),record_e) -> t_e
```

be shared across candidates. Applying it pointwise to any finite external
registry `K` and restoring exact identities gives a permutation-equivariant
family:

```text
S_theta(pi K,x)=pi S_theta(K,x).
```

A shared pair scorer has the analogous action on ordered pairs. A
permutation-invariant set reducer may summarize the family, while any selected
identity is returned through the exact registry.

This construction supports a variable number of **queries** with fixed
parameters. It does not guarantee calibrated or correct scores for a novel
candidate, injectively store unbounded independent evidence in one fixed
summary, or remember a candidate whose record is absent.

### Theorem 5 (finite-evaluation non-closure obstruction)

No procedure whose observation is restricted to an evaluated set `K` can, in
general, turn “`g` is undominated in `K`” into “`g` is globally undominated in
every extension of `K`.”

#### Proof

Take two worlds with identical candidates, evidence, and comparisons on `K`.
In the first there is no additional candidate. In the second, add an unseen
`e_star` with a valid comparison certifying that `e_star` dominates `g`. The
procedure receives the same observation in both worlds and therefore returns
the same answer, while global non-domination differs. ∎

The supported claim is always indexed by the exact evaluated set and search
trace. Sparse evaluation costs `Theta(|K|+|E_K|)` only for the pair questions
actually requested. Supporting non-domination for every member may still
require quadratic pair evidence unless a separately proved certificate
compresses the search.

## 7. Joint license/computation sufficiency

### 7.1 General obstruction

Let `F` be a declared license-query family and `C` an independently declared
downstream-computation family. Define

```text
omega ~_(F,C) omega'
```

iff all consumers in `F union C` agree. The architecture-neutral factorization
condition is `ker(c) subseteq ~_(F,C)`, but that definition alone is not counted
as the representation result.

### Theorem 6 (equal-code separator)

If there are `omega,omega'` with

```text
c(omega)=c(omega')
```

and some declared computation `C_j` satisfies

```text
C_j(omega)!=C_j(omega'),
```

then no deterministic downstream map of `c` can realize `C_j` exactly.

#### Proof

A function of `c` must take the same value on equal codes. ∎

In particular, two plans can have the same adequacy scalar and different
predictions, costs, grades, or traces. The scalar

`ReLU(m_support)` is therefore not a general computational payload. This is an
obstruction for that specified code, not a claim that one arbitrary
infinite-precision real can never encode several finite fields.

### 7.2 Positive named-channel construction

Fix `n` hypotheses. For every channel `i`, declare:

- an exact hypothesis/address and domain;
- a certificate-valid signed support margin `m_i`;
- a positive scale `sigma_i` with common normalization semantics;
- an exact mode-relative atom state `r_i`; and
- the downstream consumers allowed to read the channel.

On the certificate-valid domain define

```text
z_i(omega)=ReLU(m_i(omega)/sigma_i).
```

On the larger system domain, invalid/missing/conflicted evidence is withheld by
the exact state/mask; a favorable neural number cannot validate it. Define the
hybrid code

```text
R(omega)=(r_1,...,r_n,z_1,...,z_n).
```

Let `H_coord` contain the state projections `r_i`, the surplus projections
`z_i`, and any declared functions of the complete vector `R`, including a
later affine/ReLU layer.

### Theorem 7 (dual-use construction and coordinate-complete minimality)

`R` is jointly sufficient for `H_coord`. More strongly, for the subfamily
containing every state and surplus coordinate, `R` is the minimal quotient up
to a one-to-one relabeling: every sufficient code `c` admits a decoder

```text
h:im(c)->im(R)
```

with `R=h compose c`.

If every `m_i:R^d->R` is CPWL, the numerical surplus vector `z` is computed
exactly by one hypothesis-indexed ReLU layer (or by named units within a larger
exact ReLU construction). Exact states and evidence masks remain beside it.

#### Proof

Every consumer in `H_coord` is, by construction, a function of `R`, proving
sufficiency. If `c` is sufficient for all coordinate projections, equal
`c`-codes imply equality of every `r_i` and `z_i`, hence equality of `R`.
Theorem 1's representative construction gives `h`. The last statement follows
by applying ReLU to each CPWL margin. ∎

This is more than the bare definition-level condition: it identifies an
explicit finite channel family, proves its minimal quotient for a
coordinate-complete consumer class, and gives the exact ReLU realization of
its numerical half.

### 7.3 The classifier example

Let the channels be named

```text
flower, dog, cat, food, person, child, house, ...
```

and, for a common request context, use

```text
m_i=(epsilon_i-upper(U_i))/sigma_i,
z_i=ReLU(m_i).
```

Here `U_i` is an accepted certificate-valid risk region and the `sigma_i` make
the displayed values commensurate. Then a vector such as

```text
(0,0.2,0.2,0,5,3,0.1,...)
```

has two legitimate uses:

1. each positive coordinate is that hypothesis's normalized positive
   certificate-relative adequacy surplus; and
2. the complete vector is numerical content for a declared later layer, for
   example `logits=A z+b`.

If the later consumer is simply the identity followed by an external tie-aware
argmax, `person` has the greatest displayed surplus. This does not make `5` a
posterior probability, a global truth score, or proof that `person` is the
globally best available model. The exact state vector is still needed because
inclusive boundary support has `z_i=0`, the same rectified value as negative,
open, refuted, invalid, and missing cases.

### 7.4 Verified approximation version

If `|hat_m_i-m_i|<=eta_i`, then ReLU's one-Lipschitz property gives

```text
|ReLU(hat_m_i/sigma_i)-ReLU(m_i/sigma_i)|
    <= eta_i/sigma_i.
```

The conservative status is exact when the ideal margin lies outside the
mode-relative `2eta_i` decision band from Theorem 2. If a downstream map `G`
is `L_G`-Lipschitz, its feature-induced error is bounded by

```text
L_G ||(eta_i/sigma_i)_i||
```

in the corresponding norm. Both the margin envelope and downstream bound must
be accepted under their named scopes. Approximation accuracy is not its own
certificate.

### 7.5 Scale covariance and normalization

Under a positive unit change

```text
m_i' = lambda_i m_i,
```

license status is unchanged but an unnormalized surplus transforms as

```text
z_i'=lambda_i z_i.
```

There are three legitimate responses:

1. **invariant normalization:** set `sigma_i'=lambda_i sigma_i`, so
   `ReLU(m_i'/sigma_i')=ReLU(m_i/sigma_i)`;
2. **covariant consumer:** transform a linear consumer by
   `A'=A diag(lambda_i^-1)` so `A'z'=Az`; or
3. **declared homogeneous quantity:** if `G(lambda z)=lambda^k G(z)` under a
   common scale, report the corresponding unit-bearing covariance.

Independent unnormalized rescalings can change cross-channel argmax. A common
positive scale preserves ordering but changes magnitudes. The reference
classifier therefore uses a fixed normalization registry. Multiplying a
variable payload by a margin is not part of this theorem: it introduces a
bilinear map in general, changes units, suppresses supported equality, and
defines a new plan requiring its own evaluation.

## 8. Annotated finite-plan realization

### 8.1 Proof-erased plan map

Fix a finite acyclic typed plan DAG. Its exact annotation separates:

```text
payload y_v,
quantitative grade g_v,
certificate/checker/assumptions kappa_v,
provenance/rank p_v.
```

The **proof-erased numerical map** keeps the payload and grade coordinates but
does not replace or predict `kappa_v` or `p_v`.

Assume:

1. every numerical primitive is a global finite CPWL map;
2. every grade transformer is CPWL on its typed real coordinates;
3. pairing, fan-out, affine transport, `min`, `max`, and ReLU are finite;
4. every hard branch is over a finite polyhedral complex and satisfies
   Theorem 4's trace agreement; and
5. the input dimension and output payload/grade dimensions are fixed and
   finite.

### Theorem 8 (finite annotated-plan CPWL/ReLU realization)

Under these assumptions, the root proof-erased joint map

```text
H_G:R^d -> R^(p+g),
H_G(x)=(y_root(x),g_root(x))
```

is global finite CPWL. Hence it has an exact finite ReLU realization with an
affine output. The certificate, checker result, assumptions, evidence scope,
and provenance remain external inputs to the Task 14C root-license rule.

#### Proof

Proceed in topological order. Input and primitive nodes are CPWL by hypothesis.
Finite Cartesian tupling of coordinate maps is CPWL after taking common
refinements of their polyhedral decompositions. Affine composition, finite min/max, and ReLU
preserve CPWL. Composition of finite CPWL maps is CPWL because on each pair of
source/target cells the relevant affine preimage intersection is polyhedral,
and only finitely many pairs occur. Hard branches glue by Theorem 4. Thus every
node's payload/grade pair, and in particular the root pair, is CPWL. Apply
Theorem 3 coordinatewise. ∎

### 8.2 Size, depth, and recursive computation

There are two exact constructions.

- **Flattened:** derive the global CPWL root coordinates and apply Theorem 3.
  The hidden-depth bound depends on input dimension, but the lattice
  decomposition and size may be enormous.
- **Compositional:** replace each primitive/grade transformer by its exact
  network and compose the finite feed-forward DAG. Depth follows the longest
  composed path and size is finite, with signed identity channels used to pad
  unequal paths when converting the DAG to a strictly layered MLP.

The second construction mirrors a recursively structured model: submodels can
compute intermediate payloads and grades consumed by later submodels. It does
not turn the forward pass into a proof. Task 14C's typed certificate term and
checker provide the proof-carrying part; erasing them leaves the numerical
computation characterized here.

### 8.3 Exact limits

The theorem excludes, unless separately reduced to CPWL:

- multiplication of two variable channels, general division, exponentials,
  or smooth curved primitives;
- unbounded loops or a dynamically growing plan in one fixed finite network;
- cyclic self-assessment without the separate fixed-point semantics rejected
  from the compact core; and
- discontinuous hard seams inside one ordinary continuous ReLU output.

For example, `(m,y)->m y` is bilinear and not CPWL on an open two-dimensional
set, so “margin times payload” is not an exact generic ReLU gate. On a compact
domain a non-CPWL continuous primitive may be approximated, but the production
claim then requires a verified envelope. Theorem 2 transports that envelope
to conservative licenses and downstream grade error; universal approximation
alone does not.

## 9. What transfers beyond ReLU

The results divide cleanly.

| result | architecture dependence |
|---|---|
| kernel/quotient factorization | none |
| conservative margin theorem | none; needs bounded statistic error and exact decoder |
| finite CPWL exact construction | ReLU-specific witness, also available to any architecture with exact finite CPWL closure |
| seam gluing theorem | none |
| discontinuity obstruction | applies to every continuous-output architecture |
| fixed/expandable library results | interface-level, not ReLU-specific |
| joint-sufficiency/minimal channel theorem | none; ReLU supplies the positive-part implementation |
| finite-plan CPWL closure | function-class theorem; exact network realization depends on architecture |

A maxout or lattice network may implement some max/min structure more directly.
A hard mixture of experts may realize discontinuities that an ordinary ReLU
MLP cannot. A graph/set model may expose a variable plan DAG more naturally.
Each remains compatible only if it preserves the same exact side packet,
evidence/checker boundary, diagnostics, mask, and fallback contract.

Universal approximation by any architecture establishes only approximate
function-class density under its stated domain and norm. It establishes none
of:

- semantic compatibility with the license calculus;
- proof or certificate production;
- efficiency or finite exact representation;
- learnability by the selected optimizer;
- calibration or validity under shift;
- preservation of missingness and exact identities; or
- interpretability or scientific-domain alignment.

## 10. Executable witnesses and claim disposition

[`verification/representation_theorems.py`](../verification/representation_theorems.py)
and
[`verification/test_representation_theorems.py`](../verification/test_representation_theorems.py)
make finite boundary cases executable. They check:

- factorization collisions and the canonical finite quotient;
- affine error propagation, conservative support/refutation, open bands, and
  one-sided withholding;
- exact ReLU max identities;
- agreeing affine traces and a rank-one seam, plus a disagreeing hard seam;
- fixed-registry failure, shared-score equivariance, and extension-sensitive
  non-domination;
- named dual-use features, boundary collision, normalization invariance, and
  the equal-adequacy/different-payload separator; and
- a finite CPWL plan jointly computing payload and grade while rejecting an
  undeclared primitive.

These are regression witnesses for the stated proofs, not proof-assistant
formalizations and not empirical evidence about training.

No new central project claim is falsified. Three overbroad readings are
explicitly blocked:

1. the conservative exact-recovery band is twice the propagated raw margin
   error;
2. an exact result on a restricted domain requires an explicit global CPWL
   extension; and
3. finite candidate-conditioned evaluation does not imply global library
   closure.

The dual-use claim `F32` is now formally supported for the named
coordinate-complete channel family, while empirical calibration, learned
semantic alignment, and usefulness of those channels remain open.

## Task conclusion

The neural correspondence now has a theorem spine rather than only an
interface specification. The exact mathematical object is a hybrid:

```text
finite CPWL numerical map
    + accepted approximation/calibration envelopes
    + exact typed evidence and metadata
    + deterministic boundary-aware K_3/profile decoder
    + exact mask, routing restriction, and fallback.
```

Within that object, ReLU supplies an exact finite realization of CPWL
statistics and proof-erased finite-plan computations, and named positive
margin channels can legitimately serve as both adequacy surplus and downstream
features. It cannot directly supply discrete boundary semantics, evidence
validity, global open-library closure, discontinuous hard seams, certificates,
or arbitrary computational payloads. Task 18's
[`04_losses.md`](04_losses.md) now chooses the structured training objective,
held-out calibration path, atom cross-entropy baseline, and separate router
loss against this fixed target without confusing optimization success with any
of those guarantees.
