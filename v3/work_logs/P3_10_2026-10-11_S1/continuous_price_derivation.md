# P3-10 supplemental interpretation: exact fixed-record price intervals

Contributor: **ChatGPT (GPT-6 Astra Pro), principal /root**, 2026-10-11.
Classification: **D/X; an exploratory extension of recorded-path interpretation**.
This analysis was specified before the principal read the final private scores.
The frozen grid remains the primary price comparison. No acquisition policy,
budget, random bit string, execution, stake assignment, or invoice is changed.

## The question the extension can answer

A finite price grid can miss a narrow interval in which one recorded complete
configuration beats the other recorded configurations. Conversely, the absence
of a practical advantage over the entire nonnegative price axis can sometimes
be proved exactly from the saved paths. Both statements concern those paths
and the fixed finite catalogue. Neither concerns a controller rerun under a
different price, or all possible ordinary methods.

Use one frozen cell: the same task family, public populations, and stakes.
Let a_i be its mean normalized terminal action loss for configuration i.
Let b_i be its mean cold units per scheduled request. Both means first give
equal weight to the scheduled seed slots within each population, then equal
weight to the populations. The deterministic control's single record has its
one exact population value; it receives no invented independent replicas.

For normalized unit price lambda, the recorded objective is

\[
J_i(\lambda)=a_i+\lambda b_i,\qquad \lambda\geq0.
\]

All parent episodes must be complete and valid, and all incurred cold costs
must be known, before a line is eligible for a complete-service comparison.
Retain the declared catalogue denominator. A missing ordinary outcome cannot
be removed to create a candidate win. Broker optional reporting costs are
separate, as in the frozen objective, and certificate tariffs are not pooled.

## Exact practical-advantage region

For candidate c and the complete distinct ordinary catalogue O, define

\[
\Delta_c(\lambda)=\min_{i\in O}J_i(\lambda)-J_c(\lambda).
\]

The primary practical threshold is epsilon=1/100 in normalized loss units.
The following equivalence is immediate from a minimum over a finite set:

\[
\Delta_c(\lambda)\geq\epsilon
\quad\Longleftrightarrow\quad
(a_i-a_c)+\lambda(b_i-b_c)\geq\epsilon
\quad\text{for every }i\in O.
\]

Each inequality is either a lower half-line, an upper half-line, the entire
axis, or the empty set. With d_a=a_i-a_c and d_b=b_i-b_c:

| Condition | Required prices |
| --- | --- |
| d_b > 0 | lambda >= (epsilon-d_a)/d_b |
| d_b < 0 | lambda <= (epsilon-d_a)/d_b |
| d_b = 0 and d_a >= epsilon | No additional restriction |
| d_b = 0 and d_a < epsilon | No feasible price |

Intersect these sets with [0,infinity). The result is an exact rational
interval, possibly a singleton, unbounded, or empty. There cannot be two
disconnected practical-advantage windows for one fixed candidate against the
same catalogue. This also follows because Delta_c is a pointwise minimum of
affine functions, hence concave, and its superlevel set is convex.

For **strict** advantage, replace the threshold with zero and every comparison
with a strict inequality. Preserve open endpoints induced by strict bounds,
including a bound at zero. A singleton price satisfying only equality is not
a strict win. For weak nonnegative advantage, use non-strict zero inequalities
and retain all ties. Report all three regions separately.

Exact fractions avoid both grid omissions and floating point errors at a
boundary. Record the binding ordinary constraints, not merely a rounded
decimal interval. They identify which comparator rules out each side of a
putative advantage window.

## The ordinary-identity obstruction holds at every price

The frozen representation catalogue gives each candidate kernel an ordinary
interpretation with the same finite computation, public path, and invoice.
For that alias, d_a=d_b=0. Its inequality for any positive epsilon is false at
every lambda; its strict zero inequality is likewise false. Thus positive
advantage over a catalogue that includes that ordinary identity is impossible
for these recorded objectives, independently of the observed numbers.

This fact does not erase improvements over a distinct implementation. It does
rule out interpreting such improvements as a numerical benefit of changing
the same kernel's name or interpretation. Separately executed mirror paths
provide an identity diagnostic; treating an alias as another independent run
would inflate the experimental denominator.

## Optional whole-catalogue lower envelope

To display the best recorded configurations over price, compute every
nonnegative pairwise line intersection and include zero. Between consecutive
intersections no pair reverses order. Evaluate one exact interior point to
identify all minimizing lines on that open interval, and evaluate every
boundary separately to preserve ties. After the final intersection, one
interior point identifies the entire remaining open ray.

Adjacent open intervals with the same minimizers can be combined only when
the boundary has no additional minimizing line. An isolated tied configuration
must remain visible. This finite calculation is an evaluator's description of
the saved catalogue; it is not a free deployed oracle that switches among
policies after observing performance.

For a finite-grid cross-check, evaluate the affine records at every frozen
price and verify each frozen whole-configuration objective and every tie set.
Keep exact lower/upper fractions in machine-readable output and use rounded
decimals only for prose. Failed or missing complete-service records make the
corresponding extended claim unavailable.

## Deployment and evidence limits

The frozen `native_price_catalogue` admits a price-sensitive ordinary combined
controller only at the price it actually received. That rule is unchanged.
The continuous extension applies only to `fixed_record_repricing`: it asks
what the already observed path costs under another exchange rate. A controller
that saw that other price might choose different purchases, retained state,
and actions. Those counterfactual paths are not identified here.

The populations and pseudo-random seed slots are fixed. Exact arithmetic and
an exhaustive price axis provide no sampling confidence interval, guarantee
on another distribution, or validation of independent fair random bits.
The practical threshold remains an effect-size convention, not a statistical
test or universal preference threshold.

This is P3-10 interpretation, with its own source, command, output and hashes.
It does not reopen the freeze, select a follow-up experiment, or start P3-11.

## Source and review binding

The definitions follow the unchanged `p309_analyze.py` hierarchical means,
complete-service checks, and `fixed_record_repricing` objectives, together
with `protocol.v1.json`'s practical threshold. The independent same-model
broker reviewer was asked to check the half-line argument before final-data
release. Its signed note is retained in `reviews/broker_reconstruction/`.
