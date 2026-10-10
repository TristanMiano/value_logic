# Ordinary antecedents for equal certificate delivery

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 10, 2026 UTC.
Task **R-P3-B-B**. DEVELOPMENT source reconstruction, with selected primary
sections read by the principal and a separate same-model source review.

## Reading scope and use

The recurrence concerns a Boolean/rational incumbent-sublevel loss certificate.
The closest ordinary antecedents are proof-producing decision diagrams and
certified compilation. The comparison must allow those methods to export
evidence; treating an ordinary diagram as an inherently uncheckable private
answer would create an artificial interface advantage.

The six records below identify the versions and selected sections actually
consulted. They do not claim a cover-to-cover reading or a systematic survey.
The principal opened the full primary documents and reconstructed the indicated
definitions and proof steps. No external benchmark number is imported into the
local cost comparison. Two initially guessed PDF locations failed; the working
author/arXiv locations below supplied the relevant material.

## Selected primary records

### Bryant — ordered decision diagrams

[R. E. Bryant, *Graph-Based Algorithms for Boolean Function Manipulation*,
IEEE Transactions on Computers 35(8), 1986; author's annotated PDF](https://www.cs.cmu.edu/~bryant/pubdir/ieeetc86.pdf).
Read: definitions 1–5, Theorem 1, parity discussion, Apply section, Table 1,
and annotations 4 and 7.

The fixed-order reduced representation is canonical. Memoized Apply bounds
distinct operand pairs by the product of argument sizes. A small resulting
diagram alone gives no corresponding bound on all intermediate construction.
The annotated complexity table distinguishes the original reduction cost
from later linear-reduction or amortized-hash assumptions. This motivates
separate node, operation, encoding and paid-work records here. It does not
supply a unit-cost model for arbitrary rational arithmetic or this Python
implementation. The local parity proof reconstructs its complete evidence
trace rather than borrowing a runtime claim from canonical root equality.

### Bahar and colleagues — algebraic decision diagrams

[R. I. Bahar et al., *Algebraic Decision Diagrams and Their Application*,
ICCAD 1993, author-uploaded proceedings text](https://www.researchgate.net/publication/215480876_Algebraic_Decision_Diagrams_and_Their_Application).
Read: §2 algebraic carrier and Boolean arguments, §2.1 ITE/Apply, and §2.2
representation and precision qualifications. The landing record also mentions
the later journal publication; the consulted four-page text is the 1993 paper.

This is the ordinary numerical-diagram antecedent: Boolean inputs may lead
to values in an algebraic carrier, and pointwise operations build new diagrams.
Exact representation depends on the carrier and precision convention. It does
not by itself provide an independently checkable certificate for our current
frame, loss units or incumbent sublevel. Our rational caps are explicit extra
implementation restrictions, not a theorem that every valid inherited input
admits an exact result within the new format.

### Darwiche and Marquis — compilation languages and scope

[A. Darwiche and P. Marquis, *A Knowledge Compilation Map*, JAIR 17,
2002; arXiv-hosted text](https://arxiv.org/pdf/1106.1819).
Read: §2 language and fixed-order definitions, Definition 3.1 on succinctness,
and the query/transformation tables including their conditional qualifications.

Representation succinctness is an existence comparison; it does not entail an
efficient compiler from arbitrary inputs. A tractable query applies after an
appropriate representation has been obtained, and supported transformations
vary by language. These distinctions prevent two invalid local inferences:
that a compact current root makes its construction free, or that a restricted
tree lower bound rules out a stronger ordinary proof language. No general
knowledge-compilation separation or complexity-theoretic assumption from the
tables is imported as a theorem about the finite P3-05 receiver.

### Sinz and Biere — checkable BDD conjunction

[C. Sinz and A. Biere, *Extended Resolution Proofs for Conjoining BDDs*,
CSR 2006, author-hosted PDF](https://fmv.jku.at/papers/SinzBiere-CSR06.pdf).
Read: §2.1 extension rules, §3 construction and its three proof obligations,
§3.1 simplifications, and §4 implementation interface.

Fresh variables define acyclic BDD nodes. Input clauses are linked to their
roots; recursive conjunction supplies implications; a final zero root closes
the refutation. The larger vocabulary does not license arbitrary replacement
of the original domain. Fresh complete definitions have a unique extension
for each input assignment. For a refutation, the required final implication
is weaker than full equivalence of every intermediate object. Our node/Apply/
expression checker is a finite service-specific reconstruction of this broad
proof-producing approach, not an invention of proof-carrying diagrams.

### Bryant and Heule — implication is enough for refutation

[R. E. Bryant and M. J. H. Heule, *Generating Extended Resolution Proofs with
a BDD-Based SAT Solver*, extended version, arXiv v4, March 27, 2023](https://arxiv.org/html/2105.00885v4).
Read: §§2.4–2.5 and §§3.1–3.3; the TACAS 2021 antecedent was identified
separately. The load-bearing source here is v4.

The proof invariant links each generated root to the original clause set.
Conjunction proof generation follows Apply dependencies and handles terminal
and tautological cases. Arbitrary existential quantification is justified by
a separate implication check. Thus sound refutation of the actual violation
query is a legitimate ordinary alternative to a complete exact-function
certificate. Our stronger denotational linkage is sufficient, not logically
necessary. Neither that paper's empirical scaling nor its checker guarantees
transfer automatically to the bounded Python service measured here.

### Bryant, Nawrocki, Avigad and Heule — certified compilation and shared lemmas

[R. E. Bryant, W. Nawrocki, J. Avigad and M. J. H. Heule, *Certified Knowledge
Compilation with Application to Formally Verified Model Counting*, arXiv v1,
January 22, 2025](https://arxiv.org/html/2501.12906v1).
Read: §2 preservation distinction, §7.2 final conditions and disjointness
restriction, §8.1 structural validation, §9.2 lemmas, and §10 soundness/trust.
The HTML labels these sections with a leading `0.`.

Shared subgraphs can become repeated tree traversals; checked conditional
lemmas avoid that expansion while retaining their activation conditions.
For counting, accepted steps and final conditions preserve input-variable
models and connect the root to the actual input. Structural partition checks
cannot borrow arbitrary input assumptions. The Lean result has stated parsing,
extraction, arithmetic and runtime trust boundaries. This work is a close
antecedent for sharing, guarded reuse and separate input linkage. Our project
neither implements CPOG nor inherits its formal verification. General RAT
equisatisfiability alone would not justify domain-wide loss or model counting.

## Consequences for this recurrence

The [local derivation](../derivations/05_equal_certificate_delivery.md) makes
three distinct claims. First, the new receiver checks a sufficient exact
Boolean/rational DAG proof of the actual current violation predicate. Second,
one concrete inherited tree calculus expands the forward/reverse parity
example, whereas an ordinary shared proof can remain polynomial under an
explicit uncapped schema. Third, fully paid finite delivery costs determine
which implemented method is cheaper on a declared stream. None of these
claims implies either of the others without its additional hypotheses.

The closest ordinary alternatives are therefore substantial: direct exact
checking, a fresh proof-producing diagram, a warm proof-producing diagram,
dependency-pruned fresh delivery, and independently admitted ordinary proofs
followed by the same portfolio kernel. The experiment implements these local
controls. A SAT/ER or CPOG compiler could be a further implementation route,
but it was not executed and is not assigned an invented cost.

For the source interpretation, the decisive preservation boundary is the
**actual complete violation query**. A sound refutation may preserve only
satisfiability along its steps. A replacement of the feasible domain that
merely preserves nonemptiness can still erase a violating rank tie. Likewise,
reusing a conditional lemma requires its guard, while reusing a checked
unconditional expression meaning does not require the old request's hard
assumptions. The local examples and induction establish these service-specific
points; they do not turn established shared reasoning into a unique value-logic
mechanism.

The contribution assessment must consequently credit the finite interface,
implementation, exact limitations and matched evidence. A claim of general
priority, proof-system superiority, improved calibration, an imported Logical
Induction guarantee, or a favorable final challenge would exceed this reading
and the development results.

## Review provenance

The independent same-model [source map](../work_logs/R_P3_B_B_2026-10-10_S1/reviews/literature_and_obstruction/source_map.md)
provided additional reconstruction. The principal checked the primary sources
above and owns the synthesis in this note. Reviews are nonblind development
checks. Their reading/execution time receives zero principal-clock credit;
the clock records only the principal's observed research intervals.
