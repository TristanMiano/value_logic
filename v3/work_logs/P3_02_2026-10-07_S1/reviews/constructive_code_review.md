# P3-02 — constructive certificate code review

Contributor: **ChatGPT (GPT-6 Astra Pro)**, delegated reviewer
**/root/scoring_sources**, October 7, 2026 UTC. Same-model internal,
nonblind **static** development review.

The reviewed modules were read as text. This reviewer did not import,
execute or modify either module, run a test, inspect the older checks,
change any ledger or support status, or attempt a gate. Mathematical
examples below are hand derivations, not reported execution results.
The companion remains a P3-02 finite-information development interface,
not a learner or a start on P3-08.

## 1. Exact reviewed snapshots

| File/version | SHA-256 | Coverage |
|---|---|---|
| Initial v3/checks/02_finite_information_audit.py | f936378a58441a0079f5d3495daa4df57491b4d6d94b750e5496be6133849453 | Input handling, exact row algebra, collisions, target and repair certificates, CLI preservation |
| Added full-law/repair certificate version | 3ec443730da479b39ae40a0e2c6ab43087f2a795d8ea3cb5c4a31ce895523366 | Full-law coordinate evidence and repaired-target evidence |
| Final reviewed v3/checks/02_finite_information_audit.py | 546a4b12df2348d284582de7e48e19378bd8a5fbc3ea191b9190605aaa9879b0 | Previous logic plus exclusive output creation and optional CPU counters |
| v3/checks/02_finite_information_verify.py | 9b1e2822a867f934fbbaa4b6b7fb1230ad69cbf9458565da1b3bf418e7d3f1f1 | Added targeted review of arithmetic-certificate soundness |

**Finding:** no remaining arithmetic or certificate-soundness defect was
found in these final reviewed bytes. Two operational issues identified in
the earlier generator are visibly addressed. This is a static finding,
not a claim that execution or an independent test harness has passed.
The separate mathematical review of the repair-count theorem remains its
own evidence; this review checks how its premises and certificates are
implemented.

## 2. Issues identified and resolved before execution

### Output preservation

The initial CLI checked whether the output existed before doing the audit,
then used a truncating text write afterward. Another process could create
the same output during the intervening computation, defeating the stated
refusal to overwrite an existing result.

The final reviewed version creates the output with exclusive mode
“x” at the actual write. The earlier existence check remains a useful
early refusal; exclusive creation is the operation that prevents replacing
a concurrently created path. The fix is appropriate.

### Optional CPU counters

The initial unconditional resource import limited execution to platforms
providing that module. The final version handles its absence and records
null CPU counters while retaining observed UTC and monotonic execution
fields. Static inspection confirms that neither the missing-module branch
nor its result construction dereferences a missing usage object.

No portability run was performed. The change removes the identified
unconditional-import limitation; it is not a tested claim about every
platform or an end-to-end resource guarantee.

## 3. Generator: exact algebra and input scope

### Input contract

The public audit path requires a JSON-object-shaped request, a positive
integer state count, a named calibration contract, and matrices of the
declared width. Unknown request fields are rejected. Matrix entries accept
integers and strings parsed as exact finite rationals; binary floats and
Booleans are rejected. A decimal supplied as a string is an exact rational
input rather than a binary floating-point observation.

Empty loss menus, empty target menus, redundant rows, zero rows and the
one-state case have meaningful branches. The default target is the identity
matrix. All parsed matrix entries reach the algebra as Fractions, so the
generator's division operations in row reduction remain rational along this
supported path.

The tool does not accept observed values or infer their semantic type.
It characterizes the observation map over the full simplex, given known
statewise rows and one of the four declared shared-calibration models.
Known calibration components have already been removed. Restricted
probability families, bounded nuisance ranges, differently transformed
future queries, unavailable row menus and native unit eligibility remain
outside this interface.

### Row operations and coefficients

The reduced-row routine retains pivot rows first and allows zero or
redundant trailing rows. Its nullspace construction sets each free
coordinate in turn and solves the pivot coordinates exactly.

The coefficient routine solves the transposed row-span system. A pivot
in its appended target column detects inconsistency; otherwise setting
free coefficient variables to zero gives a valid representation. Its
empty-row behavior is also appropriate: only the zero target has an
empty representation.

The repair code uses this routine on a second transpose to obtain
directions \(h_j\) satisfying
\[
B h_j=0,\qquad Q_i h_j=\delta_{ij}.
\]
The dimensions match: the coefficient vector returned by that call has
one entry per state, rather than one entry per source row. Redundant old
rows impose consistent zero right-hand sides and do not invalidate the
construction.

### Positive target and full-law evidence

For known scale, the supplied coefficients prove
\[
c=\alpha\mathbf1^\top+\beta M,
\]
where \(M=L\) or the differences from one retained reference row,
depending on whether the offset is unknown.

For unknown positive scale, the certificate proves both
\[
uM=\mathbf1^\top,\qquad wM=c.
\]
The corresponding observed linear forms are \(s\) and \(s\,cp\).
Their ratio is justified by the shared positive-scale premise.
Constant targets correctly bypass calibration altogether.

The added full-law certificate supplies either a decoder for every
coordinate or an actual collision separating one coordinate. This makes
the full-law verdict independently checkable without trusting the reported
rank. The repaired-target certificates similarly establish the sufficiency
of the proposed enlarged menu.

## 4. Collision construction and completeness

For known scale, the hidden basis annihilates both the effective loss rows
and normalization. A nonrecoverable target must be nonzero on at least one
basis direction. The uniform interior law is sufficient in this branch.

