# A Hybrid ReLU Architecture for Value Logic

Created: 2026-07-14
Task: TODO Task 16
Status: reference architecture fixed; representation results completed in Task 17; training objective completed in Task 18

## Executive decision

The reference system is a **ReLU statistic scorer inside a symbolic license machine**, not an end-to-end license classifier.

```text
exact request and finite record
    -> symbolic WF and dependency projection
    -> ReLU statistic/payload/grade proposals
    -> separately calibrated and checked envelopes
    -> exact atom diagnostics and K_3 values
    -> profile meet and four-way public outcome
    -> exact active mask
    -> separately declared selection or fallback.
```

For scalar risk atoms, the learned default is a center plus nonnegative predicted half-width and an uncertainty score. A named calibration procedure supplies an externally checked error radius. Their conservative region yields two signed margins:

```text
m_support = epsilon - upper(U_safe),
m_refute  = lower(U_safe) - epsilon.
```

The decoder supports at `m_support>=0`, refutes at `m_refute>0`, and otherwise stays open, subject to the certificate mode's permitted polarity. ReLU can expose positive normalized surplus

```text
z=ReLU(m_support/sigma),
```

but the interpretation comes from the construction of `m_support`, not from
ReLU. For an arbitrary preactivation, `z>0` means only that the preactivation is
positive. For a learned point margin it means predicted positive slack. Only
when `m_support` is computed from the accepted conservative envelope does
`z>0` mean strict certificate-relative surplus for this named atom and scope.
Even then it is neither target-world truth nor a full profile license. Also,
`z=0` does not distinguish supported equality from open, refuted, missing,
invalid, or conflicted evidence. The signed margins, diagnostic, support bit,
validity state, exact address, and evidence handles therefore remain available.

The architecture admits the author's dual-use intuition in a deliberately narrow way. Named hypothesis channels with common normalization and accepted calibration may use `z_i` both as positive certificate-relative slack and as an input to a declared downstream computation. That computation is itself a plan to be evaluated. Arbitrary hidden units receive no adequacy interpretation, and variable expert payloads are not multiplied by margin magnitude as a semantics-free gate.

This task fixes the construction. Task 17's [`03_representation_theorems.md`](03_representation_theorems.md) now proves the exact CPWL, robust decoding, seam, expandable-library, joint-sufficiency, and annotated-plan claims at their scoped strengths. Task 18's [`04_losses.md`](04_losses.md) now selects standardized center–radius training, held-out residual calibration, the atom-classification baseline, and the separate router objective.

## 1. The system boundary

### 1.1 Exact side packet and numerical view

Task 15 defines the atom input

```text
x(s,e,q,a)=(a,pi_a),
pi_a=Env(s;e,q)|R_s((s,e,q),a).
```

The parser produces:

```text
chi_a    exact symbolic side packet
u_a      finite numerical/categorical vector presented to the scorer.
```

`chi_a` retains the exact address, task/domain/frame, loss and risk functional, tolerance and units, fallback, comparison set, certificate mode, currentness/conflict state, checker and calibration versions, loss-estimator identity, registry identity, provenance handles, and profile roles. Some of those fields may also have embeddings in `u_a`; their embeddings never replace the exact values used by the decoder and auditor.

The system checks `WF(s,e,q,P)` before meaningful atom assessment. If `WF` fails, the public result is `Undefined` with `WFDiag`; neural output is ignored. Missing evidence after a well-formed request is instead an open diagnostic.

### 1.2 Three trust levels

The implementation distinguishes:

1. **proposal:** a neural output such as a risk center, spread, uncertainty score, payload, or grade;
2. **accepted envelope or certificate:** a versioned external result showing what error, coverage, scope, and polarity may be relied upon; and
3. **decoded judgment:** the exact diagnostic and `K_3` value obtained from the accepted evidence and boundary rules.

A proposal can be numerically accurate without being accepted evidence. A predicted uncertainty is not its own calibration record. A grade can lie below a tolerance without proving that the grade is valid. These separations remain even when the scorer, calibrator, and decoder are packaged into one deployed system.

## 2. ReLU scorer and output heads

Let `rho(t)=max(0,t)`. For a statistic schema `sigma(a)`, the learned core is an ordinary finite MLP:

```text
h^0 = u_a,
h^ell = rho(W_ell h^(ell-1)+b_ell),    ell=1,...,L,
o_a = A_sigma h^L+c_sigma.
```

The affine output is split by a schema registry rather than interpreted as one anonymous vector.

| head | reference parameterization | semantic status |
|---|---|---|
| statistic center | `c_hat=o_c` | learned proposal |
| predicted half-width | `r_hat=ReLU(o_r)` | nonnegative proposal, not calibration |
| uncertainty/calibration score | `q_hat=o_q` or `ReLU(o_q)` according to its target | input to a separately fitted/versioned calibration map |
| learned validity/OOD score | `v_hat=o_v` | conservative reject signal only |
| computational payload | `y_hat=A_y h^L+c_y` | proof-erased content for the declared plan |
| quantitative grade | typed affine, paired-signed, or nonnegative ReLU heads | proposed error/resource bound, separate from its evidence |
| selection utility | optional separate head | ranking input after the exact active mask; never a license |

