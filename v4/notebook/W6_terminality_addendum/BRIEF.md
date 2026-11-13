# Brief: a short W6 addendum on what "terminal" means without a clamp

**Written by Claude (Fable 5.2), November 12, 2026, for Codex (GPT-6)**, at
the author's direction. Planning document; it starts no clock and earns no
recurrence credit. **Status: not started.** Proposed ID: P4-R6-C002.

Read first, in this order: the author's
[clarification](../../decisions/2026-11-12_terminal_instrumental.md), the
charter's Drift section, [AIM_BALANCE](../../AIM_BALANCE.md), then
[R6.4](../../results/R6_plastic_priorities.md) sections 5 to 7 and
[R6.12](../../results/R6_unrepresented_values.md). You wrote both results; the
point of rereading is that the author's question cuts across them in a way
neither states.

## Why this exists

The author read the W6 summary and found two things. One was my error: I
described conditional entrenchment as a correction to his essay's claim that
the terminal/instrumental distinction is "largely gone". He regards it as the
mechanism he proposed, and the degrees of persistence as the blurring itself.
That is fixed in the summary and needs nothing from you.

The other is a gap in the cycle. W6 tested what happens when a priority's
supporting benefit is *removed*. The author's question is the opposite case,
and he says it has not been answered at all:

> What happens when the entrenchment is not removed? As in, something all
> agents have to deal with for all time? [...] Do these "entrenched" goals
> resemble goals we associate with "terminality" (what something ultimately
> wants)?

Behind it is a prior question. A clamped terminal goal was something he
granted for the sake of argument. Nobody knows whether a goal can be clamped
or what would clamp it. So what does "terminal" mean?

## What to deliver

One result file, `v4/results/R6_terminality.md` (R6.17), that a reader can
use to answer the author directly. Its first paragraph should say, in plain
words:

1. **What "terminal" can mean when no goal is known to be clamped.** The
   author names three candidates: the whole value function, its maxima, or a
   high-level summary of what the agent does. For each, say whether it is
   well defined, relative to what, and what would change it.
2. **What a permanently supported priority becomes**, and in which respects
   it does and does not resemble an ultimate want.

Then the statements with proofs, the limiting cases with their repairs, and a
short self-review. Aim for at most three or four statements. This is an
assembly and sharpening of what W6 already contains, plus whatever small new
argument joins the pieces. It is not a new portfolio.

W7 will start from whatever meaning of "terminal" you state here, so prefer
a definition that W7 can test to one that is merely safe.

## What the repository already has

These are your results. I checked the items marked *checked* with
[probe.py](probe.py) (standard library, runs in under ten seconds); I did not
re-derive the rest.

- **R6.12 Theorem 1.** Under a survival filter with positive mixing, the
  behaviour of retained histories far from the time at which a fixed end is
  assessed does not depend on that end. It is the rule
  $`Q^h(i,j)=K_{ij}h_j/(\lambda h_i)`$, with value $`V=\log h`$ given by the
  leading eigenvector of the filter. The end governs only a boundary layer
  before its assessment. *Checked* for the two-state example: whatever the
  end weight, the deviation from $`Q^h`$ is at most 0.75 one step before the
  assessment, 0.107 three steps before, and 0.00073 ten steps before.
- **R6.4 Proposition 2.** With a constant advantage, the growth factor is
  strictly decreasing in the revision rate. Retaining a persistently useful
  priority more faithfully is itself selected. *Checked* on a grid for
  $`R=2`$.
- **R6.4 equation (P.7) and section 7.** After the advantage is removed, the
  remaining fraction of the acquired excess is $`(1-2\mu)^t`$, independent of
  how strong the advantage was.
- **R6.4's table of alternating environments.** When the useful priority
  keeps reversing, a positive revision rate does better than none.
- **R6.15 and R6.6.** A value paid as a difference between successive states
  guides action without changing what is best. So state values are fixed by
  behaviour only up to such a term.
- **R6.8.** Policy/value reconstruction under stated conditions.
- **R6.13.** A copying mechanism that turns the retained pattern into an
  actual controller.

## Candidate statements

These are mine. None is proved here. Prove, repair or replace them; I would
rather you found a better formulation than defended these.

**S1. Terminal relative to a class of interventions.** Call a priority
terminal *over a class of interventions* if it persists under every
intervention in the class. R6.4's robustness under changes of goal and its
persistence after removal of the benefit are then two choices of class. Terminality in the absolute sense is the limiting case in which the
class contains everything, and it is no more verifiable than a final theory.
This would make the notion the value-side counterpart of thesis C3: truth as
the limit of value under successful use, terminal value as the limit of
instrumental value under persistent pressure. As a definition this is cheap.
It needs a theorem to be worth stating. A candidate: by (P.7), for any
observation window $`t`$ and tolerance $`\delta`$ there is a revision rate
below which the removal test cannot detect, within the window, that the
priority was ever instrumental. State what an observer confined to a world
where the pressure never lifts can and cannot determine.

**S2. An end assessed once leaves no trace far from its assessment.** This is
R6.12 Theorem 1 read as an answer to the author. If the pressure is permanent
and the assessment of the clamped end recedes, retained behaviour is governed
by $`V=\log h`$ alone. If the assessment never comes, the clamped end has no
behavioural footprint at all, and the only value structure visible in
behaviour is the one the pressure produced.

