# F17 mathematical source map and presentation review

Reviewer: **ChatGPT (GPT-6 Astra Pro)**, separately assigned same-model internal
review; not external peer review. October 6, 2026 UTC. Entry source:
`2e44ed1b711508d7ad451e1ca6272ff989deef81`.

The author has now approved Gate C and authorized F17. Older source headings
retain their historical next-task/gate statements; the report should take its
current disposition from the author-approved project state, while preserving
those historical records. This review assembles existing mathematics. It changes
no theorem, rule, experiment, frozen source or scientific claim. Concurrent
review time receives **zero principal credit**; no duration is estimated here.

## 1. Recommended report structure and authoritative sources

Lead with the supported difference: a specialized retention/repair and coherent
recovery analysis for revisable correlated reset costs, integrated with explicit
source and request contracts. The general arithmetic, checked-evidence pattern
and linear/moment optimization are established ingredients. Then introduce the
core needed to understand the contribution. Do not lead with project task
chronology or imply that the whole core is a new foundational logic.

| Report role | Current mathematical source | Claim anchors / scope |
|---|---|---|
| Question and candidate selection | [F02 candidates](../../../foundations/02_candidate_semantics.md), opening and §1; [F05 choice](../../../foundations/03_provisional_core.md) §1 | Scalar evaluation, aligned profiles, continuation transformers and guarantee fronts are different semantic objects. The selected CPWA loss model is a pragmatic, revisable choice. |
| Definitions and source semantics | [F05](../../../foundations/03_provisional_core.md) §§2–6 | Finite signed values, typed conversions, shared source identities, nonempty finite polyhedral cases, independent semantic consequence and observation-legal policies. |
| Actual rules | [F06](../../../derivations/02_inference_rules.md) §§1–4 | Signed budgets, common-source composition, residual polarity, exhaustive cases. |
| Soundness and receiver boundary | [F07 consolidated acceptance](../../../derivations/03f_soundness_acceptance.md) §§1–3; [full native proof](../../../derivations/03_soundness.md) | F07-C01/C16. Exact native acceptance plus binding to the current request; advertised producer fields require separate contracts/checks. |
| Constructive characterization | [F08 U1–U8](../../../derivations/04_characterization.md); [acceptance reconstruction](../../../derivations/04g_characterization_acceptance.md) §§1–3 | F08-C01/C03. Completeness is exactly reduct-relative; stronger full-source claims have explicit closure conditions. |
| Boolean / phase-one comparison | [F09 map](../../../derivations/05_fragments_and_comparisons.md); [B1–B4](../../../derivations/05a_boolean_and_phase_one.md) §§1–2.1a | F09-C01/C02. Exact Boolean sublanguage and specified evidence-consumer adapters, not a full phase-one embedding. |
| Genuine worked composition | [F07 acceptance](../../../derivations/03f_soundness_acceptance.md) §§4–5; [F13 cases](../../../derivations/06_case_studies.md) §§2.9, 4 | Conditional relative comparison, shared-baseline cancellation, actual bounded later reasoning. Gate C §3 reproduces the key numerical derivations. |
| Exact retention and repair | [C4](../../../derivations/09_c4_price_revision.md) §§1–6, 8 | C4-T1/T2/T3; ledger C4-C02/C03. Exact linear summaries of full reset-order means under fixed outcome laws. |
| Conditional intervals and canonical input | [C4](../../../derivations/09_c4_price_revision.md) §11 | C4-A2/C4-C05. Exponential-size old summary; residual uncertainty reduces to a one-mean level-law polytope. |
| Compatible optimal decoder | [F16-C1](../../../derivations/10_f16_coherent_recovery.md) §§1–8 | F16-C1. Full exact equal-old-price fibers; common minimax tolerance; explicit compatible law. |
| Sharp limits and corrected interpretation | [F16](../../../derivations/10_f16_coherent_recovery.md) §§9–11; dated F16-R01 in [C4](../../../derivations/09_c4_price_revision.md) §10 | C4 coordinate-midpoint counterexample survives at k=4; the earlier k=3 warning was corrected. Extra source restrictions/noisy old observations alter the theorem's domain. |
| Current contribution disposition | [Gate C](../../../checkpoints/C_1.md) §§1–5; [claim ledger](../../../claim_ledger.md), C4, F16 and C1 entries | Modest synthesis/formal adaptation/specialized application, supported only at the stated comparison scope. Worldwide priority unestablished. |

