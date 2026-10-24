# A stronger scalar control for the shared-source contrast

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; a conventional variational
comparison reconstructed here. This further limits the apparent gain of
[the relative certificate](relative_pair.md).

Let w=(I+MM^T)^(-1)v, b=M^T w, s=||w||^2+||b||^2>0 and
m=||w||^2/s in [0,1]. For a unit-norm edit, retaining b as a trial primal
solution gives

    f_0/s <= A(m)=2-m+2*sqrt(m*(1-m)).

Scaling w in the quadratic dual and optimizing its scalar coefficient gives

    f_1/s >= 1/B(m),  B(m)=1+m+2*sqrt(m*(1-m)).

These follow directly from ||v-N_0 b||<=||w||+||b|| and
||N_1^T w||<=||b||+||w||. They require no assumption that a trial solution
remains optimal after the edit. Also, the ordinary two-edit ratio bound
f_0<=b_* f_1 holds with b_*=3+2*sqrt(2). Thus

    (f_0-f_1)/s <= H(m)
       := A(m)-max(1/B(m),A(m)/b_*).                  (C1)

Optimizing this scalar expression over the unknown m provides a valid
universal control even when m itself is not retained. The point is the
stronger inequality, not credit for extra information.

## Exact scalar maximum

Put

    z_*=(sqrt(5*b_*-1)-3)/5,
    m_*=(1-sqrt(1-4*z_*^2))/2,
    G_*=[2-m_*+2*z_*]*(1-1/b_*).

Then max H(m)=G_*, approximately **2.1668350851**.
To verify it, write z=sqrt(m*(1-m)). Direct multiplication gives
A(m)*B(m)=2+6*z+5*z^2. This product increases on [0,1/2] and equals
b_* at m_*. Simple rational square comparisons put m_* between .30 and
.31: at .30 use sqrt(.21)<.459, and at .31 use sqrt(.2139)>.462,
together with 1.414213<sqrt(2)<1.414214.

For m<=m_*, H(m)=A(m)-1/B(m). Set
xi=(1-2m)/sqrt(m*(1-m)). On 0<m<=.31, xi>=19/25 and B<=231/100.
Consequently

    H'(m)=xi-1+(xi+1)/B^2
      >= -6/25+(44/25)*(100/231)^2 >0.

For m>=m_*, H(m)<=A(m)*(1-1/b_*). The function A decreases after its
maximum at (1-1/sqrt(5))/2<.30. Hence this last bound is at most its
value at m_*, proving the global maximum. The expressions agree there.
Endpoint continuity handles m=0 and m=1. Reversing the edits proves the
same absolute-value control.

The [numerical screen](pair_control.py) and [result](pair_control_result.json)
first located this crossing and the weaker primal/dual-only maximum
2.1702448015. It used two scalar optimizations, taking 410,600 ns on
Python 3.13.14. Its decimals alone were not a global bound; the above
monotonicity proof supplies that claim.

## Revised comparison

The exact relative coefficient 2.1596506315 improves G_* by about
**0.33156%**, rather than the 0.42418% comparison against the simpler
triangle/ratio coefficient. The latter remains a correct weaker comparison.
Both controls are ordinary deductions, and an exact joint Gram optimization
is stronger still. None of these percentages measures saved computation.

This is a useful example of why a contribution assessment should keep
strengthening the comparator. The near-optimal rational joint inequality
survives this particular stronger control, but the comparison does not
establish that no published analytic inequality already supplies it.
# Later comparison

The [exact ordinary diameter](pair_radius.md) is stronger than this
primal/dual-reuse control and the earlier rational SDP coefficient. Preserve
the computations below, but use zero positive advantage against that strongest
comparison in the final assessment.
