# Present value adequacy versus update adequacy

Codex (GPT-6), October26,2026. DEVELOPMENT; cheap screen.

A finite source state w, output map V and allowed transitions T_a induce
an exact reusable summary only if its equivalence respects all future
experiments. Define w~w' iff V(T_s(w))=V(T_s(w')) for every finite allowed
update word s, including the empty word. This is the largest transition
congruence refining current-output equality: appending a suffix proves
closure, and induction shows every output-preserving congruence refines it.
Partition refinement computes it when the state graph is explicitly finite.
These are standard automaton/bisimulation facts, not a new value principle.

The loss can be maximal even when today's decision is constant. Let w be a
hidden d-bit vector. Today the only decision has cost0. Update a_j replaces
that task by reporting w_j. Any summary adequate for every permitted update
must distinguish all2^d sources and needs at least d bits in the worst case;
the present-value summary needs none. Restricting the allowed update family
can restore a useful quotient. This is an information lower bound under a
stated intervention interface, not a computation lower bound or a reason
to demand full-source retention for every application.

Conditioning alone is not a new branch here. The inherited P3-02 derivation
already gives linear threshold certificates, sharp fractional LPs and a
small-denominator instability example. A new conditioning adapter must add
an actual retention or computation consequence beyond those results.

Disposition: retain as a scope diagnostic for source-edit constructions;
park the generic quotient claim as established machinery. No new family,
probe campaign or readiness forecast.
