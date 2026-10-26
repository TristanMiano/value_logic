# N16 screen: what a conventional second-moment reduction supplies

Codex (GPT-6), October25,2026 UTC. DEVELOPMENT; same-model comparison.
This is the capped novelty screen, not a new N16 extension or confirmation.
The [original event](../s17/claim.md) remains fixed. This note tests a possible
routine route to the analytic formula, rather than merely observing an SDP tie.

Let0<C<I, ||c||=1, H=I-C, E=e^2>0, and h=(E+sqrt(E^2+4E))/2.
Write Q=W^T S^2 W for the unretained second-response block. Standard
compression gives C^2<=Q<=C. Every C^2<=Q<C is realizable by the finite
completion in [the prior development](../s17/completion.md); Q=C is a boundary
relaxation. Define T=C-Q. The exact retained-(C,Q) formulas were developed
separately in [s17](../s17/second_block.md). Their exactness is a premise of
the first reduction below, not something granted by a generic minimax theorem.

## Upper endpoint: eliminate the hidden moment by ordinary convex minimax

For a trial coefficient alpha, put

    A(alpha)=1-2c^T H alpha+alpha^T H alpha,
    q_Q(alpha)=alpha^T(C-Q)alpha,
    J_Q(alpha)=A+E q+2e sqrt(q(A-q)).

A is the old primal objective and is positive. For every Q in[C^2,C],
0<=q<=qmax=alpha^T C H alpha and A-q>=0. The last property follows
from the positive Gram representation of the old residual.

For fixed Q, J_Q is convex in alpha: it is the squared sum of the old
residual norm and e times the old coefficient norm, plus the coefficient
norm squared. This remains convex when T is singular. For fixed alpha,
J_Q is concave in Q, since q is affine and sqrt(q(A-q)) is concave on[0,A].
The Q interval is compact and convex. Sion therefore gives

    max_Q inf_alpha J_Q(alpha) = inf_alpha max_Q J_Q(alpha).       (U1)

For each alpha, varying Q over the interval fills every q in[0,qmax],
for example by the segment joining C^2 and C. Young's exact variational
identity gives

    J(A,q)=inf_(eta>0) [(1+eta)A+(E+E/eta-eta)q].                 (U2)

The right side is affine in q and convex in eta, so another application
of Sion on compact q in[0,qmax] yields

    max_q J(A,q)
      =inf_(eta>0) [(1+eta)A+max(E+E/eta-eta,0)qmax]
      =inf_(0<eta<=h) [(1+eta)A+(E+E/eta-eta)qmax].              (U3)

The last equality follows because eta>h makes the coefficient of q
negative and leaves(1+eta)A, minimized over that range at h. At eta=0
use the usual limit/closed perspective. Exchanging the two infima over
alpha and eta and minimizing the positive quadratic in alpha gives

    inf_(0<=eta<=h) a b c^T C(aI+kappa C)^(-1)c,
    a=1+eta, kappa=E+E/eta-eta, b=a+kappa.                       (U4)

This is precisely N16's upper formula after its recorded scalar change
of parameter. The cap h arises from the sign of an elementary multiplier.
No new generic optimization principle is needed to obtain the formula.

## Lower endpoint: the same sign cap after convex minimax

For0<r<1, define

    ell(Q,r)=c^T C [Q+(C-Q)/r+E Q/(1-r)]^(-1) Cc.                (L1)

This is the fixed-Q lower dual with t=(1-r)/r. For fixed r it is convex
in Q, by matrix inverse convexity. For fixed Q it is concave in r: use
the variational maximum over w of

    2c^T Cw-w^T Qw-w^T(C-Q)w/r-E w^T Qw/(1-r).

The expression is jointly concave in(w,r); all matrices multiplying the
quadratic perspectives are positive semidefinite. The Q interval is
compact and ell is continuous there for each interior r. Sion gives

    min_Q sup_(0<r<1) ell(Q,r)
      =sup_(0<r<1) min_Q ell(Q,r).                              (L2)

In t coordinates the denominator is(1+t)C-dQ, d=t-E-E/t.
For d>=0 its inverse is minimized at Q=C^2. For d<0 it is minimized
at Q=C, giving s/(1+E+E/t), s=c^T Cc. That scalar is increasing in t,
so the portion t<h cannot exceed its value at h. The optimized expression
therefore reduces to

    max_(t>=h) c^T C[(1+t)I-dC]^(-1)c,                          (L3)

exactly N16's lower formula.

## What this does and does not settle

The two scalar formulas and their common cap are conventional minimax
consequences once the fixed-second-block extremal problems are supplied.
This is a more explicit comparison than a generic exact-SDP observation.
It does not by itself settle N16's contribution event: the fixed-Q lower
exactness includes a completion/limiting argument, and closure at Q=C
does not establish finite attainment for the original strict class.
Those steps must be mapped to inspected prior results or retained as part
of the particular synthesis. The old direct endpoint witnesses resolve
the latter mathematical duty, but not its novelty judgment.

