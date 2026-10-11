# Exact conformance tables

## Structural outputs and declared costs

| Case | Decision / worst loss | Candidate cold | Ordinary cold | Candidate local | Ordinary local |
|---|---|---:|---:|---:|---:|
| counterpossible_tied_minima | fallback / 3 | 833,231 | 403,492 | 747,256 | 356,700 |
| external_sources_not_repairs | fallback / 3 | 1,075,376 | 616,776 | 989,401 | 569,984 |
| fixed_falsity_constant_infeasible | INFEASIBLE | 181,480 | 106,210 | 95,505 | 59,418 |
| conditioning | INFEASIBLE | 114,776 | 72,133 | 28,801 | 25,341 |
| occurrence | fallback / 6 | 123,850 | 80,690 | 37,875 | 33,898 |
| actor_replacement | fallback / 6 | 123,052 | 80,915 | 37,077 | 34,123 |
| shared_replacement | commit / 5 | 123,094 | 80,923 | 37,119 | 34,131 |
| shared_and_copy | commit / 4 | 123,014 | 80,873 | 37,039 | 34,081 |
| shared_copy_and_new_predictor | commit / 2 | 123,240 | 81,078 | 37,265 | 34,286 |

## Information designs across calibration modes

Each cell is full-law recovery / all-target recovery / minimum extra raw queries. Y and N are exact logical verdicts. Modes follow the frozen roster.

| Design | Known | Unknown offset | Unknown scale | Unknown affine |
|---|---|---|---|---|
| one_state_empty | Y / Y / 0 | Y / Y / 0 | Y / Y / 0 | Y / Y / 0 |
| one_state_duplicate | Y / Y / 0 | Y / Y / 0 | Y / Y / 0 | Y / Y / 0 |
| one_state_no_target | Y / Y / 0 | Y / Y / 0 | Y / Y / 0 | Y / Y / 0 |
| rational_signed | Y / Y / 0 | N / N / 1 | N / N / 1 | N / N / 2 |
| brier_anchor | Y / Y / 0 | Y / Y / 0 | Y / Y / 0 | Y / Y / 0 |
| four_state_basis | Y / Y / 0 | N / N / 1 | N / N / 1 | N / N / 2 |
| zero_reference | N / N / 1 | N / N / 1 | N / N / 2 | N / N / 2 |
| partial_target_offset | Y / Y / 0 | N / Y / 0 | Y / Y / 0 | N / Y / 0 |
| larger_exact | N / N / 2 | N / N / 2 | N / N / 3 | N / N / 3 |
