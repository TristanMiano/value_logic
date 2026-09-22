# Phase Two Claim Ledger

Version: F01 completion, September 21, 2026.
Task status: **F01 complete: 60.243613 credited derivation minutes and 76 passing example checks**.
No calculus has been selected and no readiness gate has passed.
This is not a statement that the demonstrated arithmetic is unproved.

## Evidence conventions

All numbered claims below are scoped to the assumptions in the
[principal derivation note](foundations/01_requirements_and_separating_examples.md).
Their proofs are direct calculations or explicitly given countermodels. They
received same-agent self-review, not independent review. The
[26-test fixture suite](checks/f01_examples.py) supplies arithmetic and finite
enumeration checks; it is not a proof of an unrestricted future calculus.
[Machine-readable results](checks/F01_results.json) and the
[work record](work_logs/F01_2026-09-20_S1.md) record that distinction.

Artifact version: the committed F01 snapshot containing this ledger; exact
content hashes are listed in the session's manifest. A changed assumption or
counterexample reopens the corresponding claim and affected requirements.
No novelty status has been established; the external comparison belongs to F03.

## Demonstrated example claims

| ID | Exact scope and statement | Status and evidence | Dependencies / effect on the project |
|---|---|---|---|
| F01-C01 | E01's absolute error for $M_c$ is $a^3$ and for $M_a$ is zero. If both are feasible, cheap weakly beats accurate under the declared $J_q$ iff $a^3\leq7\lambda$. | Proved in the example; direct substitution; `test_e01_*`. | Stipulated reference, costs, weighted loss. Supports R01; no global model preference follows. |
| F01-C02 | At $a=1/2,\lambda=1/56$, both E01 combined scores equal $1/7$, but only the accurate model meets $\epsilon=1/100,b=8$. | Proved by exact collision; `test_e01_equal_combined_loss_different_admissibility`. | F01-C01 and the separate constraints. Refutes the sufficiency of this particular score alone for this admissibility query, not all scalar encodings. |
| F01-C03 | E02's ranking reverses at $\theta=3/4$. Uniform comparison over every $\theta\in[0,1]$ is equivalent to componentwise error comparison. | Proved by algebra and endpoint queries; `test_e02_*`, including 81 vector pairs. | Declared linear task family with comparable units. Supports R02; restricted task families may differ. |
| F01-C04 | E03's two means, and even its separate marginal laws, do not determine the expected pointwise minimum: the required paired cases yield $-1$ and $1$. | Proved by countermodel; `test_e03_required_witness`. | Joint query under specified finite means. Supports R03; exact answers from those summaries alone are impossible on a class containing both pairs. |
| F01-C05 | Finite linear means determine an additive composite mean. Two component means plus $\mathbb E|X-Y|$ determine the expected binary minimum. | Proved by finite-sum and real-number identities; 625 tested pairs. | Same joint scope and units. Positive sufficiency for R09; no nested closure or acquisition-cost advantage is established. |
| F01-C06 | Means fixed at one give no finite uniform lower bottleneck bound over the stated unbounded family. With E03's two-point marginal laws, the sharp interval is instead $[-1,1]$. | Proved by the parameterized family and joint-table parameter $t$; finite family/coupling fixtures. | Section 10.1; identifies exactly which extra premises license an informative bound. |
| F01-C07 | Under the stated reachable-scope and Lipschitz hypotheses, E04 composite error is at most $\eta+K\delta$; the linear fixture attains $51/50$, refuting the unweighted $3/100$ bound. | Proved by triangle inequality; `test_e04_*`. | Reuses a simple instance of phase-one transport ideas. R04 needs sensitivity and scope; it does not demand Lipschitz semantics universally. |
| F01-C08 | Nonempty evaluation sets with equal midrange can differ on uniform nonnegativity. On a nonempty finite set, the scalar minimum suffices for that query. Empty compatibility satisfies both universal sign formulas vacuously but not the requested nonempty justification. | Proved by sets and elementary quantification; `test_e05_*`. | E05's explicitly defined question. Supports R05; neither K3 nor a set-valued primitive is mandatory. |
| F01-C09 | For uniform $N=0,\ldots,5$ and residue-only adapters, the optimal loss matrix is $[[0,2/3],[1/2,0]]$; joint residues recover all six inputs. | Proved by conditional fiber counts and table injectivity; all 9 mod2-to-mod3 and 8 reverse deterministic decoders checked. | E06's information restriction is essential. Supports R06; no claim about actual set-theoretic axiom selection or raw-input adapters. |
| F01-C10 | E07's monotone recoding can reverse additive plan rankings when ordinary addition is naively retained; transported addition preserves exact sums. Approximate codes alone need not certify adjacent large values' ordering. | Proved by displayed arithmetic, inverse formula, and midpoint overlap; `test_e07_*`. | Declared additive task and exact versus finite-precision contracts. Supports R07, not a verdict against bounded carriers. |
| F01-C11 | The unbounded payoff $X(k)=k$ under $p_k=2^{-k}$ has expectation $2$ and tail probability $\Pr[X\geq8]=1/128$, unlike constant payoff $2$. | Proved by induction and geometric remainder; finite partial sums checked, not treated as an infinite computation. | E07's specified countable weighting. Distinguishes object boundedness, integrability, and evaluation family. |
| F01-C12 | E08's no-observation value is $1$; optional symmetric signal acquisition gives $\max\{1,4p-1-\kappa\}$ for $p\in[1/2,1]$. | Proved by enumeration of four policy forms and linearity; `test_e08_*`. | Declared information schedule, action set, law, and cost. Supports R08; a pointwise envelope is not automatically an attainable plan. |
| F01-C13 | The two three-by-three tables have identical marginal laws, variances, and covariance zero but minimum means $-7/18$ and $-1/2$. | Proved by exact table sums; covariance fixture. | Section 10.2; covariance is not a universal replacement for the required joint statistic. |
| F01-C14 | Equal pairwise laws of three binary payoffs do not determine their three-way minimum mean: the even/odd fixtures give $0$ and $1/4$. | Proved by four-row enumeration; triple-minimum fixture. | Section 10.3; binary sufficiency does not establish nested closure without further information. |

