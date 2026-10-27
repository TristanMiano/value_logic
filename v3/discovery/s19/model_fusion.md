# Dependence-robust model fusion with an abstention action

Codex (GPT-6), October 26, 2026. DEVELOPMENT; a broad candidate outside the
receipt and proof-scheduling harnesses. Classical experiment comparison is
a likely direct antecedent; this is not yet a novelty claim.

## An exact example with genuinely fallible reports

Let theta be binary with prior1/2. Model A reports L or H. Its calibrated
posterior values are1/10 and3/5, with marginal report probabilities1/5 and4/5.
Model B reports L or H with posterior values2/5 and9/10 and marginal report
probabilities4/5 and1/5. Equivalently, their conditional report probabilities are

    Pr(A=L | theta=0)=9/25; Pr(A=L | theta=1)=1/25;
    Pr(B=H | theta=0)=1/25; Pr(B=H | theta=1)=9/25.

The client knows these two channels but does not know their conditional
dependence. No independence assumption is made. The permitted actions predict
0, predict1, or abstain. Incorrect prediction costs1, correct prediction0,
and abstention1/4. This is a specified finite decision duty, not a claim that
real model calibration or a prior over mathematical truth is given for free.

For either model alone, Bayes loss is

    (1/5)*(1/10)+(4/5)*(1/4)=11/50.

Let s_0=Pr(A=L,B=H | theta=0) and s_1 analogously for theta=1.
Every compatible coupling is described by independent parameters
s_0,s_1 in[0,1/25]. In the order LL,LH,HL,HH, the two conditional joint rows are

    theta=0: (9/25-s_0, s_0, 3/5+s_0, 1/25-s_0);
    theta=1: (1/25-s_1, s_1, 3/5+s_1, 9/25-s_1).

Use the fixed policy: predict0 on LL, predict1 on HH, and abstain on LH or HL.
Its error contribution is1/25-(s_0+s_1)/2; its abstention probability is
3/5+s_0+s_1. Total loss is

    19/100-(s_0+s_1)/4 <= 19/100.

This is sharp: s_0=s_1=0 gives posterior values1/10,1/2,9/10 with marginal
probabilities1/5,3/5,1/5. Bayes loss even with that joint channel known is
19/100. Therefore the policy is minimax over all compatible couplings.
Its worst loss is3/100 below the best individual model, a3/22 (13.636...%)
reduction on this constructed duty. The comparison includes the best
single-model Bayes action, not a threshold heuristic. An ordinary robust
fusion policy is exactly the same method and ties.

For binary prediction with no abstention action, the same channels have
single-model Bayes error17/50, and the least-informative joint channel above
also has error17/50. Thus this gain depends on the actual decision menu.
More information is not required to improve every loss function in order
to improve one useful task.

## General binary-state route, pending primary comparison

For any experiment with posterior P and fixed prior pi, write its stop-loss
curve C(t)=E[(t-P)_+]. Binary Blackwell comparison corresponds to convex
order of these posterior laws. For two known experiments, the pointwise
maximum of their convex stop-loss curves is again a valid curve with the
same mean; it defines their least common upper experiment in that order.
The following argument describes why that object is relevant to unknown
signal coupling, assuming the standard experiment/garbling equivalence.

Every compatible joint signal is more informative than each marginal, so
its curve dominates their pointwise maximum. Conversely, take the least
common upper experiment Z and the two garbling kernels producing the given
marginal channels. Generate both reported signals from Z using those
kernels, independently conditional on Z. The pair is a garbling of Z and
still dominates each marginal; least-upper minimality makes it equivalent
to Z. This supplies a compatible least-informative joint channel.

For a finite decision problem, its Bayes loss is a concave piecewise-affine
function of the posterior. The least-upper experiment therefore maximizes
Bayes loss over compatible couplings simultaneously for all such decision
problems. Finite minimax duality then identifies that value with an optimal
randomized policy robust to the unknown coupling. Producing that policy
can be done with the corresponding finite game or transport LP; the curve
alone is a value calculation, not an executable rule. The later2026
primary comparison below also gives a more direct binary-decomposition
construction, so a full joint-signal LP is not necessary.

A binary two-action loss has one posterior kink, so its worst-case joint
Bayes loss equals the better marginal Bayes loss at that kink. Three or more
actions can have several kinks; different marginal experiments can supply
the stronger information at different thresholds. This explains the
abstention example without claiming a new information principle.

## Boundaries

The channels, prior and their calibration are external premises. Estimated
or interval-valued channels require another uncertainty set and may lose the
gain. This argument is binary-state specific; general Blackwell comparison
does not automatically provide a lattice or the same construction. Zero-cost
joint reporting is also an explicit assumption: any extra inference or
acquisition cost must be below3/100 in the example's loss units to preserve
its net advantage. No empirical or mathematical-truth learning claim follows.

## Primary comparison and disposition

The generic construction is **PARKED as reproduced**. De Oliveira, Ishii and
Lin, *Robust Merging of Information* (February13,2021), section4.1 Lemma1,
Proposition1 and AppendixA.1, give precisely the compatible Blackwell-supremum
argument, including conditionally independent garblings of that supremum.
Their section4.2 treats the best-single-experiment two-action result. The later
*Robust Aggregation of Correlated Information* draft (August16,2025) develops
the decision-decomposition route further. The small abstention example is a
worked application of this prior mechanism, not a new robust-fusion theorem.
The value characterization alone is not a robust policy: the earlier paper
explicitly warns that arbitrary behavior on zero-probability cells can fail.
Our four-cell policy was separately bounded above and matched by a coupling.
No readiness event or empirical gain is claimed for this parked branch.

The September2026 version, arXiv2106.00088v3 (posted October4), was also
inspected: Theorem2 and AppendixA.2-A.4 provide binary decomposition and
dominating maps for constructing robust policies from local comparisons.
Corollary2 needs at most |A|-1 sources. This is a stronger conventional
control than solving an unrestricted joint-signal LP. Sections7.1-7.2
distinguish overlapping known marginals from disjoint blocks and establish
the best-source result for two actions with convex marginal uncertainty.
The restricted overlap route in overlap_fusion.md reduces to older discrete
Chebyshev classification, rather than supplying a new general solution.
