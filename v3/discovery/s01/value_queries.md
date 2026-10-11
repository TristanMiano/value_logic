# Paying for value contrasts under correlated error

Codex (GPT-6), October 11, 2026. DEVELOPMENT; S05, connected to S01/S03/S04.

## 1. The missing constructive part after P3-02

P3-02 already characterizes exact/noisy value fibers, shared calibration and
decision-only recovery. Repeating those results would not supply P3-POS01.
The question here is an acquisition rule: which partial value computations
should be bought, at what precision, when errors share a source and prices
are charged? Existing optimal recovery, active experimental design and
adaptive numerical precision are the comparison families.

Let a declared uniform finite population of deterministic mathematical
queries induce a true frequency p. This gives one possible operational
meaning to p without random mathematical truth. Computing p exactly can
require many evaluations. A supplied approximate-value service must justify
its error bound from its algorithm or checked evidence. We do not grant
approximate means or calibrated forecasts as free inputs.

Actions A and B have canonical expected losses 1-p and p. Suppose two priced
reports at a common refinement stage satisfy

    z1 = a*p + b + e1
    z2 = a*(1-p) + b + e2,
    0 < a_min <= a,   |e1|,|e2| <= delta.

The reports share the *same* unknown a,b. This common-source contract is
essential. Separate errors of magnitude delta can be adversarial; no
independence or distributional coverage is assumed. If actual reports do not
share the offset, the following cancellation does not apply.

## 2. Decision bounds that ignore irrelevant calibration

Write d=z1-z2 and g=2p-1. Then d=a*g+e1-e2. If d>2delta, g>0 and A is
optimal; if d<-2delta, B is optimal. At equality, the sign is weakly known
and the corresponding action still has zero regret. With zero residual
error, the sign of d identifies the optimal action despite unknown scale
and offset. It does not identify p: for d=1/2, both (p,a)=(3/4,1) and
(5/8,2) are compatible with suitable b for the same two reports. This is a
concrete reuse of P3-02's calibration distinction, not a new identification
theorem.

For d>=0 choose A. If it is wrong, g<0 and

    regret(A) = -g <= (2delta-d)/a_min.

Therefore the uniform regret bound is

    min(1, max(0, (2delta-|d|)/a_min))

when choosing the action indicated by d (either tie choice at d=0). The
bound is sharp over an unconstrained common offset and permitted scale/error
family, up to clipping by p in [0,1]. For example set a=a_min and put the
error contrast at the adverse endpoint; choose p to attain the resulting
gap whenever it lies in [-1,1]. This supplies a stopping test for a specified
regret tolerance without recovering nuisance calibration.

At d=0 the pure-action bound is 2delta/a_min, while the 50/50 action lottery
has at most half that regret. More generally if checked information gives
g in [-u,v] with u,v>0, selecting A with probability v/(u+v) gives worst
expected regret uv/(u+v); equating the two adverse endpoint risks proves
optimality. This is a two-action instance of the region LP, with an expected
regret interpretation and fixed action consequences.

## 3. Joint purchases and sequential refinement

A single report may carry no action information if b is unrestricted: any
p can be matched by adjusting b. The pair can decide immediately. Thus
singleton information value can be zero while the bundle has value, even
without XOR and even when the desired object is a linear value contrast.
Treating the two marginal errors as independent unknown offsets would erase
this benefit; correct source identity is operational information.

At levels j=0,1,... let delta_j=delta_0*2^(-j). Buy a paired refinement only
when the current regret bound exceeds the requested epsilon and the remaining
cost contract permits it. Reuse already obtained work only if the service
supplies a resumable state and charges the actual incremental cost. Do not
subtract past work merely because two levels share a formula.

For a fixed nonzero true gap |g|, every valid pair has
|d_j| >= a_min*|g|-2delta_j. Therefore delta_j<a_min*|g|/4 ensures
|d_j|>2delta_j and forces a correct sign certificate. At exact equality
g=0, pure sign certification need not terminate under arbitrary residual
errors, although epsilon>0 terminates once 2delta_j/a_min<=epsilon.
For a known finite denominator N, a nonzero gap has an explicit lower
separation (at least 1/N is conservative). An equality fallback or positive
regret tolerance remains necessary; one cannot silently assume a margin.

If a fresh level j has total cost c_j and c_j grows by at least a factor
gamma>1, the sum through the first adequate level J is at most
gamma/(gamma-1)*c_J. This elementary geometric bound compares to that same
level's cost, not to an omniscient optimal algorithm or an arbitrary exact
solver. Faster-than-geometric jumps can overpay relative to an untested
intermediate precision, and arbitrary c_j need their own scheduling rule.

## 4. Constructive obstacles and fair comparisons

- A direct contrast evaluator may eliminate b symbolically and be cheaper
  than buying two reports. Give that ordinary method the same expression graph
  and access; a hidden black-box restriction must have an actual application.
- Shared numerical approximations do not automatically imply shared error.
  The matching coefficient and source identity must be checked under revision.
- Scale a_min has a role in quantitative regret. Positive sign information
  alone cannot price a small decision error in canonical units.
- A tighter bound can fail to justify its computation price. Certifying an
  action and maximizing a paid expected objective are distinct services.
- A learned estimate of future precision gain can guide the schedule, but
  only the checked current bound warrants stopping. Compare ordinary adaptive
  arithmetic filters and algorithms with predictions, not full exact recovery
  alone.

The next promising synthesis is to allow proposal policies to choose *pairs
of bound refinements* and let the region/certificate checker decide when to
stop. Completion-cost feedback then teaches which proposals are useful.
No oracle for all uncomputed values, calibration or future runtime is allowed.
This is a developmental integration target, not evidence of material benefit.
