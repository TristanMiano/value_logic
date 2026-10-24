# Review of the existing rational checker against N16-C/v1

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; same-model review.
The preserved implementation is [s16/block_check.py](../s16/block_check.py),
SHA-256 ce818e6154059b8c7f6ef64f0819f6d22afe1b41baffcdf65e5e8bd32515e6b4.
This review does not replace historical code or turn finite tests into proof.

## Acceptance argument

After exact type, shape and rational parsing checks, the verifier establishes
0<C_minus<=C_plus<I by checking C_minus positive definite, I-C_plus positive
definite and C_plus-C_minus positive semidefinite. Each positivity check also
checks symmetry. These three premises imply all the other needed orders.
The task weight is symmetric PSD with trace one. Thus the implemented target
includes the core's rank-one weight, but also valid non-sharp weighted means.

The Schur routine is justified inductively. A negative diagonal excludes PSD.
For a zero diagonal, PSD forces every entry in that row to vanish: a nonzero
off-diagonal gives a negative two-by-two principal determinant. Removing the
zero row and column therefore preserves equivalence. For a positive pivot,
congruence reduces positivity to positivity of the Schur complement. Strict
positivity excludes every zero pivot. The code updates only the trailing
submatrix; leaving an already eliminated column in memory does not alter
future pivots or Schur updates.

Gaussian elimination on [A,I] preserves the equation A*A_inverse=I, provided
each chosen pivot is nonzero. Row exchanges and row operations are exact.
The code's denominator matrices have already passed positive definiteness,
so singularity should not occur on an accepted input. The additional runtime
check rejects it rather than guessing an inverse. Fraction arithmetic uses
unbounded Python integers; no floating point participates in a verdict.

For E>0 the exact inequalities t>0 and t^2>=E(1+t) imply d=t-E-E/t>=0.
The [proof](proof.md), equations (3)-(6), then yields the two matrix orders
for truthful external compression and edit premises. If A<=B and V>=0,
tr(VA)<=tr(VB), since tr(V(B-A)) equals the trace of a PSD congruence.
Consequently the trace calculation remains sound even when V does not
commute with a bound. The final scalar target lies in [0,1], justifying
intersection with that interval. This is not matrix eigenvalue clipping.
For E=0, the edit is zero and the direct trace of the supplied brackets is
valid. Equality with either threshold endpoint correctly yields abstention.

These steps supply a readable code-to-mathematics argument. They do not
verify Python, its runtime, the host hardware, or the physical premises.

## Focused independent arithmetic checks

[checker_audit.py](checker_audit.py) uses cofactor determinants, principal
minors and adjugate inverses instead of the checker's Schur and Gaussian
helpers. Its [record](checker_audit_result.json) preserves executed hashes,
runtime and exact values. The run passed 1,460 PSD/PD comparisons, including
zero pivots created after elimination; these are finite regression checks.

A rational 3-by-2 source with a two-dimensional retained subspace exercises
a case omitted from the old probe's n>p branch. Its full resolvent has an
eigenvalue one, while the compressed C is strictly interior as required.
Both rational bracket errors are positive definite and fail to commute
with C. A rank-one edit of exactly norm 1/10 produces the separately
computed target value 16900/56439, inside the verified interval. A rational
orthogonal basis change preserves the bounds after transforming V too.

Other checks cover strict threshold boundaries, E=0, dimension 16, a dense
rank-one task weight and six malformed mathematical inputs. Changing only
the source label leaves the bound unchanged, as the conditional contract
requires. No test failed; no hardware explanation or retry was needed.

## Interface and resource limits

The algorithm checks a supplied mathematical object. Its returned JSON is
not a self-authenticating attestation: it omits the full input, edit budget,
task weight and an input digest. Preserve the input and checker hash with
any decision record. The repository evidence manifest can bind those bytes;
the source_id field cannot establish their external truth.

The CLI checks file size before reading, accepts JSON's normal duplicate-key
semantics, and does not translate every decoding or recursion error into a
structured INVALID response. A concurrent file replacement can also defeat
the stat-then-read size check. These are deployment/interface limitations,
not demonstrated false mathematical verdicts. The bounded contribution is
about a successfully parsed, supplied certificate and exact computation;
it makes no hostile-service, concurrent-file or uniform response-time claim.
Any later service wrapper should specify and enforce those stronger duties.

Dimensions, raw digit counts and normalized rational bit lengths are bounded.
Elimination has a finite number of exact operations, but intermediate
fractions and their cost can grow. Neither the input cap nor the recorded
118,962,300 ns audit runtime is a general checking-cost guarantee. Checking
and acquisition remain charged work in a complete decision comparison.

No implementation change is necessary for the bounded conditional claim
based on this review. Independent reconstruction remains a confirmation
duty; an expanded trusted-input or service claim would require new work.
# Late large-input finding and versioned repair

The later [format review](format_limits.md) found a valid-input output
serialization failure in the original checker. Its arithmetic did not
produce a false approval; Python rejected conversion of the resulting
large integer to decimal text. [v2](block_check_v2.py) repairs only that
serialization, with [targeted regression evidence](format_repair_result.json).
The historical checker and its executed evidence are preserved. The same
review proves that some premises within4096 bits require an upper witness
beyond that cap, making fixed-format incompleteness concrete.
