# F17 report v1: literature, contribution and attribution review

**Reviewer:** ChatGPT (GPT-6 Astra Pro), separate same-model internal review.
**Principal concurrent credit:** zero. **Date:** October 6, 2026 UTC.

**Fixed artifact:** `drafts/report_v1.md`, 88,634 bytes, 1,953 lines; SHA256
`af2a98350273c59eb2b682e62be9df13c11f8f1f9d67df7b0c94d73e24673784`.
The snapshot remained unchanged. Its complete text was read in bounded chunks,
with the whole introduction and contribution discussion read before the
source crosscheck.

## Disposition

**The contribution, comparison boundaries, bibliography and writing-guide
attribution are supported at the existing scope, with one required local
citation correction (LIT-01) before final report handoff.** This is not a
scientific defect, a contribution displacement, a Gate C reconsideration,
or a Gate D decision. The correction concerns the evidential role assigned
to one established probing paper.

## Required correction: LIT-01

**Location:** §10.3, lines 1412–1414 in this immutable snapshot.

The sentence says that probe controls help distinguish accessible information
from what the original computation uses, citing Hewitt–Liang. Their controls
put decoding accuracy in context by asking what the probe can learn or
memorize. That is a limit on a decoder-based interpretation, not a test of
causal use by the underlying model. The report’s later decodability warning
is correct, but the citation sentence itself needs the narrower statement.

Suggested replacement:

> Probe controls put decoding accuracy in context by testing what the probe
> itself can learn or memorize (Hewitt–Liang). Causal use
> requires the separately specified intervention evidence.

Support: the F14 primary-source table, the F17 `HewittLiang2019` source record,
and the freshly checked official ACL abstract recorded as `turn82view4`.
Retain the existing report citation link when applying this sentence.
The original paragraph’s interchange-intervention and patching citations
already cover the separate causal-evidence discussion. No new citation,
experiment, threshold or hypothesis is needed.

**Status at this snapshot:** open; root notified. The reviewer did not edit
the paper. Root should record the replacement and bind its disposition to
the next report hash.

## Contribution contract: no substantive expansion

| Field | Assessment against Gate C |
|---|---|
| Object | The same revisable reset-cost consumer and explicit retained-source/current-request contracts. |
| Type | Modest synthesis, formal adaptation and specialized mathematical application. |
| Exact delta | Evaluated revision ranks, actual-new-mean repair, sharp bounds/witnesses and the compatible endpoint/adjacent-level common-radius construction. |
| Magnitude | Modest project-level contribution with a substantive local theorem. |
| Evidence | Accepted linked derivations, adverse cases, stipulated frozen application evidence and the preserved neural null. |
| Comparison scope | Named inspected antecedents; worldwide priority unestablished; the close 2022 Choquet theorem remains unread. |

The abstract and introduction lead with the concrete question and application.
They explicitly retain ordinary reproduction of the service, absent general
performance superiority and 0/5 complete neural support. Section 7.2 gives the
equal-price rank a direct Gasanova–Nicklasson Theorem 3.4 antecedent, while
identifying the price-dependent kernel/intersection as the relevant extension.
Section 7.4 identifies the family-specific compatible-radius proof and its
additional-source counterexample rather than claiming that generic convexity
suffices. Sections 11–12 retain the large old summary, modest contribution,
strong ordinary comparison and optional future branches.

No speculative priority claim or empirical superiority claim was found.
The statement that an ordinary implementation can use the same construction
is consistent with the contribution contract. The report does not promote
a local proof into a new general optimal-recovery principle.

## Neural interpretation

The requested explanation about the absence of a training incentive for
clean eight-neuron expected-cost blocks is prominent in both introduction
and §10.3. The logarithmic decomposition is labeled an available explanation,
not an observed mechanism. Distributed features and technical superposition
are kept distinct, and superposition is not declared demonstrated.

The complete-support conjunction remains 0/5. The later fractional-mask
results are explicitly development point criteria; calibration shows why
capable controls can prevent the full endpoint even with accessible
structure. More data, richer extraction and a joint causal explanation are
not conflated. Optional F15-ND02 remains a separate prospective question.
The only source-scope issue here is LIT-01.

## All 24 references checked

All 24 report reference blocks were compared with the verified bibliography
fields and source-reading records. Titles, author identities, stated years,
reported pages and explicit inspected versions are consistent. Automated
normalization additionally confirmed every title/year and each supplied page
range. All 24 anchors are unique, all are cited, and all 31 reference uses
resolve. This is a document check, not a new full rereading of 24 papers.

Particularly relevant version checks passed:

- The 1991 Ruspini paper is not dated by its 2013 archival upload.
- Cousot–Cousot is POPL 1977; the full bibliography uses Fourth Annual,
  consistent with the original PDF/BibTeX rather than the landing-page typo.
- Miranda–Zaffalon, Ranzato–Tapparo, Paruchuri–Chatterjee and Wu et al.
  retain their explicit inspected preprint versions.
- Happach’s 2022 journal identity is distinguished from the linked 2020
  manuscript in the bibliography note.
- The final Makelov paper correctly lists Makelov, Lange, Geiger and Nanda.
- The DAS venue/pages and author order match the official PMLR record.
- The 2022 Choquet reference explicitly preserves its unavailable theorem.
- Elhage’s abbreviated report author list is expanded in the bibliography
  from the inspected primary PDF, not by guessed authorship.

The [machine-readable review](report_v1_literature.json) supplies a separate
record for each reference, including its anchor, citation key, comparison
result and reference-block hash.

## Writing-guide attribution

The requested GitHub plugin freshly retrieved the complete README and LICENSE
at commit `a542dbe5a70e6441b651bd659d93041558110136`. The repository title,
Scott Armstrong/Amélie Loher attribution and CC BY 4.0 designation match §14.
The report supplies the repository link, license link and an explicit statement
that the advice was adapted for Markdown. It does not imply that the external
authors supplied the Value Logic theorems, endorsed this report, or audited it.

The stated adaptations match the saved `writing_guidance.json`: mechanisms
before technical details, stable theorem contracts, one canonical editor and
separate source/reader checks. This review does not certify every external
skill instruction, legal compliance, a rendered LaTeX/PDF or publication
readiness. The user asked that the advice be considered, and the report
accurately describes that limited use.

## Review boundary

This review read the whole fixed report and examined literature attribution,
claim scope and the 24 references. It did not substitute for the separately
assigned proof and empirical reviews, run a new scientific stage, or write to
the paper, bibliography or ledger. Pending root-owned claim-map/work-log links
are outside this scoped finding. Minor empty administrative reads were resolved
by targeted reads and are recorded in the JSON; there were no new scientific
attempts or failures.

**Signed: ChatGPT (GPT-6 Astra Pro).**
