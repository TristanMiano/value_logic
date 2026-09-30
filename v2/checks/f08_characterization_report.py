"""Reproduce checked F08 supplied certificates, without general proof search.

Research contributor: Codex (GPT-6), 2026-09-30.
Run with --json PATH to save the report; this command does not run the test suite.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

from v2.checks import f06_inference_rules as K
from v2.checks import f06_source_transport as T
from v2.checks import f06_derived_cases as D
from v2.checks import f07_soundness as H
from v2.checks import f08_unit_characterization as U
from v2.checks import f08_revision_portfolio as P
from v2.checks import f08_warranted_report as W
from v2.checks import f08_transfer_audit as A


def entry(ctx, proof, expected, *, attaining_point=None):
    root = H.receive(ctx, proof, expected)
    packed = D.pack_proof(proof)
    restored = D.unpack_proof(ctx, json.loads(json.dumps(packed)))
    H.receive(ctx, restored, expected)
    if restored != proof:
        raise H.AuditError('Proof changed in the storage round trip.')
    out = {'context': K.serial(ctx), 'request': K.serial(expected),
           'root_budget': str(root.budget), 'proof': packed,
           'used_rows': [list(row) for row in sorted(T.used_rows(ctx, proof))],
           'native_rules': sorted({s.rule for s in proof.steps}),
           'round_trip_checked': True}
    if attaining_point is not None:
        cases = [root.case] if root.case is not None else [h.name for h in ctx.cases]
        if not any(H.case_feasible(ctx, case, attaining_point) for case in cases):
            raise H.AuditError('Attaining point is outside the requested domain.')
        value = H.value(root.new, ctx.signature, attaining_point)-H.value(root.old, ctx.signature, attaining_point)
        if value != root.budget:
            raise H.AuditError('Supplied point does not attain the claimed bound.')
        out['attaining_point'] = H.jsonable(attaining_point)
        out['attained_difference'] = str(value)
    return out


def report():
    records = {}
    ctx, proof, methods = U.three_region_example()
    new = K.add(K.src('z'), K.add(K.maximum(K.src('x'), K.num(0)),
                                K.maximum(K.sub(K.num(1), K.src('x')), K.num(0))))
    # Preserve the exact fixture's independently declared comparison syntax.
    expected = H.request(ctx, 'h', new, K.src('z'), 2)
    records['three_regions'] = entry(ctx, proof, expected,
                                     attaining_point={'x': F(-1), 'z': F(7)})
    records['three_regions']['methods'] = list(methods)
    ctx = P.family_context((0, 10, 20)); proof = P.family_proof(ctx)
    _, _, new, old = P.family_data(ctx)
    records['uniform_portfolio'] = entry(ctx, proof, H.request(ctx, None, new, old, 0),
                                        attaining_point={'x': F(0), 'y': F(0), 'z': F(17)})
    changed = P.family_context((10, 0, 20), revision='replayed')
    replayed = K.replay(ctx, changed, proof)
    records['replayed_portfolio'] = entry(changed, replayed, H.request(changed, None, new, old, 0),
                                          attaining_point={'x': F(0), 'y': F(0), 'z': F(-19)})
    ctx = P.gap_context(); term, proof = P.union_separator(ctx, 'U')
    records['characteristic_probe'] = entry(ctx, proof, H.request(ctx, None, term, K.num(0), 0),
                                            attaining_point={'x': F(-1)})
    ctx = W.rectangle_context(); r = F(4, 7)
    proof = U.affine_certificate(ctx, 'h', W.risk(r), K.num(r, 'P'), F(0), (1-r, r, F(0), F(0)))
    records['least_report'] = entry(ctx, proof, H.request(ctx, 'h', W.risk(r), K.num(r, 'P'), 0, 'P'),
                                     attaining_point={'p': F(1), 's': F(1, 4)})
    ctx = A.cap_context(); proof = A.hinge_deduction(ctx)
    new, old = K.maximum(K.sub(K.src('x'), K.num(1)), K.num(0)), K.maximum(K.src('x'), K.num(0))
    records['row_free_deduction'] = entry(ctx, proof, H.request(ctx, 'h', new, old, 0),
                                          attaining_point={'x': F(0)})
    ctx, proof, gain, point = A.geometry_fixture(F(1, 100), F(1, 100))
    records['geometry_sharpness'] = entry(ctx, proof,
        H.request(ctx, 'h', K.add(K.src('x'), K.src('y')), K.num(0), F(201, 100)), attaining_point=point)
    records['geometry_sharpness']['matrix_gain'] = str(gain)
    obstruction = U.one_way_fixture(); reduct = U.unit_reduct(obstruction, 'P')
    point = {'x': F(0)}
    if not H.case_feasible(reduct, 'h', point) or H.case_feasible(obstruction, 'h', point):
        raise H.AuditError('One-way obstruction fixture lost its domain distinction.')
    kernel = Path(K.__file__)
    return {'author': 'Codex (GPT-6)', 'format': 'F08-supplied-certificates-v1',
            'kernel_sha256': hashlib.sha256(kernel.read_bytes()).hexdigest(),
            'scope': 'Finite supplied witnesses for separately written characterizations U1-U18.',
            'certificates': records,
            'one_way_obstruction': {'context': K.serial(obstruction),
                'target_unit': 'P', 'requested_upper_bound': '-1',
                'reduct_countermodel': H.jsonable(point), 'query_value': '0',
                'is_full_source_countermodel': False,
                'nonderivability_justification': 'U1 necessity, not bounded-search failure'},
            'not_claimed': ['automatic complete proof search', 'formal runtime verification',
                            'empirical source validity', 'independent external review', 'global novelty']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', type=Path, required=True)
    args = parser.parse_args()
    result = report()
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n', encoding='utf-8')
    print(f"Checked and saved {len(result['certificates'])} native certificates.")


if __name__ == '__main__':
    main()
