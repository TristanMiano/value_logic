# Which conditional values are worth calibrating?

Codex (GPT-6), DEVELOPMENT bridge; this is conventional task-relative error
propagation and allocation applied to the new response interface, not a new
statistical theorem. It connects Q4/Q5 to the grouped counterfactual model.

Let each feasible procedure have affine expected cost g(x)+sum_i theta_i v_i(x).
Write D_i=max_x v_i(x)-min_x v_i(x). If a point-estimate optimizer x_hat is
optimal at theta_hat, and |theta_i-theta_hat_i|<=delta_i, then

```math
C(x_{\rm hat},\theta)-\min_x C(x,\theta)
\le \sum_i D_i\delta_i.
```

For each comparator x, subtract the two costs at theta_hat, where the
difference is nonpositive, and bound the remaining contrast. Taking the
maximum proves the result. Thus only response ranges matter: an uncertain
coefficient adding the same amount to every feasible procedure has D_i=0
and needs no calibration for this decision. A separate absolute-budget duty
may still need it.

For an aliased group with A_g=sum_i w_i and at most H individual flips,
the exact one-group response extrema (including terminal zero) are

```math
a_g^{\max}=\max\{0,A_g+2\sum_{H\ \mathrm{largest}}(-w_i)_+\},
\qquad
a_g^{\min}=\min\{0,A_g-2\sum_{H\ \mathrm{largest}}(w_i)_+\}.
```

Their difference gives D_g. In a known query cell it is multiplied by p_z.
Separate coordinate ranges can overcount the shared global flip budget, but
remain valid. They also show a real cost of enlarging the revision menu: more
allowed changes can make additional uncertainty decision-relevant, even though
the larger menu cannot worsen the true source-aware optimum.

Suppose, specifically, a priced oracle supplies independent fresh +/-1 samples
of each conditional mean at price f_i per sample. A simultaneous Hoeffding
bound over K coordinates has sample sufficiency
n_i>=2*log(2K/alpha)/delta_i^2 for fixed predeclared sample counts. Ignoring
integer rounding and inactive upper bounds on delta, the cheapest allocation
subject to sum_i D_i*delta_i<=epsilon is

```math
\delta_i=\frac{\epsilon(f_i/D_i)^{1/3}}
                 {\sum_j f_j^{1/3}D_j^{2/3}},\qquad
\sum_i f_i n_i\ \lesssim\
\frac{2\log(2K/\alpha)}{\epsilon^2}
\left(\sum_i f_i^{1/3}D_i^{2/3}\right)^3.
```

The displayed last expression is the continuous sufficiency expression, not
a strict bound after integer ceilings; add at most sum f_i for rounding, and
handle any capped halfwidth separately. Coordinates with D_i=0 can be omitted.
This familiar constrained-allocation calculation is a screening tool.

Its query interface is load-bearing. An ordinary stream may not permit fresh
conditional draws: discovering the query cell, waiting for a rare cell,
repeated identities, unresolved proof outcomes and failed purchases all have
costs. Adaptive stopping needs an appropriate time-uniform event instead of
silently reusing this fixed-sample inequality. Within-request correlated
observations cannot be selected using revealed outcomes and then treated as
unbiased unconditional labels. The s10 selection-bias record still applies.

Disposition: retain this as a cost forecast and source-admission obligation,
not an executed calibration result. Do not build another large learning panel
until a concrete access model makes its estimated acquisition bill plausible.
