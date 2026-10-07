# Coefficient-alphabet boundary for an exact two-action decision

Contributor: **ChatGPT (GPT-6 Astra Pro)**. Status: internal same-model targeted mathematical review; **hand derivation only**. No code, arithmetic program, or executable challenge was run. No principal time credit or new contribution-support claim is created.

**Disposition:** The proposed example and all its stated minimum counts are sound. The lower bounds apply to arbitrary exact decoders under the declared finite fixed linear-query contracts. They do not restrict the decoder to linear arithmetic.

## 1. Target, source, and access contract

Let \(p\) range over the full normalized simplex \(\Delta_3\). The two known action-loss rows are

\[
A=(1,\sqrt2,0),\qquad B=(0,0,1),
\]

with contrast

\[
d=A-B=(1,\sqrt2,-1).
\]

The service is to return **some Bayes-optimal action** at every law:

\[
dp<0\Rightarrow A,\qquad
dp>0\Rightarrow B,\qquad
dp=0\Rightarrow A\text{ or }B.
\]

It does not require recovering \(p\), either absolute action risk, or the numerical contrast \(dp\).

Queries are finitely many fixed known linear loss rows. We compare real versus rational query coefficients and signed versus nonnegative query rows. The exact observations are either \(y=Lp\) in known units or \(v=sLp\) with one unknown common \(s>0\). The offset is known in both cases. Query choices are fixed; no adaptive acquisition or restricted price menu is analyzed.

The target includes a known algebraic coefficient \(\sqrt2\). Upper bounds permit an external exact decoder to use that coefficient and exact comparisons. They do not claim that an irrational payoff row or irrational coefficient comparison is already available in the phase-two native rational piecewise-affine language.

Both actions have a unique-optimum region containing strictly positive laws: \(d\) is positive near \(e_1\) and negative near \(e_3\). A useful interior tie law is

\[
p_*=\frac{(1,1,1+\sqrt2)}{3+\sqrt2}.
\tag{1}
\]

Its coordinates are strictly positive, sum to one, and satisfy \(dp_*=0\). This interior crossing prevents boundary or tie-breaking exceptions from defeating the lower bounds.

## 2. Two exact decoder criteria for a crossing contrast

The following argument applies to any fixed real contrast having an interior zero law and taking both signs.

### 2.1 Known units

Some optimal action can be returned from \(Lp\) for every full-simplex law iff

\[
d\in\operatorname{row}[\mathbf1;L].
\tag{2}
\]

Sufficiency follows from an identity \(d=\alpha\mathbf1+\beta L\): the exact contrast is \(dp=\alpha+\beta y\).

For necessity, if (2) fails, choose \(h\) with

\[
\mathbf1h=0,\qquad Lh=0,\qquad dh\ne0.
\]

For sufficiently small \(\varepsilon>0\), the two laws \(p_*\pm\varepsilon h\) are strictly positive and normalized. They give the same query vector but opposite nonzero contrast signs. Their unique optimal actions differ. No decoder receiving that shared vector can satisfy both.

### 2.2 Unknown common positive scale

Some optimal action can be returned from \(sLp\) for every law and every \(s>0\) iff

\[
d\in\operatorname{row}L.
\tag{3}
\]

Sufficiency follows from \(d=\beta L\): \(\beta v=sdp\), whose sign is the sign of \(dp\).

For necessity, work with the positive homogeneous vector \(x=sp\). If (3) fails, choose \(h\in\ker L\) with \(dh\ne0\). At the interior zero vector \(x_*=p_*\), choose sufficiently small \(\varepsilon>0\) so that

\[
x_\pm=x_*\pm\varepsilon h>0.
\]

The query vectors \(Lx_+\) and \(Lx_-\) coincide, while \(dx_+\) and \(dx_-\) have opposite signs. Put

\[
s_\pm=\mathbf1x_\pm>0,\qquad
p_\pm=x_\pm/s_\pm.
\]

These are admissible normalized laws and positive scales with the same raw observation. Because the normalizing denominators are positive, \(dp_\pm\) still have opposite signs. The unique optimal actions differ.

Thus the lower bound covers normalization, nonlinear transformations, arbitrary tie conventions, and any other exact decoder acting on the same data. Randomization cannot give an almost-sure optimal-action guarantee at both colliding laws either.