Not every atom uses every head. A formally checked trace may use no learned statistic. A pure adequacy scorer need not produce a payload. A plan node may use payload and grade heads but no comparison head. Separate modules may share a trunk where their input types match; the architecture does not require one network to predict every core and atlas extension.

### 2.1 Why center-radius is the default

Directly predicting support, open, and refutation logits creates three avoidable problems: contradictory atom heads, hidden boundary conventions, and no reusable quantitative region. The reference instead predicts

```text
U_hat=[c_hat-r_hat,c_hat+r_hat].
```

Let a named calibration map and checker provide a nonnegative accepted error radius `eta` under exact scope, assumptions, version, and polarity. The conservative region is

```text
U_safe=[c_hat-r_hat-eta,c_hat+r_hat+eta].
```

`eta` is not whatever the network says its error is. It is the output of the declared calibration/certification path applied to the relevant proposal and group, with an exact record pointer in `chi_a`. If that record is absent, expired, conflicted, out of scope, or checker-rejected, `U_safe` cannot support or refute the atom.

Center-radius guarantees ordered scalar endpoints and remains compatible with ReLU's piecewise-affine arithmetic. Direct endpoint heads are allowed if the external layer verifies `lower<=upper`. Non-scalar ordered risk spaces use a schema-specific region representation and exact relation decoder; they are not silently reduced to this interval.

### 2.2 Evidence polarity

An accepted region may justify both support and refutation, only support, or only refutation. For example, a certified upper bound may establish `risk<=epsilon` but supply no valid lower bound for concluding failure. The mode registry therefore contains

```text
can_support(m), can_refute(m).
```

If the numerical region lies wholly on a polarity the mode does not certify, the decoder returns open with `CertificateModeCannotSupport` or `CertificateModeCannotRefute`. The architecture never turns a one-sided guarantee into a two-sided fact.

## 3. Exact atom decoding

### 3.1 Scalar upper-risk atom

For acceptable region `(-infinity,epsilon]`, define

```text
m_support = epsilon-upper(U_safe),
m_refute  = lower(U_safe)-epsilon.
```

After the exact evidence gate succeeds:

```text
m_support >= 0  and can_support -> supported
m_refute  >  0  and can_refute  -> refuted
otherwise                       -> open.
```

The order is consistent: a nonempty interval cannot be wholly at or below `epsilon` and strictly above it. At `U_safe={epsilon}`, support obtains inclusively while

```text
ReLU(m_support)=0.
```

Consequently the channel bundle retains

```text
(m_support,
 m_refute,
 ReLU(m_support/sigma),
 ReLU(-m_support/sigma),
 exact K_3 diagnostic,
 exact validity/evidence references).
```

The paired ReLU channels reconstruct signed support slack, but even they do not determine status without the refutation margin, evidence state, polarity, and inclusive boundary rule.

### 3.2 The error-buffer special case

For a point estimate `J_hat` with an accepted two-sided error bound `delta`, set

```text
U_safe=[J_hat-delta,J_hat+delta].
```

Then

```text
J_hat+delta <= epsilon -> support
J_hat-delta >  epsilon -> refutation
otherwise              -> open.
```

The width-`2 delta` estimate-space uncertainty band is a deliberate open region. Task 17 generalizes it: raw affine margin error is `r`, conservative decoding is sound, and uniform recovery of the ideal decision is guaranteed outside the `2r` ideal-margin band.

### 3.3 Fallback improvement

For candidate and fallback regions `U_e,U_F` under the same criterion and units,

```text
m_support^F = lower(U_F)-(upper(U_e)+Delta),
m_refute^F  = (lower(U_e)+Delta)-upper(U_F).
```

Support uses `m_support^F>=0`; refutation uses `m_refute^F>0`; overlap is open. Both evidence paths, identities, scopes, and calibration/checker records remain in the diagnostic. A good candidate score cannot compensate for missing fallback evidence. This preserves the motivating “better than status quo” threshold as its own atom rather than folding it into hard adequacy.

### 3.4 Trace and comparison atoms

Trace status remains checker-derived. A neural trace-completeness or anomaly score may conservatively request review, but cannot accept its own trace.

Comparison uses shared candidate or pair scorers only to propose quantitative evidence. Exact candidate identity, `K`, eligibility, search-view validity, pair certificates, and mode remain symbolic. A valid certified dominator may refute immediately. Supporting `RelUndom` still needs a valid declared search over exact `K`; supporting `CertUndom` still needs every relevant pair resolved or ineligible. A dense learned dominance matrix is not an alternative proof of search completeness.

### 3.5 Learned validity is one-way

Let `Reject_theta(x)` be an OOD or learned-validity predicate using the declared threshold. The effective evidence gate is

```text
exact evidence usable AND not Reject_theta(x).
```

Thus a learned reject may change a would-be support or refutation to open. A favorable validity score cannot change missing, expired, conflicted, checker-rejected, or uncalibrated evidence into support. This asymmetric use prevents a validity head from becoming a disguised self-certificate.

