# C4 same-assistant reconstruction

Contributor/reviewer: **Codex (GPT-6)**, October 4, 2026.
This is a deliberate reconstruction by the authoring assistant, not an
independent reviewer or proof-assistant verification. F16 remains due.

## Load-bearing checks

1. **Linear retention with arbitrary decoding.** On a relatively open affine
   source, two sufficiently small opposite perturbations realize every kernel
   direction. An exact decoder therefore requires the summary kernel to lie
   inside the query kernel. Equal minimal ranks make their row spaces equal.
   Arbitrary real encodings and free source reacquisition are excluded; the
   argument does not assume the decoder itself is linear.
2. **Weighted single-profile kernel.** Adjacent swaps compare c_b*v_(S+a)
   with c_a*v_(S+b), including the (c_a-c_b)*v_S term. Omitting that last term
   would incorrectly replace the weighted kernel by level-constant moments.
   Subtracting already-determined elementary-symmetric terms leaves connected
   subset-layer equations. Positive costs make their products nonzero.
3. **Two-profile intersection.** At every size 1 through k-1, constant ratios
   of all r-fold cost products imply equal individual ratios by exchanging
   one index. The argument stops before the full set, where the exchange is
   unavailable. That is exactly why the full-failure direction survives until
   a numeric positive penalty or differing cross-profile penalties detects it.
4. **Proportional exceptions.** A proportional price family leaves the old
   proper kernel unchanged. Its remaining constraints act on two coordinates,
   S_c(t) and v_all. Numeric rank uses the parameter-row rank, while all
   differences use the affine rank of those rows. Three noncollinear profiles
   can contribute two dimensions to the latter; duplicate profiles add none.
5. **Repair is incremental.** The k-1 measurements are added to an already
   exponential old summary. Each is an actual new mean with an old mean
   available for subtraction. Exact population means are oracle observations
   for this statement, not free empirical measurements. M=0 removes one
   required proper-moment probe but leaves the full moment unidentified.
6. **Known marginals.** Fixing sizes through s forces t_1 through t_s to zero.
   The remaining common mean functional is nonzero until s=k-1. At that edge,
   rank is one or zero according to M>0 or M=0. Full support is essential;
   zero singleton probability imposes additional higher-order equalities.
   Positive-width intervals normally do not lower exact affine dimension.
7. **Approximation and robust objectives.** Pathwise cost differences lie in
   an interval of width |epsilon|. Monotonicity and translation, then old
   optimality, give the regret bound for fixed mean/CVaR and a common-source
   worst-case version. A law-dependent common offset can still change an
   absolute minimax choice; the supplied two-law example is feasible.
8. **A1 sharpness.** Inverting the moment kernel gives the four Hamming-level
   signed masses. Their multiplicities are 1,3,3,1. L1<=2 is both necessary
   and sufficient for a probability-law difference. Weighted-median minima
   give the singleton and piecewise pair diameters; direct world nullspaces
   independently reproduce them at both breakpoints and on either side.
   The attaining laws have all old means equal to two. Their action agreement
   prevents an invalid conversion into a policy-regret lower bound.
9. **A2 is about differences, not exchangeable populations.** Equal old
   profiles imply an exchangeable signed difference. The original laws may
   be asymmetric. The three-support extremizer follows from the two
   normalizations and one common cost mean. It is not a new general moment
   extremality theorem. The global error radius costs O(k^4) arithmetic
   operations; reading an arbitrary old summary still has exponential size.
10. **Conditional recovery.** Within-level contrasts and one average old mean
    have exactly the old rank. Subtracting a level minimum is decoder work,
    not an additional retained nonlinear measurement. Nonnegative residual
    level masses obey two equalities, giving attainable two-level endpoints.
    Direct execution checks the endpoints' entire old profiles, not merely
    their average. Individually sharp intervals need not have jointly feasible
    midpoint moments; the negative mass -3/496 is an explicit witness.
11. **Native admission.** All C4 rank/recovery controls are ordinary exact
    mathematics. Prices are fixed external parameters for each query.
    Unknown prices multiplied by unknown probabilities are bilinear and are
    not silently admitted into the native CPWA language. No new native rule,
    receipt guarantee, empirical calibration or learned network is established.
12. **Closest-method reconstruction.** The reset costs also have a Choquet
    representation; normalizing away unresolved mass would change the model.
    Optimal recovery and capacity identification already provide generic
    numerical machinery. C4's delta is the explicit price-family structure,
    repair, special radii and integration interpretation, with modest scope.
13. **Do not infer a coherence penalty.** Exact midpoint infeasibility does
    not force a larger common maximum error. A feasible law achieves 21/496
    in the very counterexample; 54 exact fiber searches found no penalty.
    Separate coordinate-optimal tolerances and a shared tolerance are different
    contracts. No universal coherent-center result follows from this search.
14. **A3 is conditional empirical repair.** One stopped trace determines all
    canonical reach indicators, including failure of the first k-1 procedures.
    Exact retained contrasts make each other subset's error equal to the
    canonical error of its size. DKW controls that one empirical CDF. The
    tests check this deterministic reduction on asymmetric laws, not a new
    concentration theorem or an empirical coverage study. Exact old population
    constraints, a fixed sample count, unchanged outcomes and iid requests
    are substantial hypotheses; neither runtime nor data acquisition is free.
15. **Native/statistical bridge.** Rational intervals/equalities give an
    admitted source only after nonemptiness, witness and unit access checks.
    Real exact summaries in the abstract rank model need not be rational
    native inputs. The coverage event concerns the true population law and
    means, not next-request realized cost. Adaptive query selection is covered;
    arbitrary sample stopping and conditional-on-acceptance calibration are not.
16. **Edge and budget audit.** k=2,M=0 already identifies all proper moments:
    A2's zero prediction radius agrees with T2's zero added-probe count.
    With all proper moments known, a positive old penalty identifies the full
    moment without new data. Proportional price families are classified by
    the two-column parameter rank, rather than incorrectly treated as a
    nonproportional pair. Multiple new attempt-price edits have the elementary
    L1-size error extension of A3, but changed penalties, arbitrary old prices
    and jointly noisy retention are not silently included. Statistical error
    counts are not CPU-cost, native-proof or real-world calibration claims.

## Contribution and stopping checks

The comparison includes strong ordinary methods with the same information,
source access and acceptance obligations. It does not require every component
to be novel. The supported assessment is bounded to the precise synthesis and
technical applications in the contribution review; worldwide priority remains
unestablished, and one close capacity-identification section was unavailable.
F16 should challenge this, not merely count passing tests or repeat the label.

The optional generalization is complete at its stated equal-price scope.
Unequal-price approximation, repair with jointly noisy old information and a guarantee for
action-only consumers remain distinct future questions. A finite exploration
found singleton-diameter dominance for k=2..12 at five penalty values, but
**no universal theorem of that kind is asserted**. There is no need to resolve
that stronger conjecture to use A2's exact finite maximum.

The review found no unresolved contradiction in T1–T3/A1–A3. Test coverage is
finite supporting evidence; the displayed arguments carry the universal
claims. C4 cannot substitute for F16's later fresh D60 or Gates C/D.
