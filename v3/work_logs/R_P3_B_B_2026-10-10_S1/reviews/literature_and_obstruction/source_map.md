# Option B: primary-source map for independently checked diagrams

Contributor: **ChatGPT (GPT-6 Astra Pro)**, integration reviewer, October 10,
2026 UTC. **R-P3-B-B DEVELOPMENT; same-model, nonblind independent task.**
Principal-clock credit: **zero**. This is a selective primary-text inspection,
not a systematic literature review or a complete reproduction of the cited
papers. The local source bindings and access dispositions are in
[source_manifest.json](source_manifest.json).

## Finding and scope

Ordinary shared decision diagrams and independently checked proofs of diagram
computations have direct antecedents. The useful task here is a concrete bridge
for the existing finite Boolean/rational request and its complete delivery bill.
A lower bound for the inherited split-and-interval receiver must name that
receiver's inference rules. A restriction to decision trees alone does not bound
all tree-shaped algebraic proofs, much less proof DAGs.

The companion [tree obstruction](tree_obstruction.md) reconstructs the actual
old rules, including arbitrary current-row multipliers in a fresh portfolio.
No primary-source theorem is imported as a resource theorem for the new code.

## B-B-L1: reduced ordered BDDs and Apply

Randal E. Bryant, *Graph-Based Algorithms for Boolean Function Manipulation*,
IEEE Transactions on Computers 35(8), 677–691 (1986).
[Author's annotated full text](https://www.cs.cmu.edu/~bryant/pubdir/ieeetc86.pdf).
Inspected full-text passages: §1.1; Definition 5 and Theorem 1, PDF page 5;
§4.3/Figure 6, PDF pages 12–14; annotation 7, PDF page 14.

Theorem 1 concerns Boolean functions under the common fixed variable ordering
built into the graph definition: reduction gives a unique graph up to
isomorphism. It does not compare different orders or arbitrary proof systems.
Memoized binary Apply is bounded by the product of operand graph sizes under
the stated graph-operation model. Annotation 7 retracts an output-sensitive
conjecture. Imported: ordered Shannon recursion and sharing. Not imported:
cheap construction from arbitrary expressions, unit-cost unbounded arithmetic,
or proof validity from an exported root alone.

## B-B-L2: algebraic terminal values

Bahar et al., *Algebraic Decision Diagrams and Their Applications*, ICCAD 1993,
188–191. [Author-uploaded full text](https://www.researchgate.net/publication/215480876_Algebraic_Decision_Diagrams_and_Their_Application).
Inspected parsed full-text §§2–2.2, including the displayed proceedings page
188. This landing page also describes the later 1997 article; the inspected
text is the four-page 1993 paper. The publisher PDF request failed.

Section 2 defines diagrams for Boolean inputs and a finite algebraic carrier.
Section 2.1's Apply operates pointwise; its ITE requires a Boolean first
operand. This supports the ordinary representation interface. The local exact
rational extension still needs its own induction and bit-cost bounds; finite
input dimension alone does not make arithmetic or intermediate storage free.
No diagram-certificate theorem is taken from this paper.

## B-B-L3: representation size is a separate question

Adnan Darwiche and Pierre Marquis, *A Knowledge Compilation Map*, JAIR 17,
229–264 (2002). [Full text](https://arxiv.org/pdf/1106.1819).
Inspected Definition 2.1 and size convention, printed page 230; Definition 3.1
and Proposition 3.1, page 236; Appendix A/Table 10 discussion, page 248.

NNF size counts DAG edges. Definition 3.1 asks whether an equivalent
polynomial-size representation exists; it explicitly does **not** require a
polynomial-time translator. Some table separations carry polynomial-hierarchy
assumptions. The parity comparison with CNF/DNF is a representation-language
separation, not a certificate lower bound. We use only that distinction; the
exact leaf count in our companion is independently derived from the actual
receiver rules, without a complexity-class assumption.

## B-B-L4: proof generation for BDD conjunction

Carsten Sinz and Armin Biere, *Extended Resolution Proofs for Conjoining BDDs*,
CSR 2006, LNCS 3967, 600–611.
[Author-hosted full text](https://fmv.jku.at/papers/SinzBiere-CSR06.pdf).
Inspected §2.1; §3, PDF pages 4–6; §3.1; §4's trace/checker interface.

The construction introduces fresh acyclic node definitions, proves clause-root
units and conjunction implications, and derives contradiction when the final
root is false. These are full-text constructions, not a numbered general
succinctness theorem. Extension variables change the vocabulary: the extended
clause set is equisatisfiable, not literally equivalent over all variables.
The definitions and input linkage must therefore be checked as well as the
resolution steps. Imported: a concrete ordinary proof-export antecedent;
not imported: its timings or a bound solely in final-diagram size.

## B-B-L5: later proof-producing BDD operations

Randal E. Bryant and Marijn J. H. Heule, *Generating Extended Resolution Proofs
with a BDD-Based SAT Solver*. Inspected
[arXiv:2105.00885v4](https://arxiv.org/pdf/2105.00885v4), dated March 27, 2023,
an extended version of the TACAS 2021 paper: §§2.2–2.3 and 3–3.3,
especially Figure 3 and the maintained implication invariant.

The BDD manager associates node definitions and proof identifiers with
computations. Conjunction follows recursive Apply; a quantified result is
checked through the required implication. Unsatisfiability certification needs
that implication, not an assertion that every elimination preserves full
formula equivalence. This is a useful distinction for our bound service.
The paper supplies an established proof-producing ordinary method. It does
not certify the repository's rational adapter or provide its construction,
export, edit or storage costs.

## B-B-L6: compiled-DAG certification and its trust boundary

Bryant, Nawrocki, Avigad and Heule, *Certified Knowledge Compilation with
Application to Formally Verified Model Counting*.
[arXiv:2501.12906v1](https://arxiv.org/pdf/2501.12906v1), January 22, 2025;
extended from SAT 2023. Inspected Definition 2, §§7.1–7.2, and §10/Theorem 1.

Partitioning requires disjoint product dependencies and disjoint sum models.
Theorem 1 yields input-CNF/root equivalence after accepted steps and the final
state consisting of root unit plus defining clauses. Footnote 3 excludes input
clauses from a sum's disjointness hint: allowing them caused a soundness bug.
Section 10 states the formal-checking result and remaining parser, extraction
and runtime trust. Imported: proof/representation separation and precise
conditional-versus-global scope. Our proposed finite rational checker is a
new implementation; it inherits neither Lean verification nor CPOG's counting
claims.

## Design consequences for this recurrence

1. Bind a certificate to the receiver's independently supplied current
   expression, semantics/source version, bit order, unit and complete request.
   A valid graph with a maliciously substituted root is insufficient.
2. Check every imported node and operation dependency before admitting its
   result. Sharing may avoid duplicate checks, but only for already validated
   identities in the same semantic environment. Scope-conditional bounds must
   not become unconditional expression denotations after an edit.
3. For a bound over the current incumbent sublevel, it suffices to certify that
   every actual violation is included in a checked empty bad set. Exact
   expression-to-root semantics is a stronger, straightforward route. Check the
   incumbent separately to establish nonemptiness; an empty bad set alone does
   not establish a nonempty service domain.
4. Account for all constructed and visited intermediates, proof encoding and
   output, receiver input, checking, arithmetic bit work, retained nodes,
   dictionaries and source setup. Final-root size is an inadequate bill.
5. Permit ordinary DAG export, exact-table evidence, algebraic preprocessing,
   valid old certificates and the candidate's own proof kernel as controls.
   Classify any advantage under the actual common receiving service and tariff.

These are proposed review criteria, not a verdict on code that was not yet
available at the initial inspection. No producer, receiver or policy execution
was performed for this note.

## Access limitations

Every load-bearing card above uses selected full-text passages. No card is
based solely on an abstract. Other search leads, including projected knowledge
compilation and quantified-Boolean dual proofs, were not imported. Web PDF
screenshot requests returned text placeholders without visible image pixels;
there is **no visual PDF or live-render validation claim**. The underlying
parsed passages and independently reconstructed arguments supply this review.
