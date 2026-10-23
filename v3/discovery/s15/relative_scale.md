# Relative edits and regularization changes from one retained value

Codex (GPT-6), October 23, 2026. DEVELOPMENT. Extends joint_target.md.
No independent reconstruction, priority claim, or measured speedup.

Use the finite-dimensional normed-space setting and p,q,F of
[joint_target.md](joint_target.md). Let ||v||=1, F(M;v)=s in (0,1],
and suppose independently paid structural information supplies

    ||N-kappa*M|| <= e,  ||w-v|| <= eta,  kappa>0.

With a=s^(1/p), b(k)=(1+k^q)^(1/q),
t=(s^(-1/(p-1))-1)^(1/q), A(k)=a*b(k), the proposed sharp
dimension-unrestricted envelopes are

    L = min_(0<=k<=t) [(A(k)-eta)_+ / b(kappa*k+e)]^p,
    U = max_(0<=k<=t) [(A(k)+eta) / b((kappa*k-e)_+)]^p.       (1)

For the lower bound, use an old maximizing dual direction y. Its ratio
k=||M*y||_*/||y||_* obeys k<=t and <y,v>/||y||_*=A(k).
The new dual denominator is at most b(kappa*k+e) times ||y||_*.
For the upper bound, every dual direction satisfies

    <y,w>/||y||_* <= min(1,A(k))+eta,
    ||N*y||_*/||y||_* >= (kappa*k-e)_+.

For k>=t the numerator is constant and the denominator nondecreasing,
so the unrestricted supremum is attained on [0,t]. These are the same
quotient-norm arguments as the additive-edit case, with relative scale
included explicitly; no bound on ||M|| is needed.

Sharpness uses M=diag(k,K) on l_p^2 and the exact old-value target
v_K=(c_K,(1-c_K^p)^(1/p)), with

    c_K^p=(s-ell(K))/(ell(k)-ell(K)),
    ell(u)=(1+u^q)^(1-p).

For the lower endpoint take N=diag(kappa*k+e,kappa*K) and reduce the
first target coordinate by min(eta,c_K). For the upper endpoint use
N=diag((kappa*k-e)_+,kappa*K) and increase that coordinate by eta.
The operator edit has norm at most e. Since kappa>0, the second
coordinate's value tends to zero as K tends to infinity, and c_K tends
to A(k). This proves limiting sharpness uniformly over the class of
spaces and dimensions. An individual fixed space may admit better bounds.

## Scalar root reductions

When e>0 and eta<a, the lower unconstrained minimizer is the unique root
on the positive portion of

    [kappa-(k/(kappa*k+e))^(q-1)-e*k^(q-1)] /
      (1+k^q)^((q-1)/q) = kappa*eta/a.                  (2)

Its numerator decreases strictly from kappa through zero; the positive
denominator increases. The derivative of the objective has the sign of
the right side minus the left side. Clip the root at t. When eta>=a,
L=0 is already available at k=0.

For the upper bound the objective increases on [0,e/kappa]. For larger k,
its derivative has the sign of the left side minus the right side in

    [(k/(kappa*k-e))^(q-1)-kappa-e*k^(q-1)] /
      (1+k^q)^((q-1)/q) = kappa*eta/a.                  (3)

The positive part decreases from infinity to zero, giving a unique root;
clip it at t. These reductions do not authorize ordinary floating
bisection as an outward-certified numerical procedure.

With e=eta=0, write T=ell(kappa*t). The exact envelopes simplify to

    kappa>=1: [T,s];       0<kappa<=1: [s,T].           (4)

For general eta and e=0, retaining the compact one-dimensional problems
in (1) avoids unnecessary special-case root machinery.

## Zero scale is a different boundary problem

When kappa=0 the premise is ||N||<=e, independent of the old operator.
The sharp bounds are instead

    (1-eta)_+^p * ell(e) <= F(N;w) <= (1+eta)^p.        (5)

For the lower bound, ||w|| <= ||w-Nx||+e*||x|| and Holder's inequality
give F(N;w)>=||w||^p*ell(e), then ||w||>=(1-eta)_+.
Scalar examples attain both endpoints while an arbitrary old s is
realized by choosing M=t. For the upper endpoint use N=0.

Substituting kappa=0 into (1)'s lower expression gives the valid but
generally nonsharp (a-eta)_+^p*ell(e). The limiting witness used for
kappa>0 ceases to work: kappa*K no longer goes to infinity. Uniform
optimization over unbounded old operators need not commute with the
limit kappa down to zero. This is a semantic boundary, not a numerical
rounding issue, and must be explicit in a decision adapter.

## A concrete regularization interpretation

For F_lambda(M;v)=min_x(||v-Mx||^p+lambda*||x||^p), lambda>0,
the substitution z=lambda^(1/p)*x gives

    F_lambda(M;v)=F(M/lambda^(1/p);v).

Changing lambda to lambda_new and the raw model M to N_raw with
||N_raw-M||<=e_raw therefore uses

    kappa=(lambda/lambda_new)^(1/p),
    e=e_raw/lambda_new^(1/p).

This supports a regularization decision without a new operator application
after the old scalar receipt and edit warrants have been paid. It is not
a full-cost performance result. At p=2 with the raw model unchanged and
r=lambda_new/lambda, (4) uses

    T=r*s/(1+(r-1)*s).

For example s=1/10 and r=4 constrain the new value to [1/10,4/13].
Concavity, spectral Jensen bounds and value-function approximation are
strong ordinary ancestors; the example alone establishes no novelty.

## Inexact old receipts and target norm bounds

If a paid certificate only gives s in [s_lo,s_hi] within (0,1], use
[L(s_lo),U(s_hi)]. L is nondecreasing because a increases and its
minimization domain shrinks as s increases. For U, use the unrestricted
expression with numerator min(1,a*b(k))+eta, which is pointwise
nondecreasing in s. Thus one need not resolve the old value exactly.

If only ||v||<=R is warranted, R>0, normalize by R and multiply the
resulting value interval by R^p, using old receipt s/R^p and edit eta/R.
The unit-norm proof extends directly with numerator cap R and
t_R=((R/a)^q-1)^(1/q). The same norm-R witnesses establish uniform
sharpness over the larger class. A structural norm warrant must be paid;
it is not inferred from the scalar objective value.

These extensions connect fallible numerical knowledge, paid computation
and explicit counterfactual changes. They are a candidate information
contract built from ordinary duality. The practical delta and closest
prior formulation still need assessment before a useful contribution can
be forecast as ready for confirmation.

The first scale_probe.py run passes1200 floating parameter cases and
242400 scalar-grid inequalities, with diagonal limiting witnesses and
old-receipt monotonicity checks. Another108 cases exercise kappa=0.
The regularization example returns [0.1,0.3076923076923077], agreeing with
[1/10,4/13]. These finite floating checks are neither outward certificates
nor independent confirmation. The e=0 implementation also uses the direct
derivative signs of (1) to locate its possibly interior extrema.
