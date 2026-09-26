# F04 first-pass sources and import limits

Session: 2026-09-25-S1 (Los Angeles); accessed 2026-09-26 UTC.
This is a small source-use record for the candidate discrimination, not a new
F03 audit or an assertion that the literature is obscure enough to imply novelty.
F03's bibliography and source identities remain unchanged. No full external paper
or screenshot is redistributed. Only the inspections listed below are claimed.

## L01 — Arithmetic/residual comparison

Giorgio Bacci, Radu Mardare, Prakash Panangaden and Gordon Plotkin,
*Rational Lawvere Logic*, CSL 2026, LIPIcs 363, article 3.
[Official HTML](https://drops.dagstuhl.de/storage/00lipics/lipics-vol363-csl2026/html/LIPIcs.CSL.2026.3/LIPIcs.CSL.2026.3.html),
sections 2–4 and the finite-arithmetic interface; DOI 10.4230/LIPIcs.CSL.2026.3.

The additive sequent and residual provide the mechanistic comparison. The
F04 signed-pair inequality retains finite operands and the source's inequality
orientation. It is not an implementation of the full proof system or a transfer
of its completeness theorem to the proposed affine/evidence semantics. F03's
previous source-rule checks remain available. No new source PDF inspection is
claimed in this session.

## L02 — Surrogate excess risk is not arbitrary pairwise ordering

Peter L. Bartlett, Michael I. Jordan and Jon D. McAuliffe,
*Convexity, Classification, and Risk Bounds*, Berkeley Technical Report 638
(2003; later journal publication in 2006).
[Report record](https://statistics.berkeley.edu/tech-reports/638),
[inspected report PDF](https://statistics.berkeley.edu/sites/default/files/tech-reports/638.pdf).

The report's displayed excess-risk comparison, equation (1), and its surrounding
calibration discussion were checked, including a rendered PDF page at index 3
(printed page 4). Locators are for this report, not silently the journal layout.
The relationship compares excess risks against their respective optima; it does
not say that every pair of predictors has the same ranking under both risks.
F04 derives its elementary Brier counterexample and bound directly. No general
surrogate theorem is proved anew, and no full-paper independent check is claimed.

## L03 — Shared uncertainty is an established baseline

Luiz Henrique de Figueiredo and Jorge Stolfi, *Affine Arithmetic: Concepts and
Applications*, Numerical Algorithms 37, 147–158 (2004),
DOI 10.1023/B:NUMA.0000049462.70970.b6.
The research group's [affine-arithmetic overview](https://www.ic.unicamp.br/~stolfi/EXPORT/projects/affine-arith/Welcome.html)
and the publisher abstract were inspected; the journal proof text was not.

The overview's affine form, common bounded noise symbols, exact affine operations
and need to enclose nonlinear remainder explain why F04 must not present shared
source tracking as new. The unrestricted nuisance vector z in F04 is separately
specified and analyzed, rather than attributed to an uninspected source theorem.
The consumer-annihilator calculation is elementary linear algebra; any later
novelty claim must go beyond this known representational pattern.

## L04 — Reflection can require a changed predictive interface

Benja Fallenstein, Jessica Taylor and Paul F. Christiano,
*Reflective Oracles: A Foundation for Classical Game Theory*,
arXiv:1508.04145v1, 17 August 2015.
[Inspected HTML](https://arxiv.org/html/1508.04145v1), section 2,
Definitions 2.1–2.2, Theorem 2.3 and the complement/diagonal example.

The source permits randomized oracle answers at an equality boundary under
its particular probabilistic-machine conditions. It is a precedent for taking
self-reference seriously without demanding deterministic exact forecasts in
every case. F04 uses no reflective oracle and does not import the existence
theorem. Its named controller is solved directly from finite probabilities;
the safe-branch and parameter-interval assumptions remain external premises.

## L05 — Interchange interventions, not decodability alone

Atticus Geiger, Hanson Lu, Thomas Icard and Christopher Potts,
*Causal Abstractions of Neural Networks*, NeurIPS 2021;
arXiv:2106.02997v2, 27 October 2021.
[Inspected HTML](https://arxiv.org/html/2106.02997v2), section 3 and
equations (1)–(3); version metadata checked against the abstract page.

The source provides the high-level/low-level intervention comparison. Our
prospective high-level variables are the task's expected action costs. The
positive-rescaling/permutation identities are derived for an ordinary single
ReLU hidden layer with affine output. No source figure was used; no trained
network result or general deep-network invariance theorem is claimed. Matching
interventions and controls do not uniquely identify a utility function.

## L06 — A second substantive value-oriented route

Enrique Miranda and Marco Zaffalon, *Nonlinear Desirability Theory*,
arXiv:2209.00686v2, 18 November 2022.
[Inspected HTML](https://arxiv.org/html/2209.00686v2), the closure/natural-extension
interface in Definitions 2–3 and the utility-transformed construction in Example 1;
version metadata checked against the abstract page.

This is an antecedent for taking desirable uncertain gains and their consequence
structure seriously, rather than assuming an RLL language is the only option.
F04's non-worsening test inf g>=0 is deliberately distinguished from strict
acceptance conventions that exclude the zero gamble. The source does not by
itself establish our reflective controller, causal neural hypothesis, or new
composition/update theorem. No mature-system ranking or global priority claim
is inferred from this selected reading.

## Session evidence boundary

The source checks orient examples and distinguish imported patterns from local
arguments. The complete candidate proofs are in
[the derivation note](01_candidate_countermodels.md). Mathematical reconstruction
is D, source inspection is L, and fixture implementation is E. Mixed or missing
clock boundaries do not receive retrospectively invented research credit.
