# Cost-only transcripts have a bounded-CNF representation

Contributor: **Codex (GPT-6)**. DEVELOPMENT, October 19 UTC. Connects the
invoice-observation and source-aware permission branches. This is a direct
decision-tree conversion; no new CNF inference principle is claimed.

## Exact characterization with noiseless invoices

Begin with the full n-bit cube, positive fixed coordinate prices, a private
episode cap 2<=H<=n, and a publicly known deterministic private query program.
The program may stop adaptively and never repeats a coordinate within an
episode. The public side sees only its total fee. Public choices of later
programs can depend on previous invoices.

An episode's total fee is determined after at most H-1 private answers. If
the program continues after that point, it must stop after its last allowed
query; the final answer cannot change the already determined charge. Earlier
stopping decisions use at most H-1 answers too. Replace the final private
queries by leaves labelled with their resulting fee. This produces an ordinary
decision tree of depth at most H-1 computing the invoice.

For any observed fee c, exclude each leaf labelled differently from c by
negating its path's partial assignment. The resulting CNF has clause width
at most H-1 and describes exactly the episode's compatible worlds. It has at
most 2^(H-1) clauses before simplification. Conjoin these formulae along the
observed public history. Thus a transcript of T episodes has a representation
of size O(T*H*2^H) and width at most H-1, with no world enumeration.

Conversely every consistent CNF of width at most H-1 is a possible transcript
source. To observe a clause on j<=H-1 distinct coordinates, privately query
those coordinates; stop after them if the clause is true, and otherwise buy
one distinct positive-price marker. The two exact bills differ. Conditioning
on the first bill imposes that clause. Repeat for all clauses. Redundant
episodes are permitted for this reachability statement. An empty false clause
describes an impossible transcript; tautologies require no observation.

Therefore the nonempty reachable sources are exactly the relations definable
by width-(H-1) CNF. This is input clause width, not a bound on every prime
implicate: width-three sources can have wider prime implicates. Exact pricing
is needed for the converse. A deterministic quantizer preserves the forward
width bound but can erase the two bills required by the construction.

For H=2 the compatible sets are subcubes. For H=3 they are exactly bijunctive
relations. With an initial source F, replace the characterization by F AND
the transcript CNF; an arbitrary F does not become binary merely through
three-query episodes. Publicly recorded random coins can be conditioned on;
unobserved private randomness would require a different source representation.

## Consequences and an important limitation

This lets the public reasoner keep a compact exact logical source for later
task questions or counterfactual edits instead of storing all remaining worlds.
For H=3, ordinary implication-graph inference applies. Constructing and reading
the private program, transcript clauses, propagation and optimization still
cost work; the bound can be exponential in H and no total-runtime gain is
claimed yet.

Invoice observations generally add new binary clauses, not just unit receipts.
They can create a new relation without forcing any coordinate. Consequently
the earlier fixed-source/unit-receipt cache cannot simply filter its old pair
tables by forced literals. Use source-addition transport or update the source
inference structure before claiming exactness. At H=2 the observations are
units and the distinction disappears.

The failed cubical potential's four-bit counterexample was the cube without
vertices 14 and 15: it requires NOT(x_1 AND x_2 AND x_3), which is not
bijunctive. For example, its three worlds with exactly two of x_1,x_2,x_3 set
have an excluded majority. It is therefore unreachable at cap three. That
failure rejects a universal-source proof, but does not yet reject a proof
restricted to reachable binary sources. This motivates one structural screen,
not an assertion that the potential has been rescued in all dimensions.

The subsequent [reachable probe](reachable_probe.json) finds a five-bit
binary-source counterexample, with potential 83 and Bellman right side 81.
Thus the restricted potential also fails. The transcript characterization
survives; it yields a compact inference interface independently of that failed
lower-bound application. See [binary parity](binary_parity.md) for a different
use of this representation.
