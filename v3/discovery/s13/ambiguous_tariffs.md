# Overlapping tariff intervals can change the optimal acquisition rate

Codex (GPT-6), DEVELOPMENT, October21,2026. A new restricted minimax
consequence, using ordinary robust coding and the cap-two reduction. It is
not a claim about a calibrated fixed price or a stochastic physical timer.

## Explicit adversarial readout contract

Use n independent fair bits, n>=H, a private cap H with distinct queries,
and exact parity required on every world. A k-query nonempty episode is
reported and charged a bill in[k*a,k*b], 0<a<=b. The bill may depend on the
private query count, world and history; the controller has no further tariff
information. A fixed reset fee f>=0 is added separately and is known.
This interval-bill contract is stronger than an unknown but stable common
query price. It can be realized by an episode-specific rate bill/k in[a,b],
but does not require that rate to be fixed before private random choices.
The public observer sees neither individual rates nor partial bills.

The minimax objective is the supremum expected charged fee over admissible
bill rules, followed by minimization over uniformly correct protocols. Random
coins are independent and otherwise free. Ambiguous bills must be handled
on all paths; inferring the count from its expected price is not allowed.

## Exact cap-three phase on 3/2 <= b/a < 2

For H3 and3/2<=b/a<2, the exact minimax parity fee is

    n*(3*b/2 + f).

Upper bound: use only counts1 and2 to transmit one coordinate per episode.
Their intervals are disjoint because b<2a. Stop after the first query on one
answer and buy a distinct marker on the other. Every bit is fair conditional
on the previous exact bit receipts, so the worst expected bill is at most
3b/2+f per bit. The constant-b tariff attains that bill for this construction.

Lower bound: the adversary may report b at count1 and2b at counts2 or3.
The latter is a valid count3 bill precisely because3a<=2b; all other interval
constraints hold too. Under this fixed count-to-bill rule, the only observable
event is whether the program stops after its first query. That choice depends
only on the first queried bit. If both answer branches continue, the invoice
is constant and conveys no information. Thus every informative episode
reveals at most that one coordinate, with expected fee at least3b/2+f when
it is still unknown. Exact full parity requires every coordinate. Fixing
independent random tapes does not help; wasted/no-op episodes only add fees.
This proves the lower bound for every allowed protocol, including ones that
attempt to use their second private answer adaptively.

For b/a<3/2, all three count intervals are disjoint. uncertain_prices.md then
gives the asymptotically optimal coefficient b*beta(3,f/b). At f0 this is7b/6,
whereas the ambiguous phase above has coefficient3b/2: a factor9/7 increase
at the boundary when normalized by b. This is a sharp theoretical change in
the declared interface, not an empirical timing slowdown. With large reset
fees the same comparison uses beta(3,f/b), not the zero-reset formula.

## Broader feasibility and constructive bounds

If b/a>=H, the bill intervals for all counts1,...,H share the point H*a.
An adversary can report that same bill on every nonempty episode. No
nonconstant target can then be learned, regardless of the number of resets.
Zero-query episodes are chosen without new information and cannot repair
this. Conversely, if b/a<H, count1 and countH intervals are disjoint, so
one-bit encoding with padding proves finite-price feasibility. Hence H>b/a
is the exact feasibility threshold in this interval-bill model.

For better constructions, a block of d fresh bits can be privately XORed
and encoded by counts d and ell=floor((b/a)*d)+1, provided ell<=H. These
intervals are disjoint. The mean worst bill for a fair block parity is at
most b*(d+ell)/2+f. Padding uses distinct coordinates outside the block;
their answers are discarded. This is an upper bound, not general optimality.
Sparse padded prefix alphabets provide other ordinary robust-code options;
their comparison should precede any large adaptive controller search.

The rate and feasibility claims fail if silently transferred to a stable
unknown tariff, because unconditional reference purchases can identify that
tariff. A nonanticipating online tariff adversary is also a different contract.
The positive contribution candidate is the exact robustness boundary and
its connection to paid information, with these stronger adversarial premises
visible. No new physical calibration guarantee is supplied.

The shared robust_probe.py first execution passed147 cap-three branch maps
under the collapse rule and three exact tariff panels, including the3/2
boundary. Its combined runtime with the separate spectral checks was
0.0502377seconds. The all-protocol minimax claim rests on the reduction
above; enumerating these maps does not constitute independent confirmation.
