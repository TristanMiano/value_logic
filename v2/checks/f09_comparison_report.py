"""Reproduce F09's supplied native certificates and explicit obstruction data.

Research contributor: Codex (GPT-6), 2026-09-30. This is an audit report, not
general proof search. Run with --json PATH; it does not execute the test suite.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

from v2.checks import f06_inference_rules as K
from v2.checks import f06_derived_cases as D
from v2.checks import f06_source_transport as T
from v2.checks import f07_soundness as H
from v2.checks import f08_unit_characterization as U
from v2.checks import f09_fragments as B
from v2.checks import f09_scaling as S
from v2.checks import f09_optional as O


def entry(ctx,proof,request):
    root = H.receive(ctx,proof,request)
    packed = D.pack_proof(proof)
    restored = D.unpack_proof(ctx,json.loads(json.dumps(packed)))
    H.receive(ctx,restored,request)
    if restored != proof: raise H.AuditError('Proof changed in serialization round trip.')
    return {'context':K.serial(ctx),'request':K.serial(request),'root_budget':str(root.budget),
            'proof':packed,'round_trip_checked':True,
            'native_rules':sorted({s.rule for s in proof.steps}),
            'used_rows':[list(r) for r in sorted(T.used_rows(ctx,proof))]}


def report():
    certificates = {name:entry(*fixture) for name,fixture in B.examples().items()}
    certificates['repaired_unit_presentation'] = entry(*S.repaired_unit_certificate())
    certificates['two_ray_boolean_observable'] = entry(*O.two_rays_boolean_certificate())
    certificates['convex_three_requirement_conflict'] = entry(*O.convex_conflict_certificate())
    old,new,proof,request = O.typed_refinement_fixture()
    certificates['refined_context_bound'] = entry(new,proof,request)
    point = {'x':F(1)}
    if not H.case_feasible(U.unit_reduct(old,'U'),'h',point):
        raise H.AuditError('Original reduct countermodel was lost.')
    if H.case_feasible(old,'h',point) or H.case_feasible(U.unit_reduct(new,'U'),'h',point):
        raise H.AuditError('Typed refinement obstruction lost its scope distinction.')
    return {
        'format':'F09-supplied-certificates-v1','contributor':'Codex (GPT-6)',
        'kernel_sha256':hashlib.sha256(Path(K.__file__).read_bytes()).hexdigest(),
        'scope':'Supplied finite native certificates; F09 results have separate written proofs. The general S8 compiler is not implemented.',
        'certificates':certificates,
        'typed_refinement_obstruction':{'original_context':K.serial(old),
            'target_unit':'U','original_reduct_countermodel':H.jsonable(point),
            'is_full_source_countermodel':False,'new_certificate':'refined_context_bound',
            'reason':'Same full-source set, different target-unit reduct; F08 U1.'},
        'not_claimed':['formal verification of Python runtime','general proof search','implemented general S8 affine compiler',
                       'independent external review','empirical source validity','global novelty']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json',type=Path,required=True)
    args = parser.parse_args()
    result = report()
    args.json.parent.mkdir(parents=True,exist_ok=True)
    args.json.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(f"Checked and saved {len(result['certificates'])} native certificates.")


if __name__ == '__main__': main()
