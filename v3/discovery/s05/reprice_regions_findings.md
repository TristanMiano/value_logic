# Uniform regret regions compiled from retained repair proofs

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT. [Implementation](reprice_regions.py) and
[source-bound profiles and invoices](reprice_regions_results.json).
The principal owns the clock. There were **no new solver calls** and no exact
diagnostic optimum entered region selection.

The saved source supports a positive uniform result: six of its sixteen rows
have a nonzero symmetric weight-perturbation box certified by one fixed action
and one retained proof. Ten rows have only radius-zero certificates of this
form at the requested tolerance. The largest individual radius is 1/4; one
common symmetric radius for all sixteen selected certificates is zero.

## Exact regions for a fixed action and proof

Use the immutable hard/soft clauses and the checked archive from
[maxsat_reprice_results.json](maxsat_reprice_results.json). A retained feasible
repair has violation vector u. A retained negative tree has soft-leaf supports
v_l, and proves `L_T(w)=min_l v_l dot w <= C*(w)` for every nonnegative w.
Rows without a negative tree use the valid baseline `L=0`, represented by
one zero support. This keeps rows 4 and 10 in the profile.

For the **fixed repair u**, its archive-derived regret bound is

```text
u dot w - min(L_T(w),p)
  = max( max_l (u-v_l) dot w, u dot w-p ).
```

It is at most tau exactly when both kinds of inequality hold:

```text
(u-v_l) dot w <= tau      for every soft leaf l;
u dot w-p <= tau.
```

For **replacement at p**, the bound is `max(0,p-L_T(w))`. For tau>=0 its
region is exactly

```text
p-v_l dot w <= tau       for every soft leaf l.
```

These are sufficient guarantees about actual regret, and exact conditions for
the selected action/tree bound. They do not assert that the retained lower
profile equals the true changed-weight optimum. Each region is an intersection
of halfspaces in `(w,p,tau)`, restricted to nonnegative weights and price.

Taking the union over archived repair/tree pairs and replacement/tree choices
recovers the pointwise archive gate

```text
min(U(w),p)-min(L(w),p) <= tau,
U(w)=min_u u dot w; L(w)=max_T min_l v_l dot w.
```

Indeed, at any specified weights the finite archive has a minimizing witness
and a maximizing tree, and the cheaper of its repair and replacement actions
attains the left side. Conversely any one pair's admitted action bounds the
archive's best achievable certificate. This is reuse of the entire archived
menu, without a new optimization oracle for the underlying hard problem.

## The maximum box radius for one fixed pair

Here the original positive weights are
`w0=(1,2,3,1,2,3,1,2)`, price `p=6`, and tolerance `tau=1`.
Consider the relative box

```text
w_j=w0_j*(1+e_j), |e_j|<=rho, 0<=rho<=1.
```

For a compiled inequality `d dot w+c*p<=tau`, its exact maximum over the box is

```text
A + rho*B,
A=d dot w0+c*p,
B=sum_j |d_j|*w0_j.
```

Each coordinate chooses its own sign, attaining this support function. Thus a
pair is inadmissible even at the center when any A>tau. Otherwise its greatest
certified radius is

```text
rho_pair = min(1, min_(inequalities with B>0) (tau-A)/B).
```

An inequality with B=0 adds no radius restriction when its center is admitted.
A tight center with B>0 yields radius **zero**, which remains a valid
certificate at w0. The result file distinguishes those zeros from null radii
for center-infeasible pairs.

The compiler maximizes rho_pair over the finite archive menu, using no exact
diagnostic values. This is the **largest box certified by one fixed action
and tree throughout that box**. It need not be the largest box covered by the
union of regions when different certificates can be used at different weights.
No parameter grid is used as a substitute for the uniform inequality proof.

The calculation covers nonnegative real weights, hence all integer weight
edits inside the box too. The earlier solver interface only accepted integer
weights; this extension concerns the algebraic proof profile and does not
claim that its backend accepts noninteger inputs.

## Source-bound profile at p=6 and tau=1

The compiled regions retain each source identity, actual witness model,
violation mask, archived tree index/budget, every leaf inequality, its center
and sensitivity, and a limiting inequality where the radius is below one.
Tree indices and row indices below are zero-based.

| Rows | Fixed feasible action | Selected tree | Maximum fixed-pair radius |
|---|---|---:|---:|
| 0 and 5 | Repair with model 128 | 0 | 1/4 |
| 6 and 12 | Repair with model 16 | 0 | 1/4 |
| 13 | Repair with model 132 | 1 | 1/10 |
| 15 | Replace at price 6 | 2 | 1/6 |
| 1, 2, 3, 4, 7, 8, 9, 10, 11, 14 | Their retained feasible repair, recorded individually | Recorded individually | 0 |

