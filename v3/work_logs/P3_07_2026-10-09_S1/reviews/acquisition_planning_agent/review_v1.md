# P3-07 acquisition-planning v1: independent targeted review

## Disposition

**The recurrence, adaptive-observation theorem, all 24 exact saved cases,
and the successful-construction accounts pass. One admission/preflight
failure boundary requires repair.** The two source metadata reads and input
guards precede the first charge, and price-component bounds are not checked
before Fraction membership comparisons. These findings do not change the
saved valid-input calculations or their actual declared construction bills.

The root has acknowledged this boundary and will preserve v1 while making
a separately versioned repair. **This v1 review is complete and its source
freeze may end.** A later source version needs its own identity and revised
accounting evidence; the mathematics does not depend on this repair.

Reviewer: ChatGPT, GPT-6 Astra Pro, same-model internal subagent, with a
same-model auxiliary exact reconstruction. The candidate recurrence and
optional-stopping formula were supplied in the task prompt. The initial
proof reconstruction was saved before inspecting the planning source or
companion. This is nonblind internal review, DEVELOPMENT, unmeasured, with
**zero principal-clock credit**.

## Frozen objects

| Object | SHA-256 |
|---|---|
| Planning source v1 | `94fb8efcbb924470d883733f3c317fc0a79c4047089104ee4ee1c03ca5141f37` |
| Adapter/tariff source | `06324b8b02a8dca3d8fbb423a7adf20708d5cc6cb39c60e60e38e720a7b97615` |
| Planning companion reviewed | `4da2376938da71ac407e3ae8048bdfefc77e90661c66c43afa016dd2da03c87e` |

The live and saved source bytes match the assigned source identity. Reviewer
snapshots preserve the source and companion read for this review. The
prospective plan fixes the two laws, equal prior, profile cost, caps 1 and 12,
horizons 128/512/4096/16384, prices 0, 1/10000 and 1/1000, online charges and
construction allowances. This run uses saved sources and individual frozen
canonical plan cores; it does not have a separate `manifest.json`. Each
core is serialized before its conditional-law forward audit. The source,
table and resource fields in those cores provide the relevant identities.

## 1. Bayesian recurrence and cost placement

Under the supplied persistent law, profile observations and future service
completions are conditionally independent Bernoulli trials with parameter
9/20 or 11/20. At count state `(n,s)`, the equal-prior posterior and predictive
success probability are exactly

```math
\pi_{n,s}=\frac{11^s9^{n-s}}{11^s9^{n-s}+9^s11^{n-s}},\qquad
q_{n,s}=\frac9{20}+\frac{\pi_{n,s}}{10}.
```

The declared future terminal choices are fallback on all H requests or the
stipulated service on all H requests. A service attempt's gain relative to
fallback is theta minus one-half, so terminal gross gain is

```math
D(\pi)=\frac H{20}(2\pi-1),\qquad M(\pi)=\max\{0,D(\pi)\}.
```

The current state's eight-unit lookup is already sunk in W. An acquired
observation requires its one-half service bill, eight control units and the
next state's eight-unit lookup. Thus its full incremental cost is
`c'=1/2+16u`. The implemented recurrence

```math
W_{N,s}=M(\pi_{N,s}),\qquad
W_{n,s}=\max\{M(\pi_{n,s}),
 -c'+q_{n,s}W_{n+1,s+1}+(1-q_{n,s})W_{n+1,s}\}
```

has the correct indexing, predictive weights, child values and cost placement.
It stops on continuation ties and selects fallback when terminal gain is zero.

Backward induction establishes optimality within this fixed bounded
profile-then-commit class. Observation order carries no information beyond
the count state under the stated law, remaining budget depends on n, and
randomizing current actions cannot exceed their maximum. These arguments
cover history-dependent bounded policies with the same observations, terminal
choices and cost interface. They do not optimize over acquiring the law model,
constructing a different planner, or enlarging the terminal deployment class.

The value of executing the table from its initial lookup is `W(0,0)-8u`.
Its construction charge h gives the reported value `W(0,0)-8u-h`. The first
lookup is part of this table-execution interface; choosing whether to consult
the table or construct it in the first place is a separate action. Once h is
sunk, a negative all-in value is consistent with a positive continuation value
and an `acquire` root action. Changing continuation choices cannot recover h.