The detailed derivation links should remain in `paper_v2.md`. A reader should
be able to distinguish a proof included in the report, a proof sketch with a
complete linked derivation, and finite executable corroboration.

## 2. Definitions to state once, with stable orientation

Fix a finite signature of named sources, units and directed positive rational
conversions. Terms are finite, closed, typed rational continuous piecewise-affine
expressions: literals, sources, addition, rational scaling, min/max,
`res(a,b)=max(b-a,0)`, nonrecursive lexical binding and declared conversions.
Negative scaling is permitted; literal infinite values, variable products and
the full Rational Lawvere Logic proof system are not included.

At one visible observation, a context is a finite nonempty union of closed
rational polyhedral source cases. Each live case has a supplied rational feasible
witness. Source coordinates are finite reals at each model; the domain may be
unbounded. Repeated occurrences of a key denote the same coordinate. An evidence
revision is distinct from changing the program, population or criterion meaning.

Use the same orientation throughout:

```math
 C\models t\le_b s:u
 \quad\Longleftrightarrow\quad
 \forall(h,x)\in D_C,\;t_h(x)-s_h(x)\le b.
```

Here **t is the new loss and s the old loss**. Negative b guarantees modeled
improvement; zero gives non-deterioration. The metalevel supremum may be infinite
even though every pointwise value is finite. Clipping the difference to a
nonnegative residual discards negative improvement margins. Absolute adequacy
is a separate zero-reference request.

The same policy must work across the hidden cases. A proof may choose different
mathematical witnesses in different cases; a deployed policy does not thereby
observe the case. A useful illustration is hidden costs `(0,2)` versus `(2,0)`:
the pointwise minimum is zero, but a fixed randomized policy has worst cost at
least one. This is the distinction between `exists policy, for all models` and
`for all models, exists action`.

## 3. Suggested main core theorem and its proof

### Theorem S — current-request soundness

For an admitted context and independently fixed request, on finite immutable
supported data with exact rational arithmetic, an accepted finite native proof
whose actual root is received against the current context, domain, unit,
expression pair and sufficient budget establishes that request's finite-real
semantics. Any additional producer field used by the caller needs its stated
producer contract or an independent receiving check.

Present the proof as three steps, retaining the receiving step:

1. **Denotation-preserving normalization.** Structural induction includes the
   captured lexical environment. Collect the binding RHS in the old environment,
   type-check before erasing zero coefficients, and preserve shared sources.
2. **Local preservation and finite-DAG induction.** All sixteen native tags have
   pointwise proofs. Addition/transitivity add signed budgets; nonnegative
   scaling multiplies them; min/max congruence takes their maximum; combining
   proofs of the same difference takes their minimum; exhaustive cases take the
   maximum over every live case. Residual congruence reverses its first argument's
   comparison and clips the summed allowance at zero.
3. **Reception.** The proof's literal conclusion is bound to the caller's request.
   A root at budget b_out discharges inclusive B only if b_out<=B, and a strict
   request only if b_out<B. Context fingerprints identify recorded data; they
   do not establish physical provenance or empirical truth.

State successful-return correctness explicitly. This theorem does not promise
successful bounded search or certify source applicability. A proof beside a
field named `penalty` or `new` does not authenticate that field. F07's receiver
repair is evidence that this distinction was tested, not a flaw left unresolved.

### Theorem U — constructive unit-directed completeness

Let A(u) be the units with a directed conversion path to the query unit u,
including u. Form C|u by retaining just rows whose common unit lies in A(u),
with the signature, live cases and witnesses otherwise retained. For each
finite common-pair admitted query and rational b:

```math
 K_C(t,s;b)\quad\Longleftrightarrow\quad C|u\models t-s\le b.
```

