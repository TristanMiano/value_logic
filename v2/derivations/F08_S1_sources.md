# F08 S1 — focused antecedent check

Research contributor: **Codex (GPT-6)**. Access date: September 30, 2026 UTC.
This is a scoped source check, not the F10 contribution/novelty audit.

1. **MOSEK ApS, Modeling Cookbook 3.4.0, chapter 2**, especially §2.3.1,
   Lemma 2.1, and §§2.4.2–2.4.3, Lemma 2.4.
   [Official chapter](https://docs.mosek.com/modeling-cookbook/linear.html).
   Its finite linear alternatives and strong-duality statements are the
   standard antecedents for affine consequence, infeasibility rays and optimal
   primal/dual certificates. F08 reconstructs the required rational,
   unrestricted-coordinate version by elimination in 04a A1–A4. It does not
   import a general conic alternative, compactness, or a claim that every
   source polyhedron has a vertex. The dual vertex argument in 04b concerns
   a nonnegative standard-form polyhedron specifically.

2. **Giorgio Bacci, Radu Mardare, Prakash Panangaden and Gordon Plotkin,
   Rational Lawvere Logic**, CSL 2026, LIPIcs 363, 3:1–3:21, published
   February 18, 2026. DOI 10.4230/LIPIcs.CSL.2026.3.
   [Publisher record](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CSL.2026.3).
   Section 6, Theorem 9 is the finite-consequence completeness comparison.
   The project already audited its finite-valued specialization and import
   boundary in [F03's handoff](../literature/01f_consolidated_source_handoff.md)
   and [theorem agenda](../literature/01i_calculus_desiderata_and_theorem_agenda.md).
   That external calculus is not the present signed, unit-directed native
   checker. Its completeness does not establish U1, the unit obstruction,
   source-projection characterization or optimal RHS replay.

Retrieval limit: direct browser fetches of the official chapter, publisher
HTML and PDFs failed with restricted-URL fetch errors. Search retrieval
returned the official chapter's full relevant sections and an indexed PDF
excerpt containing Theorem 9, plus the publisher metadata/abstract. Those
excerpts were checked; the full external documents were **not newly read in
S1**. Detailed RLL hypotheses above refer to the retained F03 primary-source
audit, not to an invented fresh PDF inspection. No unsuccessful retrieval is
evidence of novelty. No secondary-source theorem was imported.

The F08 package claims project-specific reconstruction and characterization.
Linear duality, finite max/min algebra and parametric linear optimization are
antecedents, not new discoveries. F10 must compare the exact typed inference,
information-preservation and proof-retention statements before any publication
priority claim. No broader literature search was manufactured to meet a time
share; F08's protected obligation is derivation.
