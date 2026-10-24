# Shared unfinished-proof constraints in cost-sensitive program selection

Codex (GPT-6), October 23, 2026. DEVELOPMENT. This combines the inherited
countable bounded-program PAC-Bayes event with a joint proof state. Convex
robust optimization, ensemble disagreement and PAC-Bayes are prior concepts;
the specific partial-execution/proof adapter needs a close comparison.

Fix the same total bounded policies, prior subprobability pi, iid cases,
known per-policy cost bounds c_h and confidence event as s15/costed_programs.md.
For each finite discovered list A and prefix N, let the true policy losses
be Y_hi in[0,1]. A sound partial-proof state supplies a nonempty compact
set K containing the true summed-loss vector s_h=sum_i Y_hi. K may retain
relations between policies that separate per-policy upper bounds discard.
All future refinements must retain truth. No randomness of theorem truth
is assumed; the iid law is a declared law of sampled cases.

For eta>0, a=1-exp(-eta), target risk epsilon and confidence delta, write

    K0=-N*log(1-a*epsilon)-log(1/delta).

On the inherited common event, the following is a sufficient certificate
for a freshly drawn Gibbs policy q on each future case:

    KL(q||pi)+eta*max_(s in K) q^T s <= K0.              (1)

The event already covers all finite q, prefixes and truthful proof
refinements. The support function is convex in q, so minimizing c^T q
subject to (1) is a convex problem. A nonconvex Boolean feasible set may
be replaced by a sound convex relaxation. Its construction/solution price
is paid, and a weak relaxation can eliminate the apparent advantage.

## A small checked certificate can replace complete logical optimization

Suppose a proof entails B*y<=d, y>=0 for the flattened losses. Let Hq
repeat each policy weight over its N cases. Any rho>=0 with
B^T*rho>=Hq proves max_(y feasible)(Hq)^T y<=d^T rho. Therefore

    q>=0, sum q=1, rho>=0, B^T rho>=Hq,
    KL(q||pi)+eta*d^T rho<=K0                          (2)

is a convex feasibility certificate for safe selection. A time-limited
solver can return any verified feasible(q,rho), together with c^T q.
It need not establish optimality to support deployment under the risk
contract. Logs and exponentials require outward numerical bounds. A
primal logical maximization incumbent has the wrong direction here too.

Refining the sound feasible set can only improve the OPTIMAL certified
cost, but a particular stale dual need not exploit every new constraint.
Adding new policies with their original prior weights preserves old
choices. Acquisition prices, proof checking and selector work remain
additional to future per-case c^T q; they must be amortized explicitly.

## Binary disagreement is useful before either answer is proved

Suppose two total policies output opposite binary answers on an unresolved
case. Exactly one loss is1. Under a fair random choice, the conditional
expected loss is therefore exactly1/2, even without a proof of the label.
For general q and known binary predictions with total weight p on answer1,
the worst possible expected loss is max(p,1-p), not automatically1.
Completed proof labels use their actual weighted loss. The resulting
piecewise-linear support function is directly representable in (2).

This concerns RANDOMIZED delivery and its average future loss. It does not
make either deterministic answer trustworthy, certify a single persistent
randomly chosen program, or justify treating paired policy losses as iid.
Policies on the same case may be dependent; only the case stream supplies
the iid sampling premise of the inherited bound.

## A concrete partial-proof state and a stronger separated control

Take N=1000, eta=1, delta=.05, epsilon=.05. There are two cheap policies
of cost1 and a correct fallback of cost100, with prior(.25,.25,.5).
On960 cases, both cheap outputs have been proved correct. On the remaining
40, they disagree and the labels are still unresolved. Thus

    s1+s2=40, s1,s2>=0, s_fallback=0.

Choosing q=(.5,.5,0) has joint score20+log2 and cost1. It satisfies(1):
1-exp(-1)>.63 and log20<3 imply K0>28.5, while log2<.7.
Neither cheap deterministic policy satisfies(1), since its pessimistic
score is40+log4 and K0<1000*(.032/.968)=4000/121<40.

A stronger separated control at least keeps s1<=40,s2<=40, rather than
calling every unfinished outcome a failure. If its total cheap mass is t,
its robust score is at least40t because KL is nonnegative. Feasibility
requires t<100/121. Its certified mean deployment cost therefore exceeds
100-99*(100/121)=2200/121, approximately18.18. The joint interface
certifies cost1 on this constructed evidence state.

This is a difference in certified capability at a partial-evidence boundary,
not a measured18-fold work gain. The960 proofs, prediction acquisition,
randomization and selection have not been priced. An ordinary randomized
ensemble using the SAME joint constraint gets the same certificate. A
fixed fair ensemble can also be analyzed directly as a bounded loss in[0,.5],
potentially giving a stronger concentration bound than this general selector.
That is an essential control, not a defect to hide.

The useful next screen is whether naturally acquired partial proofs create
enough disagreement/constraint structure to justify adaptive joint selection,
against direct ensemble certification and existing semi-supervised PAC-Bayes.
No new universal induction or generic ensemble theorem is claimed.

The primary-source screen in[literature](literature.md) found direct prior
minimax ensemble aggregation and its combination with PAC-Bayes in
Balsubramani–Freund2015, plus earlier label-free disagreement bounds.
Generic novelty is therefore rejected. The remaining possible delta is
the explicit anytime unfinished-proof and bounded-program cost interface.
