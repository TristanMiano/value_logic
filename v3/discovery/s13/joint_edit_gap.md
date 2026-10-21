# Correct local edit values need not compose

Codex (GPT-6), DEVELOPMENT, October21,2026. A constructive limit for the
numerical route in numeric_edits.md, using ordinary matrix identities.
No application, new lower-bound technique or numerical speedup is claimed.

## Even every proper intervention subset can agree

Fix r>=3 edit ports, a boundary coordinate0 and input/output b=c=e0.
Define two symmetric port matrices V+ and V- with diagonal2, magnitude1/2
on the edges of an r-cycle, and zero elsewhere. Every cycle edge in V+ is
positive; V- flips exactly one cycle edge's sign. Both are positive definite:
the sum of off-diagonal magnitudes in any row is1, strictly below2.
Let g=e1 on the port coordinates and set

    R+ = [[10,g^T],[g,V+]],    R- = [[10,g^T],[g,V-]],
    A+ = (R+)^(-1),           A- = (R-)^(-1).

Both R are positive definite, since V>=I and the Schur complement
10-g^TV^(-1)g is at least9. These are two admissible full models with the
same physical b,c and port selectors; no input is silently changed between
models. They share the boundary value y(0)=10.

For diagonal nonnegative port edits D, Woodbury gives

    10-y(D)=g_S^T(D_S^(-1)+V[S,S])^(-1)g_S,

where S is the strictly positive support of D. An empty S gives zero.
If S is a proper subset, the cycle restricted to S is a forest. Its two
signings differ by a diagonal sign gauge T: V-[S,S]=T V+[S,S] T. If port1
is in S, choose the gauge of its component so T_11=1. Other components do
not affect g_S. T commutes with D, so the displayed scalar is identical in
the two models for *every choice* of positive edit strengths on that S.
If port1 is absent, g_S=0 and both changes vanish. Thus even unlimited
exact value observations on every proper subset cannot distinguish them.

For a full-support edit D=tI, t>0, the numerator of the (1,1) inverse entry
is a principal cofactor that deletes one vertex and leaves a path. It is
independent of cycle-edge signs. The two determinants differ: the two
oriented full-cycle permutation terms contribute
2*(-1)^(r-1) times the product of all off-diagonal cycle entries; flipping
one edge flips that nonzero contribution. All other determinant terms use
only diagonal entries and squared edge magnitudes. Consequently the full
edit values differ. Positive definiteness keeps both denominators positive.

For r3 and t1, the reductions 10-y are7/20 and5/14, respectively. Every
single and pair edit agrees for arbitrary nonnegative strengths, but the
triple does not. A threshold between the two values yields different
decisions. The distinction can be amplified by scaling the input/output
or the declared stakes; scaling also changes the acquisition/error units.

## What this changes about the candidate

A bounded number of simultaneous edit coordinates is a real adequacy scope.
Accurate marginal or pairwise intervention values do not warrant a newly
combined operation, even in a smooth, linear, positive-definite system.
The rank-bounded *one-parameter family* from numeric_edits.md is different:
its2r observations vary the strength of the same combined edit, and so can
expose the cycle interaction. They are not obtained for free from separately
calibrated coordinate curves.

This is generic SPD algebra; the negative off-diagonal port responses mean
it is not automatically a valid claim about every nonnegative electrical
network model. Known coordinate-sign gauges and cycle products are ordinary
linear-algebra/graph notions. The useful delta here is an explicit failure
of a proposed local-value composition rule, with its corrected acquisition
scope. No large experiment or new numbered family is warranted.

Prospective cheap screen: exact rational solves on r3 throughr6, all edit
strength vectors in{0,1,2}^r. Check full matrices are SPD, proper-support
values agree, full-support values differ, and the port formula matches a
direct solve of each edited full matrix. Expected under30seconds. This
checks the construction rather than estimating a prevalence or a saving.

The first numeric_probe.py execution passed:4 panels,1080 edit vectors,
960 proper-support equalities,120 full-support differences,2160 direct full
solves and2152 port solves. Rational arithmetic took1.4557636seconds. The
probe checks the cycle construction and compression identity; it does not
execute the2r interpolation or the noisy LP from numeric_edits.md. Source
hashb1a9a3a88349b04f0082c0902b948f9ac319f4a944d6bf632f6cae18f6aef541.
