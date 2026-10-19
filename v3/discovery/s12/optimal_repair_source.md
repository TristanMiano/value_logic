# Keep every optimal implication-theory repair as one source

Codex (GPT-6), October 19, 2026. DEVELOPMENT early derivation, Q2/Q3/Q5.
This is a weighted model-repair semantics, not a solution to genuine
counterpossibles with every original axiom and meaning kept fixed.

Consider soft Boolean implications u implies v and positive/negative units,
each with a positive rational violation fee. Impose a set of hard literal
counterfactual assumptions A. A repaired world minimizes the total fee of
violated soft clauses subject to A. Fees express the announced repair policy;
they are not probabilities of the clauses being false. Preserve every minimizer
when reporting hypothetical consequences, rather than hiding ties by selecting
one convenient world.

The ordinary minimum-cut reduction is immediate. Introduce s,t. Give arc u->v
the implication's fee; encode a positive unit x by s->x, and a negative unit
NOT x by x->t. Add sufficiently large hard arcs for A (larger than the sum of
all finite fees), or handle hard reachability separately. A cut's source side
assigns one to its variable vertices. Its finite capacity is exactly the
violated-clause fee. Contradictory hard assumptions admit no repaired world;
they must not be interpreted as a universal warrant.

After one maximum flow, form the positive-capacity residual graph. A cut is
minimum exactly when no residual arc leaves its source side. Indeed its
capacity minus the flow value is the sum of residual forward capacities across
the cut, including reversals of backward flow. Thus all optimal repaired
worlds are represented by the 2-CNF implications z_u implies z_v for every
residual arc, together with z_s=1,z_t=0. Remove the terminal variables and
propagate their units. The result is a compact exact source for every optimum.

This gives direct access to the earlier local projection/permission interface:
check whether a hypothetical consequence holds in every optimal repair, retain
the possible values of a disputed consequence, or compile a further atomic
edit that works for every tied optimum. Hypothetical tie worlds are not a
hidden physical world to which the ordinary paid truth-query interface can
automatically be applied. A further selection needs its own policy or premise.

The restriction to implications and units is essential. General Horn 2-CNF
adds negative pairs NOT x_i OR NOT x_j. With a guard g and soft implications
g implies x_i, hard independent-set clauses on the x_i, and counterfactual g=1,
minimum violation fee includes maximum-weight independent set. The original
theory is consistent at g=0 and all x_i=0. Consequently even one contradictory
new literal need not admit cheap weighted repair in the broader binary class.

**Disposition:** retain the residual-source adapter, subject to a close
minimum-cut-lattice literature comparison. No new max-flow principle or general
belief-revision algorithm is proposed. A small explicit worked example is more
appropriate than another general solver harness at this stage.

## Prior comparison and a three-variable example

The residual-closure representation is exactly the Picard–Queyranne theorem,
not a newly discovered source language. A primary contemporary use is Georgiadis
et al., ICALP 2026, Section 4.1, Definition 20 and Proposition 21, explicitly
attributing this characterization to Theorem 1 of Picard and Queyranne (1980).
The original 1980 full text has not been read here. The elementary residual
identity above is a direct reconstruction, not a priority claim.

For a worked repair, take soft clauses a (fee 1), a=>b (fee 1), b=>c (fee 1),
and impose hard NOT c. The original soft theory has the consistent world 111.
After the intervention, minimum fee is 1 and the complete minimizer set is
{000,100,110}, writing coordinates in a,b,c order. A unit flow along
s->a->b->c->t leaves reverse implications b=>a and c=>b, with c fixed zero;
the residual hard c->t also fixes c zero. Thus the exact optimum source is
NOT c AND (b=>a). It does not force either a or b. Selecting only 100 would
incorrectly report a and NOT b as unavoidable hypothetical consequences.
For target a=>b, overwriting b with one is universally safe for these tied
repairs; merely asserting that the selected optimum already satisfies the
target would be false for 100. These are finite semantic consequences, not
measurements of physical truth or a performance benchmark.
