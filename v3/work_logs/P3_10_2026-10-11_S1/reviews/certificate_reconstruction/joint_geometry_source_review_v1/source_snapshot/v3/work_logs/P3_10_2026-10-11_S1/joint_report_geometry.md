# Joint report geometry and the exact F–V relation

Contributor: **ChatGPT (GPT-6 Astra Pro), principal /root**, 2026-10-11.
Status: **post-outcome exploratory interpretation of the completed P3-10 reports**.
The derivation extends the earlier public-key marginal-bound observation. It
adds no paid run, primary endpoint, fair-bit assertion or contribution decision.

## 1. F and V have an observable affine relation

Let `q_t` be the immutable issued forecast, `y_t` its binary truth, and `S` the
positions with delivered checked receipts. On a successful parent path every
selected position supplies its checked label. The endpoints are

\[
F=\sum_t(q_t-y_t)^2,\qquad
V=\sum_{t\notin S}[q_t+(1-2q_t)y_t],\qquad
Z=\sum_t\mathbf1\{a_t\ne y_t\}.
\]

Using `(q-y)^2=q+(1-2q)y-q(1-q)` at unselected positions yields

\[
F-V=\underbrace{\sum_{t\in S}(q_t-y_t)^2
-\sum_{t\notin S}q_t(1-q_t)}_{C\text{ known from public trace and paid labels}}.
\]

This is an exact deterministic relation for the saved episode. It concerns
end-of-episode knowledge and does not retroactively change an issued forecast.
F and V remain different scientific targets, but their remaining label
uncertainty is the same translated coordinate. Their matching marginal widths
are therefore not two independent empirical successes. All three frozen
endpoints and their separate names must still be retained in the results.

The shift also limits how a joint confidence statement should be interpreted:
a rectangular display that independently varies F and V includes impossible
pairs unless it explicitly enforces `F=V+C`. The experiment does not become a
joint-coherence theorem merely because it returns all three intervals.

## 2. Grouping the unresolved full keys

For binary truth, each per-position contribution to F or Z is affine in its
label. Group all occurrences by the complete semantic/source/version key. Use
all checked end-of-episode paid labels to resolve known keys. The remaining
joint target has the form

\[
(F,Z)=A+\sum_{k\in U}b_k y_k,\qquad y_k\in\{0,1\},\qquad b_k\in\mathbb Q^2.
\]

Here `A` includes every constant and known-label contribution, and `b_k` sums
the F and Z coefficients over occurrences of unknown key `k`. No private CNF
truth is used to build A or the vectors. The unresolved-key cube is a relaxation:
logical relationships between distinct CNFs may remove some assignments, and
those relationships have not been purchased by this construction.

The discrete feasible image can have up to `2^|U|` points. Its convex hull is

\[
\mathcal Z=A+\sum_{k\in U}[0,b_k],
\]

an exact rational planar zonotope. Calling it a convex hull does not claim that
fractional mixtures are actual mathematical truth assignments. Its extreme
linear bounds are nevertheless sharp on the binary-key relaxation, because
any linear objective chooses each `y_k` at an endpoint.

For every rational direction `c`, the support bounds are

\[
\min c\cdot(F,Z)=c\cdot A+\sum_k\min(0,c\cdot b_k),\qquad
\max c\cdot(F,Z)=c\cdot A+\sum_k\max(0,c\cdot b_k).
\]

This proves each marginal bound by choosing an axis and each coupled bound by
choosing a non-axis direction. It also proves that no stronger linear bound
follows from the relaxed key identities and paid labels alone. It says nothing
about the price of maintaining this representation as a deployed service.

## 3. Why separate extreme endpoints may be incompatible

For a target coordinate, a positive coefficient attains its upper endpoint at
`y_k=1`, a negative coefficient at `y_k=0`. Thus simultaneous coordinate maxima
exist exactly when every unknown key's nonzero coefficient requirements agree.
A key with opposite-sign F and Z coefficients prevents the joint top-right
corner of the marginal rectangle from being attainable. The corresponding
criterion applies to each of the four corners after reversing the signs for
coordinates minimized. Zero coefficients impose no requirement.

A concrete one-key case illustrates the distinction: suppose the same unknown
label occurs once with forecast `q=1/4` and terminal action `a=1`. Then
`F=1/16+y/2` and `Z=1-y`. The possible pairs are `(1/16,1)` and `(9/16,0)`.
The rectangle's top-right point `(9/16,1)` is impossible, although each of its
individual coordinates is an attainable marginal upper endpoint.

If all nonzero vectors are collinear, the convex hull is a segment, and if all
vectors vanish it is a point. An audit must preserve those degeneracies and
not divide by a zero rectangle area or claim a two-dimensional region.

## 4. Exact construction without exponential enumeration

Flip each vector into the closed upper half-plane, shifting A by the original
vector when a sign is reversed. Ignore zero vectors and combine parallel
vectors after sorting by exact rational cross products. Start at the resulting
A, follow the sorted positive edges, then their negatives in the same order.
This constructs the convex hull with at most twice as many vertices as distinct
nonparallel unknown-key vectors. The proof is the Minkowski-sum boundary rule:
each directed edge changes only the generators whose supporting direction
crosses that edge normal. Each vertex is realized by a binary endpoint choice.
No floating-angle tolerance or hidden truth enumeration is necessary.

The implementation audit will independently verify its directional support
values against the direct sum formula, all four marginal extrema, convex
orientation, and later containment of the already independently checked true
(F,Z). It will write the public construction before reading the private numeric
observer for that last containment check. The investigator is not blinded:
this extension was chosen after observing the final experiment's outcomes.

## 5. Interpretation boundary

A smaller joint region or sharper key-based interval would be a deterministic
information-use observation for these already paid traces. It is not a result
of the original paid reporting algorithm and cannot replace its A5 score.
The original grid confidence intervals use a different conditional sampling
argument; a deterministic marginal interval can be wider than a delivered
sampling interval on a particular path. Any proposed intersection keeps the
sampling interval's original assumptions and confidence qualification. No new
joint confidence level, empirical coverage guarantee, report-dependent feedback
policy or free reporting economy is inferred here.
