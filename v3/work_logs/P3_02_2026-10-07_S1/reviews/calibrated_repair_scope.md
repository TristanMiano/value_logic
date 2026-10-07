# Additional scope boundaries for calibrated target repair

Contributor: **ChatGPT (GPT-6 Astra Pro)**. Status: internal same-model focused hostile review, October 7, 2026 UTC. This note contains only additional scope results and counterexamples beyond the [calibrated-repair review](calibrated_repair_review.md).

**Evidence type:** All proofs, examples, ranks, and counts in this note are **hand derivations**. No arithmetic program or constructive harness was run for this review. No principal time credit, final challenge, gate attempt, method-completion claim, or contribution-support claim is created.

The baseline theorem concerns exact recovery of \(Cp\) for every \(p\in\Delta_n\), using a fixed finite old matrix \(L\), arbitrary additional fixed known rational loss rows, and one of four shared scale/offset contracts. Its rank gap is \(r\), with one additional reference query when the offset is unknown and the old menu is empty. Constants-only targets are handled first and require no query.

## 1. Unrestricted nonnegative or strictly positive added rows do not increase the count

### Additional result

For the same full-simplex linear-target problem, the free signed-row minimum is also attained when **every added row must be entrywise strictly positive**, provided there is no upper payoff bound. It is therefore attained under the weaker entrywise-nonnegative constraint as well.

This positivity condition concerns the **added rows only**. The old rows may be signed. If a problem instead requires every historical row to satisfy a positivity restriction, that is an additional validity assumption on its old menu; this result does not retroactively change those rows.

The result uses freely available constant payoff shifts of arbitrary finite rational size. It does not assert that those shifts are free in money, risk, budget, or a restricted purchase system. The count is a scalar-query count.

### 1.1 Shared row-space facts

Write \(\mathbf1\) for the constant-one payoff row. Greedily select the required rows that raise the appropriate old base span. With known scale, that base includes \(\mathbf1\) through normalization. With unknown scale and a nonconstant target family, the required rows are \(\mathbf1\) and the target rows; put \(\mathbf1\) first in the selection order.

Once \(\mathbf1\) belongs to the current base span, replacing a selected row \(q\) by

\[
q+K\mathbf1
\]

does not change the span added by that row. More generally, \(\alpha q+\beta\mathbf1\), with known rational \(\alpha\ne0\), adds the same direction modulo the base.

For every finite rational row \(a\), one can choose a positive integer \(K\) with \(a_i+K>0\) for all outcomes. Thus strict positivity can be achieved using rational rows. The treatment of the constant direction is essential: with unknown scale it is not initially free unless already retained.

### 1.2 Offset known, scale known

The free base is \(\operatorname{row}[\mathbf1;L]\). For each selected required row \(q\), acquire

\[
a=q+K\mathbf1>0
\]

entrywise. The corresponding known-unit expected value gives \(qp=ap-K\). Its augmented span is exactly the same as that obtained by acquiring \(q\).

Each selected direction costs one strictly positive raw query, so the original minimum \(r\) is attained. Old signed rows cause no difficulty.

### 1.3 Offset known, scale unknown

If \(\mathbf1\notin\operatorname{row}L\), the first selected required direction is \(\mathbf1\). Acquire a strictly positive constant row \(K\mathbf1\), \(K>0\). Its value is \(sK\), which identifies \(s\), and its row adds exactly the constant direction. This costs one of the \(r\) already-required queries.

If \(\mathbf1\) is already retained, that step is unnecessary. In either case, every remaining selected target row can be acquired as \(q+K\mathbf1>0\). The constant row is now retained, so this shift preserves the added row-space direction and target recovery.

The count remains \(r\). The proof does not incorrectly treat an unobserved constant-payoff value in unknown units as free information.

### 1.4 Offset unknown, an old reference exists

Choose an old raw reference \(a=L_0\); its entries may have either sign. Let \(M\) be the old difference matrix.

With known scale, the base already contains \(\mathbf1\). For each selected row \(q\), acquire

\[
f=a+q+K\mathbf1>0.
\]