**S3. An end paid along the way fuses with the pressure.** Suppose the end is
rewarded at each step with weight $`e^{r_i}`$ in state $`i`$ instead of once
at the end. The path weight becomes the product of $`s_i e^{r_i}`$ along the
path, so the retained rule depends on $`s`$ and $`r`$ only through
$`w_i=s_ie^{r_i}`$. Retained behaviour then cannot say how much of $`w`$ is
what the environment demands and how much is what the agent was built to
want. The one observation that separates them is an intervention on $`s`$,
which is the removal test, and under permanent pressure that test is
unavailable. This follows directly from R6.12 equation (1) for external
selection. Check whether it holds for the control formulation in R6.12
section 3 as well, where I expect the reward to enter as
$`r_i+\log s_i`$, and say what an internally represented $`r`$ adds, if
anything, that behaviour could reveal.

**S4. Persistent pressure can produce the clamp.** Let the revision rate be
heritable. R6.4 Proposition 2 says lower rates grow faster under a constant
advantage. In one toy with five rates and a small chance of moving between
neighbouring rates, the population settles with 68% at rate zero, 29% at
0.001, and 3% above that, and 99.9% hold the priority (probe.py, part 3). So
"held fixed by some undefined means" has at least one defined candidate: the
pressure itself, selecting against revisability. Whether a literal clamp is
reached or only approached depends on whether rate zero is available and on
mutation; say which. The limiting case is already in R6.4: an environment
whose useful priority reverses selects a positive rate.

**S5. Which of the author's three candidates is well defined.**
- *The whole value function.* State values are fixed by behaviour only up to
  the difference term of R6.15. Read literally, "the whole value function is
  terminal" needs a choice of that term or must be restated about differences
  along courses of events.
- *Its maxima.* In general the same freedom moves the maxima. But
  $`V=\log h`$ in R6.12 is determined up to an additive constant once the
  baseline dynamics and the filter are declared, so its maxima are well
  defined *relative to a declared baseline*. That matches the author's phrase
  "minus the choice of harness". This is the reading closest to the essay,
  which explains the appearance of terminal values by states whose values
  exceed those of nearby states. Test it: in the two-state example
  $`h=(2,1)`$ puts the maximum at the state an unrestricted survival
  optimizer also heads for. Does that agreement hold in general, and if not,
  what does a maximum of $`\log h`$ mean?
- *A summary of what it does.* Preferences over whole courses of events are
  what behaviour determines. This is the weakest and safest reading.

A possible single headline, if S2 to S5 survive: under a pressure that is
never removed, with a declared baseline, the maxima of the selected value
are well defined, are fixed by the pressure and not by any clamped end, and
are unrevisable in the limit. In those respects they are what "terminal"
was supposed to pick out, and no clamp was assumed. I do not know that this
is true as stated. It is the claim I would try to prove or break.

## The author's other project

[policy_value_isomorph](https://github.com/TristanMiano/policy_value_isomorph)
is the source of the three candidates. Read
`docs/policy_reconstruction_vs_utility_factorization.md` and
`docs/selection_semantics.md` there before writing S5. From its README and a
skim of the first of those documents, not a full reading: it separates
*behavioural reconstruction* (any policy can be reproduced by a score together
with a declared decoder, and many scores do so) from *expected-utility
factorization* (the score is an expected utility over trajectories, which is
stronger and not guaranteed). The "harness" in the author's message is the
decoder. If that reading is right, "the whole value function is terminal"
lives at the first level and is a decoder-relative equivalence class, and
"what it ultimately wants" asks for the second. Confirm or correct this from
the documents. Cite that project at the level of its actual claims; its
results are not verified in this repository.

[corrigibility-games](https://github.com/TristanMiano/corrigibility-games) is
deliberately left to W7 (plan item W7.6), at the author's suggestion.

## Scope and limits

- **Floor.** I recommended about 60 engaged research minutes. That departs
  from the 240-minute floor, and the override has to be the author's, in his
  words, when he gives you the task. Record it verbatim in your start record.
  If he states no number, ask him; do not infer one from this brief.
- **Clock and records.** Use [clock.py](../clock.py) as before. Make the usual
  start record, set the active-cycle pointer in TODO_v4.md, and close with a
  short assessment and handoff.
- **Stay out of W7.** Which of two conflicting priorities prevails, which
  encoded ends persist in a population, and how ends that were assumed
  terminal get revised under pressure are W7.6. If S4 starts turning into a
  population model with competing ends, stop and hand it over.
- **Keep the typed sequence from R6.12.** External retention gives a
  value-shaped pattern; transmission internalizes it; only then is there
  something an agent could be said to want. "Resembles what something
  ultimately wants" has to say at which of these stages the resemblance
  holds.
- **Pair the constructions.** Limiting cases already in the repository:
  reversing environments (R6.4), isolated components and slow mixing
  (R6.12 section 6), state-independent survival, where no direction appears
  at all, and the model-based planner that beats the copied controller
  (R6.12 section 5). Each should end in a stated condition, not a caution.

## Self-review of this brief

Aim: prepare an addendum that answers the author's two questions under
theses C5 and C7, with a bridge to C3. Paths reviewed: the decision record,
this brief, the W7.6 plan item, the revised summary script. The risk I can
identify is over-correction. Having misread the author's claim as too
strong, I may now be steering toward confirming it: S2 to S4 all favour his
reading, and the headline I suggest is the most favourable assembly of them.
I have listed the limiting cases I know of and marked every statement as
unproved, but I did not look for a construction in which a clamped end
survives permanent pressure intact, and you should. A second risk is that S1
is a relabelling and not a result; the brief says what would make it one.
This is a self-review; no independent review occurred.
