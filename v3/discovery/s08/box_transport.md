# A retained scalar lower survives interval refinement cheaply

**DEVELOPMENT derivation — Codex (GPT-6), October14,2026 UTC.**

Keep the same supplied m-copy action and a checked old lower L for the
transformed objective q in box_regret.md. Refining one interval from[l,u]
to[l',u'] changes its q coefficient by

```math
\delta=a(u'-u)+(m-a)(l'-l).
```

Every feasible feature is binary, hence q' dot v >= q dot v+min(0,delta).
So L'=L+min(0,delta) is a valid new scalar lower without a new proof call.
The action upper cost falls by a(u-u'). Substituting into the regret upper
gives the exact decrease of this transported bound:

```math
\Delta=\min\{a(u-u'),\ (m-a)(l'-l)\}\ge0.
```

For an exact audit t, this becomes min(a(u-t),(m-a)(t-l)). Several
coordinates sum independently; applying the update sequentially or from
the original saved q gives the same valid correction. Source identity,
action count a, old bound, interval inclusion and acquired receipt all
remain required. Nonnegative objectives also permit max(0,L') as a lower;
this can further sharpen the bound. The original regret certificate stays
valid on the smaller box in any case.

The limitation matters for the proposed next experiment. For m=1, every
a is0 or1, so this generic transport gives zero guaranteed regret-bound
contraction from any audit. Cost upper bounds can still improve the
replacement branch, and exact regret can decrease, but another source-aware
argument, retained proof-tree reweighting, or new scalar proof may be needed
to expose that decrease. Do not price every audit as if it automatically
improves the checked repair bound. For an interior count0<a<m, a middle
receipt contracts both endpoints and gives a positive guaranteed decrease.
This is consistent with the earlier middle-receipt query structures.

For example m=2,a=1,[l,u]=[0,2], audit t=1 gives delta0, upper cost down1,
and retained regret upper down1 with no additional proof. An endpoint audit
t=0 or2 gives this generic contraction0. A source-specific equality can
do better: if the feature is proved mandatory, its change is delta rather
than min(0,delta). That requires the very geometry receipt whose acquisition
and reuse costs the continuation is meant to measure.

This is an elementary scalar lower-bound transport, not a new general
reweighting theorem. It does not claim that the transferred lower is sharp,
or that a fresh complete proof is worth its cost. It refines the next
service design by separating a free algebraic update from a paid new
logical acquisition. No additional physical proof/audit was run for this
derivation; br02's six actual receipts are the executed bridge so far.

The monotonicity statement keeps the action, copy count and source fixed.
A newly proposed action changes a and requires a separately checked
transport or proof; its smaller claimed nominal cost does not inherit the
old regret warranty. Price changes leave q and repair-only regret intact
but require recomputing the replacement comparison. Receipts belong to
their original request/source identities; a reused mathematical proof is
not permission to reuse another request's physical observations.
