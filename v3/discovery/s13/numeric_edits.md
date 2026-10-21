# Value-only receipts for a numerical intervention family

Codex (GPT-6), DEVELOPMENT, October21,2026. Q1/Q2/Q3/Q5. This is a broader
representation candidate and a quick comparison screen. Sherman–Morrison–
Woodbury, Kron reduction, rational interpolation and fractional programming
are established methods. The proposed task contract below is an adapter;
no new numerical-analysis theorem or algorithmic superiority is claimed.

## A stated mechanism is indispensable

Let A be a fixed unknown symmetric positive-definite matrix. A stipulated
intervention replaces A by A+tUU^T, with t>=0 and U having at most r columns.
Fix input b and output c. The requested value is

    y(t)=c^T(A+tUU^T)^(-1)b.

This can represent a known rank-bounded stiffness/conductance edit or a
family of numerical linear problems. It is not a generic logical
counterfactual rule, and observations alone do not warrant its mechanism.
All evaluations, precision, matrix products, solves and model assumptions
are paid/source-bound duties. Changing b,c or the edit directions changes
the task. A globally incorrect full model may nevertheless predict this
one curve exactly; that is the adequacy target being tested.

Writing V=U^TA^(-1)U, g=U^TA^(-1)b and h=U^TA^(-1)c gives the ordinary identity

    y(0)-y(t)=d(t)=t h^T(I+tV)^(-1)g.

Because V is positive semidefinite, d=P/Q where P has degree at most r and
P(0)=0, while Q=det(I+tV) has degree at most r, Q(0)=1 and nonnegative
coefficients. Q is positive for every t>=0. Thus the retained task can have
2r scalar rational coefficients even if A has far more unknown entries.
This is a representation count, not a bit/storage/accuracy cost claim.

## Exact values repair the whole stated curve

Suppose y(0) is already retained and exact d(t_j) are purchased at 2r
distinct positive t_j. Solve the linear equations

    sum_l p_l t_j^l = d(t_j)*(1+sum_l q_l t_j^l),
    q_l>=0,                              l=1,...,r.

An actual coefficient solution exists. Any feasible solution gives the
same curve at every nonnegative t. Indeed, cross-multiplying it with the
actual P/Q gives a polynomial of degree at most2r. It vanishes at all2r
sample points and at0, hence is identically zero. Positive denominators
exclude spurious zero-over-zero interpolation at a purchased point. This
also handles lower actual degree and nonunique coefficient solutions:
uniqueness of the rational function is what matters.

For r1, d(t)=tp/(1+ta), with a>=0. Two nonzero observations recover p,a
when p!=0; if one positive-time d is exactly zero, p=0 and the whole curve
is constant. Two are a sufficient worst-case count, not a lower bound on
every instance or arbitrary kinds of information purchase.

One nonzero observation generally does not suffice. Take b=c=e1,U=e2,
and two inverse matrices

    A1^(-1)=[[1,1/2],[1/2,1]],
    A2^(-1)=[[1,3/4],[3/4,7/2]].

Both are positive definite. Both have y(0)=1 and y(1)=7/8, but y1(2)=5/6
whereas y2(2)=55/64. A model fitting the original value and one edited
value can still misrank a later edit against a threshold between these.

Shared affine report units z(t)=alpha*y(t)+beta do not obstruct predicting
the report curve: differences multiply P by alpha, leaving Q unchanged.
This does not calibrate alpha or price comparisons in external units.
Unknown arbitrary monotone recodings need not preserve the rational family.

## Incomplete numerical work can still certify a decision

Suppose purchased evaluations only warrant l_j<=d(t_j)<=u_j, and the
baseline is exact. Keep the coefficient polyhedron

    q_l>=0,
    l_j Q(t_j)<=P(t_j)<=u_j Q(t_j).

It contains the actual curve coefficients. It may include nonphysical
rational functions, so its resulting bounds are conservative. At a new
fixed t>=0, deciding whether all compatible d(t)<=z is an ordinary linear
inequality implication P(t)-zQ(t)<=0. A primal counterexample or an LP dual
certificate gives a checkable task answer. Sharp scalar ratio bounds for
this outer family use ordinary linear-fractional programming. Further
interval refinement only shrinks the family. An empty polyhedron reports
inconsistent premises/receipts, not a valid answer to everything.

No acquisition count analogous to the exact2r result follows under noise.
Ill-conditioning can make small value errors uninformative away from the
probed region. Unknown baseline errors require joint variables or interval
constraints, rather than treating correlated differences as exact. Exact
arithmetic certificates do not supply physical measurement reliability.

## Early disposition

This supplies a concrete non-Boolean connection between useful values,
fallible full models, bounded computation and changed mechanisms. It avoids
requiring identification of A to answer a declared edit family. But ordinary
data-driven model reduction already has this organizing idea and stronger
interpolation algorithms. Dörfler and Bullo's
[Kron-reduction paper](https://motion.me.ucsb.edu/pdf/2011d-db.pdf), §III.D,
TheoremIII.14, gives explicit interior-edge sensitivity identities.
Mayo and Antoulas's
[generalized realization framework](https://doi.org/10.1016/j.laa.2007.03.008)
is a close rational-interpolation antecedent (abstract inspected, full
algorithm not reconstructed here). Keep the task-specific noisy certificate
route as an option; do not build a large solver benchmark or label the basic
compression a new contribution. A useful next question is whether paid
partial value intervals certify requested edits sooner than strong ordinary
residual-based and rational-model controls under identical resources.
