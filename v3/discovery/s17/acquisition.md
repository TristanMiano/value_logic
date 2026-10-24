# The worked decision from unfinished old solves

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; one exact interface check.
This uses conventional primal-dual bounds and the existing polarization
adapter. It is part of reviewing the decision's premises, not a new theorem.

For an old source M and any proposed vectors x,w, completion of squares gives

    2 v^T w-||w||^2-||M^T w||^2 <= F(M;v)
                                      <= ||v-Mx||^2+||x||^2.

Neither vector needs to be optimal. The products with M and M^T and their
arithmetic must actually be performed or otherwise truthfully certified.
The external source binding is a separate premise of the small checker.

For the three-dimensional version of the cancellation example take
M=diag(40,1/3,40), W=[e1,e2]. For each z in {(1,0),(0,1),(1,1)}, choose

    v=Wz,
    x=(z1/40, 3z2/10, 0),
    w=(z1/1600, 9z2/10, 0).

These simple rational candidates give exact intervals for the three old
values. The first interval is [1599/2560000,1/1600], the second is exactly
9/10, and the pair interval is the first shifted by 9/10. No exact inverse
or exact optimizer is used to form these intervals.

Polarization of their midpoints has zero off-diagonal entry. The established
row-sum error adapter gives matrix half-width 1/2560000. Feeding that bracket,
V=cc^T with c=(1,1)/sqrt(2), E=9, t_lower=10, t_upper=100 and threshold 3/5
to the unchanged s16 checker produces

    upper = 6638538943999339100 / 11472231479226969481
          = 0.578661523350... < 3/5.

[acquisition_check.py](acquisition_check.py) and its
[record](acquisition_result.json) passed this exact pipeline in 446,700 ns.
The separate analytic exact values in the script only audit the intervals;
they do not construct the receipt. The acquisition code makes six matrix-
vector calls (one of each orientation per query), followed by scalar and
small-matrix arithmetic. Shared calculations or a direct small solve can
be cheaper on this deliberately simple fixture. These counts and this run
are not a comparative speedup or a full service price.

The earlier rounded-bracket result 0.583119 remains useful because it tolerates
a substantially wider input error. This new result verifies that an actual
primal-dual acquisition path can meet the decision contract without exact
old optimization. The guarantee is still conditional on the source, target
and edit warrants; the small checker does not authenticate them. A future
application must account for those duties rather than treating the three
intervals as free observations.
