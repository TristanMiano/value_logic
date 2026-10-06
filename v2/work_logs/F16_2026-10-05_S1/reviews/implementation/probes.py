"""F16 hand-selected exact implementation attacks; no population generation.

Run from the repository root with PYTHONDONTWRITEBYTECODE=1. All output stays
beside this file. Ordinary frozen dataclasses, exact integers/Fractions only.
This is finite corroboration and attempted falsification, not formal proof.
"""
from __future__ import annotations

from dataclasses import asdict, is_dataclass, replace
from datetime import datetime, timezone
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import traceback

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from v2.checks import f05_semantics as S
from v2.checks import f06_inference_rules as K
from v2.checks import f06_source_transport as T
from v2.checks import f07_soundness as A
from v2.verification import catalogue, native, receipts, selected_cache
from v2.verification import program, program_control, program_reference
from v2.verification.model import Evidence, Query
from v2.verification.producer import Limits, produce
from v2.verification.reference import reference, task_losses
from v2.verification.reuse import reuse
from v2.verification.program_model import ProgramEvidence, ProgramQuery

BASELINE = '6ef27f20e3ac0920953a27dd84d6c91a021ba58f'
SOURCES = (
    'v2/checks/f05_semantics.py', 'v2/checks/f06_inference_rules.py',
    'v2/checks/f06_source_transport.py', 'v2/checks/f07_soundness.py',
    'v2/checks/f06_derived_cases.py', 'v2/verification/model.py',
    'v2/verification/native.py', 'v2/verification/producer.py',
    'v2/verification/reference.py', 'v2/verification/receipts.py',
    'v2/verification/reuse.py', 'v2/verification/selected_cache.py',
    'v2/verification/catalogue.py', 'v2/verification/program.py',
    'v2/verification/program_model.py', 'v2/verification/program_reference.py',
    'v2/verification/program_control.py', 'v2/verification/program_differential.py',
    'v2/verification/experiment.py', 'v2/verification/README.md',
    'v2/verification/F12_results.md', 'v2/verification/F12_test_design.md',
    'v2/work_logs/F11_2026-10-03_S1.md', 'v2/work_logs/F12_2026-10-03_S1.md',
    'v2/derivations/03_soundness.md', 'v2/derivations/03a_soundness_scope_and_use.md',
)
ATTEMPT = sys.argv[1] if len(sys.argv) > 1 else 'attempt1'
OUTPUT = HERE / f'{ATTEMPT}.jsonl'
if OUTPUT.exists():
    raise SystemExit('Refusing to overwrite a retained attempt.')
RESULTS = []


def plain(value):
    if isinstance(value, Q):
        return str(value)
    if is_dataclass(value):
        return plain(asdict(value))
    if isinstance(value, dict):
        return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, (tuple, list, set, frozenset)):
        return [plain(v) for v in value]
    return value


def record(name, fn, *, rejects=()):
    result = {'name': name}
    try:
        result['details'] = plain(fn())
        result['status'] = 'FAIL' if rejects else 'PASS'
        if rejects:
            result['failure'] = 'Unexpected acceptance instead of required rejection.'
    except Exception as error:
        result['exception'] = type(error).__name__
        result['message'] = str(error)
        result['status'] = 'PASS' if isinstance(error, rejects) else 'FAIL'
        if result['status'] == 'FAIL':
            result['traceback'] = traceback.format_exc()
    RESULTS.append(result)
    line = json.dumps(result, sort_keys=True)
    with OUTPUT.open('a', encoding='utf-8') as stream:
        stream.write(line + '\n')
    print(line, flush=True)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def brief(outcome):
    return {'status': outcome.status, 'reason': outcome.reason,
            'bound': outcome.upper_bound, 'proof_steps': 0 if outcome.proof is None else len(outcome.proof.steps),
            'basis_checks': getattr(outcome, 'basis_checks', None),
            'row_candidate_checks': getattr(outcome, 'row_candidate_checks', None)}


