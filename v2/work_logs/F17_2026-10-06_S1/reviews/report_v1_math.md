# F17 report_v1 mathematical and continuous-reader review

Reviewer: **ChatGPT (GPT-6 Astra Pro)**, same-model internal review with prior
source familiarity; not blind or external peer review. October 6, 2026 UTC.

Fixed snapshot: `v2/work_logs/F17_2026-10-06_S1/drafts/report_v1.md`,
88,634 bytes, SHA256
`af2a98350273c59eb2b682e62be9df13c11f8f1f9d67df7b0c94d73e24673784`.
Read continuously: abstract, introduction, §§2–8 and §§11–12. Read-only comparison
with the earlier core review and accepted sources. No manuscript changes,
scientific stages or tests; principal concurrent credit **zero**.

## 1. Scoped disposition

**The five theorem statements and their contribution scope remain supported.
The earlier substantive M1–M5 issues are addressed.** No stronger completeness,
retention, decoder, worldwide-priority or empirical-superiority theorem has been
introduced in the reviewed sections. The report has a coherent standalone route
and clearly distinguishes the core proof, constructive proof outlines and the
complete linked envelope derivation.

Before finalizing this snapshot, fix **R1's capability/speed implication** and
**R2's residual-index domain**, and make the short symbol introductions in R3.
These are local report repairs. They do not require changing scientific results,
reopening an experiment or starting a research recurrence. This assessment is
not a final report audit or Gate D decision.

## 2. Regression of M1–M5

| Prior finding | Revised location / evidence | Disposition |
|---|---|---|
| M1: correct kernel for the rank lower bound | Theorem 3 explicitly defines requested map Q, retained map T, rank(T)<rank(Q), and v in ker(T) outside ker(Q). Interior perturbations preserve retained data while changing requested values. | Resolved. |
| M2: constructive chain and residuals | Theorem 4 defines a reference order with j last, prefixes with cardinality r, recursive t_r, residuals, the reference mean and the positive triangular diagonal. | Substantive gap resolved; add R2's explicit proper-subset domain to the new formula. |
| M3: fixed edited procedure versus all prefixes | Theorem 5 uses subsets excluding j, realizes every size, identifies size-only varying contributions and obtains the singleton lower bound for k>=2. | Resolved. |
| M4: finite/quantified/domain clauses | Finite Boolean premises/atoms, a common budget map over all real baselines, rational native price/penalty instances and the R>0 decoder branch are explicit; R=0 has radius zero. | Resolved. |
| M5: define P in the chain antecedent | The paragraph gives L=J(P) as the ideals of a finite poset P. | Resolved. |

The twelve mathematical/literature source snapshots in the prior review's
manifest remain byte-identical. The change from earlier inline/display math
delimiters does not alter the reviewed formulas. This is a content-level
assessment of the Markdown source, not a rendered-output verification.

## 3. Precise remaining findings

### R1 — ordinary reproducibility does not by itself refute a speed claim

**Location:** §11.1, paragraph beginning “This is substantive local mathematical
content,” lines 1497–1502 of this snapshot.

The sentence says that reproduction by an ordinary implementation defeats an
exclusive-capability **or general-speed** claim. Reproducing the function or
service establishes a capability comparison; it does not logically determine
relative running time. The report correctly says elsewhere that general speed
superiority is unestablished, so only this implication needs changing.

**Minimal repair:** Separate the conclusions: ordinary reproduction rules out an
exclusive-capability interpretation; the reported cost evidence establishes no
general speed advantage. This preserves both the ordinary comparator and the
bounded contribution without making a stronger negative performance claim.

### R2 — state the domain of the new residual definition

**Location:** Theorem 4's new canonical-summary formula, lines 774–783.

The definition
`r_A=m_A−sum_(r=1..|A|) t_r e_r(c_A)` must be restricted to **nonempty proper
subsets A of [k]**. The current formula does not state this domain, although
only t_1,…,t_(k−1) have been defined. At A=[k] its displayed sum calls for
t_k, and “off the reference chain” could include that full set. The accepted
C4 construction uses proper residuals and obtains the full moment separately
from the reference mean.

**Minimal repair:** Add `for emptyset != A subsetneq [k]` beside the residual
formula, and say that the canonical summary stores those proper residuals off
the chain. No formula or rank otherwise changes.

### R3 — complete the local symbol introductions

These short additions would satisfy the requested standalone notation standard:

