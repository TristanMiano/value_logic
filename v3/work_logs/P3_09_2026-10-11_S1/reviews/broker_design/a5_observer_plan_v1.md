# P3-09 A5 observer amendment plan

Contributor: **ChatGPT (GPT-6 Astra Pro)**. **DEVELOPMENT observer only**,
October 11, 2026. Principal clock credit: **zero**.

The root authorizes one pre-freeze amendment to `p309_broker.py`: compare the
existing paid report's delivered interval with its already computed
deterministic observable envelope. Existing worker and reporter code, report
basis, rate grid, policies, populations and acquisition rules stay unchanged.
The previous adapter and complete development closure remain preserved in
`development_v1/source` at adapter SHA-256
`466546c583880575867dcfb827baede19d4905a9f28681213da27ccc22998ebd`.

## Definitions fixed before checks

For each reported quantity `V`, `F`, `Z`, retain both lower/upper bounds and
their widths. The normalized reduction is the deterministic width minus the
delivered width, divided by the scheduled horizon. Signed lower-bound gain is
delivered lower minus deterministic lower; signed upper-bound gain is
deterministic upper minus delivered upper. Retain both raw and horizon-scaled
gains. A per-quantity normalized width reduction at least `1/100` is the
declared practical indicator; retain same-threshold side indicators as
descriptive details. Never clamp a negative gain to zero.

A conflict is not a usable interval or a positive reporting gain. Keep its
raw bounds and signed span for audit, with usable width/reduction absent and
all practical indicators false. Explicit status distinguishes no report,
failed report, successful report and a reported conflict. Keep the actual
optional source-plus-execution invoice, fixed basis/radius metadata and an
explicit absence of empirical coverage claims. Existing score width fields
remain compatible; new detail goes in `paid_report_comparison`.

## Fixed saved inputs and checks

Use only the already saved 30 public development episode records in
`development_v1/run/results.json`, SHA-256
`7a2d6d7eba3699008f6d31a05eeb07fa0a02518bf11601f0ae630382022585e7`.
Do not call a method, provider, reporter, private truth solver, generator,
random stream or selfcheck. The new observer may import the fixed source
closure, then perform rational arithmetic on those immutable public records.

Independently calculate exact widths and side gains using `Fraction`, compare
every returned value and practical indicator, verify optional fees, and check
explicit no-report/failed-report states. Additional synthetic observer inputs
are: no improvement, improvement exactly at `1/100`, a valid but wider
interval with adverse signed gains, and a conflict with reversed endpoints.
These are arithmetic/status checks, not policy runs or new scientific cases.

Before running the check, freeze a new source closure and the checker itself
under `a5_observer_v1/source`, and bind the old immutable input and plan in a
manifest. Save all outputs and assertions before reporting PASS or failure.
Keep original old-source paid bills unchanged. Recompute the current common
source invoice from new bytes as a separate prospective tariff calculation;
do not attach that newer bill to old paid executions.

Stop after this bounded observer check and hand the amended source/hash to
root. Root's later copied-source preparation gate will execute the current
full closure. No final population, generator, P3-10 action, existing-evidence
rewrite or new agent clock credit is authorized.
