# Phase Two Claim Ledger

Version: F02 completion plus F03 partial audit, September 22, 2026.
Task status: **F01 complete (76 checks); F02 complete (124 dedicated checks and 61.118295 credited derivation minutes)**.
No calculus has been selected and no readiness gate has passed.
This is not a statement that the demonstrated arithmetic is unproved.

## Evidence conventions

The F01 claims below are scoped to the assumptions in the
[principal F01 derivation note](foundations/01_requirements_and_separating_examples.md).
F02 claims identify their own candidate and reconstruction notes in their sections.
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


## F02 partial candidate comparison — September 21, 2026

The following claims refer to [the candidate note](foundations/02_candidate_semantics.md)
and [53 exact development checks](checks/f02_candidates.py). Proof status means
conditional mathematical demonstration in that note, not the later calculus
soundness theorem. Review is same-agent and non-blinded; no novelty or independent
review is claimed. [The session](work_logs/F02_2026-09-21_S1.md) records 17.095003
credited D minutes: **at the end of S1, F02 was partial and D60 was not met**.
S2 completion is recorded below; the original timing and proof history is retained.
The philosophical commitments and all completed F01 claims remain unchanged.

| ID | Scoped statement and derivation location | Evidence / project impact |
|---|---|---|
| F02-C01 | At fixed units and a linear task evaluation, additive return values and fixed mixtures follow the scalar formulas; approximate scalar comparisons chain additively (§2). | Displayed finite-sum proof and exact fixtures. Positive scalar baseline; not arbitrary sequential-program value. |
| F02-C02 | Evaluated pointwise minimum equals the minimum of the evaluations iff one profile is pointwise no worse on positive-weight scenarios; the gap is `(E abs(x-y)-abs(E(x-y)))/2` (§3.2). | Nonnegative-part proof, 625 profile-pair checks and zero-weight case. Alignment matters for this nonlinear operation. |
| F02-C03 | A finite convex hull of linear task weights can be checked at its supplied generators; this compression need not preserve pointwise bottleneck evaluation (§3.3). | Convex-combination proof plus E03 counterexample. The admitted operations matter, not only the current query. |
| F02-C04 | Finite T expressions denote monotone common-shift-preserving maps, hence uniform-norm nonexpansive maps; primitive affine probability rows sum to one (§4.1-4.3). | Induction and sandwich proofs; exact finite tests. Excludes subprobability and arbitrary terminal-value amplification without new assumptions. |
| F02-C05 | Lower envelopes of affine expectations cannot represent controlled `max(h_L,h_R)` (§4.2). | Midpoint concavity counterexample. The proposed T permits min and max; pure lower semantics needs another control layer. |
| F02-C06 | Typed T sequencing yields `9/2` in the displayed two-stage case and optional signal value `max(1,4p-1-kappa)` under its joint-law/observation contract (§4.4-4.5). | Direct propagation and independent finite-policy checks. Immediate scalar equality does not preserve all future tasks. |
| F02-C07 | Stagewise lowering of shared-theta rewards theta and 1-theta gives zero instead of their exact total one; lower composition is exact for the displayed independent product-choice identity (§4.6). | Explicit common-model and product-choice calculations. Coupling and quantifier order cannot be reconstructed after erasure. |
| F02-C08 | For affine one-input maps with probability vectors p,q, uniform finite-error comparison on all real continuations forces p=q; on span<=M it is exactly `r-s+epsilon>=M TV(p,q)` (§4.7). | Analytic separating continuation and attaining box-vertex proof; all specified finite vertices checked. Relative task span can be bounded without bounding absolute value. |
| F02-C09 | Approximate T substitution composes with summed errors when the suffix maps its task family into the prefix's admitted family; omitting that condition admits the 0-versus-10 counterexample (§4.8). | Monotonicity/shift derivation and closure counterexample. Sufficient span propagation is proved separately. |
| F02-C10 | Singleton shift maps give S's additive fragment; the profile map `T_x(c)=x+c` does not preserve profile addition as ordinary function addition (§4.9). | Algebra and duplicated-continuation fixture. Representation is not automatically preservation of all operations. |
| F02-C11 | Finite G budget sets admit Pareto pruning, menu union, free-pair addition, and separate-feasibility intersection with the stated finite-set identities (§5.1-5.2). | Elementwise/set proofs and 125 front triples. Witness existence and compatible controlled choices are explicit premises. |
| F02-C12 | Menus A={(0,2),(2,0)} and B=A union {(3/2,3/2)} have identical nonnegative weighted optimum costs but different feasibility for budget (3/2,3/2) (§5.4). | All-weight analytic bound and 101 weight checks. Hard deterministic budgets may retain nonconvex options discarded by weighted optima. |
| F02-C13 | Marginal frontier addition can promise an incompatible cost-zero plan; immediate-cost pruning can lose a valid cost-one route. Matching-endpoint cost relations restore the demonstrated sequence (§5.5-5.6). | Explicit controlled-choice and endpoint countermodels, compatible-path proof and fixtures. Extra hidden policy compatibility still must be retained. |
| F02-C14 | Pure-output and added-lottery menus can induce the same optimized scalar continuation map for every h but different simultaneous mean-cost feasibility when free randomization is not otherwise admitted (§9.1). | Convex-average identity and exact mean-budget witness. Extensional map and syntax/menu are different information contracts. |
| F02-C15 | Robust coordinate maxima per action exactly characterize one-before-model action satisfying every component cap, but can lose later sum objectives; observing the model before choice gives a different intersection of menu capabilities (§9.2). | Quantifier equivalence and before/after fixtures. Nonprobabilistic compression is exact for its specified queries only. |
| F02-C16 | Strictly increasing exact recoding preserves scalar/profile/component orders with transported operations; a fixed bounded interval with ordinary addition is not the same unbounded carrier (§2.6, §3.6, §5.7). | Displayed inverse/operation formulas and recoding fixtures, reusing F01. No precision, tail, or runtime advantage follows automatically. |
| F02-D01 | S, P, T, and G are candidate foundations with different primitive meanings and admitted operations. | Proposed, not selected. Finite examples, retained information, costs, and limits are compared; full F01 coverage by one small candidate is unestablished. |
| F02-T01 | F02 has met every task-completion obligation. | **Established at the F02 comparison scope after S2:** four concrete candidates, multiple worked examples each, common comparison, explicit assumptions, 124 passing dedicated checks, and 61.118295 credited D minutes. Next F03 is unstarted; no core or gate is selected. S1 alone did not meet the minimum. |