## 4. Symbolic aggregation, diagnostics, and safety

For every instantiated address, the external decoder emits exactly one dependent-sum constructor:

```text
Support(a,witnesses,provenance)
Open(a,obstacles,provenance)
Refute(a,counterwitnesses,provenance).
```

The profile layer then computes:

```text
value_P = meet {nu(a): a in Req(P)},
Assess = Undefined if not WF
         Refused   if value_P=-
         Withheld  if value_P=?
         Granted   if value_P=+.
```

Report-only diagnostics and the complete address map remain available. `Alarm` and `PendingSafety` are exact projections of safety-address diagnostics, not neural classes. Invalid, missing, expired, conflict, boundary, and polarity-mismatch states retain distinct obstacles even when several of them produce the same open `K_3` value.

The production architecture has no aggregate-status head and no flat reason classifier. Such heads may be trained only as disconnected ablations to measure contradictions, information loss, or baseline accuracy. Their predictions cannot override the atom map or supply the public outcome.

## 5. Annotated plan nodes

For a Task 14C node `v`, the ReLU module consumes the node's numerical view and produces a proposal

```text
N_theta(v,x)=(y_hat_v,g_hat_v,q_hat_v,v_hat_v),
```

while the exact side packet retains:

```text
operator and version
input/output types, ports, frames, and metrics
grade schema, units, validity tube, and resource aggregators
certificate/checker/version/assumptions
provenance sources and dependency rank
loss-estimator identity/version, when present.
```

The output channels are:

1. **payload:** prediction, transformed object, route tag, estimate, or other ordinary computation;
2. **quantitative grade:** error, risk-to-go, coverage, or typed resources;
3. **validity/missingness:** exact state plus optional learned reject proposal; and
4. **certificate/provenance:** opaque checked references, never inferred from grade magnitude.

Payload and grade may share hidden features, but their output schemas remain separate. Nonnegative resource bounds may use ReLU heads. Signed quantities use affine or paired channels. Resource types are not concatenated and summed merely because they occupy one vector.

### 5.1 Two certification routes

The root can be handled in either of two explicit ways:

- **direct composite:** predict/evaluate the root payload and grade and attach an independently accepted root certificate; or
- **propagated composite:** attach accepted local envelopes and use Task 14A/14C's declared grade and certificate transformers along the typed DAG.

For the path-sensitivity instance,

```text
b_v=delta_v+sum_(u in pred(v)) L_(u,v)b_u.
```

If sensitivities are fixed certified constants, this grade update is affine in the local bounds. If both sensitivities and bounds vary, their products are not automatically CPWL and are not silently assigned to the ReLU theorem. The external transformer may compute them, or Task 17's theorem requires a CPWL grade map or controlled approximation with a verified envelope.

Component licenses are never met to produce a composite license. The composite diagnostic consumes the checked root claim produced by one of these two routes.

## 6. Fixed-library ReLU design

Fix a registry

```text
K_0={e_1,...,e_n}
```

and a finite address/output schema `A_0`. A fixed baseline uses

```text
F_theta^fixed:R^d -> R^(n times p)
```

or one shared trunk with `n` registered affine head blocks. The exact registry maps every block to its plan, atom schema, units, calibration group, and evidence/checker path. Pair outputs, if included densely, have registered `(i,j)` axes and quadratic size.

Advantages are simplicity, fixed tensor shapes, and direct simultaneous/empty-set evaluation. Limitations are equally explicit: candidate `e_(n+1)` has no output block; permuting the registry requires permuting inputs/heads/outputs together; and a memorized ID embedding has no guaranteed cold start.

The fixed architecture still derives all statuses symbolically. Its `n` statistic blocks are not `n` grant logits.

## 7. Candidate-conditioned shared ReLU design

For a variable external registry, use a shared ReLU scorer

```text
F_theta^cand(
  phi_E(e_i), phi_Q(q), phi_A(a_i), phi_X(pi_i)
) -> (statistic_i,uncertainty_i,validity_i,payload_i?,grade_i?).
```

The exact plan/address packet travels beside each embedding. Applying the same function candidate-by-candidate makes the learned outputs equivariant to candidate order. Exact identities are restored before decoding and selection.

Pair evidence uses an on-demand shared scorer

```text
G_theta^pair(e_i,e_j,q,pi_ij) -> pair statistic/envelope proposal.
```

A permutation-invariant set summary may be supplied through an external sum/max/set reducer when comparison context requires it, but that summary does not replace exact `K`. Evaluating only edges `E_K` costs `Theta(n+|E_K|)` at the interface. The semantic evidence obligation remains linear for one fully certified candidate and potentially quadratic for all candidates.

Shared parameters permit evaluation of a new candidate representation; they do not guarantee calibration, semantic coverage, or lossless storage of an indefinitely growing independent library. Those are empirical and capacity questions.

## 8. Hypothesis-indexed dual-use channels

### 8.1 Channel registry

Fix a finite named hypothesis set `H={1,...,k}`. Every channel has an exact registry entry

