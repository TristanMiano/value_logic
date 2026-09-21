# Phase Two Claim Ledger

Version: F01 bootstrap, September 20, 2026.
Task status: **partial because the protected derivation minimum remains unmet**.
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

## Commitments, design defaults, and unproved targets

| ID | Role and statement | Status |
|---|---|---|
| F01-P01 | Epistemic nonfinality, pragmatic model use, and investigation of value as primary motivate the project. | Author-approved commitments, not derived metaphysical theorems. |
| F01-D01 | R01-R09 are conditional capability requirements for admitted queries; candidates may explicitly restrict their fragment. | Provisional requirements supported by examples, revisable through the queue. |
| F01-T01 | A useful calculus can be selected and proved sound with a nontrivial characterization result. | Research target; unproved. No core, general soundness theorem, completeness theorem, or Gate A-D pass exists yet. |
| F01-T02 | A candidate reasoner will offer a measured practical benefit over declared baselines. | Untested future empirical question, not established by the fixture tests. |
| F01-T03 | F01 satisfies all of its completion conditions. | **Not established: D60 is not met.** Keep F01 selected and unchecked. |

## Dependency and repair policy

The operational requirements depend on their named example assumptions, not on
an adopted universal semantic carrier. F02 should compare candidates against the
same fixtures and information access. Later rules must cite the exact premises
needed by each reused claim. A counterexample to an example calculation repairs
F01 and its downstream uses; a candidate's deliberate restriction is recorded
as a capability limit rather than concealed. No mathematical gate has yet been
attempted or invalidated.
