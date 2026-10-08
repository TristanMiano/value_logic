# P3-05 — selected transport and reuse comparisons

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 8, 2026 UTC.
New reconstruction session; these are newly inspected source passages, not a
restoration of the lost P3-05 source log. No full priority review or full
external algorithm replication is claimed. Inherited theorem scopes remain
those of their original sources.

## T05-S1 — structural changes

Halpern, *Axiomatizing Causal Reasoning*, JAIR 12 (2000), 317–337;
[arXiv v1](https://arxiv.org/pdf/cs/0005030), section 2.1, printed pages 318–319,
and section 2.3, pages 320–321. Selected text and page 319 were inspected.
Intervention substitutes fixed variables into retained equations; acyclicity
suffices for a unique solution. General models need not have one. This supplies
the ordinary interpretation for named occurrence changes. It does not identify
which copy or predictor follows a function replacement. The routing table in
the new derivation is supplied input, not a theorem imported from this paper.

## T05-S2 — incremental certificates

Albert, Arenas and Puebla, *An Incremental Approach to Abstraction-Carrying
Code*, LPAR 2006, 377–391; [15-page author manuscript](https://cliplab.org/papers/inc-acc-lpar06.pdf).
Inspected sections 3.1–3.2, 4–5's interface and Theorem 1 statement, and section
6; PDF page 6 visually checked. Answer/dependency tables support checking only
affected parts. Theorem 1 identifies the resulting stored tables with those
of full checking under its stated certificate premises; its proof is referred
to a technical report and was not reconstructed here. The conclusion expressly
notes the tradeoff with storage and update frequency. These are close ordinary
antecedents for retained verification. They do not by themselves certify that
a changed optimizer family lies in a previously verified loss domain.

## T05-S3 — optimization already has incremental reuse

Martins, Joshi, Manquinho and Lynce, *Incremental Cardinality Constraints for
MaxSAT*, CP 2014; [18-page manuscript](https://arxiv.org/pdf/1408.4628), section
3.2 and the opening of 3.3. Inspected parsed text around equations 4a–4c.
A requested screenshot of PDF page 9 failed; no table/graph result is used.
Assumption-controlled bounds retain the underlying encoding and learned
clauses. A feasible assignment supplies an objective upper bound. Encoding a
wide bound can consume more resources; changing input literals needs another
scheme. We import neither implementation nor a performance figure. This
prevents a comparison that gratuitously restarts an ordinary solver after
 every bound update. Reusing such a solver is compatible with our outer-domain
certificate test and must be allowed in later same-resource evaluations.

## Project antecedents and exact delta

[P3-04](../derivations/04_counterfactual_semantics.md) C04-5/6 supplies all-winner
coverage and task bounds; its [companion](../derivations/04_selection_extensions.md)
CE04-12 explains failed monotonicity after restricting candidates.
[Phase-two paper 4.2](../../paper_v2.md#42-reuse-after-source-revision) supplies
localized proof transport and withdrawal penalties; the argument is inherited,
not new P3-05 credit. P3-03 also supplies current-record and certificate scope.

CT05-2 joins these into an explicit sufficient condition for reusing a wider
rank-sublevel loss certificate even when every old optimum disappears. Its
short perturbation proof is directly reconstructed mathematics, not an imported
newness claim. The new finite receiver tests the separate domain, rank and loss
conditions. Comparative significance must be assessed against an ordinary
constraint solver with caching and the same certificates, not against an
ordinary method forced to discard the information. Reproduction of an algorithm
by ordinary computation does not itself disprove originality; the named prior
results and the exact useful guarantee are the relevant comparison.

Bounded Inductive Rationality is a pertinent deferred comparison for P3-06/07,
not a replacement source for these static transport claims. This session does
not infer that a static certificate satisfies an online induction criterion.
