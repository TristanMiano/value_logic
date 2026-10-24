# Proof completion order is an observation, not a random audit order

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass52.

Consider a fixed catalogue with exactly half its claims false. Draw20
independent uniformly random claims and start their checking computations
in parallel. Correct claims finish in one unit of time; incorrect claims
finish in100. At time1 every completed result is correct. Treating these
completed results as an ordinary iid uniform audit sample is invalid: the
completion rule selected them by their truth-correlated computation time.

For a null failure fraction at least1/2, the one-sided all-zero test would
multiply wealth by2 for each observed success. It crosses20 after five
successes. The invalid completion-order procedure crosses at time1 with
probability

    1-sum_(j=0)^4 binom(20,j)/2^20 =1042380/1048576 >.994.

Thus an apparently cheap high-throughput proof scheduler can destroy the
nominal5% guarantee. This is a selection counterexample, not an empirical
claim about proof engines.

## Retain the sampled slots and bound unfinished truth

Use the original sampled sequence. Before drawing slot i, choose a
nonnegative factor K_i-b_i*Y_i whose null conditional expectation is at
most1. Retain that factor's parameters and its slot even while the
computation is unfinished. At physical time t, let C_t be any sound
constraint set on those fixed sampled truths, including joint proofs.
For a fixed sampled prefix n, report

    L_(n,t) = min_(y in C_t) product_(i<=n)(K_i-b_i*y_i).

Since the actual truth vector lies in C_t, L_(n,t)<=E_n pointwise. Therefore
P(sup_(n,t) L_(n,t)>=1/delta)<=delta whenever E_n is a test supermartingale.
Physical-time selection need not be a stopping time for the latent sequence:
the pathwise domination by sup_n E_n supplies the simultaneous guarantee.
The optimization needs a certified LOWER product bound (equivalently an
UPPER weighted failure bound after logs), not an arbitrary feasible value.

Factors must be chosen before their slot's fresh random draw. Public
progress on earlier slots may guide the next factor or computation schedule.
With a fixed catalogue and independent sampling with replacement, even
truth-correlated progress on those earlier slots does not change the
next draw's population failure rate. Choosing a slot's bet after inspecting
its own progress, or deleting it because it is slow, is a different and
generally invalid operation. A new proposal or edited catalogue also needs
the previously stated scope/transport conditions.

In the counterexample, the all-zero alternative gives wealth0 to any prefix
that might contain a failure. It can certify at time1 only prefixes with
every result completed. It cannot extract an artificial twenty-success
sample by discarding slow slots. More permissive positive-failure alternatives
can use upper bounds on the unfinished failure count, but must pay their
corresponding factor penalty.

This preserves freedom to choose proof-search order using a fallible speed
forecast. It does not establish a scheduling advantage or an optimal policy.
The output is a practical interface rule linking unresolved proofs, paid
computation and honest statistical reuse; conventional censored-observation
and adaptive-testing methods are mandatory comparisons.