## 2. Arbitrary-prior adaptive profiling obstruction

The companion's stronger analytic result is valid within its explicit model.
For any prior/posterior pi, multiply a child terminal positive part by its
predictive branch probability. Success produces
`(H/20)(pi-9/20)_+`; failure produces `(H/20)(pi-11/20)_+`. Hence

```math
\mathbb E[M(\pi')\mid\pi]-M(\pi)
=\frac H{20}\big[(\pi-9/20)_++(\pi-11/20)_+-(2\pi-1)_+\big].
```

This equals zero outside `[9/20,11/20]`, rises as `H(pi-9/20)/20` up to
one-half, and falls as `H(11/20-pi)/20` afterwards. Its exact supremum is
H/400 at one-half. The proof uses the same Bayesian model at every step; it
does not assume observed empirical completion rates equal either parameter.

If `c'>=H/400`, then `M(pi_n)-c'n` is a supermartingale. For every bounded
stopping count N, optional sampling gives expected terminal gain minus profile
cost no greater than immediate optimal stopping. If `E[N]<infinity`, apply
the bounded conclusion to `min(N,k)`: M is bounded by H/20, and the expected
truncation error in the cost tends to zero. If `E[N]=infinity`, the positive
cost lower bound `c'>=1/2` and bounded terminal reward give extended expected
net value minus infinity. Nontermination creates no extra terminal reward.

Indeed, when the gap is strict and the expectation is finite, the proof gives

```math
\mathbb E[M(\pi_N)-c'N]
\le M(\pi_0)-(c'-H/400)\mathbb E[N].
```

For H128, H/400 is 8/25 and c' is at least one-half. Thus each expected pure
information probe loses at least 9/50 relative to immediate optimal stopping,
before any other setup or initial lookup bill. This holds for every supplied
initial prior and includes arbitrary adaptive profile counts with finite
expectation, beyond the implemented cap 12.

The companion correctly restricts this conclusion to the persistent two-law
model, fixed H, pure information probes, cost lower bound and two terminal
choices. It says nothing analogous about observations with their own task
payoff, another service law, changing future opportunities, or unrestricted
computation/deployment programs. The theorem is about prior expected value;
it does not promise nonnegative conditional gain separately under each law.

## 3. Independent exact numerical verification

The auxiliary reconstruction was saved before candidate-source inspection.
Its implementation uses unnormalized likelihood-weighted Bellman values and
enumerates reached ordered histories under each law. It does not import or
execute the candidate planner and does not use saved Bellman values to produce
the conditional-law gains.

**All 24 cases, all 1,128 saved states and 10,608 exact field comparisons pass,
with zero mismatches.** Checked quantities include posterior/predictive values,
terminal and continuation values, actions, root values, buy probabilities,
expected profile lengths, online charges, conditional gains and their prior
averages. The average conditional gain equals `W(0,0)-8u` in every case.
The independent script's construction multiplication used the saved counts;
Section 4 independently derives those counts and verifies their cores.

At u=1/1000, the companion's eight-row summary agrees with the exact results,
including the negative all-in values at H512/H4096 and positive values at
H16384. In the cap-12/H16384 case, the low-law operating gain is approximately
-305.313633 and the high-law operating gain approximately 513.886367. Their
average is approximately 104.286367 before construction and 58.212367 after
the v1 table bill. The expected profile length is approximately 9.224131 under
either law. Low-law deployment probability is approximately 0.366877; high-law
deployment probability is approximately 0.633123. These figures support the
companion's explicit distinction from per-law safety or three-quarter symmetric
sign identification.

No profile observations or future deployments were physically executed by
these calculations. They are exact evaluations of the supplied probability
model. The online lookup/control charges are the declared execution tariff,
not an empirical measurement from a deployed acquisition loop.

## 4. Core integrity and construction bill

The two frozen source files contain 22,795 and 9,047 bytes. The declared
read/hash charge is therefore

```math
2\big(\lceil22795/8\rceil+\lceil9047/8\rceil\big)=7962.
```

