# F16 contribution review: sources actually inspected

Contributor: **ChatGPT (GPT-6 Astra Pro)**, delegated separate reviewer.
Access date: **October 5, 2026 UTC**. This is a targeted primary-source
comparison, not a systematic review or a worldwide-priority claim.
Concurrent principal-clock credit: **zero**.

The parent must open any external primary source itself before citing it in
the root answer. Web reference IDs below are retrieval locators for that
handoff; the durable bibliographic references are the linked titles/URLs.
No external code, experiments, private account or authenticated source was used.

## A. Incremental abstraction-carrying code — main new comparison

**Elvira Albert, Puri Arenas and Germán Puebla. _An Incremental Approach to
Abstraction-Carrying Code_.** LPAR 2006, Lecture Notes in Computer Science
4246, pp. 377–391. DOI: `10.1007/11916277_26`.

- [Primary author-group PDF](https://cliplab.org/papers/inc-acc-lpar06.pdf),
  15 pages; conference manuscript, not the distinct January 2007 short note.
- [Publisher metadata](https://link.springer.com/chapter/10.1007/11916277_26).
- Web locators: `turn22search0`, `turn23view0`, `turn31view0`.
- Actually read: abstract; §§1–2; §§3.1–3.2; the incremental algorithm and
  explanation in §5, including Definition 4 and Theorem 1; §6 conclusion.
  Relevant PDF pages 2–7 and 11–14. Web lines 81–146 (separate validity/policy
  test), 175–194 (answers/dependencies), 224–271 (updates and reduction limit),
  438–475 (current update/rechecking), 518–551 (theorem and storage tradeoff).
- Theorem 1's proof is referred to technical report CLIP3/2006; that proof was
  not obtained or independently verified here. No soundness result is imported
  into the repository from this reading.

**Read-content paraphrase:** ACC separates certificate fixpoint checking from
consumer-policy compliance. For updated programs it retains answers and
dependencies, validates incremental certificates, propagates affected changes,
and tests the reconstructed updated information against the policy. It notes
that reducing a certificate can remove information essential to later
incremental checking. Its concluding assessment charges retained certificates
and dependencies against transmission/checking savings and update frequency.

**Comparison judgment:** This is a close established assembly for the broad
revision/retention/rechecking story. It does not evaluate the reset-price
observation matrix in the inspected sections. A claim limited to that
application's explicit quantitative consequences remains a separate question.

## B. Original proof-carrying code — consumer interface and validation

**George C. Necula. _Proof-Carrying Code_.** POPL 1997, pp. 106–119.
DOI: `10.1145/263699.263712`.

- [University-hosted primary paper](https://courses.grainger.illinois.edu/cs421/fa2010/papers/necula-pcc.pdf),
  14-page manuscript copy; PDF text extraction has damaged glyphs.
- Web locators: `turn23view1`, `turn31view1`, `turn25view2`.
- Actually read: introduction and §2 overview, PDF pages 1–3, especially
  consumer safety-policy/interface, certification and validation; conclusion
  excerpt, PDF page 10. Selected Appendix A safety-precondition statement
  was exposed by search, but no claim of a full proof reread is made.
- Exact main locators: web lines 149–248; 1048–1079.

**Read-content paraphrase:** The consumer declares both authorized operations
and an interface with invocation/return conditions. The producer supplies a
proof for that policy; the consumer validates it and relies on its own policy
and checker. Certification can be separated from later repeated execution.
The claimed protection is relative to the specified safety policy.

**Comparison judgment:** The general consumer-specific certificate-binding
idea is established. Matching an old proof to a new loss request is a specific
application of that requirement. This reading does not verify the repository's
current Python implementation or transfer PCC's performance results.

## C. Computational optimal recovery — renewed direct theorem inspection

**Mahmood Ettehad and Simon Foucart. _Instances of Computational Optimal
Recovery: Dealing with Observation Errors_.** SIAM/ASA Journal on Uncertainty
Quantification 9(4), 1438–1456 (2021), DOI `10.1137/20M1328476`.

- [Primary author manuscript](https://foucart.github.io/publi/OR_Uncertainty_v2.pdf),
  21 PDF pages, filename `OR_Uncertainty_v2.pdf`. No assertion that the file
  is byte-identical to the journal typesetting or that the filename supplies
  an arXiv version number.
- Web locator: `turn36view0`.
- Actually read: introduction equations (1)–(9); §2.1, Theorem 1 and its
  dual-LP proof, equations (10)–(19), PDF pages 1–5. Later function-space
  theorems were not required or used.
- Exact locators: web lines 28–120, 124–209.

**Read-content paraphrase:** The framework recovers a linear quantity from
linear observations and a model set, allowing bounded observation errors.
It distinguishes local from global worst error and defines the compatible
set. For a polytope model and coordinatewise bounded errors, Theorem 1 gives
an LP for a locally optimal sup-norm center; its constraints are obtained
from LP duality.

**Comparison judgment:** Set the model to the probability simplex, observations
to retained old means and target to revised means. This directly yields the
ordinary conditional-answer method, with zero or bounded observation error.
The reset-price closed-form radius and attaining-law calculation are a
specialized evaluation, not a new recovery principle or new LP algorithm.

## D. Limited-access leads — no theorem-body credit

**Henrique Evangelista de Oliveira, Leonardo Tomazeli Duarte, João Marcos
Travassos Romano. _Identification of the Choquet integral parameters in the
interaction index domain by means of sparse modeling_.** Expert Systems with
Applications 187, 115874 (2022), DOI `10.1016/j.eswa.2021.115874`.

- [Publisher preview](https://www.sciencedirect.com/science/article/abs/pii/S0957417421012331).
- Direct open failed (`turn23view2`); indexed publisher content (`turn21search0`)
  first supplied abstract/introduction. A later targeted publisher-indexed
  query (`turn49search0`) supplied the introductory rank/spark distinction and
  the opening of §4, formulating `M^t mu = u` before truncating its matrix.
  That later excerpt was read by this reviewer as well as the nested reviewer.
- The nested source reviewer searched legitimate primary alternatives and
  recorded its own exact reading scope in [source_review.md](choquet/source_review.md).
- This main review does not claim that the unread section lacks the C4 formula.

**Henrique E. Oliveira, João M. T. Romano and Leonardo T. Duarte.
_Identificação dos Parâmetros da Integral de Choquet via uma Abordagem baseada
em Processamento de Sinais Esparsos_.** SBrT 2017, pp. 692–696.

- [Primary proceedings PDF](https://www.sbrt.org.br/sbrt2017/anais/1570362091.pdf).
- Nested reviewer read all five pages, §§I–V. This reviewer separately opened
  the PDF and read introduction, §II definitions/design/QP, the §III
  transformed optimization, and §§IV–V setup/conclusion; no numerical figure
  values were independently reconstructed. Locators `turn49view0`,
  `turn50view0`, `turn50view1`.
- The paper uses normalized capacities and a linear observation/design
  representation with constrained fitting and interaction-coordinate
  regularization. The nested full reading found no all-permutation or
  price-revision classification. This does not substitute for the unreviewed
  2022 identifiability theorem and is not evidence of worldwide absence.

**Silvia Angilella, Salvatore Greco and Benedetto Matarazzo. _Non-additive
robust ordinal regression: A multiple criteria decision model based on the
Choquet integral_.** European Journal of Operational Research 201(1),
277–288 (2010), DOI `10.1016/j.ejor.2009.02.023`.

- [Institutional record](https://www.iris.unict.it/handle/20.500.11769/26453),
  `turn39view1`, supplies only the abstract and restricts its file to archive
  managers. No attempt was made to bypass that restriction.
- The primary preview describes compatible capacities and LP-based necessary/
  possible comparisons. No full theorem or application section was obtained;
  this is a close lead, not a decisive theorem-body comparison here.

The related 2009 conference paper, _Non-additive robust ordinal regression with
Choquet integral, bipolar and level dependent Choquet integrals_, is listed
with an institutional full-text link at
[Portsmouth](https://researchportal.port.ac.uk/en/publications/non-additive-robust-ordinal-regression-with-choquet-integral-bipo/).
The linked `https://researchportal.port.ac.uk/files/230517/tema_1194.pdf`
returned 403 (`turn46view0`). Its abstract is not counted as a full reading.

An attempted 2019 ROR-SMAA primary preprint
`https://arxiv.org/html/1905.07941v1` and corresponding `/pdf/1905.07941v1`
both failed with `DisabledError` (`turn39view0`, `turn40view0`). A PMC open of
`https://pmc.ncbi.nlm.nih.gov/articles/PMC7274728/` returned a browser/CAPTCHA
challenge (`turn42view0`), not a read paper. No browser bypass was attempted.

## E. Search record

Queries were used to find sources, not to measure literature absence. The
first engine was followed by the stronger engine when primary/full-text
coverage was inadequate. Unrelated or secondary hits were not used as
technical authority.

| Engine | Queries | Result/disposition |
|---|---|---|
| system2 | `"Incremental Abstraction-Carrying Code" pdf`; `Necula proof carrying code 1997 safety policy verification condition code consumer pdf`; `"Identification of the Choquet integral parameters in the interaction index domain" pdf` | Located ACC leads, Choquet preview, and many secondary PCC hits. A same-author short ACC note was kept distinct from the full conference paper. |
| system1 | `"An Incremental Approach to Abstraction-Carrying Code" cliplab`; `"Proof-Carrying Code" Necula 1997 filetype:pdf site:berkeley.edu`; `"Identification of the Choquet integral parameters" "Oliveira" filetype:pdf` | Obtained primary ACC and PCC PDFs. The strict Berkeley query did not return a Berkeley copy; a university-hosted primary paper was used. Choquet full text was not obtained. |
| system2 | `"Non-additive robust ordinal regression" filetype:pdf`; `"Robust ordinal regression" "necessary" "possible" Choquet capacity` | Located institutional/primary previews, a 2019 preprint lead and related PMC paper. Full-text endpoints above failed. |
| system1 | `"Non-additive robust ordinal regression" "pdf" "Greco"`; `"1905.07941" pdf`; `"The Necessary and Possible Importance Relation" pdf` | Located 2009 institutional PDF link; PDF access failed. Other results were irrelevant, secondary or preview-only and were not used for technical conclusions. |
| system2 | `"Identification of the Choquet integral parameters in the interaction index domain" "Identifiability aspects"` | Recovered the opening of journal §4 from the primary publisher's indexed preview; the substantive theorem/proof remains inaccessible. |

No global priority conclusion follows from these queries. Generic architecture
and recovery-method antecedents are established by the actual positive
readings. Whether a particular C4 quantitative consequence has a closer prior
statement remains a separate, bounded comparison question.

## F. Local source identities

The following were read in the working tree rooted at entry commit
`6ef27f20e3ac0920953a27dd84d6c91a021ba58f`. Principal F16 administrative edits
were concurrent; no principal control/clock file was changed by this reviewer.

| File | SHA256 observed during review |
|---|---|
| `v2/contribution_review.md` | `80afe9d6efed85fa465acca8d2ba8068f410b276c962c7dee11bb8788b35074b` |
| `v2/contribution_plan.md` | `11645d7047a859c938cae01112fd4d171b935debc61532a9681a56cfc0414635` |
| `v2/literature/06_c4_contribution_comparison.md` | `f8fd091dbf08ceafe79c86d00dd0ecf351c10a0bd77bfe852b2ebaa25631e4d4` |
| `v2/decisions/2026-10-04_novelty_scope.md` | `ecdce992ac19779deae951263f1f884a1bdc27c75cc2338277cf8a98575639ad` |
| `v2/derivations/09_c4_price_revision.md` | `28a96abb125ffa3fa4527bd2a1939ed0b384ecd722598a9a472505c2b529ceaa` |
| `v2/experiments/results.md` | `333ef2b80b9108d288529d9bc0c7925c8c76471eb1a1ae4fc055d5d475341d74` |
| `v2/experiments/F15_ND01_results.md` | `e1aff33a3b59c9dc0c53e530e3b1c6305969a1c073814069e2ab824e6880ac6a` |

The first broad batched local reads exceeded the response output limit.
Targeted section reads supplied the substantive material used above; no
claim is made to have inspected every line of the long historical plan or
every experiment artifact. This was a review of preserved evidence and
mathematical reconstruction, not independent experimental reproduction.
