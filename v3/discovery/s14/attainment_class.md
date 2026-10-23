# When the two-scalar lower envelope has a finite extremizer

Codex (GPT-6), DEVELOPMENT, October 23, 2026 UTC. Continues the proposed
theorem in second_receipt.md; same-model derivation, not independent review.

Let e>0, 0<s<1 and s^2<m<s. Set q=sqrt(s-m). The sharp lower infimum
L=s^2/[m+(q+e*sqrt(m))^2] is attained by finite matrices if and only if

    e=(2*m-s)/sqrt(m*(s-m)).                              (1)

In particular the right side must be positive. For the separate boundary
m=s^2, a scalar construction attains the bound for every e. At e=0 no
edit occurs. At s=m=1 a rank-one edit attains 1/(1+e^2). The boundary
m=s<1 is not a finite old receipt pair.

## Necessity

Write w=(I+MM^T)^(-1)v, z=M^T*w, ||w||=sqrt(m), ||z||=q, H=N-M.
Equality in the two inequalities used by the lower-envelope proof forces

    H^T*w=(e*sqrt(m)/q)*z,
    H*z=(e*q/sqrt(m))*w.                                 (2)

The first identity follows from equality in the triangle and operator-norm
bounds. The second follows because ||H^T*w||=e*||w|| implies
H*H^T*w=e^2*w for a contraction H/e. Put a=e*sqrt(m)/q. Since M*z=v-w,

    (I+NN^T)*w=(1+a)*v+beta*w,
    beta=-a+e*q/sqrt(m)+e^2.

Equality in the variational restriction to multiples of w requires the
true new response vector to be alpha*w, alpha>0. Because m>s^2 makes
v,w linearly independent, this is possible only when beta=0 and
alpha=1/(1+a). Solving beta=0 gives (1).

## Sufficiency

Choose unit v and w with v^T*w=s, ||w||^2=m in dimension two. Set
M=(v-w)/q as one column and H=e*w/sqrt(m). Then M^T*w=q, the old moments
are s,m, and ||H||=e. Under (1), the displayed identity gives
(I+NN^T)*[w/(1+a)]=v. Thus g(N)=s/(1+a)=L.

Equivalently m/s is the sensitivity-maximizing ratio r_star(e) from
second_receipt.md. This recovers the special finite extremizers behind
the one-scalar linear branch. The remaining interior pairs have a strict
inequality g(N)>L for every finite pair, although the earlier two-dimensional
diagonal sequence approaches L while preserving both old moments exactly.

## Why the distinction matters

The result separates an information-limited infimum from an actual finite
counterexample. Strict threshold decisions at exactly L can use this fact,
but numerical receipts generally remove that knife-edge benefit. A finite
operator-norm cap prevents the unbounded sequence; the dimension reduction
in finite_geometry.md makes the capped feasible set compact. This is a
mathematical boundary clarification, not a demonstrated resource saving.
