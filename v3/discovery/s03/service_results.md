# Heterogeneous proof service: developmental outcome

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT, not confirmation.
[Prospective recipes and costs](service_plan.md); [first native failure](hetero01_failure.json).
The alternate-engine [hetero02.json](hetero02.json) completed all three cohorts
and all six arms, with exit code zero. The fixed mathematical cohort hashes
match the available first-run inputs. Native engine changes preclude treating
the two runs as paired solver repetitions.

Reused-service lifecycle milliseconds, including acquisition, checking,
selection, profiling and cleanup:

| Policy | A: true 328, target 282 | B: true 342, target 333 | C: true 284, target 308 |
|---|---:|---:|---:|
| Exact cost-directed | 2,154.8525 warrant | 90,208.8750 deadline abstention | 38,232.6906 abstention |
| Direct uniform | 1,808.2407 warrant | 90,297.2357 deadline abstention | 38,031.8016 abstention |
| Stratum gain heuristic | 5,721.9529 warrant | 90,759.6854 deadline abstention | 38,027.9777 abstention |
| Ordinary Neyman allocation | **976.9474 warrant** | 90,073.7314 deadline abstention | 38,034.7287 abstention |
| Joint cost-directed | 2,923.9609 warrant | 90,436.6411 deadline abstention | 38,719.9705 abstention |
| Joint bounded/resume | 1,283.4752 warrant | **89,710.3442 warrant** | 38,620.0420 abstention |

Shared native dependency import was 29.5622 ms; numerical import another
355.1425 ms. Input-generation/source binding and receipt export are separately
recorded, and must not disappear from a one-shot bill. The diagnostic full
references cost 5,730.9608, 73,358.0927 and 38,368.4130 ms; their negative
answers are trusted native diagnostic outputs, not proof receipts used by the
service. All returned warrants agree with these realized full counts.

The strong ordinary allocation wins A. On B, the bounded policy reaches the
threshold with **333 checked positive receipts**, after 512 sampled identities
and 715 native calls. That final warrant is entirely hard evidence; it does
not show an incremental benefit from joint statistical profiling. An equally
bounded exact/ordinary scheduler is the missing control for any such claim.
All arms correctly abstain on C after exhausting 512 identities. Unsupported
negatives remain unknown; a lower-only service cannot certify the false target.

The 90-second deadline is cooperative between native calls, not a hard time
bound. Do not interpret timing overrun or deadline abstention as statistical
failure. The raw first MiniSat22 access violation and incomplete B arm remain
preserved; the alternate engine's completion does not diagnose the cause.

Disposition: retain the positive-proof/delayed-receipt construction, but
deprioritize further tuning of this exposed joint controller. No clear joint
economic advantage or material-positive readiness is established. Develop
stateful counterfactual/value representations while keeping the ordinary
bounded-control obligation visible if this empirical branch is resumed.