| Location | Reader currently infers | Minimal introduction |
|---|---|---|
| §4.2 before equation (7) | P denotes the old localized proof; b_P is its original root budget; a_i is the left side of a withdrawn source row. | “Let P be the old localized proof with root budget b_P and rows a_i(x)<=eta_i.” |
| §6.1 before the Boolean connective table | The atom clause of the recursive translation is implicit. | “For each atom p_i, set L(p_i)=x_i, its Boolean loss bit.” |
| §8.1 near equation (21) | u,v are coefficients of the linked polynomial family; S_j,Q_j are weights on the union of nodes. | Identify those roles and set d=u/4−v explicitly. The full polynomial/weight construction may remain linked as it already is. |

The intended meanings are recoverable from the accepted sources and surrounding
prose. This finding requests definitions, not a different semantics or example.

## 4. Continuous reading and source agreement

The abstract and introduction accurately present the selected source-based
loss semantics, reduct-relative completeness and specialized reset application.
The wording “can require k−1” in the abstract is existential; the detailed
Theorem 4 gives its necessary M>0 and exact-information assumptions. The
introduction does not turn that requirement into a practical memory or regret
lower bound. Its philosophical premise is labeled motivation rather than an
axiom used in proofs. The negative neural result is not made a condition for
the mathematical application or treated as an automatic representation
falsification.

Sections 2–6 retain the finite typed domain, shared sources, signed orientation,
case coverage and observation-legal action distinction. The soundness theorem
still requires binding the actual root to an independently specified current
request. The constructive converse still concerns the target-unit reduct, with
full-source completeness only at its separate graph condition. The normal-form
alternative is described as having independent proof ingredients, avoiding
circular use of completeness. The Boolean and phase-one interfaces remain
restricted translations, and the general affine construction is not described
as an implemented compiler.

Section 7 retains the full-law versus proper-moment distinctions at zero
terminal penalty, exact-linear rather than arbitrary-encoding ranks, actual new
means for repair, and the difference between exact information and useful
approximation. Theorem 5 retains full exact equal-old-price fibers, unchanged
outcomes/penalty and separately applied edits. The common-radius objective is
not replaced by coordinate-midpoint attainment. Both envelope inequalities are
displayed as the substantive family-specific step, with their complete proof
linked and their reduction described. Its O(k) statement remains scalar-radius
arithmetic only. The k4 midpoint witness, corrected k3 scope and additional-source
triangle do not overstate what each demonstrates.

Section 8's scientific bound agrees with F13 §2.9:
`1/64+(3/200)(28633/46200)−1/32 = −4873/770000`.
The shared target discrepancy cancels before the absolute-value bound, and no
absolute-accuracy conclusion is claimed. The ordinary interpolation and Gaussian
quadrature alternatives are retained. The self-assessment example matches
F13 §§4–4.3: `C−9<=−1/4+20q`, non-deterioration at q<=1/80, cascade means
35/4 and 55/4, and the stronger source-visible control's five/six emitted-node
means. Unresolved bounded search is explicitly separated from falsehood;
same-population applicability and total inspection/runtime costs remain separate.

Sections 11–12 preserve the adopted contribution's object, type, exact delta,
magnitude and comparison scope. They credit established ingredients, identify
the explicit compatible-center equality as additional family-specific content,
and leave worldwide priority and broad deployment benefit unestablished. They
also keep the incomplete 2022 comparison incomplete, with no favorable inference
from missing text. R1 removes the sole new logical overreach identified in that
discussion. Future acquisition, comparison and joint-neural chunks are concrete
but deferred, with no optional work presented as completed.

## 5. Evidence and handoff limits

The report snapshot was hash-verified at entry and closure. The reader inspected
all requested sections, compared the repaired passages to the earlier findings,
checked the unchanged earlier source snapshots, and reread the scientific and
self-assessment source passages and current Gate C contribution scope. No new
primary-literature search was needed for this revision; the earlier targeted
chain-algebra theorem check remains recorded in the core review.

Sections 9–10's detailed data/metadata, the full bibliography, rendered GFM
output, administrative state and time ledger are outside this assigned review.
The abstract's numerical wording was assessed for claim scope against the
established supplied counts, not independently re-audited here. Those areas
retain their separately assigned checks. After R1–R3, the reviewed mathematical
and contribution-scope content is suitable for the subsequent final audit.
