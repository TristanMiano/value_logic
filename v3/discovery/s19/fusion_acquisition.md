# Purchasing fallible models: a submodular case and its boundary

Codex (GPT-6), October 26, 2026. DEVELOPMENT. Broad constructive screen;
the binary robust-fusion theorem is imported, not rediscovered novelty.

## Known channels, unknown dependence

Fix a binary prior pi and a finite decision menu. Its posterior Bayes loss
phi(p) is concave and piecewise affine, so write

    phi(p) = alpha + beta*p - sum_t w_t*(t-p)_+,   w_t >= 0.

For known marginal experiments i, let C_i(t)=E[(t-P_i)_+] and let
C_0(t)=(t-pi)_+ denote the uninformative experiment. Under arbitrary
compatible conditional signal dependence, the imported Blackwell-supremum
result gives the robust value of acquiring a set S. Its improvement over
no information is exactly

    G(S) = sum_t w_t * (max_(i in S union {0}) C_i(t) - C_0(t)).

Each summand is a nonnegative weighted maximum. Therefore G is monotone
and submodular: adding i improves each maximum less when the current set
is larger. Under an equal-price cardinality budget b, ordinary greedy
selection obtains at least 1-(1-1/b)^b of the best improvement achievable
with b channels, hence at least 1-1/e. The standard proof is immediate:
some member of an optimal b-set closes at least one b-th of the remaining
gap, by submodularity; iterate that gap contraction b times. The zero-budget
case is handled separately. Unequal prices need their own known knapsack
algorithm; plain benefit/price greedy is not silently given this guarantee.

This is a useful acquisition interpretation of existing information-order
and submodular machinery. It is not a standalone novel theorem. The actual
robust joint policy still needs construction. Prior, channels, reporting,
calibration and selection computation all need warrants and payment. A
single binary decision kink makes G a maximum over individual values, so
additional channels cannot improve robust benefit in that special case.

## Uncertainty about marginal channels destroys that shortcut

Use the left and right channels from [model_fusion.md](model_fusion.md),
prior1/2 and abstention loss1/4. Baseline loss is1/4; either known channel
alone has loss11/50 and gain3/100. Both together have worst loss19/100 and
gain6/100, under unknown conditional dependence.

There are three purchasable services A,B,C. B is the left channel, C the
right channel. A is either left or right; its type is unknown before
purchase but a certified type tag is returned with its signal. Nature
chooses A's type before the observations. All compatible signal couplings
within each type remain allowed. The tag lets a policy use the appropriate
robust rule after purchase, so the value is the minimum of the two known-
type values. Without A the channels are unchanged. Thus

    G({A})=G({A,B})=G({A,C})=3/100,
    G({B,C})=G({A,B,C})=6/100.

Adding B to {A} gains zero; adding it to {A,C} gains3/100. Diminishing
returns fails. The certified tag matters: without it, taking a minimum
of known-model optimum values can overstate the value of one policy that
must serve every unknown model. This is a finite, exact counterexample
to extending the greedy guarantee to uncertain marginal calibrations.

Disposition: PARK generic novelty. Keep the contract distinction as a cheap
design screen. Do not start a tuned acquisition experiment from this small
constructed benefit or describe it as learning actual mathematical truth.

Primary comparison: de Oliveira--Ishii--Lin2026 Theorem2 already states a
sum of best-source values over binary decision components; the weighted-
maximum acquisition formula is an immediate corollary. Krause, McMahan,
Guestrin and Gupta2007 section2 explicitly treats max-min submodular
observation selection and the failure of submodularity/greedy guarantees
under adversarial objectives. Our tagged example instantiates that known
boundary. These findings support the PARK disposition.