## F02 continuation claims — September 22, 2026

Locations refer to [the S2 supplement](foundations/02a_candidate_reconstruction.md).
[71 new checks](checks/f02_continuation.py) and their
[report](checks/F02_continuation_results.json) complement the original 53 tests.
Statements are proved conditionally in the supplement unless explicitly scoped
otherwise. Review is same-agent and non-blinded. The max-min representation
input is attributed in the [source record](work_logs/F02_2026-09-22_S2_sources.md);
none of these claims is labeled novel, independently checked or a later gate.

| ID | Exact scoped statement and location | Evidence and project impact |
|---|---|---|
| F02-C17 | For nonempty finite cost menus, agreement of every nonnegative weighted optimum is equivalent to equality of convex upper hulls (§A.1). | Convex-combination and separating-point proof. Identifies exactly which hard-budget information is lost, not an impossibility for all scalar encodings. |
| F02-C18 | Free lotteries with expected deterministic costs replace the menu by its convex hull; per-use hard caps do not acquire the same relaxation. Mixing before a hidden-model worst case differs from mixing after it (§A.2–A.3). | Explicit feasible menus and 405 finite robust-mixture cases. Observation and aggregation assumptions cannot be omitted. |
| F02-C19 | Blind-before-input and observed-input branch maxima satisfy the stated inequality; equality requires a common maximizing branch on positive input mass. Two menus can give identical optimized maps for every continuation but different blind values (§B). | Nonnegative-gap proof and identity/swap versus constant-output witness; 405 observation cases. An extensional map can erase later-needed policy information. |
| F02-C20 | The exact affine output-span bound is `max_ab(r_a-r_b+M TV(p_a,p_b))`; suffix substitution can cancel differing prefix rows when `(p-q)Q=0` (§C). | Attaining continuation and row-product proofs; 675 span cases and exact cancellation fixtures. Gives less conservative task-family interfaces without bounding absolute stakes. |
| F02-C21 | All aligned coordinate-mask bottleneck tests recover a bounded profile when supplied scenario weights are positive; additive evaluations admit a mean-only closed fragment (§D). | Explicit coordinate inversion, 270 masks and positive additive control. Retained query family, not raw storage dimension, determines this distinction. |
| F02-C22 | Separate-feasibility intersection does not distribute through free-pair addition; bounded infinite menus can lack attained optima or finite Pareto fronts (§E). | Finite witness and `(1/n,0)` family. Different existential witnesses, closure and attainment must be stated. |
| F02-C23 | In the declared finite shared-model two-stage problem, stagewise lowering is exact iff some prefix-lower minimizer has zero suffix gap on its reachable support (§F). | Nonnegative-gap proof and 1296 finite cases. Forgetting uncontrollable dependence is conservative here; forgetting legal controlled-choice compatibility can instead be optimistic. |
| F02-C24 | Backward propagation of budget sets composes exactly along cost-labelled relations; fixed nonnegative scalarization preserves its weighted-cost recurrence. Fixed-weight endpoint min-plus kernels preserve all admitted later scalar continuations (§G). | Witness/path constructions and finite tests. Hard-budget probes need extra output structure; fixed-task scalar compression can be useful and exact. |
| F02-C25 | With freely supplied stochastic affine primitives and finite min/max/composition, scalar finite T expressions denote exactly global finite continuous piecewise-affine, monotone, common-shift-preserving maps (§I.1). | Forward induction, slope constraints and attributed max-min representation with worked reconstruction. This is extensional, not a theorem about a fixed physical primitive library or efficient representation size. |
| F02-C26 | The supplied four-piece map is neither convex nor concave but lies in T; `h -> 2h` fails the common-shift law and is not uniformly approximable on all real inputs by unit-shift maps (§I.2–I.3). | Explicit formulas and growing-shift argument; 1083 grid checks for the normal form. Unit-mass semantics is a substantive restriction, not a universal value principle. |
| F02-C27 | The smooth two-input log-mean-exp map is not exactly finite piecewise-affine, but the supplied eleven real-coefficient planes approximate globally within 1/32. Sixty-five exact rational planes give a certified global under-approximation error at most `1/32+2/1701<1/16` (§I.4–I.5). | Curvature/tail and relative-entropy bounds with explicit rational log intervals; finite fixtures do not establish the infinite-domain statement. No universal approximation or minimal-size theorem is claimed. |
| F02-C28 | Directed slack `d_s` exactly characterizes budget-set inclusion after a nonnegative scale shift; it obeys triangle, menu-union maximum, independent-sum additive and separate-intersection maximum bounds (§J.1–J.2). | Elementwise witness proofs; 343 triangle and 256 operation cases. Requires positive unit scales and the stated compatibility semantics. |
| F02-C29 | Equal scalar optimum functions need not bound hard-budget slack; upward grid rounding of finite cost fronts gives a conservative finite-precision repair under an explicit bounded range (§J.3–J.4). | Scalable menu counterexample and rounding proof. Does not impose a universal bound on value or preserve hidden implementation labels automatically. |
| F02-C30 | For convex upper hulls, the least directed slack equals `max_(w>=0,w.s=1)(f_B(w)-f_A(w))_+` (§J.5). | Separation proof and 256 two-dimensional comparisons against a direct mixture optimizer. This is the relaxed budget problem, not the nonconvex deterministic one. |
| F02-C31 | Boolean terminal tests and the original box vertices need not determine nonlinear T equality or order; a joint affine-region refinement gives a finite exact test on an explicitly supplied bounded-relative-stakes polytope (§K). | Exact legal T counterexamples and crossing enumeration. The finite repair assumes explicit pieces; no generic black-box efficiency or arbitrary-real algorithm is claimed. |
| F02-C32 | Quantizing absolute bounded codes can destroy bounded-relative-stake decisions. No continuous extension to the whole closed code square uniformly approximates the encoded arithmetic mean with error below one (§L.1–L.2). | Shared-code ambiguity and cancelling-large-value paths; fifteen path checks. The latter obstruction is for the closed-square continuous presentation, not every bounded encoding. |
| F02-C33 | Centering before encoding and retaining the common offset yields finite inverse-error and `2 delta` greedy-regret bounds on the declared span-bounded family; unit-shift normalization is necessary for offset cancellation (§L.3–L.4). | Lipschitz and simultaneous-error proofs, 153 centered-choice fixtures and row-mass counterexamples. Absolute queries still need the offset. |
| F02-C34 | The encoded output of a bounded-relative-coordinate presentation extends continuously in the encoded common offset, with the stated `(1+B)^2` offset Lipschitz factor (§L.5). | Explicit shift-fraction identity and endpoint limits. Encoded accuracy is not automatically absolute-real accuracy. |
| F02-C35 | The shared signal/cost example has the same supplied errors, prices, caps and observation schedule for S/P/T/G, producing the displayed feasible menus and values (§N). | Exact common fixtures. Additive resource propagation alone is not physical prediction-error propagation; the S1 common-table wording was narrowed accordingly. |

