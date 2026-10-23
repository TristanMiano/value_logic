# Anytime conditional risk for selected program mixtures and late proofs

Codex (GPT-6), October 23, 2026. DEVELOPMENT; pass 35.

This connects [open programs](anytime_programs.md) with conditional release.
It does not treat repeated occurrences of a fixed unresolved theorem as
independent samples. Cases are iid from a declared population; the complete
bounded policy, including learned parameters and abstention, is indexed by h
under a fixed countable prior subprobability pi.

For each h and case, the latent outcome is B (bad release), G (good release),
or O (abstention), with fixed probability vector p_h. Different policies'
outcomes on a case may be arbitrarily dependent. Let mu_h be the empirical
three-outcome frequency at prefix n. A posterior q chooses a whole policy
afresh for each future case. Its true population probabilities are p_q=sum q p_h;
conditional risk is p_q,B/(p_q,B+p_q,G), when the denominator is positive.
It is generally NOT the q-average of the individual conditional risks.

## Common event

For each h, mix the categorical likelihood ratio against p_h with the uniform
Dirichlet(1,1,1) prior. With counts n_j and C_n=(n+1)(n+2)/2,

    M_n^h = [2 product_j(n_j!)/(n+2)!] / product_j(p_h,j^n_j)
           >= exp[n KL(mu_h || p_h)] / C_n.

The inequality follows because the multinomial probability of those counts
under mu_h is at most one. Each M is a nonnegative martingale, or a
supermartingale on a proper support. Their pi-mixture starts at most one.
Ville, the change-of-measure inequality and joint convexity of KL give, on
one event of probability at least 1-delta, for ALL n and finite posteriors q,

    n KL(mu_q || p_q) <= KL(q || pi) + log(C_n/delta) = c(q,n).       (1)

Zero probabilities use the usual KL conventions. The event is about latent
complete outcomes, so delayed sound proofs can reveal them in any order.
No repeated confidence charge is needed for reselecting q or inspecting
another prefix. The polynomial C_n penalty is real; this bound is not claimed
to beat specialized fixed-policy or fixed-time confidence intervals.

## Incomplete labels and a computable conditional bound

Assume each release decision is known, but some released answers have not
been proved correct or incorrect. Let rho_hat=sum q R_count(h)/n. Let
beta_U be the q-weighted fraction of known-bad OR unproved releases: every
unproved release counts as potentially bad. If rho_hat>0, put b_U=beta_U/rho_hat.
The KL chain rule and minimization over the unknown population release rate
give from (1)

    n rho_hat kl(b_hat || risk(q)) <= c(q,n),

where b_hat is the latent empirical bad fraction among releases. Since
b_hat<=b_U, a valid upper bound is

    sup {r in [b_U,1] : kl(b_U || r)<=c(q,n)/(n rho_hat)}.           (2)

If b_U=1 or rho_hat=0 use the vacuous upper one. The one-sided binary-KL
endpoint is monotone in b_U, so proving a previously unresolved release good
can only improve a fixed-q certificate. Selecting q again remains covered
by (1). Selecting the desired risk threshold after the evidence also costs
no extra union budget: (1) is one full confidence region.

The release rate itself is covered by n kl(rho_hat || p_q,R)<=c(q,n).
Positive empirical release gives a positive lower endpoint for finite c.
Report that endpoint if availability matters; the conditional ratio alone
does not promise useful coverage. New environments and counterfactual sampling
distributions require their own transport warrant.

For fixed epsilon, a different route is to apply the earlier bounded-loss
certificate to Y_h=B_h+epsilon(1-R_h). E Y_q<=epsilon implies conditional
risk<=epsilon. That supplies a convex fixed-threshold program-selection
constraint. In contrast, optimizing (2) over q is not automatically the
closed-form Gibbs optimization from pass 30; its computational cost remains.

This is a multinomial PAC-Bayes/confidence-sequence adaptation. Generic
novelty is not claimed. Potential value is an explicit bounded-program,
partial-proof and conditional-delivery contract, with close selective
PAC-Bayes literature still to compare.
## Release decisions can also be unfinished

The known-release assumption above can be relaxed. For each policy/case retain
a sound nonempty set of possible outcomes in {B,G,O}. For the conditional-risk
upper endpoint, the pessimistic ordering is B > O > G. Fill each partial set
with its highest element and use its resulting weighted bad/good counts in
(2). This covers incomplete execution as well as incomplete correctness proofs.

To see the ordering, fix a candidate risk r above the empirical bad fraction
and write the binary likelihood statistic for nonnegative counts b,g as

    T_r(b,g)=b log[b/(r(b+g))]+g log[g/((1-r)(b+g))].

Its derivatives are log[b/(r(b+g))]<=0 in b and
log[g/((1-r)(b+g))]>=0 in g. Adding a bad release (O to B), or removing
a good one (G to O), can only increase the upper endpoint. Boundary cases
follow by limits, with no releases giving upper one. Apply this coordinatewise
to q-weighted counts; the common confidence penalty c(q,n) stays fixed.

For availability use a separate pessimistic fill: count only definitely
released outcomes when forming the lower release-rate endpoint. Both bounds
hold on the same event (1). Do not use the conditional-risk fill to claim a
lower release rate. Sound refinements shrink each possible-outcome set, so
both guarantees improve or remain unchanged for a fixed posterior.

The [finite check](selective_probe.py) / [result](selective_probe.json) uses exact
rational stopped-path calculations through prefix 12, four primitive-case
distributions, three confidence levels and eleven posteriors, including
dependent policy outcomes. All twelve crossing checks pass. Floating-point
illustrations at n=1500, 1000 released and delta=.05 give conditional bounds
5.7233%, 4.0422%, 1.6789% as potentially bad releases fall 20 to 10 to zero.
They are confidence-bound changes, not measured error reductions, and are not
outward-rounded numerical certificates. Runtime 581,058,200 ns, Python 3.12.14;
the result records its source hash.
