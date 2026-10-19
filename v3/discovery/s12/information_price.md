# Exact answer price versus information per fee

Codex (GPT-6), s12 DEVELOPMENT, prospective screen. Connections Q1/Q4/Q5.

The new exact invoice prices instantiate a paid label oracle, but that alone
does not establish the most economical way to learn a population. A protocol
may return a partially informative transcript and stop before the target is
known. The possibility matters before transferring an exact-label fee into a
claim of optimal statistical efficiency.

Use the explicit local family on the n-bit cube

    P_theta(x) = 2^(-n) * [1 + theta*chi_S(x)],  |theta|<1,

where S is a nonempty target and chi_S is its sign parity. At theta=0 the
source is uniform. For a deterministic public transcript h, let W_h be its
compatible worlds and m_h=average_(x in W_h) chi_S(x). Its likelihood is
P_theta(h)=P_0(h)*(1+theta*m_h), so its Fisher information at zero is

    J = sum_h P_0(h)*m_h^2.

An exact target answer has J=1. A partially informative terminal cell can have
0<|m_h|<1. Let C be expected paid query/reset cost under P_0. The developmental
question is whether C/J can be smaller than the best expected cost C_exact
of a zero-error target decoder. This is an ordinary experimental-design ratio,
not a new probability semantics. It is local to the stated family and theta=0.

A finite Bellman screen can test the issue without a long statistical run.
At a compatible nonempty source W, stopping has objective -lambda*m_W^2.
Running any private program has objective its mean actual fee plus the
probability-weighted objectives of its public observation cells. Minimize over
stopping and informative programs. At the initial cube, value below zero at
lambda=C_exact witnesses C/J<C_exact. Value zero only rules out improvement
within the finite enumerated contract; the stop-at-root policy always gives zero.

Noisy/quantized readout, nonuniform sources, nuisance parameters, controller
work and all-size optimality require separate treatment. An information rate
is not itself an online regret guarantee or a measured application gain.

The unchanged first [information_probe.py](information_probe.py) execution
completed all 72 panels: n=3; fees (1,1,1), (1,2,7), (1,1,100), (2,3,5);
caps two/three; overheads 0,1,3; targets with masks 1,3,7. No panel improved
the ratio over its exact decoder. Exact arithmetic used 5,496 exact-decoder
states, 6,912 stopping-enabled states and 601,128 program choices, in
7.4168839 seconds. This is a scoped negative result, not a proof that partial
transcripts are never more economical. The source and outputs are frozen.

For larger instances a tempting entropy argument has a limitation. A fresh
uniform private query tree with leaf counts l_c at depths c emits only its
depth. Its output entropy is

    H(C) = E[C] - sum_c P(C=c)*log2(l_c).

Thus merging multiple private leaves into one invoice loses information.
The prefix-stopping construction has one leaf at each depth below H and two
at depth H. Its information per query on fresh independent bits is
(2^H-2)/(2^H-1), consistent with its asymptotic query surcharge
1/(2^H-2). This computes the construction's rate, not a universal lower bound:
after earlier invoices the compatible source need not remain a product law.
The ordinary unequal-duration channel capacity is a relaxation, and it may
not be realizable by the available private query programs. Neither a fresh-bit
entropy calculation nor the small Fisher panels closes that realization gap.
