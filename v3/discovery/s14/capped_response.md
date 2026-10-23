# A norm cap makes the one-receipt lower envelope stronger

Codex (GPT-6), DEVELOPMENT, October 23, 2026 UTC. This extends the
receipt-limited counterfactual calculation; no novelty or confirmation verdict.

Let ||v||=1, g(M)=v^T(I+MM^T)^(-1)v=s, ||M||<=K, and ||H||<=e.
Feasibility requires l=1/(1+K^2)<=s<=1. Hidden dimensions are unrestricted.
The lower endpoint for g(M+H) has a one-dimensional exact construction.

## An intermediate optimal residual curve

For t>=0 let R(t) be the smallest possible ||v-Mz|| over all such old M
and vectors z with ||z||=t. For 0<s<1 put

    x=sqrt((1-s)/s),
    t_K=sqrt((1-s)/(1+K^2)),
    t_0=sqrt(s*(1-s)),
    c=sqrt((1-s)*(1+K^2)).

Then

    R(t)^2=1-2*c*t+K^2*t^2,          0<=t<=t_K;
    R(t)^2=s-t^2,                    t_K<=t<=t_0;
    R(t)=1-x*t,                      t_0<=t<=1/x;
    R(t)=0,                         t>=1/x.               (1)

For s=1, R(t)=1. Values and first derivatives join at the displayed
boundaries. This is a best-possible information curve, not the residual
curve of one fixed old matrix across every t.

To prove it, write z=t*e_1 and b=Mz. The first column fixes b/t, with
||b||<=K*t. With all other columns zero the old value is
1-(v^T*b)^2/(t^2+||b||^2). Other columns can monotonically lower this
to l by completing MM^T to K^2*I. Therefore old value s is attainable
iff the first-column-only value is at least s. For a=||b||/t, the largest
permitted projection v^T*b/t is min(a,sqrt((1-s)*(1+a^2))). Minimizing
1-2*t*projection+t^2*a^2 over0<=a<=K gives (1): the optimum is K,
then sqrt((1-s)/t^2-1), then x, then1/t in the four respective regions.
The t=0 case follows directly. Two row coordinates and added completion
columns suffice for this intermediate feasibility argument.

An edit can move Mz by any vector of norm at most e*t, so

    inf g(M+H) = min_(t>=0) [max(0,R(t)-e*t)]^2+t^2.    (2)

Interchanging the two minima is legitimate: g itself is a minimum over z.
Every feasible (t,b) has an old-operator completion, and a rank-one edit
can move b toward v by min(e*t,||v-b||). Conversely every actual triple
(M,H,z) satisfies this residual lower bound.

## Piecewise endpoint and finite extremizers

For e>0 let a=(sqrt(e^2+4)+e)/2, s_plus=a^2/(1+a^2), and
s_cap=(1+a^2)/(K^2+2+a^2).

- If s>=s_plus, the uncapped scalar endpoint remains exact:
  1/[1+(sqrt((1-s)/s)+e)^2]. Its scalar old operator fits the cap.
- If s_cap<=s<=s_plus, the uncapped linear endpoint s/a^2 remains exact.
  The finite rank-one extremizer has old norm squared
  (1+a^2)/s-(2+a^2)<=K^2.
- If l<=s<s_cap and s<s_plus, minimize

      F(t)=[sqrt(1-2*c*t+K^2*t^2)-e*t]_+^2+t^2

  on[0,t_K]. This is a convex scalar problem, strictly convex because
  of t^2, and its value is the exact endpoint. For e>0 the minimizer is
  interior except for degeneracies inherited from the branch joins.
  This branch strictly improves the uncapped envelope.

The interval s_cap<=s<=s_plus is empty if K<1/a; then every feasible s
is in the scalar branch. At e=0 the endpoint is s, and at s=1 it is
1/(1+e^2). For the capped branch, take the single column

    M=(c, sqrt(K^2-c^2))^T, v=(1,0)^T.

At the minimizing t, choose H in the direction v-t*M, of length e.
The optimum has R(t)>e*t; first-order optimality makes t the actual
new scalar least-squares solution. This realizes (2) with TWO rows and
ONE column. Thus no dimension limit or infinite operator norm is needed.

The middle-region minimizer without a cap is t=sqrt(s/(1+a^2)); it lies
above t_K exactly when s>=s_cap. The last-region minimization yields the
scalar endpoint. These observations establish the branch choices in (2).

## Relation to two old moments

For w=(I+MM^T)^(-1)v, m=||w||^2 and s^2<=m<s, the smallest possible
old operator norm is

    K_min^2=(1-2*s+m)/(s-m).

Indeed Mz=v-w, ||z||^2=s-m forces this lower bound, and
M=(v-w)*z^T/(s-m) attains it while M^T*w=z. Consequently a cap imposes
m<=(1+l)*s-l. The sharp two-moment UPPER extremizer in two_scalar_upper.md
already uses this minimum-norm old operator, so a feasible cap does not
further improve that upper endpoint. The lower endpoint can improve.

This is a paid extra structural premise: K is not inferred from s. The
ordinary least-squares variational and conic formulations are direct
comparators. No solver runtime, complete-cost saving or external novelty
assessment has been established.

capped_probe.json passes120 explicit endpoint constructions,240 small
actual-matrix inequalities and240 residual-curve checks. These use floating
scalar minimization with exact rational input matrices, not outward solver
certificates. At s=0.1,e=1,K=4 the proposed sharp lower endpoint is about
0.0452737201423, versus0.0381966011250 without the cap (18.5281% stronger).
The extra information is essential: the norm cap alone gives only1/26.
The matching upper endpoint and partial-value rule are in capped_upper.md.