The left side means existence of a finite native proof with exactly the requested
global pair and root budget at most b. It ignores implementation resource caps.
If its optimal bound is finite, it is rational and attained by both a finite
proof and a rational reduct model. Otherwise no finite native bound exists.

The proof has real constructive content:

- Root ancestry can only preserve units or follow named conversion edges; thus
  every used source row survives in the reduct. Induct in each local domain and
  only then aggregate the union.
- Positively transport accessible rows and certify retyping of the query into
  u. Distributing conversion through min/max needs a native equality proof,
  not merely a normalizer assertion or an invented inverse bridge.
- Split finite CPWA syntax into affine sign cells. Rational affine consequence
  supplies exact multipliers; rational feasibility supplies live witnesses or
  strict empty-branch rays. Eliminate temporary guards by the existing hinge
  discharge construction. Finally graft original source proofs, restore literal
  query equalities and cover every original case.

This route is enough for a report sketch. Link F08 §§9–14 and its acceptance
reconstruction for the complete proof. The alternative finite max-min route is
worth mentioning, but proving its normal form by invoking U1 would be circular;
its identities are derived from existing lattice/arithmetic and hinge rules.

Give the failure of unrestricted completeness immediately after the theorem.
With only a factor-one conversion U→V, source x:U and a V-row
`convert(x)<=-1`, the U-query `x<=-1` is semantically valid. Its U-reduct has no
rows, and x=0 is a reduct countermodel, so no native proof exists. That point
does **not** refute the original full source.

For a fixed unit graph, full-source completeness uniformly over source
declarations and unit-u queries holds exactly when A(u) has no outgoing edge
to its complement, equivalently every unit in u's weak component reaches u.
For all targets this means each weak component is strongly connected. The
fixed-signature criterion U7 can be weaker because it concerns actually declared
source keys. Do not demand conversions between disconnected units.

## 4. Boolean and phase-one material: a compact proposition is enough

Encode Boolean truth as loss zero and falsity as loss one. Then:

| Classical syntax | Loss expression on Boolean sources |
|---|---|
| top / bottom | 0 / 1 |
| not A | 1−L(A) |
| A and B | max(L(A),L(B)) |
| A or B | min(L(A),L(B)) |
| A implies B | res(L(A),L(B)) |

Structural induction proves truth preservation. For a finite premise family,
P_Gamma=max of its losses (zero for no premises), and the all-valuations Boolean
context C_B gives

```math
 \Gamma\models_{\mathrm{CL}}B
 \iff C_B\models L(B)\le P_\Gamma
 \iff K_{C_B}(L(B),P_\Gamma;0).
```

Encoding premises in the query preserves classical inconsistent-premise
entailment without admitting an empty source context. The Boolean fragment is
not closed under every arithmetic operation, and replacing discrete sources by
the interval [0,1] invalidates the identification: at x=1/2, excluded middle
has loss min(x,1−x)=1/2.

Phase one's `refuted < open < supported` meet algebra embeds as losses
`1 > 1/2 > 0`, with max as aggregate meet. This is a status code, conditional
on the original well-formedness and diagnostics, not an expected loss or
probability interpretation of open. The supplied interval consumer [l,u] at
threshold tau is supported iff u<=tau, refuted iff l>tau, and open otherwise.
The finite-region and rectangle adapters have similarly exact scope. Missing
evidence, invalid frames, provenance and arbitrary acceptable regions are not
silently absorbed into a scalar. A report should say “specified phase-one
adapters,” not “phase one is fully recovered.”

## 5. Retention and repair: theorem statements worth displaying

For k>=2 reset procedures, one fixed arbitrary Boolean outcome law, strictly
positive attempt prices and terminal penalty M>=0, every permutation pi has

```math
 C_\pi(c,M)=\sum_{j=1}^k c_{\pi_j}m_{\{\pi_1,\ldots,\pi_{j-1}\}}
              +Mm_{[k]},\qquad m_S=P(S\text{ all fail}),\quad m_\emptyset=1.
```

