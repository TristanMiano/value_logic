# A restricted price path needs a smaller operational warrant

Codex (GPT-6), DEVELOPMENT, October21,2026. Adapter combining ordinary
parametric closure with the threshold-response preimage compiler. This is
not a new parametric-flow algorithm or an all-price guarantee.

Use ordered_responses.md's fixed, nonempty feasible action system A on
N=sum_i K_i threshold bits b_i,k=1[a_i>=k]. Its constraints are implications
and units, so feasible assignments are closed under intersection and union.
Consider the one-parameter objective

    c_lambda(b)=constant(lambda)+sum_v (d_v-lambda*w_v)*b_v, w_v>=0.

Fix a finite lambda interval and the greatest optimal assignment at each
lambda as the tie rule. The additive constant can keep absolute prices
nonnegative if required; it never changes the selected action.

## Ordinary nesting, with the exact tie convention

Let U be the greatest optimizer at lambda1 and V at lambda2>lambda1.
Optimality against U intersection V and U union V implies

    c_lambda1(U)+c_lambda2(V)
      -c_lambda1(U intersection V)-c_lambda2(U union V) <=0.

By modularity the left side is (lambda2-lambda1)*sum_(v in U minus V) w_v,
which is nonnegative. Therefore equality holds and U union V is an optimizer
at lambda2. Greatestness of V gives U subset V. Greatest optimizers exist
because the minimizers of the modular objective on this lattice are closed
under union. Thus the selected action vectors form an increasing chain with
at most N+1 distinct members over the entire price interval.

This is established monotone parametric optimization. A parametric minimum-cut
algorithm can construct the breakpoints; its preprocessing and arithmetic are
paid. Enumerating all feasible actions to find them is not the proposed
efficient implementation. The guarantee concerns this selected policy, not
every tied optimum: a zero objective can have exponentially many ties.

## Compile exactly what that whole policy needs from the world

Let the distinct chain be a^(0)<=...<=a^(m), m<=N. For one physical goal
implication y_i=>y_j, the common success condition over the chain is

    for every chain pair(s,t)=(a_i,a_j):
        theta_j>t implies theta_i>s.

This is the same ordinary weakest-precondition substitution as before, now
on a much smaller exposed menu. For equal s keep only the smallest t; for
equal t keep only the largest s. The remaining staircase has both coordinates
strictly increasing, hence at most min(K_i+1,K_j+1) pairs. Remove tautological
or impossible endpoint clauses using the declared finite threshold domains.
A positive goal unit needs theta_i<=a_i^(0); a negative one needs
theta_i>a_i^(m). Their conjunction W_ray is exactly the largest world set
on which every selected policy action succeeds.

An equivalent membership test at a complete threshold world is especially
simple. For each implication find the first chain action at which a_i>=theta_i.
If there is none, that implication is safe throughout. Otherwise check
theta_j<=a_j at that first action. Subsequent actions only increase a_j.
For a truthful product-box receipt [L_i,U_i], use L_i in that first-crossing
test and U_j on the consequent. This is an exact universal test over the box,
since its endpoints can occur jointly. Correlated receipt sets may admit a
less conservative test; do not silently treat box validity as exact for them.

Compared with compiling arbitrary near-optimal action-pair projections, this
route can replace many constrained optimization calls by a paid parametric
policy construction and staircase traversal. It protects all lambda values
in the declared interval without assuming that every near-optimal action can
occur along that price path. No numerical resource saving is measured here.

## Boundaries that change the warrant

W_ray may admit worlds outside the generating model F. Keep optimizing the
original A with the original ray/tie rule; do not infer that all actions
certified after conditioning F remain safe. Changing the ray, goal, effect
model, availability or tie rule changes the protected policy. Arbitrary
multi-parameter changes are not a chain. Allman/Lo/McCormick's general
two-parameter min-cut obstruction warns against importing the one-parameter
bound; its full graph class is broader than our hard-closure fragment.

Calibration can test the one fixed event theta in W_ray, including adaptively
refined truthful boxes. The statistical premise and purchase bill are still
needed. No new concentration theorem, label-saving percentage or empirical
deployment claim follows from the staircase representation alone. The
prospective delta is a more economical *specified* price-change service,
to be compared with an identical ordinary parametric-cut implementation.

ray_probe.py's first execution passed24 finite panels at484 exact price
points (including all pairwise line crossings and interval interiors), with
59 tied points. It checked65 selected chain actions,678 full worlds and288
partial boxes. Staircase pruning reduced133 raw pairs to80 on these exposed
panels; this is a representation count, not a workload or runtime saving.
Twelve ray warrants were strictly weaker than the all-action warrant.
The whole screen took0.0352404s and did not benchmark a parametric-flow solver.
