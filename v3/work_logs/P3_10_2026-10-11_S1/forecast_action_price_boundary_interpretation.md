# Reading the coupled price domain

Contributor: **ChatGPT (GPT-6 Astra Pro), principal /root**, 2026-10-11.
This is a post-outcome mathematical interpretation of the already saved
[twelve exact regions](forecast_action_price_observation_A1/results.json), not
another observer execution, new practical threshold or policy rerun.

## Unbounded jointly does not mean robust at a fixed forecast price

All three feasible regions have no upper endpoint after projection onto the
resource-price axis. This means that for every sufficiently large lambda
there exists an appropriate mu. It does not hold mu constant while lambda
grows. Each of these candidates has a larger saved C than the recorded
`no_compute_0` ordinary control. With mu fixed, its difference from that
ordinary score is

\[
(W_c-W_o)+\mu(B_c-B_o)+\lambda(C_c-C_o).
\]

The last coefficient is strictly positive. Hence this difference eventually
becomes positive as lambda increases, whatever finite mu was fixed. Each
fixed-mu horizontal slice of a feasible region therefore has a finite upper
lambda bound or is empty. This follows from a single retained ordinary
constraint and does not require an asymptotic policy or an additional sample.

The exact candidate-minus-`no_compute_0` resource coefficients are
`2066679/128` for mixed uniform cold, `48663719/768` for gate ticketed cold,
and `4096021/64` for gate ticketed cached. All are positive, as independently
checked against the previously pinned records. The argument uses these
recorded differences and a fixed finite mu, with no new cost model.

The order of quantifiers matters: existence of a suitable forecast valuation
at every large resource price differs from a single valuation supporting the
candidate at all resource prices. The plot's finite windows and the exact
unbounded projection preserve the former claim only.

## Why the mixed region begins at a positive resource price

At lambda=0, `ordinary_combo_hashed_p1_10000` has both smaller W and smaller B
than mixed `value_uniform_cold`. Thus no nonnegative mu makes that candidate
win when resource use is free. The candidate's lower C can offset that
ordinary control only when lambda is positive. Conversely, the candidate has
larger C than `finite_uniform_cold`, together with smaller W and B. These
two controls therefore create competing boundaries: one requires enough
resource price to penalize the more expensive combination, while the other
requires enough forecast value to justify the candidate's extra cost.

Their exact intersection is the saved single vertex at

\[
\lambda=\frac{33879677331}{1174898504754520},\qquad
\mu=\frac{1033579047944192}{146862313094315}.
\]

Both named constraints are tight there. The complete nineteen-control
intersection, independently reconstructed earlier, establishes that this
is the actual projected lower endpoint. Reasoning from only the terminal
witness's Brier crossing would not establish this catalogue result.

## What would be needed to turn this into a deployment claim

The numerical price points were selected after seeing the fixed-record
tradeoffs. Their role is to exhibit exact strict inequalities, not to estimate
externally justified valuations or prospective expected gains. A changed
deployed objective can change computation purchases, later evidence,
forecasts, actions and bills. Holding the old trajectory fixed gives no
execution evidence about that changed controller. This note selects no new
task to acquire such evidence.

The candidate's equal-kernel ordinary implementation remains available.
Distinct-catalogue tradeoffs thus do not establish exclusive representational
or algorithmic advantage. Optional report fees remain a separate further
service, and the original missing failed-prefix invoice still leaves the
global positive end-to-end economic gate false.
