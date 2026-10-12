# Optional repair mixtures with exact expected-regret certificates

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 12, 2026 UTC.
DEVELOPMENT; same-model auxiliary construction. No helper time is added to
the principal clock. All ordinary controllers may use this same routine.

## Callable result and its changed output duty

`mix_repair.mix_certificate(profile, costs, price)` accepts an already admitted
witness/tree profile and the same joint finite-cohort cost state as
`joint_repair.CostState`. It returns an exact rational probability simplex over
the retained feasible repairs and replacement, its checked bound, the chosen
lower-proof dependency, a fixed-action fallback, and LP/checking records.
The default rounding denominator is 1,000,000 and each LP has a two-second
limit. These were selected before this run, not tuned to its outcome.

The guarantee is **expected regret over the service's random action**, uniformly
over the common cost source. It does not guarantee the tolerance for every
individual repair drawn. The routine exposes the changed duty explicitly;
it does not replace the fixed-action controller's gate. The returned simplex
is an actionable distribution, not a fractional assignment asserted feasible.
Every repair in its support has an admitted full feasible witness.

### Derivation and numerical trust boundary

Let `pi_a` be rational probabilities on admitted witnesses `u_a` and let
`pi_R` denote replacement. Set `d=sum_a pi_a*u_a` and `k=p*pi_R`. Its expected
cost at w is `k+d dot w`. For one admitted tree with supports v_l, the exact
checked expression is

```text
max(0, k+h_W(d)-p, max_l [k+h_W(d-v_l)]).
```

The tree proves `min_l v_l dot w <= C*(w)`. Comparison against each support
and replacement therefore upper-bounds expected regret against the true best
repair-or-replacement action. For the retained finite cohort,
`h_W(c)=sum_i max_(mode in possible_i) c dot mode`; costs here are **cohort
sums**, so divide costs and bounds by eight for the intended cohort mean.
The rowwise maximization covers every compatible cohort, with no probabilities
on unknown cost modes and no enumeration of hidden realized means.

A sparse LP introduces one epigraph variable for each proof-comparison/row
pair and constraints for each possible mode. It proposes probabilities.
The implementation clips negative numerical proposals to zero, normalizes
their exact binary floating-point values, and rounds by largest remainders
onto the declared rational simplex. It then recomputes every signed support
in rational arithmetic. Fixed pure actions are independently checked and
retained as fallbacks. A failed LP, poor numerical proposal, or nonoptimal
proposal cannot invalidate the accepted upper bound. No dual certificate or
global mixture optimality is claimed from a native solver status.

The [SciPy 1.17.0 `linprog` primary documentation](https://docs.scipy.org/doc/scipy-1.17.0/reference/generated/scipy.optimize.linprog.html)
was read for inequality/equality conventions, unrestricted-variable bounds,
the HiGHS method and result status interface. The runtime used SciPy 1.17.0.
The robust epigraph and independent rational admission above are derived here;
the solver's numerical output is only a proposal.

## Executed developmental scope

Command from the repository root:

```text
python v3/discovery/s06/mix_repair.py v3/discovery/s06/joint_source.json v3/discovery/s06/joint_results.json v3/discovery/s06/mix_results.json
```

The source, implementation, underlying checker and original raw archive hashes
are in [the full result](mix_results.json). The raw archive was actually
rechecked before its witness/tree bank was admitted. No compact-cache checksum
was treated as validation of unseen proof bytes.

The scope was selected before inspecting mixture outcomes: all 16 original
admitted repair profiles at audit prefixes 0, 4, 8 and the final 16 of the
existing certificate-directed joint trace. Every prefix retains all unresolved
row modes. The original logical bank is held fixed throughout; newly acquired
logical results from the joint trace are not used. Historical cost observations
are replayed; no new audit or logical provider call occurs.

At the requested mean regret tolerance 0.5 (sum tolerance 4):

| Historical audit prefix | Fixed-action closures | Expected-action closures | Rows with a strictly smaller bound | Sum of fixed bounds | Sum of mixture bounds |
|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 1 | 336 | 324 |
| 4 | 0 | 0 | 1 | 268 | 263.2381 |
| 8 | 0 | 0 | 0 | 209 | 209 |
| 16 | 5 | 5 | 0 | 124 | 124 |

Bounds in the last two columns use the cohort-sum scale. They are certificate
width/duty measures, not action bills or observed regrets, and summing them
does not define a new performance endpoint. Only row 15 improves: its bound
falls from 32 to 20 initially, with half repair/half replacement; after four
audits it falls from 20 to the exactly checked `152381/10000`. The latter
probabilities are `47619/100000` for its sole retained repair and
`52381/100000` for replacement. Both remain above the requested sum tolerance 4.

Thus mixtures are a working additional output option, but **they close no
additional requests at the present duty using this original bank**. No
controller win or reason to tune this exposed fixture follows. A useful next
question is whether a richer legitimately acquired witness/proof bank gives
mixtures more opportunity before another cost audit is needed.

## Costs and limitations

The measured run made 80 floating LP proposals across 64 profile/source-state
queries. All native LP statuses were zero, but only rationally checked upper
bounds entered the answers. The full measured run took about **1.366 seconds
wall / 1.399 seconds process time**. Summed native LP calls took **0.242 seconds
wall / 0.250 seconds process time**; exact checking of their rounded proposals
took **0.273 / 0.299 seconds**. The latter excludes separately checked pure
fallbacks, which remain included in the total query timing. These small
measurements include warm process effects and are not a deployment forecast.

Actual raw witness/source admission used 4,374 declared operation units;
raw lower-proof checking/compilation used 3,601. Reading/hashing the 544,143-byte
raw archive is separately quoted at 76,521 units under the inherited word/block
tariff. The four prefix query runs report respectively 1,054,351; 723,923;
414,122; and 228,310 software units, including rational support arithmetic,
LP matrix construction and rounding. Native LP internal operation counts are
unknown and are not converted to these tariffs. Input/output serialization
and hashes beyond the named raw-archive tariff are represented in measured
run time, not fully priced as operation counts. The saved result occupies
969,841 bytes in this run.

The original logical acquisition bill is 77,646 historical units. The 16
existing audits and their originating controller's complete historical invoice
are retained separately. Their choice may have depended on that controller's
other paid work; replay does not make historical acquisition free. Prefixes
are alternative evidence states, not a newly executed competing acquisition
policy. One preliminary raw-profile inspection printed bank sizes before the
measured run; its operation totals and timing were not saved and are explicitly
unknown. Therefore these are scoped measured invoices, not a claim of a fully
priced end-to-end economic advantage.

No exact diagnostic repair optimum was calculated or used in this mixture
experiment. No fresh validation population was exposed. This construction
extends the usable certificate interface, leaving S26-S28 in DEVELOPMENT,
readiness unassessed, and P3-POS01 outstanding.
