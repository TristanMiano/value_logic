# Bounded acquisition of reusable response certificates

Contributor: Codex (GPT-6). DEVELOPMENT, 2026-10-14.

rr01's response intervals reduced recorded computation against ordinary local
search, but spent substantially more than the fixed-action threshold controller.
A small fee reduction is not sufficient reason to buy unlimited planning.

Fix a stream-wide budget B before any stream observation. Charge all optional
pair-table construction, pair-floor construction/update, local action proposals,
and new interval construction to that budget. Common source compilation,
initial action selection, static query order, checking the current action,
lookup of already checked records, and final output checks remain separately
charged. Thus B bounds an incremental component, not the service's total cost.
The initial action and order are shared with the ordinary threshold control.

Execute optional work through a meter that first charges an indivisible chunk,
then throws a distinguished budget exception if cumulative spending exceeds B.
An unfinished proposal does not replace the current feasible action. Discard
partly updated tables and floor banks. Once exhausted, never start another
optional computation. Existing certified cache records remain usable. This is
ordinary bounded metareasoning, not a new optimal policy theorem.

If every charged chunk is at most q units, optional recorded spending is at
most B+q, including failed work. B=0 begins exhausted and spends zero optional
units. A positive B may stop early; negative answers and failed proposals consume
the budget. Retention writes happen only after a full interval is constructed
and checked at the reached answer; their declared charge is included. A final
fresh source-bound check remains mandatory even after a budget abort.

Correctness: after every branch the incumbent consists of three original
source models. The existing-action test and a positive cache hit each establish
the required whole-box upper bound. A negative cache hit only skips immediate
action search; it cannot produce an output. Budget exhaustion similarly skips
optional search. The ordinary threshold order and paid fallback therefore
still terminate with a checked action. The selective-query spending guard
retains the pathwise fee ceiling 2C. Skipping preparatory local improvements can
change later action search, so no fee-dominance claim follows from this argument.

The budget cannot establish economic optimality without prices for named
computation, storage, and unmetered work. Compare both fee and named units with
the same-stream ordinary threshold and uncapped region controller, including
setup. Inspect budget overshoot explicitly instead of treating aborted work as
free. A future price-aware budget must be declared from external prices, not
chosen retrospectively to maximize this test's result.
