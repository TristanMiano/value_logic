# P3-05 — Counterfactual dependence and proof reuse

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 8, 2026 UTC.
Status: **IN PROGRESS — new reconstruction, not recovered earlier evidence**.
[Session](../work_logs/P3_05_2026-10-08_S2.md) ·
[Recovery disposition](../work_logs/P3_05_2026-10-08_S2/recovery_disposition.md) ·
[Source contracts](../literature/05_transport_sources.md).

This note continues from the published P3-04 completion at
`21a7ccd96f30d073ae58ea8ae73aec7df46fa21c`. The prior P3-05 snapshot contained
no research artifacts or clock records. Its informal descriptions motivate
this reconstruction but are not evidence for any theorem, run or duration here.
P3-06 and all later gates remain unstarted. All tests are development.

## 1. The missing obligation

P3-04 defines a finite feasible family F, a repair ranking rho and the family
S of **all** minimum-ranked alternatives. It supplies sound interrupted covers
and warns that a new hard restriction can exclude every old optimum. Those
results do not yet justify using an old loss certificate after an edit.

There are two separate questions:

1. Does the old proof, with an explicit interpretation/substitution and any
   required premise correction, still bound the quantity at a specified case?
2. Do its case domains cover **every currently selected alternative**?

An unchanged proof file answers neither question on its own. A sound proof on
an old optimizer family may remain perfectly sound as a historical theorem
while no longer supporting the new request. Conversely, preserving optimizer
identities is sufficient in some circumstances but is not necessary for useful
reuse. A wider certified domain can contain the new winners.

The target service is a uniform comparison of one specified pair of actions.
It is not a new probability law, an online learning guarantee, or a discovery
of the correct counterfactual dependence graph from observational data.

## 2. Finite selection and domain-first transport

For each episode j, take an explicitly admitted finite feasible set
$`F_j\subseteq X_j`$, an exactly specified ranking into a totally ordered
set, and known task-loss difference $`d_j=\ell_{a,j}-\ell_{b,j}`$ in a
common unit. Set

```math
S_j=\{x\in F_j:\rho_j(x)\le\rho_j(z)\text{ for all }z\in F_j\}.
```

The finite constructions make feasibility and evaluation explicit and charged.
The theorem does not give free access to complete arithmetic worlds. Unknown
exogenous facts are handled separately: apply the theorem within each source
case, then cover all those cases, rather than minimize rank over which unknown
source fact is most convenient. This preserves P3-04 CE04-6's distinction.

**CT05-1 (coverage plus numerical bridge).** Suppose $`F_1\ne\varnothing`$.
For every $`y\in S_1`$, suppose a permitted pair $`(i,x)`$ exists such that:

- an admitted old or repaired proof i guarantees $`d_{0,i}(x)\le B_i(x)`$;
- the interpretation/quantity bridge guarantees
  $`d_1(y)\le \alpha_i d_{0,i}(x)+\delta_i(x,y)`$, with $`\alpha_i>0`$;
- the chosen pair is in the proof's actual valid domain, not just its old
  displayed name or an unrelated domain with the same number of cases.

Then, writing I(y) for those permitted pairs,

```math
d_1(y)\le \min_{(i,x)\in I(y)}
                 \{\alpha_i B_i(x)+\delta_i(x,y)\},
\qquad
\max_{y\in S_1}d_1(y)
 \le \max_{y\in S_1}\min_{(i,x)\in I(y)}
                 \{\alpha_i B_i(x)+\delta_i(x,y)\}.
```

For infinite I(y), replace the minimum by an infimum under its stated
existence conditions; the present implementation uses finite choices only.
**Proof:** apply each bridge to its valid old inequality, then take the
minimum of valid upper bounds and finally the maximum over the nonempty
selected family. Positive scaling preserves the inequality. Nothing requires
the same proof to be best at every y. This is selection of a *proof*, not
permission for the acting policy to observe hidden y and change its action.
The action pair itself is fixed across cases.

This elementary composition is reconstructed, not a new general transport
principle. The additional P3-05 problem is obtaining coverage economically
without first solving the complete new selection problem.

### 2.1 The inherited withdrawal correction

