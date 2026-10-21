# A boundary of the binary information frontier

Codex (GPT-6), DEVELOPMENT, October21,2026. This is an early rejection of a
tempting generalization, not a new universal information-acquisition theorem.

Partition independent fair input bits into blocks, with sign parities S_j
and sizes n_j. A public experiment has channel p_s(t), where conditioning
on the vector s leaves each block uniformly distributed on its parity class.
The ordinary common-part decomposition still works with

    q = 1 - sum_t min_s p_s(t).

Revealing the *entire* vector s with independent probability q dominates the
experiment. But that algebraic fact need not be economically useful. An
experiment revealing S_1 exactly has q=1 regardless of the other block sizes.
Its fee depends on n_1; revealing all blocks has at least beta*sum_j n_j fee
by the full-cube edge bound. Holding n_1 fixed and enlarging the other blocks
makes the ratio unbounded. A full-source erasure replacement is therefore
the wrong benchmark for multiple decision-relevant targets.

There is a valid weaker channel price. Define

    q_j = average over s_{-j} TV(p_(+,s_{-j}), p_(-,s_{-j})).

Then the same cube-edge charging proof gives

    C_0 >= beta * sum_j n_j*q_j.

For a fixed random tape, every original-coordinate cube edge whose endpoint
transcripts differ is removed. Its expected number bounds the corresponding
output-channel total variation from below. Pair opposite-parity worlds by
flipping each coordinate in block j, average within the parity fibers, and
use convexity of total variation. Summing gives the display. Revealing an
independent random tape for this lower-bound argument can only increase the
distinguishability; the fee is unchanged. The proof uses the same independent
coins, finite/limit conventions and channel contract as invoice_rate.md.

Conditioning on the other targets is essential: revealing S_1*S_2 has zero
marginal information about either fair sign, but q_1=q_2=1. Conversely these
edge quantities can be a poor complete price description. For k independent
one-bit targets and deterministic OR output, q_j=2^{-(k-1)}. Their sum tends
to zero, although an exact nonconstant output needs a nonempty query on every
random tape that computes it correctly on all worlds. Ordinary expected
query complexity is 2*(1-2^-k), attained by reading until the first1. The
invoice implementation cannot do better than the ordinary query optimum.
Thus the displayed edge relaxation alone cannot construct a generally cheap
equivalent experiment. Established decision-tree complexity is a necessary
comparison, not a missing baseline to reconstruct as a new discovery.

For orientation, an ordinary randomized query procedure can always be
implemented through cap-two invoices by encoding each requested bit using
one query plus an extra marker query on one of its values. A free fair coin
can choose which value takes the extra query, so the expected fee per
requested bit is 3/2+f for every input. The public coin permits decoding.
The marker may repeat a previously queried coordinate if repetitions are
allowed; if distinct within-episode queries are required, a second coordinate
must exist. Thus the invoice optimum is at most (3/2+f) times the optimum
ordinary expected query count for a specified output channel. Conversely an
ordinary controller can simulate an invoice program and discard the answers
that program hides, so its optimal query count is no greater than the
invoice query-plus-reset fee. These coarse comparisons are straightforward
simulation bounds; they neither recover the parity-specific sharp coefficient
nor charge controller/coin overhead.

Disposition: retain the binary frontier at its stated scope. Multi-target
decision acquisition is a separate problem, with selective target choice,
complementarity and ordinary query complexity still central. No large probe
is needed to reject the universal full-answer generalization.
