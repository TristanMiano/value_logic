# A decision consequence: finitely many paid ordinal reports

Codex (GPT-6), s18 DEVELOPMENT. This is a separate access contract from
the always-observed, unknown-corruption-budget mistake bound.

There are d fixed named alternatives, arbitrary available subsets, and
fixed unknown utilities with ties. The learner may pay to obtain an asserted
best member of the current subset. A trusted global ceiling C0 bounds the
number of false reports among those acquired. A report supplies all its
winner-versus-context weak comparisons. Decisions made without buying a
report must be guaranteed optimal under that ceiling.

Maintain c_ab, saturated at C0+1. Declare a directed comparison certified
when c_ab>C0; such an assertion is true because at most C0 reports can be
false. Maintain reachability of the certified comparison graph. Its cycles
certify equality, not inconsistency. If some available action reaches all
other available actions, choose it and buy no report. Otherwise choose any
available action, buy the report, and update every winner-versus-context
count once. The proposed action on a query round need not be safe.

Before any purchased report, no available action reaches all other available
actions. In particular its subsequently returned winner i lacked such a
warrant. Some j in the available set was not reachable from i; hence
c_ij<=C0. The update increments that pair. Charge the purchase to one such
pair. A directed pair can be charged at most C0+1 times, proving

    purchased reports <= d*(d-1)*(C0+1),                 (Q1)

independent of horizon, contexts, true ties and the placement of bad reports.
Every non-query round is optimal. With fee f per report, acquisition fees
are at most f times (Q1), versus f*T for always buying feedback. This is a
worst-case bound, not an empirical percentage improvement or a comparison
against a complete competing active-learning method.

Counts require O(d^2 log(C0+2)) bits. Recompute reachability only when a
new edge crosses the threshold; at most d(d-1) such events occur. A simple
implementation uses O(d^3) work per recomputation and O(d^2) work to inspect
one context for a certified best action. These reasoning costs and report
processing must be charged alongside fees. An incremental reachability
implementation is an ordinary improvement, not necessary to (Q1).

Exact shared-report min cuts can certify additional safe choices sooner
than thresholded paths, but require more storage/work. They preserve (Q1):
if no available action has all required cuts>C0, the returned winner has
some cut<=C0, hence its direct count to that item is<=C0. A bounded reasoner
can therefore compare the cheaper sufficient warrant with the stronger
exact warrant on an explicit acquisition-versus-computation tariff.

## Why the trusted ceiling changes what can be promised

No deterministic learner can both acquire only finitely many reports on
every stream and make only finitely many errors for every unknown finite
corruption count. Already use the same two-action menu forever. In a world
where A is strictly better, give truthful replies until the learner's last
query. The finite-error promise makes it eventually always choose A.
Now take the world where B is strictly better and corrupt exactly those
finitely many replies to the same A answers. The learner sees the identical
history, never queries again and eventually always chooses A, causing
infinitely many errors despite finitely many corrupted reports.

This does not prevent sparse, indefinitely continuing queries, probabilistic
guarantees under a specified noise law, or a finite query budget supplied
with C0. It explains why an unknown-C mistake bound alone does not justify
stopping paid feedback. Robust comparison learning, selective sampling and
abstention are required prior comparisons; the counting argument itself
is elementary and no novelty forecast is assigned to it alone.

An ordinary per-menu cache is also a strong paid-query control. With known
C0, buy reports for a menu until one winner has appeared C0+1 times, then
reuse it safely. Among at most d possible winners, d*C0+1 reports suffice
by the pigeonhole principle. Across q recurring menus this costs at most
q*(d*C0+1) reports. The cross-menu pair construction improves the dependence
on q, but need not beat this cache when few menus recur. Genuine report
rounds are counted here; copying one retained receipt does not create a new
fault-independent report. A warranted bound on false rounds, not stochastic
independence, is the premise in either construction.
