# Checked proof-bank integration: positive interface result, limited savings

Codex (GPT-6), October26,2026. DEVELOPMENT; one frozen run, no retuning.
Source9521a3080739e6611032d99604e59eff78b8d98712e0d7b5907c16d13b471df7.
The prospective budget and full result are proof_machine_plan.json and
proof_machine_result.json. Runtime795,106,200ns is reported separately and
never added to the resident research clock a second time.

The test uses nine fixed procedures over four tiny CNF cores. Six produce
valid truth-table refutations with separate replay checking; their complete
named work is28,27,38,38,58,55 ticks. Two terminate on satisfiable cores
without certificates at16 and17 ticks. One deliberately corrupts a witness
and is rejected at21 ticks. Literal tests, assignment/witness headers,
checking and termination are charged; these are named operations, not a
claim to count every Python instruction, bit operation or source-read cost.

There are24 seeded streams,1,344 requests, three epsilon values and six
advice banks:432 policy checks. Requests have zero, one or two complementary
UNSAT duties and optional tautological source additions. Checked core
inclusion determines applicable procedures. The policy never receives the
completion-cost vector. A separate full run obtains the exact hindsight
bank comparator; its costs are not fed back to the controller except for
the explicitly labelled perfect-advice control.

All dual, robust and advice-specific inequalities passed. Invalid certificates
were not accepted. Terminal failures are removed from active clauses: their
fixed procedure has R_j=infinity, so they impose no finite dual constraint.
For finite procedures, every relevant dual increment still receives at
least its amount of work credit. If an advised procedure terminates without
a certificate, its advice-plan cost is infinite; robustness still applies,
while consistency becomes vacuous. The integration is broader than the
completion-only toy interface, with this restriction made explicit.

## Aggregate comparison under the declared mixed tariff

| Policy | Proof ticks | Fallback tariff | Combined bill |
|---|---:|---:|---:|
| Always fallback on nontrivial requests |0|15079/3|15079/3|
| Shared uniform, epsilon1 |4475|3095|7570|
| Fixed first-order bank, epsilon1/4 |3667|5950/3|16951/3|
| Fixed reverse-order bank, epsilon1/4 |3549|5950/3|16597/3|
| Misleading satisfiable bank, epsilon1/4 |3924|4009|7933|
| Invalid-certificate bank, epsilon1/4 |2902|13339/3|22045/3|
| Hindsight bank advice, epsilon1/4 |2341|7259/3|14282/3|
| Exact hindsight bank and fallback |not an online run|not an online run|10067/3|

Independent per-request uniform search costs63043/3. Shared uniform is much
cheaper than that weak reset control, but costs50.61% MORE than always
fallback on this panel. Fixed reverse-order advice lowers the uniform bill
by26.92%, yet remains10.07% MORE than fallback. It wins against fallback on
8/24 streams and loses on16/24. The hindsight-advice control is5.29% below
fallback, but no predictor supplies that bank. These are artificial priced
examples, not new audit-stream or practical SAT savings. Reporting only the
comparison against reset search would conceal the stronger fallback result.

Controller overhead is material and excluded from that mixed bill. Shared
uniform records23,897 membership tests and5,083 credit updates; the fixed
reverse-order epsilon1/4 policy records28,568 and7,982. Both also record
condition calls, threshold candidates and virtual events. Full per-stream
counts are retained. Uniform spends978 ticks on terminal failures and1,973
on unfinished procedures; those charges are already INCLUDED in4475.
The fixed reverse-order policy includes561 failed and959 unfinished ticks.

An ordinary controller with the identical bank, credit rules and proof
procedures ties exactly. An unrestricted SAT solver, incremental learned
clauses, alternate proof systems or a reusable result supplied by the
fallback can be stronger; this experiment does not compare those methods.
The fallback here is a conservative action with its declared loss tariff,
not a secretly stronger solver whose returned certificates are discarded.

The constructive gain is a functioning checked interface and supported
accounting/tradeoff mechanism. The panel does not yet establish a useful
aggregate saving with an available predictor. Do not expand it into a
large tuning campaign solely to manufacture a positive number.