### Completion and next dependency

The current F02 comparison obligation is satisfied; 3667.097704541 cumulative
D seconds are recorded, not inferred from word count. F03 must audit the actual
candidate definitions and load-bearing mathematical results against primary
literature before Gate A. F04 must test the chosen candidates adversarially.
No downstream task has been started by the package, and there is no gate pass
to invalidate. A later flaw reopens the relevant claim and its uses, not the
historical record of what was attempted or tested.

## F03 partial literature audit

Status: **partial**; no new core, novelty disposition, independent review, or
readiness gate. [Source cards](literature/01_foundations.md),
[versioned locators](literature/F03_sources.json),
[bibliography](references.bib), and [mapping proofs](literature/01a_import_boundaries.md)
separate imported definitions from finite specializations. Source checks cover
only the specified passages, not every proof in every work. The
[31-test suite](checks/f03_imports.py) checks witnesses, not the source theorems.

| ID | Exact scope | Evidence and limitation | Downstream impact |
|---|---|---|---|
| F03-C01 | S01's abstraction results require complete ordered domains and stated map inequalities; M01 gives a powerset/interval instance and distinct query polarities. | Source locators checked; direct inclusion proofs and square/membership witnesses. | Overapproximate possible outcomes versus underapproximate feasible budgets according to the query, not a universal direction. |
| F03-C02 | S02's common-error max-metric rule excludes ordinary addition; M02's capped-sum lifting admits it on an unbounded real carrier. | Source definitions plus elementary metric/lifting proof; finite grid checks. No full completeness import. | A signature mismatch is not a no-go result for quantitative algebra or unbounded values. |
| F03-C03 | A finite affine transformer r+Ph preserves every common shift iff P has all row sums one. | M03 proof, finite duality and composition checks; S03 permits loss of mass. | Preserve F02's stochastic premise; a cemetery-state rewrite changes the continuation interface unless specified. |
| F03-C04 | S04 supplies the finite piecewise-affine representation step used in F02-C25; S05's general minimax can have infinitely many outer choices and separates positive from additive homogeneity. | Exact source hypotheses checked; M04 slope and majorant derivations. | No expression-size, restricted-library, policy-witness or finite-algorithm claim is inferred. |
| F03-C05 | G's finite union/Minkowski algebra does not automatically satisfy S06's arbitrary-join, unit/top, or multiplication-idempotence conditions. | M05 signed-unit and finite two-dimensional no-supremum proofs; explicit full-upper-set comparison; finite fixtures. | F02-C11's finitary result survives. The cited c-semiring/local-consistency results require separate hypotheses. |
| F03-C06 | Weighted optima of a finite menu characterize its convex upper image, not necessarily its unrandomized hard-budget feasibility. | S07 scalarization/separation passages and M06 direct specialization; equal-score/budget witness. | Preserve F02-C12/C17/C18's convexification and lottery interpretation. |
| F03-C07 | A shared latent choice cannot generally be replaced by independently pasted stagewise choices while preserving an exact robust value. | S08 rectangularity conditions; M07 value-one versus value-zero witness and relaxation argument. | Keep uncertainty and information schedules explicit; a conservative lower bound is not an equality claim. |
| F03-C08 | S10 permits arbitrary algebra operations but its quantitative substitution must preserve variable relations; zero fuzzy distance is not automatically equality. | Definitions 3.1–3.6/4.1 and theorem statements checked; M08 countermodels. | Do not delete soundness side conditions to admit amplification; full theory translation remains open. |
| F03-C09 | S11's relational variety/exactness results impose specific lifting/quotient conditions and are not an implemented complete deduction system. | Sections 3–6 inspected; source explicitly places the concrete deduction-system direction in further work. | Ordered or directed candidates have relevant antecedents, not automatic general metatheory. |
| F03-T01 | F03 satisfies all completion conditions including L60. | **Not established.** Partial session clock record gives credited L and remaining floor. | Continue F03; F04 and Gate A remain unattempted. |

