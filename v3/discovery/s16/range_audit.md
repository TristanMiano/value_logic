# Proof-restricted loss range sets the minimum bounded audit probability

Codex (GPT-6), October 23, 2026. DEVELOPMENT. This is a sharp elementary
query-interface observation, with importance sampling, label-efficient
prediction and loss-range active learning as necessary ordinary comparators.

For a current case, a fixed randomized policy has known expected loss
ell(y) in[0,1] as a function of its still unresolved true label y. A sound
partial proof supplies a nonempty finite feasible label set A containing y.
Prediction evaluation and the partial proof are already paid. Define

    l=min_(y in A) ell(y), u=max_(y in A) ell(y), R=u-l.

An audit either buys the true label or does not. Its purchase decision
uses only current known information and fresh coins, never the unknown
label. Require an estimate Z in[0,1] that is unbiased for EVERY y in A.
No calibrated distribution over the unresolved label is supplied.

## Sharp minimum purchase probability

Any such procedure has purchase probability pi>=R. Indeed, the expected
output on the no-purchase branch is identical for any two labels. On the
purchase branch the difference between conditional expected outputs is
at most1. Thus |E[Z|y1]-E[Z|y2]|<=pi. Apply this to extremal labels.

The bound is attained. For0<R<1, buy with probability R. If bought, use

    Z=(ell(y)-l)/R;

otherwise use the known constant Z=l/(1-R). Both outputs lie in[0,1],
because l+R=u<=1, and E[Z|y]=ell(y). If R=0 use the known loss l with
no audit; if R=1 buy with certainty and return ell(y). This is a bounded
unbiased score, not a revelation of the unbought label or realized policy
error. Costs of sampling the specified probability and rational arithmetic
must be included when they matter.

The sharpness is confined to one optional full-label query and this
conditional-unbiased bounded-score duty. Biased estimators, known label
distributions, multistage partial queries and different score ranges are
different contracts; they can have different optimal prices.

## Binary disagreement and a limit on the hoped-for saving

Let p be the policy's probability of predicting1. Then ell(0)=p and
ell(1)=1-p, so R=|1-2p|. On a no-audit branch Z=1/2. On an audit
branch Z is the0/1 error of the more probable answer. At p=1/2 the
expected policy loss is known exactly and no label is needed to score it.

But this cannot by itself yield arbitrarily cheap LOW-RISK certification.
For either true label, ell(y)>=(1-R)/2. Therefore for any case population,

    expected audit saving 1-E[R] <= 2*expected policy loss.       (1)

If the actual policy risk is at most epsilon, this source of label saving
is at most2epsilon. A claimed90% saving from near-balanced predictions
would imply risk at least45%, not a high-reliability reasoning service.
This rejects the tempting cheap-audit headline before a large experiment.

For K-class0/1 loss with prediction probabilities q_y and no label proof,
R=max q_y-min q_y. Since min q_y<=(1-max q_y)/(K-1),

    1-R <= [K/(K-1)]*ell(y).

Sound partial proofs can change this comparison: restricting A may make
the loss nearly constant and small, even when the unrestricted loss range
is large. That gain comes from paid structural evidence, not arbitrary
confidence in a model. Agreement of several models alone does not justify
shrinking A.

## Statistical use and predictability

For a fixed complete policy h evaluated on iid cases, the bounded score
has the same population mean as its loss. A standard bounded-loss test
or the inherited PAC-Bayes mixture can therefore use these scores without
the larger importance-weight range from an arbitrary tiny propensity.
All policies/predictions, feasible-label evidence and audit probabilities
must meet the original timing contract. A late audit can remain an
unresolved latent score with a sound upper bound until its proof arrives.

Selecting a NEW policy after seeing these audits is not automatically
covered by the old fixed-policy score process. Use a prior/common event
over the whole declared policy universe, or a fresh evaluation stream.
Likewise a changing policy's conditional risk is not the risk of its final
revision. The score construction does not waive those distinctions.

This gives a useful explicit tradeoff between unresolved answers, policy
randomization, partial proof strength and audit price. It does not yet
establish novelty or an end-to-end gain over ordinary label-efficient
estimation on the same proof state.
