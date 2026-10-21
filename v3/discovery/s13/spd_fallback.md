# General positive-definite systems: a strong ordinary fallback

Codex (GPT-6), DEVELOPMENT, October21,2026. This screen closes an overbroad
extension of weak_ports.md; it is not a new numerical-analysis algorithm.

Let A be positive definite, S and T positive-semidefinite retained and omitted
updates, and y(B)=b^T(A+B)^(-1)b. Suppose an independently justified relative
bound T<=rho*A is available in the Loewner order. Then

    A+S <= A+S+T <= (1+rho)*(A+S),
    y(S)/(1+rho) <= y(S+T) <= y(S).

Thus the omission error is at most rho*y(S)/(1+rho), uniformly in every
positive-semidefinite retained update S. A coarse sufficient premise is
A>=alpha*I and T<=tau*I, giving rho=tau/alpha. With a validated retained
response interval [L,U], the full response lies in [L/(1+rho),U]. This
already permits robust threshold decisions without identifying latent ports.

The inequalities follow directly by positive-definite inverse order. They
are sharp: scalar A=1,S=0,T=rho attains the lower endpoint. No M-matrix sign
condition is needed, but the certified global relative-update bound is an
input. It can be expensive or grossly conservative, and cannot be inferred
from small singleton task effects. The zero-singleton counterexample in
weak_ports.md rules out that inference.

A proposed stronger task-specific bound would need to control the conditional
port vector and Gram matrix after retained updates. Writing the original
port data as g,V, their exact forms are

    g_T(S)=g_T-V_TS*(D_S^(-1)+V_SS)^(-1)*g_S,
    V_TT(S)=V_TT-V_TS*(D_S^(-1)+V_SS)^(-1)*V_ST.

The omitted reduction is

    g_T(S)^T*(D_T^(-1)+V_TT(S))^(-1)*g_T(S).

An initially dormant g_T=0 can therefore become active through V_TS. Bounding
only the singleton reductions misses both this activation and the inverse's
conditioning. Unmeasured cross terms or a global coercivity certificate are
not free substitutes. Certified port reduction and goal-oriented residual
estimators are strong established comparators for any such extension.

Decision: retain the elementary Loewner fallback as an explicit comparator;
do not build a general-SPD omission harness until a cheaper, independently
available premise yields a material delta. The M-matrix edit-box construction
remains a narrower adapter with a clear, falsifiable structural assumption.
