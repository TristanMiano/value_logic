# A price region, with deterministic interpolation included

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass50.
This is an economic screen of private_repairs.md, not a measured speedup.

Let h=r-d0 be the maximum number of new public error directions, D the
total polynomial degree, q>D the grid size and k the sealed batch size.
Set rho=D/q and require h*rho^k<=delta. If there are m proposals before
the rank certificate finishes, write c_A(q) for one truth-vector acquisition,
c_B(q) for one model evaluation and c_M for one exact membership check.
Up-front truth acquisition and public repair search have the upper bound

    [k+h/(1-rho)]*c_A(q).

Private model evaluations and membership work can cost m*k*(c_B(q)+c_M),
plus public-search, basis, storage and privacy-enforcement work. Even m
correct proposals cost m*k model checks unless a reusable symbolic receipt
can discharge them. Do not turn the truth-query bound into a total-cost one.

A fresh-batch control can reuse a batch until rejection, publish its failing
residual, and retire it. It has at most h epochs. A full k evaluations per
epoch costs at most h*k truth vectors; lazy rejection can use fewer. The
persistent batch beats this full-epoch component only if

    k+h/(1-rho) < h*k,

or k > h/[(h-1)*(1-rho)] for h>1. For h=1 the extra public repair is
never justified by this truth-query comparison. The full-epoch control's
cost is actually incurred only on a specified stream, for example one
true accepted scope before each false scope. This is not an expected-cost
dominance statement over arbitrary streams.

## Deterministic reconstruction is another strong control

If an available baseline B0 satisfies deg(A-B0)<=D on p input variables,
the whole residual polynomial has N=binom(p+D,D) coefficients per output.
A known unisolvent set of N points and exact vector truth queries determine
it everywhere. Subsequent A(x)=B0(x)+(A-B0)(x) uses this retained polynomial;
interpolation, storage and evaluation remain paid. The set and coefficient
representation must be available over the admitted field/domain.

For the earlier univariate D=4,r=4 example, N=5. That is LESS than the
persistent-private expectation bound1534/253>6, and gives deterministic
exact reconstruction. Thus that example cannot establish a truth-query
advantage over all strong conventional controls. For p=2,D=4, N=15;
the same private bound can improve this component, but still needs a
plausible access contract and complete prices. No dimensionality increase
is evidence that a real application satisfies those conditions.

If one fixed baseline's error already spans the full warranted rank r,
fresh public residuals can acquire r independent directions in expectation
at most r/(1-rho), with no private batch. Its rank-r stopping certificate
then covers the entire admitted common error space. When that baseline's
actual rank is smaller, a promised upper bound r does not say when this
search will finish. This distinguishes a rank-complete baseline from the
changing-model regime; both controls must be considered before deployment.

## Grid size has a price

Making q larger reduces k and the expected public-search tail, but can
increase input bit length and arithmetic work. Minimizing k alone is not
the economic objective. For a declared tariff c_A(q), compare the discrete
quantity [k+h/(1-D/q)]*c_A(q), and add model/membership/privacy costs.
The tariff is a premise or a measured implementation property, not something
established by the error probability. A bounded field and a large rational
grid are different input and arithmetic contracts.

Disposition: retain the reusable-checking mechanism and its lifetime proof;
reject a universal or univariate truth-query advantage. A useful moderate
contribution would need a natural workload where a declared expensive
truth primitive can be retained privately and these stronger controls are
either included or shown to have genuinely larger complete cost.
