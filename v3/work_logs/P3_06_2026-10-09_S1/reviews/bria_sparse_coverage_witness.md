# Sparse recurring errors separate normalized forecast criteria from BRIA coverage

Date: 2026-10-09. Author: ChatGPT (GPT-6 Astra Pro), delegated literature
reviewer. Status: definition-level witness, checked against the primary source
and independently reviewed algebraically. This is a prescribed computable tape,
not a trace of either production forecaster. No executable run or principal time
credit is claimed.

## 1. The exact coverage quantifiers

Source: Oesterheld, Demski and Conitzer,
[A Theory of Bounded Inductive Rationality](https://arxiv.org/pdf/2307.05068),
arXiv:2307.05068v1, EPTCS 379 (2023), 421–440, §§4.2–4.4, Definitions 2–7,
printed pp. 424–425.

For an agent $`\alpha`$ and hypothesis $`h`$, put

```math
B=\{t:h_t^e>\alpha_t^e\},\qquad
l_T(\alpha,r,M,h)=\sum_{t\in M,\ t\le T}(r_t-h_t^e).
```

Definition 4 permits precisely test sets satisfying
$`M\subseteq\{t:\alpha_t^c=h_t^c\}`$. It does **not** require
$`M\subseteq B`$, or require every test set to be infinite. Definition 6 requires
either finite $`B`$, or $`l_T\to-\infty`$ as $`T\to\infty`$ through $`T\in B`$.
Definition 7 requires coverage for every hypothesis in the chosen class, together
with no overestimation. Thus successful coverage when $`B`$ is infinite implies
infinitely many tests; this is a consequence, not an additional restriction in
Definition 4. The zero-record reasoning below also occurs in the source's §4.5
examples, printed p. 426.

## 2. A completely specified tape

Use unit stakes and rounds $`t\ge1`$. Let

```math
P=\{2^k:k\ge0\},\qquad N(T)=|P\cap\{1,\ldots,T\}|=\lfloor\log_2T\rfloor+1,
\qquad y_t=\mathbf1_P(t),\qquad p_t=\frac25\mathbf1_P(t).
```

Both actions are available every round, with losses
$`c_0(y)=y`$ and $`c_1(y)=1-y`$. Their forecast cost difference is
$`\Delta(p)=1-2p`$. For any positive dyadic smoothing schedule
$`\eta_t\le1/16`$, the main smooth readout gives

```math
s_t=\min\!\left(1,\max\!\left(0,\frac12-\frac{1-2p_t}{2\eta_t}\right)\right)=0,
```

because $`1-2p_t\ge1/5>\eta_t`$. Hence the realized choice is always
$`\alpha_t^c=0`$, its reward is $`r_t=1-y_t`$, and its issued reward estimate is
$`\alpha_t^e=1-p_t`$. Include the perfect supplied expert $`q_t=y_t`$. The
power-of-two pattern is computable; the example does not hide an unavailable
oracle or mathematical shortcut.

The following are direct calculations on this tape:

```math
R_T^{\rm Brier}
=\sum_{t\le T}\bigl((p_t-y_t)^2-(q_t-y_t)^2\bigr)
=\frac9{25}N(T)=O(\log T).
```

The perfect expert also has the lowest possible cumulative Brier loss, so this
is regret to the best supplied expert. For every fixed bounded report test $`f`$,

```math
\sum_{t\le T}f(p_t)(y_t-p_t)=\frac35 f(2/5)N(T),\qquad
\frac1T\sum_{t\le T}f(p_t)(y_t-p_t)\longrightarrow0.
```

This is normalization by all rounds. Conditional calibration on the rare
$`p_t=2/5`$ subsequence fails: its residual divided by its own count remains
$`3/5`$.

The fixed-action losses are $`L_{0,T}=N(T)`$ and $`L_{1,T}=T-N(T)`$. Since the
agent always chooses 0, its external regret is
$`\max(0,2N(T)-T)`$, which is eventually exactly zero. Its reward overestimation
satisfies

```math
\frac1T\sum_{t\le T}(\alpha_t^e-r_t)=\frac{3N(T)}{5T}\longrightarrow0.
```

It therefore satisfies BRIA's no-overestimation clause.

## 3. Coverage nevertheless fails

Choose a hypothesis class containing the computable hypothesis
$`h_t^c=\mathbf1_P(t)`$, $`h_t^e=1`$. It strictly outpromises the agent exactly
on $`B=P`$, an infinite set. The action-matching set is exactly $`P^c`$.
Every admissible test set therefore satisfies $`M\subseteq P^c`$. At each of
these tests, $`r_t=h_t^e=1`$, so

```math
l_T(\alpha,r,M,h)=0\qquad\hbox{for every admissible }M\hbox{ and every }T.
```

There are infinite admissible test sets, but none has a record tending to
negative infinity along $`B`$. The agent fails coverage of $`h`$, and therefore
fails the BRIA criterion for any class containing $`h`$.

**Correction to the proposed rationale:** failure follows from the identically
zero record for every admissible test set. It does not follow from a supposed
requirement that tests occur in $`B`$, or from absence of infinite test sets.
The existing source note's §8 displayed definition already used the correct
action-matching restriction; the added explicit clarification makes this
quantifier distinction visible.

## 4. Precisely what this separates

Vanishing time-averaged Brier regret, vanishing time-normalized bounded report-test
residuals, eventually zero fixed-action regret, and BRIA no-overestimation do
not jointly imply BRIA coverage. This example supplies the perfect pattern
expert as well as the pattern-based BRIA hypothesis, so its comparison does not
depend on omitting the pattern from the available library.

This is not a claim that either production algorithm generates the tape. In
particular, the simultaneous exponential-capital comparator's constant expert
regret, with a positive prior on the perfect expert, fixed positive learning
rate and bounded total capital allowance, excludes this particular tape's
unbounded $`9N(T)/25`$ regret. The witness establishes no non-implication from
that stronger guarantee. It introduces no new priority, contribution, logical
induction, or paid-computation result.

Independent proof review confirmed the spike count, smooth readout, all four
metric identities, and the zero-record argument under Definitions 4 and 6.
Primary retrieval receipts: `turn44view0`, reopened as `turn49view0`. These are
session references; the URL and publication locators above are the durable
source identifiers. Subagent research time is unmeasured and contributes zero
to the principal Research90 ledger.
