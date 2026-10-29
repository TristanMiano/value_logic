# A scalar measurement duty for the exact-range construction

Codex (GPT-6), October 28, 2026. DEVELOPMENT; constructed example,
not observed deployment data. This supplies a more explicit use contract for
V19-R/v1 without changing its contribution event.

## Observation contract

A static response is an upper envelope of independently uncertain affine
pieces: h(z) = max_i (theta_i dot phi(z)). Each theta_i has a supplied compact
rational polytope B_i, which may differ across pieces. At k chosen inputs z_j,
only a bounded-error scalar measurement of h is available. The physical
measurement does not expose which piece produced the envelope. The task is
to retain all model predictions at a new fixed z_star, for later consistency
or forbidden-band queries. Negate every affine response and measurement
interval to obtain exactly the V19 input contract.

This is a conditional set-membership prediction problem. The number and form
of pieces, their fixed parameters, individual bounds, and measurement-error
bounds are assumptions to criticize, not conclusions of the algorithm. An
empty intersection with a new report rejects their conjunction; it does not
identify which assumption failed. No probability of correctness follows from
the geometric computation.

The scalar-only restriction here need not be a storage policy that carelessly
discarded a cheap winner label. A sensor for an aggregate maximum or a black-box
value interface may never supply that label. Conversely, if individual pieces
or winning labels really are cheaply available, include them: conditioning on
that richer information can be substantially easier. This is an intended
interface, not evidence that any particular deployed sensor satisfies it.

## Two affine pieces in one input variable

Parameterize a piece by its responses u_i at z=-1 and v_i at z=1:

    h_i(z) = ((1-z)/2) u_i + ((1+z)/2) v_i.

Let 0 <= u_i,v_i <= 1, with different midpoint calibration strips

    c_i-delta <= u_i+v_i <= c_i+delta,
    c_1=6/5, c_2=9/5.

The local polytopes are two-dimensional for delta>0 small enough. Observe

    1-epsilon <= max(u_1,u_2) <= 1,
    1-epsilon <= max(v_1,v_2) <= 1.

If c_2+delta < 2(1-epsilon), neither piece can witness both lower observation
bounds. Exactly two witness assignments remain: piece 1 witnesses u and
piece 2 witnesses v, or the reverse. Nonzero error and full-dimensional
parameter sets therefore need not connect these alternatives.

At z_star=2, h_i(2)=(-u_i+3v_i)/2. For a piece with c=c_i:

- In its u-witness slice, u in [1-epsilon,1] and
  v in [c-delta-u,c+delta-u], provided the box bounds do not clip those
  endpoints. Its prediction interval is
  [(3(c-delta)-4)/2, (3(c+delta)-4+4epsilon)/2].
- In its v-witness slice, v in [1-epsilon,1] and
  u in [c-delta-v,c+delta-v], with the same proviso. Its prediction interval
  is [(4-4epsilon-c-delta)/2, (4-c+delta)/2].

For epsilon=delta=1/100, the endpoints lie inside the local boxes. The
u-witness interval of each piece lies strictly below the other piece's
v-witness interval. Independence then makes the envelope prediction equal to
the v-witness interval in each assignment. Hence the exact predicted set is

    [43/40,221/200] union [11/8,281/200]
      = [1.075,1.105] union [1.375,1.405].

A new report [6/5,5/4] is incompatible, although the sharp interval hull
[43/40,281/200] admits it. The distance of the exact set from 5/4 is 1/8,
so |1/(h(2)-5/4)| <= 8 for every compatible model. The sharp interval hull
cannot certify a finite reciprocal bound. This is a worked conditional
decision consequence, not a measured saving or a model identification theorem.

## Strong ordinary controls and the resource duty

Direct mixed-integer or disjunctive feasibility with the new band rejects
the same report. For one band, constructing all gaps may be wasteful. Sharp
endpoints suffice for all scalar convex worst-loss decisions, including
absolute and squared error. The proposed answer object is useful when the
output contract itself requires every possible value, or when a fixed future
readout serves many later band/threshold/nonconvex queries. Changing z_star
changes the LP objectives and generally requires new extrema.

After a sorted disjoint union with m components is available, intersection
with a closed query band and distance to a point take O(log(m+1)) endpoint
comparisons. A witness query also pays for selecting stored backpointers,
reconstructing n local parameter vectors, and exact interpolation. Its output
length is not free. The input acquisition and the parameter/measurement bounds
are common costs; full-range preparation pays up to 2*n*2^k local LPs, its
subset-combination work, retained certificates and verification.

An ordinary implementation can cache these same local extrema and use the
same anchored formula. It ties. A generic MIP control can instead answer each
band adaptively and may be faster on particular instances. No uniform or
empirical speedup is claimed. The proposed mathematical delta is an explicit
fixed-parameter, certifiable whole-range algorithm under the specified
factorization, not the invention of set-membership prediction or model
falsification.

For n>=k with identical piece bounds and identical response maps, the easier
homogeneous result in s19 remains a necessary control. The calibration strips
above deliberately differ, so that shortcut does not apply. This example
justifies a nonvacuous heterogeneous contract; it does not establish the
frequency or economic importance of heterogeneous instances in practice.

## A precise reusable-answer interface

One bounded duty is an offline/online consistency service. Fix the original
model, old observations and future readout before answering a sequence of
closed rational bands B_1,...,B_q. The bands may arrive adaptively. Preparation
produces a normalized interval union and a complete local certificate. A
consumer first verifies that certificate against the original input, then
answers whether each B_t intersects the union by endpoint search. On a YES
answer it may request a full compatible source; on a NO answer the already
checked complete union is the exclusion evidence. The service never infers
which model premise is false from a NO answer.

The online query count q, band bit lengths, endpoint comparisons, certificate
verification and requested witness lengths all belong in its resource bill.
Preparation is worthwhile only when required by this complete-answer contract
or justified by the anticipated queries. A conventional solver offering the
same verified compiled object is an equal control. The contribution is the
explicit compilation and certificate bound, not a new statistical guarantee,
cryptographic proof system, or assertion that caching itself is novel.

The local endpoint tables are sufficient for every such fixed-readout band
question: replacing the individual slices by other compact convex slices
with the same indexed scalar images leaves the anchored union unchanged.
They need not preserve the parameter source or predictions at other inputs.
The normalized union is the smaller sufficient answer for scalar band queries;
the larger certificates and backpointers are retained for checking and source
recovery. This separates answer size from evidence size rather than crediting
the final interval list as the entire memory bill.
