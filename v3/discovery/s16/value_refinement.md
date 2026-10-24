# Refine a counterfactual certificate through scalar values alone

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass58.
This is an ordinary coordinate-descent adapter to query_witness.md, not a
claim of a new optimization algorithm. It makes the access and progress
cost explicit when the old oracle returns only quadratic values.

Let q(z)=z^T C z,0<C<=I, and suppose exact scalar queries q(z) are available.
For a fixed target c and valid a=1+t,d=t-E-E/t>0, the upper-certificate
objective divided by a is

    f(z)=q(z)+||c-z||^2/d,
    A=C+I/d,
    z_star=(I+d*C)^-1 c.

Acquire k diagonal values q(e_i)=C_ii and one starting q(z). At an iteration,
ONE additional value q(z+e_i) gives

    (Cz)_i=[q(z+e_i)-q(z)-C_ii]/2,
    g_i=(Cz)_i+(z_i-c_i)/d,
    z_new=z-(g_i/A_ii)*e_i.

The exact identity q(z+s*e_i)=q(z)+2s*(Cz)_i+s^2*C_ii updates the retained
value without another oracle query. The certificate improves by a*g_i^2/A_ii.
No full matrix, response vector or source derivative is returned for free.

Choose coordinate i with probability A_ii/tr(A). Then, with
G=f(z)-min f and g=A*(z-z_star),

    E[G-G_new | z]=||g||^2/tr(A)
                  >= G/[k+d*tr(C)].

Thus E G_T <= (1-1/[k+d*tr(C)])^T * G_0. The inequality follows from
lambda_min(A)>=1/d. It is the conventional coordinate-descent contraction.
Setup uses k+1 scalar queries; T iterations use T more. Full recovery of a
general symmetric block from this scalar oracle uses k*(k+1)/2 values, but
supports ALL later tasks and need not be the best control for a single one.

The lower witness can be refined similarly by minimizing
||c-a*z||^2/d-a*q(z). Its positive Hessian matrix in the same convention
is A_lower=(a/d)*(aI-dC). The corresponding contraction bound is

    1-(a-d)/[k*a-d*tr(C)].

The diagonal acquisitions can be shared. Existing upper/lower witnesses
remain valid after every finite iteration, so an interruption returns the
best certified interval so far. A fallible model may propose a jump; one
new exact q-value checks whether its certificate improves. Alternating at
most one such proposal with each ordinary descent step spends at most
twice the iteration query count of that protected schedule, plus setup.
Algebra, forecast work, randomization and storing the vectors are additional.

If the best fixed-t upper certificate is below a decision threshold by a
strict margin gamma, Markov's inequality and the geometric expected-gap
bound give an explicit high-probability query budget to find that decision.
That probability concerns how quickly refinement succeeds. Soundness of
each returned certificate remains deterministic conditional on truthful
values and warrants. At equality, finite-time resolution is not promised.

Exact q-values are an actual interface restriction. Approximate values
require interval-safe updates or independently checked new witnesses;
the algebraic update above must not be applied to rounded point values.
Likewise an actual solver that returns C*z cheaply supplies a stronger
gradient control. Under that access, the scalar-query accounting may be
irrelevant. Generic coordinate descent and its rate are established; the
remaining question is whether this explicit value-only adapter has a
natural economical use beyond a standard variational implementation.
