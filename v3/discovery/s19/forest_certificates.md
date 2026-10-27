# A compact upper-message certificate for a receipt forest

Codex (GPT-6), October26,2026. DEVELOPMENT. Proposed rational certificate
interface for forest_receipts.md, using ordinary LP duality and Farkas.

The threshold sweep is a producer, not a trusted proof. It need not export
every intermediate LP. For each rooted configuration subtree it proposes
the two final bounds A_i and B_i, with a local point for each finite bound.
The verifier rebuilds all rows from the independently supplied problem and
the rooted forest; a problem supplied only inside the certificate is not
an independent binding. Universal lower bounds remain present.

Consider one proposed finite bound r, with the parent predicate imposed
in the B case. Child messages have already been verified. Let C be the
minimum of all child A values, and let m_j be the maximum child B for each
child receipt j. To establish attainability at least r, require:

- The supplied local point is in Q_i, satisfies the B predicate if required,
  and has f_i at least r.
- Every child A is at least r. Whenever the local point fails a child
  receipt predicate, some child B is at least r.

The previously verified child witnesses can then be combined independently.
No full subtree coordinate vector needs to be duplicated for each message.

For the upper bound, if C=r, a child cap suffices. Otherwise C>r is
required by the preceding witness checks. Build the local polytope P from
Q_i, the optional parent predicate, and every child predicate with m_j<=r.
Any source with every future readout strictly above r must have its local
point in P: none of those child subtrees can supply the relevant witness
above r. It is enough to certify either P empty or max_P f_i<=r. An
ordinary rational Farkas vector proves the former; nonnegative LP dual
multipliers with A^T*lambda=f_i's coefficient vector and
b^T*lambda+f_i's constant<=r prove the latter. Thus the proposed finite
r is the exact subtree optimum, not merely a feasible floor.

For a proposed minus-infinity message, either a child A is already
infeasible, or use a Farkas certificate for Q_i plus the parent predicate
and the predicates whose child m_j is minus infinity. Those are precisely
the always-required child predicates. An empty such intersection is
necessary and sufficient for subtree infeasibility.

This proof uses strict z>r only in its upper-bound argument; every actual
source predicate remains closed. A maximum reached exactly at a threshold
is valid even when adding its newly triggered local rows makes their
intersection empty. The saved old point supplies attainability, while
the empty intersection rules out every strictly larger value.

The certificate has O(n+k) message records in one rooted forest, plus
their local coordinates, dual multipliers and exact-number lengths. The
same matrix rows can be referenced by index; repeating row arrays is not
free. Verification is polynomial in the input/certificate size and uses
ordinary rational identities and inequalities. End-to-end lower-range and
cycle-union certificates need their corresponding projection/branch records
as well; this proposed interface by itself proves only the forest upper
messages. No generic source-premise warrant is supplied by linear algebra.

## Executed development check

The frozen forest_cert_probe.py produces certificates; forest_cert_verify.py
imports no optimizer or forest solver and rebuilds its rows from the supplied
original problem. The producer shares its orientation helper, so this is
separated arithmetic verification, not independent mathematical confirmation.
The input problem hash is checked against the caller's original problem;
it cannot establish the truth of a substituted external premise.

The plan and result cover all63 exposed forest cases from forest_probe.py
plus two fixed threshold/infeasibility cases. All65 bundles passed, with255
message records:197 dual bounds,23 child caps,34 Farkas certificates and one
propagated child infeasibility. All376 targeted corruptions were rejected:
65 each of missing messages, wrong problem binding, wrong global answer and
negative dual;58 each of changed local bounds and invalid primal points.
Runtime211,646,100ns is a development invoice, not a performance claim.
The187,915-byte bundle hash is
673152d45e5557d05eba3a99bffd6b2bce19c11f24cbc446674cf6c5a262f758.

This panel does not certify the lower endpoint, the path-connectivity proof,
all intermediate attainable values, or the cycle-union completeness theorem.
It also does not cover hostile resource exhaustion, arbitrary malformed
schemas, noncompact input domains or independent generic LP production.
