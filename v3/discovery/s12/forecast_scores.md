# Forecast amplification is useful only with the right performance premise

Codex (GPT-6), s12 DEVELOPMENT early screen, Q1/Q3/Q4. The imported starting
point is Ben-David–Blais [Sections 3.1 and 3.4, Lemma 3.10](https://arxiv.org/pdf/2002.10802):
their hs scoring rule and independent repetition. This is established work,
not a proposed new logical-uncertainty learner.

For fixed truth y, put R_1(p)=sqrt((1-p)/p), R_0(p)=sqrt(p/(1-p)) and score
1-R_y(p). Restrict p to (0,1) here to avoid extended-value endpoint cases.
Multiplying forecast odds multiplies the R_y factors. Independent repeats
at a fixed input therefore multiply their expected factors. The premise is
performance over procedure randomness for each input, not population-average
accuracy or model agreement.

## A concrete population-to-repetition failure

Consider a fixed forecast giving probability 4/5 to its chosen answer. Across
a task population, its chosen answer is correct on 3/4 of inputs. Its hs score
is 1/2 when correct and -1 when wrong, giving mean 1/8. Combining two copies
of that same forecast by multiplying odds produces confidence 16/17. The new
scores are 3/4 and -3, so the population mean is -3/16. A positive initial
average score has become negative; it did not amplify to 15/64.

By contrast, if on *each fixed input* independent runs choose the correct
answer with probability 3/4 and report confidence 4/5, both individual scores
have mean 1/8 and the combined mean is 15/64. The difference is the joint
experiment being warranted, not the displayed confidence numbers. Running a
deterministic model twice does not supply that second experiment.

## Conditional acquisition contract

An ordinary multiplicative-process extension makes the needed adaptive
premise explicit. On one fixed input with truth y, let paid procedure t return
p_t after history H_(t-1). Suppose a justified predictable s_t in [0,1) obeys

    E[R_y(p_t) | H_(t-1)] <= 1-s_t.

Then M_t=product_(j<=t) R_y(p_j)/(1-s_j) is a nonnegative supermartingale.
At a bounded stopping time tau with product_(j<=tau)(1-s_j)<=eta on every
path, optional stopping gives E[product R_y(p_j)]<=eta. The combined forecast
has expected hs score at least 1-eta. Predicting its more likely answer has
error probability at most eta, because a wrong-side forecast has R_y>=1.
This proof uses a conditional performance premise, so procedures may be
selected from the current history. Unconditional empirical scores do not
automatically supply it. Bounded stopping avoids silently importing a
convergence/integrability assumption.

If fixed procedures have valid uniform score floors s_i and fixed costs c_i,
each use contributes -log(1-s_i) to a sufficient progress budget. Optimizing
that budget is an ordinary covering/allocation problem; integer batching,
controller cost and budgeted abstention still matter. The hard step is
obtaining those score floors for the current unresolved truth. A model's own
confidence is not such a certificate.

For proof-producing randomized searches, returning the exact answer on a
checked success and 1/2 otherwise already has score equal to success
probability (using the correct endpoint convention). Repetition then reduces
to familiar independent proof-search attempts. Without a new way to obtain
useful conditional guarantees more cheaply, this branch does not justify a
new learner harness. Retain the counterexample and contract; continue discovery.
