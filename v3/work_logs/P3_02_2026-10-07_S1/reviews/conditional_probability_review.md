# P3-02 internal review — ratios and conditional probability

Reviewer: **ChatGPT (GPT-6 Astra Pro)**, October 7, 2026 UTC.
Status: **conditional claims accepted after direct proof and boundary checks**.
This is internal same-model, nonblind checking of the principal's proposed
extension. It adds no principal research credit, changes no primary text
or status, and makes no new scientific contribution claim.

## 1. Known units on a convex source

Let \(P\subseteq\Delta_n\) be nonempty and convex. Let \(a,b\) be
known finite real rows such that
\[
bp>0\qquad(p\in P),
\]
and let the target
\[
T(p)=\frac{ap}{bp}
\]
be nonconstant on \(P\). Observe \(y=Lp\) for a fixed known matrix \(L\).
Write
\[
V=\operatorname{span}(P-P),\qquad N=V\cap\ker L.
\]
The proof below also works for any finite-dimensional convex source;
normalization is only needed for the probability interpretation.

### R1 — nonconstant ratio characterization

An arbitrary exact decoder of \(T(p)\) from \(Lp\) exists on all of \(P\)
if and only if
\[
\boxed{ah=bh=0\qquad\text{for every }h\in N.}
\]
Equivalently, both \(ap\) and \(bp\) are individually recoverable from
the known-unit observation.

**Necessity.** Fix \(h\in N\) and \(p\in\operatorname{ri}(P)\).
For all sufficiently small positive and negative \(t\),
\(p+th\in P\) and \(L(p+th)=Lp\). Exact target recovery implies
\[
\frac{ap+tah}{bp+tbh}=\frac{ap}{bp}.
\]
Cross multiplication for any sufficiently small nonzero \(t\) gives
\[
(ah)bp-(bh)ap=0. \tag{R1.1}
\]
This holds at every relative-interior law.

If \(bh\ne0\), equation (R1.1) forces
\[
T(p)=\frac{ah}{bh}
\]
throughout \(\operatorname{ri}(P)\). The relative interior is dense in
\(P\), and \(T\) is continuous at every point of \(P\) because its
denominator is strictly positive there. Thus \(T\) would be constant on
all of \(P\), contrary to the premise. Hence \(bh=0\), after which
(R1.1) and \(bp>0\) imply \(ah=0\).

**Sufficiency.** The ordinary convex-source linear-target criterion shows
that both numerator and denominator are constant on every observation fiber.
Their positive-denominator ratio is therefore constant too. \(\square\)

The obstruction is constructive. If either annihilation condition fails,
there is an interior law where the numerator in
\[
T(p+th)-T(p)
=\frac{t\big((ah)bp-(bh)ap\big)}
       {bp\,(bp+tbh)}
\]
is nonzero. A sufficiently small perturbation gives two admitted laws
with one observation and different target values.

### Affine fractional decoder and full-dimensional probability sources

When the conditions hold, there are affine decoders
\[
ap=\alpha+uLp,\qquad bp=\beta+wLp
\]
on the source's affine hull. Therefore a concrete decoder is
\[
T(p)=\frac{\alpha+uy}{\beta+wy},
\]
with a positive denominator on attainable observations.

On the simplex interior, or on any convex probability source with the same
affine hull, the criterion becomes
\[
a,b\in\operatorname{row}\begin{pmatrix}\mathbf1^\top\\L\end{pmatrix}.
\]
This is a restriction on a fixed linear expectation observation. It does not
say that an arbitrary nonlinear summary cannot simply store the ratio.

## 2. Constant ratios, open sources and zero denominators

### The constant-target exception is essential

If \(ap=k\,bp\) throughout \(P\), the target is the constant \(k\).
Neither numerator nor denominator has to be identified.

For example, on
\[
P=\{(t,t,1-2t):0<t\leq1/2\},\qquad
a=(1,0,0),\quad b=(1,1,0),
\]
the ratio is always \(1/2\), while numerator \(t\) and denominator \(2t\)
vary. No observation is needed for that ratio.

More generally, constant means that the affine function
\((a-kb)p\) vanishes on \(\operatorname{aff}(P)\); it need not mean
that the original ambient rows satisfy \(a=kb\).

### Positivity need not have a uniform margin

Closedness and compactness are unnecessary for R1. In particular, the
conditional-probability domain
\[
\{p\in\Delta_n:bp>0\}
\]
is convex and may exclude a boundary face. Pointwise positivity suffices
for the local perturbation and relative-continuity arguments. It does not
give a uniform stability bound as the denominator approaches zero.

For the full closed simplex, positivity at every law requires every
coordinate \(b_i>0\). On the simplex interior, nonnegative \(b\ne0\)
suffices and allows zero coordinates. A conditional-event row commonly
has such zeros, so the undefined zero-event boundary must be excluded.

