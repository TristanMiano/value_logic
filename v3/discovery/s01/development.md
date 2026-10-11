# C001 developmental observations

Codex (GPT-6), October 11, 2026. All findings DEVELOPMENT; self-review only.

## First prototype

Command: `python v3/discovery/s01/probe.py v3/discovery/s01/run01.json`.
[Raw output](run01.json) binds the source hash, interpreter, scope and runtime.
It completed in 0.194 seconds of measured process runtime; waiting for the
process was excluded from the principal research clock.

- All 6,372 guided-policy cases enumerating n=1..5, every nontrivial threshold,
  truth vector and bit prediction returned the correct threshold value.
  This checks this finite implementation domain, not a general theorem.
- The n=32, k=2 witness has two wrong predicted bits, yet requires all 32 queries
  instead of the false proposed allowance k+2=4. The complete path is saved.
- The conventional SBB rule and its cached-order implementation matched exact
  product-model Bellman costs in nine small cases (n=3,5,7; low, middle and high
  thresholds). Guided point prediction never improved on that expected query
  optimum, as it cannot under the stipulated correct product model.
- In six constructed n=12 inputs and six possible selected policies, alternate
  replay completed 125 of 216 paths. All 216 intervals contained the privately
  evaluated actual query cost. Replays used only the selected policy's receipts.
- Those replays consumed 25,834 counted controller events in aggregate. This
  observation is about synthetic query tariffs and explicitly counted events;
  it is not a measured mathematical solver speedup. Event categories have
  different real machine costs; unit-event repricing is only a diagnostic.

On the six n=12 cases, the guided method also fails to beat the best named
ordinary *whole policy* separately available on that instance after adding one
unit per counted controller event. The per-instance minimum is hindsight,
not a deployable selector. Nonetheless these fixtures offer no material
positive economic evidence. They diagnose a route needing better structure.

The initial SBB implementation spends repeated work scanning remaining indices.
It is a valid comparator for its mathematical query path but not evidence that
SBB inherently has expensive control. Derivation below supplies a cheaper
equal-price implementation before further economic interpretation.

## Equal-price SBB can use constant work per query after sorting

This is a derived implementation specialization of the classical algorithm,
not a new expected-query theorem. Assume all prices are equal and probabilities
are strictly in (0,1). Sort coordinates by descending p, using the *reverse*
tie order for the ascending-p permutation. The first k descending entries and
the first n-k+1 ascending entries meet in precisely the kth descending entry.
Any consistent tie choice with that reverse-order convention is permissible.

Start at index k-1 in the sorted list. After querying it, keep an unevaluated
prefix to its left and unevaluated suffix to its right. If the last result is
one, the new k decreases by one and the next pivot is the last prefix entry.
If zero, k stays the same and the next pivot is the first suffix entry.
Evaluated entries always form one contiguous block, even when the next probe
switches sides. Inductively the unevaluated left prefix has size k (after a
one) or k-1 (after a zero), which proves the indicated pivot choice. Stop at
k=0 or k greater than the remaining count.

Thus there is one initial O(n log n) sort, followed by O(1) pointer and bound
updates per evaluated bit. This removes a potential artificial advantage for
the guided policy. Nonuniform prices need the two distinct orderings; this
specialization does not cover them. For two-level equal-price predictions,
bucket partitioning can replace the sort with O(n) input scanning, and the
same transformation is available to the ordinary comparator.

## Why exact replay needs a resource policy

The current replay recomputes sorting and selector state. A compiled fixed
query order permits replay until the first missing receipt in O(prefix length),
and a trie can share identical policy prefixes. Yet constructing that trie,
computing model predictions and scanning many long prefixes may cost more than
the additional feedback is worth. No speedup is inferred from a replay hit.

Next development: a priced replay budget and a usefulness bound based on the
*decision change* it can cause, rather than always replaying the whole library.
Also develop a branch that chooses a value/counterfactual computation bundle
directly; the program should not spend the full discovery cycle polishing one
threshold example.
