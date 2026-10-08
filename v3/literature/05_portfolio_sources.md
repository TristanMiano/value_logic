# P3-05 S3 — portfolio and operation-sensitive comparison sources

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 8, 2026 UTC.
New selective source inspection during continuation S3. Earlier source cards
remain unchanged. These cards import interfaces, not worldwide-priority claims
or a complete reproduction of the papers' proofs.

## T05-S4: pointwise causal abstraction

Beckers and Halpern, *Abstracting Causal Models*, AAAI 2019,
[arXiv v4](https://arxiv.org/html/1812.03789v4), sections 3.1–3.3,
Definitions 3.5, 3.7, 3.12–3.13, Proposition 3.6 and its appendix proof.
Inspected HTML including the countable-intervention intersection argument.

The compatibility condition compares an abstracted intervened outcome with
the high-level intervened outcome at each low-level context. Uniformity over
context laws is stronger than equality for one selected law. The proof of
Proposition 3.6 uses countably many interventions to choose a context matching
all of them. Abstraction additionally constrains intervention maps through
state-restriction images. We reconstruct finite commuting diagrams directly;
we do not import unrestricted-domain existence, a search algorithm for the
right map, or runtime preservation. One-sided loss reuse needs less than a
full exact causal abstraction, but must prove its specific coverage and loss
bridge. This is an established comparator, not a new P3-05 idea.

## T05-S5: soft interventions expose unreachable-state differences

Massidda, Geiger, Icard and Bacciu, *Causal Abstraction with Soft Interventions*,
CLeaR/PMLR 213 (2023),
[primary PDF](https://proceedings.mlr.press/v213/massidda23a/massidda23a.pdf),
sections 5.2–5.3, Definition 9, Theorem 10 statement, Definition 11.
Inspected parsed text and PDF page 6 (zero-based 5). The later constructive
abstraction theorem and its full proof were not imported.

The paper distinguishes consistency on exogenously reachable outcomes from
consistency of structural functions on all endogenous settings. Distinct soft
interventions can agree on the former yet differ on the latter. Its stronger
soft-abstraction definition exposes that extra requirement; uniqueness is a
property under the specified abstraction contract. This is a close antecedent
to the danger of applying a proof after an edit opens previously excluded
states. Our portfolio checks a declared finite receiving domain, not every
state of an unrestricted program, and supplies no inference of logical
counterpossible dependence. No claim is made that simply tracking changed
function identities is novel.

## T05-S6: established composition and renaming

Rubenstein et al., *Causal Consistency of Structural Equation Models*, UAI 2017,
[arXiv PDF](https://arxiv.org/pdf/1707.00819), section 4.3, Definition 3,
Lemmas 4–5 and Theorem 6 statement. PDF page 4 (zero-based 3), including
its commuting diagram, was inspected visually.

Exact transformations preserve interventional distributions through a state
map and a surjective order-preserving intervention map. Renaming and
composition are already included. We do not rename these as new invariance
theorems. A finite task-output quotient below is an ordinary congruence
construction specialized to the declared edits, costs and statuses. Neither a
coarser representation nor equality of distributions automatically preserves
checking cost, hidden dependency information or a pointwise comparison.

## Inherited ordinary components and the remaining delta

The earlier [transport source cards](05_transport_sources.md) already include
incremental abstraction-carrying certificates and incremental MaxSAT. The
inherited [phase-two loss calculus](../../paper_v2.md#42-reuse-after-source-revision)
already provides proof alternatives and withdrawal penalties. Nonnegative
combinations of justified inequalities with a bounded residual are direct
arithmetic: their validity is proved in the companion, not imported from an
optimizer's success flag.

The S3 research target is narrower: join **partially applicable** stored
certificates into a single checked guarantee over all newly preferred cases,
with current assumptions, selection coverage and the receiving action pair
explicit. The ordinary method may use the same portfolio, positive-combination
certificates and symbolic simplifications. Useful integration or a precise
limitation requires its own concrete statement; identical implementation
availability does not itself settle contribution status.

BRIA remains a relevant named comparison for P3-06/07, not an imported theorem
for this static certificate receiver. No calibration, sequential-regret or
learning result is claimed here.

## T05-S7: exact-output minimization is established

Berstel, Boasson, Carton and Fagnot, *Minimization of Automata*,
[arXiv:1010.5318v1](https://arxiv.org/html/1010.5318v1), sections 2 and 4.1,
Propositions 2.1, 4.1–4.2. The manuscript contains both reconstructions and
original algorithm comparisons; only the stated congruence/refinement interface
is used here. The rendered timestamp is not used as its publication date.

Two deterministic states are equivalent when every finite continuation gives
the same acceptance result. The coarsest output-preserving congruence is found
by refining according to successor classes. Our edit alphabet and finite value
outputs specialize that construction. We use a simple bounded implementation,
not the paper's optimized algorithms or asymptotic performance claims.
Direct attempts to read the original Stanford Hopcroft scan and Princeton
Paige–Tarjan report failed (timeout/403); no full reading of them is claimed.

## T05-S8: overlapping compatible covers are also established

Kam, Villa, Brayton and Sangiovanni-Vincentelli, *A Fully Implicit Algorithm for
Exact State Minimization*, UCB/ERL M93/79, November 19, 1993,
[primary report](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1993/Archive/ERL-93-79.pdf),
section 3 introduction and Definitions 3.1–3.5 (printed pages 7–8; PDF pages
10–11). Definitions were checked in the scanned pages as well as extracted text.

Incompletely specified outputs permit overlapping compatible state sets. A
closed cover must cover the states and map each chosen set, on each input,
inside a chosen successor set. This is a close ordinary antecedent, not an
invention of value logic. The new application uses arbitrary acceptable-action
sets and checks their **whole intersection**. It does not import the source's
pairwise-compatibility characterization into that larger output contract:
three action sets can be pairwise compatible yet have no common action.
No BDD implementation, optimal synthesis performance or general complexity
claim is imported from the report.

## T05-S9: memoized ordinary decision diagrams

Bryant, *Graph-Based Algorithms for Boolean Function Manipulation*, IEEE
Transactions on Computers 35(8), 677–691 (1986),
[author's annotated PDF](https://www.cs.cmu.edu/~bryant/pubdir/ieeetc86.pdf),
Definition 5/Theorem 1 and sections 4.2–4.3, especially Figure 6.
The reduction statement and Apply pseudocode were visually checked on PDF
pages 5 and 14 (zero-based 4 and 13). Fixed variable order, merging equal
subgraphs and memoized operations supply a substantially stronger ordinary
comparator than enumeration. The annotated paper retracts its optimistic
output-sensitive Apply conjecture; it is not imported here. No polynomial
worst-case guarantee for arbitrary Boolean functions is claimed.

Bahar et al., *Algebraic Decision Diagrams and Their Applications*, ICCAD 1993,
188–191, sections 2–2.2, were inspected in an
[author-uploaded full-text copy](https://www.researchgate.net/publication/215480876_Algebraic_Decision_Diagrams_and_Their_Application).
The landing page says 1997, while the displayed copy's pages are the four-page
1993 proceedings paper. Arbitrary terminal values and pointwise Apply are the
relevant prior interface. The PDF download failed; only the displayed text was
used, not its unread tables or later matrix algorithms. The publisher's 1997
PDF URL returned an abstract page. The new comparator reconstructs the finite
rational recursion and checks it independently; it is not the authors' code.

## T05-S2 continuation: validating a certificate is not validating its use

The same Albert–Arenas–Puebla manuscript was re-opened in S3 at section 2,
equations (2)–(4), and section 3.2/Definition 2. PDF pages 4 and 7 (zero-based
3 and 6) were inspected. It explicitly separates checking the abstraction
from regenerating and checking the safety condition. It also warns that
certificate compression can remove information needed for later incremental
checking. Thus neither of those distinctions is new here. Our finite sublevel
coverage and loss request instantiate a particular receiving condition; ordered
portfolio replay supplies the stated restricted conditional result, not an
extension of the paper's entire logic-program analysis.

## T05-S10: epigraph and dual certificate antecedents

Boyd and Vandenberghe, *Convex Optimization*, with revised lecture slides by
Boyd, Vandenberghe and Nobel, [author-hosted slides](https://web.stanford.edu/~boyd/cvxbook/bv_cvxslides.pdf).
Inspected the epigraph/sublevel definition (PDF page 57), duality slides 5.8
and 5.12 (PDF pages 162 and 166), and parsed robust-optimization slides 4.23–24.
The dual expressions and weak/strong distinction were visually checked.
The full book URL failed; no full-book reading is claimed for this continuation.

An epigraph replaces a finite maximum of affine functions by linear upper
constraints; a feasible dual bound meeting a feasible primal value certifies
optimality. Our margin receiver proves that elementary inequality directly,
without trusting the capped basis search. The project adaptation is the
finite minimum over outside cases needed for **all-minimizer coverage**, not
new linear programming, robust optimization, or sensitivity theory. An
uncertain weight is universally quantified, not selected for favorable loss.
No solver-performance theorem is imported into the prototype.
