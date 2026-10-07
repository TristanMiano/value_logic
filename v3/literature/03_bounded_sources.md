# P3-03 — Bounded reasoning: source and comparison contracts

Contributor: **ChatGPT (GPT-6 Astra Pro)**, with same-model internal,
nonblind source reconstruction by `/root/bounded_sources`.
Selected passages inspected on **October 7, 2026 UTC**.
Scope: a bounded finite information/update process, its ordinary counterparts,
and the distinction between warranted loss bounds and learned point estimates.

This note resumes the [P3-A choice](../checkpoints/A_1.md) and
[P3-01 source contracts](01_source_contracts.md). It does not reopen P3-01,
claim a new Logical Induction theory, or survey worldwide priority. Source
definitions are inherited; the finite arguments and implementation obligations
below are our reconstruction and adaptation.

## 1. Selected primary sources

| ID | Primary source and inspected version | Selected locators |
|---|---|---|
| P03-S1 | Garrabrant, Benson-Tilsen, Critch, Soares and Taylor, [Logical Induction](https://intelligence.org/files/LogicalInduction.pdf), 2016 author PDF, 131 pages | Definitions 3.2.1–4 and 3.3.1; §4 standing assumptions; Theorems 4.1.1–2 and 4.2.1; §5.5, Proposition 5.5.1 |
| P03-S2 | Patrick and Radhia Cousot, [Abstract interpretation: a unified lattice model for static analysis of programs by construction or approximation of fixpoints](https://cs.nyu.edu/~pmc309/publications.www/CousotCousot-POPL-77-ACM-p238--252-1977.pdf), POPL 1977, pp. 238–252, author-hosted scan | §6, p. 242, especially 6.0–6.5; §9.3, pp. 247–248; §9.5, p. 249 |
| P03-S3 | Johan de Kleer, [An assumption-based TMS](https://dekleer.org/Publications/An%20Assumption-Based%20TMS.pdf), *Artificial Intelligence* 28(2), 127–162, 1986, author-hosted scan | §1.1, pp. 129–130; §§4.2–4.4, pp. 142–148; §§4.7–4.9, pp. 150–153 |
| P03-S4 | Halpern and Pucella, [Probabilistic Algorithmic Knowledge](https://www.cs.cornell.edu/home/halpern/papers/probalgk.pdf), 26-page author manuscript; [LMCS publication record](https://lmcs.episciences.org/2261), 2005 | §2, pp. 3–5; §5 opening examples, p. 10; §5.3, pp. 18–20 |
| P03-S5 | A. M. Turing, [On Computable Numbers, with an Application to the Entscheidungsproblem](https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf), 1936 paper, pp. 230–265 | §8, pp. 246–248; eventual specified-symbol printing obstruction on p. 248, also visually checked by the principal |

### P03-S5 — later targeted obstruction check

The fifth source was selected after the first development run to sharpen the
unbounded-extension boundary. Turing's §8 rules out a decider for whether an
arbitrarily described machine ever prints a specified symbol. The project
reconstructs the simulation reduction to modern halting, then the contradiction
from waiting for an eventually accepted sound positive or negative certificate.
Its separate pointwise-convergent simulation estimate is proved directly.
Neither modern interface is attributed verbatim to the historical paper.
See the [exact addendum](../work_logs/P3_03_2026-10-07_S1/reviews/halting_certificate_obstruction.md)
and principal §9.1. This is classical background adapted to the status contract,
not a new undecidability theorem or a lower bound against every restricted method.

### P03-S1 — eventual deduction and anticipatory induction

$`D_n`$ is a computable nested finite sequence. Its assessment worlds obey
Boolean composition; $`\Gamma`$-completeness means
$`PC(D_\infty)=PC(\Gamma)`$. Section 4 assumes consistent, computably enumerable
$`\Gamma`$ and a market satisfying the induction criterion. Efficient emission
means polynomial time on unary input $`n`$; it does not bound the inductor's
own runtime by the same polynomial.

Fixed-sentence convergence and coherent limiting probabilities are
Theorems 4.1.1–2. Theorem 4.2.1 is stronger than waiting for each proof: for
every efficiently emitted sequence of theorems, $`P_n(\phi_n)\to1`$, with the
dual statement for disprovable sentences. Section 5.5 leaves practical runtime
tradeoffs open; Proposition 5.5.1 rules out a computable general theoremwise
convergence modulus under its representability assumptions.

**Disposition:** selected definitions/statements rechecked, not the full
construction proof. P3-01's S16 correction boundaries remain controlling;
the unrestricted finite-day perturbation and conditioning-closure claims are
not imported. P3-03 needs its own finite guarantee and resource account.

### P03-S2 — sound abstraction and decreasing approximation

Section 6 compares an abstract computation with a concrete one using
abstraction and concretization maps. Order preservation, concrete containment,
and a local transfer condition support the global consistency result. The
abstract answer may contain extra concrete possibilities.

Section 9.3 refines an upper approximation of a least fixpoint through a
sound decreasing sequence. Its termination devices have stated order and
stabilization conditions. A timeout by itself is not that construction.
Section 9.5 distinguishes approximation directions and which fixpoint they
bound.

**Disposition:** sound approximation and refinement are inherited methods.
The finite cover invariant below is an elementary specialization proved
directly; it does not invoke the entire fixpoint theory or implement a general
abstract interpreter. The scanned pages were inspected visually because the
PDF has no usable text layer.

### P03-S3 — dependencies, incomplete propagation and withdrawal

The problem solver supplies justifications; the ATMS records assumption
environments supporting conclusions. Completed labels are consistent, sound,
complete and minimal relative to those justifications. Context membership
uses a supporting-environment subset test. These are properties of supplied
inferences, not independent validation of their application meanings.

Section 4.7 states that label consistency and completeness need not hold
before its propagation algorithm terminates. Section 4.9 represents
defeasibility with an added assumption; it also discusses direct withdrawal,
recursive consequence invalidation and recomputation. Removing a recorded
inconsistency can affect previously subsumed environments and many labels.

**Disposition:** dependency-sensitive retention and reopening have a strong
ordinary predecessor. P3-03's interruptible cover/cache protocol requires its
own intermediate-state invariant. No general speed advantage, completed-label
guarantee at arbitrary interruptions, or full ATMS implementation is imported.

### P03-S4 — an algorithm's answer has its own semantics

Section 2 uses terminating knowledge procedures returning Yes, No or unknown.
The explicit-knowledge predicate holds when the procedure says Yes; No and
unknown both fail that predicate. In particular, generic No is not a theorem
of the queried sentence's negation. Soundness is an additional condition.

The state-access discussion requires the modeler to prevent use of unavailable
global information. Section 5.3 distinguishes conditional response reliability
from a posterior over hypotheses; selected evidence bounds additionally use
complete procedures and the stated observation model.

**Disposition:** the procedure/knowledge/reliability distinctions are inherited.
P3-03 must use separately checked positive and negative evidence and declare
any probabilistic adapter. **Locator correction:** P3-01 S12 placed the
unavailable-global-state warning in §4; it is in §5's opening examples,
printed p. 10 (PDF index 9). This corrects a locator, not the inherited claim.

## 2. An ordinary finite reconstruction of the proposed service

The following argument is ours, using finite set inclusion. It explains why a
constraint-and-loss implementation belongs in the ordinary comparison scope.
It is not a new abstract-interpretation or probability theorem.

Fix a finite set of active Boolean coordinates $`Q`$ and actually admitted hard
constraints $`H`$. Let

```math
V_H=\{x\in\{0,1\}^{Q}:x\models H\}.
```

This is a mathematical target set; defining it does not provide its enumeration
for free. A computation may instead maintain a finite frontier of partial
assignments $`F`$, whose represented completion sets have union $`U_F`$. Start
with the all-unassigned cell, so $`V_H\subseteq U_F`$.

Splitting a cell into its two children preserves its completion set. Removing
a cell only after a sound check that it violates $`H`$ preserves
$`V_H\subseteq U_F`$. If a new constraint is admitted before the frontier has
been filtered against it, the old cover still contains the smaller target
set. It is a valid outer cover, although it may contain assignments violating
the newly admitted constraint. That distinction must be visible in the output.

For a requested loss $`g`$ and nonempty $`V_H`$, suppose every cell has a computed
enclosure $`[l_f,u_f]`$ valid on its represented completions. Then

```math
\min_{f\in F}l_f\ \le\ \min_{x\in V_H}g(x)
\ \le\ \max_{x\in V_H}g(x)\ \le\ \max_{f\in F}u_f.
```

If the intended valuation $`x^*`$ satisfies the hard premises, this also bounds
$`g(x^*)`$. A learned point estimate is a separate record and cannot justify
discarding a completion without a sound bridge.

This proof gives ordinary constraint propagation, a finite abstract domain and
branch-and-bound a direct route to the same warranted-loss service. Candidate
and comparator can share a frontier, checker, arithmetic, dependencies and
stopping policy. Their cost and information parity is then an implementation
question, rather than a distinction created by renaming the output a value.

### What remains to be paid or proved

| Operation or property | Concrete obligation |
|---|---|
| Frontier construction | Charge parsing, allocation, splitting, constraint checking and storage. A symbolic initial cell is not a free list of $`2^{|Q|}`$ assignments. |
| Semantic coverage | Show why admitted hard constraints hold under the intended theory/interpretation or execution semantics. An arithmetic certificate proves its declared problem. |
| Loss enclosure | Compute a valid enclosure for the actual expression and rational inputs. Signed coefficients require directed interval endpoints; repeated variables can make naive interval bounds loose. |
| Finite coherent source | Distinguish a certified cover from exact satisfaction of every represented constraint. A probability supported on an unfinished outer cover may violate a newly received constraint. |
| Intermediate output | Publish an old valid snapshot or a newly certified intermediate result. A half-mutated frontier or incomplete dependent cache is not an implicit certificate. |
| Exhaustion | An empty frontier means inconsistent admitted constraints only if pruning and coverage were sound. Return typed conflict; do not use vacuous minima as a numeric answer. |
| Future information | Admit only receipts actually available. Ground-truth labels and offline final assignments used for evaluation are not live features. |
| Resource ceiling | Bound declared operations and rational bit lengths, or return a typed limit before publication. A single arbitrarily expensive host-language call is not one fixed-cost primitive. |

## 3. What convergence of the bounded process could establish

There are three distinct quantifiers.

**Fixed finite snapshot.** A fair exhaustive refinement of a fixed finite
fragment terminates if each scheduled primitive terminates, storage remains
available, and enough cumulative resources are supplied. With exact leaf
evaluation it can recover $`V_H`$ and exact extrema. The exponential worst case
has not disappeared. A fixed hard ceiling can stop before this happens.

**Fixed eventually settled query.** If a sound positive or negative certificate
for a retained query is eventually supplied, its checking is eventually
scheduled to completion, and the relevant scope remains stable, its status can
eventually settle. A proof enumeration only provides this for claims provable
or refutable in the specified system. Failure to find either certificate does
not decide a true, false or independent arithmetic claim.

**Growing query stream.** The preceding statements do not yield a bound at
the time each new query is asked. For a simple separating receipt policy,
activate $`q_n`$ on round $`n`$, provide its positive certificate only on round
$`2n+1`$, and otherwise keep its two Boolean possibilities. Every fixed query
eventually resolves, but the current query always has interval $`[0,1]`$.
A midpoint forecast therefore stays $`1/2`$ on these positive queries. This is
an obstruction to the stated receipt-only policy, not a lower bound on every
bounded reasoner: another same-access procedure might infer a useful common
pattern from the query descriptions or earlier evidence. P3-03 must not award
that unimplemented inference to the cover invariant.

Consequently, finite containment and fixed-query settlement can make precise
progress on U01–U05 at a restricted scope while leaving anticipatory U06,
calibration, expert regret and paid-policy improvement separate. This allocation
uses the project's [duty matrix](../foundations/01_desiderata.md), not a claim
that the four sources share one performance criterion.

## 4. Withdrawal changes the inclusion direction

Within a stable scope, adding hard premises shrinks $`V_H`$. Old upper covers
remain covers, and a previously justified lower/upper interval remains valid
for the narrower target while it is nonempty. Neither fact makes a new
narrower bound free.

Withdrawing a premise can expand $`V_H`$. Consider one coordinate $`q`$, an old
premise $`q=1`$ and loss $`g(q)=q`$. The completed old cover is $`\{1\}`$ and its
bound is $`[1,1]`$. Remove the premise: the new target is $`\{0,1\}`$, so carrying
the old cover forward loses a valid case. Invalidation of a dependency label
alone cannot recreate the lost case. The system must restore saved branches,
recompute a covering source, or return a broader previously certified fallback.

A smaller retained summary can still suffice. For a new task with constant
loss $`h(q)=7`$, $`[7,7]`$ is valid without recovering either assignment. Thus
reopening is specific to the changed source, dependency and consumer. This is
the operational counterpart of P3-02's distinction between full source
recovery and recovery of a requested loss family.

Versioning should therefore preserve the historical certificate and its
premises, mark its current eligibility separately, and charge any new source
construction or transport proof. Exact unchanged dependencies can justify
selective reuse. Removing a relevant assumption, changing the payoff meaning
or increasing the represented query family can require more retained data.

## 5. Point probabilities and fair contribution scope

A feasible assignment set does not choose weights. Even a default uniform
rule depends on its chosen presentation: two cases with $`q=0,1`$ give mean
$`1/2`$, while splitting the $`q=1`$ case into two unweighted aliases gives mean
$`2/3`$. Their image under the query $`q`$ is still $`\{0,1\}`$. Preserving a
probabilistic interpretation under this refinement requires transporting mass,
not resetting it uniformly. The interval $`[0,1]`$ is unchanged.

This finite calculation motivates an explicit probability/credal adapter;
it does not forbid using a justified prior, empirical model or learned
forecast. Each must retain its own interpretation and error or reliability
contract. A semantic payoff, its subjective expected loss, an algorithm's
estimate and an observed realized loss remain separate quantities.

The named comparison scope is **ordinary bounded constraint reasoning plus
loss queries, with an optional finite probability/credal adapter and dependency
maintenance**, under the same receipts, available procedures, precision,
retention and resource account. It may use the candidate's complete code.

| Disposition | P3-03 content |
|---|---|
| Inherited | Finite Boolean constraints, sound approximation, justification dependencies, conditional probability/loss semantics and the source-specific learning distinctions. |
| Reconstructed | The finite cover/extrema argument; the addition/withdrawal separator; the fixed-query versus current-query separator; the alias-weight calculation. These are elementary arguments supplied explicitly for this interface. |
| Adapted | A concrete bounded producer, atomic publication and dependency-aware repair protocol, when actually specified and checked in P3-03. |
| Open | A demonstrated benefit beyond the matched ordinary combination; anticipatory learning, calibration and paid-policy performance at a stated scope; stronger expressivity with justified cost/error control. |

The existence of ordinary reconstructions does not make an implementation or
well-scoped combination uninformative. It does determine what must be named
as inherited and what further evidence a contribution claim needs.
**P3-N01 remains NOT YET SUPPORTED** unless a later explicit assessment changes
its disposition. Neither this source note nor finite development results can
silently make that change.

## 6. Reading and version boundaries

The repository reading starts from main commit
`c573b58165826b30ccbb78107ea752169531c45a`, source tree
`a0e5782e554cac6946ef2de23106bae092e551d2`. Notation-only rendering repairs
made in this task do not alter the source hypotheses used here. The
[source comparison review](../work_logs/P3_03_2026-10-07_S1/reviews/source_comparison.md)
records the inspected historical file hashes and retrieval locators.

P03-S1 and S4 selectively revisit already used sources. S2 and S3 add focused
ordinary comparison contracts. The remaining archive was not reread. No
published theorem is imported outside the stated passages and hypotheses;
no full proof-assistant verification, final challenge exposure or new
scientific execution is claimed by this literature task.

## 7. Final additions: exact limits of the imported comparisons

The principal revisited the author PDF's Logical Induction Theorem 4.2.1 and
its C.3 proof specifically against the new U03-8a task-proof equivalence.
Our result eventually finds a proof of one fixed finite Boolean task
predicate if such a proof exists. The LI comparison concerns the day-indexed
prices of an efficiently emitted sequence and rests on its own induction
criterion and standing theory hypotheses. Relabelling the fixed task
predicate as a loss does not transfer that stronger sequence guarantee.
The prototype's explicit VM work bound instead comes from its stated finite
horizons, retained replay, frontier and evidence caps.

The principal also visually inspected Cousot and Cousot's printed pp.242–243,
including the local consistency conditions and the opening discussion of
ordered abstract interpretations. The new capped-cover example in companion
§5 establishes directly that one particular two-cube class lacks a least
enclosure for a three-point source. It does not contradict the source's
lattice results: that arbitrary cap is not shown to meet their hypotheses.
Our safety argument needs only the concretization containment preserved by
its actual transitions. No universal best abstraction, transfer transformer
or cost-optimal cover construction is borrowed from the cited framework.

These checks resolve the comparison scope of the new corollaries; they do
not repeat the earlier full source orientation or add a new scientific run.
The [task-proof review](../work_logs/P3_03_2026-10-07_S1/reviews/proof_stream_task_certification_addendum.md)
and [finite minimum review](../work_logs/P3_03_2026-10-07_S1/reviews/loss_minimum_recovery_review.md)
record the independent mathematical checks and their nonempty-source,
encoding, exactness and loss-family qualifications.
