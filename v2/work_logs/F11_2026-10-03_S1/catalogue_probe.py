"""One explicitly charged catalogue build plus three changed-budget selections."""
from dataclasses import asdict
from fractions import Fraction as Q
import json

from v2.verification import catalogue
from v2.verification.cost_probe import timed
from v2.verification.model import Evidence, Query
from v2.verification.producer import produce
from v2.verification.reference import reference

observations = []
source = Evidence(beta=Q(0), gamma=Q(0), revision='catalogue-build')
for action in ('T1', 'T2', 'R'):
    query = Query(action)
    stored, build_ns = timed(catalogue.build, source, query)
    encoded = json.dumps(asdict(stored), default=str, sort_keys=True, separators=(',', ':')).encode('utf-8')
    records = []
    for i, (beta, gamma) in enumerate(((Q(0), Q(8, 85)), (Q(1, 64), Q(1, 4)), (Q(1), Q(1)))):
        current = Evidence(beta=beta, gamma=gamma, revision=f'catalogue-use-{i}')
        selected, select_ns = timed(catalogue.select, current, query, stored)
        fresh, fresh_ns = timed(produce, current, query)
        expected = reference(current, query).maximum
        assert selected.outcome.upper_bound == fresh.upper_bound == expected
        records.append({'revision': current.revision, 'bound': str(expected),
                        'selection_and_checked_emission_ns': select_ns,
                        'fresh_search_and_checked_emission_ns': fresh_ns,
                        'selection_evaluations': selected.template_evaluations,
                        'fresh_basis_checks': fresh.basis_checks})
    observations.append({'action': action, 'build_ns': build_ns,
                         'build_basis_checks': stored.build_basis_checks,
                         'template_count': stored.template_count,
                         'serialized_catalogue_bytes': len(encoded), 'uses': records})
print(json.dumps({'status': 'PASS', 'observations': observations,
                  'scope': 'three builds and nine fixed-schema changes; ordinary preprocessing, not novelty',
                  'limits': 'Single-host, shared-process observations; caches are not reset. Fresh means re-enumerated templates, not a cold process. Include build and storage before amortization claims.'},
                 indent=2, sort_keys=True))