The interior crossing is essential. For a contrast of one sign throughout the source, a fixed action can already be optimal and these row-space necessities need not hold.

## 3. Known units: one real query versus two rational queries

One real signed query \(d\) supplies its exact expected contrast and therefore decides the action. No query cannot suffice, since the optimal action changes across the source.

Suppose one rational row \(\ell\in\mathbb Q^3\) sufficed. Criterion (2) would give real \(\alpha,\beta\) such that

\[
d=\alpha\mathbf1+\beta\ell.
\]

Taking coordinate differences from the third coordinate gives

\[
2=\beta(\ell_1-\ell_3),\qquad
1+\sqrt2=\beta(\ell_2-\ell_3).
\]

The first equation forces \(\beta\ne0\) and \(\ell_1-\ell_3\ne0\). Dividing yields

\[
\frac{1+\sqrt2}{2}
=\frac{\ell_2-\ell_3}{\ell_1-\ell_3},
\]

whose left side is irrational and right side is rational. This is impossible.

Two rational nonnegative event rows \(e_1,e_2\) suffice. Their known-unit observations give \(p_1,p_2\), after which

\[
dp=2p_1+(1+\sqrt2)p_2-1.
\]

The exact known-unit minimum is therefore **one real signed query** or **two rational queries**. Two rational nonnegative queries already attain the rational minimum.

For completeness, a single real nonnegative query also suffices in known units: query

\[
d+\mathbf1=(2,1+\sqrt2,0),
\]

then compare its expectation with one. This shift uses known normalization in known units.

## 4. Unknown positive scale: one real signed query versus two rational signed queries

One real signed query \(d\) gives \(sdp\), preserving its sign. This attains the nonzero-query lower bound.

Define the rational rows

\[
u=(1,0,-1),\qquad e_2=(0,1,0).
\]

They satisfy

\[
d=u+\sqrt2\,e_2.
\]

Their raw values \(v_u=su p\) and \(v_2=sp_2\) therefore give

\[
v_u+\sqrt2\,v_2=sdp.
\]

The sign determines the action. The common scale itself need not be recovered.

One rational query cannot suffice under unknown scale, since any decoder valid for every positive scale would in particular work at scale one, contradicting Section 3's known-unit lower bound. Thus the exact rational signed minimum is **two**.

The retained rational plane is

\[
W=\operatorname{span}\{u,e_2\}
=\{(a,b,-a):a,b\in\mathbb R\}.
\tag{4}
\]

It does not contain \(\mathbf1\). Consequently this construction is an example of a nonconstant exact decision under unknown scale without globally recovering any nonconstant linear expectation. The scalar contrast is only available multiplied by \(s\); its sign is sufficient for the stipulated service.

## 5. Unknown positive scale with rational nonnegative queries: three are necessary and sufficient

### 5.1 The rational plane containing \(d\) is forced

Any two-dimensional rational row space containing \(d\) has a nonzero rational normal vector \(h=(h_1,h_2,h_3)\). Orthogonality to \(d\) requires

\[
h_1+\sqrt2\,h_2-h_3=0.
\]

All \(h_i\) are rational, so irrationality of \(\sqrt2\) forces

\[
h_2=0,\qquad h_1=h_3.
\]

The normal is therefore proportional to \((1,0,1)\), and the plane is exactly \(W\) in (4). A rational one-dimensional space cannot contain \(d\), since the ratio of its second to first coordinate is irrational.

Equivalently, a rational row space containing \(u+\sqrt2 e_2\) must retain the two rational components \(u,e_2\). In dimension two it must be their whole span.

### 5.2 Nonnegative rows cannot span that plane

A nonnegative row in \(W\) has the form \((a,b,-a)\) with all three entries nonnegative. This forces \(a=0\) and \(b\ge0\). Hence

\[
W\cap\mathbb R_{\ge0}^3
=\{b e_2:b\ge0\},
\]

which spans only one dimension.

If two rational nonnegative rows sufficed, criterion (3) would require their row space to contain \(d\). It would have to be the two-dimensional plane \(W\), yet its nonnegative rows cannot span that plane. This is a contradiction.

Three rational nonnegative event rows suffice:

\[
L=I_3,\qquad v=(sp_1,sp_2,sp_3).
\]

The sign of \(v_1+\sqrt2 v_2-v_3\) decides the action. No normalization or explicit scale estimate is needed for that decoder. Thus the exact minimum is **three**.

