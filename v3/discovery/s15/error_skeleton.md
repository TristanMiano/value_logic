# Sparse exact anchors can correct a structured fallible model

Codex (GPT-6), October 23, 2026. DEVELOPMENT; pass 28.
This is an application of learned error scope, not a new skeleton identity.

Let A(x),B(x) be n-dimensional vectors of polynomials over a field K, each
residual coordinate F_i=A_i-B_i having degree at most D. The model B and
degree warrant are fixed before random training points. Coordinates of A
have a declared paid exact-evaluation interface. Draw training points from
a finite grid S^p, |S|=q>D. The Schwartz–Zippel argument works also over
characteristic-zero K with a finite sampling grid; K need not be finite.
Let V be the span of all residual vectors F(x).

The polynomial range procedure gives a common event, probability at least
1-delta, on which its returned basis U spans V. Once it returns, choose d
linearly independent rows J of U (d=dim U) and invert the d-by-d matrix U_J.
For every future x, including adaptively chosen x, on that common event,

    A(x) = B(x) + U * U_J^-1 * (A_J(x)-B_J(x)).             (1)

The identity follows from F(x) in image(U); it adds no new probabilistic
test or union bound over future inputs. An incorrect scalar prediction at
every coordinate can still permit exact recovery from d paid anchor
coordinates when its residual vectors lie in a d-dimensional space.
This is a structural guarantee, not population-average calibration.

## Cost and failure scope

Training calls for full residual vectors. If s such vectors cost n exact
coordinate evaluations each, that acquisition bill is ns. A subsequent
case needs d exact coordinate evaluations, the model evaluation, and the
matrix arithmetic in (1). In equivalent-coordinate cost units c for those
other operations, a benefit against n direct coordinate evaluations needs
d+c<n and more than ns/(n-d-c) future cases to repay training. Shared batch
evaluation of A, direct symbolic cancellation, low-rank skeleton methods
and a model exposing U for free are stronger controls and must be priced.

For illustration only, n=128,d=4,s=7,c=16 gives a training bill 896 and
per-case bill 20 versus 128; break-even is above 896/108, about 8.30 cases.
These are access-contract arithmetic, not measured CPU or audit-stream
savings. A synthetic oracle that hides a factorization from our method but
gives it to a comparator, or the reverse, would not be a fair comparison.

For ordered rational losses, perform the algebra over the rationals and
charge coefficient bit growth. Finite-field reconstruction alone does not
give an order on real losses or determine an integer without a valid lift
bound. In numerical floating point, conditioning and residual bounds need
separate treatment; exact field identities cannot silently become stable
approximation guarantees.

## Reusing scope after an explicit edit

If a new residual satisfies F'(x)=L*F(x)+G(x), and a separately justified
constant subspace T contains every G(x), then image(LU)+T contains every
new residual. Select independent columns of that known spanning matrix and
new anchor rows; (1) applies with the enlarged basis. No fresh probability
charge is needed on the inherited common event. A model edit within image(U)
is a particularly cheap case. An arbitrary newly trained model outside that
scope cannot inherit the guarantee merely because it predicts better.

Ordinary cross approximation, low-rank correction, polynomial identity
testing and invariant discovery cover the underlying ingredients. The
possible useful synthesis is a paid, adaptive, lifetime correction service
with partial receipts and explicit edit scope. Its complete-cost advantage
and distinction from the closest implementations remain open.