## Reconstruction claims (S2)

All claims below refer to the [reconstruction note](foundations/01a_reconstruction_and_information_contracts.md)
and the [exact fixtures](checks/f01_reconstruction.py). They are example-level
conditional proofs, not theorems of a selected calculus. Review is same-agent,
non-blinded; none is labeled independently checked or novel. The
[machine-readable results](checks/F01_reconstruction_results.json) separate finite
checks from the general arguments. Changed hypotheses require rechecking uses.

| ID | Exact scoped claim and proof location | Evidence and limits | Requirement impact |
|---|---|---|---|
| F01-C15 | For affine two-coordinate loss differences on a closed task interval, nonpositive values at both endpoints are equivalent to nonpositivity throughout (§A.1). | Proved by convex combination, including the singleton interval; finite grids checked. | R02: the actual task family, not all conceivable weights, controls uniform comparison. |
| F01-C16 | Known nondegenerate binary supports, marginals and compatible covariance uniquely fix the four-cell joint law (§B.1). | Explicit table and feasibility inequalities; 105 support/table checks. | R03/R09: covariance is sufficient in a stated fragment, not universally. |
| F01-C17 | With uniform ternary marginals, minimum means range sharply over [-2/3,0]; adding zero covariance narrows this to [-1/2,-1/3] (§B.2). | Complete symmetric-table proof and attaining family; 120 integer tables checked. | R03/R09: failed exact recovery can coexist with a useful tolerance guarantee. |
| F01-C18 | The latter sharp bounds already follow from support [-1,1], zero means, second moments 2/3, and cross-moment zero (§B.3). | Alternative pointwise proof; 289 grid pairs. Five-point rational countermodels refute dropping support. | R03/R07: full marginal laws can be unnecessary, but retained support premises matter. |
| F01-C19 | Without support bounds, the stated moment class has sharp minimum-mean range [-1/sqrt(3),0), with unattained upper endpoint (§B.3-B.4). | Squared-deviation bound and explicit finite-support family; infinite-class claims proved analytically, not by finite tests. | R05: strict sign, closed hull, attained extrema, and uniform margins differ. |
| F01-C20 | Even/odd n-bit laws agree on every proper marginal but differ on the n-way minimum; nonnegative scaling keeps the gap large (§C). | Counting proof for all n>=2; tests n=2 through 7. | R03: bounded retained interaction order does not imply unrestricted nested exact or fixed-error sufficiency. |
| F01-C21 | Shared loss uncertainty can leave improvement exactly two despite a wide marginal-interval bound; finite interval-bound equality requires co-attained extrema (§D). | Explicit paired sets, slack proof, 511 finite joint sets; infinite nonattainment counterexample. | R04/R05: distinguish lost dependence from an unsound bound. |
| F01-C22 | All ordinary two-component sum comparisons are preserved iff a real recoding is positive affine; unequal-length uncorrected sums also require zero offset (§E.1). | Additivity and rational-density proof; 5,625 comparisons plus variable-length counterexample. | R07: operation and count conventions determine valid rescalings. |
| F01-C23 | The bounded recoding has a finite-range inverse-error guarantee with both decoded values in range; no fixed global code precision controls real-unit regret (§E.2). | Exact identities, clipping repair, interval width, midpoint ambiguity; fixed fixtures. | R07: encoding, operation, numerical accuracy and decision accuracy are distinct. |
| F01-C24 | The best uniform absolute numerical error on a nonempty real-answer fiber is half its diameter; a deterministic epsilon-regret action exists iff compatible epsilon-optimal sets intersect (§F.1-F.2). | Endpoint and intersection proofs; finite numerical/choice witnesses. | R09: decision sufficiency need not imply exact value recovery. |
| F01-C25 | For scores (n-kappa,0), n>=1 integer, always choosing the first action has sharp worst regret max(kappa-1,0); any positive probability of the second has unbounded worst expected regret (§F.2). | Direct parameterized formula and growth witness; finite checks do not claim exhaustive infinity. | R02/R09: a task change can destroy exact choice without destroying a useful tolerance guarantee. |
| F01-C26 | Simultaneous per-action error delta gives regret <=2 delta. Marginal coverage alone does not; union bounds plus a failure-loss bound give scoped replacements (§F.3-F.4). | Decomposition, sharp tie, constructed reporting law; 729 score pairs and 1,215 reporting-law checks. | R08: selection must not silently promote marginal accuracy to simultaneous evidence. |
| F01-C27 | Finite signal-policy value lies between no-information and oracle values; oracle equality needs a common optimal action on each positive-signal support (§G). | Explicit optimization and nonnegative-gap proof; 2,835 law/payoff cases. | R08: operator order encodes when information and choice are available. |
| F01-C28 | Matching current payoff/signal marginals need not preserve conditional evaluation; a supported positive denominator supplies the stated ratio bound (§H). | Matched-marginal and rare-event countermodels; 180 ratio checks. | R04/R05: update stability needs a stated event and joint/precision premises. |
| F01-C29 | The three pair constraints have a common approximate uniform-marginal model iff their upper error caps sum to >=1; exact errors require nonnegative derived pattern weights (§I). | Necessary/sufficient constructions; 125 caps, 125 exact vectors, 165 pattern mixtures, and 1,716 joint laws checked. | R05: exact matching, upper caps, objectives, and extra independence assumptions are separate choices. |
| F01-C30 | Bottleneck uniform errors use a maximum, but mean-absolute errors may require their sum; mean local sensitivity cannot replace a uniform sensitivity (§J). | Pointwise inequalities and sharp profiles, including composite mean range [1,n]; 15,625 tuple pairs and 16 sensitivity profiles. | R04: retain aggregation and joint products, not just scalar error labels or correct units. |
| F01-C31 | A finite checked prefix does not bound expectation over the stated integrable tail-spike family; a supported envelope Ck gives sharp tail allowance C(N+2)2^-N (§K). | Series identity and explicit extensions; 48 spike cases and finite remainder checks. | R07: integrability per model, class-wide tail control, and a complete declared model are different premises. |