def source_manifest():
    rows = []
    for source in SOURCES:
        present = (ROOT / source).read_bytes()
        original = subprocess.run(['git', 'show', f'{BASELINE}:{source}'], cwd=ROOT,
                                  check=True, capture_output=True).stdout
        rows.append({'path': source, 'sha256': hashlib.sha256(present).hexdigest(),
                     'baseline_sha256': hashlib.sha256(original).hexdigest(),
                     'unchanged_from_baseline': present == original})
    data = {'baseline': BASELINE, 'utc': datetime.now(timezone.utc).isoformat(),
            'reviewer': 'ChatGPT (GPT-6 Astra Pro), separate implementation audit agent',
            'principal_minutes_credited': 0,
            'python': sys.version, 'attempt': ATTEMPT,
            'probe_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'sources': rows}
    (HERE / f'{ATTEMPT}_source_manifest.json').write_text(json.dumps(data, indent=2) + '\n')
    require(all(row['unchanged_from_baseline'] for row in rows), 'Reviewed baseline source was changed.')
    return {'source_count': len(rows), 'all_unchanged': True}


def receiver_attacks():
    x, z = K.src('x'), K.num(0)
    sig = K.Signature('F16-request-contract', ('U', 'V'), (('x', 'U'),))
    ctx = K.Context(sig, 'same-observation', 'v1', (
        K.Case('a', (K.Row(x, z),), (('x', Q(0)),)),
        K.Case('b', (K.Row(x, K.num(1)),), (('x', Q(1)),))))
    b = K.Builder(ctx, 'a'); local_index = b.rewrite(b.row(0), x, z)
    local = b.proof(local_index)
    expected = A.request(ctx, 'a', x, z, 0)
    record('receiver_valid_local_equality', lambda: A.receive(ctx, local, expected).budget)
    for name, request in (
        ('receiver_wrong_global_scope', replace(expected, case=None)),
        ('receiver_wrong_local_case', replace(expected, case='b')),
        ('receiver_wrong_unit', replace(expected, unit='V')),
        ('receiver_stricter_budget', replace(expected, budget=-Q(1, 2**255))),
        ('receiver_different_pair', replace(expected, old=K.num(-1))),
        ('receiver_equivalent_but_nonliteral_pair', replace(expected, new=K.add(x, z))),
    ):
        record(name, lambda request=request: A.receive(ctx, local, request), rejects=(A.AuditError,))
    for label, changed in (
        ('revision', replace(ctx, revision='v2')),
        ('observation', replace(ctx, observation='changed')),
        ('scope', replace(ctx, signature=replace(sig, scope='changed-interpretation'))),
        ('row_with_same_revision', replace(ctx, cases=(replace(ctx.cases[0], rows=(K.Row(x, K.num(2)),)), ctx.cases[1]))),
    ):
        record(f'receiver_stale_request_{label}', lambda changed=changed: A.receive(changed, local, expected), rejects=(A.AuditError,))
        record(f'receiver_stale_proof_{label}', lambda changed=changed: A.receive(changed, local, A.request(changed, 'a', x, z, 0)), rejects=(K.ProofError,))
    b.case = 'b'; other = b.rewrite(b.row(0), x, z)
    whole = b.proof(b.all_cases((local_index, other)))
    record('receiver_union_maximum', lambda: A.receive(ctx, whole, A.request(ctx, None, x, z, 1)).budget)
    record('receiver_union_not_best_case', lambda: A.receive(ctx, whole, A.request(ctx, None, x, z, 0)), rejects=(A.AuditError,))
    forged = replace(whole, steps=whole.steps[:-1] + (replace(whole.steps[-1], budget=Q(0)),))
    record('kernel_forged_union_budget', lambda: K.check(ctx, forged), rejects=(K.ProofError,))
    missing = replace(whole, steps=whole.steps[:-1] + (replace(whole.steps[-1], parents=(local_index,), budget=Q(0)),))
    record('kernel_omitted_live_case', lambda: K.check(ctx, missing), rejects=(K.ProofError,))


def source_attacks():
    x, y, z = K.src('x'), K.src('y'), K.num(0)
    old = K.context(('x', 'y'), (K.Row(x, z),), {'x': 0, 'y': 0}, scope='F16-source')
    b = K.Builder(old, 'h'); p = b.proof(b.rewrite(b.row(0), x, z))
    empty = replace(old, revision='withdrawn', cases=(replace(old.cases[0], rows=()),))
    record('transport_missing_nonconstant_source', lambda: T.transport(old, empty, p, {}, {'h': 'h'}), rejects=(T.UnavailableProof,))
    other = replace(old, revision='other-direction', cases=(replace(old.cases[0], rows=(K.Row(y, z),)),))
    nb = K.Builder(other, 'h'); q = nb.proof(nb.rewrite(nb.row(0), y, z))
    replacement = {('h', 'h', 0): q}
    record('transport_wrong_replacement_direction', lambda: T.transport(old, other, p, replacement, {'h': 'h'}), rejects=(K.ProofError,))
    mapped = T.transport(old, other, p, replacement, {'h': 'h'}, {'x': y, 'y': x})
    record('transport_explicit_substitution_changes_request', lambda: A.receive(other, mapped, A.request(other, None, y, z, 0)).budget)
    record('transport_substitution_does_not_prove_original_pair', lambda: A.receive(other, mapped, A.request(other, None, x, z, 0)), rejects=(A.AuditError,))
    record('transport_omitted_source_map_key', lambda: T.transport(old, other, p, replacement, {'h': 'h'}, {'x': y}), rejects=(K.ProofError,))
    record('transport_free_local_replacement', lambda: T.transport(old, other, p, replacement, {'h': 'h'}, {'x': K.loc('a'), 'y': y}), rejects=(S.SemanticError,))
    record('transport_changed_interpretation', lambda: T.transport(old, replace(other, observation='new-observation'), p, replacement, {'h': 'h'}), rejects=(K.ProofError,))
    bz = K.Builder(old, 'h'); zero = bz.proof(bz.scale(0, bz.row(0)))
    constant = T.transport(old, empty, zero, {}, {'h': 'h'})
    record('withdrawn_zero_dependence_is_constant', lambda: {'budget': K.check(empty, constant).budget, 'used_rows': sorted(T.used_rows(empty, constant)), 'point': A.audit_points(empty, constant, [{'x': 37, 'y': -11}])})
    mixed = K.context(('x',), (), {'x': 0}, units=('U', 'V'), scope='F16-zero-type')
    record('zero_scale_preserves_type_check', lambda: K.infer(K.scale(0, K.add(x, K.num(0, 'V'))), mixed.signature), rejects=(S.SemanticError,))
    alt = K.context(('x',), (K.Row(x, z), K.Row(x, K.num(1))), {'x': 0}, scope='F16-alternative')
    ba = K.Builder(alt, 'h'); r = ba.rewrite(ba.row(0), x, z); s = ba.rewrite(ba.row(1), x, z)
    pa = ba.proof(ba.meet(r, s))
    current, weakened = T.restrict_rows(alt, pa, frozenset({('h', 1)}), revision='removed-best-row')
    record('withdrawal_recomputes_surviving_alternative', lambda: {'old': K.check(alt, pa).budget, 'new': A.receive(current, weakened, A.request(current, None, x, z, 1)).budget, 'new_point_refutes_old_budget': S.check_point(current, S.goal(current, x, z, 0), 'h', {'x': 1})})
    record('withdrawal_cannot_keep_old_budget', lambda: A.receive(current, weakened, A.request(current, None, x, z, 0)), rejects=(A.AuditError,))
    record('withdrawal_no_remaining_alternative', lambda: T.restrict_rows(alt, pa, frozenset()), rejects=(T.UnavailableProof,))
    relaxed = replace(old, revision='relaxed', cases=(replace(old.cases[0], rows=(K.Row(x, K.num(2)),)),))
    replayed = K.replay(old, relaxed, p)
    record('rhs_replay_recalculates_budget', lambda: A.receive(relaxed, replayed, A.request(relaxed, 'h', x, z, 2)).budget)
    record('rhs_replay_rejects_changed_direction', lambda: K.replay(old, other, p), rejects=(K.ProofError,))


def signed_native_probe():
    x, y, z = K.src('x'), K.src('y'), K.num(0)
    ctx = K.context(('x', 'y'), (K.Row(x, K.num(-Q(1, 3))), K.Row(y, K.num(Q(1, 2))),
        K.Row(K.scale(-1, x), K.num(1)), K.Row(K.scale(-1, y), K.num(Q(1, 2)))),
        {'x': -Q(1, 3), 'y': Q(1, 2)}, scope='F16-signed-native', units=('U', 'V'),
        conversions=(K.Conversion('uv', 'U', 'V', Q(3, 2)),))
    b = K.Builder(ctx, 'h'); rx = b.rewrite(b.row(0), x, z); ry = b.rewrite(b.row(1), y, z)
    b.constant(K.add(x, K.num(Q(1, 7))), x)
    b.trans(b.rewrite(rx, K.add(x, y), y), ry); b.add(rx, ry); b.scale(Q(3, 7), rx)
    nx, ny = b.negate(rx), b.negate(ry)
    converted = b.conversion('uv', rx); loose = b.slack(Q(1, 6), rx); b.meet(rx, loose)
    b.max_common(rx, ry); b.min_common(nx, ny)
    b.congruence('min', rx, ry); b.congruence('max', rx, ry)
    residual_index = b.res_congruence(rx, ry); clipped = b.res_congruence(rx, rx)
    for tag in ('min_left', 'min_right', 'max_left', 'max_right'):
        b.lattice(tag, x, y)
    p = b.proof(b.all_cases((rx,)))
    points = ({'x': -Q(1, 3), 'y': Q(1, 2)}, {'x': -1, 'y': -Q(1, 2)}, {'x': -Q(5, 7), 'y': Q(2, 9)})
    require({step.rule for step in p.steps} == A.NATIVE_RULES, 'Not every native tag was covered.')
    require(p.steps[converted].budget == -Q(1, 2), 'Positive conversion lost negative bound.')
    require(p.steps[residual_index].budget == Q(1, 6) and p.steps[clipped].budget == 0, 'Residual budget recurrence mismatch.')
    result = A.audit_points(ctx, p, points)
    lexical = K.let('a', x, K.let('a', K.add(K.loc('a'), K.num(1)), K.sub(K.loc('a'), x)))
    require(all(A.value(lexical, ctx.signature, point) == 1 and S.evaluate(lexical, ctx.signature, point) == 1 for point in points), 'Lexical shadowing mismatch.')
    return {'tags': sorted(A.NATIVE_RULES), 'steps': len(p.steps), 'points': points, 'checks': result, 'negative_converted_bound': p.steps[converted].budget, 'residual_bound': p.steps[residual_index].budget, 'negative_sum_residual_bound': p.steps[clipped].budget, 'lexical_value': 1}


def scientific_and_receipt_attacks():
    # Fixed hand-selected points; no random generator or Cartesian population.
    points = ((Q(0), Q(0)), (-Q(7, 13), Q(5, 17)), (Q(-1), Q(1)), (Q(1, 2**255), -Q(1, 2**254)))
    def loss_encoding():
        ctx = native.context(Evidence())
        checked = []
        for point in points:
            losses = task_losses(point)
            actual = {action: A.value(native.loss(action), ctx.signature, dict(zip(('beta', 'gamma'), point))) for action in ('T1', 'T2', 'R', 'F')}
            require(actual == losses, 'Native frozen loss differs from exact polynomial execution.')
            checked.append({'point': point, 'losses': losses})
        return checked
    record('scientific_loss_encoding_direct_execution', loss_encoding)
    old, query = Evidence(0, 0, 0, 0, 'F16-origin'), Query('T1')
    original = produce(old, query)
    payload = receipts.make_receipt(old, query, original)
    record('receipt_original_current_request', lambda: receipts.receive_receipt(old, query, payload).budget)
    record('receipt_wrong_action', lambda: receipts.receive_receipt(old, Query('R'), payload), rejects=(receipts.ReceiptError,))
    record('receipt_strict_exact_strength', lambda: receipts.receive_receipt(old, Query('T1', original.upper_bound-Q(1, 2**255)), payload), rejects=(A.AuditError,))
    record('receipt_new_revision_same_bounds', lambda: receipts.receive_receipt(replace(old, revision='F16-version-only'), query, payload), rejects=(receipts.ReceiptError,))
    current = Evidence(beta=0, gamma=Q(3, 32), revision='F16-relaxed-strict-margin')
    record('receipt_withdrawn_source', lambda: receipts.receive_receipt(current, query, payload), rejects=(receipts.ReceiptError,))
    changed_action = json.loads(json.dumps(payload)); changed_action['action'] = 'R'
    record('receipt_action_metadata_cannot_rebind_root', lambda: receipts.decode_receipt(changed_action), rejects=(A.AuditError,))
    changed_bound = json.loads(json.dumps(payload)); changed_bound['bound'] = '0'
    record('receipt_bound_metadata_cannot_replace_root', lambda: receipts.receive_receipt(old, query, changed_bound), rejects=(receipts.ReceiptError,))
    # Relabel a genuine historical proof with current identity: arithmetic must still fail.
    same_schema_relaxed = Evidence(1, 1, 1, 1, 'F16-relabeled')
    relabeled = json.loads(json.dumps(payload)); relabeled['evidence'] = receipts.evidence_payload(same_schema_relaxed)
    for step in relabeled['proof']['steps']:
        step['context_id'] = K.fingerprint(native.context(same_schema_relaxed))
    record('receipt_relabeling_does_not_skip_source_arithmetic', lambda: receipts.receive_receipt(same_schema_relaxed, query, relabeled), rejects=(K.ProofError,))
    fresh, rebuilt, semantic = produce(current, query), reuse(current, query, payload), reference(current, query)
    def reconstruction_miss():
        require(fresh.upper_bound == semantic.maximum == -Q(3, 8192), 'Known strict-margin fresh value changed.')
        require(rebuilt.status == 'unavailable' and rebuilt.upper_bound == Q(3, 8192), 'Retained miss was mislabeled or changed.')
        return {'source': current, 'query': query, 'fresh': brief(fresh), 'reused': brief(rebuilt), 'reference': semantic}
    record('documented_strict_reconstruction_miss', reconstruction_miss)
    rebuilt_payload = receipts.make_receipt(current, query, rebuilt)
    record('reused_bound_receipt_accepts_only_weaker_request', lambda: receipts.receive_receipt(current, Query('T1', Q(3, 8192)), rebuilt_payload).budget)
    record('reused_miss_not_current_zero_certificate', lambda: receipts.receive_receipt(current, query, rebuilt_payload), rejects=(A.AuditError,))
    fresh_payload = receipts.make_receipt(current, query, fresh)
    record('fresh_boundary_budget_is_accepted', lambda: receipts.receive_receipt(current, Query('T1', semantic.maximum), fresh_payload).budget)
    record('fresh_stricter_budget_is_rejected', lambda: receipts.receive_receipt(current, Query('T1', semantic.maximum-Q(1, 2**240)), fresh_payload), rejects=(A.AuditError,))
    def zero_limits():
        basis = produce(old, query, Limits(0, 128)); steps = produce(old, query, Limits(440, 0))
        require(basis.status == steps.status == 'unavailable' and basis.proof is None and steps.proof is None, 'Resource refusal became acceptance.')
        return {'basis_limit_zero': brief(basis), 'step_limit_zero': brief(steps), 'reference': reference(old, query).maximum}
    record('producer_zero_resource_limits_are_unavailable', zero_limits)
    # One unusual exact source exercises large admitted denominators and asymmetry.
    unusual = Evidence(Q(1, 2**255), Q(7, 19), Q(5, 23), Q(3, 29), 'F16-large-rational')
    def unusual_source():
        outcome = produce(unusual, Query('R', 2)); semantic = reference(unusual, Query('R', 2))
        require(outcome.upper_bound == semantic.maximum, 'Large-rational producer/reference discrepancy.')
        wire = receipts.make_receipt(unusual, Query('R', 2), outcome)
        checked = receipts.receive_receipt(unusual, Query('R', semantic.maximum), wire)
        return {'source': unusual, 'bound': semantic.maximum, 'witness': semantic.witness, 'bound_component_bits': max(abs(checked.budget.numerator).bit_length(), checked.budget.denominator.bit_length()), 'steps': len(outcome.proof.steps)}
    record('scientific_large_rational_current_receipt', unusual_source)


def cache_attacks():
    origin = Evidence(Q(1, 8), Q(1, 9), Q(1, 7), Q(1, 6), 'F16-cache-origin')
    relaxed = Evidence(2, 2, 1, 1, 'F16-cache-relaxed')
    query = Query('T1', 3)
    outcome = produce(origin, query)
    selected = selected_cache.from_outcome(origin, query, outcome)
    cat = catalogue.build(origin, query)
    def same_schema():
        selected_out = selected_cache.replay(relaxed, query, selected)
        cat_out = catalogue.select(relaxed, query, cat).outcome
        truth = reference(relaxed, query).maximum
        for out in (selected_out, cat_out):
            require(out.status == 'certified' and out.upper_bound >= truth, 'Cache produced unsafe current bound.')
            A.receive(native.context(relaxed), out.proof, native.request(native.context(relaxed), query))
        return {'origin_bound': outcome.upper_bound, 'current_reference': truth, 'selected': brief(selected_out), 'catalogue': brief(cat_out)}
    record('same_direction_cache_rechecks_current_relaxation', same_schema)
    def refuses():
        rows_changed = replace(relaxed, plus=None)
        answers = {'selected_rows_changed': selected_cache.replay(rows_changed, query, selected),
                   'catalogue_rows_changed': catalogue.select(rows_changed, query, cat).outcome,
                   'selected_action_changed': selected_cache.replay(origin, Query('R', 3), selected),
                   'catalogue_action_changed': catalogue.select(origin, Query('R', 3), cat).outcome,
                   'selected_tight_request': selected_cache.replay(relaxed, Query('T1', 0), selected),
                   'empty_catalogue': catalogue.select(origin, query, catalogue.build(origin, query, max_bases=0)).outcome}
        require(all(out.status == 'unavailable' and out.proof is None for out in answers.values()), 'Schema/screen refusal furnished an unchecked proof.')
        return {key: brief(out) for key, out in answers.items()}
    record('cache_schema_and_numeric_screen_refusals', refuses)
    mislabeled = replace(selected, action='R')
    record('wrong_cached_coefficients_cannot_prove_new_action', lambda: selected_cache.replay(origin, Query('R', 3), mislabeled), rejects=(K.ProofError,))


def program_attacks():
    evidence = ProgramEvidence(foreign_zero=True, revision='F16-unit-reduct')
    query = ProgramQuery('risk_vs_full', budget=-Q(1, 20))
    def separation():
        answer = program_control.assess(evidence, query)
        require(answer['decision'] == 'unavailable' and not answer['reduct_attainer_satisfies_full_source'], 'Reduct witness was promoted to full-source refutation.')
        require(answer['native_bound'] == '-1/40' and answer['full_source_maximum'] == '-3/40', 'Expected unit-boundary values changed.')
        return answer
    record('program_full_source_reduct_separation', separation)
    ctx = program.context(evidence); outcome = program.produce(evidence, query)
    _, reduct_point = program_reference.reference(evidence, query, reduct=True)
    new, old, _ = program.terms(query)
    record('reduct_attainer_rejected_as_full_source_point', lambda: S.check_point(ctx, S.goal(ctx, new, old, query.budget), 'h', dict(zip(('error', 'second'), reduct_point))), rejects=(S.SemanticError,))
    record('program_insufficient_reduct_proof_rejected', lambda: A.receive(ctx, outcome.proof, program.request(ctx, query)), rejects=(A.AuditError,))
    changed = ProgramQuery('mean_edit')
    record('program_changed_consumer_rejected', lambda: A.receive(ctx, outcome.proof, program.request(ctx, changed)), rejects=(A.AuditError,))
    def near_one_alpha():
        extreme = ProgramQuery('risk_vs_full', alpha=1-Q(1, 2**255), budget=0)
        out = program.produce(evidence, extreme)
        full, full_point = program_reference.reference(evidence, extreme)
        reduct, reduct_point = program_reference.reference(evidence, extreme, reduct=True)
        require(out.status == 'unavailable' and out.upper_bound == reduct == Q(17, 20) and full == 0, 'Near-one confidence lost exact atom behavior or domain separation.')
        return {'alpha': extreme.alpha, 'producer': brief(out), 'full': full, 'reduct': reduct, 'full_point': full_point, 'reduct_point': reduct_point}
    record('program_near_one_exact_tail_confidence', near_one_alpha)
    def strict_boundary():
        mean_evidence = ProgramEvidence(second_cap=Q(9, 40), revision='F16-mean-equality')
        equality = program_control.assess(mean_evidence, ProgramQuery())
        strict = program_control.assess(mean_evidence, ProgramQuery(budget=-Q(1, 2**255)))
        require(equality['decision'] == 'certified' and strict['decision'] == 'refuted', 'Exact strict inequality was rounded or confused.')
        return {'equality': equality, 'stricter': strict}
    record('program_exact_zero_vs_strict_refutation', strict_boundary)


record('source_manifest', source_manifest)
for name, operation in (
    ('receiver_probe_setup', receiver_attacks),
    ('source_probe_setup', source_attacks),
    ('signed_native_16_tags', signed_native_probe),
    ('scientific_probe_setup', scientific_and_receipt_attacks),
    ('cache_probe_setup', cache_attacks),
    ('program_probe_setup', program_attacks),
):
    record(name, operation)
summary = {'attempt': ATTEMPT, 'records': len(RESULTS),
           'passed': sum(row['status'] == 'PASS' for row in RESULTS),
           'failed': sum(row['status'] == 'FAIL' for row in RESULTS),
           'failures': [row for row in RESULTS if row['status'] == 'FAIL'],
           'status': 'PASS' if all(row['status'] == 'PASS' for row in RESULTS) else 'FAIL',
           'scope': 'Hand-selected exact attacks only; no full suite, population generation, F15/ND01 replay, time credit, or unrestricted soundness claim.'}
(HERE / f'{ATTEMPT}_summary.json').write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')
print(json.dumps(summary, sort_keys=True), flush=True)
raise SystemExit(0 if summary['status'] == 'PASS' else 1)