Let n=2^k−1. These are **exact linear-information ranks**, with constants free
and arbitrary decoding of a retained linear summary. Prices are fixed parameters
for each query; treating both prices and moments as unknown native variables
would add bilinear syntax.

| Consumer | One price profile | Two nonproportional positive profiles (c,M),(d,N) |
|---|---:|---:|
| All numerical order means | n−k+1 = 2^k−k | n if M>0 or N>0; otherwise n−1 |
| All within-profile differences | n−k | n−1 |
| All differences, including cross-profile | n−k for one profile | n if M!=N; otherwise n−1 |

For C4-T1, show the adjacent-swap difference
`(c_a−c_b)v_S+c_b v_(S+a)−c_a v_(S+b)`. Its zero set gives
`v_A=sum_r t_r e_r(c_A)` for proper subsets. Intersecting the two profiles'
kernels forces every proper coefficient to zero by positivity and
nonproportionality. The terminal direction survives precisely in the cases
listed. Small perturbations of an interior law turn the linear null directions
into actual feasible indistinguishable laws. Proportional profiles and known
lower-order marginals have separate formulas in C4 §§4,8.

**C4-T2.** From a minimum-rank exact summary of all old numerical means with
c>0 and M>0, change only c_j by nonzero epsilon while keeping it positive and
M fixed. Exactly k−1 additional independent linear measurements are necessary
and sufficient to recover the law; they can be k−1 actual new-order means.

For sufficiency, choose nested prefixes P_r avoiding j. Placing each P_r just
before j makes the new-minus-old mean epsilon m_(P_r). Those k−1 chain moments
solve triangular equations for the missing kernel coefficients; the old mean
then recovers m_all by division by M. For necessity, the old kernel has dimension
k−1. With fewer exact responses it retains a feasible null direction; fixing an
adaptive transcript does not remove this indistinguishability. If M=0 the full
law remains unidentifiable, although k−2 new means recover all proper moments.

The interpretation must stay narrow. The initial summary already has exponential
dimension. Ranks are neither bits nor sample complexity. Any nonzero price
change can destroy exact sufficiency while every old-optimal policy still has
new-price regret at most |epsilon| under the stated common policy/law objective.
The ordinary midpoint estimate gives a universal |epsilon|/2 numerical bound.
This distinction between exact information and useful decisions is central.

## 6. F16-C1: recommended central application theorem

### Exact statement and explicit decoder

Use unit old prices, k>=2, fixed M>=0, and the **full** nonempty set of Boolean
laws consistent with one complete exact old numeric profile. Retain the canonical
contrast summary or equivalent information. It determines nonnegative residues
rho_w, residual mass R and residual old mean B_rem. If R=0 the law is known.
Otherwise every compatible law is uniquely represented by

```math
 p_w=\rho_w+\frac{R q_{|w|}}{\binom{k}{|w|}},\qquad
 q_h\ge0,\quad\sum_hq_h=1,\quad\sum_hg_hq_h=\mu=B_{\rm rem}/R,
```

where `g_h=(k+1)/(k+1−h)` for h<k and g_k=k+M. Put
`f_r(h)=binomial(h,r)/binomial(k,r)` for 1<=r<=k−1.

Let alpha=(mu−1)/(k+M−1), q^-=(1−alpha)e_0+alpha e_k, and let q^+ be
the adjacent-g-level mixture of mean mu. Set q*=(q^-+q^+)/2 and
beta=E_(q^+) f_1. The compatible law obtained from q* attains the unrestricted
common minimax error over every proper-prefix moment. The conditional radius is

```math
 r(C)=\frac{R}{2}(\beta-\alpha).
```

For one admissible price edit epsilon, revised-mean error is |epsilon|r(C).
The same decoded law works for each **separately applied** one-price edit; a
bounded family of edit magnitudes with supremum E has common error Er(C).

### What makes the proof substantive

The singleton lower extremum is alpha and the upper is beta, giving the lower
bound r(C). For each r, write L_r,U_r for extrema of E_q f_r and B_r=E_(q^+)f_r.
The linked proof establishes the simultaneous envelope inequalities

