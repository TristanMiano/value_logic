# Reuse the all-map compiler for warrants and priced overwrite repair

Codex (GPT-6), DEVELOPMENT, October20,2026. Applies
[permission closure](permission_closure.md) beyond toggles. The first-pass
all-map compiler below was already established in s12/permission_compiler.md
section7; its initial reconstruction this session is not a new result. The
second warrant pass and priced overwrite fragment are the proposed deltas.

For coordinate i represent a unary Boolean action by its truth-table entries
u_i=a_i(0) and v_i=a_i(1). The four pairs00,01,10,11 mean set-zero, keep,
complement and set-one. An action is thus2n Boolean variables. A binary
availability formula A0 may restrict this table: banning complement is the
single implication u_i=>v_i, leaving the ordered overwrite/keep menu. Requiring
toggle-or-keep is u_i!=v_i, also binary. Cross-coordinate binary restrictions
are possible. General resource budgets do not automatically have this form.

For source F and binary postcondition G, first obtain the source projections
on each goal clause's one or two coordinates. At a pattern x_i,x_j, replace
each postcondition literal on coordinate i by the corresponding signed
truth-table variable u_i (if x_i=0) or v_i (if x_i=1). Conjoin all resulting
clauses with A0. The result A is precisely the set of actions safe on all F,
and is 2CNF. A union of binary source models still admits each required
projection by a union of ordinary 2SAT checks.

To compile the maximal warrant W, consider each possible world pattern on
each goal clause. Ask whether A has an action making that clause false on
that pattern: this is A plus at most two unit literals on selected table
entries. If it is satisfiable, forbid the world pattern in W. There are at
most four such calls per binary goal clause. Their conjunction is exactly

```math
W=\{x:\text{every }a\in A\text{ sends }x\text{ into }G\}.
```

It is the largest source retaining precisely the original allowed actions
relative to A0, by the same two-inclusion argument. Fixed unary substitutions
preserve binary clauses, so the strongest binary hull of F is again inside W.
The second pass does not enumerate4^n actions. Both passes use ordinary 2SAT
and local projection; no new logical connective or source-truth oracle is
introduced. Later truthful receipts can condition W soundly with the original
coverage event, while the earlier conditional-equivalence limitation remains.

## The strong ordinary reset control

If every coordinate may be overwritten, any known satisfying assignment of G
supplies a blind reset action safe on *all* worlds. An application cannot
claim that a model enabled safe action merely because it finds such a reset.
Its useful role would be to avoid expensive writes, preserve valuable state,
or satisfy meaningful action restrictions. Finding a satisfying G is easy
for this binary fragment, but minimizing weighted edits is not generically
easy. Prices, preservation losses and action constraints must be compared
against that reset control before an economic claim.

The first pass is retained machinery, not evidence of a new capability or
complete-cost gain. In particular, a budget on how many coordinates are overwritten cannot
be inserted for free: the overwrite indicator depends on equality of u_i and
v_i, and arbitrary cardinality constraints need their own representation.

## A tractable priced overwrite fragment

Suppose G consists only of positive implications x_i=>x_j and unit constraints.
Restrict actions to set-zero, keep and set-one, so u_i<=v_i. Let writing zero
cost c_i0>=0, writing one cost c_i1>=0, and keeping cost zero. These are prices
for issuing a write command, whether or not the old value already agrees.
Each robustly compiled goal clause is an implication between two truth-table
entries, and availability may add more implications or units. The exact cost
of a valid monotone action is

```math
\sum_i\bigl[c_{i0}(1-v_i)+c_{i1}u_i\bigr].
```

For00,01,11 this gives c_i0,0,c_i1 respectively. Therefore choosing a cheapest
universally safe overwrite action reduces to a linear objective over an
implication-closed set of2n Boolean entries: the ordinary minimum-cut/maximum-
closure problem. Encode every implication with an effectively infinite arc,
and each signed unary coefficient by a source or sink arc. A finite sentinel
greater than the sum of all finite capacities suffices; contradictory unit
requirements are reported infeasible rather than treated as a paid violation.

For g binary implications, at most4g compiled implication arcs plus n local
monotonicity arcs are needed before duplicates, plus units and availability.
The source projection bill is separate. A returned action is safe for F and
also for the compiled maximal warrant W; with a supplied coverage event for W,
the full model F may be wrong. This is a concrete ordinary optimizer coupled
to a weaker model premise, not superiority over ordinary maximum closure.

The fragment excludes arbitrary binary postconditions, arbitrary cardinality
budgets and arbitrary joint preservation losses. If charging only actual bit
changes instead of commands, the expected coefficients require warranted
marginal probabilities; a worst-case joint bill is a different optimization.
Allowing complement at price c_if keeps the two-bit cost submodular only when
c_i0+c_i1<=c_if. The overwrite-only theorem needs none of those extensions.

The previous s12 implication optimization in permission_compiler.md section4
assumed source=goal and toggle actions. This fragment admits an arbitrary
source with affordable pair projections, a positive-implication goal and
priced overwrite/keep actions. It still uses the established maximum-closure
optimizer. Source acquisition, maximal-warrant acquisition and meaningful
application economics remain separate obligations.

unary_probe.py passes73 general compiler/warrant panels and84 priced repair
panels, including11 infeasible cases. Enumeration agrees with the minimum-cut
optimum in all84. The finite first-pass checks partly duplicate earlier scope;
do not count them as an additional capability. The new second-pass and priced
checks are development diagnostics, with no arm runtime comparison.
