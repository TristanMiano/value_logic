# Two-sided usefulness diagnostic from the sealed public certificates

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC.
R-P3-B-A, prospective post-run D/R extension. Existing centered results and
private summary scores are already exposed; this is additional DEVELOPMENT
analysis, not a new confirmatory experiment. No service/policy/RNG/label run.

Question: an upper bound can certify acceptable performance, but can the
purchased evidence also diagnose a bad forecast? Before computing these
results, fix the following reporting rule for every one of the23 existing arms.

Use the same centered estimates and fixed lambda=8/R. Apply the exponential
argument to both signs, with error1/80 per tail. Since exp5 exceeds its first
five terms, which sum to65.375, and its first six terms, which sum to91.416...,
log80<5. Hence rho_two=Q/R+5R/8 bounds both deviations on a shared event of
probability at least39/40. The SAME deviation serves V and F, so no extra
metric correction is needed. Conditional action randomization similarly has
two tails1/80 using r_a_two=ceil_sqrt(ceil(5(T-m)/2)). Union gives at least95%
joint two-sided V, F, and actual terminal-error intervals at the fixed end.
The sampling part retains its fixed-lambda prefix statement; the action part
does not gain an anytime statement. No simultaneous23-arm guarantee.

Read only the sealed centered public results, their public record-derived
sufficient statistics and the already sealed basic public result if needed.
Do not open private results or evaluator members to form intervals or decide
which rows to retain. Preserve source/result/design hashes and all23rows.
Intersect V and F with their public deterministic lower/upper envelopes;
intersect terminal errors with[0,T-m]. Any empty intersection must remain
explicit (no hidden deletion of an unsuccessful confidence event).

For each row report: whether F lower >T/4 (worse than the immutableq=1/2
Brier null), whether V upper <(T-m)/2 (better than its conditional-action null),
and whether V lower >(T-m)/2 (worse). These are formula-based certificates
under the fair-bit theorem premise. Deterministic development seeds do not
establish confidence coverage, nor does a comparison of23displayed rows make
the statements simultaneously95%. No future predictive guarantee or changed
purchase policy is inferred. Costs of this calculator remain offline analysis.

A source-bound hard-answer override may improve outputs pointwise without
changing the underlying purchase/update path. Base-policy UPPER bounds may
transfer by pointwise dominance if the base statistics are retained; the
shared error identity, direct recomputation from overriddenq, and LOWER bounds
do not automatically transfer when current purchased answers change later
forecasts inside their block. P3-08 must preserve this distinction.
