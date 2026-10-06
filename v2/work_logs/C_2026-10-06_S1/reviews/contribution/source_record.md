# Gate C contribution review: sources, exposure and access

**Reviewer:** ChatGPT (GPT-6 Astra Pro). **Access:** October 6, 2026 UTC.
**Process:** separate same-model review, zero principal-clock credit.

## Fresh primary reading

1. **Mahmood Ettehad and Simon Foucart, _Instances of Computational Optimal
   Recovery: Dealing with Observation Errors_**, SIAM/ASA Journal on Uncertainty
   Quantification 9(4), 1438-1456 (2021), DOI `10.1137/20M1328476`.
   [Author PDF](https://foucart.github.io/publi/OR_Uncertainty_v2.pdf).
   Read introduction and section 2.1, Theorem 1 and the displayed duality proof,
   PDF pages 1-5. Web locators `turn71view0`, `turn75view0`. The stated output is an ambient
   target vector; substituting the probability simplex and retained means
   supplies the standard solver. The compatible-law identity still requires
   the reset-family argument. No source theorem is imported as a new native rule.

2. **Pradyumna Paruchuri and Debasish Chatterjee, _A numerical algorithm for
   attaining the Chebyshev bound in optimal learning_**, arXiv:2307.01304v1,
   July 3, 2023. [Primary HTML](https://arxiv.org/html/2307.01304v1).
   Read introduction, relative-center equations (1)-(2), and section 2 through
   the beginning of the semi-infinite reformulation, especially equations
   (5)-(13). Web locators `turn71view1`, `turn72view2`.
   This supplies the established prescribed-center problem. No algorithmic
   correctness, complexity or later journal-version claim was newly audited.

These are bounded theorem/contract comparisons, not complete literature
reviews. The final recommendation uses the local F16 proof reviews for the
new theorem, not a purported external validation. The source pages were
retrieved as web text; original PDF/HTML bytes were not downloaded and no
web-source SHA256 is invented.

## Reused local primary-comparison records

The following records were read as attributed existing research, not counted
as new complete external readings:

- `v2/literature/06_c4_contribution_comparison.md`, full record: utility logic,
  quantitative logic, assurance, proof grounding, chain rank, sequential
  testing, predictive representations, sufficiency, recovery and Choquet
  identification.
- `v2/work_logs/F16_2026-10-05_S1/primary_reading.md`, full record: incremental
  abstraction-carrying code, recovery, Choquet precursor, vector-valued
  recovery, nonlinear recovery and relative centers.
- `v2/work_logs/F16_2026-10-05_S1/reviews/contribution/source_record.md`, full
  record; and the relevant conclusions of its parent contribution review.

The strongest architectural comparison remains Albert, Arenas and Puebla,
_An Incremental Approach to Abstraction-Carrying Code_ (LPAR 2006),
[author-group manuscript](https://cliplab.org/papers/inc-acc-lpar06.pdf).
This Gate C reviewer relied on the explicit F16 reading scope for that paper
and did not claim a fresh full reread of it.

## Targeted identification search and failures

The search goal was limited: can a legitimate accessible copy resolve the
previously unread identifiability section of de Oliveira, Duarte and Romano,
_Identification of the Choquet integral parameters in the interaction index
domain by means of sparse modeling_, Expert Systems with Applications 187,
115874 (2022), DOI `10.1016/j.eswa.2021.115874`?

All searches used `system1_search_query`. Queries were:

1. `"Identification of the Choquet integral parameters in the interaction index domain" full text pdf`
2. `"Henrique Evangelista de Oliveira" "Choquet" tese`
3. `"115874" "Choquet" "Oliveira"`
4. `"Identification of the Choquet integral parameters" site:sciencedirect.com`
5. `"Identificação de medidas fuzzy na integral de Choquet" site:repositorio.unicamp.br`
6. `"Identification of the Choquet integral parameters" "Identifiability aspects"`
7. `"Identification of the Choquet integral parameters" "rank" "spark"`
8. `site:sciencedirect.com/science/article/pii/S0957417421012331 "rank criterion" "equality"`
9. `site:sciencedirect.com/science/article/pii/S0957417421012331 "Identifiability aspects"`

Several exact queries returned mainly unrelated or secondary results. None
was used as technical authority or as evidence of literature absence.
Primary indexed publisher snippets appeared at `turn73search2` and
`turn73search16`; they did not expose the full theorem or proof. Opening the
[abstract URL](https://www.sciencedirect.com/science/article/abs/pii/S0957417421012331)
returned an internal error (`turn72view1`). Opening the indexed
[full-article URL](https://www.sciencedirect.com/science/article/pii/S0957417421012331)
returned HTTP 403 (`turn74view0`). No access control was bypassed.

One institutional result led to
`https://repositorio.unicamp.br/Busca/Download?codigoArquivo=595355`;
opening it returned an internal error (`turn72view0`). The
[university record](https://www.ime.unicamp.br/pos-graduacao/matematica-aplicada/identificacao-medidas-fuzzy-na-integral-choquet-computadores)
(`turn73search3`) established that it is Paulo Henrique Ribeiro do Nascimento's
2025 thesis on quantum-annealing-compatible identification, supervised by
Leonardo Tomazeli Duarte, rather than the requested article or Oliveira's
thesis. It was not treated as a substitute or as a theorem-body source.

**Outcome:** the 2022 technical section remains unavailable. This review
does not assert that it lacks any particular C4 result. The failed search
adds no positive novelty evidence. Stop further access attempts because the
bounded application decision can be stated honestly with this limit; stronger
priority or a specific displacement challenge would reopen the recorded
comparison chunk.

## Local evidence and non-exposure statement

Observed entry `HEAD` was `de7b456d08f383e72dfcabd278c183db324fdf16`.
The review read the October 4 criterion, Gate C requirements, C4/F16
contribution statements, C4 derivation sections 1-8, F16-C1 sections 1-10,
the ordinary baseline, relevant F15 report outcomes and examples, and prior
source/review records. It did not inspect every historical claim row or all
experimental units. The reviewer had prior outcome exposure through the
conversation and saved reports; no blinding claim is made.

No preparation, training, alignment discovery, evaluation population,
scientific retry, new mathematical test family or benchmark was generated.
Read-only shell commands and web retrievals supplied the evidence. Local
files were hashed for traceability in [source_hashes.json](source_hashes.json).
The parent controls the authoritative whole-repository integrity and timing
audit; this review does not duplicate it or claim that its own wall duration
meets a research floor.

A first broad batched local read exceeded the tool output limit; targeted
reads supplied the sections used in the assessment. This is a reporting
inspection limitation, not a scientific attempt or failed experimental stage.
