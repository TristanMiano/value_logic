# Canonical potential-relative compression: candidate derivation

Codex (GPT-6), DEVELOPMENT. Extends S11L, with Q1/Q2/Q3/Q4/Q5 connections.
This is a prospective derivation, not a verified novelty or promotion claim.

## Finite interface and known ingredients

There are n hidden states. Terminal actions a have cost vectors c_a. A purchased
operation e has expected immediate cost q_e and nonnegative outcome-transition
matrices K_eo. Their sum T_e is stochastic. K_eo maps a next-state column
function back to its unnormalized expectation at the current state; beliefs
are row vectors. A finite policy tree uses operations and observed outcomes,
then selects a terminal action. All operators, costs and their acquisition
semantics are supplied or separately justified. This is a finite reasoning
interface, not a truth oracle or learned counterpossible semantics.

For a state potential b, define terminal residuals r_a=c_a-b and charged
increments g_e=q_e+T_e b-b. Standard telescoping gives V_pi-b as the transformed
policy cost vector. This uses the transition EXPECTATION in g_e; no observation
of hidden b is required. Every terminal path must include its residual cost.

Let cl(S) be the smallest linear space containing S and invariant under every
K_eo. Linear value-directed compression uses such spaces. Define

```math
M_b=\mathrm{cl}\bigl(\{c_a-b:a\in A\}
  \cup\{q_e+T_e b-b:e\in E\}\bigr).
```

No constant feature is imposed unless required by the costs or requested output.
If observation probabilities or normalized beliefs are also requested, include
the constant vector 1 in every generating set. Both variants below use the
same choice consistently.

## Candidate canonical-minimality statement

Fix ANY available terminal action a0 and set b0=c_a0. Then

```math
M_{b_0}\subseteq M_b\qquad\text{for every potential }b.
```

Proof candidate: d=c_a0-b belongs to M_b. Every terminal difference
c_a-c_a0=(c_a-b)-d belongs to M_b. Invariance under the outcome operators also
gives invariance under their sum T_e. Hence

```math
q_e+T_e c_{a_0}-c_{a_0}
 = (q_e+T_e b-b)+(T_e-I)d
 \in M_b.
```

All generators of M_b0 lie in invariant M_b, proving inclusion. Applying the
inclusion with two terminal references shows their canonical spaces are equal.
Thus a terminal reference minimizes the required invariant space by inclusion,
not only by dimension, among this specified class of potential transformations.
It does not minimize arbitrary nonlinear decision representations or planning
runtime. Computing the space from a huge explicit source may itself be costly.

This strengthens the earlier S11L example: no search over arbitrary potentials
is required to find the least such space. A pointwise minimum of terminal costs
can still add unnecessary features, as the earlier exponential example shows.
Whether this modest extension is already stated in the closest literature is
unresolved and must be checked before a novelty claim.

## Policy execution without a probability-normalization feature

Take a basis F for M_b0, with K_eo F=F B_eo, r_a=F u_a and g_e=F v_e.
For unnormalized hidden-state weights p, keep z=pF. A terminal coefficient is
u_a; an operation tree with child coefficients alpha_o has coefficient

```math
\alpha=v_e+\sum_o B_{eo}\alpha_o.
```

Its transformed expected cost is z alpha. Update z after outcome o by z B_eo.
All policy costs at a realized history share the same positive posterior
normalizer, so minimizing these unnormalized costs chooses the same policy.
The baseline expectation is common to every available continuation and also
cancels. A zero-probability history can be assigned any action. There is no
claim that z identifies observation probabilities or the posterior distribution.
Normalization-free planning is inherited from ordinary value compression;
the candidate extension is the canonical baseline result and its paid/revision
interface. A separate output contract requesting absolute costs needs the
omitted baseline information.

## Next cheap screens

Check the inclusion using exact small rational systems and compare full and
compressed finite policy trees, including informative observations and nonzero
charges. Look for a failure caused by early stopping, negative transformed
charges, heterogeneous observation menus or a changed operation. Derive a
small source family where source construction and feature acquisition stay
compact, rather than merely computing a small rank from a huge table. Compare
with the same ordinary Krylov compression after potential shaping.

## Stronger candidate: the span of all policy differences

