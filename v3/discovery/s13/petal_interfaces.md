# Shared context and disjoint target blocks

Codex (GPT-6), DEVELOPMENT, October20,2026. Strengthens the singleton-scope
adapter in [interface_expansion.md](interface_expansion.md). Ordinary 2-SAT,
forgetting and join representations remain the underlying machinery.

## A useful extension of the two-model boundary

Let the nonempty scope family be S_j=Q union T_j, with pairwise disjoint
petals T_j, each disjoint from Q. Petals may contain arbitrarily many Boolean
coordinates. Let U be the union of M nonempty 2-CNF sources F_m and
H(U)=intersection_j cylinder P_(Q union T_j)(U). Maintain only the supplied
warrant x in H(U), even when every full F_m is false.

For each m prepare B_m=P_Q(F_m). For a petal's own unit receipts h_j,
the residual projected source on Q is

```math
P_Q(F_m\wedge h_j)=B_m\wedge C_{mj},
```

where C_mj is a conjunction of unary Q consequences, or false if that
receipt makes F_m inconsistent. This follows from binary prime implicates:
conditioning units can introduce new unit consequences but no genuinely new
binary consequence between two still-unfixed coordinates. Such a binary
consequence was already in B_m, or is implied by a new unit consequence.
Equivalently, use the exact binary receipt-pruning lemma from s12.

The key is to compute this separately for every model/petal pair. Combining
all petals' receipts inside one F_m would impose a common branch witness,
which the weaker joint envelope does not warrant.

After all current receipts, the possible Q values are

```math
\bigvee_{\varnothing\ne B\subseteq[M]}
 \left(\bigwedge_{m\in B}B_m\;\wedge\;
       \bigwedge_j\bigvee_{m\in B}C_{mj}\right),
```

together with actual receipts on Q. For the forward direction, choose all
models compatible with q. For the converse, each petal obtains its own model
and completion, and disjointness lets those completions coexist. This is
exactly the singleton argument with a whole privately completed block.

For M<=2, use at most3 2-SAT branches. In the two-model branch each petal's
OR of unary conjunctions has the linear selector encoding. Bounded-size new
projection queries add temporary unit receipts to whichever petals they
touch. Thus the positive adapter handles arbitrary-size disjoint original
target blocks, not only singleton targets. The earlier three-model hardness
already uses singleton petals and still applies.

Preparation and updates need charges. One safe upper bound recomputes each
P_Q(F_m AND h_j) using ordinary binary inference whenever that petal changes;
the Q remainder is encoded by its forced literals, after checking consistency.
Then rebuild the at-most-three selector formulas and solve them for each
requested bounded pattern. This is polynomial but can duplicate model work
across petals. No previous unit-only O(n+R) service bound is inherited.

## Where this argument stops

If two petals share a coordinate outside Q, their individually possible
completions need not agree. For example, one local block can require z=0 and
another z=1. The displayed branch test only checks Q and would miss the
conflict. Move all such shared coordinates into Q, or use an explicitly
costed separator/join algorithm. Arbitrary overlap is not covered by the
disjoint-petal derivation. Enlarging Q changes the original adequacy envelope;
do not silently strengthen the physical warrant just to apply this theorem.

An explicit adapter failure uses one source F=(a=>z) AND (b=>not z),
Q empty, petals{a,z} and{b,z}. The actual join H(F) equals F. Receipts a=1,
b=1 are jointly inconsistent, but each petal's receipts alone are consistent.
The invalid no-separator test would say yes. This rejects the naive extension
of this adapter, not tractability of all one-model binary envelopes.

A separate computational strategy may condition shared coordinates by case
analysis while keeping the original H; that spends exponential work in the
number conditioned, without changing the warrant. The common-context size
itself also supplies a simple alternative: enumerate2^|Q| contexts, test each
model/petal compatibility, and retain consistent contexts. That works for any
M and is often more useful than a bare worst-case hardness statement when
the original context is genuinely small.

## Ordered-source lead, not yet an imported theorem

A finite ordered coordinate can be represented by threshold bits with chain
constraints. Median-closed sources become majority-closed threshold images,
and thus binary Boolean relations. An exact-value or interval observation
becomes unit threshold receipts. This suggests applying the petal argument
to median-closed sources on finite chains, with source/threshold encoding
size charged. Nonconvex observations are not unit conjunctions and remain
outside the claim. Check the source representation and the ordered antecedent
before treating this extension as established.

The finite-chain proof can in fact be completed without a new statistical
assumption. Map x_i to bits1[x_i>=k] for all thresholds k in its finite chain.
This embedding commutes with componentwise median/Boolean majority. The image
of a median-closed source is therefore majority-closed and has an exact2-CNF
description, including the monotone threshold-chain clauses. Each original
petal becomes a disjoint block of threshold bits. An interval receipt fixes
some threshold bits to0 or1, so the disjoint-block adapter applies. New value
or interval feasibility questions likewise add units; arbitrary finite
bounded-size value projections can be enumerated with their domain cost.

This is an explicit adapter of the established majority/2-CNF correspondence.
If source relations are given as tables, enumerating all threshold unary/pair
consequences costs O(|F_m|*N^2), where N is the total number of threshold bits.
That price may be enormous for large integer domains encoded in binary.
No strongly polynomial temporal-network bound is claimed. Nonconvex
observations require disjunctions and can destroy the convenient form.

## A paid tractable fallback for many models

Dropping the third model is not a sound repair of the hardness result: the
original warrant x in H(union_m F_m) need not place x in the smaller envelope
of a selected subset. Instead overapproximate the *warranted* H.

Before any new receipts, a requested assignment on k coordinates touches at
most k petals. For each touched petal choose one witnessing model; if no petal
is touched, choose one model for the Q projection. For a fixed tuple of model
choices, conjoin their B_m bases and their per-petal unary consequences, plus
the requested Q values. This is2-CNF. At most M^k tuples suffice when a petal
is touched (and M otherwise). Untouched petals can use any selected eligible
model to obtain a completion. Thus initial width-k projections of H are
computable in polynomial time for fixed k, despite hard inference after an
unbounded number of new target receipts. Charge the exponential dependence
on k and the model/petal preparation; do not call it free compilation.

In particular, compile the full binary hull K2(H): all unary and binary
patterns admitted by H, expressed as forbidden-pattern2-CNF clauses. It has
the same initial unary/pair projections as H and contains H. The original
coverage event x in H therefore implies x in K2(H). Maintain K2(H) under
arbitrary future unit receipts and use the ordinary binary receipt service.
This stays sound and cheap but may lose conditional precision, exactly where
the three-model reduction places hard information. Initial binary target
permissions match the full warranted source; later permissions can be fewer.

The construction is the established binary/majority abstraction, adapted to
the paid joint-warrant interface. It gives an explicit fallback tradeoff:
preserve the physical warrant, pay polynomial preparation, and accept loss
of higher-order conditional information. It is not an inference algorithm
for the hard exact source. Already-observed target receipts cannot be hidden
in the preparation step: compiling the exact conditioned source may be hard.

## Finite development check

[petal_probe.json](petal_probe.json) checks48 sources with one, two or three
models,1728 conditioned-projection identities,2592 expanded receipt contexts
for the one/two-model adapter, and3456 initial pair patterns for the many-model
compilation method. The linear selector encoding is exercised, with4314
selector checks. All pass against finite world enumeration. Three guarded
3-CNF cases include a known-consistent forced-bit instance derived from an
unsatisfiable input. Combined runtime0.3911907 seconds. These are same-model
development screens, not unrestricted proof or independent confirmation.
