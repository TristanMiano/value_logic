# F16: narrow Choquet primary-source review

Contributor: **ChatGPT (GPT-6 Astra Pro)**, delegated separate source reviewer.
Date: **2026-10-05**. Concurrent principal time: **ZERO**.
Scope: source retrieval and comparison only; no experiments rerun and no
derivation files edited.

## Disposition

**The substantive identifiability analysis in §4 of Oliveira, Duarte and
Romano (2022) remains unreviewed.** This search recovered the beginning of
§4 in the publisher's indexed preview, a complete same-author conference
precursor, and official records of Oliveira's 2020 doctoral thesis. It did
not recover the journal article's full text or the thesis text.

Consequently this review neither establishes exact priority for C4 nor
clears the 2022 paper as lacking an equivalent theorem. An incomplete
retrieval is an access limitation, not novelty evidence.

## Primary material actually inspected

| Source | Accessed material | What it establishes for this review |
|---|---|---|
| H. E. de Oliveira, L. T. Duarte and J. M. T. Romano, *Identification of the Choquet integral parameters in the interaction index domain by means of sparse modeling*, ESWA 187, 115874 (2022), [DOI](https://doi.org/10.1016/j.eswa.2021.115874), [publisher preview](https://www.sciencedirect.com/science/article/abs/pii/S0957417421012331) | Publisher-indexed abstract, introduction, section preview headed “Identifiability aspects,” and conclusion preview | The introduction describes rank analysis for an overdetermined design and spark analysis for an underdetermined sparse model. The §4 preview sets up the uniqueness problem as `M^t mu = u`, but truncates during the displayed matrix. No substantive §4 theorem or proof was available. |
| H. E. Oliveira, J. M. T. Romano and L. T. Duarte, *Identificação dos Parâmetros da Integral de Choquet via uma Abordagem baseada em Processamento de Sinais Esparsos*, SBrT 2017, pp. 692–696, [full primary proceedings PDF](https://www.sbrt.org.br/sbrt2017/anais/1570362091.pdf) | All five pages, §§I–V and references | §II-A normalizes `mu(empty)=0`, `mu(C)=1`, leaving `2^m−2` free coefficients. §II-B linearizes supervised fitting and gives the constrained quadratic program, Eqs. (2)–(4). §III introduces interaction coordinates and sparsity regularization, Eqs. (7)–(12). §IV gives a numerical fitting example. The complete paper contains no price-revision result or all-permutation rank classification. |
| Unicamp, [2020 FEEC doctoral-thesis annual record](https://www2.unicamp.br/anuario/2020/FEEC/FEEC-tesesdoutorado.html), item 14; [official defense announcement](https://www2.unicamp.br/estatico-2023/teses/2020/09/03/identificacao-dos-parametros-da-integral-de-choquet-uma-abordagem-baseada-em/) | Entire announcement and the relevant annual-record item | Confirms Oliveira's same-title doctoral thesis, supervised by Romano with Duarte as co-supervisor, defended 18 September 2020. These records provide no thesis PDF and are not theorem evidence. |

## Comparison with the C4 questions

The following judgments distinguish an inspected primary precursor from
the uninspected portion of the journal paper.

| C4 question | 2017 precursor | 2022 §4 |
|---|---|---|
| Rank `2^k−k` of all full-order numeric means at one positive price profile | Not supplied in the inspected text | Unresolved |
| Identifiability from two nonproportional positive price profiles, with terminal-penalty cases | Not supplied in the inspected text | Unresolved |
| Exact repair with `k−1` actual new order queries following a one-price edit | Not supplied in the inspected text | Unresolved |
| General capacity fitting through a linear observation matrix | Explicitly supplied | Explicitly announced and set up in the accessible preview |

**Mathematical comparison by this reviewer:** C4's §13 maps its observations
to Choquet evaluations at the special scores
`x_(pi_j)=M+sum_(l>j)c_(pi_l)`. An unrestricted capacity-fitting method does
not, merely by existing, evaluate the rank or kernel of this particular
price-generated matrix. Conversely, a theorem about that matrix in the
unavailable §4 could be highly relevant. The normalization difference is a
comparison condition, not a novelty argument: fixing the total capacity
would remove C4's unresolved-mass coordinate.

## Retrieval limitations and routes checked

- Direct publisher access at both `/science/article/abs/pii/S0957417421012331`
  and `/science/article/pii/S0957417421012331` returned **403 Forbidden**.
  No paywall or authentication bypass was attempted.
- The [ResearchGate journal record](https://www.researchgate.net/publication/354699326_Identification_of_the_Choquet_integral_parameters_in_the_interaction_index_domain_by_means_of_sparse_modeling)
  explicitly states that no full text is available and offers an author
  request. No message or request was sent.
- The Semantic Scholar record for paper
  `b69a51b9c47a6abbd57f9c7a18bb85a22180a136` failed to open.
- OpenAlex's public record, queried at
  `https://api.openalex.org/works/https://doi.org/10.1016/j.eswa.2021.115874`,
  returned work `W3200063529`, a closed-access status, no best OA location,
  and no repository full-text location. This was used only as a locator
  check; it is not proof that no lawful manuscript copy exists.
- Searches covered exact English title/DOI, Portuguese title, author aliases,
  institutional repository terms, thesis/identifiability terms, and relevant
  rank/permutation/price terms in both available search engines. Some results
  were plainly off-topic, so absence of relevant search hits is not used as
  evidence about the mathematics.
- A 2024 Pelegrina–Duarte preprint was examined as a possible route to a
  repository citation. Subsequent retrieval returned **502 Bad Gateway**.
  It is not used to attribute any theorem to the 2022 article.

## Recommended status for the principal review

Keep **generic Choquet/capacity identification established** and retain the
specific C4 matrix, revision and repair claims as an **unsettled priority
comparison** against this 2022 source. The next decisive evidence would be a
lawful full copy of journal §4 or the relevant identifiability chapter in
Oliveira's 2020 thesis. The 2017 precursor improves the primary-source
baseline but does not settle that remaining comparison.
