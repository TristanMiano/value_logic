# F17 core_v1 reader and mathematical review

Reviewer: **ChatGPT (GPT-6 Astra Pro)**; separately assigned same-model internal
review, October 6, 2026 UTC. The reviewer prepared the earlier mathematical
source map and therefore had prior familiarity. This is not a blind review or
external peer review. The source map was not consulted during the first
reader-facing reconstruction below.

Fixed draft: `v2/work_logs/F17_2026-10-06_S1/drafts/core_v1.md`,
37,342 bytes, SHA256
`768ba568517f21fe8996c3456dbcd7465bd05c0ef74d7b6d968163d3437efae1`.
Scope: §§2–7; the explicit temporary abstract/introduction markers are excluded.
No manuscript, scientific source, kernel, ledger or experimental output is
changed by this review. Principal concurrent credit: **zero**.

## 1. First pass: route reconstructed from the fixed paper alone

The reader first sees why a single evaluated mean is insufficient for some
later nonlinear questions, followed by four semantic choices. The selected
typed CPWA core retains shared uncertain quantities and proves signed relative
loss comparisons. An independent action/observation interface prevents numerical
minima from becoming unavailable policies.

The rule table explains how signed comparison budgets compose and how source
identity enables cancellation. Revision changes the premises or their allowance
functions, rather than giving unconditional authority to a stored number.
Theorem 1 then validates the current request through normalization, local rules,
finite derivations and receiving checks. Theorem 2 characterizes exactly which
source rows can reach the query unit; it supplies a constructive converse and
a concrete one-way-conversion obstruction to unrestricted completeness.

The Boolean and phase-one sections give precise interfaces rather than turn
every loss into truth. The application then specializes to fixed reset outcomes:
Theorem 3 computes price-family ranks, Theorem 4 fills an old summary's missing
directions using actual new means, and §7.3 separates exact information from
bounded error/regret. Theorem 5 is the main further mathematical consequence:
on full exact equal-price fibers, one explicitly compatible law attains the
unrestricted common minimax radius. Its envelope inequalities are visibly the
substantive lemma, with a complete linked derivation and adverse boundaries.

This is a coherent route. The reader can reconstruct what is mathematical,
conditional, a source contract, or a computational limitation without knowing
the task chronology.

### Places where the first-pass reader must guess

1. Theorem 4 invokes a “canonical summary associated with this chain” and
   “retained residuals” before defining either. A quotient-space argument could
   fill the gap, but the displayed triangular reconstruction is not immediately
   reproducible from the report alone.
2. The final paragraph of Theorem 3 does not name which null space supplies the
   lower-bound perturbation. Its “surviving null directions” follow a calculation
   of the query map's own kernel, while the following sentence needs a direction
   killed by a proposed retained map but visible to the query map.
3. Theorem 5's invocation of all proper prefixes after equation (14) leaves the
   reader to distinguish all-order prefixes from prefixes before one fixed
   edited procedure. The conclusion is plausible because the uncertain part
   depends only on prefix size, but that is the bridge the proof should state.
4. Theorem 5 implicitly continues the preceding R>0 branch; saying so in its
   first sentence would remove any ambiguity about mu when R=0.

## 2. Source-comparison pass

**Disposition: all five mathematical statements match accepted results at their
intended scope. Three local proof clarifications and the short explicit-domain
clarifications below should be made before this draft is treated as the final
report. No new experiment, rule change or scientific recurrence is indicated.**

The first-pass reconstruction and reader gaps above were written before
reopening the accepted derivations. The subsequent comparison found:

