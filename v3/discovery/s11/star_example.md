# A branching repair example and its exact witnesses

Codex (GPT-6), DEVELOPMENT hand derivation. This checks a small consequence of
the proposed structured adapter without building another large LP experiment.

Use original bits (c,a,b) satisfying c implies a and c implies b, with the
same target constraints. The five source worlds are 000,001,010,011,111.
Only c is queryable, at fee 1/4. The total query/edit cap is two, edit fees are
zero, terminal zero costs zero, and terminal one costs the sum of the three
revised signs (zero bit means sign -1). Edits are an atomic batch.

Before a query only the identity mask preserves every source world. Observing
c=0 allows arbitrary leaf flips; with the remaining cap, at most one leaf may
be flipped. Observing c=1 allows identity or the single center flip. These
claims follow by checking the two implications, not by treating the leaves
as independent probabilistic evidence.

There are fourteen pure policies: two root terminals, or one query followed
by four choices at c=0 (abstain, identity, flip a, flip b) and three at c=1
(abstain, identity, flip c). Their point-source minima are

```math
B=(-3,-11/4,-11/4,-3/4,0).
```

The full randomized optimum is 89/48. A primal witness uses root identity
with probability 7/12 and queries with probability 5/12. After c=0 it flips
one uniformly chosen leaf and releases; after c=1 it abstains. Its worldwise
regrets are

```math
(45/48,89/48,89/48,49/48,89/48).
```

A dual witness puts masses 11/24,11/24,1/12 on 001,010,111. Every pure policy
has expected regret at least 89/48 under that law. In particular root identity
and a query followed by either leaf flip attain it. Conditional identity also
attains the same expected value under this dual law; this is harmless dual
degeneracy, not a missing feasibility condition.

The optimized no-query class uses root identity with probability 11/16 and
abstains otherwise; its worst regret is 33/16. A no-query dual uses total mass
3/4 split equally between 001/010 and mass 1/4 on 111. Therefore the full
improvement against this restricted class is 5/24, or exactly 10/99 of its
regret. Both classes use the SAME full operational comparator B. An equally
informed ordinary repair optimizer ties the full construction.

The branching menu also exposes the cap issue: giving each leaf flip marginal
probability 1/2 and sampling independently violates the one-remaining-edit cap
with probability 1/4. The joint choice 'flip exactly one leaf' is valid.
Expected cardinality alone cannot replace a cap on each realized output.

Before the following finite screen, fix exactly this source, fourteen-policy
enumeration and the displayed rational primal/dual witnesses. Check every
mask by universal truth enumeration and every expected regret by fractions.
One case only, no optimization/tuning or measured acquisition. At most two
unchanged retries. The screen supports this example, not the whole treewidth
extension or a practical service gain.

The [exact screen](star_probe.py) passed st01/c00a0 on its first attempt.
Its source hash is
431a2d373cc236c788d2d367135c44f939afdf533adaf6af37389d0e70e67942.
All five point-source values, fourteen dual inequalities and both primal
witnesses are checked with fractions; no numerical LP output is involved.
