"""Development probe: seven source states, three actions, 147 ordered pairs.

The initial identical loop was run via stdin; it crashed natively. Retain this
source for the bounded unbuffered retry and subsequent reconstruction.
"""
from fractions import Fraction as Q
from v2.verification.model import Evidence, Query
from v2.verification.producer import produce
from v2.verification.receipts import make_receipt
from v2.verification.reuse import reuse

states = [Evidence(), Evidence(Q(0), Q(0), Q(0), Q(0)), Evidence(beta=Q(0)),
          Evidence(gamma=Q(0)), Evidence(Q(0), Q(0)),
          Evidence(beta=Q(1,64), gamma=Q(1,4)), Evidence(Q(1,4), Q(1,4))]
for action in ('T1', 'T2', 'R'):
    query = Query(action)
    for old in states:
        produced = produce(old, query)
        receipt = make_receipt(old, query, produced)
        for new in states:
            reused = reuse(new, query, receipt)
            fresh = produce(new, query)
            if reused.proof is None or reused.upper_bound != fresh.upper_bound:
                print(action, 'old', old.bounds, 'new', new.bounds,
                      'reused', reused.status, reused.upper_bound,
                      'fresh', fresh.status, fresh.upper_bound, flush=True)
print('Completed 147 ordered reuse comparisons.', flush=True)
