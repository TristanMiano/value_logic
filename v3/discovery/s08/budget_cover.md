# A bounded fee policy improvement over the anchor

**DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**

The graph cover gives a valid action at quota Q; an anchor query of fee C
always reaches Q. Expected-marginal greedy can spend more than C before
finishing, and source-law misspecification can make its expected-fee claim
irrelevant. Consider a narrower, implementable baseline-policy improvement.
At an uncovered state s, let p_i(s) be the conditional probability that
query i alone completes cover. With independent uniform node costs, count
the cached response marginals that meet the remaining quota and divide by
the support size. This is not the expected fractional cover increment.

Choose any unqueried node with c_i < C p_i(s), otherwise buy the anchor.
An optional remaining pre-anchor budget b restricts eligible nodes to
c_i <= b, and the selected fee is subtracted from b. A deterministic
tie rule can maximize the immediate expected saving C p_i(s)-c_i.
The source model affects selection but every final action retains the
distribution-free receipt/cut certificate from gc02.

## Expected fee and a pointwise cap

Let V(s,b) be the expected remaining physical fee, conditional on the
correct public source model and current observations. Backward induction
on remaining unqueried nodes gives V(s,b) <= C at every uncovered state.
Fallback has value C. For an eligible query, completed children have value
zero and other children have value at most C, so

```math
V(s,b)\le c_i+(1-p_i(s))C<C.
```

This is an elementary one-step improvement of an executable ordinary
baseline policy, not a new decision-theoretic principle. Correlation is
allowed if the conditional p_i(s) really is known; using unconditional
probabilities under correlation does not prove the inequality. The chosen
conditional probabilities and any cost of learning them are not free.

Budget B gives a pointwise physical-fee bound B+C, because node spend
never exceeds B and at most one anchor is acquired. If initial B=C,
the expected fee is at most C and every realization costs at most 2C.
The guarantee is relative to anchor-only, not optimal expected fee. It
ignores computation and is not an all-resource economic claim.

For the exact model a stronger accounting identity follows by summing
conditional expectations along reached nonterminal states. Assign
potential C before termination and zero afterward. Every node query has
expected fee plus potential change c_i-C p_i(s); the eventual anchor has
fee plus change zero. Finite stopping yields

```math
\mathbb E[\mathrm{fee}]
=C-\mathbb E\!\left[\sum_{\text{node queries }i}
                         (C p_i(s)-c_i)\right].
```

This identity explicitly measures why the restricted controller may save
money and why it may fail to find a multistep opportunity. If no one query
can complete cover, every p_i is zero and the policy immediately buys the
anchor, even if two inexpensive queries almost always finish. Increasing
B does not repair that limitation. The gc02 larger graphs often require
several nodes, so a finite screen should precede paid service.

For horizon h, define V_0(s,b)=C unless covered, when it is zero, and
V_h as the minimum of C and c_i plus the conditional mean of
V_{h-1}(child,b-c_i) over affordable unobserved nodes. Then
V_h <= V_{h-1}. Recompute the same h-step rule after every observation,
rather than decreasing h. Its true expected remaining fee is at most
V_h: apply backward induction, using the child inequality
V_h(child) <= V_{h-1}(child). Budget still gives B+C. Thus a small
lookahead can use two-query opportunities while retaining the anchor
comparison. This is ordinary receding-horizon policy improvement; it
does not import an optimal-policy guarantee or erase its planning cost.

## Prospective small screen bc01

Use the already exposed ac01 four anchor-star sources and gc02 twelve
graphs. Compute the initial one-query completion probabilities, fee
eligibility, and one-/two-step fallback expected fees without acquiring new
costs. For ac01, evaluate both resulting budget-C policies exactly on all
public source worlds and compare it with anchor, greedy and the saved
optimal expected policy. Charge the policy construction and evaluation
operations as diagnostic work. Verify the potential identity, expected
fee bound, and worst-case cap; include a two-query complementarity case
where the one-step policy stops prematurely. Retain negative screens
without launching a paid service just to fill a denominator.
