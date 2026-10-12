# Fixed-action certificates from separately checked cost anchors

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 12, 2026 UTC.
DEVELOPMENT; same-model auxiliary derivation. No auxiliary time enters the
principal clock. This develops [calibrated repair](../s05/calibrated_repair.md)
and [certificate-directed acquisition](acq_theory.md), with no readiness or
material-positive promotion.

## 1. Different proofs can support one action across a cost hull

Let the fixed logical source have feasible violation vectors `Z`, and let
replacement cost `p`. For a nonnegative penalty vector `w`, define

```text
C*(w) = min_(z in Z) z dot w,
Cbar(w) = min(p, C*(w)).
```

The feasible set and ordered objective meanings must be common to all cost
queries. A checked repair `u in Z` has affine cost `g_u(w)=u dot w`;
replacement has constant cost `g_R(w)=p`. The actual regret of one fixed action
is `r_a(w)=g_a(w)-Cbar(w)`.

**Proposition.** Suppose `W subseteq conv{v_1,...,v_H}` and an independently
admitted scalar lower bound `ell_h <= C*(v_h)` is available at each anchor.
Then the same fixed action `a` satisfies, uniformly over W,

```text
r_a(w) <= max_h [g_a(v_h)-min(p,ell_h)].                 (1)
```

**Proof.** The clipped optimum is a pointwise minimum of affine functions
(the feasible repair costs and the replacement cost), so it is concave. For
any `w=sum_h alpha_h*v_h`, with `alpha_h>=0` and `sum_h alpha_h=1`,

```text
Cbar(w) >= sum_h alpha_h*Cbar(v_h)
        >= sum_h alpha_h*min(p,ell_h).
g_a(w)  = sum_h alpha_h*g_a(v_h).
```

Subtract and bound the resulting convex combination by its largest term.
Equivalently, fixed-action regret is convex and is bounded on the hull by
its anchor values. An admitted feasible action has nonnegative true regret;
using `max(0,...)` in a certificate is harmless. The anchors need not be the
minimal vertex set: any verified finite outer hull containing W is sufficient.

An anchor lower bound may be the maximum of several valid receipts evaluated
at that exact objective. In particular, if retained tree P gives
`L_P(w)=min_leaf v_leaf dot w <= C*(w)`, take
`ell_h=max_P L_P(v_h)`. Different anchors may choose different proofs. This
does **not** claim that the pointwise maximum of retained concave lower
functions is itself concave. The proof uses concavity of the true optimum.

For one fixed candidate action, the quantifiers improve from

```text
single proof: min_P max_h gap(a,P,h)
stitched:     max_h min_P gap(a,P,h),
gap(a,P,h) = max(0,g_a(v_h)-min(p,L_P(v_h))).
```

Minimizing over the same admitted actions preserves the improvement. The
stitched bound is at least as strong, though it can be equal on a particular
bank. Every conventional controller can use this same certificate routine.

### Scalar anchors avoid a global proof-projection requirement

Equation (1) only needs an admitted scalar lower bound at each anchor.
It does not need an exported repricable tree or enumeration of Boolean
objective masks. For an integer objective `q dot z`, a separately checked
UNSAT proof of the bounded source `q dot z <= b` gives `C*(q)>=b+1`.
Rational objectives require an explicit common-denominator conversion and
conversion of the checked bound back to the original cost units.

The receipt must bind the logical source, variables, ordered soft clauses,
exact anchor weights, integer scaling, bound and checked proof bytes. An
optimum status, raw core, generic UNSAT log or checksum is insufficient.
Fresh bounded proof calls, admission and hull construction are paid work.
Anchor transport is valid on the established hull; it is not an unrestricted
repricing license. A missing anchor receipt or unproved hull containment
leaves the requested uniform certificate unresolved. Source-changing logical
updates need fresh admission or a separately proved transport rule.

## 2. A two-coordinate example with a strict gain

Take hard clauses `[x1]`, `[x2]`, and soft clauses `[-x1]`, `[-x2]`. Both
violations are forced, so the checked repair has `u=(1,1)`. Set `p=2` and
`W=conv{(1,0),(0,1)}`. Two bounded questions at the endpoint objectives, each
with budget zero, have separately checkable UNSAT answers. They give the
scalar anchor bounds `ell_1=ell_2=1`.

Their weak, independently valid repricable lower functions are
`L_1(w)=w1` and `L_2(w)=w2`: the respective unit objective cut proves the
corresponding violation is forced. Each single lower proof leaves worst
certificate gap one over W. Using both inside the pointwise lower envelope
`max(w1,w2)` still leaves an artificial midpoint gap one-half. However, both
endpoint gaps for the same repair are zero. Equation (1) certifies zero
regret over the entire segment. Indeed, its cost and the true clipped optimum
are both one everywhere on W.

The [executed anchor probe](vertex_results.json) contains the checked source,
witness and two actual RUP purchases, and reproduces the single-proof bound
one and stitched bound zero. It uses no Boolean-mask projection for the
anchor certificate. The source is deliberately tiny and scoped; this is a
proof of the mechanism, not a solver-performance comparison.

### The action cannot change with the unobserved anchor

If the feasible vectors were instead `(1,0)` and `(0,1)`, one could choose a
zero-cost action at each opposite endpoint. Those two pointwise choices do
not give one uniformly zero-regret repair: either fixed repair has regret
one at one endpoint. A controller may change actions after an actual audit
separates the surviving source states. It may not silently use the unknown
anchor to choose its output.