```text
H_i=<
  hypothesis and atom address,
  domain/case interface,
  target statistic and loss units,
  positive normalization sigma_i,
  common normalization semantics N,
  certificate mode and calibration/checker versions,
  downstream consumer set C_i
>.
```

All channels compared or combined by one consumer must share the same consumer context and normalization semantics. The raw `sigma_i` may differ when it converts each margin to the same unitless meaning—for example certified standard-error units or a declared fraction-of-tolerance scale. “All outputs are real numbers” is not a common scale.

For a supported upper-risk address, define the accepted normalized margin

```text
m_i=(epsilon_i-upper(U_i^safe))/sigma_i,
z_i=ReLU(m_i).
```

If the evidence gate fails, `m_i` has no accepted adequacy meaning. The numerical implementation sets its downstream `z_i` to zero and exposes the non-supported diagnostic and validity bit. If the gate succeeds, `z_i>0` means only strict positive normalized support surplus for this registered atom; supported equality still has `z_i=0`, and the remaining required atoms may still block the profile license. The complete channel is therefore

```text
(z_i,b_i,m_i^signed,Diag_i,certificate/calibration handles),
b_i=1 exactly when the atom is supported.
```

At the inclusive boundary, `(z_i,b_i)=(0,1)`. For open or refuted evidence, `b_i=0`, with the diagnostic distinguishing the cases. The ReLU scalar alone is never the whole logical code.

### 8.2 Downstream construction

The declared consumer may use `z` in a later ReLU computation:

```text
h_next=ReLU(W_z z+W_b b+W_c c+b_next),
```

where `c` contains any separately required payload/content features. In this construction, `z_i` has two roles:

- its positive magnitude is normalized certificate-relative adequacy slack; and
- that same number is a feature used by the named downstream plan.

This supplies the architecture requested by the project author. Task 17 proves that the exact-state-plus-normalized-surplus code is jointly sufficient and minimal for the coordinate-complete named-channel family, while general consumers still require the kernel test and obstruction cases. The consumer weights and outputs are part of a versioned plan that must itself be evaluated.

### 8.3 Classifier example

For channels named

```text
flower, dog, cat, food, person, child, house, ...
```

use class-specific adequacy addresses under one image domain, one class-statistic convention, one normalization semantics, and a shared or explicitly comparable calibration mode. A vector

```text
z=(0,0.2,0.2,0,5,3,0.1,...)
```

then means that `person` has the largest positive normalized surplus among the displayed supported hypotheses. It may be processed by the next feature layer. It does not by itself mean highest posterior probability, exclusive truth, or global optimality. Several hypotheses may remain supported simultaneously.

An `argmax` may be a declared label-selection policy only after the full required profile produces an exact active mask. It returns a selected label, not a new adequacy fact. Boundary ties need an explicit rule; an empty active set returns the named unknown/defer/fallback action.

### 8.4 Worked toy: one plan, three requirements

This example is the canonical reader-facing witness for the sign semantics. A
candidate plan `M` is considered for one fixed domain and request. Its required
profile is the conjunction

```text
P = A and I and C,
```

where

```text
A: expected task loss J(M) <= 0.20,
I: J(M) <= J(F)-Delta = 0.35-0.05 = 0.30,
C: latency T(M) <= 50 ms.
```

`A` is an adequacy atom, `I` is improvement over the fallback, and `C` is a hard
constraint. Supporting `A` alone does not give the full license. Nor does the
full license imply that `M` is true, globally best, or selected; it says only
that this plan presently satisfies every required atom under the named evidence
and context.

The levels are therefore:

1. **Predicted adequacy:** the learned statistic lies on the favorable side of
   the threshold; this can be wrong and is not yet accepted evidence.
2. **Certificate-relative atom support:** accepted evidence conservatively
   supports `A` (or another individual atom).
3. **Full profile license:** the request is well formed and every atom required
   by `P` is supported. This is the `Granted` status for the fixed use plan.
4. **Selection/use:** a later policy chooses among fully licensed plans, or uses
   the fallback. Licensing does not force selection.

#### Accepted intervals and two signed margins

For a scalar upper-bound atom with threshold `t`, accepted interval
`U=[lower,upper]`, and registered positive scale `sigma`, retain both

```text
s_support = t-upper,
s_refute  = lower-t,
z_support = ReLU(s_support/sigma),
z_refute  = ReLU(s_refute/sigma).
```

Subject to valid evidence and its permitted polarity, the exact decoder uses

```text
Supported  when s_support >= 0,       # inclusive boundary
Refuted    when s_refute  > 0,        # strict counter-side separation
Open       otherwise.
```

The signed quantity `s_support` is **slack**: it is a distance from the support
boundary in the original units and can be positive, zero, or negative. In this
project, **surplus** names the normalized positive part `z_support` after the
interval and evidence mode have been accepted. Thus positive slack and surplus
refer to the same favorable direction, but they are not quite synonyms:
surplus emphasizes the rectified, normalized number safe to expose to a named
downstream consumer. Neither is a full license.

Suppose the accepted envelopes are