The new difference from the reference is \(q+K\mathbf1\). It adds the same direction as \(q\) modulo the augmented base, and its constant contribution is known by normalization.

With unknown scale, first inspect whether \(\mathbf1\in\operatorname{row}M\). If not, the first selected required direction is \(\mathbf1\). Choose a sufficiently large positive integer \(K\) and acquire

\[
f=a+K\mathbf1>0.
\]

Its difference from the old reference is \(K\mathbf1\), whose measured value is \(sK\). It supplies the required constant calibration direction using one of the \(r\) queries. After that, or if the constant direction was already retained, acquire every remaining selected \(q\) as \(a+q+K\mathbf1>0\). Its new difference adds the same direction as \(q\).

There are exactly \(r\) added raw queries in either scale case. Offset differencing remains valid because the same nuisance values govern the reference and new rows.

### 1.5 Offset unknown, no old reference

The signed construction may use the zero row as reference. For strict positivity, use instead a positive rational constant row

\[
a=\tau\mathbf1,\qquad \tau>0.
\]

This is the already-required first reference query.

With known scale, acquire each selected target direction as

\[
f=a+q+K\mathbf1>0.
\]

Its difference is \(q+K\mathbf1\); normalization supplies the constant term. There are \(r\) queries after the reference.

With unknown scale, the empty effective old matrix does not contain \(\mathbf1\). Acquire a second positive constant row, for example

\[
f=(\tau+1)\mathbf1.
\]

Its difference from the reference is \(\mathbf1\), so the measured difference is \(s\). This is the first of the \(r\) required effective directions. Acquire each remaining selected target direction using \(a+q+K\mathbf1>0\), whose constant shift is now removable in the retained row space.

Thus the strict-positive construction uses exactly \(r+1\) raw queries, attaining the lower bound. In this construction the positive constant reference also permits offset recovery once scale is known: its raw value is \(s\tau+b\). This is a property of the chosen reference, not a promise that every minimum partial-target repair recovers the offset.

### 1.6 Limits of this positivity result

The result covers finite rational semantic payoff rows and unconstrained positive common scale where applicable. The rank theorem supplies the lower bound because nonnegative or positive queries form a subclass of free signed queries; the constructions supply the matching upper bound.

It does not cover fixed upper stakes, a finite purchasable menu, a ban on constant-payoff queries, action-dependent acquisition prices, or a smaller nonconvex source of laws. Concrete failures under such changes appear below.

## 2. A fixed payoff box can increase the minimum

Here a box such as \([0,1]^n\) constrains each **semantic outcome payoff in declared units**, before applying the unknown measurement scale or offset. It does not assert that the raw readings \(sLp+b\mathbf1\) lie between zero and one.

The box fixes allowable payoff stakes relative to the old rows and target interpretation. Re-expressing all semantic payoffs in new known units would also transform the box. Keeping the numerical box fixed while changing only a candidate row is an operational restriction, not a free relabeling. In particular, rescaling a proposed new row alone does not rescale an old reference or its shared offset.

### 2.1 Hand-derived four-outcome example

Let

\[
a=(0,0,1,1),\qquad c=(0,1,0,1),
\]

with old menu consisting only of \(a\), target \(cp\), and source the full \(\Delta_4\). Require every added raw payoff row to belong to \([0,1]^4\). The old row itself satisfies that same box.

The two binary payoff patterns are independent directions modulo constants. The key geometric fact is

\[
\boxed{
\bigl(a+\operatorname{span}\{\mathbf1,c\}\bigr)\cap[0,1]^4
=\{a\}.
}
\tag{1}
\]

To prove it, a candidate in the affine plane has coordinates

\[
f=a+\alpha c+\beta\mathbf1
=(\beta,\alpha+\beta,1+\beta,1+\alpha+\beta).
\]

The first and third coordinates lying in \([0,1]\) force \(\beta=0\). The second and fourth then force \(\alpha=0\). This proves (1) for positive, negative, and zero values of the proposed coefficients.

### 2.2 Known scale, unknown offset: the minimum rises from one to two

The free signed-row count is \(r=1\), since the old difference matrix is empty and \(c\) is nonconstant. A free query \(a+c=(0,1,1,2)\) works by differencing, but violates the payoff ceiling.

