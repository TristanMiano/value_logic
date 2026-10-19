# Paying to learn whether one cheap relation is useful

Codex (GPT-6), s12 DEVELOPMENT derivation. Extends the fallible-source portion
of [graph_invoices.md](graph_invoices.md). This is a concrete application of
ordinary selective prediction and binomial testing, not a new calibration
principle. No new deployment experiment or novelty assessment yet.

## Fix the target and the cheap relation before calibration

On each new instance, an exact target route has actual invoice D(X). A fixed
alternative relation predicts that target using cheaper exact queries with
actual invoice A(X). A calibration case buys both and compares their
answers. The relation may be wrong, and other parts of its generating model
may be false even when this relation is right. No whole-model truth assumption
is needed for the following empirical comparison.

For a transparent rule, buy N paired calibration cases. Deploy the cheap
relation on later cases only if all N comparisons agree; otherwise keep the
exact target route. Freeze the relation before those N cases. The learner
cannot treat a relation fitted to its calibration labels as this fixed object.
Charge the exact calibration purchases, cheap predictions, admission check
and later query/controller work. The formulas below concern acquisition
invoices only; all other costs remain additional.

## Three distinct error contracts

Assume calibration and later cases are independent draws from the same fixed
law. Let p be the unknown failure probability of the fixed relation. The
admission probability is (1-p)^N. Each later answer is wrong with unconditional
probability

```math
p(1-p)^N\le g_N:=\frac{N^N}{(N+1)^{N+1}},
```

where the maximum occurs at p=1/(N+1). This marginal guarantee averages over
calibration and the new case. It does not say that the conditional error after
admission is at most g_N: that conditional error is p.

For a different, confidence-style contract, fix desired error alpha and
confidence failure delta. Taking (1-alpha)^N<=delta ensures that a relation
with p>alpha is admitted with probability at most delta. This statement
concerns the reliability of the accepted rule, rather than just one future
answer averaged over calibration.

For M independent future uses, the probability of at least one wrong answer is

```math
(1-p)^N[1-(1-p)^M]
\le \left(\frac{N}{N+M}\right)^{N/M}\frac{M}{N+M}.
```

Set q=1-p and maximize q^N(1-q^M); its interior optimum has
q^M=N/(N+M). Thus a small marginal error does not imply an equally small
probability of any error in a long deployment. No fixed finite calibration
sample makes that familywise guarantee uniform over an unbounded future.

If only exchangeability of the N calibration cases and the next case is
assumed, a simple valid marginal bound is 1/(N+1). The event "first N correct,
last wrong" has at most that probability: conditional on exactly one error
among these N+1 cases, each position is equally likely. Independent draws give
the sharper g_N above. Arbitrary temporal shift supplies neither guarantee.

## Acquisition economics, with calibration cases counted as real tasks

Compare against exact target recovery on the same N calibration tasks and M
later tasks. Both methods already owe D(X) on each calibration task to answer
it. Write mu_A=E[A(X)] and mu_gap=E[D(X)-A(X)]. The extra expected training
invoice is N*mu_A. Independence of calibration and future cases makes the
expected later saving M*mu_gap*(1-p)^N, even if costs and relation errors are
correlated within an instance. Relative expected invoice difference is

```math
N\mu_A-M\mu_{gap}(1-p)^N.
```

This accounting applies when the calibration cases themselves are requested
tasks. For additional training-only cases, charge their full expected A+D instead.
Do not silently switch between those two baselines.

For the constructed graph duty, D(X)=100+x_e and A(X)=3+z_1+z_2+z_3 when
the three cheap path bits are z_j and marker purchases signal bit one.
Hence mu_A<=6 and mu_gap>=94, giving the sufficient difference bound
6N-94M(1-p)^N. At p=0, the marginal 1% iid contract needs N=37 and amortizes
this conservative surcharge after three later tasks. The 1%-error/95%-confidence
contract needs N=299 and amortizes it after twenty later tasks.

For an explicit law, take independent fair z_j and set x_e to their parity
flipped with independent probability p. Then mu_A=9/2, E[D]=201/2 and
mu_gap=96 for every p. The exact expected difference is
(9/2)N-96M(1-p)^N. At p=0 this amortizes after two later tasks for N=37 or
fifteen for N=299. These are constructed finite-law acquisition calculations,
not measured population performance or complete computation-cost savings.
The exact rational screen below checks both minimal N values.

**Corrected draft error:** the first draft substituted worst-route bills
d=101 and a=6 into N*a-M*(d-a)*(1-p)^N and quoted nineteen later tasks for
N=299. Those bills vary with the hidden answers, so subtracting the two maxima
does not give the mean saving or its lower bound. The formulas above retain
actual bills, a valid 94-unit pointwise lower saving, and the specified finite
law's 96-unit mean saving. No experiment used the erroneous draft calculation.

## Useful even when the complete model is always false

In the three-path graph example, set x_e to the parity of the three edges
leaving u. Set at least one of the other path edges to disagree with its
partner, so the full circulation model fails on every instance. The cut
relation at u nevertheless holds exactly. Its shortcut can therefore have
p=0 while the full model's probability of being correct is zero. This is an
explicit task-specific usefulness example, consistent with established local
model adequacy/value-equivalence ideas.

Unlabelled cheap edges alone cannot certify that relation: two populations
can have identical cheap-edge distributions and opposite target assignments.
Some paid target feedback or a separate sound premise is required. The rule
above supplies that feedback rather than presuming reliability from internal
agreement.

## Selection and continuation limits

If K fixed relations share calibration labels and the service may select any
that passes, separate marginal guarantees are insufficient without selection
control. A union bound gives K*g_N in the iid setting or K/(N+1) under the
stated exchangeable one-case setting, with appropriate capped probabilities;
stronger joint tests may improve this. Predictions for all tested relations
must be charged, while shared exact labels are bought only once. Repeatedly
trying until one calibration block passes also changes the guarantee.

The primary comparison is recorded in [literature.md](literature.md). The
confidence-style rule is a binomial special case of Learn then Test; ordinary
simultaneous testing also handles the selection concern. Conformal Risk
Control provides the relevant distinction between marginal and conditional
guarantees, under its own hypotheses. An identical conventional test-and-deploy
service ties this one. The retained synthesis is the explicit coupling of
paid relation feedback, source-independent invoice bounds, and a model that
can be globally false yet useful for the requested task.

## Finite arithmetic screen

[calibration_probe.py](calibration_probe.py), unchanged first execution with
bundled Python 3.12.14, passed: 60 iid scenarios, 16,746 joint assignments and
44 extreme exchangeable error laws. It enumerates the fair three-bit law and
a second law where cheap costs depend on the relation error, and checks the
actual mean-cost formula, one-answer risk and familywise event probability.
Every generated graph violates the full source model. Exact fractions confirm
minimal N=37 and N=299 and the stated 3/20 conservative and 2/15 fair-law
amortization counts. [Output](calibration_probe.json) records 0.0932734 seconds
for this finite screen; that is neither controller cost nor application gain.
This is a same-model DEVELOPMENT check, not independent confirmation.
