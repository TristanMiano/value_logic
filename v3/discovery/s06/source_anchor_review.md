# Focused review of scalar-anchor transport and acquisition quotations

Reviewer: **ChatGPT (GPT-6 Astra Pro)**, October 12, 2026 UTC; same-model
auxiliary review, DEVELOPMENT. The principal's research clock was already
closed at **60.07154650425 effective minutes**. This publication review adds
**zero research minutes**. No acquisitions, solver calls or test campaign were
run; frozen code and result bytes were preserved.

## Outcome and two binding qualifications

The rowwise scalar transport, positive/negative logical quotation bounds,
and fixed-action audit argument are mathematically valid on the declared
**nonnegative-weight, fixed-logical-source service domain**. The descriptions
and reported counts in [source_anchor.md](source_anchor.md) agree with the
four reviewed result records.

Two adjacent comments/contracts need the following explicit qualifications.
They do not invalidate the executed nonnegative-cost results:

1. **`cut_dual.point_lower` is not an unrestricted-real-weight evaluator.**
   The exact raw dual expression `K-sum_j max(a_j-w_j,0)` is a valid lower
   bound for arbitrary real weights given its admitted Boolean cuts. The
   implementation then clamps this value to zero. That additional step uses
   nonnegative objective costs. Thus the certificate field mentioning
   "any real weight vector" must not be read as authorization to export the
   clamped evaluator on negative weights. For example, a forced Boolean
   violation `z=1` has optimum -1 at weight -1; returning a clamped zero would
   be invalid. The actual service accepts nonnegative weights. A future
   generalized interface must enforce that domain or separately preserve the
   unclamped formula and revise its dependent contracts.
2. **The clamped dual lower function is not generally concave.**
   The comment in `dual_hull_probe.py` about a globally concave unrounded
   dual is correct for the raw expression, but not generally after
   `point_lower` applies `max(0,...)`. With admitted cut `z1+z2>=1`, the raw
   unit-multiplier lower on `[0,1]^2` is `w1+w2-1`; its zero clamp takes
   values 0, 0 and 1 at `(0,0)`, `(1/2,1/2)` and `(1,1)`, violating
   concavity. **Anchor transport relies on concavity of the true optimum
   `C*`, not concavity of a clamped dual surrogate.** Each returned scalar
   anchor bound is independently valid, which is all `anchor_certificate`
   requires. Integer ceiling is likewise used only at admitted integral
   objectives. Neither property requires the ceiling/clamped interpolating
   function itself to be concave.

These qualifications preserve the frozen evidence while defining the
intended interface accurately. They are not claims that the proof-admission
chain works for unseen sources or objectives.

## Mathematical checks

### Row modes transport paid scalar proof work

For N fixed cost rows, let `ell_k<=C*(N*m_k)` and set `d_k=ell_k/N`.
For compatible modes `h_i`, their cost sum satisfies

```text
w = (1/N)*sum_i N*m_(h_i),
C*(w) >= sum_i d_(h_i).
```

This is concavity of the minimum of the same feasible source's linear
objectives. For fractional mixtures within each row, apply the same argument
to their mode coefficients; the total convex coefficients still sum to one.
No stochastic law or independence premise is inserted.

For fixed repair u, its regret against the repair-or-replacement optimum is
bounded by the maximum of its comparison with replacement and its comparison
with this transported lower. Maximizing these expressions over each row's
allowed modes gives exactly the two sums implemented in
[source_anchor.py](source_anchor.py). The replacement formula follows from
the minimum possible transported lower. Different anchors can use different
checked proofs, but every returned action is fixed over the surviving source.

The full-cohort objective scaling in `source_anchor_probe.py` is explicit:
it maps each saved anchor back to a public mode and checks equality to
`N*mode`. It rechecks raw cut exports, reconstructs the nonnegative rational
dual coefficients, recomputes scalar anchors and checks candidate witnesses
before reuse. A saved optimum status or `checked` flag supplies no new proof.

### Both logical outcomes have valid conditional bounds

For a checked SAT witness u with integer query `q dot u<=b`, Boolean
violations and the warranted coordinate enclosure give

