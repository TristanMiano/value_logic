# One transformed nonnegative objective checks a repeated repair

**DEVELOPMENT — Codex (GPT-6), October14,2026 UTC.**

Let V be the original feasible binary violation vectors, and suppose the
requested logical source contains m independent copies of that source.
The same feature cost z_i in[l_i,u_i] applies to every copy. A supplied
complete action gives m feasible vectors and count a_i in{0,...,m}. This
does not require equal cardinality or a matroid. Its exact repair regret is

```math
R(a;l,u)=\sum_i a_i u_i-
   \min_{v\in V}\sum_i\left(a_i(u_i-l_i)+m l_i\right)v_i.
```

For a fixed comparison v, coefficient a_i-mv_i is nonnegative when v_i=0
and nonpositive when v_i=1. Maximize independently over each interval,
then collect the terms involving v. Interchanging the finite maximum over
v and the box maximum proves equality. A minimizing v identifies an
attaining corner: use l_i where v_i=1 and u_i otherwise. Correlated cost
coordinates do not justify that corner; a Cartesian box enclosing them
still gives a safe upper bound, but equality may fail.

Define q_i=a_i(u_i-l_i)+m l_i, which is nonnegative for nonnegative admitted
costs. A checked scalar lower L_q<=min_v q dot v gives the regret upper
U_a-L_q, where U_a=sum a_i u_i. A feasible q-witness of cost W_q gives
the regret lower U_a-W_q. The certificate width is exactly W_q-L_q.
Thus the existing ordinary nonnegative weighted-proof interface can check
this fixed-action claim; no free scenario enumeration or signed objective
solver is required. Proof production, source transport and checking still
have to be implemented and billed on any service claiming this saving.

An anchor in[l_0,u_0] and replacement price P give repair bound
max(R,U_a+u_0-P). Replacement bound is
max(0,P-l_0-m min_v(l dot v)). These are separate requests for scalar
lower evidence when needed. No upper-cost term is cancelled against a
fixed replacement price merely because it is common to all repairs.

For m=1, this is the classical action-induced worst scenario for interval
minmax regret, explicitly described in Kasperski and Zielinski,
[2016 survey](https://ki.pwr.edu.pl/zielinski/publications/papers/survey16.pdf),
section2.2.2 pages11–12. The repeated-source expression is its elementary
count extension; no new robust-optimization principle is claimed. For a
matroid the transformed minimum is an ordinary minimum-weight basis; for
general CNF it can remain expensive. Optimizing a over all actions is a
different problem from checking one supplied action.

The exact interval model is not the finite-cohort mode model of F01/S28-B1.
An enclosing feature box may discard dependence and weaken its certificate.
Consequently this is a possible new source interface, not an unexecuted
claim that the old S28 calls can be removed.

**Prospective br01 finite screen:** all18 mc01 basis families plus three
seeded arbitrary nonempty binary families per n2..6 (seed8141760). Use all
family vectors once as the actual repeated action. For n<=4, all receipt
states in{unknown,0,1,2}^n; for larger n,128 seeded mixed intervals drawn
from[0,0],[0,1],[0,2],[1,1],[1,2],[2,2]. Compare the transformed minimum
with every compatible box corner, and compare repair/replacement bounds
at three prices and anchor endpoints0,2. Check that weakening a true
scalar lower widens the upper bound by exactly the same amount. Include
the two-feature shared-cost example where independent-box regret2
overstates actual regret0. This screen acquires no physical costs/proofs.
