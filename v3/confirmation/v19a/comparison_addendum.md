# Further primary comparison during P3-11-A1

Codex (GPT-6), October 28, 2026. This adds read scope and analysis without
editing the frozen development comparison or changing the candidate event.

Cerny's [ILPIC: Some Applications, Theory and Algorithms](https://fhi.euba.sk/www_write/files/katedry/kove/zborniky/Praha2013.pdf),
proceedings pp.38--42, supplies an earlier primary account. Read sections1--4,
Theorem2.1 and its proof, and the application/conclusion discussion. Its
binary search needs a convex admissible parameter set, continuity and
bracketing scenarios; the paper separates finding those brackets from the
search itself. This reinforces the ordinary inverse-value antecedent. It
does not recover the inaccessible Cerny--Hladik2016 full text or settle its
exact scope. That access limitation remains unchanged.

Li, [Inverse Optimization of Convex Risk Functions](https://arxiv.org/pdf/1607.07099),
published2021; read the July2022 arXiv version's section2.2, section3.1,
Propositions1--3 statements, Proposition2 proof and Lemma EC.3.1 proof.
Observed optimal decisions, elicited comparisons and proximity to a reference
risk function constrain a nonparametric family. Finite convex representations
and a feasible pointwise worst-case function are established there. The read
results are substantially broader than choosing an ad hoc risk estimate,
but use a different source class from V19's finitely many individually bounded
unknown generators. The whole function-space family must not be mistaken
for the same constrained parameter family. No experimental result is imported.

Javeed, Kouri and Surowiec's [Inference as risk identification](https://link.springer.com/article/10.1007/s10287-026-00572-7)
(September2026) was screened at the introduction and formal problem definitions.
It characterizes variational posteriors as risk identifiers, rather than
recovering a full predictive image from scalar risk observations. Its later
proofs were not reviewed; it supplies no novelty clearance here.

## Convex function ambiguity is an exact ordinary control

The following is our direct derivation, not a new theorem attributed to those
papers. Consider a class of convex risk functions constrained by monotonicity,
normalization, cash translation, optional positive homogeneity or law invariance,
and linear inequalities between evaluations at fixed losses. A fixed sup-norm
ball around a reference function is another convex constraint. If two functions
satisfy these requirements, so does every pointwise convex combination. Each
property follows by multiplying the two defining inequalities by nonnegative
weights and adding. Consequently the set of their possible values at any fixed
future loss is an interval (possibly open or unbounded without further
attainment assumptions). The same statement holds for the corresponding
concave lower expectations with their sign conventions changed.

Thus the gapped example is not evidence that general nonparametric convex
risk-function elicitation fails to preserve something its own contract needs.
That larger function class admits intermediate values which the specified
bounded-generator class excludes. A purported application that only licenses
the larger class cannot claim V19's smaller predictive set.

For finite lower envelopes l_A(L)=min_i p_i dot L and l_B(L)=min_j q_j dot L,

    lambda*l_A(L)+(1-lambda)*l_B(L)
      = min_(i,j) (lambda*p_i+(1-lambda)*q_j) dot L.

This identity follows by choosing independent minimizers in the two finite
sets. The mixed lower expectation can be represented by at most n_A*n_B
probability generators. It need not obey the original generator count or
individual generator regions; a smaller representation can sometimes exist.
That is why convexity in function space does not establish convexity of
V19's restricted source class.

## Two different mixtures in the exact worked example

Take the attainable low endpoint21.2 with responses

    A1=(10.1,11.1), A2=(11.1,10.1),

and the high lower endpoint21.9 with responses

    B1=(11.8,10.1), B2=(10.1,11.8).

Both report old coordinate minima10.1. Mix their LOWER-ENVELOPE FUNCTIONS
with weights4/7 and3/7. The old reports stay10.1 and the new total-response
report becomes21.5. The four mixed response generators include
(10.1,11.4) and(11.4,10.1); the other two lie between those on the line
x1+x2=21.5. Neither endpoint belongs to either original response polygon,
so even this two-generator representation violates the original region
restrictions. It is admissible in a larger coherent-function class, not in
the fixed V19 source. Dividing responses by30 gives the probability embedding
in question_fit.md.

In contrast, mix the LABELLED SOURCE VECTORS, keeping A1 with B1 and A2
with B2. Convexity keeps each mixed block in its original base polygon.
Their coordinate minima both become747/70, greater than the allowed101/10.
So this source mixture violates the old receipts. Its total-response minimum
is21.5, demonstrating directly why the receipt-conditioned parameter set is
not convex. The two mixing operations are different: min does not commute
with this labelled averaging.

The ordinary comparison therefore sharpens, rather than removes, the scoped
benefit. The exact construction uses warranted generator restrictions and
joint receipt information. It does not gain precision merely by renaming a
general convex ambiguity class, and it cannot retain its gap after those
restrictions are withdrawn. Useful moderate novelty still concerns the explicit
input/output/resource synthesis, with the same ordinary algorithm tying.
