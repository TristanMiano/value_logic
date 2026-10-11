# SAT-family value service: developmental observations

Codex (GPT-6), October 11, 2026. DEVELOPMENT; no material claim promoted.

[First source-bound run](sat_values01.json): six fixed seeded populations of
256 random 3-CNFs, n=40 or 60, clause/variable ratios 3.8,4.15,4.4. Each
population receives the explicit independent unit additions 1,-2,3. Five
methods start from separately paid identical base histories, retain ordinary
incremental MiniSat22 state and checked base SAT models, and can transport
base UNSAT. New SAT models are clause-checked; native UNSAT remains trusted.
All 90 returned decisions agree with the exact cohort values. The statistical
contract spends total alpha=.05 across the three requests per lifecycle;
actual seeded paths are development fixtures, not a reliability estimate.

| Method | Aggregate marginal ms | Including base history, ms | Edited native calls |
|---|---:|---:|---:|
| Exact, scan cheap proofs first | 31.812 | 257.877 | 413 |
| Uniform direct statistical test | 46.030 | 272.473 | 750 |
| Remove old UNSAT, direct test | 35.642 | 261.589 | 512 |
| Scan proofs, direct test | 36.168 | 267.211 | 502 |
| Remove old UNSAT, mixture confidence interval | 36.792 | 266.033 | 512 |

These are one warm installed-runtime pass, not stable timing estimates.
Marginal cost includes native cleanup at lifecycle end. Common formula
generation and imports are excluded. Initial history dominates the total.
Cheap proof scanning often settles easy positive cohorts; monotone UNSAT
transport settles the negative ones. Near the decision boundary, small
populations and conservative dyadic sample stages often reach a census.
There is **no positive aggregate resource result** here.

The partial-label decision state separately passed 4,911 finite ternary
prefix states (N<=7), checking that a warrant with missing labels is also
warranted for every compatible complete prefix. The explicit timeout-dropping
counterexample is reproduced. The SAT run itself used completed native calls;
it did not yet exercise actual censored solving.

## Constructive next revision, specified before its run

Two mechanisms justify a new developmental scale probe, rather than selecting
a favorable subcell from this run:

1. A fixed .8 alternative may be badly mismatched to a true rate just beyond
   the decision boundary. Replace it with an equal-weight mixture of fixed
   count alternatives at fractions 1/64,1/16,1/4,1/2,1 of the distance from
   the null boundary to the upper endpoint. The mixture of nonnegative
   supermartingales retains the same test level. Repeated alternatives are
   deduplicated before assigning equal weights. This is an ordinary sequential
   test, available to all controllers, not a learned truth model.
2. An exact early decision can require a number of new labels proportional to
   the unresolved population. For a uniform order of R remaining bits with M
   ones, the expected position of the a-th one is a*(R+1)/(M+1). With a a
   fixed fraction of R, this is linear. Statistical sample requirements can
   instead depend on the gap from the decision threshold. This query-interface
   comparison does not lower-bound every solver that sees formula structure.

Use two populations, N=1024, n=60/100, ratio 4.15, and eight predeclared
signed unit edits +1,-1,+2,-2,+3,-3,+4,-4. Retain the same formula generator
and seed rule. Charge all preparation and compare exact proof-first, the old
fixed-alternative proof-first rule, and mixture tests with/without the proof
scan and monotone partition. Use approximately sqrt(2) sample growth after
small stages to reduce paid overshoot; this costs more test evaluations.
Keep total alpha=.05 per eight-request stream, every result and timing,
including adverse cases. This is DEVELOPMENT after the first exposed cohort,
not independent confirmation or a claim that increasing scale must help.

## Larger run: failure preserved, diagnostic continuation completed

The first v2 invocation terminated without a result file or traceback. Its
exit code and completed exposure units were not captured; see
[the failure record](sat_values02_failure.json). This remains an unexplained
failed attempt. Separately versioned v3 added durable boundary writes and
native fault reporting. It completed with exit code zero and no reported
native fault; that does not explain the original termination. Its lifecycle
timings include diagnostic writes and must not be presented as clean timing
replications. [Diagnostic results](sat_values03.json), [exit](sat_values03_exit.json).

All 80 actions in the completed run agree with the exact cohort values. The
alternative-mixture screen checked 238 composite count/level cases at N<=8,
and verified that rejection is monotone in the observed number of ones.

| n | Method | Edited native calls | Sum of request ms | Base history ms |
|---|---|---:|---:|---:|
| 60 | Exact proof-first | 2051 | 116.056 | 207.672 |
| 60 | Fixed alternative, proof-first | 2557 | 140.846 | 211.340 |
| 60 | Mixture, uniform | 1971 | 119.340 | 209.577 |
| 60 | Mixture, old-UNSAT partition | 1391 | 89.149 | 211.389 |
| 60 | Mixture, proof-first | 801 | 52.215 | 213.651 |
| 100 | Exact proof-first | 1773 | 593.340 | 1157.714 |
| 100 | Fixed alternative, proof-first | 1312 | 458.857 | 1179.980 |
| 100 | Mixture, uniform | 1033 | 382.101 | 1166.435 |
| 100 | Mixture, old-UNSAT partition | 879 | 313.261 | 1160.879 |
| 100 | Mixture, proof-first | 664 | 254.863 | 1167.328 |

The proof-first mixture cuts native calls and request time substantially at
this scale in the observed run. Those request timers exclude the subsequent
diagnostic write; full instrumented lifecycle bills remain in the raw record.
Initial-history costs limit the end-to-end ratio. This is promising scoped
development, with only two correlated seeded populations, fixed arm order and
an unexplained prior failure. No transfer or stable speedup claim is confirmed.
The conventional method can use the identical mixture and receipt rules.

Next develop the censored-computation mechanism, rather than rerunning timing
until a favorable number is obtained. In particular, a positive value warrant
may need only checked SAT witnesses: unresolved or untrusted negative answers
can remain unknown. This could connect sampling to the earlier provider-
independent evidence duty while avoiding expensive UNSAT proof production for
requests that only need a lower value bound.