There are 55 action/tree regions: 36 are center-infeasible and 19 admit the
center. The selected original-weight memberships pass for all sixteen rows.
The fifteen selected repair assignments were rechecked against their fixed
hard clauses, and their violation masks were recomputed and matched. The
remaining selected action is the available replacement option. These checks
are separately charged and do not acquire new solver results.

### A concrete 25% certificate

For row 0, model 128 sets Boolean variable 8 true and variables 1–7 false.
It is hard-feasible and violates only soft clause 8, so its cost is w_8.
The selected archived tree has original budget 1 and leaf masks
`[2,3,4,5,9,16,17,24,65,128,129,136]`.

One limiting leaf is mask 2, giving the condition `w_8-w_2<=1`. At the center
its value is zero; its weighted absolute coefficient sum is four. Its exact
box maximum is `4*rho`, so rho<=1/4. Every other inequality in this pair is
also certified at rho=1/4. The repair therefore has regret at most one for
**every independent weight change of up to 25%**, with the clauses and p=6
fixed. This is an actual feasible action and an explicit retained proof pair.

For row 13 the limiting comparison is
`w_3+w_8-w_2-w_6<=1`, with sensitivity ten, giving radius 1/10.
For row 15, tree 2's limiting leaf mask 7 has original cost six. Replacement
requires `6-(w_1+w_2+w_3)<=1`; its worst value is `6*rho`, giving radius 1/6.

### What the zero radii mean

For row 1, a limiting condition is `w_4+w_5-w_2<=1`. It already equals one
at w0 and has sensitivity five, so any positive symmetric box contains a
weight edit that violates this pair's tolerance certificate. Rows 4 and 10
have only nonnegativity as their archived lower proof, and their unit-cost
repairs similarly exhaust the current tolerance.

This does not erase their useful repricing regions. All sixteen rows possess
a center-admitted repair pair. Any such pair remains admitted under uniform
downscaling `w=lambda*w0`, `0<=lambda<=1`: its leaf contrasts scale by lambda,
and its repair-versus-replacement cost only decreases. This fact follows from
homogeneity and is also available to a strong scalar control. The original
[repricing findings](maxsat_reprice_findings.md) additionally show useful
structured edits that a zero symmetric radius does not describe. The full
halfspaces, directional neighborhoods and their union are more informative
continuation targets than replacing a zero radius with an inflated number.

## Paid compilation and membership

The previously paid witness/source compilation was 4,374 units and the
tree rechecking/compilation was 3,601 units. This task reuses those checked
profiles, verifies their source and implementation hashes, and adds:

| Incremental operation tariff | Units |
|---|---:|
| Archive admission and hash processing | 98,117 |
| Region coefficient/radius compilation and pair selection | 20,510 |
| Sixteen original-weight box memberships | 816 |
| Selected feasible-action checks | 953 |
| Total | 120,396 |

Archive admission is large because this prototype reads the full saved JSON
bundles, although only `old_weights` and `compiled_profiles` feed gate selection.
It charges eight-byte input words and SHA-256 message blocks. A compact,
independently bound certificate archive is a concrete cost-reduction option;
the present artifact does not pretend those existing bundles were free to
load. The preceding diagnostic optima are never consulted by the selection
code. Their old diagnostic computation is not a prerequisite for the regions.

After admission and compilation, a cached profile's box membership needs only
source/price/tolerance binding and eight coordinate bounds: **51 named units
per row** here. It returns the certified fixed action and tolerance, rather
than recomputing the complete lower/upper value profile. Consequently this
figure is not an equal-output speed comparison with the earlier full repricer.
The original-weight action checks are one-time profile-admission work.

The measured process time was 18,367,339 ns and wall time 18,377,334 ns for the
read/compile/membership/action-check pass, ending before final JSON serialization.
Those timings include implementation overhead and exact algebraic assertions
not separately itemized in the named operation tariff. Serialization and
delivery add overhead. Service units are operation prices, not currency, and
are not the same units as repair weight, replacement price or regret. No net
economic advantage is inferred from this one profile.

Command: `python v3/discovery/s05/reprice_regions.py`. Existing outputs are
protected from overwrite. The useful continuation is to compare cached box
guards, full polyhedral-region membership, and direct repricing at the same
requested regret duty, while retaining actual feasible actions and paying
for any additional proof acquisition.
