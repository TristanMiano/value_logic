# Local policy changes can expose much cheaper counterfactual feedback

Codex (GPT-6), DEVELOPMENT. S06/S23 continuation, Q1/Q2/Q3/Q4. A candidate
information-acquisition consequence rather than another complete-cost optimizer.

## Adjacent exchange identity

Consider a fixed order of deterministic score computations, with fixed
nonnegative identity-specific fees. A monotone, order-independent predicate
of the acquired set decides when a sound certificate has been obtained. A
nonnegative sum threshold is one example; a two-sided Boolean threshold
certificate is another. Both compared policies have the same suffix and
fallback. Swap only adjacent computations a,b. Let R be their common prefix.
If R already stops, their bill difference is zero. Otherwise write A and B
for the indicators that R plus a alone, or R plus b alone, would stop. Then

```math
C_{ab}(x)-C_{ba}(x)=c_a B-c_b A.
```

The two local bills are c_a+c_b(1-A) and c_b+c_a(1-B). If either stops early,
monotonicity ensures the shared two-element set stops; if neither does, the
same state and suffix follow. Hence all later costs cancel pathwise. No
independence or probability model is involved. Changing query outcomes,
stateful evaluators, order-dependent overhead, or different fallback semantics
would invalidate this simple identity unless explicitly incorporated.

## One extra receipt reveals the entire adjacent neighborhood

Run the base order until its stopping index L. For swaps strictly before the
last observed coordinate, both values are already known. For swaps after L,
the common prefix has already stopped and the difference is zero. Only the
swap of the last observed coordinate with the next one can lack a receipt.
Buying that next score, when it exists, therefore determines exact costs for
ALL n-1 adjacent-swap policies, with at most one extra computation. Prefix
states and the identity above suffice; full alternative executions are not
needed. The extra receipt is charged even though it is unnecessary for the
already sound output.

One extra receipt can be necessary: n=2, Q=1, fees (1,2), first score 1.
The base trace is identical whether the second score is 0 or 1, but the
adjacent-swap difference is respectively -2 or -1. A method restricted to
that trace cannot always give exact counterfactual feedback.

This extends s02's exact post-certificate *interval* replay to a specific
neighborhood whose remaining uncertainty is removed by one purchased value.
The ordinary two-replay interval method is a valid strong comparator, but
does not supply that unobserved value for free. An ordinary implementation of
the same local identity has identical acquisition requirements.

## A larger product family from fixed blocks

Partition an order into fixed contiguous blocks, each of at most b coordinates.
Allow arbitrary permutations WITHIN each block, keeping block order fixed.
Because the stopping predicate is monotone and order-independent, the index
of the block containing the first certificate is identical for every policy
in this family. Earlier blocks must be fully bought, and later blocks are
unreached. Only the internal order of the stopping block changes the bill.

After the base execution, purchase its remaining stopping-block coordinates.
At most b-1 extra receipts then determine every counterfactual bill in the
product family, whose size is the product of the block factorials. Within
each block the unknown score vector can be arbitrarily dependent on every
other block. This conclusion needs no estimated joint law. Known setup fees
can be added per policy; changing path-dependent work charges needs separate
accounting. Exponential policy count does not mean exponentially cheap planning:
enumerating b! internal orders or optimizing their losses still costs work.

## Conventional online-learning consequence, with all feedback costs

For each block maintain a positive-prior expert distribution over its internal
orders. The global policy samples one order per block. A request's cost is a
constant common to all policies plus a variable loss for its invariant stopping
block. Fully audited stopping-block data give the full loss vector of that
block, so exponential-weights updates factor across blocks. If block g is
active T_g times and its variable losses lie in [0,R_g], the usual fixed-rate
full-feedback bound is

```math
\sum_g\left(\frac{\log(1/\pi_g(\sigma_g^*))}{\eta_g}
 +\frac{\eta_g T_g R_g^2}{8}\right).
```

This is prediction regret against a fixed product of orders. To compare
complete bills, ADD every extra receipt fee, planning/checking cost, and
failed computation. The displayed conventional bound alone does not prove
that learning pays for itself.

Instead audit with a fresh pre-outcome coin of probability rho>0 and update
using the audited vector divided by rho, using zero on unaudited rounds.
For a nonanticipating fixed source sequence, the expected exponential-weights
bound replaces T_g R_g^2 by T_g R_g^2/rho. The reason is that the squared
per-round loss range is zero unless audited, and its expectation is R_g^2/rho.
Add expected audit fees at most rho times the sum of per-request block-fee
bounds. Balancing these terms gives the familiar T^(2/3) costly-feedback scale
when the other parameters are fixed. This is label-efficient prediction
machinery, not a new learning principle. For adaptive adversaries and random
comparators, state the exact expectation/comparator convention before reuse.

Fallible models can propose positive priors or orders. They need not supply
correct truth probabilities for the above feedback identity. Strong ordinary
label-efficient/cascading-feedback methods remain essential comparisons.

## Next cheap screen and restrictions

First check the adjacent and block feedback identities on varied short fully
enumerated sources, with exact fees and receipts. Check the one-receipt lower
example. Then assess the closest sequential-testing and costly-feedback
literature before building a learning service. This is a candidate to develop,
not an established novelty claim or a complete empirical saving.

## Initial finite check and closest comparisons

`local_feedback.py` completed six declared cases in `lf01`, all first attempts
under Python 3.12.14. They cover nonnegative sum thresholds, two-sided Boolean
threshold certificates and DNF witnesses, with nonuniform fixed fees. Each
world was enumerated and reconstructed adjacent/product-family bills were
compared with direct execution. The one-extra lower example also passed.
These are modeled receipt fees and deterministic finite checks, not purchases
from an external computation service.

Berend et al. (2014), section 3, Theorem 1 and its adjacent-exchange proof,
<https://doi.org/10.1016%2Fj.dam.2013.07.014>, establish the independent-test
ordering rule. The 2017 dependent-test companion's abstract was available;
its detailed hypotheses have not been reconstructed. Exchange arguments and
the importance of dependence are established, not new claims here.

Cesa-Bianchi, Lugosi and Stoltz (2005), section III, Figure 2, equations
(2)-(4), Theorem 1 and Remark 1.1,
<https://stoltz.perso.math.cnrs.fr/Publications/CBLS-LabelEff.pdf>, supply the
label-efficient framework, unbiased loss estimates and expected-regret analysis.
Our displayed range-based bound is a separate Hoeffding calculation within
that established framework. Their adaptive-environment treatment is stronger
than the fixed-sequence scope currently used here.

Gergatsouli and Tzamos (2022), section 4, Algorithm 2 and Theorem 4.1,
<https://proceedings.mlr.press/v162/gergatsouli22a/gergatsouli22a.pdf>, already
learn search orders with costly partial feedback by occasionally opening all
boxes and obtaining the whole loss function. Their comparator includes all
orders with approximation guarantees. The proposed restricted-family delta
is replacing that full reveal with a small exact local feedback acquisition;
restricting the comparator is a substantive tradeoff, not general superiority.

Zhou et al. (2018), section 3,
<https://www.ijcai.org/proceedings/2018/0448.pdf>, study cost-aware cascading
bandits with stochastic arm states/costs and prefix feedback. That is a strong
learning antecedent; no theorem from its stochastic model is transferred to
arbitrarily dependent deterministic context sequences here.
