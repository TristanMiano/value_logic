"""Retained source of the six-case optional program smoke probe."""
from fractions import Fraction as Q
from v2.verification.program_model import ProgramEvidence, ProgramQuery
from v2.verification.program import produce
from v2.verification.program_reference import reference

queries = [ProgramQuery(), *[ProgramQuery('risk_vs_full', a)
                             for a in (0, Q(1, 6), Q(1, 3), Q(9, 10))]]
for query in queries:
    evidence = ProgramEvidence()
    produced = produce(evidence, query)
    expected = reference(evidence, query)
    print(query.kind, query.alpha, produced.status, produced.upper_bound, expected, flush=True)
    assert produced.upper_bound == expected[0]
evidence = ProgramEvidence(foreign_zero=True)
query = ProgramQuery('risk_vs_full', budget=Q(-1, 20))
produced = produce(evidence, query)
print('Unit gap', produced.status, produced.upper_bound,
      'full', reference(evidence, query), 'reduct', reference(evidence, query, reduct=True), flush=True)