Do not replace strict positivity by nonnegativity and silently define
\(0/0\). That changes the target and can invalidate the characterization.
For a concrete attempted weakening, set
\[
P=\Delta_3,\quad a=b=(0,1,2),\quad L=(1,0,0),
\]
and define an artificial extension to be one where \(bp>0\) and zero
where \(bp=0\). This extended target is nonconstant and recoverable from
\(p_1\): it is zero exactly at \(p_1=1\). But \(ap=bp=p_2+2p_3\)
is not recovered. This is not an ordinary conditional probability at a
null event; it demonstrates why R1's denominator premise matters.

## 3. Nonconvex counterexample

Take the catalogue
\[
P=\{e_1,e_2,e_3,e_4\},\quad
a=(1,2,1,2),\quad b=(1,2,2,4),\quad L=(0,0,1,1).
\]
All denominators are positive. The target values at the four laws are
\[
(1,1,1/2,1/2).
\]
They are exactly determined by the observation, with
\(T=1-\tfrac12 y\) on the attainable values \(y\in\{0,1\}\).
Neither numerator nor denominator is constant on either two-point fiber.
Thus convexity cannot be dropped from R1.

Convexifying this catalogue destroys the ratio identification. For example,
\[
p=(1/2,0,1/2,0),\qquad q=(0,1/2,1/2,0)
\]
both have \(Lp=Lq=1/2\), but
\[
T(p)=2/3,\qquad T(q)=3/4.
\]
The correct general rule for nonconvex sources remains literal constancy
of the ratio on every complete observation fiber.

## 4. Conditional probability from a partial linear observation

Use three states: the first is in events \(A\subseteq B\), the second
is in \(B\setminus A\), and the third is outside \(B\). Then
\[
a=(1,0,0),\qquad b=(1,1,0),\qquad
T(p)=P(A\mid B)=\frac{p_1}{p_1+p_2}.
\]
Use the domain \(P=\{p\in\Delta_3:p_1+p_2>0\}\), and observe the known
loss row
\[
L'=(2,0,1).
\]
Normalization gives
\[
y=2p_1+p_3=1+p_1-p_2.
\]
Put \(d=y-1=p_1-p_2\) and \(m=p_1+p_2>0\). Every compatible law has
\[
p=\left(\frac{m+d}{2},\frac{m-d}{2},1-m\right),
\qquad |d|\leq m\leq1,\quad m>0,
\]
and
\[
T=\frac12+\frac{d}{2m}.
\]

### The proposed observation \(y=6/5\)

Here \(d=1/5\) and \(1/5\leq m\leq1\). Hence the sharp conditional
range is
\[
\boxed{3/5\leq T\leq1.}
\]
The lower endpoint is attained at
\((3/5,2/5,0)\), and the upper at \((1/5,0,4/5)\).
Both laws have the same observation \(6/5\).

The threshold \(T>1/2\) is settled even though the ratio itself is not:
\[
\left(a-\frac12b\right)p=\frac12(p_1-p_2)=1/10>0.
\]
The denominator is positive, so this is the desired strict ratio inequality.
The sharper lower bound is also affine-certifiable on the fiber:
\[
\left(a-\frac35b\right)p=\frac1{10}p_3\geq0.
\]
The upper bound follows from \(ap\leq bp\). These tests need only
known rational coefficients and a justified positive-denominator premise;
they do not require a native variable-division operation.

### Zero difference and the other observation boundaries

For \(d=0\), the admissible fiber has \(p_1=p_2>0\), so \(T=1/2\)
exactly while both numerator and denominator vary. For example,
\((1/4,1/4,1/2)\) and \((1/2,1/2,0)\) share \(y=1\), with different
numerator/denominator values and the same ratio. This is a **locally
constant target**, which is precisely R1's exception after restricting
the source to that fiber. The excluded law \(e_3\) would instead make
the conditional probability undefined.

The complete sharp ranges are
\[
\begin{array}{c|c}
-1\leq d<0 &[0,(1+d)/2]\\
d=0 &\{1/2\}\\
0<d\leq1 &[(1+d)/2,1].
\end{array}
\]
At \(d=-1\) and \(d=1\), the fiber is the pure second or first state,
respectively. Values \(|d|>1\) are incompatible.

There is a real stability boundary at \(d=0\). For arbitrarily small
\(\epsilon>0\), laws \((\epsilon,0,1-\epsilon)\) and
\((0,\epsilon,1-\epsilon)\) have observations \(1+\epsilon\) and
\(1-\epsilon\), yet conditional probabilities one and zero.
Thus an arbitrarily small positive observation-error band around \(y=1\)
admits the whole conditional range \([0,1]\) unless extra denominator
information is retained. Explicitly, for \(0<\epsilon\leq1\) and any
\(r\in[0,1]\), the law
\((\epsilon r,\epsilon(1-r),1-\epsilon)\) has ratio \(r\) and
\(|y-1|\leq\epsilon\). This does not refute exact local identification.

