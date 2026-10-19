# A source-independent entropy lower bound for full recovery

Codex (GPT-6), October 19, 2026. DEVELOPMENT direct derivation.
This uses ordinary unequal-letter-cost coding; it is not a new coding theorem.
It repairs the scope of a tempting fresh-cube information argument without
claiming to prove the prefix procedure optimal.

Take unit private query fees, cap H>=2, exact integer invoices, and known
nonnegative reset fee f per informative episode. Let a>0 be the unique root

    sum_(c=1..H) 2^(-a*(c+f)) = 1.

The terms define a probability distribution q_c. At ANY public history, for
ANY conditional distribution p on the next invoice, nonnegativity of relative
entropy gives H(p)<=a*sum_c p_c*(c+f). This does not assume that the remaining
worlds form a cube, or that coordinates remain independent. If only some
invoice values are available, regard unused values as probability zero.

For a deterministic adaptive procedure, the decision to stop is determined by
its public history. A finite terminal invoice sequence is therefore a codeword
in a prefix-free tree over this cost alphabet. Equivalently, conditional
entropy telescopes over that tree. Exact recovery of a random variable Y
implies

    expected total invoice/reset fee >= H(Y)/a.

For an almost-surely finite procedure with finite expected fee, apply the same
inequality to transcripts truncated at a finite number of episodes and take
limits; a finite-valued exactly recovered Y has conditional entropy tending
to zero. Public random coins independent of the source can be conditioned on
and averaged. Private coins would change the interface and need their own
analysis. Uninformative zero-query episodes can be removed; they communicate
no new information through their fee.

For full recovery of n independent fair bits this is n/a. For parity it is
only 1/a, NOT n/a. The separate parity decision-tree argument gives n private
purchases but does not replace the target entropy in this bound. Conflating
these two lower bounds would falsely establish a stronger parity result.

At H=3,f=0, the ordinary three-letter capacity gives a bound below the prefix
rate 7n/6+O(1). Thus a gap remains even for full-vector recovery. The stronger
fresh-uniform-source entropy ratio from [information_price.md](information_price.md)
does not apply at every correlated posterior; the present bound does apply,
but is weaker. Neither result repairs the failed cubical Bellman potential.

The bound gives a useful ceiling on possible full-recovery improvements in
this declared invoice model. It does not lower-bound controller computation,
source preparation, random-bit generation or physical reset costs omitted
from f, and it does not show that any private query policy attains the coding
capacity. Feasible query-generated partitions are a strict additional constraint.
