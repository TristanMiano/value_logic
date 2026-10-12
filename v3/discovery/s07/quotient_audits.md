# Quotient audits from checked affine source constraints

**DEVELOPMENT — ChatGPT (GPT-6 Astra Pro), October 12, 2026 UTC.**

This extends [S29's affine construction](s29_affine.md) into a prospective
proof and audit interface. It derives a sufficient objective quotient,
regions where an audit can stop before identifying that quotient exactly,
and a complete small decision tree for a scalable family. No new acquisition,
stream rerun, service modification or principal-clock credit is claimed.
The earlier S29 receipts retain their original tiny-example scope.

## 1. The objective quotient and the remaining replacement scalar

Let F be the nonempty set of original feasible violation vectors in
$`\{0,1\}^m`$. Suppose source-bound receipts prove
$`Az=b`$ for **every** $`z\in F`$, with checked rank r. Choose
a checked feasible witness $`z_0`$ and a full column-rank matrix N
whose columns span $`\ker A`$. There are $`d=m-r`$ columns.

Every repair can be written $`z=z_0+Nt`$. Consequently:

```math
w^\top z=\beta(w)+\pi(w)^\top t,
\qquad
\pi(w)=N^\top w,
\qquad
\beta(w)=z_0^\top w.
```

The quotient coordinate $`\pi(w)\in\mathbb R^{m-r}`$ determines
all repair-to-repair cost differences. Two objectives have the same
quotient precisely when their difference belongs to $`\mathrm{row}(A)`$.
For such a difference $`w-v=A^\top\lambda`$, all repairs shift by
$`b^\top\lambda=\beta(w)-\beta(v)`$.

Thus at most one additional scalar, beta, determines their absolute costs
and their comparison with the fixed replacement price p. The pair
$`(\pi,\beta)`$ is sufficient for every action cost on this logical
source. If b is zero, beta is already determined by pi and there is no
independent additional scalar. A relevant finite cost source can have
still fewer varying directions.

This is a sufficient quotient, not automatically the smallest one. The
actual space of repair differences is
$`D=\mathrm{span}\{z-z':z,z'\in F\}`$. The smallest linear
quotient preserving every pairwise cost difference has dimension
$`\dim D\leq m-r`$. Equality holds if the admitted affine equations
describe the actual affine hull. Proving a complete affine hull can be
expensive. Even different points of that smallest quotient can have the
same optimal action; preserving cost differences is stronger than
preserving the choice needed for one price and tolerance.

Exact rational elimination can check the rank and a basis N. A checker
verifies $`AN=0`$, the two ranks, and $`Az_0=b`$, in addition to
the logical receipts establishing the equations. Dense elimination and
rational bit growth are charged computation. The family below instead has
an explicit sparse basis.

## 2. An audit leaf needs a fixed adequate action

For a source-compatible objective w, write:

```math
V(w)=\min\{p,C^*(w)\},\qquad
\mathcal A_\tau(w)=
\{a:\ c(a,w)-V(w)\leq\tau\}.
```

An audit cell S admits a fixed action at tolerance tau exactly when:

```math
\bigcap_{w\in S}\mathcal A_\tau(w)\ne\varnothing.
```

This is a semantic necessary-and-sufficient condition. A checked lower
method supplies a sufficient certificate for it; failure of that particular
certificate need not mean that the intersection is empty. A deterministic
audit policy is sound if its compatible outcome cells cover the current
source and every terminal cell has one admitted action with such a
certificate. The action may differ between observed leaves, but is fixed
throughout the remaining uncertainty in each leaf.

### Leaves that identify a quotient class

Suppose a cell has fixed quotient c. Select an admissible nonnegative
representative query q with $`\pi(q)=c`$, a paid checked point
lower $`L_q`$, and a checked repair with **unclipped** query cost
$`U_q`$. For the remaining objectives, let
$`\kappa(w)=\beta(w)-\beta(q)`$. The S29 bounds give:

```math
B_R=\max\{0,U_q-L_q,U_q+\kappa_{\max}-p\},
\qquad
B_P=\max\{0,p-\max(0,L_q+\kappa_{\min})\}.
```

Repair is certified when $`U_q-L_q\leq\tau`$ and
$`U_q+\kappa_{\max}\leq p+\tau`$. If $`p>\tau`$,
replacement is certified when
$`L_q+\kappa_{\min}\geq p-\tau`$; if
$`p\leq\tau`$, replacement is already adequate for any
nonnegative repair costs.

Identifying pi alone can therefore be insufficient: one quotient class
may need to be split by the remaining scalar to choose between repair
and replacement. Conversely, complete identification of beta is often
unnecessary. A valid threshold bound is enough.

A canonical linear representative of a quotient class can have negative
coordinates. It cannot be submitted to the existing nonnegative-integer
proof provider without a checked admissible conversion. Selecting an actual
compatible nonnegative representative, or solving for one, is part of the
quoted work.

### Leaves that merge different quotient classes

Suppose several quotient cells all satisfy a uniform certificate for the
same repair and the same replacement comparison. Their union is an
admissible leaf, even if pi is not identified. For an exactly-one pair,
all objectives with $`w_2-w_1\geq0`$ prefer the first repair.
A cell containing quotient differences H and 2H can therefore close
with that repair, provided its replacement bound also closes.

The resulting audit frontier depends on the current price, tolerance,
proof bank and logical source. It can merge distinct quotient classes or
split a single class by beta; it is not globally ordered against the
partition by pi alone. For a general source, an admitted pointwise lower
$`\ell(w)\leq C^*(w)`$ certifies a repair u on S if:

```math
\sup_{w\in S}
\max\{u^\top w-p,\ u^\top w-\ell(w)\}\leq\tau.
```

How that supremum is bounded remains part of the method and its bill.
A few successful points do not certify the cell.

This is the conventional stopping criterion of a minimax decision tree:
collect enough information to select an adequate action. The quotient
supplies a checked sufficient statistic for constructing and merging its
cells; it does not introduce a new general decision-tree optimality claim.

## 3. What a quotient audit is allowed to observe

The existing [CostOracle](../s06/joint_repair.py) supplies a paid coordinate
of one committed cost row. Under that interface, an audit node partitions
the public modes by the returned coordinate value. It must include every
compatible value and retain the actual receipt.

The quotient can change **where the tree stops** or which coordinate it
buys. It does not create a cheaper physical sensor. A new operation that
reports a linear contrast, a quotient-class label, or a threshold on an
aggregate beta would require its own source contract, available observation
channel, truthful-response warrant and price. Computing a contrast from two
already purchased coordinates costs two observations if that is the only
supported access.

Several raw outcomes may share a continuation or a terminal action.
Merging those branches reduces planning or representation work; it does
not refund the physical observations. A coarse state should retain the
original mode IDs and raw receipts, so later prices or logical sources can
reuse the observations without pretending to recover discarded facts.

For product row sources, pi and beta are additive across rows. Grouping
each row's modes by exact projected values avoids enumerating all row
configurations. Preserve the correlation between pi and beta within those
modes. Replacing their joint image by independent marginal ranges is a
conservative outer approximation, not an exact source representation.
An observation of a sum across rows may introduce joint constraints that
the present product representation cannot store exactly.

## 4. Buying an equality can reduce the remaining observation duty

If new source-global equations increase the admitted rank by k, the
sufficient quotient dimension falls by k. Previously distinct objective
classes can merge. The physical source and its true feasible repairs
have not changed; the reasoner has purchased a stronger justification
for ignoring certain cost distinctions.

The equality receipt must bind the original hard clauses, ordered
violation features and active assumptions. For the compact next
implementation, two inexpensive proof forms are enough:

- A hard unit fixes an atomic violation feature to zero or one.
- A hard at-least-one clause and all pair exclusions prove exactly one
  violation in a selected group of distinct atomic features.

Literal polarity is part of the checker. Other soft features may remain
outside the selected group. General clauses need a checked relation
between their actual violation indicators and any introduced variables.

For derived equations, the provider can certify that the original source
conjoined with the equation's negation is unsatisfiable, with a checked
encoding for any pseudo-Boolean arithmetic. A failed entailment query
returns a counterexample; a capped attempt can remain unresolved. A
complete acquisition plan must include those outcomes and their fallback,
or limit its quote to the directly checked source forms. An expected
equality is not admitted in advance to make a bundle appear complete.

A point proof might already support a derivation of a useful equality.
The checked extraction is paid, but its original acquisition is not
bought or credited twice. Likewise, explicit source clauses require real
admission and checking but do not require an unnecessary new SAT call.

### Three scopes that must remain distinct

**Original feasible source.** Equations proved for every original feasible
violation vector support the quotient theorem and true repair ranking
invariance. Equations under temporary assumptions apply only while those
assumptions remain part of the admitted source.

**Retained witnesses.** An equality shared by currently retained repairs
controls their mutual comparisons only. It does not cover unseen feasible
repairs or justify a transported optimum. For example, retained vectors
(1,0) and (0,1) both sum to one, but an unseen feasible (0,0) defeats the
claim that a common positive weight shift raises the optimum by one.

**Tree representations.** An equality of forced-violation leaf masks can
describe an affine change of that particular lower representation when
its own checker proves the arithmetic. It does not prove that complete
feasible repairs obey the equality. With a true repair (1,1) and a valid
partial lower mask (1,0), a common unit weight increase raises the actual
repair cost by two but the mask cost by one. Such a representation-level
identity is not a source-global objective quotient.

## 5. A family with one necessary cost audit and many unnecessary ones

Take any fixed weighted repair problem R with nonnegative integral
weights v, an optimal cost C, and a checked optimal repair r. The nominal
proof described below establishes that value; C is not an unbilled
diagnostic label. Add an independent exactly-one decision pair and n
mandatory violation features. The combined feasible vectors are:

```math
F=\{(x_0,x_1,y,z):
x_0+x_1=1,\ y_1=\cdots=y_n=1,\ z\in F_R\}.
```

The public source declares one decision cost row with modes (0,H) and
(H,0), and n independent mandatory-cost rows with
$`\theta_i\in\{a,2a\}`$, for positive a and H. All auxiliary
weights v are fixed and known. Thus the actual objectives are:

```math
w=(c_0,c_1,\theta_1,\ldots,\theta_n,v).
```

A paid equality receipt proves the decision-pair equation and the n fixed
features, of rank n+1. If R has k soft features, the sufficient quotient
has dimension k+1; only its decision-pair coordinate varies in this
declared cost source. The n mandatory cost directions are outside the
varying repair quotient but still affect the replacement scalar.

Use the nominal query:

```math
q=(H,H,a,\ldots,a,v).
```

Acquire and check a matching point lower and witness upper at
$`H+na+C`$. This point certificate includes real work on R.
It does not follow merely from the displayed added equalities when R
itself has a nontrivial objective. Acquiring an exact point certificate
can require several complete decision calls; a single negative call
suffices only when a suitable incumbent and the relevant successful
proof are actually available. Charge the entire acquisition.

Check both combined repairs made from r and the two decision choices.
For every source mode, the source-support calculation from S29 gives:

```math
\min_{F\text{ relaxation}}(w-q)^\top z
=-H+\sum_i(\theta_i-a).
```

The auxiliary displacement is zero; the decision pair contributes -H
and each mandatory feature contributes its signed change. Hence the
transported lower is $`C+\sum_i\theta_i`$, exactly matched by the
combined repair selecting the zero-cost decision feature.

A single ordinary coordinate audit of the decision row returns 0 or H.
Each child selects that repair. If the **known shared replacement price**
satisfies:

```math
p\geq C+2na,
```

both children have uniform regret zero. None of the n mandatory rows
needs an observation. Each leaf retains $`2^n`$ compatible original
cost configurations.

With strict inequality in that price condition, replacement has positive
regret in some compatible source, and any fixed repair chosen without
the decision audit has regret at least H in the opposite decision mode.
Thus no fixed zero-regret action can be supplied without learning that
decision distinction. Logical work on the same immutable source cannot
reveal the independent hidden bit.

Complete identification of all row modes using the stated coordinate
channels takes n+1 observations. The construction takes one. This is a
comparison with full identification, **not** a lower bound on what a
strong ordinary decision method must buy. Ordinary preprocessing and
the same quotient calculation also take one audit.

For a numerical illustration only, take n=2, a=1, H=3 and an auxiliary R
with a checked optimum C=2. The nominal paired certificate is at 7,
so an appropriate negative proof is at budget 6. At p=9, the selected
repair's cost ranges from 4 to 6. One decision audit leaves four cost
configurations unresolved and certifies zero regret. This arithmetic
illustration has not been executed as a new acquisition.

### Further coarsening beyond exact quotient identification

Replace the decision row by four modes:
(0,H), (0,2H), (H,0), (2H,0), and use nominal pair weights (2H,2H).
One audit of the first coordinate has outcomes 0, H and 2H.
Outcome 0 leaves **two different quotient values**, H and 2H, yet the
first repair is optimal in both. The other two raw outcomes choose the
second repair. The same high-price condition removes the mandatory
cost duty. Thus complete audit leaves can stop strictly before quotient
identification as well as before full mode identification.

## 6. An inexpensive complete tree when replacement is competitive

After k mandatory rows have been audited, let h be the number with high
value 2a. For the remaining mandatory total T:

```math
T_{\min}=na+ah,
\qquad
T_{\max}=na+a(h+n-k).
```

The optimum repair cost is C+T and is independent of the hidden decision
bit. For $`0\leq\tau<H`$, replacement is certified if
$`C+T_{\min}\geq p-\tau`$. A decision audit can deliver a
certified repair if $`C+T_{\max}\leq p+\tau`$.

When $`p\leq C+na`$, replacement closes at zero tolerance without
even buying the decision audit. When $`p\geq C+2na`$, one decision
audit closes. Between these thresholds, audit the common repair cost
only until a sufficient threshold is established; buy the decision
audit only on a repair leaf.

For equal complete mandatory-audit price A and decision-audit price D,
define the following worst-cost recursion after the proof bank is admitted:

```math
J(k,h)=\min\left\{
\begin{array}{ll}
0 & \text{if }C+T_{\min}\geq p-\tau,\\
D & \text{if }C+T_{\max}\leq p+\tau,\\
A+\max\{J(k+1,h),J(k+1,h+1)\}
  & \text{if }k<n.
\end{array}\right.
```

Unavailable alternatives are omitted. At k=n at least one terminal
alternative applies, so the recursion is complete. There are only
$`(n+1)(n+2)/2`$ count states. Their equality follows from the
proved mandatory-feature symmetry, the independent binary supports and
the equal observation tariff; raw row identities still remain in the
actual receipts.

This is exact finite minimax planning for the stated audit menu and
certificate conditions. An early decision audit cannot improve its
worst cost: it gives no information about T or the replacement test.
Its two branches have identical future mandatory-cost problems up to
relabeling the two repairs. Defer it to whichever terminal branches
actually return a repair. Other channels, unequal row prices, additional
logical purchases or correlated modes require a different state space
or a new argument.

The recursion is a constructive complete quote, not a calibrated model
of outcomes. It uses a maximum over both replies. Logical acquisition,
table construction, source checking, updates and retention are additional.
If A and D cover only external observation tariffs, carry every remaining
local, CPU and storage charge explicitly; do not present J as an all-in
economic deadline.

## 7. A concrete next interface and its comparison

A compact new version can expose the following boundaries:

```text
admit_affine(source, assumptions, feature_map, raw_derivations)
    -> checked A, b, receipt dependencies

compile_quotient(affine_receipts, checked_feasible_witness)
    -> exact N, rank evidence, transform identity

quote_audit_frontier(cost_source, current_raw_mode_sets,
                     allowed_channels, proof_bank, price, tolerance)
    -> complete outcome cells, fixed leaf actions, proof dependencies,
       maximum path invoice and remaining unpriced resources

observe_and_recheck(raw_audit_receipt, quoted_node)
    -> remaining original modes and a checked child cell

certify_leaf(child_cell, geometry, original_query_receipts, witness)
    -> source-bound fixed action and uniform bound, or unresolved
```

The next small implementation should support the explicit unit and
exactly-one proof forms, use the existing coordinate channels, and
realize the count-state recursion. It needs new versioned files; the
one-group S29 constructor is not already this interface. Quote and
execution must use the same source identities and include unsuccessful
or interrupted purchases.

Let the one-time bill include source admission, equality acquisition and
checking, the paired q certificate, both witness checks, quotient
compilation, planning and retention. A complete policy adds the actual
observation/check/output path and its separately stated resource caps.
Proving the equalities can cost more than the n skipped observations.
The inequality comparing those full bills is an explicit symbolic
price region until actual tariffs and measurements are supplied.

The strong control is an ordinary robust decision method supplied the
same checked constraints, source modes, sensors, point evidence and
output tolerance. It can perform the same elimination and stop at the
same action regions. Persistent preprocessing is a required comparison;
the [existing primary-source bridge](../s05/reprice_sources.md) records
the relevant CP 2021 and SAT 2022 methods. The
[regret-elicitation source record](../s06/acquisition_sources.md) supplies
the conventional minimax and finite-lookahead context.

Useful follow-up evidence would show that acquiring and retaining these
source constraints pays for itself on repeated requests, or that the
compiled complete frontier is cheaper to quote than an equally informed
ordinary implementation. This note supplies neither result. It supplies
a scalable, fully specified observation reduction relative to identifying
the whole source, an explicit paid route to its logical premise, and
a concrete next controller with strong ordinary ties left visible.