The comparison must not cite our own s17 extension as an external theorem
and thereby declare N16 routine by circular attribution. The useful next
question in this capped screen is which fixed-Q reduction and equality
steps actually follow immediately from the closest primary prior.

## The comparison can avoid the fixed-Q exactness premise

For the purpose of obtaining N16's bounds, the full fixed-Q endpoint
theorems are unnecessary. Ordinary primal reuse gives F<=inf_alpha J_Q;
the retained-response dual squares give F>=sup_r ell(Q,r). Applying the
two minimax reductions to these inequalities yields the same universal
endpoint bounds. Only equality at the selected canonical or cap moment
needs checking. Thus our own fixed-Q extension is not required as an
external theorem, nor does its limiting construction supply novelty here.

There is no hidden compactness assumption in U1: J_Q>=A and
A=s+(alpha-c)^T H(alpha-c), uniformly over the closed moment interval.
All minimizing alpha can be restricted to one compact ball since J_Q(0)=1.
This also makes min_alpha J_Q continuous in Q, justifying the closed
moment relaxation for values. Lower inverse matrices are positive for
each interior r, including Q=C, because C>0. Finite attainment still
requires an actual compatible source.

## A smaller finite cap witness

This is a consequence found during the equality comparison, rather than
a new promotion requirement. Put s=c^T Cc, m0=c^T C^2c and
g=c^T C(I-C)c=s-m0>0. At either cap the required second moment is

    m_star=s(1+h)/(2+h)  (lower),
    m_star=s/(2+h)      (upper).

The respective endpoint derivative condition gives m0<=m_star<s.
Let delta=m_star-m0. If delta>0, define the column

    v=sqrt(delta) C(I-C)c/g,
    Q=C^2+v v^T,  T=C-Q,
    W=[I;0], R=[C;v^T], X=T^(1/2), M=(W-R)T^(-1/2).             (F1)

Here v^T[C(I-C)]^(-1)v=delta/g<1, hence T>0. Also
R^T(W-R)=T, MX=W-R and M^T R=X. These identities imply
R=(I+MM^T)^(-1)W, W^T R=C and c^T R^T Rc=m_star.
The source has n=k+1 outputs and p=k inputs. For delta=0, omit the
zero hidden row and use n=p=k. This uses elementary rank-one moment
completion; it is not a new general completion theorem.

Write w=Rc, x=Xc. For the lower cap, the edit
Delta=e(w/||w||)(x/||x||)^T satisfies
(I+(M+Delta)(M+Delta)^T)w=(1+h)Wc. For the upper cap, choose the
negative sign: the new residual at x is(1+h)w and
(M+Delta)^T[(1+h)w]=x. The norm ratios are exactly those in the old
cap proof, so these finite sources attain the endpoints. Interior and
cancellation branches already use n=p=k. Thus one extra output
coordinate suffices for every scalar endpoint; input dimension k suffices.

This output dimension is necessary for a strict cap requiring delta>0.
If n=k, W is orthogonal and Q=C^2, whereas equality in the cap's Young
step requires c^T Qc=m_star. Input dimension p>=k is necessary for
every source in the class because I-C is positive definite and
I-C=W^T M(I+M^T M)^(-1)M^T W has rank at most p. This is a
dimension statement for scalar equality, not simultaneous equality for
all targets or a fixed ambient source.

The smaller witness further weakens any suggestion that the cap requires
an intrinsically difficult new dilation theorem. The possible contribution
is the useful explicit sharp-information corollary and its decision
interface. Whether that synthesis clears moderate novelty remains a
literature and contribution judgment, rather than a question of ordinary
versus value-logic algorithms.

For the necessity claim above, the exact cap bound chain can be displayed
without assuming that every optimal edit has our rank-one form. For any
compatible source write w=SWc, x=M^T w, m=||w||^2, q=||x||^2 and m+q=s.
At h, a=1+h and E=h^2/a. In the lower variational bound, testing w/a gives

    F(N;Wc)>=2s/a-[m+||N^T w||^2]/a^2
           >=2s/a-[s+E m+2e sqrt(m q)]/a^2 >=s/a.

The last inequality is the largest-eigenvalue bound for
[[E,e],[e,0]], whose largest eigenvalue is h. Equality forces m=a*q,
so m=m_star. For the upper bound, testing the old x gives

    F(N;Wc)<=q+(sqrt(m)+e sqrt(q))^2
           =s+E q+2e sqrt(m q) <=a*s.

Equality in this cap value forces q=a*m, by the analogous2-by-2 matrix.
Thus no alternative edit in n=k can avoid the required second moment.
The smaller rectangular source has an unobserved eigenvalue1 in S when
rank(M)=k<n; this is allowed by the original claim, which requires only
0<C<I, not S<I on all output coordinates. It does not introduce an
infinite-norm source or change the information class.

The exact two-case check uses C=diag(1/8,1/4) and c=(3/5,4/5), with
rank-one moment increases1/9 and1/400. It attains lower5699/90280 and
upper10291/15400 at the separately stated edit budgets in
[cap_rank_v2_result.json](cap_rank_v2_result.json). These are structural
equality checks, not benchmark improvements or an audit of every branch.
