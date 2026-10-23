# A common comparison experiment for symmetric summary channels

Codex (GPT-6), October23,2026. DEVELOPMENT; pass23 extension.
Same fresh-reset count interface and Q=(weight-n/2)^2 as balanced_summary.md.

Let d=min(H-1,n). Every pure cap-H count channel is a garbling of the
following experiment: sample d distinct input coordinates uniformly and
return T=min(K,d-K), where K is the number of ones in that sample.

To prove this, put the uniform distribution on a Q-cell. Adaptive distinct
coordinate choices expose an exchangeable sample without replacement.
After d queries, the probability of an ordered bit sequence depends only
on its number of ones and is invariant under complement. Conditional on T,
the ordering and the choice of complementary weight are uniform and do not
depend on Q. Generate these from independent coins, run the episode's
decision rule and output its count. A count-H event is fixed after H-1
queries, so the simulation covers every possible public count. Finally,
pointwise purity transfers the uniform-cell law back to every fixed input.

For n=2m, Q=a^2, define C(u,v)=0 outside0<=v<=u. The exact comparison law is

    P_a(T=t) = [C(m+a,t)*C(m-a,d-t)
                 +C(m+a,d-t)*C(m-a,t)] / C(n,d),

except when2t=d, when only the first term is used. This law is the same for
weights m+a and m-a. Taking d=2 recovers pair agreement.

Consequently any cap-H repeated protocol with finite expected episodes and
binary error<=epsilon between Q=0 and Q=1 has

    E_0 T_episodes >= kl(1-epsilon,epsilon)/KL(P_0 || P_1).

This is a necessary bound, not a promise that the whole folded experiment
fits the count cap: it may have more output symbols than remain after d
queries. Directly transmitting its value by padding costs cap d+floor(d/2).
In particular, a full d-bit observation cannot be treated as a free public
message merely because the private query budget allowed those reads.

The comparison experiments become more informative as d grows: sample d
bits, randomly remove one, and fold the remaining count. This gives the
d-1 experiment by a Q-independent random transformation. Hence their KL
divergence is nondecreasing in d. For every d<n, P_0's support is contained
in P_1's; when d=n they are disjoint. The center cannot be identified with
zero error after a finite transcript under cap<=n, consistent with the
nonnegative-literal obstruction.

This extends the comparison across caps without introducing a claim that
signed polynomial degree determines information rate. The complete cost
frontier, including varying counts, padding and reset charges, remains open.
# Probe record

`folded_probe.py` passed 476 exact hypergeometric laws, 434 one-bit deletion checks, 76 direct subset enumerations and four shared-coin inputs. Source SHA-256: `ad40185ded0a5e27cf0c72004c33e94fed5bd6d016e5ed53dbee8667ac949012`. The reported `perf_counter` duration is 10,025,300 ns. These finite checks supplement the argument; they are not independent confirmation or a total computation benchmark.