For unknown scale, a hidden direction need not sum to zero. The relevant
change in a normalized target is
\[
ch-(\mathbf1^\top h)cp.
\]
If the direction has zero total, any nonzero value works at the uniform
law. If its total is nonzero, this expression cannot vanish at every law
in the generator's candidate bank for a nonconstant target: the uniform
law and its midpoint mixtures with every vertex affinely span the simplex.
Thus the finite bank resolves an exceptional uniform choice.

For a selected law and direction, the step
\[
\tau=\frac{\min_i p_i}{2\max_i|h_i|}
\]
is positive because a nullspace basis vector is nonzero. It gives
\(x=p+\tau h>0\). Put \(T=\mathbf1^\top x>0\),
\(q=x/T\), and, when scale is unknown, \(s_q=T\). These are interior
normalized laws with positive admissible scales. The target-separation
test is exactly the numerator of the normalized target difference.

When an offset is unknown, the new offset matches the reference row.
Annihilation of every other row's difference then matches the complete
record. If the old menu is empty there is no reference constraint to match,
and the zero offset is a valid witness. The implementation recalculates
both records and both target values before returning the witness.

### A useful hand-derived hostile fixture

For two states, let
\[
L=\begin{bmatrix}1&0\\0&1\end{bmatrix},\quad
c=(1,0),
\]
with both common scale and offset unknown. The effective hidden direction
\(h=(1,1)\) produces no normalized change at the uniform law.
The next interior candidate does:
\[
p=(3/4,1/4),\quad q=(7/10,3/10),\quad
s_p=1,\quad s_q=5/4,\quad b_p=0,\quad b_q=-1/8.
\]
Both records are \((3/4,1/4)\), but the target is respectively \(3/4\)
and \(7/10\). This is a useful harness case for the candidate-bank branch;
the reviewer did not execute it.

## 5. Repair construction and minimality evidence

The generator's base is \(M\) for unknown scale and
\([\mathbf1^\top;M]\) for known scale. If at least one target is nonconstant,
its required rows are \([\mathbf1^\top;C]\) in the unknown-scale contracts
and \(C\) otherwise. The constant-only and empty-target branches correctly
require zero repair even when other law information is absent.

The selected rows \(Q\) are required rows that successively increase rank
modulo the old base. Their hidden-direction identity pairing certifies
independence modulo that base. The pairing supplies a checkable lower
dimension requirement without requiring the verifier to reproduce rank
elimination.

With an existing unknown-offset reference \(\ell_0\), the proposed raw
queries are \(\ell_0+Q_i\), so differencing against its old observed value
gives the intended effective rows. With no old row and an unknown offset,
the code first adds the zero-loss reference and then the selected rows.
That one additional raw query is appropriate because \(k\) raw values with
an unrestricted common offset supply at most \(k-1\) effective differences.
All added queries explicitly share the original law and nuisance parameters.

For example, an empty old menu and one nonconstant binary target require
respectively \(1,2,2,3\) additional raw queries in the known,
unknown-offset, unknown-scale and unknown-affine contracts. Those are
mathematical implications of the stated free-row model, not run results.
A preexisting zero-loss row is already a reference and must not be charged
again; the implementation makes that distinction.

These are minima for freely selected fixed rational loss queries.
They are not minima for a restricted menu, decision-only service,
nonlinear or adaptive observation interface, or actual acquisition cost.

## 6. Independent verifier: acceptance and boundaries

The verifier imports neither the generator nor a row-reduction routine.
Its scientific checks have the following direct content:

| Claim | Arithmetic checked |
|---|---|
| Effective observation matrix | Reconstructed from the declared losses and offset contract |
| Positive target recovery | Exact constant, affine-row or normalizer/numerator identities |
| Negative target recovery | Interior normalized laws, allowed positive scales and offsets, equal recalculated records, distinct recalculated target values |
| Full-law recovery or failure | Every coordinate decoder, or one verified separating-coordinate collision |
| Repair lower dimension | Selected rows belong to the required family; directions annihilate the old base and pair as the identity with selected rows |
| Raw repair implementation | Added rows exactly implement those effective rows, including the reference when required |
| Repair sufficiency | Every requested target has a verified positive certificate for the enlarged menu |
| Summary recovery verdicts | Boolean verdicts agree with the checked target/full-law evidence |

The pairing condition prevents duplicated or irrelevant rows from inflating
the certified minimum: required-row membership and independence modulo old
information are both checked. The repaired-target identities ensure the
chosen rows actually suffice, rather than proving only a lower bound.
The unknown-scale nonconstant-target exception and unknown-offset
reference count are retained in these checks.

No arithmetic route to acceptance of a false scientific verdict was found
within this declared full-simplex format. Malformed structures may fail
with ordinary Python exceptions rather than the custom certificate exception;
that is an error-reporting limitation, not acceptance of a false proof.

### What “verified” does not certify

Acceptance is relative to the problem contained in the record. It does not
authenticate that problem against a separate original input, prove semantic
payoff or sampling premises, or verify execution provenance. The reported
summary ranks are expressly outside its independent checks. Auxiliary
collision construction fields such as the hidden direction and step are
also not checked; the actual laws, observations and separated targets are
the negative certificate.

A harness comparing a generated result with a particular input should
therefore bind the declared state count, loss rows, targets and calibration
to that input separately. Script hashes, timestamps, CPU counters and
other descriptive metadata need their own provenance checks if relied on.
None of these limitations undermines the directly checked arithmetic
statements, and none turns this verifier into the inherited native proof
checker.

## 7. Review disposition

The final reviewed generator and verifier are ready for the principal's
separate development execution and independent harness assessment at
these hashes. This statement grants no frozen-challenge status, empirical
learning evidence, resource comparison, contribution support or gate pass.
Changes after the recorded hashes are not covered by this static review.