If one boxed new row \(f\) sufficed, the full-simplex target criterion would require

\[
c\in\operatorname{span}\{\mathbf1,f-a\}.
\]

Because \(c\) is nonconstant, its coefficient on \(f-a\) is nonzero. Rearranging gives \(f=a+\alpha c+\beta\mathbf1\), with \(\alpha\ne0\). Equation (1) rules out such a boxed row. Thus one additional query cannot suffice, regardless of decoder.

Two boxed queries do suffice: acquire \(0\) and \(c\). Their raw difference is \(cp\), with the shared offset canceled. Consequently the exact bounded-menu minimum is **two**, versus the free-row minimum **one**.

### 2.3 Unknown positive scale and offset: the minimum rises from two to three

The free-row count is \(r=2\), because the empty old difference space must acquire the independent rows \(\mathbf1,c\).

Suppose two boxed rows \(f,g\) sufficed. The scale-unknown target criterion requires

\[
\operatorname{span}\{\mathbf1,c\}
\subseteq
\operatorname{span}\{f-a,g-a\}.
\]

The left side has dimension two, while the right side has dimension at most two. Equality must hold. Therefore each difference belongs to \(\operatorname{span}\{\mathbf1,c\}\), and both raw rows lie in the affine plane in (1). That equation forces \(f=g=a\), contradicting the required two-dimensional difference span.

Three boxed queries suffice: acquire \(0,\mathbf1,c\). Their readings are \(b,s+b,scp+b\), from which

\[
s=v_{\mathbf1}-v_0>0,\qquad
cp=\frac{v_c-v_0}{v_{\mathbf1}-v_0}.
\]

Hence the exact bounded-menu minimum is **three**, versus the free-row minimum **two**.

The lower bounds use the full-simplex recovery criteria, so neither an arbitrary decoder nor boundary laws create a loophole. The construction retains the original raw row; the old observation is simply unnecessary for this particular bounded repair.

## 3. When a freely available payoff box does preserve the count

The preceding example does not justify saying that any finite payoff ceiling increases the count.

### 3.1 Known offset

If the offset is known and every new row in \([0,1]^n\) is available, the free count remains attainable. Once the constant direction is free or retained, replace each required row \(q\) by

\[
\tfrac12\mathbf1+\alpha q
\]

for a sufficiently small positive rational \(\alpha\), so every coordinate lies strictly between zero and one. This adds the same direction modulo constants. If scale is unknown and the constant direction is absent, first acquire \(\tfrac12\mathbf1\), which supplies it using its already-required query.

### 3.2 Unknown offset, a reference with interior slack

If an available old reference \(a\) lies in \((0,1)^n\), each required direction \(q\) can be acquired as

\[
f=a+\alpha q\in(0,1)^n
\]

for sufficiently small positive rational \(\alpha\). The difference is exactly \(\alpha q\). This realizes every required row-space direction, including a missing constant direction under unknown scale, with one query each.

A directly observed old row is sufficient but not necessary. A known rational affine combination of old rows, whose coefficients sum to one, is also an available virtual reference: the same combination of their raw readings equals \(sap+b\). Differences from this reference span the same old difference space. Thus an interior virtual reference also suffices without an additional query.

### 3.3 No old reference

If the offset is unknown and the old menu is empty, choose the first reference as \(\tfrac12\mathbf1\), which is interior to the box. The preceding construction realizes every required effective direction within the box. The original \(r+1\) count is therefore attainable even with strict interior payoff bounds.

### 3.4 At most one extra query for a freely available full box

Suppose the offset is unknown, an old reference exists, and every row of \([0,1]^n\) is purchasable as one query. If the free minimum is \(r>0\), the bounded minimum is either \(r\) or \(r+1\).