A single fixed rational distribution over admitted repairs and replacement
also has affine **expected** action cost, so (1) extends to that explicitly
different duty. It certifies expected regret over the output randomization,
not the regret of every sampled action. See [the mixture construction](mix_findings.md).

## 3. A finite minimax audit planner needs no outcome prior

Let `H` be a finite declared hypothesis set. Hypothesis h fixes both its cost
vector `v_h` and the exact observable outcome `o_q(h)` of every offered audit.
With a fixed admitted logical bank, define a decision region for action a:

```text
R_a = {h : g_a(v_h)-min(p,max_P L_P(v_h)) <= tau}.
```

For a nonempty residual set `S subseteq H`, a stopping condition is
`S subseteq R_a` for some single fixed action a. This also certifies that
action over `conv{v_h:h in S}`. For a declared batch of logical requests,
each request may choose its own fixed action, but each must cover all of S.

Suppose each offered audit has a known positive complete cost `c_q`, with no
extra history-dependent state. Write `S_(q,o)={h in S:o_q(h)=o}`. Exact worst
additional audit cost satisfies the finite dynamic program

```text
V(S) = 0,                                      if S is terminal;
V(S) = min_q [c_q + max_(o:S_(q,o)!=empty) V(S_(q,o))], otherwise.  (2)
```

Only informative deterministic queries need consideration: every nonempty
child must be a strict subset of S. The finite recursion follows by choosing
the first query of any successful policy and then choosing a worst feasible
outcome; optimal child policies attain the reverse inequality. If no query
has finite cost for every possible child, set `V(S)=infinity`. No probability
distribution on H is introduced.

This terminal predicate is a decision-region determination connection, but
the objective and assumptions differ from a Bayesian approximation theorem.
[Javdani et al., *Near Optimal Bayesian Active Learning for Decision Making*,
AISTATS 2014](https://proceedings.mlr.press/v33/javdani14.pdf), Section 2,
pp. 431–432, defines a known prior, deterministic test outcomes, overlapping
regions covering the hypotheses, and expected test cost. Section 3.5,
Theorems 2–3, pp. 433–434, gives properties of the HEC objective and an
expected-cost approximation under its assumptions. These sections were read
directly. Here (2) is an elementary minimax recursion with a fixed checked
bank; no HEC or adaptive-submodular guarantee transfers to it or to a mixed
audit/logical-search controller.

### Coverage, state and invoice limits

* An incomplete bank can leave a singleton outside every certified region.
  Then even learning the exact cost mode cannot complete that request using
  this bank. `V=infinity` concerns the declared audit-only problem; it does
  not say that the repair is bad or that the discovery program has ended.
* A state or arithmetic cap leaves planning unresolved. It is distinct from
  exhausting the complete finite recursion and proving no audit-only policy
  succeeds. Proof calls with a possible interruption must include that
  no-progress outcome in any guaranteed-completion planning extension.
* Version space S is sufficient only when it determines future test menus,
  prices, admitted evidence and required outputs. Warm solver state, setup
  charges, spending caps, deadlines or newly purchased logical proofs may
  require an expanded state. Pure audit planning holds the logical bank fixed.
* Coordinate outcomes belong to hypotheses, not arbitrary convex combinations
  introduced for certification. For several cohort rows, two configurations
  with the same mean may return different cell-audit outcomes. Merging them
  solely by their mean is unsound unless the observable transitions and
  remaining costs are also equivalent.
* Query counts are not complete economic costs. Admission, region compilation,
  planning, checking, storage and actual observation fees remain payable.
  If all requests are planned jointly, their availability and required
  completion schedule are part of the declared batch service.

The accompanying [planner](vertex_repair.py) and [probe](vertex_probe.py)
use a declared **one-row, six-mode** source, price 6 and tolerance 1/2, with
unit audit-count prices and the same 16 original admitted cache banks in both
proof policies. This is a planning rehearsal, not the executed eight-row
joint source. There are no new audits or native optimization calls in this
rehearsal. The result compares all 63 nonempty mode subsets for every bank
(1,008 comparisons): stitching is never weaker and has no strict gain in
this bank. Every request has at least one singleton with insufficient checked
coverage, so all full-source audit-only plans remain unresolved. The result
retains these coverage failures; the strict constructive gain is the separate
two-anchor example above.

## 4. A practical route from cohorts to affordable anchors

For independent admissibility constraints on N rows with allowed mode sets
`Q_i`, the convex hull of feasible total costs is `sum_i conv(Q_i)`. Group
rows with identical allowed mode sets into types g with multiplicity `n_g`.
Then a finite generating set is

```text
{sum_g n_g*m_g : m_g in Q_g},
```

because `n_g*conv(Q_g)=conv{n_g*m:m in Q_g}` and Minkowski sums commute with
finite convex hulls. Initially, if every row has the same six-mode menu,
only its six scaled generators are needed for a hull certificate, rather
than all six-to-the-N cohort assignments. Divide generators by N for mean
costs. Different admissibility groups can grow the generator product again;
charge construction and cap it explicitly. Dropping genuine cross-row
constraints gives a safe outer hull, with possible loss of certificate power.

This compression serves the cost hull certificate. It does not establish
an equivalent quotient of the audit state. A useful next construction is to
pay for missing scalar anchors only when their completed hull certificate
offers a justified output benefit, while preserving the unresolved anchor
and logical-search paths when the acquisition cap is reached.
