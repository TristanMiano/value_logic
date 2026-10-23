# Relation discovery can continue through unresolved probes

Codex (GPT-6), October23,2026. DEVELOPMENT; generation pass20.
Uses the polynomial contract of polynomial_scope.md and ordinary betting.

## Frozen membership questions, growing known span

Let F have n polynomial outputs, total degree<=D, independent grid
coordinates of size q>D, and unknown image-span V of dimension r.
Write zeta=D/q in(0,1). Maintain S as a span of soundly acquired actual
F values. Before probe i, freeze the current S_i and draw a fresh X_i.
Let B_i=1{F(X_i) in S_i}. If S_i is incomplete, the degree argument gives

    P[B_i=1 | complete past] <= zeta.

Fix theta in(zeta,1). Set a=theta/zeta>1 and
b=(1-theta)/(1-zeta)<1. While S is incomplete, multiplying by a for B_i=1
and by b for B_i=0 has conditional expectation<=1. Stop this latent wealth
process at the first time the maintained span becomes complete. That time
is a stopping time in the full-information mathematical filtration even
though the bounded reasoner cannot recognize it.

At any computation step, a sound receipt L_i<=B_i is initially0 and can
become1 only after membership in the FROZEN S_i is proved. The lower wealth
is product a^L_i b^(1-L_i). Announce current-span completeness only when
this lower wealth reaches1/delta. If the current span is still incomplete,
it has never been complete earlier, because S only grows. The displayed
wealth is then bounded by the unstopped portion of the latent process.
Ville therefore bounds the probability of ANY false completeness announcement
by delta, despite out-of-order proofs, adaptive scheduling and new draws.

Membership in a later enlarged span cannot be substituted for membership
in S_i. The later statement may be true merely because the probe itself
was added; that would turn every known probe into free positive evidence.
If the full F(X_i) is acquired, it can enlarge current S even while the
corresponding frozen membership question is unresolved. Versioned receipts
and a source fixed before the fresh draws remain necessary.

The stopping-time proof can be formalized on computational steps: keep
wealth constant on proof-only steps, and use the current frozen span at
each draw. After S first equals V, freeze the latent supermartingale.
The sound-receipt lower bound is only needed on a false-announcement path,
where this freeze has not happened. It is not asserted globally after
completion. This distinction avoids an unjustified domination claim.

## A sharper complete-evaluation query cap

When each probe is fully evaluated before the next draw, every B_i=0 raises
the rank by one. After j such probes and R redundancies, wealth is a^R*b^j.
Define

    H(j)=ceil((log(1/delta)+j*log(1/b))/log(a)).

Allow the numerical equality convention explicitly. The stopping rule has
a deterministic probe cap r+H(r), with false-completeness probability<=delta.
The actual rank need not be supplied to run it. Before completion j<=r;
at j=r, all future probes are redundant, so no path can exceed that cap.

For D=4,q=257,delta=.001,theta=.5 and actual r=4, H(r)=3 and the cap is7
complete paired evaluations. The earlier consecutive-three rule has cap15
and expected-count upper7.064 for that rank. This is a smaller WORST-CASE
query bound (15 to7), not a measured mean or runtime improvement. Both
rules use the same polynomial degree and exact evaluation premises; the
new rule has a direct delta guarantee independent of the ambient output
count. It is still an ordinary statistical algorithm under this contract.

## A small mixture and asynchronous limits

A predeclared mixture sum_k w_k a_k^R*b_k^j is also valid, provided each
theta_k>zeta and weights sum to1. It adapts to unknown rank without choosing
the betting parameter from the observed redundancy count for free. Its
complete-evaluation cap is r+min{R:sum_k w_k a_k^R*b_k^r>=1/delta}.

With unresolved probes, a negative frozen-membership result need not raise
the current rank: another probe may already have supplied that direction.
The r+H(r) cap does NOT extend unchanged to asynchronous execution. Unknown
questions keep their b factors and may prevent certification indefinitely.
The new capability is valid continued acquisition and refinement rather
than mandatory suspension of a single unresolved batch. It is not a bound
on proof completion or a license to discard expensive evaluations.

Primary comparisons should include sequential randomized identity testing,
adaptive randomized rank estimation and delayed test-martingale interfaces.
The ingredients are established. The candidate useful delta is the explicit
combination of frozen membership, growing span, unresolved proof refinement
and a rank-adaptive finite query cap under the complete special case.

The [exact finite probe](range_anytime_probe.json) checks16 uniform linear
image laws, the F3 polynomial counterexample's actual law, and rational cap
arithmetic. The half/tenth mixture has caps7,21,139 at ranks4,16,128,
respectively; the earlier consecutive-three caps are15,51,387. These are
same-contract worst-case paired-evaluation counts, not empirical average
speedups. The probe also exposes a decisive stale-span counterexample:
in dimension8 over F2, adding each vector and then calling it redundant
produces a nominal .1-level certificate after six vectors, necessarily
before the span is complete. Its false-certificate probability is1.

The recorded monotonic elapsed time for this short probe is0ns on the
host's clock. Preserve that reading; do not infer a positive duration or
attribute it to hardware damage. The enclosing observed E interval carries
the implementation and finite-analysis research time.
