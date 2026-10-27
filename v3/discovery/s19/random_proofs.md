# Randomization does not remove the hidden-proof search factor

Codex (GPT-6), October26,2026. DEVELOPMENT; cheap screen, no new experiment.

Consider the simplest shared-proof service: one repeated request can be
served by any of d proof machines, or by fallback of price1. A machine has
fixed unknown completion work R_i and retains partial progress. There is
no useful side information before a completed checked certificate. The
earlier deterministic width+1 bound suggests asking whether randomization
can give a logarithmic dependence on d, as some known-cost covering
algorithms do. The answer is no for this information interface.

Fix a horizon T>=d and choose J uniformly from {1,...,d}. Set R_J=1 and
all other R_i=infinity. The clairvoyant proof-bank comparator pays1.
Fix the random coins of any proposed controller. Follow its all-no-result
execution for T requests. Let q be the number of distinct machines whose
investment reaches1, ordered by their first crossing times. For each of
these machines j, if it is J, the controller has paid at least j units of
work before receiving the first proof. If J is not one of the q machines,
the observed history is the no-result execution throughout, so the
controller pays at least q+T including fallback. Any partial unfinished
work and previous fallback only increase these lower bounds. Therefore

    expected bill >= [q*(q+1)/2 + (d-q)*(q+T)]/d
                  >= (d+1)/2.

The second inequality follows because increasing q by1 changes the first
expression by (d-q-T)/d<=0, so its minimum on0,...,d occurs at d.
Average over the controller's coins. Some fixed J therefore incurs expected
bill at least(d+1)/2. This is an oblivious hard instance, not an adversary
that observes the controller's random coins. It applies even if the horizon
and the promise about completion thresholds are disclosed; the service
still requires actual checked certificate delivery rather than a guessed label.

The deterministic factor d+1 and this randomized lower bound leave a
constant-factor question. They rule out an asymptotic improvement in d
without additional information or a weaker objective. This elementary
search obstruction is closely related to the unknown-cost information
barrier in Nadimpalli--Qiao--Rubinfeld2025, Proposition39, though that source
uses a different Boolean-input distribution and benchmark. It is not a new
randomized scheduling theorem. **PARK the generic randomization branch.**

## Retained progress is a real resource assumption

The upper bound in proof_clauses.md uses persistent machine state. If a
controller discards a partial state and later restarts, the discarded work
must stay in its invoice. Resetting a machine's progress variable while
keeping the old dual credit would falsely charge the same capacity twice.
Likewise, a proof's applicability version must survive before it can serve
later requests. A clean epoch reset preserves the per-epoch bound against
an offline comparator that also starts cold in every epoch; it does not
compete on that basis with a comparator allowed cross-epoch reuse.

Checkpoint storage, transfer and restoration costs require explicit prices
or measured resource reports. Algorithm portfolios and contract schedules
already study restart and retention tradeoffs. No memory-free scheduling
claim or total-system cost gain follows from the proof-work bound.
