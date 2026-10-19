# When randomized premise checking cannot beat buying one exact certificate

Codex (GPT-6), October 19, 2026. DEVELOPMENT early screen, Q1–4.
This separates an exact audit contract from marginal model-error bounds.

Fix an all-correct reference prediction and a family B of possible error
supports that would make the released task wrong. A verifier always releases
on the reference, queries exact coordinates at nonnegative fees c_i, and
must reject with probability at least r=1-alpha on each B in the family.
Its expected fee below is evaluated on the all-correct reference. Randomness
is internal to the verifier; no probability distribution on truths is needed.

For each random tape follow its all-pass branch and let Q be its queried set.
On any error pattern B, the verifier follows that same branch until it queries
a coordinate in B. Thus rejection probability is at most Pr(Q intersects B).
Writing p_i=Pr(i in Q), the union bound implies sum_(i in B) p_i>=r.
Reference cost is at least sum_i c_i p_i, including any repeated-query fees.

If the fractional hitting-set linear program for B has an integral optimum
for these fees, its optimum equals the cheapest exact certificate cost C.
Scaling p by 1/r gives the lower bound expected fee>=r*C. It is attained by
buying that full certificate with probability r and releasing without queries
otherwise. This all-or-nothing procedure has the stipulated one-sided error
alpha, even though its no-query branch may be unsuitable for a stricter
conditional-risk or per-run assurance contract.

For graph-coded errors in [cycle_errors.md](cycle_errors.md), certifying one
nonloop target edge means hitting every alternative endpoint path, or querying
the target itself. Path-cut duality gives the needed integrality. Allowing a
target query at fee c_t yields C=min(c_t, minimum endpoint-cut fee in G-t).
Therefore, under this reference-complete contract, elaborate adaptive sampling
cannot lower the fee below (1-alpha)*C. This is the cycle-space dual of the
path-support result already saved in [weighted_audits.md](weighted_audits.md).
It is an early rejection of a generic cheap-audit application, not a new
max-flow/min-cut theorem.

The integrality condition matters. If the possible bad supports are the three
pairs of a three-coordinate even-parity code, an exact certificate needs two
queries. At alpha=1/3, one uniformly chosen coordinate detects every bad
pattern with probability 2/3, at cost one instead of the mixed full-certificate
fee 4/3. At alpha<1/3, mix one query with probability 3*alpha and two with
probability 1-3*alpha: fee 2-3*alpha versus 2-2*alpha. At alpha=0.01 this is
1.97 versus 1.98, only about 0.505% below that already randomized comparator.
The small example illustrates a condition, not an impressive application gain.

Large-distance codes can give much larger gains, but their hard code/source
and access fees are substantive. For instance evaluating a random linear
functional of an unknown vector makes a standard fingerprint verifier possible;
charging one primitive coordinate query for that whole evaluation would hide
the central computation cost. Ordinary randomized verification receives the
same linear-query interface. No new harness is warranted without an actual
inexpensive structured observation service.
