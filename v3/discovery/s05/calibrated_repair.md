# Calibrate the costs that can change the repair decision

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT synthesis and next construction. No integrated statistical repair
experiment has yet been run. This connects [paid calibration](threshold_calibration.md),
[shared value queries](threshold_values.md), [action regions](reprice_regions_findings.md)
and [actual repeated repair requests](repair_stream_results.json).

## Replace supplied penalty weights with an explicit observation contract

The current repair experiments receive their penalty weights. A useful next
mechanism should learn relevant costs as well as buy logical proof work.
Suppose a paid observation reveals bounded nonnegative cost features
`Z=(Z_1,...,Z_m)` under a declared sampling process. The intended penalty is
`w_j=E Z_j`. This model makes the observation and interpretation of a penalty
explicit. It does not infer stakes from an unobserved utility oracle.

The additive interpretation also requires the declared cost-feature law to
apply across the compared actions: expected cost of x is `E[Z dot z(x)]`.
The features may be mutually dependent; independence is unnecessary. If choosing
an action changes their distribution, or only chosen-action costs are observed,
an action-conditional observation/identification bridge is needed instead.
A source or feature-meaning revision does not inherit the old confidence event
automatically. The sampling price includes whatever actually reveals Z.

Maintain a common confidence source W with a justified event `w in W`. A box
of simultaneous mean intervals is the simplest instance. A joint value source
can retain dependencies and be tighter. The event must cover the actual
sampling and refinement policy: fixed-sample bounds need fixed sampling
conditions, while optional stopping needs a valid time-uniform construction.
The earlier fixed-n threshold and anytime calibration constructions are
different choices, with different prices and widths.

For each current hard-feasible assignment, retain its checked violation vector
u. A checked proof tree supplies lower supports v_l. The same deterministic
inequalities already developed for supplied weights now require

```text
sup_(w in W) (u-v_l) dot w <= tau    for every leaf l;
sup_(w in W) u dot w - p <= tau.
```

If they pass, the returned fixed repair has actual regret at most tau whenever
the common statistical event holds. Replacement instead requires
`sup_(w in W) [p-v_l dot w] <= tau` for every leaf. A box permits exact signed
support calculations; a polyhedral source permits checked linear certificates.
All admission, audit, support-query and proof costs belong in the service bill.

The action and its proof may be selected after the observations. Their guarantee
is still covered by the same event because each accepted pair is checked
uniformly over W. There is no extra probability assumption that the selected
proof is independent of the data. In contrast, an individually calibrated
post-selected contrast needs its own selection-valid construction; it cannot
borrow a fixed-query bound merely because a checker accepts its arithmetic.

## Two different purchases can close the same action gap

The service now has two constructive ways to improve its answer:

1. Buy more cost observations, shrinking W while keeping the logical evidence.
2. Buy logical search, improving a feasible action or its lower proof while
   keeping the current cost confidence source.

These channels address different uncertainty. Resolving every logical optimum
can still leave ambiguity about which action is useful when weights are poorly
known. Conversely, exact weights do not provide a cheap proof of the best
hard-feasible repair. A useful acquisition controller chooses between these
purchases from the state actually available and records their separate effects.

There is a cheap structural guide to avoid a pointless proof purchase for a
particular action. If some retained feasible alternative v and some w in W
satisfy `(u-v) dot w > tau`, then u's true regret at that w exceeds tau, because
the actual optimum is no more expensive than the feasible v. No stronger lower
proof can make u uniformly tau-good over the unchanged W. The controller must
shrink W or choose a different action. This rejects only that action's robust
duty; an undiscovered third action might still work uniformly.

For a simple illustrative source requiring at least one of two Boolean repairs,
the minimal violation vectors are (1,0) and (0,1). If both costs range from
0.8 to 1.2 and replacement is expensive, neither repair is uniformly within
0.1 of optimum. The feasible alternatives themselves demonstrate this, even
when the complete logical source is known. A cost audit or a relaxed requested
tolerance is required to certify one fixed action at that precision. This is
a derived example, not an additional experimental dataset.

If the requested guarantee concerns expected loss under randomized actions,
give conventional controls access to mixtures of checked repairs too. In the
two-repair example, a half-and-half mixture has worst expected regret 0.2,
whereas each fixed repair has worst regret 0.4. Both remain insufficient for
tau=0.1, but the mixture meets tau=0.25. The violation vector becomes a checked
convex combination of feasible witness vectors; each realized assignment is
still feasible. This expected-action guarantee differs from guaranteeing the
same tolerance for every sampled repair. The service must state which is asked.

## Let action geometry determine which values need calibration

The guard depends mainly on contrasts `(u-v_l) dot w`, plus the chosen action's
absolute cost against replacement. Estimating every probability or every
penalty equally well may be unnecessary. If observed cost features share one
declared latent source, the [common value-query machinery](threshold_values.md)
can ask directly for these contrasts using the same simultaneous source.
Otherwise use a prospective contrast bank, fresh observations after selecting
a contrast, or another justified uniform construction. Counting adaptive
choices does not replace the needed statistical argument.

The paid threshold work supplies a concrete precedent: partially resolved
observations can support value queries before their latent state is fully known.
The repair work supplies an executable action and a checked region of cost
vectors on which it remains useful. Their combination could make an audit
valuable because it admits a good action, and make a proof valuable because it
enlarges the cost region that current observations can certify.

This is the most promising next synthesis beyond the supplied-weight fixture.
Use the same observation access, common confidence source, feasible actions,
proof reuse, cost forecast and spending cap for conventional controllers. The
comparison should include straightforward robust optimization and the existing
coverage-acquisition methods in [the primary-method bridge](frontier_sources.md).
The intended gain is better paid acquisition for a meaningful output duty,
not a claim that robust optimization or simultaneous confidence is new.

Keep actual action cost, statistical coverage, certified regret, audit work,
logical search work and future reuse distinct in the output. A small successful
example would develop the mechanism; it would not establish deployment transfer
or an 80–90% readiness forecast for a material project result.

## The next small construction should close the loop

Use one explicit cost-observation interface, one current repair source, and
one spending account. Start with a coarse common W and the already checked
action/proof bank. Implement the two available purchases and record which
inequality each purchase could help. Return an action as soon as its requested
statistical and logical guarantee is established, or return its honest current
bound at the spending cap. Retain the evidence for the next source/price request.

Compare the complete trace with an equally informed robust controller that
can audit, search, reuse receipts and stop at exactly the same duty. Include a
simple fixed allocation and an established possible-improvement acquisition
rule when their interfaces match. A live external application can supply the
meaningful monetary or latency conversion; until then expose the full tariff
tradeoff rather than selecting one favorable conversion after the outcome.
The first deliverable should be this executable joint acquisition example,
with a useful derived policy revision if the initial choice is weak. It should
not be another long attempt to certify a marginal advantage on the old fixture.