## 5. Unknown common scale: the sharpened criterion

Now observe
\[
v=sLp,\qquad s>0
\]
with unknown common scale, retaining the same nonconstant ratio target.
The correct general convex-source direction space is
\[
W=\operatorname{span}(P),
\]
not just \(V=\operatorname{span}(P-P)\).

### R2 — general convex source under unknown positive scale

The target is globally recoverable from \(sLp\) for every \(p\in P\)
and \(s>0\) iff
\[
\boxed{ah=bh=0\qquad(h\in W\cap\ker L).}
\]

**Proof by homogeneous coordinates.** Define the positive cone
\[
C_+(P)=\{sp:s>0,\ p\in P\}.
\]
It is convex: a convex combination of \(s_1p_1\) and \(s_2p_2\) can be
written as a positive total scale times a convex combination of \(p_1,p_2\).
It does not contain zero. Its affine direction space is \(W\), since
every \(x\in C_+(P)\) is the difference \(2x-x\) of two cone points,
and the cone spans the same space as \(P\).

For \(x=sp\), the observation is \(Lx\), \(bx>0\), and homogeneity gives
\[
T(p)=\frac{ax}{bx}.
\]
Apply R1 to this convex homogeneous-coordinate domain. Its hidden space
is \(W\cap\ker L\), which proves the claim. \(\square\)

The quotient representation here is linear rather than affine:
\[
a|_W=u(L|_W),\qquad b|_W=w(L|_W).
\]
It yields
\[
T=\frac{uv}{wv},
\]
where \(uv=sap\) and \(wv=sbp>0\). These are the **scaled** numerator
and denominator. The theorem does not assert recovery of the unscaled
expectations \(ap,bp\).

### Full-dimensional probability source

On the simplex interior, or another full-affine-dimensional convex
probability source, \(W=\mathbb R^n\). Thus
\[
\boxed{T\text{ recoverable from }sLp
\iff a,b\in\operatorname{row}L.}
\]
There is no additional requirement that the constant row belong to that
span. One can also verify necessity directly: normalize \(p+th\) for
\(h\in\ker L\), adjust the scale by its total mass, and observe that
the normalization cancels from the ratio. The cross-multiplied identity
(R1.1) again forces both rows to annihilate the kernel.

Setting \(b=\mathbf1^\top\) makes the ratio the linear probability target
\(ap\), and this criterion becomes exactly PI-10:
\(\mathbf1^\top,a\in\operatorname{row}L\). Thus the extension sharpens
the target distinction without contradicting the linear-target result.

## 6. Conditional information survives without calibrating the scale

For the conditional-event rows
\[
L=\begin{pmatrix}1&0&0\\1&1&0\end{pmatrix}
=\begin{pmatrix}a\\b\end{pmatrix},
\]
the constant row is absent from \(\operatorname{row}L\). Nevertheless,
\[
v_1=sp_1,\qquad v_2=s(p_1+p_2)>0,\qquad
P(A\mid B)=v_1/v_2.
\]
The conditional ratio is globally identified on the positive-event domain
and is nonconstant there. The common scale itself need not be identified.

For example,
\[
p=(1/4,1/4,1/2),\ s=2,\qquad
q=(1/8,1/8,3/4),\ t=4
\]
give the same observation \(v=(1/2,1)\). Their unscaled numerators and
denominators differ, but both conditional probabilities are \(1/2\).
This does not violate R1, whose known-unit observation would be \(Lp\);
the homogeneous-coordinate quantities individually recovered here are
\(sap\) and \(sbp\).

Nor does it violate PI-10: a conditional ratio is not a nonconstant linear
functional of the normalized law. The same interior perturbation behind
PI-10 still obstructs global recovery of nonconstant linear law targets
on this full-affine-dimensional conditional domain.

## 7. Validation and disposition

Exact standard-library rational calculations checked:

- The four nonconvex catalogue ratios and the \(2/3\) versus \(3/4\)
  collision introduced by convexification.
- The \(y=6/5\) endpoint laws, their sharp ratios \(3/5,1\), and the
  affine lower-bound identity.
- Two \(y=1\) laws with different numerator/denominator values but ratio
  \(1/2\).
- The unknown-scale collision \(v=(1/2,1)\).

Both proposed characterizations are accepted with strict denominator
positivity on the actual domain, a nonconstant target, a convex source and
the stated scale quantifiers. Neither requires a closed source, a uniform
positive denominator lower bound, or a polyhedral boundary.

The relevant result is exact information recovery. The ratio decoder,
finite precision, threshold certification and empirical accuracy remain
separate implementation or evidence contracts. All calculations and
counterexamples here are development material.
