# A single-constraint countermodel for positive contact information

Codex (GPT-6), s18 DEVELOPMENT. This reveals a strong ordinary explanation
for several closure results: version-space reasoning over conjunctive models.
It is not claimed as a new principle of logic.

Let A be finite and let R be a known family of permitted constraint relations
on A. The unknown nonempty feasible source F is an intersection of members
of R; the empty conjunction A is allowed. The information consists of
reliable points B subset F and m existential contacts T_i, of which at most
r<m can be false. Then define a constraint C in R as individually compatible
when

    B subset C, and #{i:T_i intersect C is empty} <= r.

The entire guaranteed-action core is exactly the intersection of all
individually compatible constraints C. Every actual F is composed of such
constraints, so a point in that intersection is in every compatible F.
Conversely, each individually compatible C is itself an admissible source:
it contains B and hits enough reports, which also makes it nonempty. It is
therefore a countermodel to any proposed action outside C. If no constraint
is individually compatible, the intersection is A, consistent with the
empty-conjunction source being the only compatible possibility.

This does not assert that the intersection core itself hits all the contacts.
Different compatible source models can disagree on every action. It is a
universal information conclusion, not a learned true formula.

## Clausal source classes and backbone sufficiency

If each permitted relation is the satisfying set of a clause, its complement
is one subcube: the conjunction of the clause's falsifying literals. Whether
a contact lies wholly in that complement depends only on its fixed literals.
Thus backbone replacement preserves every individually compatible constraint
and hence the guaranteed-action core. Horn, dual-Horn,2-CNF and unrestricted
CNF source classes all fall under this observation with their respective
allowed clause families. The number of clauses to consider can be exponential;
the earlier Horn/2-CNF structure supplies their particular efficient tests.

Parity constraints have a different complement shape. They can depend on
correlations inside a contact, as the affine example in backbone_receipts.md
shows. Calling every relation a CNF does not repair this: the individual
clauses of that CNF need not themselves be allowable affine sources.

## Known base constraints and the limits of the argument

If every source must also obey a known base H, use countermodels H intersect C
and include H in the resulting core. Compatibility is tested on T_i intersect H.
For clausal variable constraints, the relevant fixed literals are therefore
the backbones of these intersected contact regions. When H and the contact
representation make those backbones tractable, this supplies a direct adapter.
If some contacts have empty intersection with H, they are necessarily false;
the error budget must cover them. The assumption r<m keeps every compatible
single-constraint countermodel nonempty.

Additional negative information not captured by the known base can invalidate
the simple enlargement F -> C: the enlarged set could include a forbidden
point. Similarly, relational coupling between the witnesses in different
reports destroys the independent-contact model. Those are changed source
contracts, not extensions established by the present proof.

This reduction makes a novelty assessment stricter. The possible contribution
would be a useful specified incomplete-evidence interface and its exact
computational/retention consequences. The act of ranging over compatible
ordinary constraints is itself conventional reasoning.
