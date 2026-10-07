# P3-02 — initial principal derivation review

Reviewer: **ChatGPT (GPT-6 Astra Pro)**, `/root/scoring_sources`.
Same-model internal, nonblind review; no principal clock, ledger, gate,
status or publication edits. This is a snapshot review of development work.

Inspected `v3/derivations/02_probability_information.md`, SHA256
`c264905dc5fbbf7306e54ee9060cffc2d1c9a46475df49c7a67bc0878f8af0a4`.
Scope: PI-2, PI-3, PI-4 and the binary/unknown-stakes discussion, with surrounding
definitions read to check their quantifiers. No new literature search was
needed for this audit; primary comparison contracts and exact citations are
in [scoring_sources.md](scoring_sources.md).

## Verdict

**No false theorem was found in PI-2, PI-3 or PI-4.** Their restrictions to
known linear measurement semantics, a fixed law, a full simplex or explicitly
convex family, and a nonempty local fiber are doing necessary work. The proofs
establish existence against arbitrary decoders, rather than only against
affine decoders. Two small wording improvements below would prevent stronger
readings than these proofs support.

## 1. PI-2: global full-simplex recovery

The equivalence is correct for any finite target matrix `C`. If a row of `C`
is outside `rowspan(A)`, finite-dimensional duality supplies `d in ker(A)`
with `Cd != 0`; uniform interior probability permits both signs of a small
perturbation. Hence even a nonlinear exact decoder fails on two admissible
laws. Conversely `C=a 1^T+B L` is an explicit affine decoder on attainable
observations. Taking `C=I` gives the stated full-law criterion.

The affine-independence equivalence for the columns of `L` is correct. The
measurement lower bound should be read as independence **modulo constants**
(restriction to the simplex tangent space), not ordinary row independence
alone. The rank criterion already makes this unambiguous mathematically;
adding those words to the prose would be slightly clearer. A constant query
has a nonzero row but adds no probability coordinate after normalization.

The theorem appropriately makes no sample, bit, numerical-conditioning,
unknown-payoff or unrestricted scalar-encoding claim. The `n=1` case is also
covered: normalization alone identifies the sole law and zero queries suffice.

## 2. PI-3: convex restricted sources

The criterion using `V=span(P-P)` is correct for nonempty convex `P`, including
nonclosed or lower-dimensional sets. Every nonempty finite-dimensional convex
set has a relative-interior point; its relative neighborhood allows every
sufficiently small signed direction in `V`. Thus the necessity proof works
without assuming that `P` contains a full-dimensional simplex neighborhood.
For a singleton source, `V={0}`, and every linear target is indeed constant.

The `[H;L]` version is valid when `Hp=h` describes the **actual affine hull**,
equivalently `ker(H)=V`. An arbitrary list of known affine equalities is
insufficient when additional inequalities are tight throughout the source.
The draft explicitly warns about that smaller-face issue and should retain it.

**Recommended wording improvement:** make clear that convexification can alter
recovery even for a linear target `T(p)=Cp`, including `T(p)=p`. The current
final sentence mentions nonlinear targets before the broader admitted-family
qualification; that emphasis may invite an incorrect linear exception.

The existing catalogue gives a precise explanation. For
`P={e1,e2,e3}`, `L=(0,1,2)` and observation `y=1`,

\[
\operatorname{conv}\bigl(P\cap\{p:Lp=1\}\bigr)=\{e_2\},
\]

whereas

\[
\operatorname{conv}(P)\cap\{p:Lp=1\}
\supseteq\{e_2,(e_1+e_3)/2\}.
\]

Thus convexifying the source and then conditioning on the observation can
introduce ambiguity absent from the original family. Preserving unconstrained
linear extrema under convexification does not justify commuting those two
operations. This is a direct explanation of the draft's example, not an
additional novelty claim.

## 3. PI-4: local full-simplex fiber

The union support `J` is the correct support. Since there are finitely many
coordinates, a finite average of witnesses yields a feasible `p*` positive
on all of `J`. Every sufficiently small signed perturbation in `ker(A_J)`
then stays in the same nonnegative normalized fiber. This proves exactly the
displayed target-constancy criterion. The singleton criterion is its `C=I`
case, and the warning against one arbitrary feasible law's support is correct.

Keep the phrase **full-simplex fiber**. For a general restricted source, support
alone does not capture all its affine constraints, and for a nonconvex source
small two-sided perturbations need not be admitted. If the theorem is later
generalized, it must use the actual affine direction space of that fiber (for
a convex source) or the literal fiber principle. The current formulation does
not make that mistaken generalization.

Computing `J` in a rational implementation can use certified tests of whether
the maximum feasible `p_i` is positive. A numerical solution displaying a zero
coordinate is not by itself a proof that this coordinate is absent from `J`.
This is an implementation obligation, not a missing mathematical hypothesis.

## 4. Binary probabilities and nuisance parameters

The event-loss inversion and error sensitivity are correct with known,
fixed `c0,c1`; the sign of the gap is handled by the absolute value in the
error bound. Equal payoffs yield no measurement information about the event.
The `(K,p)=(10,7/10)` versus `(100,97/100)` example correctly demonstrates
confounding in an admitted family where the stake is unknown.

**Minor correction:** the sentence “A realized zero loss reports one outcome”
requires a nonzero `K` and the zero-versus-`K` loss contract without an unknown
additive offset. At `K=0`, zero loss occurs on either outcome. A precise version
is: “For `K>0` under this zero-versus-`K` contract, a realized zero loss reveals
that the event occurred; it does not recover its earlier subjective
probability.” A generic realized value should not be said to identify an
outcome when distinct states can share that value.

The shared-scale construction is correct because the event partition is
exhaustive, the same scale multiplies every coordinate, and that scale is
nonzero. The positive-scale specialization correctly licenses the inequality
direction in the rational-threshold test. The offset anchor is sufficient
when it obeys the same affine reporting transformation. It must be an exact
expectation or equally justified report under that transformation, rather
than a single noisy realized payoff; the existing section's exact-value
scope supplies this assumption.

For unrelated unknown per-event scales, normalization does not **generally**
identify `p`. This leaves constructive exceptions such as a known one-point
support. The draft's “do not obey it” is best understood as rejecting a
general decoder formula, not as asserting universal nonidentification for
every conceivable restricted nuisance family.

When later connecting these examples to the general fiber theorem, the
compatible states should include the unknown nuisance parameters explicitly,
for example `(p,s,b)` with observations `v_i=b+s p_i`; the target may still
be only `p`. The observation map is then nonlinear in the enlarged unknown
vector, so PI-1 applies directly but the fixed-known-`L` rank theorems do not
apply without an additional parametrization or proof. The draft's native
variable-division warning already recognizes the associated language issue.

## Review disposition

The central reconstruction is ready for further development and adversarial
examples. Suggested edits are limited to the convexification emphasis,
nonzero-stake realized-outcome qualification, and optional clarifications of
modulo-constant independence and explicit nuisance fibers. This review does
not establish executable correctness, final challenge status, contribution
support or completion of any gate.