```text
U_J = [0.14,0.18],       sigma_J = 0.01,
U_T = [43,47] ms,        sigma_T = 1 ms.
```

Then

```text
                 s_support/sigma     s_refute/sigma     z_support
A: loss <= .20          2                   -6               2
I: loss <= .30         12                  -16              12
C: time <= 50           3                   -7               3
```

All three exact atom states are `Supported`, and the normalized support-surplus
vector is

```text
z = (2,12,3).
```

The same accepted loss interval supplies both `A` and `I`. The architecture
therefore does not need one independently learned interval or status head per
logical atom. It does, however, need more than one **information channel** for
the full semantics. The interval has two endpoints (or center and radius); the
fixed decoder derives separate support and refutation margins; rectification
produces two ReLU channels; and exact state, validity, and missingness remain
beside them. “Several channels” and “several learned heads” are not the same
claim.

#### What negative, zero, open, refuted, missing, and invalid mean

Holding the adequacy threshold at `0.20` and `sigma_J=0.01` gives the complete
boundary picture:

| evidence for `J(M)` | normalized `s_support` | normalized `s_refute` | exact state | `z_support` | diagnostic reading |
|---|---:|---:|---|---:|---|
| accepted `[0.14,0.18]` | `2` | `-6` | `Supported` | `2` | strict positive support slack |
| accepted `[0.17,0.20]` | `0` | `-3` | `Supported` | `0` | supported exactly at the inclusive boundary |
| accepted `[0.18,0.22]` | `-2` | `-2` | `Open` | `0` | interval crosses the boundary |
| accepted `[0.23,0.25]` | `-5` | `3` | `Refuted` | `0` | counter-side interval is strictly separated |
| no evidence record | not semantically defined | not semantically defined | `Open` | stored as `0` only after masking | `Missing` |
| expired/rejected record | untrusted even if numerically favorable | untrusted | `Open` | forced to `0` downstream | `Invalid/expired` |

A negative support margin is not itself a logical state. Both the open interval
and the refuted interval have negative `s_support`; the separate refutation
margin and exact evidence state distinguish them. `Missing` and `Invalid` are
diagnostic reasons for an open atom, not numerical forms of zero.
`Refuted` likewise means that accepted counter-side evidence supports violation
of this atom at this stage; it is not a declaration of final metaphysical
falsehood.

Negative values remain useful. A signed negative `s_support` records distance
from established support and can be used for diagnostics, boundary-aware
training, prioritizing new evidence, or sensitivity analysis. It can be passed
through an affine coordinate directly or retained in paired ReLU form

```text
s_support = ReLU(s_support)-ReLU(-s_support).
```

But `ReLU(-s_support)>0` means only support shortfall. It does not mean
refutation; the open row demonstrates why the distinct `s_refute`, evidence
polarity, and exact decoder are required.

Consequently, a rectified zero has no unique semantic reading. It can accompany
supported equality, an unresolved interval, a refuted atom, missing evidence,
or invalid evidence. The exact state and diagnostic determine which case is
present.

Even the **pair** of rectified values is insufficient. Under the inclusive
boundary convention,

```text
strict support      -> (z_support>0, z_refute=0),
strict refutation   -> (z_support=0, z_refute>0),
boundary support    -> (0,0),
open interval       -> (0,0),
missing/invalid     -> (0,0) after masking.
```

Thus two ReLU channels expose positive evidence on either side, but they do not
by themselves encode the three-valued atom or its evidence condition. At least
the exact support/state information is additionally required for logical
status, and validity/missing diagnostics are additionally required for audit.

#### Encode the logical statement as a vector

Use exact one-hot atom states

```text
Supported = (1,0,0),
Open      = (0,1,0),
Refuted   = (0,0,1).
```

For audit preservation, one possible fixed-request vector is

```text
v = [WF
     | state_A | state_I | state_C
     | valid_A,valid_I,valid_C
     | missing_A,missing_I,missing_C
     | m_support_A,m_support_I,m_support_C
     | m_refute_A,m_refute_I,m_refute_C
     | z_support_A,z_support_I,z_support_C
     | z_refute_A,z_refute_I,z_refute_C].
```

Here `m_support=s_support/sigma` and `m_refute=s_refute/sigma` retain the signed
normalized margins. Missing or invalid rows use a declared masked placeholder
or sentinel for these coordinates; `valid` and `missing` make clear that the
placeholder has no margin semantics.

For the strictly supported envelopes above,

```text
v = [1
     | 1,0,0 | 1,0,0 | 1,0,0
     | 1,1,1
     | 0,0,0
     | 2,12,3
     | -6,-16,-7
     | 2,12,3
     | 0,0,0].
```

This is intentionally redundant. The one-hot states answer the logic query;
validity and missingness preserve why a state is usable or open; the signed
margins retain favorable and unfavorable boundary distances; and the surplus
coordinates retain nonnegative numerical room for downstream computation. A
status-only consumer could use a smaller quotient, but it would lose audit and
quantitative information.

#### A simple exact ReLU operation on the vector