Let D be the linear span of V_pi-V_rho for all finite contingent policy trees
over this fixed interface, allowing stopping at any history. Then D=M_b0.
One inclusion follows from the transformed recursion: every V_pi-c_a0 belongs
to M_b0. For the other, terminal differences belong to D. Each charged increment
q_e+T_e c_a0-c_a0 is the difference between doing e then stopping with a0 on
every outcome, and stopping with a0 immediately. Finally D is invariant under
each K_eo: place two policies in outcome o of otherwise identical trees rooted
at e. The root charge and other branches cancel, leaving K_eo(V_pi-V_rho).
Thus D contains the generators and their closure. This also gives finite
policy-pair witnesses for every generated vector.

Consequently the canonical space is necessary for any LINEAR representation
that exactly recovers all policy-cost difference functionals, even if it is not
initially described through a potential. This is still stronger than merely
choosing an optimal policy: dominated policies can make D larger than needed
for that weaker task. A constant function is sometimes free at a normalized
root, but not over arbitrary unnormalized history weights. Distinguish vector
space dimension from the number of acquired scalar observations.

The assumptions matter. The reference terminal action must be available after
every history used in the branch construction. State-dependent action menus
need their own predicates. There is no infinite-horizon claim about negative
transformed increments or convergence. If paid invoices reveal hidden outcomes,
their observations must also appear in K_eo. Source construction and basis
acquisition remain charged even when the resulting rank is small.

## Bounded horizons and a sharper limit on the interpretation

For policies using at most h operations, let D_h span V_pi-c_a0. Stopping is
allowed at every stage. Direct branch insertion gives

```math
D_0=\mathrm{span}\{c_a-c_{a_0}\},\qquad
D_{h+1}=\mathrm{span}\left(D_0\cup\{g_e\}
                 \cup\bigcup_{e,o}K_{eo}D_h\right).
```

The spaces increase monotonically. A single equality D_h=D_h+1 implies closure
and equality with M_b0 thereafter. If d0=dim(D0), the canonical space is attained
by depth at most n-d0: every nonstationary step increases rank by at least one.
This bounds the depth needed to generate the linear span, not the cost of
enumerating optimal policy trees.

For a finite horizon, choose bases F_h. The smaller layered identities
K_eo F_h=F_h+1 B_eo,h suffice; one need not compute the full invariant space.
An initial z=pF_H can update to the next layer after each observation. This
is a candidate exact representation for bounded reasoning rather than an
infinite-horizon obligation. The same policy-pair argument makes D_H minimal
for recovery of all horizon-H cost-difference functionals.

An essential qualification: for an arbitrary potential b, the span of the
COMPLETE transformed policy vectors is only

```math
\mathrm{span}\{V_\pi-b: |\pi|\le H\}
     =D_H+\mathrm{span}\{c_{a_0}-b\}.
```

It exceeds D_H by at most one dimension. The larger M_b computed from separate
local generators is a stronger compositional invariant-space requirement. Its
possible exponential growth is not an information-theoretic lower bound on
complete policy evaluation. Telescoping can cancel intermediate terms before
representation. A compiler that carries differences and one separately priced
baseline can avoid that inflation. This distinction must accompany any claimed
dimension saving against pointwise-minimum normalization.

## First executed screen

The original full-run attempts failed at different interpreter locations;
[failure dispositions](failures.md) preserve them. The explicit per-case
amendment completed all 25 declared cases with **4,314 exact policy-recursion
comparisons**, five unnormalized-weight action-set checks per case, and
canonical inclusion against five potential choices. The 20 random dense
systems had full canonical rank: compression is not generally guaranteed.

Structured examples had canonical versus raw-cost invariant dimensions 2 versus
4, and 0 versus 0 for the null case. Allowing a counterfactual operation to
change the former nuisance increased its canonical rank from 2 to 5; the old
representation is not automatically transportable. In the inherited signed
flip family, m=3 gives canonical rank 4 versus pointwise-minimum invariant rank
7; m=5 gives 6 versus 21. These are representation dimensions at a specified
interface, not economic savings or superiority over ordinary shaping/compression.
The layered recurrence and the complete-policy-span qualification above were
derived after this probe and are not additional executed claims from it.
