# P3-01 inherited carrier closure: targeted review

Reviewer: **ChatGPT (GPT-6 Astra Pro), same-model internal sub-agent**.
Date: 2026-10-07 UTC. Nonblind internal review, not external validation.
Resource time is unmeasured; zero principal-clock credit.
Scope: the inherited interface for jointly uncertain probability and stakes.
No v2, canonical or control edits, numerical reruns, extension choice or P3-02
representation theorem.

## Exact inherited boundary

The current report, `paper_v2.md` §3.1, permits rational literals, source
coordinates, addition, fixed rational scaling, min/max, residuals, finite
nonrecursive bindings and declared conversions. It expressly excludes variable
multiplication and warns against turning a fixed application parameter into a
second unknown multiplier. Its §7.1 likewise keeps query prices fixed and
rational when presenting native instances of expected costs.

`v2/foundations/03_provisional_core.md` §§1–3 gives the same grammar and
explicitly excludes variable division. Its denotation is rational continuous
piecewise-affine (CPWA). Section 2 permits only named fixed positive rational
conversion factors and distinguishes a valuation bridge from a mere unit
change. Section 4 and paper §3.1 admit finite nonempty families of closed
rational polyhedra, with typed affine rows and rational feasible witnesses.
The executable report uses one literal expression pair across cases.

Accordingly, if `p` and `c` are both unknown source coordinates, writing
`c*(1-p)` as an interpreted expectation does **not** make it a native term.
The same issue applies to recovery by dividing a cost by an unknown stake.
These statements concern this selected fragment, not a limitation of classical
arithmetic or every possible future value-logic carrier.

## Continuous rectangle and auxiliary-coordinate check

Assume the source contains a rectangular region of positive width in both
coordinates. A diagonal parameterization `p=p0+alpha*t`, `c=c0+beta*t`, with
nonzero `alpha` and `beta`, restricts `c*(1-p)` to a quadratic with coefficient
`-alpha*beta`. A native term restricted to that segment is finitely
piecewise-affine. The quadratic cannot equal an affine function on any
nontrivial subinterval, so there is no exact native term on this rectangle.
This is a direct closure check, not a selected phase-three extension.

A fresh cost coordinate `z` is a legal native source. The proposed exact
constraint `z=c*(1-p)` is not an affine row. Nor is its graph over the
rectangle a finite union of polyhedra: intersecting it with the same diagonal
plane gives a curved parabola, which cannot be covered by finitely many
straight polyhedral pieces. Adding finitely many auxiliary variables with
linear constraints does not evade this, since their projections remain
finite unions of polyhedra.

Introducing `z` with only affine bounds can therefore give a native **outer
model**, if exact-model inclusion is justified. It does not retain the exact
nonlinear dependency by declaration. Conversely, declaring `z` as a primitive
cost measurement is allowed, but its relation to probability and stake is then
an additional evidence obligation. Do not treat the primitive's name as that
evidence.

The positive-width rectangular condition matters. Fixed parameters, finite
supplied cases, or special restricted sources can remove the obstruction.
A blanket prohibition on every expression involving two uncertain quantities
would be too strong.

## Sound available routes, without selecting one

| Route | What remains inside the inherited fragment | Boundary to retain |
|---|---|---|
| Fix one parameter per query | With fixed rational `p0`, `(1-p0)c` is rational scaling. With fixed rational stake, the expected cost uses rational coefficients and an explicitly declared valuation bridge. | A revised parameter defines a new query/interpretation as appropriate. A fixed irrational parameter is not automatically a native rational literal. |
| Supply finitely many cases | Rational singleton pairs permit exact rational costs. More generally, finitely many fixed rational stake values give affine graph relations within each case while `p` may remain continuous. | A finite sampled grid does not cover the original rectangle. Hidden case identity cannot become free policy information. A common cost coordinate can preserve the executable single-term contract. |
| Certify an enclosure | Rational affine lower/upper component bounds yield a polyhedral outer source and native cost coordinates. | Establish inclusion for the full declared domain, retain error and shared dependence, and charge construction/checking. A countermodel in the larger source may reflect enclosure slack. |
| State an explicit extension | Variable products or richer source constraints can be proposed as a changed carrier. | Identify the changed syntax, source interpretation and checking obligations. Native soundness/completeness and exact rational certificates do not transfer merely by retaining the same names. P3-02 owns the choice and any new result. |

Known nonzero rational division can be expressed by a rational reciprocal
factor where the typing/conversion interface permits it; unknown-denominator
division remains outside. A zero stake gives a native zero-cost literal but
cannot support inverse probability recovery. The direction of a valuation
bridge must not be silently inverted.

## Existing adapter and revision precedents

Core §12 already treats `theta^2` as external to native CPWA syntax. Its
§12.1 constructs a component enclosure, introduces a native source coordinate,
and proves inclusion of the exact model into a polyhedral outer model. It also
warns about potential spurious countermodels. Section 12.2 explains the
polarity of upper/lower substitutions. This is an inherited sound alternative,
not a new adapter architecture proposed by this review.

Core §11 makes `SELF-MIX-v1(r)` affine by fixing rational `r`; §11.4 changes
the behavior and obtains a different comparison sign. It does not license
promoting `r` to an unknown multiplier, or retaining the old cost formula after
a policy/version change. The same identity discipline applies to a stake
revision and to any future observation-dependent pricing interpretation.

No contribution support or gate disposition follows from this interface check.
