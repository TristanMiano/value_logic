# Randomized reliance with an expected fee limit

Codex (GPT-6), DEVELOPMENT, October 22, 2026. Extends the distinct duty left
open in [s13's hard inspection budget](../s13/inspection_budget.md).
This is a proposed general certificate adapter, not independent confirmation.

## Interface

There is a guaranteed blind corrective action of cheapest fee B>0. A
prediction supplies a world, not evidence. A cheapest certificate confirming
that world can be implemented by exact inspections and writes, at total fee
C=Q+W<=B. It remains valid if all its inspected predictions match. After
inspections, recompute a safe completion from receipts; blind correction at
fee B remains available. Thus inspecting the certificate costs at most Q+B
on every world and at most C when the prediction is correct. Source stability,
truthful receipts and correct write semantics are premises. This abstracts
the implication/min-cut implementation without claiming all duties have it.

Fix 0<lambda<=1. Set p=min(1,lambda*B/Q), with p=1 when Q=0. With independent
probability p inspect this certificate and then perform cheapest safe
completion. Otherwise perform the blind correction. Charge the random coin,
planning and computation separately; the following is query/write fee only.

## Expected robustness and consistency

For every fixed actual world, correctness holds on both branches and

    E[fee] <= (1-p)B+p(Q+B) = B+pQ <= (1+lambda)B.

When the prediction is correct,

    E[fee] <= (1-p)B+pC.

Write s=C/B in[0,1], q=Q/B<=s. If q<=lambda, the ratio to C is at most1.
Otherwise p=lambda/q>=lambda/s; since C<=B, the ratio is at most

    g_lambda(s) = (1+lambda)/s-lambda/s^2.

Over s in[lambda,1], its maximum is at s=2lambda/(1+lambda), giving

    E[fee | correct prediction] <= [(1+lambda)^2/(4lambda)] C.

Here conditioning means assessing a fixed world equal to the predicted
world, averaging only the algorithm's independent coin. It is not an
assumption that prediction correctness is independent of inputs. For C=0,
Q=W=0 and the zero-fee certificate is used with certainty. For B=0, use the
zero-fee blind correction. Lambda=0 uses blind correction and has no uniform
finite consistency factor against arbitrarily small positive C.

The oracle computing the certificate may itself be costly. No runtime,
complete-cost ratio or cheap universal certificate optimizer is supplied.

## Matching one-bit obstruction

One unknown Boolean bit must end at1. Writing1 costs B=1; exact inspection
costs q in(0,1); the prediction is1. Until the first inspection, the policy
has no information about the bit. Inspecting with probability p requires
expected cost at least1+pq on world0: either it writes blindly, or it pays
for inspection and still must write. Extra inspections/writes cannot help.
An all-world expected fee bound1+lambda therefore forces p<=lambda/q.
On world1 the expected cost is at least1-p(1-q), while C=q. Choosing
q=2lambda/(1+lambda) forces ratio at least (1+lambda)^2/(4lambda).
At lambda1 this is the trivial lower bound1, approached as q tends to1.

Thus the displayed frontier is sharp for this certificate-interface class,
subject to reconstruction and comparison with prior randomized advice work.
It does not beat the earlier theorem under the SAME contract: the earlier
1/lambda factor protects every realized bill, while this result allows some
bills above(1+lambda)B and controls their expectation for each fixed world.

At lambda1/4 the expected-budget consistency factor is25/16=1.5625;
the prior hard-budget factor is4. This is a theorem-factor comparison under
different risk contracts, not a measured62% fee saving. The one-bit worst
case uses q2/5 and p5/8, with correct-world mean fee5/8 and wrong-world
mean fee5/4. An ordinary randomized implementation is identical and ties.

## Next cheap screens

Check rational parameter/fee panels and the one-bit equality case. Read close
learning-augmented randomized inspection, testing-versus-repair and ski-rental
work before naming a new contribution event. A useful development direction
is an explicit chance limit or repeated-task fee concentration, rather than
another large Boolean enumeration. General adaptive query optimality is not
claimed, and the blind benchmark can be much worse than an adaptive oracle.

## Close prior-work screen

Scheduling with testing already has precisely the primitive of paying for
a test that might reduce a guaranteed fallback cost. Durr et al.'s
[section6](https://arxiv.org/pdf/1709.02592) and Albers/Eckl's
[section4 and Appendix D.7](https://arxiv.org/pdf/2009.13316) give the tight
4/3 randomized makespan ratio against the true offline optimum. The one-bit
primitive here reduces to their zero-or-full processing-time case. Their
algorithm tests with probability (1-q)/(1-q+q^2) after normalizing fallback
to1; it is a mandatory strong comparison, not a weak always-write baseline.

The present parameterized claim imposes a chosen blind-relative expected
budget and compares correct predictions with a confirming certificate.
Those denominators differ from the scheduling theorem. The extension from
one test to a coupled certificate and the explicit risk constraint may be a
useful adapter, but generic randomized testing and its balanced4/3 ratio
are not new. Do not promote the formula alone as a new algorithmic paradigm.

The first [rational screen](reliance_probe.json) passed15,594 abstract fee
panels and six exact one-bit frontier equalities in0.0822514 seconds. This
is same-model development evidence, not a service performance measurement.
