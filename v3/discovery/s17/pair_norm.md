# A finite source-norm cost for approaching the universal contrast

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; separate from N16-C/v1.
Use g,lambda and the positive curvature constant K from
[pair_gap.md](pair_gap.md). To avoid overloading that constant, write B
for a known bound on the original source norm: ||M||<=B. Then
S_M>=[1/(1+B^2)]I=beta*I. The spectral loss bound gives

    g*s-contrast >= K*beta*||(S_M-lambda*I)Wc||^2
                   >= K*beta*||(C-lambda*I)c||^2.   (N1)

Thus every finite norm budget creates a positive deficit unless
Cc=lambda*c. It quantifies why a supremum obtained only through
unbounded hidden source norms need not describe a bounded application.
The new premise is essential: it is not available from C alone.

For fixed0<C<lambda*I and beta<lambda_min(C), the explicit construction
in [pair_block.md](pair_block.md), with delta=beta, has source norm
sqrt(1/beta-1)=B and contrast deficit

    g*beta*(lambda-s)/(lambda-beta).                 (N2)

Combine N1 and N2 to bracket the exact optimum over sources obeying B:

    K*beta*||(C-lambda*I)c||^2
       <= g*s - sup_(||M||<=B, compatible edits) contrast
       <= g*beta*(lambda-s)/(lambda-beta).

Both constants are strictly positive for fixed C,c in this regime.
Consequently the deficit is Theta(1/B^2) as B tends to infinity, with
explicit bounds. This is an asymptotic order statement about the
information class, not a measured computational convergence rate.

The lower estimate follows directly from z>=beta and the squared spectral
gap; the upper estimate is a genuine finite source and two edits, so the
order does not depend on numerical optimization. No exact bounded-source
diameter is asserted. Ordinary completion and scalar functional calculus
give the construction; novelty of this consequence remains unassessed.