| Draft component | Accepted source and result | Assessment |
|---|---|---|
| Theorem 1, §§3–4 premises and rules | F05 §§2–6; F06 §§1–4; F07 consolidated acceptance §§1–3 | MATCH. Signed orientation, finite pointwise values, nonempty cases, lexical normalization, all sixteen tags, local/global scope, current literal request and extra-field reception are retained. |
| Theorem 2 and one-way-conversion example | F08 U1/U4/U7/U8 and the acceptance reconstruction | MATCH. Reduct rather than full-source completeness, rational attainment, common literal pair, positive directed conversions and mathematical existence rather than capped search are explicit. The reduct countermodel is not presented as a full-source countermodel. |
| Theorem 3, all rank-table entries | C4 §§2–4 / C4-T1 | MATCH. Positive prices, nonproportionality, full simplex, terminal-penalty cases, numerical values versus within/cross-profile differences and exact-linear information scope agree. Its last proof paragraph needs the null-space clarification in M1. |
| Theorem 4 | C4 §5 / C4-T2 | MATCH. The old minimum-rank exact summary, M>0, unchanged outcome law, admissible nonzero one-price edit, actual new means and deterministic adaptive lower bound agree. The constructive paragraph needs M2's definitions. |
| Theorem 5 and formulas (16)–(20) | C4 §11 canonical summary; F16-C1 §§1–8 | MATCH. Full exact equal-price fibers, fixed M, nonexchangeable residues, one compatible law, shared maximum error, explicit decoder and the substantive envelope inequalities are correctly separated. M3 makes the fixed-edited-coordinate bridge explicit. |
| Adverse midpoint/source examples | C4 §11 and dated F16-R01; F16 §§9–11 | MATCH. The k4 midpoint failure is retained without incorrectly inferring a common-radius premium. The k3 correction and source-dependent triangle premium remain correctly scoped. |

### M1 — name the retained-map kernel in the information lower bound

**Location:** Theorem 3's final proof paragraph, draft lines 609–613.
**Type:** required local proof precision; theorem statement unchanged.

The just-computed “surviving null directions” are directions in the requested
query map's kernel. They give equal requested values, so they cannot themselves
justify the next sentence about *different* requested values. The intended rank
argument needs a proposed smaller retained map.

**Minimal repair:** Name Q as the requested linear map and T as a candidate
retained map on the simplex direction space. If rank(T)<rank(Q), choose
`v in ker(T) \ ker(Q)`. Small opposite perturbations of an interior law then
have identical retained data and different Q-values, excluding every decoder.
This is the standard rank lower-bound step already used in the accepted source;
it introduces no stronger result.

### M2 — define the chain size and canonical residuals used by repair

**Location:** Theorem 4 proof, draft lines 630–648.
**Type:** required constructive-presentation clarification; theorem unchanged.

Nested sets alone do not state `|P_r|=r`; for example an empty first prefix
would give the constant m_empty rather than a missing independent moment.
The proof also uses an undefined canonical summary and retained residuals.

**Minimal repair:** Choose a reference order with j last and let P_r be its
first r elements. Define t_r recursively from
`m_(P_s)=sum_(r<=s) t_r e_r(c_(P_s))`, and define, for proper A,
`r_A=m_A−sum_(r<=|A|) t_r e_r(c_A)`. State that the canonical old summary
stores these residuals off the reference chain and one reference old mean.
The residuals on P_r are zero. This supplies the exact triangular reconstruction
already given in C4 §5 and its F13 antecedent. A short displayed definition plus
the existing source link is sufficient.

### M3 — make the single-edited-procedure query family explicit

**Location:** Theorem 5 proof after equation (19), draft lines 800–804.
**Type:** required quantifier clarification; theorem unchanged.

For a fixed edited procedure j, equation (14) exposes prefixes preceding j,
which exclude j. Merely saying all proper prefixes occur among available
orders obscures why the full proper-moment radius is also attained for that
one edit.

**Minimal repair:** State that every subset of `[k] \ {j}` can precede j,
so every prefix size from 0 to k−1 occurs. In (16), the varying contribution
to a prefix moment depends only on its size; its residue offset is fixed.
Since k>=2, a singleton prefix excluding j occurs and supplies the same lower
bound. Thus the common radius for the fixed edit is exactly the displayed one.

### M4 — restore short explicit domain clauses

**Type:** precision edits, not new mathematical obligations.

| Location | Missing explicit clause | Minimal repair / source |
|---|---|---|
| §6.1, before P_Gamma (line 433) | A native maximum and the valuation family must be finite. | Say “For a finite premise family Gamma over finitely many atoms.” F09 B2 states precisely this finite contract. |
| §6.3 rigidity sentence (lines 486–491) | The budget transformation is common across all baselines; preserving selected or baseline-dependent tests does not force affinity. | Add “through one common budget map, for all real baselines.” F09 S3 assumes `x−y<=b iff h(x)−h(y)<=g(b)` for all real x,y and rational b. |
| §7.1 native-admission sentence (lines 533–535) | M is described as nonnegative but not explicitly rational, whereas the native language permits rational coefficients. | Say that the native instances take all fixed price/penalty parameters rational, or explicitly distinguish the real-parameter mathematical calculation from its rational native instances. The rank and recovery statements themselves do not fail for real M. |
| Theorem 5 first sentence (line 745) | The definitions of mu and the decoder continue the R>0 branch. | Begin “For R>0, under these assumptions…” and retain the preceding known-law R=0 case (radius zero). |

