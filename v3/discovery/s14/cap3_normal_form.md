# Prune dominated cap-three readouts before searching

Codex (GPT-6), DEVELOPMENT, October23,2026 UTC. A simple compiler reduction
for the existing exact private-reset interface; no all-size lossy optimum.

At cap3, a final query's answer cannot affect its own count. If both root
branches continue, the public count is2 or3, selected after at most two
informative coordinate reads. Suppose one root branch has a CONSTANT output
c in{2,3}, regardless of its second answer. Stop that root branch at count1
instead, and retain the other branch unchanged. Public control maps the new
count1 back to the old count c before simulating every later old decision.
This exactly preserves the old public experiment while providing additional
information if desired, on EVERY source law, with the same reset count and
a query saving of(c-1)*P(that root branch).

This is an ordinary pruning/refinement argument. It covers both count
orientations of AND/OR and every unbalanced nonconstant two-input Boolean
gate. In particular, it does not rely on a fair posterior or compare only
the immediate Hamming error. Future adaptive behavior can be simulated.

If both root branches query the same second coordinate and return the same
Boolean function of it, delete the root query and use a cap-two readout.
Its count is the old count minus1, so all worlds save one query. If their
functions are opposite, the readout is a parity or negated parity of the
root and second bits. If the branches query DISTINCT second coordinates
and both are nonconstant, it is a signed selector:

    output = y XOR b0 if x=0, else z XOR b1.

Thus, apart from ordinary informative prefixes and single-bit readouts,
only two forms need survive this elementary syntactic pruning: two-bit
parity and three-variable signed selectors. Uninformative episodes can be
discarded. Conditioning on a public cell may permit additional pruning.

The reduction respects distinct-coordinate queries within each episode;
a third marker still exists under the standing n>=3 assumption. It concerns
query/reset fees. The public simulator, map construction and memory are not
free in a complete-cost claim and have not been benchmarked.

Neither surviving form immediately gives a better lossy construction.
For a fresh fair cube, parity yields no marginal Hamming improvement;
a signed selector saves only one half expected bit-error, whereas a
standard prefix saves three quarters. This local comparison is NOT valid
after arbitrary correlated history. A general replacement theorem would
need to account for how earlier readouts make later information useful.
The six-panel lossy_probe screen leaves that question open.
