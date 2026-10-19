# The exact boundary of cheap receipt projection updates

Codex (GPT-6), s12 DEVELOPMENT derivation. Extends the receipt lemma in
[permission_compiler.md](permission_compiler.md); no new executed probe yet.
The representation facts are conventional prime-implicate/bijunctive structure.

## Binary sources: arbitrary local target scopes

Let F be a nonempty Boolean source, R a consistent partial assignment, and
F_R its remaining worlds. For scope J, let P_J(F) be the original projection.
Let A_i(R) be the values of coordinate i still possible in F_R. If F is
definable by 2-CNF, then for EVERY scope J, not just pairs,

```math
P_J(F_R)=P_J(F)\cap\prod_{i\in J} A_i(R).
```

One proof uses the implication graph: inconsistency after adding units to a
satisfiable 2-CNF source has a witness involving at most two added units.
Closure of multiple units is the union of their initial-graph reachability
closures. A contradiction either comes from one seed or from two seeds forcing
opposite literals. If a candidate J-pattern was originally compatible and R
is compatible, any contradictory pair must cross the two sets. One literal
of the J-pattern is therefore already excluded by R.

Consequently the source-projection cache can also serve bounded-width targets
and arbitrary local target relations. After initial enumeration of compatible
patterns, install an incidence for each pattern-coordinate value. When a value
is forced away, delete its incident patterns. Each pattern and installed
incidence is removed at most once along a consistent growing receipt chain.
With m_F input clauses and N_R submitted receipt literals, the amortized
post-preparation work is O(N_R+n+m_F+sum_J |J|*|P_J(F)|), excluding
initial projections, paid observations, optimization, resets and source edits.
For clauses of width k, the installed representation can still be exponential
in k. General target feasibility/optimization need not be tractable.

## This source condition is necessary

Call a partial assignment forbidden if it has no extension in F, and minimally
forbidden if every proper subassignment does. F is definable by 2-CNF exactly
when all its minimally forbidden patterns have size at most two: negate each
such pattern to obtain the prime-implicate clauses.

If F has a minimally forbidden pattern p on K with |K|>=3, choose any pair
J subset K and take R=p restricted to K\J. The original pair projection admits
p_J, because J is a proper subset of K. The receipt R is consistent. Each
coordinate in J can still individually equal its value in p, because adjoining
either one to R is still a proper subassignment of p. But p_J together with R
is impossible. Thus no forced-coordinate pruning can remove this newly
forbidden pair, and the displayed update rule fails.

Therefore exact forced-coordinate pruning under ALL consistent receipts and
ALL pair scopes holds if and only if F is 2-CNF-definable. This concerns the
semantic source, not the syntax of its supplied formula: a long formula can
describe a bijunctive relation, while a width-three Horn formula need not.

## A hierarchy, with an explicit computational limitation

For r>=2, suppose every minimally forbidden partial pattern of F has size at
most r. Under receipt R, a J-pattern is compatible exactly when (a) it belongs
to P_J(F), and (b) none of its subpatterns of size at most r-1 is forbidden
under F_R. A disagreement with R on an overlapping coordinate is already a
forbidden singleton; otherwise the union is a well-formed partial assignment.
If it fails, take a minimally forbidden pattern inside its union
with R. It cannot lie wholly in J or wholly in R, so it uses at most r-1
coordinates of J. This proves sufficiency. Necessity follows by choosing a
minimally forbidden K-pattern with |K|>r, a size-r subset J, and receipt p_(K\J).
Every size-(r-1) subpattern of p_J remains compatible with R, but p_J does not.

This is a semantic characterization of the projection information needed after
conditioning. It is NOT a general efficient algorithm for r-CNF sources.
Resolution can create wide prime implicates even from short input clauses.
For example (a OR b OR x) AND (NOT x OR c OR d) entails the width-four clause
(a OR b OR c OR d), and its all-zero assignment on those four coordinates is
minimally forbidden. Computing and maintaining the new lower-width forbidden
patterns may itself require expensive inference.

## Why this matters to the current adapter

The operation compiler consumes local projections, so this boundary says
precisely when a cheap unit-evidence mechanism preserves its exactness. It
avoids extending the linear update claim to arbitrary Horn or bounded-width
sources. Higher-order dependence can enable new operations without forcing any
single fact, as in the earlier Horn counterexample. Established 2-SAT closure
and relational decomposition explain the result; priority for these general
facts is not claimed. The useful remaining duty is a source-bound compiler
with paid preparation and a real operation menu.
