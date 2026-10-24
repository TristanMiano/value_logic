# A finite catalogue can be audited before individual proofs finish

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass39.
Sequential finite-population likelihood ratios are conventional. The proposed
adapter is a sound aggregate-proof interface for fixed mathematical truths.

## Fixed truths, random sampling

There are N fixed Boolean losses Y_j, possibly strongly dependent as logical
statements. Let S=sum_j Y_j. Test the fixed-catalogue null S>=S0, where
0<S0<=N. Before sampling choose an integer alternative 0<=S1<S0. Sample
indices uniformly without replacement, using fresh randomness independent
of the catalogue and previous proof work. Let s_t be the actual number of
losses among the first t sampled indices. Define the latent process

    E_t(s)= (S1)_s (N-S1)_(t-s) /
            [(S0)_s (N-S0)_(t-s)],                    (1)

where (a)_b is a falling factorial. Stop at zero if s>S1. A prefix with
more than N-S0 successes is impossible under every null catalogue and can
reject deterministically. Handle this case explicitly, rather than dividing
by zero. E_0=1.

Under a null catalogue and a possible prefix with s<=S1, the next failure
probability is p=(S-s)/(N-t)>=p0=(S0-s)/(N-t). The alternative probability
is p1=(S1-s)/(N-t)<p0. The next factors are p1/p0 on failure and
(1-p1)/(1-p0) on success. They are decreasing in the next loss, so their
conditional mean under p>=p0 is at most one. At p0=1, a success is null-
impossible; the only possible factor is p1<=1. Thus (1) is a nonnegative
supermartingale under every fixed null catalogue. No iid truth premise is
used. The filtration may contain past sound proofs, provided the next index
is still sampled uniformly from the remaining indices.

## Compile a count bound, without completing every sampled loss

Suppose arbitrary later computation supplies a sound proof that s_t<=r_t.
It need not resolve any individual Y_j. Over null-possible counts, E_t(s)
is nonincreasing, since

    E_t(s+1)/E_t(s)
      =[(S1-s)/(S0-s)] *
       [(N-S0-t+s+1)/(N-S1-t+s+1)] <=1.

Set L_t=E_t(r_t), or zero when r_t>S1; tighten r_t to t if necessary.
If r_t<t-(N-S0), the certificate itself rules out the null. Otherwise
L_t<=E_t(s_t) under the null. All later proof refinements, historical-prefix
choices and stopping times are covered by the same latent crossing event:

    P_null(any certified L_t>=1/delta) <= delta.

The visible lower process need not be a supermartingale. Proof delays and
completion order do not need independent censoring assumptions. A randomized
proof checker needs its own soundness event, added to the statistical error.
An unverified fallible prediction is not a sound count bound.

The latent factors depend on unresolved prior losses. The bounded reasoner
can freeze the FUNCTION (1) before sampling and evaluate a certified lower
bound only later. This does not fit new bets to later outcomes. Choosing S1
after inspecting r_t is invalid unless covered by a prospectively weighted
mixture or another justified selection correction.

## Constructed capability example

N=1000, S0=200, prospectively S1=100, t=100. A sound aggregate proof of at
most10 sampled losses gives the exact rational quantity

    L = choose(100,10)*choose(900,90) /
        [choose(200,10)*choose(800,90)]
      = 56.346176573130215... >20.

It supports a level.05 test of catalogue loss rate>=.2. The sampled count
bound alone does not deterministically bound the total below200: as many as
910 losses remain logically possible. If the interface can only say that
each sampled loss is unresolved, its count bound100 gives no crossing.
An ordinary finite-population sequential test given the aggregate proof ties.
No fee or runtime improvement is inferred; deriving and checking the count
certificate, random sampling, big-integer arithmetic and recording all cost.

A simpler constant bet lambda=.5 uses the remaining-null mean
(S0-s)/(N-t). For a fixed count at most10 and t=100, the worst order places
all ten failures first; an adjacent01/10 swap verifies this. The resulting
lower wealth is32.598425900177915...>20. The likelihood-ratio interface
avoids ordering optimization and is stronger in this constructed case.

## Boundaries that prevent a cheap false gain

Sampling only obligations whose proofs finish quickly is not the uniform
sampling design. The initial sampled indices must stay in the catalogue
receipt even if their proofs never finish. Proof work may be adaptive, but
unfinished outcomes keep their conservative contribution. Changing the
catalogue or the loss definition after sampling requires a new contract.
This estimates a rate over a declared finite family; it does not assign a
learned probability to the truth of one arbitrary unresolved theorem.

Joint proofs may be hard to obtain, and the latent formula is not evidence
that they occur cheaply. The next useful screen is a natural source of
compressed count certificates with a complete acquisition/checking bill.
Do not claim a new sampling theorem from this adapter.
