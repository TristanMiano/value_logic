# P3-03 proposal — refine a task certificate before resolving truth

Contributor: **ChatGPT (GPT-6 Astra Pro), internal bounded-reconstruction
reviewer**. October 7, 2026 UTC. Mathematical proposal; no new scientific
execution and no additional concurrent time credit.

## 1. A precise additional service

The present kernel can refine individual loss bounds while truth coordinates
stay unresolved. A useful next construction is a **certificate for one named
action**, under a fixed finite action catalogue and common known loss units.
It asks whether the action is within a specified nonnegative tolerance of the
best action at every assignment compatible with the current admitted source.
It does not select which computation to buy, update a learned forecast, or
define a counterfactual.

Let $`S`$ be the nonempty received finite assessment source, and let $`\ell_b(x)`$
be the supplied loss of action $`b`$ at one shared assignment $`x\in S`$. For the
named action $`a`$, define

```math
R_a(x)=\max\bigl(0,\ \max_b(\ell_a(x)-\ell_b(x))\bigr).
```

This is exactly its pointwise regret:

```math
R_a(x)=\ell_a(x)-\min_b\ell_b(x).
```

The equality follows by subtracting each competitor's loss from the same
$`\ell_a(x)`$; including $`b=a`$ supplies zero. A finite maximum, addition and
known negative scaling express the term in the existing loss language when
the resulting finite expression meets the prototype's size and arithmetic
limits. It requires no probability coordinates.

**Certificate theorem.** A sound current-source upper bound $`u_a`$ on $`R_a`$
with $`u_a\leq\varepsilon`$ warrants

```math
\ell_a(x)\leq\min_b\ell_b(x)+\varepsilon
\quad\text{for every }x\in S.
```

At the actual truth vector this transfers through the existing containment
and semantic bridge. Exact finite evaluation yields the converse for this
uniform certificate service: such a certificate is semantically available
exactly when $`\max_{x\in S}R_a(x)\leq\varepsilon`$. A loose interval that
fails the threshold is not by itself a counterexample.

Under fixed source assumptions, objective and units, the kernel's split/prune
refinement makes its upper bound on this term nonincreasing. Once a threshold
certificate is obtained, further such refinement preserves it. Withdrawal or
a changed loss makes the dependent warrant stale through the existing binding
rules; no new revision principle is needed.

## 2. Constructive case using the implemented loss language

Take one unresolved Boolean claim $`x`$ and two supplied actions:

```math
\ell_A(x)=10x,\qquad \ell_B(x)=10x+1.
```

The marginal intervals remain `[0,10]` and `[1,11]`, even after fully processing
the Boolean source `{0,1}`. Neither actual loss is identified, and the truth of
$`x`$ is unresolved. Those marginal intervals overlap, so comparing only the
upper endpoint of A with the lower endpoint of B does not certify A.

The shared-assignment regret query for A is

```math
R_A(x)=\max(0,10x-(10x+1))=0.
```

The current compositional interval evaluator, applied directly to the
uncancelled syntax on the all-star cube, may give `[0,9]`. After splitting
into the two Boolean singletons, both regret intervals are `[0,0]`. Thus
bounded processing can certify the action without resolving the individual
truth or either actual loss. This is a stronger task-specific output than
merely offering two uncertain loss values.

An ordinary symbolic cancellation rule can obtain the same answer earlier.
That shortcut must be available to O-COMB as well; matching repeated terms and
checking the reduction are computations. The construction does not claim that
enumeration is an efficient way to discover an obvious common-cost identity.
Its purpose is to expose exactly which shared information the certificate
uses and to give the current kernel a concrete terminal task.

The pattern extends to $`\ell_b(x)=g(x)+d_b(x)`$: every comparison cancels the
same common cost $`g(x)`$. The relevant information can therefore be smaller
than that needed to recover the individual cost levels. Separate marginal
intervals can discard this relationship.

## 3. A matching obstruction

Keep the same unresolved source `{0,1}`, but set

```math
\ell_A(x)=x,\qquad \ell_B(x)=1-x.
```

At zero, A is uniquely best; at one, B is uniquely best. Each fixed pure action
has worst-case regret one on the received assessment source. Consequently no
sound uniform certificate for either action can meet a tolerance below one
without a stronger source or a different permitted service.

This is an obstruction to that **source-scoped certificate**, not an
information-theoretic lower bound against every bounded program inspecting
the original query. Another permitted computation might resolve $`x`$ cheaply;
ordinary competitors may use it. Nor is the obstruction about a separately
supplied subjective law, whose expected-loss optimum answers another question.

The two constructions explain when uncertainty about truth matters to the
consumer: common uncertainty can cancel from every relevant comparison, while
uncertainty that reverses the best action cannot support the same uniform
certificate.

## 4. Binding and contribution scope

The comparison request must bind the selected action, complete supplied
competitor catalogue, exact loss expressions, common units, tolerance and
active-source identity. A numeric bound on a term called `regret_A` is not
enough if that term was assembled from the wrong original losses. Expression
construction or a checked normalization remains separate from the existing
kernel's interval warrant.

The mathematics is an elementary ordinary dominance/regret reconstruction.
Its phase-three value would be a precise adaptation to the bounded, versioned
loss-query interface and a decision-relevant refinement example. It does not
establish novelty from the identity, a new induction theory, a learned
anticipation guarantee, or a computation-selection policy. P3-N01's disposition
still requires the project's later named comparison assessment.

If the principal adopts an executable example, record that small prospective
question and its exact input before running it. The existing attempt-1
evidence does not already contain this named-action certificate construction.

## 5. Subsequent implementation

The principal adopted this scoped construction and separately authorized its
wrapper. The [implementation record](task_certificate_implementation.md) binds
the resulting code, prospective plan and distinct
`task_certificate_attempt_1` evidence. The original generic development
`attempt_1` remains unchanged. The new dedicated attempt reports nine passing
suites and 64 assertions; it receives no additional concurrent time credit.
