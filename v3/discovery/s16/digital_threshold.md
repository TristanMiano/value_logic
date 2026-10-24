# Exact interval decisions with finite expected random-bit work

Codex (GPT-6), October 23, 2026. DEVELOPMENT. Random-bit simulation and
retrospective sampling are conventional; this fills a computational premise
in the proposed receipt adapter. It does not make real-number oracles free.

Let0<=L<=F<=U<=1, with exact rational L,U. Reveal fair bits of a uniform
V lazily. After k bits, V lies in a dyadic cell I_k of length2^(-k).
If I_k lies entirely below L, return1. If entirely above U, return0.
If entirely inside(L,U), request/refine the expensive value F and continue
the same-bit comparison until V<F or V>F is certified. Otherwise reveal
another bit. Null endpoint events can be ignored mathematically, while a
finite implementation needs exact interval comparisons rather than rounded
point tests.

The expensive oracle is called exactly on V in(L,U), almost surely,
so its probability is U-L. Before this decision, an undecided dyadic cell
must contain L or U. Thus for the number K of bits needed to settle the
call/no-call decision,

    P(K>k)<=min(1,2*2^(-k)),  E[K]<=3.                 (1)

This is uniform even when U-L is tiny. Conditional on the rare call event,
more bits may be needed; unconditional expectation is the stated duty.
If the oracle returns F as an exact rational, the entire procedure's
stopping cell can only remain undecided at one of L,F,U. Therefore its
total random-bit count T satisfies

    P(T>k)<=min(1,3*2^(-k)), E[T]<=7/2.                (2)

This bounds random bits, not arithmetic or oracle effort. Integer comparison
uses the endpoint encoding lengths as well as k; those lengths must be paid.
The geometric tail also bounds every fixed polynomial moment of k. If F
is supplied only by converging certified intervals, almost-sure comparison
can still follow, but expected refinement cost needs the rate/price premise
from threshold_proofs.md. No finite expected oracle price follows from(2).

An alternative cap of k initial bits can call the full oracle whenever the
dyadic cell still intersects[L,U]. Its call probability is at most
min(1,U-L+2^(1-k)). This is a conservative cost option, not a discretization
of the final decision: continue exact comparison after that call. It trades
extra oracle calls for a fixed initial-bit budget and never replaces the
unknown loss by the midpoint of its receipt.

These details make the analytic call comparison implementable in an exact
rational interface. They do not establish a whole sampling application's
speedup, and an ordinary lazy-bit interval sampler obtains identical counts.
