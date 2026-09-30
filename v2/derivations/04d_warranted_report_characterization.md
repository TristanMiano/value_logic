# F08 optional application: the least warranted report under a fixed control law

Research contributor: **Codex (GPT-6)**, September 30, 2026 UTC.
Status: accepted F08 derivation; scoped bounded reflection, not unrestricted
self-soundness. This extends the F06/F07 report example without changing its
native rules or treating empirical calibration as a logical axiom.

## 1. The model and the query must stay explicit

Let p,s be two P-valued source probabilities. A reported number r in [0,1]
also controls a fresh mixture with modeled failure probability

    H_r(p,s)=(1-r)*p+r*s.                            (R)

The branch laws and the mixture interpretation are fixed. R is a supplied
operational model; it does not follow from the syntax of a report or from an
agent's belief about itself. A fixed rational r gives an admitted affine term.
The report is warranted in the modeled source when H_r<=r throughout it.
Changing r changes the query's literal coefficients, so an old proof object
cannot be accepted as a proof of the new report without reconstruction.

For native warrants, use the P-reduct's joint projection onto (p,s). Require
that the accessible source rows imply 0<=p,s<=1. Its projected domain Q is a
nonempty finite union of rational compact polytopes. This follows from finite
rational projection together with the probability bounds. Let V be the finite
union of their vertex sets; lower-dimensional cases are included.

Q is the source for the following theorem. If every useful original premise
is accessible in P, Q is the full source projection. Otherwise a separating
model can belong only to the reduct: the result characterizes native warrants,
not an automatic refutation of the more constrained full model.

## 2. Exact least report, including the zero-denominator corner

For v=(p_v,s_v) define

    d_v=1+p_v-s_v.

The probability box implies d_v>=p_v>=0. It vanishes exactly at (p_v,s_v)=(0,1).
That corner satisfies H_r=r for every r and imposes no inclusive restriction.
Do not divide by its zero denominator.

For vertices with d_v>0, rearranging the requested inequality gives

    H_r(v)-r = p_v-r*d_v <=0
       iff r>=p_v/d_v.

For a fixed r this is an affine source inequality, so it holds on each
polytope exactly when it holds at all its vertices. Define

    r_* = max({0} union {p_v/d_v : v in V, d_v>0}).  (R*)

Every ratio is rational and between zero and one. Thus r_* is rational,
and the complete interval of warranted reports is [r_*,1]. This proof uses
vertices of the bounded probability projection, not an assumption that the
original source with nuisance coordinates has a vertex.

An alternative check of the ratio argument is useful near the degenerate
corner. If a point is a convex combination of vertices, its p and d are the
same combination of their p_v and d_v. Vertices with d_v=0 also have p_v=0.
Where d>0, p/d is therefore an average of the positive-denominator vertex
ratios with weights proportional to their d_v. It cannot exceed their maximum.
No continuity of the ratio at (0,1) is assumed or needed.

**Corollary U14 (least native warranted mixture report).** Under these fixed
finite probability-source assumptions, rational r has a native zero-budget
proof of `H_r<=[0]r_P` exactly when r is in [r_*,1]. At r_* such a proof exists.
For rational r<r_*, a rational vertex attaining R* gives a strict violation
`p_v-r*d_v>0`; rational back-substitution lifts it to its source case.

Native proof existence follows from U1's constructive affine consequence,
including explicit directed conversion/grafting of usable premises. The
calculation of r_* is outer mathematical analysis; it adds no native
variable-multiplication or division rule. Each returned report certificate
still concerns one fixed rational r and the actual current request.

## 3. Strict reporting and a boundary that cannot be ignored

If Q contains (0,1), every r has a source model with H_r=r, so no strict report
H_r<r is valid. A report larger than r_* does not fix this boundary.

If Q excludes (0,1), all vertex denominators are positive. For r>r_* every
vertex has a negative gap, and a uniform margin is at least

    (r-r_*)*min_(v in V) d_v >0.

At r=r_* some vertex has zero gap, including when r_*=0, because V is finite
and nonempty. Hence, within [0,1], the strictly warranted reports are exactly
`(r_*,1]` when Q excludes (0,1), and none when Q contains it. In particular,
if r_*=1 the strict set is empty. This agrees with U5's attained-bound result;
it does not replace a strict request by an inclusive one silently.

## 4. Shared evidence matters: marginal caps can double the required report

Suppose Q is the segment `p+s=1`, 0<=p<=1. Its vertices are (1,0) and (0,1).
The first gives ratio 1/2 and the second imposes no inclusive condition, so
r_*=1/2. Directly, H_(1/2)=(p+s)/2=1/2. The P-valued row p+s<=1 supplies a
native certificate by scaling by 1/2; the reverse inequality is unnecessary
for that upper bound. A vertex with p=1 refutes every r<1/2.

The separate marginal caps p<=1 and s<=1 permit (1,1), which instead forces
r_*=1. Thus a summary retaining only those caps loses precisely the joint
constraint needed for the stronger self-assessment. Both domains contain
(0,1), so neither permits a strict report under R. The result is conditional
on the shared source law, not an assertion of statistical independence.

For the earlier rectangular example 0<=p<=1, 0<=s<=1/4, the largest ratio is
at (1,1/4), giving r_*=4/7. Its native proof combines the p and s cap rows
with weights 3/7 and 4/7. At r=7/16 the same corner gives gap 15/64, reproducing
the F07 failed report update. The characterization explains those constants
as a least-warrant boundary rather than a new fixed-point rule.

## 5. Least warranted report and best modeled loss are different questions

If the declared criterion is worst-case loss

    J(r)=sup_(p,s in Q) [w*H_r(p,s)+c*r],

with fixed rational w>0 and c>=0 in the declared loss unit, then

    J(r)=max_(v in V) [w*p_v+r*(w*(s_v-p_v)+c)].     (J)

This is a finite convex piecewise-affine function of the *outer* parameter r.
It attains its minimum over the warranted interval [r_*,1] at a rational
endpoint or an intersection of two of its affine pieces (a flat interval
also contains such a candidate endpoint). Evaluating that finite candidate
set identifies a robust-loss-optimal warranted report. One can then emit the
fixed-report native certificates. This does not assert an implemented report
optimizer, native bilinear arithmetic, or an empirical guarantee for w,c,Q.

The two notions need not coincide. At the single model (p,s)=(1,0), r_*=1/2.
For w=1,c=1/10, J(r)=1-9r/10, so the cost-optimal warranted controller uses r=1.
For c=2, J(r)=1+r, so it uses r=1/2. A least upper report is not a universal
value criterion or a requirement to choose the least fallback probability.

Nor does a smaller worst-case loss prove pointwise improvement over an old
controller. On the two models (9/10,1/10) and (1/10,9/10), r_*=1/2. With c=0,
switching from r=3/4 to r=1/2 improves J from 7/10 to 1/2. At the first model,
however, failure probability rises from 3/10 to 1/2. The paired change there
is +1/5. A native uniform-improvement request must therefore fail, even though
the declared robust-objective optimization succeeded. F07's distinction
between current paired guarantees and other comparison criteria remains live.

This application gives a concrete bounded reflective consequence of F08's
characterization. It does not establish that the agent knows all premises,
that its announced risk is empirically calibrated, or that the model remains
correct when its report changes the branch laws or observation process.
