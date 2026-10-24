# A finite budget for substantial correction witnesses

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass37.
The determinant mechanism is established reduced-basis machinery; see
DeVore–Petrova–Wojtaszczyk, Lemma2.1 and Theorem3.2, in literature.md.

Suppose every possible error vector v has ||v||<=B and lies within epsilon
of one fixed, unknown r-dimensional space R. Starting from U=0, add a
checked vector v only when dist(v,U)>tau, where tau>epsilon. This is a
threshold rule; no maximization over all possible witnesses is assumed free.

After m additions the Gram determinant of the selected vectors exceeds
tau^(2m), by Gram–Schmidt. Their matrix V has Frobenius norm squared at
most mB^2, and a rank-r approximation with squared Frobenius error at most
m*epsilon^2. AM–GM on the first r and remaining m-r squared singular values
therefore gives, for m>r,

    tau^(2m)
      < (m*B^2/r)^r * (m*epsilon^2/(m-r))^(m-r).     (1)

This is the familiar determinant comparison, reconstructed here to expose
the correction budget. It bounds the number of additions independently of
ambient dimension. For t=(tau/epsilon)^2>1 and b=(B/epsilon)^2, a looser
explicit consequence is

    m <= max(r, [2r/log(t)]*log[2b/log(t)]),         (2)

when B>=tau and epsilon>0. Indeed (1) implies
m*log(t)<=r[1+log(mb/r)], and
log(y)<=y*log(t)/2-1+log(2/log(t)). If B<=tau there are no additions;
if epsilon=0, exact rank gives at most r.

## An exact finite-budget example

Let r=4, B=1, epsilon=1/100 and tau=1/20. The right side of (1) divided
by its left side is above1 at m=14 and below1 at m=15 (about.0643738).
These comparisons are exact rational-power calculations, not a simulation.
The logarithm of that ratio has derivative

    log[m*epsilon^2/((m-r)*tau^2)],

which is negative for every m>=5. Thus there can be at most FOURTEEN
above-tolerance additions. If fourteen occur, no further vector in the
promised family can violate the tolerance. Earlier failure to find a witness
does not by itself certify that none exists.

The norm bound and strict margin matter. With tau<epsilon, arbitrarily many
orthogonal noise vectors can trigger additions even when r=0. With no bound
on vector norms, increasingly large components along R can expose small
angular errors repeatedly. A finite-dimensional ambient-space cap remains,
but the useful small correction budget is then absent.

## What this enables, and what it does not

The bound can replace exact rank in accounting for genuine substantial
correction witnesses. It gives a route from an approximate model class to
a finite amount of learned correction structure. Fourteen is a number of
accepted witness updates, not a bound on the number or price of attempts
needed to find them.

It cannot simply replace r in private_repairs.md. A tolerant point test lacks
the exact one-sided identity guarantee, and an invalid SOS certificate need
not expose an above-tolerance witness. Those separate obligations remain in
tolerant_checks.md. The strongest ordinary reduced-basis method has the same
determinant guarantee. No new convergence claim, measured savings or promotion
is inferred from this adaptation.
