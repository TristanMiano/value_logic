# Information required for selective coverage depends on the base error rate

Codex (GPT-6), October 23, 2026. DEVELOPMENT; pass 36.

Let Y=1 mean an answer is wrong, with population probability pi. Evidence E
drives a release decision R, possibly using extra independent random coins.
Let q=P(R=1), and require P(Y=1|R=1)<=epsilon. If pi<=epsilon, releasing
everything already meets the requirement with zero information. No positive
abstention lower bound follows from an upper bound on I(Y;E) alone.

For 0<=epsilon<pi<1, feasibility requires q<=(1-pi)/(1-epsilon). Define

    J(q;pi,epsilon) = h(pi)-q h(epsilon)
                     -(1-q) h((pi-q epsilon)/(1-q)),              (1)

with continuous endpoint conventions and natural-log binary entropy h.
Then I(Y;E)>=J(q;pi,epsilon). This is SHARP as an extremal information
statement: take E=R with P(Y=1|R=1)=epsilon and
P(Y=1|R=0)=(pi-q epsilon)/(1-q). It does not construct such evidence from
an arbitrary given model or computational oracle.

Proof: data processing gives I(Y;E)>=I(Y;R). For fixed coverage q, write
b=P(Y=1|R=1)<=epsilon and r=(pi-q b)/(1-q). The information is
h(pi)-q h(b)-(1-q)h(r). Since b<pi<r, increasing b toward epsilon reduces
this expression (derivative q[h'(r)-h'(b)]<0). Its minimum is therefore (1).
The stated joint distribution proves attainability.

Equivalently, J=q kl(epsilon||pi)+(1-q)kl(r||pi). It increases strictly
and convexly over its nontrivial domain:

    J'(q)=kl(epsilon||r),
    J''(q)=(pi-epsilon)^2/[(1-q)^3 r(1-r)]>0.

Thus an information ceiling kappa gives coverage at most the unique inverse
of J, capped by (1-pi)/(1-epsilon). The simpler bound
q<=kappa/kl(epsilon||pi) follows by dropping the second KL term. Its small
kappa slope is sharp. The base rate and target error are essential premises.

## Cost and logical-uncertainty scope

If a sequential acquisition oracle supplies at most c nats of conditional
information about Y per active query, uniformly over the past transcript,
and query choices/stopping use only that transcript and independent coins,
the chain rule gives I(Y;transcript)<=c E T. Therefore E T>=J(q)/c.
Finite expected length or a justified truncation limit is needed. This is a
query lower bound only with the stated information-per-query warrant; token
entropy, a model's confidence, or a fee schedule does not establish it.
Y varies over a task population. Repeatedly contemplating one fixed theorem
does not produce iid draws of its truth value.

## A source claim that must not be imported

Akter, Shihab and Sharma, [arXiv:2509.12527v2](https://arxiv.org/pdf/2509.12527v2),
Theorem 2.6 and Appendix C.3 were inspected while comparing selective
certificates. Appendix C.3 uses
min(KL(P0||P1),KL(P1||P0))<=2 I(Y;E). This is false: for a balanced Y
passed through a binary symmetric channel with flip probability .1, the
left side is .8 log 9, whereas the right side is 2[log 2-h(.1)]. The former
is larger. Also, a base error pi<=epsilon permits full coverage independently
of the information ceiling. These local counterexamples are sufficient to
exclude that argument as support here. Other results and experiments in the
paper were not audited. No broader conclusion about the authors is drawn.

The replacement is a direct binary information/decision frontier, closely
related to classical rate-distortion and information-constrained decision
theory. Generic novelty is not claimed. Its role in this portfolio is to keep
information, correctness, coverage and computation costs connected through
explicit premises rather than assume one controls the others.
## Uncertain base rates and an illustrative delta

At fixed feasible q and epsilon, J increases with pi, since
partial J/partial pi = h'(pi)-h'(r)>0. If only a warranted lower bound
pi>=pi_L is available, use pi_L for a necessary information bound. If
pi_L<=epsilon, that evidence supplies no positive information requirement.
In particular, many proofs of correctness without any warranted baseline
error lower bound cannot establish that abstention or new information is
necessary. A guarantee under a changed population must re-establish this
premise; the same numerical information ceiling can imply a different frontier.

[The numerical screen](information_probe.py) checks 18,966 feasible binary
joint laws and nine inverse-frontier examples. At information ceiling .1 nats
and target error .01, base error .1 permits at most about 69.95% coverage.
At base error .5, target zero and the same ceiling, the limit is about 13.02%.
These are sharp extremal ceilings under distinct premises, not observed model
performance. The source counterexample evaluates to 1.75778 > .73613.
Result/source hash, Python 3.12.14 and 21,917,900 ns are recorded in the
[result](information_probe.json). The roots are floating-point illustrations.
