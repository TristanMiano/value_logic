# A common partial-margin receipt can bound error conditional on release

Codex (GPT-6), October23,2026. DEVELOPMENT. Extends drift_margins.md.
Ordinary conditional distributionally robust optimization is close prior;
the local target is an explicit small-information, partial-evidence adapter.

## Fixed interface and explicit deployment change

Let a finite metric space Omega be partitioned into three nonempty sets:
B (bad release), G (good release), and O (no release). The delivered domain
is R=B union G. These sets and the protected model-use interface are fixed
before calibration. Let d_B(x),d_O(x) be distances to B and O. A deployment
coupling X~P,Y~Q has separately warranted expected edit cost at most rho.
The desired risk is Q(B)/Q(R), with a positive release-mass guarantee.

For target error epsilon in [0,1], put

    h_epsilon(y)=(1-epsilon)*1_B(y)-epsilon*1_G(y).

If Q(R)>0, conditional risk<=epsilon iff E_Q[h_epsilon]<=0. For lambda>=0,
the exact pointwise transport envelope is

    sup_y {h_epsilon(y)-lambda*c(x,y)}
      = max(1-epsilon-lambda*d_B(x), -epsilon,
            -lambda*d_O(x)).                         (1)

To verify the apparently constant good-region term: if x is in G, its
distance to G is zero; if x is in B, the first term already has the global
maximum1-epsilon; if x is in O, the last term is zero and dominates any
negative good-region term. Thus only TWO distances are needed.
The coupling inequality gives

    E_Q[h_epsilon] <= lambda*rho+E_P[(1)].             (2)

Finite transport linear-program duality makes the infimum over lambda
exact when the entire source distribution and distances are known. The
following simpler receipt does not require acquiring that full object.

## A sharp bound from two margin thresholds and one mass bound

Fix b>0,o>0 and let S={x:d_B(x)>=b and d_O(x)>=o}. A paid common receipt
states P(S)>=1-p. On S every point is a good release. Elsewhere the source
is unresolved. When

    epsilon=p+rho/b <= min(1,o/b),                    (3)

choose lambda=1/b. On S, (1) is at most-epsilon, while elsewhere it is
at most1-epsilon. Hence (2) is at most

    rho/b + p - epsilon = 0.

Separately, moving a protected source point outside R costs at least o,
so Q(O)<=p+rho/o and

    Q(R)>=1-p-rho/o.                                 (4)

If (4) is positive, (3) certifies conditional error at most p+rho/b.
This retains the fact that the same edit budget must pay for both failure
and denominator reduction. It does not divide two separately attained
worst cases. The receipt and argument also support later choices of rho
and epsilon within this stated region, with separately warranted budgets.

For b>=o, the bound is sharp over this information class in the region
(3), (4)>0. Use three points at0 (G), o (O), b (B), with source mass1-p
at0 and p atb. Move rho/b mass from0 tob. The cost is rho, every point
is released, and conditional risk is p+rho/b. Feasibility follows from
epsilon<=1. At b=o, use an appropriate three-point metric with distinct
B,O points both at distance b from G; no distinct coincident points are
required. No unrestricted formula outside region(3) is asserted here.

## Partial proof acquisition and an exact binomial calibration

Fix b,o and a predeclared iid cohort of N cases. Its latent good-margin
bits Z_i=1{X_i in S} exist even if unresolved. Sound computation supplies
lower bits L_i<=Z_i, by proving both distance thresholds. The scheduler
may choose and refine these computations using all prior receipts.

For a predeclared p0 and count threshold k, define

    alpha0=P[Bin(N,p0)<=N-k].                         (5)

If the true mass outside S exceeds p0, the probability that the latent
cohort has at least k members in S is at most alpha0. Any truthful
refinement reaching sum L_i>=k is contained in that one event. Thus with
failure at most alpha0, every such refinement that reaches k supplies
the common receipt p=p0. There is no optional sample-size or data-chosen
threshold loophole. A full confidence family would need its own scope;
this fixed test is enough for the following duty.

## Worked capability delta, with unresolved cases retained

Take N=1500,k=1470,p0=3/100,b=10,o=2,rho=1. The exact binomial tail(5)
is approximately0.01065477499317834, verified by exact integer arithmetic
in conditional_probe.json, and is less than1/20.
If1470 sound joint-margin certificates have been acquired,30 cases can
remain unresolved. Equations(3),(4) give

    conditional bad-release risk <= 13/100,
    release mass >= 47/100.

The corresponding separate worst-case bounds are Q(B)<=13/100 and
Q(R)>=47/100; dividing them gives13/47, approximately27.66%.
The joint conditional upper bound13% is53% lower than that separate-bound
calculation. Both comparisons use the same margin/mass receipt and edit
budget. These are guaranteed-bound values in a possible receipt state,
not observed failure rates, a dataset result, or a measured computation saving.

An ordinary conditional transport optimizer given the same information
matches the joint bound. Exact binomial calibration is already a stronger
appropriate control than a loose multiple-Hoeffding-grid implementation;
there is no reason to build the latter merely to claim an improvement.

## Cost, semantics and boundaries

All1470 certificates, the cohort, knowledge of the metric and protected
sets, and the deployment coupling warrant are paid. Certificates can be
partial proofs of the two distances; exact distances and the remaining30
labels need not be acquired. Counting30 unresolved cases is a capability
fact, not a claim that their computations dominate the total bill.

The good/bad distinction must protect the declared inference interface,
not merely a convenient proxy. Selecting a narrower release subset after
calibration can raise conditional error and is NOT covered by this fixed
R. No guarantee for a learned causal intervention is inferred from the
metric. If (4) is zero, conditional delivery may be undefined. A source
mass bound without both margin thresholds does not imply(3).

The exact screen checked6912 pointwise envelope equalities and1042
conditional transport cases, plus sharp three-point receipt witnesses.
It is not independent verification or a deployment experiment. The closest
primary-source screen in literature.md rejects generic priority for joint
conditional transport. The small-information adapter remains unassessed.
This is still discovery, with no readiness forecast or promotion.
