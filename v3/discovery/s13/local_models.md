# Many fallible models with locally bounded overlap

Codex (GPT-6), DEVELOPMENT, October20,2026. Extension of
[petal interfaces](petal_interfaces.md), not a new numbered family.

The two-model query construction need not mean only two models globally.
Let B_m be the projection of model F_m onto shared coordinates Q. Suppose
every Q assignment belongs to at most two B_m, throughout the region allowed
by the current Q receipts. The exact petal-envelope query is the union of the
same singleton and pair branches, now over all M models. At a feasible q,
take its complete nonempty eligibility set, of size at most two. Conversely,
any singleton/pair branch gives a source witness in each petal separately.
This is precisely the earlier argument with a structural overlap bound.

Thus polynomially many models are permitted: at most M+M(M-1)/2 ordinary
2SAT branches, each using one selector per petal for the pair case. Omit
pairs whose base conjunction is inconsistent. The relevant parameter is
maximum simultaneous eligibility, not the raw number of models. This does
not generalize to overlap three: the previous hardness instance has exactly
three eligible models everywhere.

The bound itself must be supplied or checked. For binary bases, test every
triple B_i AND B_j AND B_k AND current-Q-receipts for inconsistency using
ordinary 2SAT. This polynomial audit can be expensive: O(M^3) solver calls,
with source size charged. Conditional receipts may establish the bound later
even when it was false initially. Pairwise intersections alone cannot certify
it, and simply choosing the best two models discards warranted worlds.

Example: Q contains s,x,y, with bases B1=(not s), B2=true, B3=s. No Q world
is eligible for all three, although the global source has three models.
For one target t, take residual clauses (t OR x), (t OR y), (t OR not x),
respectively. After t=0, exact acceptance is

```math
(\neg s\land x)\ \lor\ y\ \lor\ (s\land\neg x).
```

The two regimes give the two pair branches. This example does not establish
a novel algorithm: finite regime selection and 2SAT are direct ordinary
implementations. Its useful delta is a less restrictive hypothesis for safely
reusing a fallible model union after newly observed receipts.

## Scope geometry is a separate resource

Pairwise disjoint petals were essential. Acyclicity of the scope hypergraph
alone does not restore tractability: the old Q-plus-singleton scopes already
form a join tree and the three-model reduction is hard. Small individual
separators are also insufficient for cheaply solving a large central factor
after arbitrary incoming constraints. Their *union* may contain all the hard
variables. A safe generic construction enumerates the entire boundary of each
factor, solves its local model disjunction under each boundary assignment,
then joins the finite boundary relations. Exponential boundary preparation is
paid. This is ordinary constraint decomposition, not a free fast extension.

## Other leads screened at this boundary

Learning these bases from task success alone cannot certify their unseen
scope: two models may agree on every purchased task and differ elsewhere.
Statistical audits can warrant a deployment distribution, but need a separate
simultaneous event for adaptively selected future queries. The existing S08,
S10, S14 and S16 mechanisms already address that distinction. No new learner
or experiment is asserted merely by attaching those bounds here.

Likewise, transporting a proof through an *unchecked* mathematical analogy
does not create a checked proof receipt. A checked syntax/semantics map can
transport a proof, and a fallible analogy can rank which map to attempt; these
are conventional proof translation and acquisition guidance. A new workload
or tractable certificate would be needed for a contribution beyond that split.