A source-condition mismatch is recorded as a restriction on a prospective import,
not as a retroactive refutation of an already correctly scoped F02 theorem.
New contradictions in a used claim would require the roadmap's repair procedure.


### F03 S2: source-adapter and guarded-inference checks

The [continued audit](literature/01b_proof_system_audit.md) and
[39-check suite](checks/f03_proof_audit.py) add the following scoped results.
Proofs are the displayed elementary adapter arguments; source theorems remain
imports only under their own hypotheses. Numerical tests are not independent
certification of those full theorems. Source S12 is a targeted supplementary
addition, with publication and inspection metadata in the versioned manifest.

| ID | Exact scope | Evidence and limits | Import consequence |
|---|---|---|---|
| F03-C10 | A finite ordered variable-relation context encodes all its supplied quantitative premises; contextual substitution must preserve each ordered pair. Mean-zero classes need not be a congruence for minimum. | Section 2 and finite context/collision checks; S02's apparent reflection wording is an unresolved transcription/proof-step question, not a declared theorem refutation. | Preserve S10's guarded substitution and ordinary equality; no full typed translation established. |
| F03-C11 | The capped directed shortfall on real values admits the displayed triangle, sum and bottleneck bounds; scaled error lambda*epsilon requires epsilon<1, with separate saturated-endpoint treatment. | Section 2.3 proof; 6,561 tuple checks and explicit half-scale counterexample. | A bounded relation does not bound the value carrier or retain a finite error bound at the cap. |
| F03-C12 | S12's stated arithmetic uses 0*infinity=0 and the specified residual endpoints; sequent antecedent multiplicity matters, and infinite cancellation is invalid. Its completeness theorem is for the full finite-theory proof system. | Primary definitions/theorem hypotheses checked; section 3 arithmetic and 125-case adjunction fixtures. Full proof system and completeness proof not independently certified or implemented. | A relevant unbounded arithmetic antecedent, not an automatic Value Logic core. |
| F03-C13 | Finite nonnegative pairs encode finite signed polynomial values and comparisons, with exact sum, negation, product and min/max adapters. | Section 4 induction/identities and exact fraction checks; infinite pair coordinates are excluded. | Finite signed comparisons can be represented without choosing undefined infinite subtraction or claiming efficient proof search. |
| F03-C14 | The minimum over a finite nonempty menu of its maximum normalized violation is zero exactly when some option is feasible. Infinite infima and per-model witness choices do not preserve that common existential guarantee. | Section 5; 729 finite menu/budget cases plus attainment and quantifier countermodels. | Complete arithmetic reasoning does not recover lost alignment, observation access or a common implementation witness. |
| F03-C15 | A once-only finite variable elimination preserves the displayed joint optimum; copying a factor into a retained factorization changes total cost from three to five. | Section 6 exact table and factor checks. Not a counterexample to S06's idempotence-qualified propagation results. | Algebra match, solution preservation and termination remain separate solver-import obligations. |
| F03-C16 | Under the stated shared two-model reward table, optimal mixing has worst value 1/2; actionwise rectangular relaxation gives zero. Conditioning on survival can reverse a finite reward comparison. | Sections 7-8, finite mixing and row-mass identities; no infinite-horizon or general measurable-policy theorem imported. | Keep S08's actionwise uncertainty condition and S03/S05's mass/shift interfaces explicit. |

F03-T01 remains **not established**: the continuation is partial and L60 is not
met. See the [session record](work_logs/F03_2026-09-22_S2.md) and appended
[clock ledger](time_ledger.csv). No F01/F02 claim is marked refuted by these
hypothesis checks, no repair gate is opened, and F04 has not begun.