Let `b_A,b_I,b_C` be the exact `Supported` coordinates and let `WF` be binary.
For this fixed four-bit input, a ReLU computes conjunction exactly:

```text
g = ReLU(WF+b_A+b_I+b_C-3).
```

Because the inputs are exact bits, `g=1` iff the request is well formed and all
three atoms are supported; otherwise `g=0`. In the displayed vector,

```text
g = ReLU(1+1+1+1-3) = 1.
```

This `g` is the grant bit for this already fixed request, not the complete
license object: the latter also names `M`, domain, task, profile, stage,
evidence, and provenance. The full one-hot vector remains necessary to
distinguish the other public outcomes:

```text
WF=0                         -> Undefined/ill formed,
WF=1 and any required R      -> Refused,
WF=1, no R, and some O       -> Withheld,
WF=1 and every required S    -> Granted.
```

The boundary row demonstrates why raw ReLU zero cannot replace the exact bit.
If `A` is supported at equality, then `b_A=1` but `z_support_A=0`, so `g` can
still equal `1`. If `C` is missing, then `state_C=Open`, `b_C=0`,
`missing_C=1`, and `g=0`; this is `Withheld`, not `Refused`.

#### Use surplus in a later computation without letting it grant

Suppose a declared post-license ranking plan computes

```text
r_raw = ReLU(0.5 z_A + 0.1 z_I + 0.2 z_C - 1).
```

For `z=(2,12,3)`,

```text
r_raw = ReLU(1+1.2+0.6-1) = 1.8.
```

This illustrates genuine dual use: the same certificate-relative surplus
coordinates quantify room inside their atom boundaries and feed a later
numerical computation. But `r_raw` cannot grant the plan. If latency evidence
is missing, `z_A` and `z_I` can still make `r_raw` positive. The selector must
first require exact `g=1` (or equivalently restrict itself to the exact active
set); otherwise it reproduces the falsified positivity-as-grant error. A
positive ranking value ranks only already licensed candidates.

#### Does this require more than one neural head?

First distinguish three implementation notions:

- a **learned head** is a parameterized output map trained from data;
- an **output coordinate/channel** is one scalar carried by that map or by the
  decoder; and
- `ReLU(s_support/sigma)` and `ReLU(s_refute/sigma)` are fixed derived
  operations once the interval, threshold, and scale are supplied. They are not
  necessarily learned heads.

More than one semantic channel per atom is generally required by this
audit-preserving interface. More than one independently learned head per atom is
not. This is not an information-theoretic lower bound on arbitrary real codes:
a single scalar could encode three finite labels by convention, but it would not
simultaneously retain the accepted interval, signed distances, boundary case,
and evidence diagnostics used here.

This toy can use one vector-valued neural head

```text
(center_J, proposed_radius_J, center_T, proposed_radius_T, optional_payload),
```

or separate loss, latency, and payload heads. `A` and `I` reuse the same loss
coordinates with different thresholds. If heteroscedastic center and radius are
both learned, the loss statistic needs at least two learned **coordinates**, but
they may be emitted by one head. If the radius comes entirely from external
held-out calibration, only the center need be learned for that statistic.

Held-out calibration and an external checker turn proposed regions into
accepted envelopes. The two signed margins and their two ReLU channels are then
deterministic calculations. The state one-hots, validity/missing diagnostics,
profile conjunction, grant bit, active mask, and fallback are exact derived
quantities, not learned heads. A payload head is needed only if the plan must
also produce a prediction or action, and its payload remains distinct from the
adequacy surplus.

A direct `K_3` classifier could instead use three logits per atom. That is the
Task 18 baseline: it represents a predicted status distribution, but without
the interval/evidence machinery it does not preserve tolerance transfer or
manufacture a certificate. Whether separate learned center/radius/status heads
optimize better than one shared vector head is an empirical architecture choice,
not a logical theorem.

The requirement is therefore **separate information and authorization paths**,
not a fixed head count. One physical output layer may contain several typed
coordinates, one learned statistic may serve several logical atoms, and one atom
still requires several exact/derived channels to preserve its complete state.

### 8.5 Default comparison: separate content and grade

The safer general interface is

```text
(payload_i,grade_i,diagnostic_i,evidence_i)
```

with the selector routing the whole payload of a licensed plan. This preserves different predictions, costs, or traces at equal adequacy margins and is the default for scientific models and recursive plans.

The dual-use form is appropriate when a named downstream computation genuinely consumes normalized margin features. A fixed outgoing column `w_i z_i` is part of that declared downstream network. Multiplying a variable expert payload `y_i(x)` by `z_i`, or using margin as a mixture weight, creates a different generally non-CPWL computation with altered units and boundary behavior. It is forbidden unless that combined plan and its calibration/risk are separately specified and licensed.

### 8.6 Scale covariance obligation

Under a joint positive rescaling of risk, tolerance, and error bounds by `lambda`, license status is unchanged while the raw margin is multiplied by `lambda`. Either normalization must transform as

```text
sigma_i' = lambda sigma_i,
```

so `m_i` is invariant, or the downstream consumer must declare the corresponding covariance. Otherwise equal semantic requests in different units produce different computational behavior.