In fact, any successful finite rational nonnegative menu for this particular decision must have rank three: rank at most two is excluded by the same argument. It can therefore also recover the full probability law under unknown scale. This necessity is specific to the combination of this target boundary, rational query coefficients, nonnegative query rows, and the full-simplex exact-decision contract. It is not a general requirement for useful decisions.

If strict positivity of added rational rows is required, three still suffice: use the rows \(\mathbf1+e_i\). Their sum of raw values is \(4s\); their individual values then recover \(p_i\). The nonnegative lower bound still applies.

## 6. Comparison table and interpretation

All minima below are for the same two-action exact-decision service on the full \(\Delta_3\), with fixed known query rows and a known offset:

| Query coefficient and sign restriction | Known units | Unknown positive common scale |
|---|---:|---:|
| Real, signed | 1 | 1 |
| Real, nonnegative | 1 | 2 |
| Rational, signed | 2 | 2 |
| Rational, nonnegative | 2 | 3 |

For the remaining table entry, two real nonnegative queries \(A,B\) suffice under unknown scale, since their raw difference is \(sdp\). One cannot suffice: a single nonnegative row cannot have the mixed-sign \(d\) in its one-dimensional row space, contradicting (3).

This example exposes two different restrictions:

- Rational coefficients can prevent a single queried affine coordinate from aligning with an irrational decision boundary, even when its decoder may use known algebraic constants.
- Under unknown scale, nonnegative rational rows cannot span the smallest rational space carrying the sign-changing contrast. Adding a constant calibration direction raises the query dimension.

There is no conflict with the prior result that nonnegative additions preserve the full-simplex **linear-target recovery** count. A nonconstant linear target under unknown scale already forces a retained constant calibration direction. This example asks only for one optimal action; its two-query signed solution avoids that direction.

The result concerns exact identification everywhere, including laws arbitrarily close to the tie plane. A declared positive decision margin, approximate optimality, a smaller source, or a larger coefficient alphabet can change the minimum. None is silently substituted here.

The external exact decoder's use of \(\sqrt2\) is part of the comparison contract. No claim is made that the current native rational piecewise-affine syntax implements an irrational payoff coefficient, an exact irrational decision boundary, or arbitrary-real equality testing. Known algebraic reasoning outside that syntax and native representability remain separate questions.

The proof is an elementary coefficient-alphabet obstruction and constructive comparison. It does not establish a new induction theory, a general representation-dimension lower bound, or superiority to ordinary probability methods.

## 7. Approximate decisions do not inherit the exact query lower bound

**Hand derivation.** For any fixed \(\eta>0\), choose a positive rational \(a\) with \(|a-\sqrt2|\le\eta\), and let

\[
q=(1,a,-1).
\]

A sign decoder for \(qp\) chooses an optimal action for the approximate losses \((1,a,0)\) and \(B=(0,0,1)\). One signed query supplies that sign in known units; under unknown positive scale, the sign of the single raw value \(sqp\) supplies it as well.

Write \(D=dp\) and \(Q=qp\). If this decoder chooses a strictly suboptimal original action, then \(D\) and \(Q\) have opposite weak signs, including a possible approximate tie. Its original expected-loss regret is therefore

\[
\operatorname{Regret}(p)=|D|
\le |D-Q|
=|\sqrt2-a|p_2
\le\eta p_2
\le\eta.
\]

If its original action is optimal, regret is zero and the same bound holds. Thus exact choice is guaranteed whenever \(|dp|>\eta p_2\), and in particular whenever \(|dp|>\eta\).

With known units, one rational nonnegative row \(q+\mathbf1=(2,a+1,0)\) suffices: subtract one from its expectation before taking the sign. With unknown positive scale, two rational nonnegative rows \((1,a,0)\) and \((0,0,1)\) suffice: their raw difference is \(sqp\).

Consequently the exact irrational-coefficient query counts do not lower-bound the queries needed for every fixed positive regret tolerance. This approximation uses exact expectations of the chosen rational payoffs; no measurement-error guarantee is implied.

The bound is in the original declared action-loss units, independently of the nuisance scale on the readings. If the true action payoffs are repriced by a positive factor \(K\), the same choices have regret at most \(K\eta p_2\le K\eta\). A uniform guarantee in those repriced units must account for that factor.