### M5 — define the cited lattice's P

**Location:** §7.2 chain-algebra antecedent paragraph, draft lines 615–620.
**Type:** minor citation/notation clarification.

The primary source was opened and its Theorem 3.4 and maximal-chain span
argument were checked. The quoted dimension formula is correct: the theorem
uses `L=J(P)`, with P the underlying poset whose ideals form L. The proof
identifies the same dimension with the rational span of maximal-chain incidence
vectors. Add `L=J(P)` when displaying `|L|−|P|` so P is defined. This is an
antecedent for the equal-price rank, not a statement of the price-revision or
actual-mean repair theorem.

Primary source: Gasanova and Nicklasson, *Chain algebras of finite distributive
lattices*, Theorem 3.4 and its proof, §3.2,
[primary publication](https://link.springer.com/article/10.1007/s10801-023-01294-8).
Opened October 6, 2026 UTC; retrieval identifiers are in the companion JSON.
This was a targeted theorem check, not a renewed worldwide-priority search.

## 3. Examples, explanatory sentences and tables

The binary example in §2 is a smaller illustrative instance of F02's established
dependence separation, not a new substantive result: direct two-state evaluation
gives expected max/min `(1/2,1/2)` for alignment and `(1,0)` for opposite bits.
The continuation-transformer table is consistent with F02 §4.9's warning that
an extensional map need not retain hidden dependence or observation structure.
The guarantee-front row does not assert arbitrary unqualified sequencing or
equate an attainable budget with scalar preference.

The hidden-action example's lower bound is direct:
`max(2q,2(1−q))>=1`. The residual clipping equation preserves the signed/unsigned
distinction. The native rule table and equations (5)–(7) agree with the accepted
pointwise arithmetic and withdrawal contracts. Their statements do not equate
evidence use with independent observations or a feasibility witness with source
truth.

The Boolean translation table, excluded-middle example, inconsistent-premise
construction and phase-one interval endpoints agree with F09 B1–B4. The scale
discussion retains the actual operation/row/conversion transport obligation and
correctly separates a proved general affine construction from the implemented
common-scale compiler; M4 only makes the rigidity quantifiers explicit.

The §7.3 regret and numerical-error statements agree with C4 §6: fixed law or
fixed source, common policy family, and mean/fixed-level CVaR or its worst-source
version. The interval of pathwise changes has width |epsilon|, so the comparison
argument is valid. The paired-trace paragraph correctly treats those traces as
additional retained information rather than free access to discarded data.

The displayed recovery constants were checked algebraically against accepted
formulas, without experimental execution. At k=3,M=4, the maximized width is
1/2, giving |epsilon|/4 and 1/160 at |epsilon|=1/40; the ordinary 1/80 bound also
meets tolerance 1/20. For the k4 midpoints, the old mean forces m4=5/372, and
`m2−2m3+m4=−3/496` is the two-failure world mass. The triangle's radii 1/400
and 1/300 are moment radii, as the draft says, and scale by edit magnitude for
revised means. None is presented as a new measured outcome or speed advantage.

## 4. Limits and handoff

This is a fixed-snapshot mathematical and reader review of §§2–7. It does not
approve the still-assembling abstract, introduction, empirical sections,
bibliography, final report, Gate D or a new contribution scope. The detailed
envelope proof is linked honestly; the report does not pretend it was reproduced
in full. No conflict with an accepted theorem was found. Apply the local report
repairs above and retain the exact theorem scopes.

No tests, theorem searches, kernel changes or experimental stages were run.
One combined source-read output was truncated; the relevant finite Boolean,
affine-transport and candidate-limit sections were subsequently read in targeted
calls. The fixed draft was checked against its supplied SHA256 before review and
again at closure. The companion JSON lists source snapshots and findings.
