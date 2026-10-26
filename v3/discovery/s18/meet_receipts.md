# An action from incomplete witnesses under meet closure

Codex (GPT-6), s18 DEVELOPMENT. Ordinary Horn model closure, model-based
reasoning and fixed-point propagation are the immediate strong controls.
The proposed information contract is existential, not a list of full models.

Let A={0,1}^d, d>=1. An unknown nonempty feasible set F is closed under
coordinatewise AND of two members. Existing truthful receipts say F meets
each nonempty explicit region T_i; retained B is known to be contained in F.
Assume there is at least one receipt or retained point. For every allowed
selector x_i in T_i, the finite nonempty meet closure of B union{x_i} is a
compatible F. Conversely every compatible F contains such a generated set.
Their intersection is the exact set K of universally feasible actions.

For z other than the all-one vector, define, for each j with z_j=0,

    D_j(z)={x: x>=z coordinatewise and x_j=0}.

Then the exact membership criterion is

    z in K iff for every j with z_j=0,
       B intersects D_j(z) OR some T_i is contained in D_j(z).       (M1)

To see this, a nonempty meet of selected points equals z exactly when the
selected points that dominate z jointly provide a zero in every zero
coordinate of z. Universal quantification over independent selectors makes
each coordinate condition hold precisely when a retained point supplies it
or one entire contact region supplies it. If neither does, select from every
region a point outside D_j(z); no meet can equal z. The condition is therefore
both sufficient and necessary, not just a sufficient closure heuristic.

For top=(1,...,1), a nonempty meet can equal top only if a selected point is
top. Thus top belongs to K iff top is retained or some T_i={top}. Do not
silently allow an empty meet, which would add an unjustified feasible action.

## Partial-coordinate regions and a least-action construction

Suppose T_i is a Boolean subcube, specified by forced-one coordinates P_i
and forced-zero coordinates N_i, with P_i and N_i disjoint. Treat each retained
point as its singleton subcube. Writing Z for the support of z, (M1) becomes

    complement(Z) subset union_{i: Z subset P_i} N_i.              (M2)

Define Phi(Z)=complement(union_{i:Z subset P_i}N_i). It is monotone, and
Z subset Phi(Z) because an active receipt forces every coordinate in Z to
one and therefore cannot force it to zero. Starting from Z=empty, iterate
Phi until stable. Every universally feasible point contains every iterate.
If the fixed point Z* is proper, (M2) shows it is itself universally feasible
and hence the least such point. If Z*=all coordinates, K is empty unless
the separate top test succeeds, in which case top is its least member.

A queue implementation tracks how many active receipts force each coordinate
to zero. When a count becomes zero, set that output coordinate to one and
disable every receipt that does not force it to one; update its zero counts.
This is ordinary monotone propagation, with representation costs explicit.
The note does not claim a new Horn inference algorithm.

For example, three-bit receipts specify (x1=0,x3=1) and (x2=0,x3=1), leaving
the other coordinate unresolved in each. Their unknown feasible witnesses
have a feasible meet001 in coordinate order(x1,x2,x3). No full witness is
retained. By contrast, a single receipt x1=0 on two bits forces no fixed
action: singleton sources{00} and{01} are both compatible.

## Meaning and scope

The closure warrant is essential. An arbitrary nonconvex feasible set can
contain separate witnesses without containing their meet. For a Horn formula
the closure fact is standard, but obtaining the formula, source binding and
truthful contact receipts remains paid. A solver that already returns full
models gives the ordinary control stronger information at little extra cost;
this construction cannot conceal those available vectors to manufacture a gain.
The possible use is a deliberately retained or legitimately value-only
interface, with its actual acquisition/storage contract stated.

No novelty or readiness estimate yet. A close knowledge-compilation screen
comes before implementation. Exact finite checking, if justified afterward,
would test the universal-selector statement and the empty-meet boundary.

The first source comparison finds a direct antecedent for the fixed-model
step: Khardon1995 explicitly tests x in closure(G) by intersecting the
members of G above x. Kautz/Kearns/Selman1993 supplies the Horn closure
representation, and Eiter/Ibaraki/Makino1998 studies intersections of such
represented theories. (M1) is a universal-selector adaptation of that
established membership test. The compact contact input differs from a list
of all selector theories; no absence of a matching title establishes novelty.
