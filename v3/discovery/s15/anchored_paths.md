# Retaining old numerical receipts across a sequence of edits

Codex (GPT-6), October23,2026. DEVELOPMENT; generation pass11.

For Euclidean quadratic response F(M;v), keep v fixed with norm1. Suppose
F(M0;v)=s and successive paid operator-norm edit receipts are e1,...,em.
The endpoint obeys ||Mm-M0||<=sum ej. Thus the original-value envelope
L_sum(s),U_sum(s) remains available without another operator application.
Intersect it with every bound transported from an acquired intermediate
value. Keeping the anchor is not the same as merely propagating the latest
interval, which forgets shared operator geometry.

For s+t<=1, invert the s14 sharp lower envelope to obtain the infimum
operator distance between response-value fibers s,t:

    d(s,t)=|s-t|/sqrt(s*t).

For s+t>=1 it is

    d(s,t)=|sqrt(1/s-1)-sqrt(1/t-1)|.

The first infimum may require a limiting large hidden singular direction;
do not claim finite attainment everywhere. These are distances between
sets of operators, NOT a metric on scalar responses. For example,

    d(.1,.2)+d(.2,.3)=1/sqrt(2)+1/sqrt(6)
                       < 2/sqrt(3)=d(.1,.3).

Hence individually feasible consecutive receipt pairs need not share a
single compatible middle operator. Pairwise endpoint constraints are a
cheap obstruction to a falsely composable scalar transition oracle.

In the small-response linear branch, propagation through two equal edits
uses s/R(e)^2, whereas the endpoint anchor uses s/R(2e), with
R(e)=exp(2*asinh(e/2)). Since asinh is strictly concave for e>0,
R(e)^2>R(2e), so the anchor is strictly stronger whenever both linear-branch
conditions hold. This is an information-retention delta, not a CPU claim.

Next screens: quantify a concrete threshold decision, compare ordinary
interval/abstract-interpretation reconditioning, and test whether all
pairwise response-distance constraints suffice for a full trajectory.
No claim of pairwise sufficiency or novel general anchor retention yet.

Worked threshold: s=.1 and two edits of size1 give the sequential upper
(.1)*R(1)^2 approximately .6854102, while the original anchor gives
(.1)*R(2) approximately .5828427. Both lie in their stated linear branches.
The anchored receipt certifies response below .6 where naive interval
propagation cannot. Acquisition and checking of the original receipt and
both norm bounds are still paid; the comparison concerns retained state.
