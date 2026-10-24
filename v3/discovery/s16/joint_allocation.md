# Exact joint contrast allocation for an isotropic source

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass46.
This develops pass40's conservative two-target example into an exact
finite-dimensional optimization; it is not an independent verification.

Let M=alpha I_n, 0<alpha<=2, and ||N-M||F<=e. Let H be any real symmetric
matrix with eigenvalues h_i. The maximum signed response tr(H(I+NN^T)^(-1))
equals the following separable concave resource-allocation problem:

    maximize sum_(h_i>0) h_i f(alpha-sqrt(u_i))
             + sum_(h_i<0) h_i f(alpha+sqrt(u_i)),
    subject to u_i>=0, sum u_i<=e^2,
               u_i<=alpha^2 when h_i>0,
    f(x)=1/(1+x^2).                                  (1)

Zero-eigenvalue terms need no budget. For minimum contrast, negate H and
negate the resulting maximum. This permits arbitrary signs in H, unlike
the PSD-objective SDP in reachable_covariance.md.

For the reduction, the Frobenius distance to alpha I is at least
sum_i(sigma_i(N)-alpha)^2: expand the square and use tr(N)<=sum sigma_i.
For any chosen singular values, align the left singular vectors with H's
eigenvectors in their best order. A positive semidefinite N with these
eigenvectors attains that response and the distance lower bound. Maximizing
a positive h_i never needs sigma_i>alpha, and maximizing a negative term
never needs sigma_i<alpha. Taking u_i=(sigma_i-alpha)^2 proves(1).

## Why this allocation is convex optimization

Both nonconstant summands in(1) are increasing and strictly concave in u.
For a positive coefficient, put r=sqrt(u), x=alpha-r in[0,alpha].
The sign of the second derivative is the sign of

    r f''(x)+f'(x)
       = 2[alpha*(3x^2-1)-4x^3]/(1+x^2)^3 <=0.

When x<=1/sqrt(3) this is immediate. Otherwise
4x^3/(3x^2-1)>=2, since
4x^3-2(3x^2-1)=2(x-1)^2(2x+1)>=0. Thus alpha<=2 suffices;
equality is isolated and does not destroy strict concavity. At u=alpha^2,
the positive term saturates at h_i. At u=0 its derivative is infinite.

For a negative coefficient, r=sqrt(u), x=alpha+r. The relevant numerator
is f'(x)-r f''(x), equal to -2[4x^3-3alpha*x^2+alpha]/(1+x^2)^3.
The bracket is positive for x>=alpha: it is alpha^3+alpha at alpha and
has derivative6x(2x-alpha)>0. This establishes strict concavity for every
alpha>0 in the negative branch. The condition alpha<=2 concerns only the
positive branch; extending it without another argument is unwarranted.

The common marginal-value multiplier characterizes the unique allocation
on nonsaturated terms. A one-dimensional monotone search can find it;
each coordinate solves a monotone equation. A numerical point alone is
not an upper certificate. Concavity gives rational tangent upper bounds
whenever the selected square roots and alpha are rational.

For alpha=1,H=diag(1,-1),e=1/10, the exact radius is the maximum of
f(1-a)-f(1+b) over a,b>=0,a^2+b^2<=1/100. This strengthens pass40's bound
e/sqrt(2)+e^2/4. The two separately sharp target intervals still have
contrast radius4000/40001. A small exact tangent certificate can quantify
the further improvement without trusting a floating optimizer.

Primary comparison to spectral perturbation and separable allocation is
still required. The proposed value is preserving the common counterfactual
budget in a signed decision, not an unexplained claim of superiority over
ordinary optimization supplied the same information.

The [exact tangent probe](allocation_probe.json) encloses the two-target
radius between0.07088415931676074 and0.07088415931753045. Its rational
feasible witness uses a about0.0754650 and b about0.0656127. Consequently
the joint radius is at least29.11406857% smaller than4000/40001 under the
SAME Frobenius information; the earlier26.78% statement was conservative.
This is an uncertainty-radius gain, not measured computation or audit fees.
The script stores exact fractions, not just these rounded displays.
It ran on Python3.12.14 in4,223,400ns, with792 supplementary rational sign
checks. The upper certificate is conditional on the concavity proof above.

The scale boundary is sharp for global concavity of the positive branch:
when alpha>2, choose x=1 and r=alpha-1. The numerator becomes2alpha-4>0.
The reduction to scalar allocations still holds, but the convex-optimization
claim no longer follows. No extrapolated local optimum is certified there.