```math
 2U_r\le\beta+B_r,\qquad
 2L_r\ge2\alpha+B_r-\beta.
```

The candidate r-coordinate is (alpha+B_r)/2, so both errors are at most
(beta−alpha)/2. The residue offsets add fixed constants and R scales the
bound. This proves attainment by an actual compatible law, including
nonexchangeable offsets. Generic convexity alone does not give these two
inequalities. F16 §§3–7 proves them through polygonal upper envelopes and a
lower affine envelope, reducing to g-level nodes and handling M=0 before M>0.
Include the decoder and this proof reduction in the report; retain the full
envelope proof as an explicit link instead of calling it “immediate.”

The sharp global radius, over all such old-summary fibers, is

```math
 \frac{|\epsilon|}{2}
 \max_{1\le j\le k-1}
 \left(\frac{j}{k}-\frac{j}{(k-j+1)(k+M-1)}\right).
```

This finite maximum uses O(k) scalar arithmetic. It does not include reading
the exponential-size old summary, producing a full probability vector,
generating a native certificate or total bit/runtime cost. For k=3,M=4 it is
|epsilon|/4, a factor two below the ordinary universal bound; both meet F15's
small-edit tolerance. Ordinary methods may use the same formula.

### Boundaries to put next to the theorem

The theorem minimizes **one common maximum error**, not every coordinate's own
midpoint tolerance. The k=4,M=1/10 example has infeasible individual midpoints,
yet a compatible common-radius optimum. The corrected k=3 case has compatible
proper-coordinate midpoints; do not repeat the superseded warning.

Noisy old observations, additional law restrictions, simultaneous price edits,
arbitrary moment linear combinations or changes in M are outside F16-C1. Its
k=4 extra-convex-source triangle gives unrestricted radius 1/400 but compatible
radius 1/300 before multiplying by |epsilon|. Thus restricting the possible law
and requiring the estimate to obey that restriction can change the comparison.
A compatible decoded law is an estimate with an error contract, not new exact
source truth. Later consumers must retain the relevant uncertainty guarantee.

## 7. Final report checks and disposition

Before accepting the report draft, check the following high-risk sentences:

- “Complete” must name the target-unit reduct or the stated full-source closure
  condition; bounded search/refusal and structural nonderivability are distinct.
- “Value” must not silently become ultimate utility, truth probability or an
  observed hidden variable. Cost meaning, source assumptions and action access
  remain separately declared.
- A source witness proves nonemptiness, not empirical coverage. Relative
  improvement does not prove absolute adequacy; shared dependence does not
  assert statistical independence.
- “Optimal repair” means the named exact-linear information contract. “Optimal
  decoder” means the named common query error on full exact equal-price fibers.
- The theorem's useful delta should be described as specialized synthesis/formal
  adaptation/application. Neither ordinary reproducibility nor lack of global
  priority eliminates that scoped contribution; neither establishes a stronger
  exclusivity or deployment-advantage claim.
- The original 0/5 neural complete-support endpoint remains negative. Ordinary
  prediction training provides no particular reason for a clean eight-neuron
  cost block; mixed or distributed representations are plausible, and technical
  superposition is not proved. Extraction failure is not a universal absence
  theorem. This is interpretive context, not support added to F16-C1.

**Disposition:** Existing mathematics supports a self-contained report with
explicit theorem statements and proof sketches linked to complete derivations.
No new result is needed for F17 assembly. Awaiting the report draft for a
separate reader-level consistency check. Gate D remains a later task.

### Inspection record

Activities performed: read TODO's F17/Gate C instructions; read the definition,
rule and theorem sections itemized in the companion inspection JSON; trace
current C4/F16/C1 claim entries; compare the F16 decoder with its complete
upper/lower envelope derivation; write this source map. Some detailed sources
are mapped by their consolidated acceptance records rather than read in full. No tests, proof searches or experiments were run. An initial path
guess `v2/definitions` did not exist; the actual sources are in `v2/foundations`.
One combined output was truncated; the relevant Boolean and F16 proof sections
were subsequently read in targeted calls. These were inspection limitations,
not scientific failures or additional experimental attempts.
