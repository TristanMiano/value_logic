# When observations can precede coordinatewise changes

Codex (GPT-6), DEVELOPMENT. A small boundary result for the permission interface,
not a general theorem about causal experiments or counterpossible mathematics.

Assume a fixed hidden original bit vector x. Actions are known unary maps
applied coordinatewise; observations reveal the current value of one bit
exactly. Action and query prices are fixed and independent of the hidden world.
Only final validity matters, actions have no external side effects, and the
interface allows the same action sequence to be postponed and applied
atomically. These assumptions exclude intermediate-state safety requirements.

An interleaved adaptive policy can be simulated by a policy that makes its
informative original-bit queries first, then executes its selected action
sequence. Maintain the composed unary map f_i for each coordinate while
simulating the original policy's control decisions. When that policy queries
the current i-th bit, either f_i is constant, in which case its result is
already known, or f_i is identity/toggle, in which case query original x_i
and compute f_i(x_i). Previously purchased original values can be reused.
Advance the simulated policy and record its chosen actions. At termination,
apply the recorded sequence in its original within-coordinate order.

The final world and branch decisions are identical. Informative query cost
cannot increase; action cost is unchanged, and the transformed policy can skip
queries of known constants. Query and action count caps are respected. This
does not replace a paid sequence with an unpriced compound action: postponing
is a permission assumption and every recorded operation remains charged.

Thus interleaving these particular changes with observation does not itself
create an extra information resource. Query-first permission analysis is
sufficient for this interface. The conclusion fails if actions couple bits,
change what a sensor measures, have state-dependent prices, or must preserve
constraints at intermediate steps. For example, an allowed paid operation that
stores x_1 XOR x_2 in another register creates a different observation menu.
Its computation and access costs must be included before claiming a gain from
reading that register. Ordinary planning and experiment design receive the same
operation permissions.
