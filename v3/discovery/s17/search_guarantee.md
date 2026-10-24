# A finite rational search for the existing certificate parameters

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; conventional search applied
to the explicit N16 families. This makes their computability concrete, not
a new optimization algorithm or a complete-cost superiority claim.

Assume rational 0<C<I, rational E>0 and rational rank-one V>=0 with
tr(V)=1. Write L(t)=tr(V L_t(C)), U(t)=tr(V U_t(C)), and fix a rational
accuracy 0<gamma<1. The theorem's exact endpoints are ell=max L(t) and
u=inf U(t), over t>=h. The [perspective argument](parameters.md) proves
unimodality of these functions: L becomes concave under r=1/(1+t),
and U becomes convex under r=E/t. Monotone reparameterization preserves
unimodality, even though convexity in t is not asserted.

## Rational horizon and cap approximation

The [precision bounds](precision.md) give, for t>=h,

    |L'(t)|, |U'(t)| <= K=E+2,

and truncating the right tail at T>E loses at most E/(T-E) for either
optimized value (the lower bound there is smaller). Set

    T=E+1+4E/gamma.

Then the tail loss is strictly below gamma/4. Since E<h<E+1, bisection
on [E,E+1], using only the exact sign of t^2-E(1+t), finds a rational
a>=h with a-h<=gamma/(4K). The left truncation therefore loses at most
gamma/4. Restriction to [a,T] loses at most gamma/4 in total: an omitted
optimizer is on one side or the other, not on both. The upper limit at
infinity is covered by the same tail estimate.

## Ternary elimination with exact comparisons

On each current interval [b,d], evaluate the objective at
x=(2b+d)/3 and y=(b+2d)/3. Unimodality permits discarding one outer
third according to their exact order; if equal, retain [x,y]. For L
maximize and for U minimize. Every retained interval still contains an
optimizer of the initially restricted problem. Stop when K(d-b)<=gamma/4
and evaluate the midpoint.

The resulting feasible rational parameters t_l,t_u satisfy

    0<=ell-L(t_l)<=gamma/2,
    0<=U(t_u)-u<=gamma/2.                            (S1)

The second quarter is the final interval's Lipschitz loss. All evaluations
are exact rational matrix operations. A sufficient number of elimination
steps for either objective is

    n=max(0,ceil(log(4K(T-a)/gamma)/log(3/2))).

Thus at most4n+2 objective evaluations find both parameters. For fixed E
this is O(log(1/gamma)) evaluations, improving the elementary exhaustive
grid count O(gamma^(-2)) in precision.md. The improvement is standard
unimodal search, credited to ordinary optimization, not a novel component.
Each evaluation can use a k-dimensional rational linear solve for a
rank-one target. The simple developmental implementation uses a full
inverse; it does not claim an optimal arithmetic kernel.

For truthful brackets C_minus<=C<=C_plus with each within operator norm
delta of C, optimize the lower family on C_minus and the upper family
on C_plus. If delta<=gamma/[4(1+T)], the resolvent difference bound in
precision.md adds at most gamma/4 to each error, yielding3gamma/4.
The brackets must remain strictly within (0,I), as the checker requires.
A true strict decision separated from its exact endpoint by gamma can
therefore be certified using these witnesses with unbounded rational
arithmetic. This conclusion does not authenticate the input premises.

## Existing checker limits and finite evidence

The fixed checker allows dimensions up to16 and input rational bit lengths
up to4096. Arbitrarily small gamma, large E or large input descriptions
can exceed those limits. S1 is an arithmetic search guarantee, **not**
completeness of that bounded format. An implementation must reject or return
unresolved when a proposed receipt exceeds its declared limits.

[scalar_search.py](scalar_search.py) leaves the existing checker unchanged.
Its [result](scalar_search_result.json) records three exact screens at
gamma=1/4096. The scalar C=9/10,E=1/100 case is checked against its exact
endpoints900/1069 and900/949. The two existing block examples produce
upper bounds approximately0.5379669054<0.539 and0.5746015412<0.6.
Their exact rational certificates pass the existing checker. Both scalar
objectives together used158,158 and242 denominator inversions respectively.
The three-case run took18,305,700 ns on Python3.12.14 after imports.

Those counts describe this new search's work. They are not reductions
against a complete solver, audit-fee savings or end-to-end CPU gains.
An already good proposed t needs much less checking; ordinary floating
search followed by exact certification may also be cheaper. An identical
conventional implementation ties. The main benefit established here is a
finite, explicit way to find a sufficiently accurate certificate parameter
without trusting a floating optimizer.