## 9. Licensing before selection

Let

```text
A_P(s,q,x)={e in K_s: Assess(s,e,q,P)=Granted}.
```

Selection is the separate function

```text
Select(s,q,P,x)=
  fallback(q,x)                         if A_P is empty,
  pi_sel({e,payload_e,utility_e,z_e})   otherwise, with e restricted to A_P.
```

The active set is computed symbolically from the complete required profile, not from one adequacy channel. The selector may rank by normalized surplus, cost, latency, robustness, a declared utility head, or an external policy. It cannot choose an inactive candidate even if that candidate has the highest learned utility or raw score. Softmax, if used, is normalized only over the active set; a softmax over all candidates is not repaired by hoping unlicensed logits are small.

Payload is routed unchanged by default. An empty active set returns the exact fallback rather than a dummy all-zero expert. The fallback's own target safety is still an evidential question; operational fallback prevents unlicensed library use, not harm in every world.

### 9.1 Why neither ReLU sign supplies authorization by itself

A failed hidden unit has `ReLU(m)=0`, but a downstream computation can still fire through its bias or another path. For example,

```text
y=3 ReLU(-10)+2+5=7.
```

Thus the unqualified claim that the ReLU zero branch implements logical quarantine or non-explosion is false. The positive branch is not a grant either: an arbitrary positive hidden unit has no adequacy semantics, a positive learned margin may be wrong, and even accepted positive surplus settles only one atom. Authorization and quarantine in this architecture come from exact evidence/state/profile evaluation, the active mask, and the restricted selector. The ReLU channel is a useful numerical carrier after its meaning has been constructed; it is not an authorization mechanism by itself.

## 10. Forbidden production heads and allowed ablations

| head or shortcut | production status | permissible ablation question |
|---|---|---|
| direct four-way aggregate-status classifier | disconnected; cannot override atoms | how often does it contradict exact `WF + K_3`? |
| flat reason-code classifier | disconnected; reasons derive from address/polarity/payload/provenance | how much audit information does a closed label lose? |
| self-grant or self-certificate head | prohibited as evidence | how badly does self-confidence track an independent held-out system audit? |
| raw candidate argmax | prohibited as licensing or global adequacy | how often would it select outside the active set or hide overlaps/gaps? |
| softmax over all candidates | prohibited for deployment selection | compare with active-set-restricted normalization |
| margin-times-variable-payload gate | new plan requiring separate evaluation | measure whether scaling harms calibration, units, or boundary behavior |
| predicted checker/certificate identifier | never accepted as the certificate itself | retrieval assistance only; exact registry resolution and checking remain required |

Ablation outputs are logged beside, not fed into, production diagnostics, active masks, or grants.

## 11. Why ReLU is the reference rather than the semantics

ReLU is analytically useful here because:

- affine preactivations expose signed distances to learned hyperplanes;
- rectification gives explicit nonnegative positive-slack channels;
- paired ReLUs retain signed values exactly;
- finite ReLU functions are continuous piecewise affine, aligning with the planned exact CPWL statistic theorem;
- affine/ReLU min/max constructions make finite threshold and routing calculations inspectable; and
- activation cells provide a concrete geometry for later alignment tests.

None of these properties establishes calibration, certificate validity, learnability, sample efficiency, semantic alignment, mechanistic interpretation, or empirical superiority. Universal approximation alone does not establish any of the license conditions. The logic and symbolic decoder do not mention ReLU and may consume statistics from another compatible architecture.

## 12. Scoped architecture variants

### 12.1 Monotone or lattice statistic model

A monotone/lattice model may replace a ReLU statistic head only for coordinates with a proved semantic monotonicity and the same output/envelope contract. It is not a reason to impose monotonicity on arbitrary model embeddings, candidate comparisons, learned domains, or plan payloads.

Much of tolerance monotonicity is already exact in the symbolic decoder: holding a risk region fixed and increasing `epsilon` cannot turn support into refutation. Feeding `epsilon` into a learned status head merely relearns that rule. A monotone comparator is therefore useful only if the experiment identifies additional learned coordinates whose target statistics are genuinely monotone and tests extrapolation or calibration there. Otherwise it adds machinery without a distinct hypothesis.

### 12.2 Hard mixture of experts or external hard router

A hard MoE variant keeps the same statistic, evidence, diagnostic, and active-mask interface but performs a discrete route among active experts. It is a genuine comparator on seam-mismatch tasks because it can represent a discontinuous expert switch that one ordinary continuous ReLU output cannot exactly reproduce.

The hard router must expose the chosen tag, exact candidate set, route trace, fallback branch, and relevant misrouting/selected-scope certificate. Selecting a branch proves neither oracle optimality nor target safety. Task 14A's route-risk and severity terms still apply. A soft MoE has different mathematics: products of soft gates and variable expert outputs are not generally CPWL, so it does not inherit the planned exact ReLU result.

### 12.3 Graph/set plan model

