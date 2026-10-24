# The explicit contribution delta after the strongest comparisons

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; same-model assessment.
The event remains [N16-C/v1](claim.md). This table distinguishes available
machinery from the particular exact solution under assessment.

| Closest construction | Information and quantifiers | Established or reconstructed consequence | Remaining N16 increment |
| --- | --- | --- | --- |
| El Ghaoui–Lebret robust least squares | Known source; one action chosen against an uncertain matrix | Norm-plus-residual robust objective, conic formulations and scalar search | These ingredients are not new; N16 additionally solves a specified unknown-source information class with reoptimization |
| Matrix S-lemma, specialized here | Known M and v; every norm-bounded edit; value reoptimized after the edit | Exact scalar upper family, including parameters below N16's cap when admissible | Compression changes the allowed uniform parameter range; exactness over the enlarged source class still needs proof |
| Bousselmi–Hendrickx–Glineur operator interpolation | Prescribed actions of unknown operators and their transposes, with or without a norm bound | Direct exact finite SDP for the same source/edit problem through two Gram matrices and kernel-compatibility LMIs | N16 supplies an explicit one-parameter solution and small finite extremizers; generic tractability and dimension reduction are already available |
| Young, inverse compression, ordinary primal/dual reuse | The same retained block C and edit warrant | Valid rational lower and upper families | Validity alone is standard; the proposed result proves those families solve the full information problem |
| Contraction completion and dilation | A prescribed compressed positive contraction or prescribed operator actions | Realizable hidden coordinates and norm-bounded completions | The specific equality conditions choose the hidden second moment and attain the edited objective |
| Quadratic optimal recovery and ridge sketching | Different declared model sets or sketches; task-relative loss guarantees | Established information-dependent estimation and resource-aware ridge approximations | Neither general idea is new; no inspected statement supplies the exact C,c,e endpoints and witnesses |

Precise primary-source inspection scopes and links are in
[literature.md](literature.md). The full-source specialization is in
[fixed_source.md](fixed_source.md), and the strongest same-information
comparison is in [gram_sdp.md](gram_sdp.md). This is not an exhaustive
absence-of-prior-art result.

## What can reasonably be proposed

A possible useful, moderately novel contribution is an explicit solution of
a particular conventional information-constrained robust optimization problem:
retain a small old response block, allow every compatible finite source and
every norm-budgeted edit, and characterize exactly the range of the new
reoptimized ridge value. The direct proof gives both interval endpoints and
finite witnesses. The scalar families also provide a small conditional
rational certificate, whose arithmetic does not trust a numerical optimizer.

The [sum-of-squares identities](dual_certificates.md) make the analytic
solution's relationship to the ordinary SDP especially concrete: they are
feasible dual certificates, and the constructed source/edit pairs attain
them. The common parameter and the cap are explained by equality conditions,
not inferred from fitting numerical solutions. The cap can require an
unobserved second moment even when every entry of C is retained.

There is a useful information interpretation as well as a calculation:
inside the sharp interval, better reasoning on exactly the same observations
cannot settle a strict universal threshold. Additional observations or a
stronger model/edit warrant are needed. Outside it, a suitable rational
certificate can often settle the decision, subject to the checker's bounded
input format. The fixed bit cap prevents a universal completeness claim.

## What the assessment does not establish

The same-information SDP ties the optimum. An identical ordinary
implementation ties every certificate. There is no measured runtime,
audit-fee or complete-cost advantage in this session. The 1.80% width gain
and the cancellation decision compare different retained information.
Their acquisition, retention and checking costs remain part of any economic
application. The successful decisions need valid bounds; they do not alone
establish novelty of the sharp theorem.

The [retention controls](retention_tradeoff.md) sharpen this limitation. One
well-chosen scalar witness already settles the worked upper decision. For a
uniform bound over every target in a subspace, its largest retained eigenvalue
suffices. The full block is relevant to directional reuse, and its three-query
example is a sufficient acquisition path rather than an optimal purchase.

The mathematical result is not a learning rule for unresolved mathematics,
a probability assignment to logical propositions, or a resolution of
counterpossibles. It is a finite model-change mechanism in the broader
program. Conventional robust optimization can embody the same task-relative
use of fallible, partial information. Attribution and the explicit new
consequence, rather than an opposition to ordinary methods, determine
whether this is a worthwhile contribution.

A later [scalar-mixture obstruction](commuting_control.md) rejects another
tempting reduction: even closed matrix-valued spectral mixtures of scalar
perturbation bounds can be strictly weaker than the N16 upper endpoint.
The interior equality construction uses noncommuting edited responses.
This gives content to the operator aspect of the solution, while leaving
the strongest ordinary noncommuting SDP comparison intact. Likewise the
separate [paired contrast](pair_block.md) can have only limiting attainment,
showing why finite attainment is not automatic from a closed SDP.

## Main comparison risk

The general interpolation formulation is a routine specialization of prior
work. The analytic solution may still be judged a routine corollary after
the particular equality construction is recognized. A close source or expert
comparison could also identify the same result under other terminology.
The present reconstruction makes that judgment reviewable; it does not
remove the uncertainty or justify counting every elementary step as novel.
