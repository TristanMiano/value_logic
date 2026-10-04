"""F12 selected fault injections: demonstrate that independent checks detect them.

Patches are confined to this process and restored after each probe. No trusted
source file is edited, and no mutation result is a valid logical certificate.
This is four named controls, not exhaustive mutation coverage.
"""
from dataclasses import replace
from fractions import Fraction as Q
import json
from unittest.mock import patch

from v2.checks import f07_soundness as A
from . import differential as D
from .model import Evidence, Query
from .producer import produce
from .reference import reference


def report():
    evidence = Evidence(0, 0, 0, 0, 'mutation-control')
    original = produce(evidence, Query('T1'))
    semantic = reference(evidence, Query('T1'))
    mutations = (
        ('forged_producer_bound', patch.object(D, 'produce', return_value=replace(original, upper_bound=Q(-100)))),
        ('ordinary_control_discards_evidence', patch.object(D, 'analytic_bound', return_value=Q(471, 256))),
        ('inadmissible_reference_attainer', patch.object(D, 'reference', return_value=replace(semantic, witness=(Q(2), Q(2))))),
        ('receiver_ignores_requested_strength', patch.object(A, 'receive', side_effect=lambda ctx, proof, request: proof.steps[proof.root])),
    )
    rows = []
    for name, mutation in mutations:
        # Freeze this valid producer output for the receiver fault so the probe
        # specifically tests the independent stricter-request check.
        producer = patch.object(D, 'produce', return_value=original) if name == 'receiver_ignores_requested_strength' else patch.object(D, 'produce', D.produce)
        # Apply the identity patch first so a producer mutation still overrides it.
        with producer, mutation:
            try:
                D.check_source(evidence)
            except AssertionError as error:
                rows.append({'mutation': name, 'detected': True, 'reason': str(error)})
            else:
                raise AssertionError(f'Undetected declared mutation: {name}')
    # A real unmodified check must still work after all temporary faults.
    restored = D.check_source(evidence)
    return {'status': 'PASS', 'mutations_detected': len(rows), 'restored_queries': len(restored),
            'rows': rows, 'scope': 'Four named artificial faults; no exhaustive mutation or new soundness claim.'}


if __name__ == '__main__':
    print(json.dumps(report(), sort_keys=True, indent=2))