## Commitments, design defaults, and unproved targets

| ID | Role and statement | Status |
|---|---|---|
| F01-P01 | Epistemic nonfinality, pragmatic model use, and investigation of value as primary motivate the project. | Author-approved commitments, not derived metaphysical theorems. |
| F01-D01 | R01-R09 are conditional capability requirements for admitted queries; candidates may explicitly restrict their fragment. | Provisional requirements supported by examples, revisable through the queue. |
| F01-T01 | A useful calculus can be selected and proved sound with a nontrivial characterization result. | Research target; unproved. No core, general soundness theorem, completeness theorem, or Gate A-D pass exists yet. |
| F01-T02 | A candidate reasoner will offer a measured practical benefit over declared baselines. | Untested future empirical question, not established by the fixture tests. |
| F01-T03 | F01 satisfies all of its completion conditions. | **Established at the F01 task scope:** eight worked examples, reconstruction, supporting records, 76 passing checks, and 60.243613 credited D minutes. This is not Gate A or a soundness claim for a calculus. |

## Dependency and repair policy

The operational requirements depend on their named example assumptions, not on
an adopted universal semantic carrier. F02 should compare candidates against the
same fixtures and information access. Later rules must cite the exact premises
needed by each reused claim. A counterexample to an example calculation repairs
F01 and its downstream uses; a candidate's deliberate restriction is recorded
as a capability limit rather than concealed. No mathematical gate has yet been
attempted or invalidated.
