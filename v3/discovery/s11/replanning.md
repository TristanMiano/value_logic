# Replanning across plausible models: a cheap boundary and repair

Codex (GPT-6), DEVELOPMENT. Q3/Q4 connection. This is a small independent
worked example of established dynamic-consistency issues, not a new principle.

## Conditioning every model is not enough to preserve a prior guarantee

There are two plausible models, A and B. An external event E arrives with
probability 9/10 under A and 1/10 under B. Outside E every available plan has
zero cost. At E the agent must guess a bit: it is certainly 0 under A and
certainly 1 under B. Incorrect guesses cost one; correct guesses cost zero.
The model-aware comparator has zero loss under either model.

Let q be the probability of guessing 0 after E. The initial worst-case
expected regret is

```math
\max\{\tfrac9{10}(1-q),\tfrac1{10}q\}.
```

Its unique minimum is q=9/10, with regret 9/100. After E, conditioning both
models and giving them equal worst-case standing yields max(1-q,q), minimized
at q=1/2. If that replanning rule is what the agent actually executes, its
initial worst-case regret is 9/20: five times the committed guarantee.

This example has a coupled two-model uncertainty set: event frequency and
conditional label are linked. It is not a counterexample to the s11 oracle's
separately stated known-mass, Cartesian conditional-mean assumptions. It shows
why an extension to several fallible models must specify the updating rule,
the comparator menu and what is committed before observation.

Likelihood weights 1 and 1/9 after E retain q=9/10 in this example. That is a
special case of existing weighted-regret updating. It does not prove that
likelihood weighting alone prevents every dynamic inconsistency; the general
literature also imposes menu and separability/rectangularity conditions.

## A conservative local replacement certificate

Fix the original comparator menu and source set U. A continuation replacement
at a node h is safe for the old regret bound if its conditional expected cost
is no greater than the old continuation under EVERY source reaching h. The
prefix and other branches are unchanged, so multiplying by each source's
reach probability and summing proves sourcewise total-cost dominance. Subtract
the same model-aware comparator value to preserve the regret bound.

For a finite source menu this is a finite list of inequalities. For the
query/flip mean box, the cost-difference certificate is an endpoint support
sum; checked aliases require the grouped coefficient, not separate copies.
Charge the new continuation's computation and queries in its cost. The source
must still belong to the certified uncertainty set; an unwarranted fallible
model is not made reliable by checking an inequality about it.

More generally, if sourcewise conditional cost increase is <=gamma_h, a
replacement at one node raises total source cost by at most Pr_mu(h)*gamma_h.
For mutually exclusive replacement nodes, add those reach-weighted bounds.
For nested replacements, use a sequence of old/new policies with the relevant
reach measure at each step; simply summing bounds from incompatible baseline
occupancies is not justified.

In the example, q=.9 to q=.5 raises A's conditional cost by .4 and lowers B's
by .4. The common-source dominance test correctly refuses a non-increase
certificate. If the total regret budget is instead 3/25, source A requires
q>=13/15; the most balanced admissible continuation chooses q=13/15. This
spends an explicit 3/100 of the original regret allowance.

## Literature and disposition

[Halpern and Leung](https://www.cs.cornell.edu/home/halpern/papers/dmwer.pdf),
section 2's likelihood updating, section 3's menu discussion and section 4,
Definition 4.4/Theorem 4.5, treat dynamic regret and its additional conditions.
[Petrik, Ghavamzadeh and Chow (2016)](https://proceedings.neurips.cc/paper/2016/file/9a3d458322d70046f63dfd8b0153ece4-Paper.pdf)
formulate robust improvement relative to one baseline under the same model.
These are direct conventional antecedents. Park a generic new
"consistent-reliance" claim. Retain the example and sourcewise replacement
check as requirements for any later adaptive multi-model implementation.