```text
u dot w <= b + sum_j max(hi_j-q_j,0) = U.
```

With the already admitted uniform lower `L=sum_i min_(k in Q_i) d_k`, choosing
the returned witness when `U<=p`, otherwise replacement, has uniform regret
at most `max(0,min(U,p)-min(L,p))`. This choice uses a known uniform bound,
not the unknown true cost vector. Retaining the old certified action safely
caps this conditional quotation by the old bound.

A checked UNSAT answer to `q dot z<=b` gives `q dot z>=b+1` because the
query objective is integral. At anchor `v_k=N*m_k`, every Boolean z obeys

```text
v_k dot z >= b+1-sum_j max(q_j-v_k[j],0).
```

Taking the maximum with the old admitted anchor and zero is valid in the
nonnegative-weight domain. Recomputing the rowwise certificate with these
stronger anchors therefore gives a sound negative-outcome quotation.

Taking the worst of the two checked outcomes is a completed-call guarantee
only when a separate complete provider contract applies. The code correctly
restores the unchanged old bound when unresolved/no-progress is a possible
outcome. The `complete` flag records that premise; it does not prove a native
cap sufficient or supply an economic runtime law.

### Zero worst-case gain for a genuinely fixed action

For an unchanged action and anchor bank, the implemented bound is the maximum
of fixed functions over the current latent configurations, together with
zero. Exact complete audit outcomes partition those configurations. Maximum
over all partitions therefore reproduces the previous maximum:
`max_outcome B_u(after)=B_u(before)`.

Permitting action choice after the observation changes the quantifier order
to `max_outcome min_u B_u(after)`, which can be strictly smaller than
`min_u B_u(before)`. The audit example has this strict separation. Its
`fixed_action_quotes` invoke a routine that also retains replacement, but in
this recorded example replacement is never selected in those branches: every
branch retains the stipulated repair. The recorded zero-gain comparison is
therefore indeed a fixed-repair comparison. The general theorem should not
be applied to a future quotation that switches from that repair to replacement.

## Description/result correspondence

| Evidence | Reviewed correspondence |
|---|---|
| [dual_hull_results.json](dual_hull_results.json) | 9 requested-tolerance banks and 12 exact banks; 54+72=126 new LP proposals; 38/54 and 63/72 anchor matches to the same-cut projection; no strict final representation-bound differences and no tolerance-4 closures. 1,031,243 named units; zero new SAT/IHS/proof/audit calls. |
| [source_anchor_results.json](source_anchor_results.json) | The same 14 recorded audit-first observations, at prefixes 0,4,8,12,14. Requested-bank closures 0,0,0,1,4; exact-bank closures 0,0,0,4,5. All 21 banks have a strictly tighter final bound. At prefix 12 one cost row remains unresolved, with closures on row 1 and rows 1,4,9,15 respectively. 1,251,524 replay units; zero new LP/SAT/IHS/proof/audit calls. |
| [anchor_quote_results.json](anchor_quote_results.json) | Initial bound 4; every single-cell audit has worst bound 4. Complete query `(q,b)=((3,3),4)` quotes SAT bound 2 and UNSAT bound 2. Allowing no progress restores worst bound 4. The already recorded SAT witness rechecks to uniform bound 0. 8,242 replay/quotation units; zero new acquisitions. |
| [audit_results.json](audit_results.json) | Modes `(0,2)` and `(2,0)`, two checked candidate repairs, price 3, tolerance 0. Each fixed repair has worst bound 2 and zero guaranteed audit gain; allowing the repair to follow the actual outcome gives bound 0 in both branches. One actual cell observation returns 2 and selects checked model 2 with bound 0. No logical or LP call; 632 named checking/quotation units plus 4 provider software units, with external observation price unassigned. |

The listed wall/process measurements also match the descriptions. These are
recorded runtime measurements and operation tariffs, not a common economic
conversion. The source-refinement query combines each completed logical
arm's own bank with the same historical cost observations; it is explicitly
retrospective, not a newly executed controller. The two constructed acquisition
regimes establish useful conditional mechanisms without a probability law or
a claim of optimal general acquisition. Discovery and readiness statuses do
not change as a result of this review.
