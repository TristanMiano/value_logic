# F16 principal primary-source reading record

Contributor: **ChatGPT (GPT-6 Astra Pro)**. Read October 5, 2026 UTC.
This records the principal's new L work, separately from the concurrent
[contribution review](reviews/contribution_review.md). It is a targeted
comparison, not a systematic literature search. Retrieval waits are excluded
by the session clock. No outside paper's correctness theorem is imported as
a trusted rule of the project.

## Directly inspected primary sources

### Incremental abstraction-carrying code

Elvira Albert, Puri Arenas and Germán Puebla, **An Incremental Approach to
Abstraction-Carrying Code**, LPAR 2006, pp. 377–391,
DOI `10.1007/11916277_26`.
[Author-group manuscript](https://cliplab.org/papers/inc-acc-lpar06.pdf).

Read §§1–6, with special attention to §2 equations (3)–(4), §§3.1–3.2,
Algorithms 1–2, Definition 4, Theorem 1 and the storage tradeoff in §6.
This is the 15-page conference manuscript. Theorem 1 refers its proof to
a technical report, which the principal did not obtain or verify.

**Relevant content:** retained abstractions and dependency tables support
incremental checking; the updated information still faces a consumer-policy
test. Certificate reduction can remove information needed for later checks.
**F16 implication:** the broad revision/retention/reception architecture is
established. Its use here must be defended through particular application
consequences, with retention and reconstruction costs included.

Root web retrieval locators: `turn51view0`, `turn52view0`, `turn53view1`,
`turn54view1`, `turn55view4`.

### Computational optimal recovery

Mahmood Ettehad and Simon Foucart, **Instances of Computational Optimal
Recovery: Dealing with Observation Errors**, SIAM/ASA Journal on Uncertainty
Quantification 9(4), 1438–1456 (2021), DOI `10.1137/20M1328476`.
[Author manuscript](https://foucart.github.io/publi/OR_Uncertainty_v2.pdf).

Read introduction and §2.1, including definitions (1)–(9), the polytope and
error model (10)–(13), Theorem 1 and its complete LP-duality proof (14)–(19).
Later polynomial/function-space sections were exposed in retrieval but are
not part of this F16 comparison.

**Relevant content:** Theorem 1 computes a locally optimal sup-norm answer
for linear targets over a polytope consistent with bounded-error observations.
**F16 implication:** substituting a probability simplex, retained old means,
and revised linear costs supplies the ordinary answer method. The specialized
matrix ranks, explicit radii and attaining laws remain the application work.
The theorem's output is an answer vector; a decoder required to return one
feasible law has an additional constraint.

Root locators: `turn51view1`, `turn52view1`, `turn53view0`.

### Choquet identification: accessible precursor and limited journal preview

Henrique E. Oliveira, João M. T. Romano and Leonardo T. Duarte,
**Identificação dos Parâmetros da Integral de Choquet via uma Abordagem
baseada em Processamento de Sinais Esparsos**, SBrT 2017, pp. 692–696.
[Primary proceedings PDF](https://www.sbrt.org.br/sbrt2017/anais/1570362091.pdf).

Read all five pages, §§I–V: normalized-capacity definition, ordered-difference
formula, linear observation representation, constrained fitting, interaction
coordinates, and the described numerical setup/conclusion. Figure values were
not independently digitized or reproduced. The direct ordered-difference
definition motivates the principal's separate mathematical translation in
the reconstruction notes; that translation is the principal's inference.

Root locators: `turn53view2`, `turn54view0`, `turn55view0`–`turn55view2`,
`turn56view0`–`turn56view2`.

The later paper by Henrique Evangelista de Oliveira, Leonardo Tomazeli Duarte
and João Marcos Travassos Romano, **Identification of the Choquet integral
parameters in the interaction index domain by means of sparse modeling**,
Expert Systems with Applications 187, 115874 (2022),
DOI `10.1016/j.eswa.2021.115874`, remains only partly accessible.
[Publisher page](https://www.sciencedirect.com/science/article/abs/pii/S0957417421012331).

The root read the indexed abstract/introduction and the opening of §4 from
`turn57search0`. It distinguishes rank-based and sparsity-based identification,
then starts the linear system before truncation. **The substantive §4 theorem
and proof were not available.** The precursor is not a substitute for that
unread comparison; neither retrieval failure nor this scope establishes
worldwide priority.

## Retrieval failures and scope controls

- Direct opens of the journal URL and delegated reference returned internal
  errors (`turn53view3`, `turn55view3`). These were read-only retrieval failures.
- The first strict PII-plus-identifiability indexed query returned unrelated
  sources. None was used as authority.
- One revised exact-title query with the publisher domain returned the primary
  indexed preview, including the §4 opening. Its full-text theorem remained
  unavailable. No further access attempt or authentication bypass was made.
- One combined tool response was truncated after the relevant primary preview;
  the unrelated author-profile material was neither needed nor used.
- The principal did not count any concurrent delegated reading toward D/L/E/O.
  This record does not claim external-human or different-model independence.

The full bibliographic/query inventory of the separate reviewer is in
[source_record.md](reviews/contribution/source_record.md). Primary statements
are attributed above; additional comparison arguments are labeled as F16
reasoning rather than as claims made by those authors.

## Targeted follow-up: joint constraints and compatible centers

Read October 5, 2026 UTC. This follow-up narrows the comparison prompted by
F16-C1; it is not an exhaustive priority review. Query families included
`"optimal recovery" "Chebyshev center" "consistent" Foucart constraints`,
`"optimal recovery" "coherent" moment probability law center`,
`site:foucart.github.io "optimal recovery" constrained`,
`"relative Chebyshev center" "optimal recovery"`,
`"Chebyshev center" "shape" "optimal recovery"`, and the exact title of
the Paruchuri/Chatterjee paper below. Unrelated quantum, document-sharing and
profile results were discarded, without using their absence as evidence.

### Simon Foucart: vector-valued prediction

**Optimal Prediction of Vector-Valued Functions from Point Samples**,
Journal of Complexity 92, 101981 (2026), as listed in the author's
[publication inventory](https://foucart.github.io/papers.html).
[Author manuscript](https://foucart.github.io/publi/OR_Multivalued_v_final.pdf).
Read the abstract, introduction, Theorems 1–2, Proposition 4 and Theorem 8
with its support-function construction/proof. Selected computational passages
were inspected; this does not claim a full review of all 21 pages.

Convex joint restrictions, including dependent probability-vector components,
are already part of optimal recovery. The inspected results construct ambient
answer vectors with optimal global sup-norm error. They do not, in their
stated output contract, require the answer to be generated by a single law in
each observation fiber. **F16 inference:** joint dependence itself is not a
new contribution; F16-C1 needs its specific compatible-law construction and
conditional sharpness proof. No assertion is made that no other result in
this literature supplies a related extension.

Root locators: `turn61view1`, `turn62view0`, `turn62view3`, `turn62view4`,
`turn63view0`, `turn63view1`, `turn64view0`, `turn64view1`, `turn67view3`,
`turn68view0`, `turn69view3`.

### Simon Foucart: nonlinear estimation with convex models

**Optimal Algorithms for Nonlinear Estimation with Convex Models**,
[author preprint, version 5](https://foucart.github.io/publi/OR_NonlinearQ_v5.pdf),
accessed October 5, 2026. The inspected title page does not supply a publication
year; no publication status beyond the author's preprint listing is inferred.
Read abstract/introduction, Theorem 1 and the initial proof reduction, not the
complete 17-page paper.

The introduction treats a data/model-consistent estimate's generic factor-two
guarantee as established background. Theorem 1 concerns optimal sup-affine
estimation of a scalar supremum of linear functionals over a convex model
containing the origin. **F16 inference:** consistency and minimax reasoning
are established methods; that scalar theorem is not a direct proof of C1's
vector compatible-law result. The probability simplex also does not contain
the origin, so its hypotheses cannot be imported without an explicit change
of variables and target analysis.

Locators: `turn61view0`, `turn62view5`, `turn69view0`. One later direct URL
open returned an internal error (`turn68view1`); opening the previously
retrieved reference succeeded. This was a read-only retrieval failure.

### P. Paruchuri and D. Chatterjee: relative Chebyshev centers

**Attaining the Chebyshev bound for optimal learning: A numerical algorithm**,
Systems & Control Letters 181, 105648 (2023),
DOI `10.1016/j.sysconle.2023.105648`.
The author's [publication page](https://www.sc.iitb.ac.in/~pradyumn/homepage/publications.html)
links the primary [arXiv manuscript](https://arxiv.org/abs/2307.01304), version 1,
July 3, 2023, titled **A numerical algorithm for attaining the Chebyshev bound
in optimal learning**; [HTML](https://arxiv.org/html/2307.01304v1).
Read §§1–2, §3.1 reformulation, §3.2 regularization argument and §4.5's
optimization limitation. Not all numerical examples or figures were reviewed,
and this is not a full-text check of the later journal version.

A prescribed set of possible centers is an established relative-center
contract. The algorithm's guarantee depends on the required global
optimization; a local numerical result alone does not certify it.
**F16 inference:** the ordinary finite-polytope baseline can use exact LPs;
no practical-speed claim follows from a generic optimizer's existence. This
comparison uses the convex norm specialization, without endorsing every
broader quasiconvex reformulation in the preprint.

Locators: `turn62view1`, `turn63view2`, `turn64view2`, `turn65view0`,
`turn66view0`, `turn67view0`–`turn67view2`, `turn68view2`, `turn69view1`–`turn69view2`.

### Additional lead and retrieval limitations

- The publisher's Paruchuri/Chatterjee page returned HTTP 403 (`turn60view0`);
  a Chatterjee author-page request timed out (`turn60view1`). The other author's
  public page supplied the arXiv link. No access control was bypassed.
- Alexandre Goldsztejn's primary author survey/preprint,
  [Optimality Conditions for Multivariate Chebyshev Approximation: A Survey](https://arxiv.org/html/2310.01851v6),
  supplied targeted context from its abstract and §2.2 relative-center
  definitions. Other exposed snippets are not a full-paper review. Its cited
  2023 relative-center article and 2024 corrigendum were not read or treated
  as checked antecedents. Locators: `turn61search6`, `turn62view2`, `turn63view5`.
- A literal find for `global maximizer` in the arXiv HTML returned no match;
  the relevant optimization discussion was obtained by section reading.
- Author inventories and indexed journal metadata establish locators and
  bibliographic context; only the stated primary passages support substantive
  comparisons. No result is classified as first worldwide.