The free theorem gives the lower bound \(r\). For an upper bound, first acquire the interior constant row \(a_*=\tfrac12\mathbf1\). Switching to it as reference preserves all old differences and may add one new effective direction. Therefore the remaining target rank gap \(r'\) is at most \(r\). Since \(a_*\) has interior slack, realize the remaining \(r'\) directions by small rational perturbations \(a_*+\alpha q\) inside the box. The total is \(1+r'\le r+1\).

If the target is already recovered, \(r=0\), no query is needed. If no old reference exists, its reference query was already included in the baseline formula and does not create an additional box penalty.

The example in Section 2 attains the extra-one bound for both offset contracts. This upper bound depends on the entire box being available, including an interior constant row; it does not apply to an arbitrary restricted menu.

### 3.5 Exact criterion for whether the box requires the extra query

The preceding upper bound admits a sharp geometric test. Assume an old offset reference \(L_0\) exists and the free gap is \(r>0\). Let \(M\) be the old difference matrix. Define the base and required spaces exactly as in the calibrated target theorem:

\[
B=
\begin{cases}
\operatorname{row}[\mathbf1;M],&\text{scale known},\\
\operatorname{row}M,&\text{scale unknown},
\end{cases}
\]

\[
R=
\begin{cases}
\operatorname{row}C,&\text{scale known},\\
\operatorname{row}[\mathbf1;C],&\text{scale unknown}.
\end{cases}
\]

Set

\[
W=B+R,\qquad r=\dim W-\dim B,\qquad
U=[0,1]^n,\qquad S=(U-L_0)\cap W.
\]

Then exactly \(r\) additional boxed rows suffice **iff**

\[
\boxed{B+\operatorname{span}S=W.}
\tag{2}
\]

If (2) fails, the exact minimum is \(r+1\). The \(r=0\) case requires no query and is excluded from this test's positive-gap statement.

**Necessity.** Suppose \(r\) successful new rows have effective differences \(d_1,\ldots,d_r\). Their completed base contains \(W\), while its dimension is at most \(\dim B+r=\dim W\). Hence

\[
B+\operatorname{span}\{d_1,\ldots,d_r\}=W.
\]

In particular, every \(d_i\in W\). Each raw row is \(L_0+d_i\in U\), so every \(d_i\in S\). The resulting spanning identity implies (2).

**Sufficiency.** If (2) holds, the images of the elements of \(S\) span the \(r\)-dimensional quotient \(W/B\). Select \(r\) elements \(d_1,\ldots,d_r\in S\) whose quotient classes form a basis. The raw rows \(L_0+d_i\) lie in \(U\), and their effective rows enlarge the old base to \(W\), supplying every required direction. They therefore recover the target with exactly \(r\) queries.

**Rational attainability.** With rational old and target matrices, \(W\) is a rational subspace and \(S\) is a bounded rational polytope, possibly empty or of lower affine dimension. If nonempty, it is the convex hull of its rational vertices, so its linear span is generated by those vertices. Therefore the quotient basis can be selected among rational points of \(S\); real versus rational queries do not create a gap in (2).

**Failure of the test.** Fewer than \(r\) queries are excluded by the free lower bound, and exactly \(r\) are excluded by necessity above. The interior-reference construction gives at most \(r+1\). Hence \(r+1\) is exact.

**Virtual reference condition.** Suppose a known rational affine combination \(a\) of the old rows lies in \(\operatorname{int}U\). Then \(\delta=a-L_0\) is in the old difference space and therefore in \(B\). For every required direction \(q\), a sufficiently small rational \(\alpha>0\) gives

\[
f=a+\alpha q\in U,\qquad f-L_0=\delta+\alpha q\in S.
\]

Modulo \(B\), this realizes a nonzero multiple of the desired class \(q+B\). Thus (2) holds. If the existence of an interior old affine combination is initially stated with real coefficients, rational coefficients summing to one can be chosen sufficiently close to preserve interior membership.

An interior virtual reference is **sufficient, not necessary**. Take the single old row \(a=(0,0,1,1)\), but target \(c=a\) itself. Its old affine hull is the singleton \(\{a\}\), which has no point in \(\operatorname{int}U\). With known scale, one new boxed zero row recovers \(ap\), attaining the free count one. With unknown positive scale, two boxed rows \(0,\mathbf1\) give the offset and scale, attaining the free count two. The target differs from the independent binary target of Section 2, and the feasible required affine plane differs accordingly.

This is a separate exact criterion for the declared full-box menu. It is not a claim that the existing free-query certificate companion implements a constrained purchase optimizer.

## 4. A restricted purchasable menu can require more rows or make repair impossible

On \(\Delta_3\), with known units and no old queries, let the target be \(p_1\). The free-row minimum is one: acquire \(e_1\).

Suppose the only purchasable rows are

\[
q_1=(1,1,0),\qquad q_2=(0,1,0).
\]

Neither query alone identifies \(p_1\):

- Under \(q_1\), the pure laws \(e_1,e_2\) both give one but have different \(p_1\).
- Under \(q_2\), the pure laws \(e_1,e_3\) both give zero but have different \(p_1\).

Both together recover \(p_1=q_1p-q_2p\). The restricted-menu minimum is therefore **two**, although the free target rank gap is **one**. All displayed payoffs are nonnegative and bounded by one; here the missing directly purchasable direction causes the increase even without any calibration nuisance.

If the only available rows are \(\mathbf1,e_2\), the same target is impossible to recover: the pure laws \(e_1,e_3\) agree on every available reading. Repeating exact queries does not add a row-space direction.

With unknown scale, a restricted menu may also fail because no combination of its rows supplies a nonzero known constant payoff. For example, the menu \(e_1,e_2\) on \(\Delta_3\) cannot globally identify any nonconstant linear target under a free positive common scale, since it does not span \(\mathbf1\).

The free rank gap remains a lower bound, but no longer supplies an attainable count. Exact feasibility is still tested by the completed-menu row-space criterion. Minimizing the number or price of purchases over a specified menu is an additional selection problem.

## 5. Full simplex, known faces, and finite boundary catalogues are different sources

### 5.1 A known support face can lower the required count

If the source is a known full support face

\[
P=\{p\in\Delta_n:p_i=0\text{ for }i\notin J\},
\]

the exact same finite-simplex argument applies after restricting every loss and target row to the coordinates \(J\). Constancy and rank are then evaluated on that smaller simplex.

For example, on the known face \(p_3=0\), the target \(p_3\) is constant and requires no query. It is nonconstant on the full \(\Delta_3\).

A nonconstant example uses old \(L=e_1\) and target \(p_2\). On \(P=\operatorname{conv}\{e_1,e_2\}\), known-unit data already give \(p_2=1-p_1\), so no additional query is needed. On the full \(\Delta_3\), one additional query is required. Under unknown positive scale and known offset, the face needs one added direction, while the full simplex needs two: the full target row \(e_2\) and full normalization row are independent modulo the old \(e_1\), whereas their restrictions to the face are dependent modulo each other.

An implementation explicitly contracted for the full simplex must not silently replace it by a favorable support face inferred without evidence.

### 5.2 A particular boundary observation can need no local repair

The global count is not a per-record necessity. With \(L=e_1\), unknown scale \(s>0\), and target \(p_1\), the observation \(v=sp_1=0\) forces \(p_1=0\). That particular record needs no added query, although global recovery over the entire simplex requires a scale-calibrating direction.

The scale itself remains undetermined at this zero observation. This is another reason that a local target conclusion does not imply global calibration.

### 5.3 Nonconvex boundary sources can change both the count and the role of signs

Consider the finite catalogue

\[
P=\{e_1,e_2,e_3\}
\]

and the target of identifying the full law, under unknown positive common scale and known offset.

One signed query

\[
q=(-1,0,1)
\]

suffices on this source: negative, zero, and positive observed values identify \(e_1,e_2,e_3\), respectively. The decoder uses the sign; it does not recover a nonconstant expectation on the full convex simplex.

No single nonnegative query can identify all three catalogue laws. For a nonnegative row, each state with zero payoff produces only zero, and every state with positive payoff can produce every positive raw value by changing the positive scale. There are at most two distinguishable classes, zero and positive.

Two nonnegative queries suffice:

\[
L=
\begin{pmatrix}
1&0&1\\
0&1&1
\end{pmatrix}.
\]

The three pure laws yield the three distinct positive rays through \((1,0)\), \((0,1)\), and \((1,1)\). Thus the exact minimum on this nonconvex boundary catalogue is **one signed query** or **two nonnegative queries**.

This does not contradict Section 1. Its positivity construction relies on the full-simplex nonconstant-linear-target necessity of retaining the constant calibration direction. That necessity fails on this nonconvex catalogue; the signed one-query solution intentionally exploits that failure. Convexifying the source changes its identification problem.

## 6. Exact conditions for recovering the offset as well as a partial target

The earlier review gave a concrete partial-target repair whose offset remains unidentified. The following additional row-space conditions state exactly what is missing.

Let \(F\) be a completed nonempty raw menu, choose \(F_0\) as reference, and let \(D\) contain its row differences. Write \(z\) for the differenced readings.

### 6.1 Known nonzero scale, unknown offset

The offset is globally identifiable iff

\[
\boxed{F_0\in\operatorname{row}[\mathbf1;D].}
\tag{3}
\]

If \(F_0=\gamma\mathbf1+\beta D\), then

\[
b=v_0-s\gamma-\beta z.
\]

For necessity, if (3) fails, there is a tangent direction \(h\) with \(\mathbf1h=0\), \(Dh=0\), and \(F_0h\ne0\). For an interior law and sufficiently small nonzero \(t\), put \(p_t=p+th\) and \(b_t=b-stF_0h\). The entire raw record is unchanged while the offset changes.

Equivalently, a known affine combination of raw loss rows must yield some known constant payoff. The coefficient sum must be one so that the offset remains with coefficient one.

### 6.2 Unknown positive scale and unknown offset

Without needing to assume target recovery first, the exact offset criterion is

\[
\boxed{
0\in\operatorname{aff}\{F_0,\ldots,F_{m-1}\}.
}
\tag{4}
\]

Indeed, if \(\lambda F=0\) and \(\lambda\mathbf1_m=1\), then \(\lambda v=b\).

For necessity, introduce \(x=sp\). Its admissible set contains all strictly positive vectors, and the observation is \(v=Fx+b\mathbf1_m\). If the row extracting \(b\) is outside the row space of the linear observation map \([F\ \mathbf1_m]\), there is a kernel direction \((h,k)\) with \(k\ne0\). Perturb a strictly positive \(x\) and \(b\) by a sufficiently small multiple of that direction. The raw observation stays fixed and \(b\) changes; renormalizing the positive vector gives another admissible \((p,s)\). Thus offset identification forces coefficients \(\lambda\) with exactly the two identities above.

In terms of a chosen reference, (4) is equivalent to \(F_0\in\operatorname{row}D\). For instance, expressing \(F_0\) as a combination of differences rearranges to an affine combination of raw rows equal to zero; the reverse implication follows by subtracting the reference.

If a nonconstant linear target is already recovered under this affine nuisance, the target theorem gives \(\mathbf1\in\operatorname{row}D\), hence identifies \(s\). Offset recovery still additionally requires \(F_0\in\operatorname{row}D\). The target rows need not imply that inclusion.

Consequently, recovering a partial family of expected losses, recovering scale, recovering offset, and recovering every old absolute expected loss are distinct services. For \(n\ge2\), full-law recovery forces the relevant offset condition, but a partial-target repair may not. When \(n=1\), the full law is already constant and known; under unknown scale and offset, a single constant-one row gives \(v=s+b\) without identifying either nuisance. A known constant reference in the from-scratch constructions supplies the missing condition automatically.

## 7. Review disposition

The signed rational-row count needs no increase for unrestricted nonnegative or strictly positive added payoffs. It does need an explicit free-query assumption: a fixed semantic payoff box can add one query when an old offset reference has insufficient feasible directions, and a smaller purchasable menu can impose a larger increase or make the service impossible.

Known support faces, local boundary observations, and nonconvex boundary catalogues require their own source semantics. In particular, nonconvex sources can invalidate both the full-simplex count and its equivalence between signed and nonnegative additions.

These are hand-proved refinements and counterexamples to overbroad formulations. They leave the full-simplex free-query result intact and do not turn its certificate companion into an acquisition or learning method.