Task 15's explicit typed-DAG model remains an optional empirical comparator for recursive-plan grade and explanation generalization. It must emit the same payload/grade/envelope proposals and preserve the same external checker/provenance packet. Task 16 does not add it to the ReLU reference or select it for training.

Checkpoint C selects no architecture alternative for the minimum empirical
core. Hard MoE is the sole eligible optional comparison and proceeds only if a
separate conforming-versus-mismatched seam study is adequately powered;
monotone/lattice and graph/set comparisons are deferred.

## 13. Task 17 proof obligations and disposition

This architecture deliberately exposed the following statements; Task 17 now adjudicates them:

1. exact factorization through the declared `WF` observations and `V/~_F`, with the finer diagnostic quotient;
2. exact decoding outside propagated error bands and conservative openness inside them;
3. exact finite ReLU computation of the chosen fixed-dimensional CPWL statistic maps;
4. the conforming-polyhedral seam iff and discontinuity obstruction;
5. the precise fixed-output/expandable-registry limitation;
6. a nontrivial joint-sufficiency construction for `(z,b,c)` plus scalar, boundary, and scale obstructions; and
7. exact proof-erased payload/grade realization for a fixed annotated CPWL plan with external certificate terms.

[`03_representation_theorems.md`](03_representation_theorems.md) proves (1)–(7) or gives the exact obstruction. It places global finite CPWL numerical maps inside the ReLU theorem; accepted calibration/evidence, `WF`, boundary-aware `K_3`, masks, routing, fallback, and certificates remain external. It also rejects a neural-width inference from finite status bits and treats `Ill/Well` only as a decoded normal form.

## 14. Executable semantic witness

[`verification/relu_architecture.py`](../verification/relu_architecture.py) implements the architecture's exact wrapper using only the standard library. It separates learned proposals from certified radii; applies inclusive support, strict refutation, polarity, validity, conflict, and calibration gates; exposes signed and rectified channels; validates dual-use normalization registries; and restricts selection to the active set.

[`verification/test_relu_architecture.py`](../verification/test_relu_architecture.py) contains thirteen regressions. They include supported equality with zero ReLU activation, conservative uncertainty-band openness, two-sided refutation versus one-sided withholding, favorable-score override by every invalid state, candidate/fallback evidence, comparable dual-use channels, inactive-candidate exclusion, fallback on a gap, explicit tie handling, exact payload routing, and the downstream-bias counterexample to ReLU-only quarantine. These are finite architecture witnesses; Task 17's separate theorem witnesses are linked from [`03_representation_theorems.md`](03_representation_theorems.md).

## 15. Decisions carried forward

1. The production architecture is a ReLU statistic scorer plus an exact symbolic decoder, not a status classifier.
2. Center-radius region proposals are the scalar default; calibration/error radii come from separately versioned accepted evidence.
3. Support is inclusive at zero, refutation is strict, and evidence polarity remains mode-specific.
4. Signed support/refutation margins, paired ReLU channels, exact validity, and complete diagnostics remain visible; rectified zero is never the full status.
5. Learned validity can conservatively open a judgment but cannot certify missing or invalid evidence.
6. Payload, grade, validity, certificate/checker/assumptions, provenance/rank, and loss-estimator identity remain separate plan channels.
7. Direct-root and certified-propagation routes are both allowed; component grants never compose by conjunction.
8. Fixed indexed and candidate-conditioned shared ReLU designs implement the same semantic contract.
9. Licensing precedes selection. Selection is restricted to the exact active set and falls back on gaps.
10. ReLU zero alone does not quarantine downstream computation; the exact mask does.
11. ReLU sign has no intrinsic adequacy semantics. Named normalized channels may be dual-use features only when their preactivations are the registered conservative atom margins; Task 17 proves joint sufficiency and minimality for the coordinate-complete state-plus-surplus family, while the full license and downstream consumer remain separately evaluated.
12. Separate content/grade channels are the general default; margin-scaled variable payloads require a new license.
13. Aggregate-status, reason-code, self-grant, unmasked argmax, and predicted-certificate heads are excluded from production and allowed only as disconnected ablations where stated.
14. Monotone/lattice and hard-MoE variants retain only their distinct scoped hypotheses; neither is presumed superior.

## Task conclusion

Task 16 derives a concrete ReLU realization of the architecture-neutral interface without assigning logical authority to the network. The scorer estimates reusable continuous quantities. Accepted calibration and checker records determine whether those quantities may enter the exact decoder. The decoder produces auditable atom states; profiles produce licenses; licenses produce an active mask; and a separate selector routes an unchanged payload or fallback.

The construction makes a conditional form of the project's strongest neural intuition precise enough to test: a named ReLU activation whose preactivation is the accepted conservative margin can genuinely be both strict certificate-relative atom surplus and a computational feature. An arbitrary positive activation means only positive preactivation, and a learned point margin means only predicted slack. Even the accepted surplus is not the whole logic. Boundary support, negative and open status, evidence validity, the remaining profile atoms, payload identity, and proof all require channels outside the rectified scalar. Task 17 now proves exactly which parts of this design ReLU realizes and where external symbolic structure is indispensable; Task 18 chooses how to learn them.