Phase two already proves replay of a localized proof with explicit residual
penalties for withdrawn rows; see [paper section 4.2](../../paper_v2.md#42-reuse-after-source-revision).
For its supported grammar and rules this yields
$`d_{0,i}(x)\le b_i+R_i(x)`$ on the relaxed retained domain. Use
$`B_i(x)=b_i+R_i(x)`$ in CT05-1. The correction is proof-relative, generally
not optimal or small, and requires actual transported premises and unchanged
operation meanings. A changed counterpossible consequence rule cannot be
repaired merely by changing a numerical bound. The native implementation of
this general proof replay is not reimplemented or newly executed here.

A transparent affine subcase shows why the correction is sound. If
$`d(x)=c+\sum_i\lambda_i a_i(x)`$ with known $`\lambda_i\ge0`$ and old rows
$`a_i(x)\le b_i`$, then for every x,

```math
d(x)\le c+\sum_i\lambda_i b_i
       +\sum_i\lambda_i\max(a_i(x)-b_i,0).
```

Each term satisfies $`a_i\le b_i+\max(a_i-b_i,0)`$. This is a direct
one-line bound, not a new soundness theorem for the full calculus.

### 2.2 Complementary proof portfolios

For two current cases x and y, suppose valid allowances are
$`B_1=(0,10)`$ and $`B_2=(10,0)`$. A pointwise choice of proof gives uniform
allowance zero, whereas taking each proof's worst case before choosing gives
10. Thus the order $`\max\min`$ matters. A scalar old best bound alone loses
this proof-support information. Ordinary dependency-aware checking can retain
exactly the same portfolio; no blanket advantage is asserted.

## 3. Rank-sublevel certificates survive optimizer turnover

This section uses a **scalar rank in fixed units**. It is a restricted
constructive refinement, not an assertion that every value or repair order
must be scalar.

Let $`\pi:X_1\to X_0`$ be an explicitly supplied map. Assume:

- $`\pi(F_1)\subseteq F_0`$;
- for all $`y\in F_1`$, $`\rho_0(\pi y)\le\rho_1(y)+\eta`$;
- a particular $`z\in F_1`$ is checked feasible;
- an old certificate covers the rank sublevel
  $`G_h=\{x\in F_0:\rho_0(x)\le h\}`$;
- $`\rho_1(z)+\eta\le h`$.

**CT05-2 (incumbent-driven sublevel coverage).** Every new winner maps into
G_h, even if **none of the old winners survives**.

**Proof.** For $`y\in S_1`$,

```math
\rho_0(\pi y)\le\rho_1(y)+\eta
                    \le\rho_1(z)+\eta\le h.
```

The domain map puts pi(y) in F0, completing membership in G_h. A feasible z
also proves nonemptiness of F1 and hence of its finite minimizing family.
The incumbent does not need to be globally optimal. Its discovery and checking
must nevertheless be charged. Combining with CT05-1 yields an action bound
without discovering the identities or exact rank of all new winners.

**Loss margin.** If the old certificate says $`d_0\le -m`$ on G_h,
$`d_1(y)\le d_0(\pi y)+\delta`$ and $`\delta\le m`$, then
$`d_1\le0`$ on S1. The useful margin is in loss units, distinct from h and
eta, which are in ranking units.

**Feasibility alone is not enough.** A surviving arbitrary candidate outside
G_h does not license the conclusion. The numerical cutoff is essential.
Nor does failure of this sufficient test show that the true comparison fails;
it can mean the supplied incumbent, sublevel or drift bound is too weak.

### 3.1 A fully explicit turnover example

Let two Boolean coordinates be p and q. Old hard constraints are empty,
old rank is $`p+2q`$, and old difference is $`4q-1`$. The old selected
family is the singleton 00. The wider sublevel at h=1 is {00,10}, and its
uniform difference is -1. Add the new hard condition p=1 without changing
rank or losses. The new selected family is {10}. The old optimum disappears,
but z=10 gives new rank 1 and eta=0, so the wider certificate still proves -1.
A proof saved only for the old rank-zero sublevel cannot pass this check.

Now add q=1 instead. The new winner 01 has difference 3. Old-winner-only
reuse would be false; the h=1 receiver rejects because z has rank 2. If the
new difference becomes old difference+1/2, successful reuse in the p=1 case
returns -1/2; an increment of 2 yields +1 and does not certify non-deterioration.

### 3.2 The familiar two-error band and its sharp boundary

If F1=F0, pi is the identity, and
$`|\rho_1-\rho_0|\le\varepsilon`$, an old minimizer z with old rank m
satisfies

```math
S_1\subseteq\{x:\rho_0(x)\le m+2\varepsilon\}.
```

The same holds for a restriction F1 subset F0 if at least one old minimizer
survives. This follows from CT05-2 with eta=epsilon and
$`\rho_1(z)\le m+\varepsilon`$. It is ordinary perturbation algebra.
With two candidates, old ranks (0,2epsilon) and new ranks (epsilon,epsilon),
the second candidate is a tied new winner. Thus the weak boundary cannot be
removed or the coefficient reduced uniformly. If their task losses are 0 and
100, the small rank change has no correspondingly small loss implication
without a loss certificate over the entire band.

The incumbent version CT05-2 is useful precisely when no old winner survives,
where this special corollary's premise is absent.

### 3.3 Checking rank drift from the actual soft constraints

For a fixed Boolean domain, collect weights of identical soft formulas after
the declared coordinate substitution. Let a_e be total old weight minus new
weight for each formula e. The violation indicator is in [0,1], hence

```math
\rho_0(\pi y)-\rho_1(y)
 =\sum_e a_e(1-e(y))\le\sum_e\max(a_e,0).
```

This supplies eta without solving for new winners. It includes added or
removed soft formulas and preserves their intentional multiplicity. Distinct
IDs with equal formulas still add their weights; an accidental duplicate of
the *same evidence identity* must be rejected by the request interface.
The bound can be loose when formulas are coupled. A tighter proved bound can
replace it, but choosing one from an unexplained favorable sample cannot.

### 3.4 Lexicographic warning

A small leading-tier change can permit an arbitrarily large later-tier value.
Old ranks (0,0) and (epsilon,M), changed to (epsilon,0) and (0,M), switch the
winner for any M while each coordinate changes by at most epsilon. Do not
turn the scalar band into coordinatewise closeness in every tier. A bound in
lexicographic order is a different object. P3-04's finite scalarization may
be used only with its actual range/multiplier proof rechecked after an edit.
The new receiver deliberately admits only one ranking tier.

## 4. Structural identity and meaning-preserving changes

Fix history h, original table f0(h)=0 and replacement f1(h)=1. Let A be the
actor, B another call registered to the same live function, C a copied table,
and P a predictor explicitly of the original table. The copied table agrees
extensionally at baseline; this does not register it for replacement.
Use declared loss $`6+A-2B-C-2P`$.

| Change | A | B | C | P | Loss |
|---|---:|---:|---:|---:|---:|
| No change | 0 | 0 | 0 | 0 | 6 |
| Only actor occurrence overridden | 1 | 0 | 0 | 0 | 7 |
| Live shared function replaced for A and B | 1 | 1 | 0 | 0 | 5 |
| Copy explicitly replaced too | 1 | 1 | 1 | 0 | 4 |
| Predictor also stipulated to track replacement | 1 | 1 | 1 | 1 | 2 |

These are ordinary supplied-graph consequences, not inferred dependencies.
The last row requires a different predictor contract; it does not follow
from implementing f1. If all equations including f0 remain unchanged,
conditioning on A=1 has no state in this deterministic example. This extends
P3-01/P3-04's worked distinction to explicitly separate the copied program.

**CT05-3 (declared refactoring).** A bijection of candidate coordinates that
preserves feasibility, rank order and the compared losses maps all minimizing
families and valid bounds bijectively. If the same map commutes with the named
edit operations, it also preserves their counterfactual results.
**Proof:** pull any putative better competitor back through the bijection;
order preservation contradicts minimality. Apply the loss equality pointwise.
Apply the commuting equation for the edit claim.

This covers consistent renaming and a specifically checked definitional
extension. It does not cover every input/output-equivalent program with hidden
internal intervention points, nor arbitrary syntactic edit distance. Inlining
or duplicating a function can change which occurrence an edit addresses. A
changed number of duplicate repair options can also alter a uniform sampling
policy even when the set of distinct consequences is unchanged.

## 5. Repeated edits, stale records and alternatives

If successive justified bridges are
$`d_1\le\alpha_1d_0+\delta_1`$ and
$`d_2\le\alpha_2d_1+\delta_2`$ with positive scales, composition gives

```math
d_2\le\alpha_2\alpha_1d_0+\alpha_2\delta_1+\delta_2.
```

Domain coverage and current feasibility must hold at **each** bridge. Adding
unscaled errors is wrong when the next bridge changes units. An edit followed
by its exact undo may permit direct reuse of the original complete record,
avoiding needless cumulative slack. It does not erase historical costs.

The same printed scope name does not establish equality of hard premises,
losses, routing metadata, ranking or units. The receiver binds full canonical
records, preserving the distinction between Boolean true and integer 1 in
metadata. This is input consistency, not proof of empirical provenance or
cryptographic authentication. It does not alter P3-04's trusted-in-process
search interface retrospectively.

No one certificate must support every possible edit. Retaining several
verified domains is useful when they offer different combinations of coverage
and tightness. Storage and matching costs matter. In particular, a wider band
can make future reuse easier but require more expensive initial proofs and
weaker bounds. There is no theorem that caching always pays.

## 6. Status of the reconstruction

CT05-1–3 are scoped hand derivations, with self-review. Their components have
ordinary antecedents in conditional inequalities, structural intervention,
abstract verification and incremental optimization. The proposed assembled
service is: certify a broad rank sublevel once, then justify a new selected
comparison using a current feasible witness, a checked rank drift and a checked
loss drift. It is not credited merely for having been restated here.

The new implementation and its coverage, costs and hostile-input tests are
recorded separately in this session. They are not the lost prior implementation.
A general native proof-transport compiler, unrestricted program-equivalence
checker, learned dependency discovery and anticipatory value learner remain
outside the implemented scope. P3-N01 remains NOT YET SUPPORTED.

The relevant duties are C01–C03 (operation/identification/coverage), R01
(revision), I01 (declared transformations), and V03/V04 (action bounds and
resource costs). This is indirect progress toward decision rationality and
counterpossible use, not a new Logical Induction calibration, non-exploitation
or learning theorem. Final task closure also requires the measured Research90
floor; unknown earlier elapsed time does not establish it.

## 7. What to retain: a monotone bound envelope

For a fixed old source and rank, define for nonempty sublevels

```math
B(h)=\max\{d_0(x):x\in F_0,\ \rho_0(x)\le h\}.
```

**CT05-4 (finite envelope and safe domination).** B is nondecreasing on the
attainable sublevel cutoffs and changes only when a new rank value is included.
For certified upper bounds U_i at cutoffs h_i, the incumbent test with threshold
$`t=\rho_1(z)+\eta`$ can use

```math
\min_{i:h_i\ge t} U_i+\delta.
```

For positive loss rescaling alpha use alpha U_i+delta instead. If certificate
A has $`h_A\ge h_B`$ and $`U_A\le U_B`$, it dominates B for **this numerical
service** on the same source, rank, loss and drift bridge. Dropping B cannot
worsen that bound when both remain available at equal access cost. A may cost
more to store or check; numerical dominance is not resource dominance.

**Proof:** increasing h only adds points. CT05-2 applies independently to each
eligible certificate. The minimum of its valid allowances is a valid allowance.
Every threshold served by B is served by A, at an at-least-as-good bound.

A band envelope avoids pretending that an old optimal value encodes all useful
future information. It does not require the full probability law. Conversely,
it need not support arbitrary changed objectives: its values concern the one
specified difference and need the explicit new-loss bridge.

For the turnover fixture, attainable cutoffs are 0,1,2,3 and the exact envelope
is (-1,-1,3,3). The h=1 certificate numerically dominates h=0 while accommodating
the removal of the old winner. h=3 accommodates every feasible old case but
certifies a weaker bound. That is a concrete retention tradeoff, not a claim
that one bound always suffices or that the wider proof is always cheap.

### 7.1 Old winner summaries are insufficient

Take two worlds a,b of old ranks 0,1. In one model their differences are (0,1),
in another (0,100). Both old selected sets, selected values and ranks agree.
The same announced edit excludes a. New exact selected values are 1 and 100.
A summary containing only the old selected data cannot distinguish the new
answers. This is an application of P3-02's information-fiber principle, not
a new universal lower bound or a ban on scalar encodings. A wider retained
loss envelope, or access to the original loss expressions, supplies information
that that particular summary discarded.

### 7.2 Counterpossible frame withdrawal is a real applicability change

Use P3-04's paired p and q support labels. Hard antecedent labels make both
p and not-p supported, and retain ordinary q normality. A soft normality link
for p is necessarily violated; a soft q-frame favors q false. The old preferred
family makes the compared difference $`4t_q-1`$ equal to -1. Removing the
q-frame admits an equally ranked alternative with q true and difference 3.
A previously valid proof restricted to the old band must not survive that
change unchanged. An additional hard q-false restriction, by contrast, preserves
its applicability. The test is about a stipulated hypothetical support space,
not a claim that ordinary arithmetic has a model of contradiction.

The band receiver uses declared numeric differences on those support states.
It does not infer how empirical payoffs extend to impossible states; that is
the explicit independent premise already isolated by P3-04 CE04-2.

## 8. The current executable fragment and its proof

Version `p305-reconstructed-v2` in
[05_counterfactual_transport.py](../checks/05_counterfactual_transport.py)
uses the unchanged P3-04 expression/request definitions, at most ten Boolean
coordinates and **one** rank tier. A bounded binary split tree covers every
old Boolean assignment. Each leaf either proves an old hard premise false,
proves the rank strictly above the cutoff, or proves the supplied difference
upper bound by rational interval evaluation with exact additive cancellation.
A separate verifier checks this exhaustive tree. A missing sibling or a split
of an already assigned coordinate is rejected.

**CT05-5 (restricted receiver soundness).** Assume the stated expression
semantics and trusted cache discipline. Every REUSE_CERTIFIED result of the
current receiver bounds the specified difference on all new minimum-ranked
feasible assignments; its reported NONEMPTY status is justified.

**Proof sketch with explicit obligations.** Structural induction proves the
interval evaluator sound, and additive collection preserves expressions by
linearity. Induction over the verified split tree proves the old band bound:
all assignments reach a checked leaf, and assignments in that band cannot be
rejected by a justified hard or strict rank exclusion.

`admit` is the only supported way to add to the trusted cache; it rechecks the
proof against the independently supplied full old record. `derive_substituted`
requires one Boolean expression for each old coordinate, producing a map from
new Boolean assignments to old ones. Substitution commutes with the arithmetic
and Boolean operations by structural induction. Every mapped old hard premise
is either an identical current hard premise or certified true on the whole
new box. Thus the map sends current feasible assignments to the old feasible
family. The current seed is checked against every new hard premise; finiteness
then supplies a nonempty selected family. The grouped-weight inequality proves
the rank drift, and CT05-2 proves coverage. A sound interval for
$`d_1-\alpha(d_0\circ\pi)`$ supplies delta. CT05-1 finishes the proof.

This is a **sufficient** checker, not a complete solver for transport. A true
mapped premise can fail its limited syntactic/interval check. A loose rank
drift or a poor feasible incumbent can make a valid reuse opportunity fail.
Bit substitution does not establish empirical quantity identity, nor infer
which copy of an actor or predictor follows an edit. The reported bound remains
conditional on the explicitly interpreted finite requests and mapping.

The earlier v1 implementation only accepted coordinate permutations and
literal retention of mapped hard rows. Its saved evidence remains v1 evidence.
The v2 extension accepts bounded Boolean substitutions and can repair some
withdrawals through an explicit loss drift rather than declaring every removed
premise inapplicable. For example, an old q=0 proof of 4q-1<=-1 can be mapped
by setting its old q to zero, but the current loss under unresolved q has drift
up to 4. The valid repaired bound is **3, not -1**. Reusing without that
penalty would be false.

This is not execution of the inherited native proof-replay compiler. The
native withdrawal theorem in section 2.1 and its relation to broader proof
portfolios remain distinct from this band-tree prototype. The library trusts
its own private cache memory; imported files must be validated again. It is
not an authenticator for malicious Python objects or untrusted serialized
cache state.

### 8.1 Observed development and resource boundary

The saved v1 corpus contains 160 specified request pairs: 65 yielded a reuse
certificate, each checked against a separate exact point evaluator; 95 were
inconclusive. Inconclusive is not false. The full v1 driver passed 1,451
assertions in seven groups; the separate band/counterpossible supplement passed
48. After changing the implementation, fresh v2 runs passed those same checks,
and a new substitution driver passed 159 assertions. These counts are not
independent discoveries, blind evaluation or reproductions of lost runs.

An illustrative seven-bit parity expression required 255 producer cells for
its initial wide-band proof. A current hard restriction allowed a fresh proof
in 129 cells; a warm reuse used no new proof-tree traversal. The measured
expression-interval visits were 3 warm versus 8,066 for fresh construction plus
admission in the saved v1 case. Full record parsing, syntax collection, memory
and initial construction still cost work. The constant example needs more
collection work through the warm bridge than direct trivial checking.

The parity example has an obvious stronger Boolean simplification. That
shortcut is permitted to ordinary methods, as is the same cache algorithm.
These diagnostics show a functioning cache tradeoff, **not** superiority over
an optimized ordinary solver or a proof that repeated reuse is profitable.
The relevant later benchmark is cost to certify the same action-quality
threshold under matched evidence, access and available shortcuts, including
initial acquisition and retained proof size.

### 8.2 What remains before closing P3-05

The missing earlier clock is still unverified; this session's actual records
must determine how much of Research90 remains. The new mathematical core and
finite checks are present, but this is not a task-closing or contribution gate.
Further task-focused investigation should target joined proof portfolios,
more complete mapped-premise discharge, and whether a useful domain/rank/loss
bridge remains cheaper than recomputation on nontrivial cases **after allowing
ordinary symbolic shortcuts**. A worthwhile null result or precise limitation
would answer that question too. No general performance margin is assumed.

The loss-scaled repeated-edit identity is proved, but an arbitrary directed
unit-conversion graph is not supported by this receiver. General program
refactoring, changing hypothetical consequence rules, and full native
transport need their respective proof contracts. Later learning tasks are not
silently added to P3-05's completion criteria.
