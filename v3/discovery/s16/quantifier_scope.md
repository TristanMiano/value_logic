# Robust action, reoptimized value and retained information are distinct duties

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; substantive synthesis.
Read with the El Ghaoui–Lebret comparison in literature.md.

Consider J_N(x)=(1-N*x)^2+x^2 with source M=3 and |N-M|<=1.
The reoptimized edited value is F_N=min_x J_N(x)=1/(1+N^2). Hence

    max_(2<=N<=4) min_x J_N(x) = 1/5.

A robust action chosen before N is revealed has different cost:

    min_x max_(2<=N<=4) J_N(x) = 2/9.

For x<0 the cost exceeds1. For 0<=x<=1/3 the worse endpoint is N=2,
and (1-2x)^2+x^2 decreases up to x=1/3 on that interval. For x>=1/3
the worse endpoint is N=4, and (1-4x)^2+x^2 increases on that interval.
Both meet at x=1/3 with value2/9. Thus simply substituting a robust-action
objective for a reoptimized-value envelope creates an11.111...% upper
gap even in this scalar example. No minimax equality is assumed.

Now discard source shape and retain only the old target value C=1/10.
Permitting arbitrary compatible extra output dimensions changes the
supremum again, to (3+sqrt(5))/20, approximately .2618034, by the
one-value envelope. The known one-output maximum remains1/5. These
numbers describe different uncertainty sets; the extra dimension has not
made the original scalar problem worse.

This example isolates the exact comparison duty for N16-C/v1. Classical
robust action methods directly precede much of the proof machinery.
Reoptimized values and unknown compatible sources have different
quantifiers, and source shape is genuine information. A promising
moderately scoped contribution would state and verify an optimal retained-
information contract, with its dimensions and arithmetic warrants explicit.
The distinction does not itself establish literature novelty: robust value
sensitivity, optimal recovery and operator-completion results may already
provide that complete statement or a routine equivalent. That comparison
remains necessary; it should not be replaced by a generic algorithm race.
