# P3-11-A1: certificate and source-service audit

Codex (GPT-6), October 28, 2026. Same-model confirmation of the frozen
`s19/range_cert_verify.py` and `s20/range_service.py`. This is a source-level
argument, supported by exposed development tests, not a claim that those
Python programs have been machine verified.

## Reconstructed constraint and certificate contract

For block i and mask T the checker starts with the caller's original
A_i x <= b_i. For every receipt it appends -h_ji x <= d_ji-a_j.
For j in T it additionally appends h_ji x <= b_j-d_ji. These are exactly
Q_i(T), including affine offsets and all receipt lower bounds. Row lengths,
right-hand-side lengths, objective dimension and receipt form counts are
checked. The source dimension must be positive. Every numeric coefficient,
endpoint, point and multiplier is parsed from a string into Fraction;
floating-point inputs are not silently rounded into exact data.

For a bounded entry, both supplied points must satisfy every rebuilt row.
Their objective values must equal the supplied lo and hi, with lo <= hi.
The low multiplier is nonnegative and satisfies lambda*A=-c; hence
f(x) >= d-lambda*b = lo for every feasible x. The high multiplier satisfies
mu*A=c and is nonnegative; hence f(x) <= d+mu*b = hi. Matching feasible
points establish attainment at both ends. Convexity then supplies every
intermediate value. No complementary-slackness or solver-status assertion
is trusted in place of these identities.

For an empty entry, nonnegative lambda obeys lambda*A=0 and lambda*b<0.
Any feasible x would imply 0=lambda*A*x <= lambda*b<0, a contradiction.
A false empty slice therefore cannot be accepted merely because a numerical
solver failed. Each block must supply exactly 2^k indexed entries. Unknown
entry kinds, missing entries and extra entry fields are rejected. The check
never infers infeasibility from an omitted table key until a complete local
certificate has justified that omission.

The top-level problem and certificate fields are fixed. Nested generator/form
objects may contain unused extra metadata; the checker does not advertise a
strict schema for every nested field. Such metadata does not alter the
reconstructed mathematical constraints. This is an ordinary JSON-like data
interface, not a sandbox against custom Python objects or resource exhaustion.
Invalid inputs may raise ordinary Python exceptions rather than one uniform
error class. Neither distinction permits an accepted false mathematical claim.

The SHA256 binds the certificate to a canonical serialization of the supplied
problem object (sorted keys, compact separators). It is not a signature,
proof of data provenance, or authentication of the modeling premises. A caller
can change both a model and its digest; the new certificate must still pass
against that new model. The scientific statement remains conditional.

## Range reconstruction, absence and infinity

The verifier's `advance` enumerates all submasks T of S exactly once, beginning
at S and using (T-1)&S until zero. Since T is a submask, S xor T is precisely
S minus T. An available candidate is min(previous[S minus T], u_i(T));
maximizing it implements the reviewed recurrence. Missing keys mean no
feasible partition, not a scalar value of zero. The empty prefix/suffix has
only the empty-mask entry, with positive infinity as the neutral bottleneck.

The implementation uses float infinities only as sentinels; every finite
value is a Fraction. Inspection of the installed Python 3.13 Fraction
comparison implementation shows that comparisons with infinite floats take
an explicit infinity branch and do not convert a huge rational to float.
The 400-digit development fixture is supporting evidence, not the reason
for this source-level conclusion. Negative infinity denotes an unavailable
candidate during a scan and is never a feasible endpoint. For n=1,k=0,
positive infinity clips away against the finite local upper value, as needed.
For n=1,k>0, only an anchor assigned all receipts has an available outside.

Prefix and suffix tables are combined over complementary outside submasks.
The checker emits precisely the nonempty anchored intervals and merges
sorted overlapping or touching closed intervals. Equality at a shared
endpoint is handled as intersection. The separately supplied range list
must already be normalized and equal this recomputation. A correct local
certificate cannot excuse a false, omitted or enlarged global component.
If no anchor interval survives, the finite branch union is empty.

## Compiled service and rational witness recovery

The service deep-copies the caller's problem and certificate before invoking
the verifier. Later mutation of the caller's objects does not alter that
snapshot. Direct mutation of service attributes (including the public digest
label) is outside its query API contract; Python privacy is not a security
boundary. A fresh return value
from `ranges()` cannot mutate the retained tuple of rational endpoints.

The service uses `None` for positive infinity and absent keys for infeasibility.
Its `smaller` and `greater` operations implement min and strict greater-than
on rationals extended by this sentinel. A first available candidate is saved
even when it is infinite. Ties retain an existing maximizing split, which is
sufficient for producing one witness. Each prefix choice records the subset
assigned to its last block; each suffix choice records the subset assigned
to its first block. Walking those choices removes disjoint subsets and ends
at the empty mask. The anchor's mask and the two outside masks together
partition all receipts. No requirement that exactly one block actually
attain an old minimum is imposed; the assignment chooses a witness, allowing ties.

Every stored outside local maximum is at least the anchor's clipping cap,
and that cap is at least an accepted q. The anchor uses its low point if
lo=hi; otherwise it interpolates with coefficient (q-lo)/(hi-lo) in [0,1].
The resulting anchor value is exactly q, all other values are at least q,
and every selected local point satisfies the receipt assignments. Thus the
returned product source satisfies all original observations and has future
minimum q. Rational endpoint certificates and a rational query yield a
rational source. Output coordinates and their exact arithmetic are charged.

The interval stabbing index sorts anchor lower endpoints and saves the
largest upper endpoint in each prefix. After the final lower endpoint <=q,
that prefix maximum contains q exactly when any anchor does. The interval
band query uses the first merged interval whose upper endpoint is >= the
band's lower endpoint; it intersects iff its lower endpoint is <= the band's
upper endpoint. Closed endpoints, empty ranges and exterior bands follow
from the same comparison. For an intersecting band it returns an attainable
q; obtaining a full source is a separate `source(q)` operation.

Before exposing queries the service also checks that the union of its
reconstructed anchors equals the verifier's answer. This detects disagreement
between the two implementations, but is not independent evidence for a
shared erroneous theorem. The mathematical reconstruction supplies that link.

## Evidence and disposition of this unit

The exposed s20 audit checked 143 bounded and 24 empty local certificates,
37 original-model sources and 114 deliberate certificate mutations. The
service panel checked 61 attainable sources, 28 rejected values and 178 band
queries, including degenerate slices, no receipts, one block, inconsistency
and mixed dimensions. They passed on their first frozen executions. These
are development fixtures and targeted falsification attempts, not held-out
reliability statistics or a calibrated correctness probability.

No soundness defect was found in the frozen checker or service. The numerical
LP proposal generator is deliberately fail-closed but is not proved to produce
a certificate for every admissible rational instance. The abstract algorithm
uses exact rational LP; the Python acceptance service guarantees sound output
conditional on a complete certificate passing. Base compactness and the
source-model interpretation are premises, not quantities inferred from this
checker. This unit supports the fixed claim with those already stated limits;
it does not complete the whole confirmation or establish novelty.
