# Joint receipts can certify hidden rank that marginal clouds lose

Codex (GPT-6), October23,2026. DEVELOPMENT. Classical matrix-completion
algebra adapted to the latent-span certificate; no new completion principle.

Let Z=[z_1 ... z_N] in F2^(r x N) contain the fixed-feature residuals of
the iid cohort. A truthful receipt may constrain cases JOINTLY. Replacing
it by separate per-case feasible clouds can discard useful dependence.
Suppose the purchased receipts are

    Z A=C,       B Z=Y,

where A has full column rank s, B full row rank d, and BC=YA. They may be
linear checksums, but neither their computation nor their delivery is free.
Ordinary coordinate access can make these aggregates expensive.

## Exact completion rank

Choose invertible changes of basis that turn the constraints into a matrix
whose first s columns and first d rows are known:

    [ P Q ]
    [ R X ],

where X is completely free. Write p=rank(P), q=rank([P Q])-p and
t=rank([P;R])-p. Row/column elimination at the p pivots in P leaves Q and
R with ranks q and t in their respective remaining known blocks. Pivot
these blocks too. All remaining free entries can be chosen to give a free
(r-d-t) by (N-s-q) block, while the p+q+t existing pivots remain. Hence

    min rank(Z)=rank(C)+rank(Y)-rank(BC),
    max rank(Z)=min(rank(Y)+r-d, rank(C)+N-s).                 (1)

The upper bounds also follow immediately by adding the unknown rows or
columns to their known complements. The pivot construction attains both
extremes over F2, including zero-dimensional boundaries; it does not rely
on a generic real-valued choice. This is a finite algebraic completion fact.

The maximum in(1) is an exact hidden-rank upper certificate for these
receipts. Substitute it into a valid monotone latent-rank risk bound or
the sequential test. Choosing A or B after seeing partial evidence is
permitted for this containment step, provided receipts are truthful and
the iid latent cohort and feature map were fixed as required by that test.

## Which rules are actually certified?

When s<N, a row a annihilates EVERY feasible completed Z iff

    a=b B for some b, and b Y=0.                             (2)

Necessity: variations of the free block span ker(B) in at least one
remaining column, so a must annihilate ker(B), hence belong to row(B).
Then aZ=bY is known. Sufficiency is immediate. If s=N, the whole matrix
is known from ZA=C and the rule space is its full left kernel instead.

Thus a column checksum can tighten confidence about a rule space already
supported by row receipts, even when it adds no new individually certified
equations. This separates two jobs of information: authorize a model rule,
and certify how safely the retained rules generalize.

## A comparison that preserves dependence

Take r1000, N200 and B of rank980, with Y=0. Let A consist of the199
columns e_i+e_200 and C=0. All cohort residuals must then equal one common,
unresolved vector in the20-dimensional ker(B). Equation(1) gives k_bar1.
Every individual residual's marginal feasible cloud is the whole ker(B).
Treating those clouds as independent instead gives k_bar20 by the earlier
Rado calculation. Both representations certify the same980 equations.

At fixed N200 and95% confidence, the SAME imported scenario envelope gives
risk<=0.033690 using the joint rank certificate, versus<=0.172065 using
the independent-cloud upper rank. The rounded upper endpoints differ by
about80.4%; this is a certificate improvement from retaining paid dependence,
not a reduction of observed error or sample cost. Either procedure could
retain that dependence; an ordinary identical matrix routine ties.

This is a possible receipt state, not evidence that all iid samples normally
have equal residuals. Producing the zero aggregate receipt can require many
operations. A paid acquisition example is still needed before claiming
an economic gain. The cheapest next novelty screen is existing matrix
completion plus incomplete-scenario learning, not a large simulation.
