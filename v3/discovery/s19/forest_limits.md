# What forest structure does and does not make easy

Codex (GPT-6), October26,2026. DEVELOPMENT; cheap constructive boundaries.

## Best receipt withdrawal can be hard on a star

The forest algorithm assumes all retained receipts are admitted. It does
not automatically optimize which fallible receipts to discard. With one
configuration, every receipt is a single affine halfspace and the incidence
graph is a star. Selecting a maximum-weight consistent subcollection is
the established maximum feasible subsystem problem, not an LP.

An explicit Boolean reduction makes the distinction visible. Let one
source block be x in[0,1]^d. For each variable include the two endpoint
receipts x_i<=0 and x_i>=1, each of weight M. They cannot both hold; an
interior coordinate satisfies neither. Encode each Boolean clause by the
halfspace sum of its literal values >=1, with unit weight. Choose M larger
than the number of clauses. Any maximum-weight feasible source has every
coordinate at an endpoint: rounding an interior coordinate to either
endpoint gains M and loses at most all clause weights. At Boolean points,
the retained clause score is exactly the number of satisfied clauses.

Each halfspace can be written as a one-configuration interval receipt by
using its affine residual and an automatic sufficiently low lower bound.
Thus maximum-weight retained receipt consistency includes weighted
MAX-SAT already at cycle rank zero, when local dimension is unrestricted.
This does not contradict polynomial feasibility of a fixed retained set
or fixed-dimensional arrangement methods. It is an ordinary reduction,
not a claimed novel complexity result.

## Sharp two-edit contrasts remain tractable on a forest

Let F=min_i f_i and G=min_i g_i on the same compatible source. Then

    max(F-G) = max_i max_source(F-g_i).

For each prospective negative anchor i, root its incidence component at i
and compute the forest upper messages for the f-readouts. Other incidence
components contribute their maximum F values as a common cap. At the root
use local variables (x_i,z), with z<=f_i(x_i), z<=the child/component cap,
and the child threshold disjunctions z<=m_j OR P_ji(x_i).

Enumerate the intervals between its sorted thresholds. On each interval,
impose the rows required in its interior and maximize z-g_i(x_i) by LP.
Use closed interval endpoints in each adjacent piece: at a threshold, the
piece below omits that threshold's optional rows, so the union remains exact.
The first interval is unbounded below in z, but the objective increases with
z and x_i is bounded, so any nonempty piece has an attained maximum. Empty
pieces are discarded. Repeating for every anchor uses at most
O(n*(n+k)) local LP calls by the simple reroot-per-anchor implementation,
plus sorting, input assembly and rational arithmetic.

The anchor need not be constrained to minimize G in its LP. Taking the
maximum over all anchors supplies that equality. A reconstructed source
has F at least the chosen z, and therefore realizes a contrast at least
the LP value; the global upper-bound argument then forces equality at
the overall optimum. Reverse F and G for the opposite endpoint. Path
connectedness makes the entire contrast image an interval.

This is a derivation only; the executed forest probe checks minimum-value
ranges, not this contrast extension. It provides a path to deterministic
minimax-regret decisions using the existing pairwise-regret identity.
Several-action randomized regret still needs joint-source optimization;
pairwise ranges do not acquire that stronger meaning.

These extensions are optional. They must not inflate the proof obligations
of the bounded whole-range contribution or replace the broader search.
