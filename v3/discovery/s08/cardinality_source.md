# A compact original-CNF source for the uniform-matroid duty

**Prospective DEVELOPMENT — Codex (GPT-6), October14,2026 UTC.**

mc01 uses an exponential forbidden-assignment diagnostic. A compact source
for uniform bases can instead enforce exactly r selected literals using
prefix counters. For each copy introduce x_i and y_ij, where y_ij means
at least j of the first i literals are selected. Fix y_i0=true and
y_0j=false for j>0. For i>=1 and j>=1 encode

```math
y_{ij}\leftrightarrow y_{i-1,j}\lor(x_i\land y_{i-1,j-1}).
```

Writing y,a,x,b for the four literals, the clauses are
(-a or y),(-x or -b or y),(-y or a or x),(-y or a or b).
Truth-table verification establishes exactly that Boolean equivalence.
Induction on i gives every counter's intended meaning; impose y_nr and
not y_n,r+1 to obtain exactly r selections. Include j through r+1.
Conversely any r-subset extends uniquely to the counter assignment, so
the auxiliary variables neither remove nor add projected basis choices.
This is a standard sequential-cardinality encoding construction, not a
new SAT encoding or a procedure to infer structure from arbitrary CNF.

Copy that source m=n times, charging x_i in every copy to the same public
cost coordinate i. Add one mandatory anchor literal h using (x_1 or h)
and (-x_1 or h), with feature(-h). A selected x_i has feature(-x_i).
The cyclic consecutive-r bases give coefficient r on every coordinate,
so their robust regret is Hr(n-r). Every upper-minimum basis selects the
r smallest admitted upper endpoints. It can be extended into a complete
original Boolean action by the prefix-count rule.

The source has O(mnr) clauses/auxiliaries and complete exported models
still contain them. Persistently admitting this schema might avoid
rechecking every clause on every request, but that service and its invoice
are not assumed here. A generic arbitrary-CNF recognizer remains open.

**Prospective mc02 encoding screen:** JavaScript implementation, n4,8,16,32,
r=n/2,m=n,H=2. Verify the gate truth table and, for n<=8, every projected
assignment plus all single-auxiliary flips of one accepted extension.
Build and save the full original source, two complete hex-encoded Boolean
actions (cyclic fallback and repeated upper-minimum basis), and their
source hashes. Check every original clause and feature coefficient.
Use a declared deterministic partially observed vector for the upper
example; these are free mathematical inputs, not actual cost receipts.
Reject altered cardinalities, flipped action bits and changed-source
certificates. Record sizes and deterministic check counts. No physical
query, actual resolution acquisition or complete SAT call is claimed.
