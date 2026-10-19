# A short-transcript tractability boundary

Codex (GPT-6), October 19, 2026. DEVELOPMENT consequence of
[transcript_sources.md](transcript_sources.md), not independent confirmation.

Keep its contract: 2<=H<=n, deterministic publicly specified private programs,
no repeated coordinate within an episode, positive fixed prices, exact invoices,
and a full-cube or binary-CNF initial source. Count the transcript/program input
size, including its clauses; do not hide source preparation in a query fee.

For H<=3 the compatible source is 2-CNF. Consistency, a forced bit, and every
fixed-arity projection can be computed using ordinary 2-SAT with assumptions.
For a binary target G, the local permission compiler then produces exactly all
universally safe toggle masks, or all safe independent unary maps, as a 2-CNF
formula of size O(|G|). There are at most four source assumption tests per target
clause. This is a polynomial inference/feasibility interface; maximizing a
general utility over its feasible edits need not be polynomial.

The fixed-source receipt shortcut is still inapplicable to new invoice clauses:
update the source before compiling its projections. Public random coins can be
conditioned on. A fallible initial source needs a separate adequacy contract.

At H=4, even deciding whether one bit is forced can encode UNSAT, despite a
promise that the transcript source is nonempty and despite a supplied witness.
Given 3-CNF psi with clauses (a OR b OR c), introduce g and a fresh z_C for
each clause. Replace each clause by

    (NOT g OR a OR z_C) AND (NOT z_C OR b OR c).

When g=1, eliminating z_C gives the original clause. When g=0, choosing all
z_C=0 satisfies the new formula for any assignment to the original variables.
Hence there is an explicitly available model with g=0, and the source forces
g=0 exactly when psi is unsatisfiable. Add irrelevant coordinates if needed
to supply a distinct marker for each width-three clause. By the transcript
converse, each clause is obtained from a cap-four episode whose low invoice
means that the clause holds. Their joint source is exactly this satisfiable
formula. The witness describes a possible world, not the unknown actual one.

Thus forced-bit inference is coNP-hard for these succinct transcripts. It is
in coNP because a compatible world with the opposite bit is a polynomial
witness. The same reduction makes testing whether the identity edit universally
achieves a unary target coNP-hard. This threshold concerns arbitrary allowed
transcripts, not every cap-four program or a source already expensively compiled.

The point is a useful interface design distinction: three private purchases per
episode preserve an exact, tractable logical source and binary action compiler;
one more purchase can express sources with hard universal inference. This does
not make probability inference easy at cap three, establish a complete-cost
application saving, or invent the 2-SAT/3-SAT boundary. The contribution under
consideration is the reduction connecting a priced observation interface to
those ordinary logical representations and to counterfactual permissions.

No additional exhaustive harness is planned: the explicit reduction and existing
transcript/source checks are sufficient for this discovery-stage consequence.
A future confirmation should independently check both directions of the source
characterization and the exact assumptions of the compiler.