Let `m=(N+1)(N+2)/2` be the table state count and `w=1024+64m` its fixed
core-word envelope. Total construction units are

```math
96+7962+128m+64m+2w+w=11130+384m.
```

| Cap | States m | Envelope w | Construction units | Cost at u=1/1000 |
|---:|---:|---:|---:|---:|
| 1 | 3 | 1216 | 12282 | 12.282 |
| 12 | 91 | 6848 | 46074 | 46.074 |

All 24 operation maps, category totals, saved construction-resource vectors,
meter totals/remaining amounts, construction prices and all-in subtractions
match this formula. Their aggregate is 700272 units. One unit price of zero
sets the converted monetary charge to zero; it does not remove the recorded
resource use or meter constraint.

All 24 canonical core SHA-256 identities recompute exactly. The cores bind
the source hashes, laws/prior, horizon, cap, unit price, lookup/control charges,
policy rows, numeric cap and construction-resource vector. Their encoded byte
counts match the result fields and fit `8w`; all saved numeric row components
fit the stated 256-bit cap. The identity is outside the hashed core, avoiding
a self-referential digest. Human model construction, standard-library/runtime
provenance and a general deployed environment are not fully captured by this
two-source numerical identity; the companion does not claim such a closure.

The state, freeze and source-word tariffs are stipulated bounded allowances.
This audit verifies exact successful-run accounting under those allowances;
it does not prove a hardware or machine-instruction cost model. External
forward enumeration and reviewer checks are explicitly audit instrumentation.

## 5. Confirmed preflight issue and narrow budget probes

In frozen v1, `build()` first checks cap, horizon and price membership, then
performs two source `.stat()` calls and checks the size envelope. Only then
does it pay the combined 96-unit admission and 7962-unit source-byte bundle.
In particular, a Fraction price is compared against the allowed prices before
its numerator and denominator have been checked against the 256-bit contract.
The source's `bounded()` helper is used for later calculated values, not this
pre-membership input boundary.

Four focused cap-one/H128/price1/1000 probes confirmed the actual order:

| Work limit | Retained paid units | Source-byte reads | Numeric state checks | Core encodings | Returned plan |
|---:|---:|---:|---:|---:|---|
| 0 | 0 | 0 | 0 | 0 | No |
| 8058 | 8058 | 2 | 0 | 0 | No |
| 8634 | 8634 | 2 | 13 | 0 | No |
| 12282 | 12282 | 2 | 13 | 1 | Yes, original exact core ID |

Both metadata-stat calls precede any charge in every row of this probe table.
By contrast, source-byte reads, new Bellman-state arithmetic and final core
encoding do occur after their relevant charge succeeds. Failed later bundles
retain previous paid work and return no partially built Plan. These probes
generated no observations or future query deployments.

The companion sentence saying admission is charged before its corresponding
work is therefore too broad for v1. The root's proposed narrow v1.1 repair is
appropriate: prepay admission before those guards, bound price components
before Fraction membership, and fund the two metadata reads before calling
`.stat()`. Its added source bytes and explicit metadata units must flow into
new construction bills and core identities. Preserve the valid v1 evidence
under its original identity rather than rewriting it.

## Evidence and scope

- [Initial independent reconstruction](independent_reconstruction.md)
- [Prospective review plan](review_plan.json)
- [Frozen source/companion identities](source_snapshot_manifest.json)
- [Core/accounting checker](core_accounting_check.py)
- [Core/accounting attempt](core_accounting_attempt.json)
- [Core/accounting result](core_accounting_result.json)
- [Auxiliary independent review](auxiliary/review.md)
- [Auxiliary exact implementation](auxiliary/independent_planning_check.py)
- [Auxiliary exact result](auxiliary/independent_results.json)

The companion's recurrence, arbitrary-prior adaptive obstruction, distinction
between expected value and per-law safety, and explicit unquantified model
acquisition boundary pass. Its prepaid-admission wording requires the repair
above. Source/protocol fixes and new-version accounting remain separate from
this completed v1 review. No root source, companion, saved evidence, clock,
ledger, gate or publication file was edited by the reviewers.
