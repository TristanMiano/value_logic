#!/usr/bin/env python3
"""Bind an additive review draft and reconstruct fixed saved-record claims.

Standard-library inspection only. No worker, proof checker, benchmark, policy
or prior analyzer is imported or executed. Zero principal research credit.
All output paths are newly created inside this review directory.
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(sys.argv[1]).resolve()
HERE = Path(__file__).resolve().parent
PREFIX = 'v3/work_logs/R_P3_B_B_2026-10-10_S1/'
INPUTS = {}
CHECKS = []
EVIDENCE = {
    'prior_overlay': 'v3/checkpoints/B_1_P3_08.v1.json',
    'prior_overlay_prose': 'v3/checkpoints/B_1_P3_08.md',
    'duties': 'v3/foundations/01_desiderata.md',
    'problem_contract': 'v3/foundations/01_problem_contract.md',
    'derivation': 'v3/derivations/05_equal_certificate_delivery.md',
    'experiment': 'v3/experiments/certificate_delivery.md',
    'contribution': PREFIX + 'contribution_assessment.md',
    'selection': PREFIX + 'selection.json',
    'forecast': PREFIX + 'forecast.json',
    'prior_assessment': PREFIX + 'reviews/literature_and_obstruction/desiderata_and_questions_assessment.md',
    'finite_review': PREFIX + 'reviews/literature_and_obstruction/finite_obstruction_v1/proof_and_results.md',
    'fresh_work_review': PREFIX + 'reviews/literature_and_obstruction/fresh_receiver_work_bound.md',
    'receiver_review': PREFIX + 'reviews/literature_and_obstruction/receiver_static_v1/review.md',
    'service_review': PREFIX + 'reviews/receiver_reconstruction/service_audit_v5/review.md',
    'rational_review': PREFIX + 'reviews/literature_and_obstruction/rational_integrity_retry_v1/review.md',
    'rational_review_results': PREFIX + 'reviews/literature_and_obstruction/rational_integrity_retry_v1/run/results.json',
    'rational_retry_summary': PREFIX + 'development/rational_service_v1_retry1/summary.json',
    'rational_original_summary': PREFIX + 'development/rational_service_v1/summary.json',
    'primary_summary': PREFIX + 'development/primary_v5/summary.json',
    'primary_analysis': PREFIX + 'development/primary_analysis_v1/analysis.json',
    'primary_prices': PREFIX + 'development/primary_prices_v1/prices.json',
    'secondary_summary': PREFIX + 'development/secondary_pruning_v1/summary.json',
    'secondary_analysis': PREFIX + 'development/secondary_analysis_v1/analysis.json',
    'cap_plan': PREFIX + 'development/consumer_cap_interpretation_v1.md',
    'cap_summary': PREFIX + 'development/actual_consumer_cap_v1/summary.json',
    'cap_analysis': PREFIX + 'development/actual_consumer_cap_analysis_v1/analysis.json',
    'cap_analyzer_source': 'v3/checks/05_certificate_delivery_cap_analyze.py',
    'todo': 'TODO_v3.md',
    'claim_ledger': 'v3/claim_ledger.md',
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(relative):
    raw = (ROOT / relative).read_bytes()
    item = {'bytes': len(raw), 'sha256': sha(raw)}
    if relative in INPUTS:
        assert INPUTS[relative] == item, ('Input changed while reading', relative)
    INPUTS[relative] = item
    return raw


def record(relative):
    return json.loads(read(relative))


def check(value, label):
    CHECKS.append({'label': label, 'holds': bool(value)})


def write_json(path, value):
    with path.open('x') as handle:
        json.dump(value, handle, sort_keys=True, indent=2)
        handle.write('\n')


CAPTURE = HERE / 'source_snapshot'
CAPTURE.mkdir(exist_ok=False)
for evidence_key, relative in EVIDENCE.items():
    raw = read(relative)
    # Preserve current narrative and review premises. Sealed run data stay in
    # their existing immutable archives and are bound by hashes below.
    if ('/development/' not in relative or evidence_key == 'cap_plan') and not relative.endswith('/run/results.json'):
        target = CAPTURE / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as handle:
            handle.write(raw)
draft_data_path = str((HERE / 'duty_drafts.json').relative_to(ROOT))
draft_data = record(draft_data_path)
read(str(Path(__file__).resolve().relative_to(ROOT)))
prior = record(EVIDENCE['prior_overlay'])
prior_by_id = {d['id']: d for d in prior['duties']}
check([d['id'] for d in draft_data] == [d['id'] for d in prior['duties']],
      'Draft has exactly the same 21 duty IDs and order as the latest overlay')
check(len(draft_data) == len(prior_by_id) == 21, 'Exactly 21 unique duties')

methods = ['P-REUSE', 'P-FRESH', 'O-ADD-COLD', 'O-ADD-WARM',
           'O-ENUM-RECEIVER', 'O-ADD-PORTFOLIO']
runs = {}
for name in ['primary_v5', 'actual_consumer_cap_v1']:
    base = PREFIX + 'development/' + name + '/'
    summary = record(base + 'summary.json')
    manifest = record(base + 'manifest.json')
    raw = read(base + 'completed_units.jsonl')
    rows = [json.loads(line) for line in raw.splitlines()]
    check(summary['status'] == 'PASS' and summary['error'] is None, name + ': author PASS summary')
    check(summary['manifest_sha256'] == INPUTS[base + 'manifest.json']['sha256'], name + ': manifest seal')
    check(summary['completed_units_sha256'] == sha(raw), name + ': complete row seal')
    check(summary['units'] == len(rows), name + ': row count seal')
    check(summary['source_hashes'] == manifest['source_hashes'], name + ': source manifest agreement')
    for relative, expected in manifest['source_hashes'].items():
        check(sha(read(relative)) == expected, name + ': current source/input ' + relative)
        check(sha(read(base + 'sources/' + relative)) == expected, name + ': captured source/input ' + relative)
    deliveries = [r for r in rows if 'method' in r and 'invoice' in r]
    check(len(deliveries) == 288, name + ': exactly 288 attempts')
    by_key = {(r['stream'], r['recipient'], r['method'], r['request_index']): r for r in deliveries}
    check(len(by_key) == 288, name + ': unique owned-session request keys')
    groups = defaultdict(list)
    for row in deliveries:
        groups[row['stream'], row['recipient'], row['method']].append(row)
        invoice = row['invoice']
        total = sum(sum(v.values()) for v in invoice['by_stage'].values())
        consumer = sum(sum(v.values()) for stage, v in invoice['by_stage'].items()
                       if stage.startswith('receiver_') or stage in ['terminal', 'failure_terminal', 'common_source'])
        check(total == invoice['total_units'] and consumer == invoice['consumer_units'], name + ': independent invoice sums')
    for group in groups.values():
        group.sort(key=lambda r: r['request_index'])
        check([r['request_index'] for r in group] == list(range(1, 7)), name + ': complete issued sequence')
    runs[name] = {'summary': summary, 'manifest': manifest, 'rows': deliveries,
                  'by_key': by_key, 'groups': groups}

primary = runs['primary_v5']
cap = runs['actual_consumer_cap_v1']
cells = sorted({(r['stream'], r['recipient']) for r in primary['rows']})
check(len(cells) == 8, 'Eight fixed stream/recipient cells')
check(all(r['status'] == 'DELIVERED' for r in primary['rows']), 'Primary all 288 delivered')
primary_cells = []
primary_prefixes = []
cold_crossings = []
for stream, recipient in cells:
    totals = {method: sum(r['invoice']['total_units'] for r in primary['groups'][stream, recipient, method])
              for method in methods}
    least = [m for m in methods if totals[m] == min(totals.values())]
    check(least == ['O-ENUM-RECEIVER'], 'Primary direct ordinary uniquely least in cell')
    primary_cells.append({'stream': stream, 'recipient': recipient, 'totals': totals, 'least': least})
    pooled = {m: Counter() for m in ['P-REUSE', 'O-ENUM-RECEIVER']}
    cold_delta = 0
    deltas = []
    for index in range(1, 7):
        for method in pooled:
            row = primary['by_key'][stream, recipient, method, index]
            for values in row['invoice']['by_stage'].values():
                pooled[method].update(values)
        q, p = pooled['O-ENUM-RECEIVER'], pooled['P-REUSE']
        dominates = all(q[c] <= p[c] for c in set(q) | set(p))
        check(dominates, 'Primary ordinary pooled-category prefix dominance')
        enum_row = primary['by_key'][stream, recipient, 'O-ENUM-RECEIVER', index]
        reuse_row = primary['by_key'][stream, recipient, 'P-REUSE', index]
        check(enum_row['invoice']['total_units'] < reuse_row['invoice']['total_units'],
              'Primary ordinary strictly lower paired request total')
        primary_prefixes.append({'stream': stream, 'recipient': recipient, 'prefix': index,
                                 'ordinary_category_dominance': dominates})
        cold_delta += (primary['by_key'][stream, recipient, 'O-ADD-COLD', index]['invoice']['total_units'] -
                       reuse_row['invoice']['total_units'])
        deltas.append(cold_delta)
    if recipient == 'resident' and stream != 'constant_n3':
        first = next((i for i, v in enumerate(deltas, 1) if v > 0), None)
        sustained = next((i for i in range(1, 7) if all(v > 0 for v in deltas[i-1:])), None)
        cold_crossings.append({'stream': stream, 'recipient': recipient, 'cold_minus_reuse_prefixes': deltas,
                               'first_strict_crossing': first, 'sustained_to_end_crossing': sustained})

cap_analysis = record(EVIDENCE['cap_analysis'])
check(cap_analysis['input_completed_units_sha256'] == cap['summary']['completed_units_sha256'],
      'Saved cap analysis uses complete capped rows')
check(cap_analysis['input_manifest_sha256'] == cap['summary']['manifest_sha256'],
      'Saved cap analysis uses exact capped manifest')
cap_aggregates = {}
failure_stages = Counter()
discrepancies = []
for method in methods:
    rows = [r for r in cap['rows'] if r['method'] == method]
    aggregate = {'attempts': 48, 'delivered': 0, 'failed': 0, 'total_units': 0, 'consumer_units': 0,
                 'failure_total_units': 0, 'failure_consumer_units': 0, 'static_bill_fits': 0,
                 'static_bill_plus_reserve_fits': 0, 'predicted_fit_but_failed': 0,
                 'predicted_unfit_but_delivered': 0}
    for row in rows:
        k = row['stream'], row['recipient'], row['method'], row['request_index']
        primary_row = primary['by_key'][k]
        invoice = row['invoice']
        delivered = row['status'] == 'DELIVERED'
        aggregate['delivered' if delivered else 'failed'] += 1
        aggregate['total_units'] += invoice['total_units']
        aggregate['consumer_units'] += invoice['consumer_units']
        check(invoice['budget'] == 2**27 and invoice['consumer_budget'] == 2**20,
              'Cap run exact total and consumer accounts')
        check(invoice['total_units'] <= 2**27 and invoice['consumer_units'] <= 2**20,
              'Cap run recorded bills within accounts')
        state = row['observer_state']
        check(state['current_receipt_present'] == delivered and not state['stale_receipts_present'],
              'Cap recorded current/stale receipt boundary')
        check(state['source_enrolled'] is True, 'Source stays installed through scientific failure')
        if delivered:
            check(row['output'] == primary_row['output'], 'Delivered capped output exactly equals primary output')
            check(invoice['total_units'] + 1024 <= 2**27 and invoice['consumer_units'] + 1024 <= 2**20,
                  'Successful capped bill includes capacity for both reserves')
        else:
            aggregate['failure_total_units'] += invoice['total_units']
            aggregate['failure_consumer_units'] += invoice['consumer_units']
            check(state['scientific_state_empty'] is True, 'Cap failed scientific state recorded empty')
            check(row['error']['type'] == 'ResourceExhausted', 'Cap expected failure type')
            check(sum(invoice['by_stage']['failure_terminal'].values()) == 113, 'Cap failed footer paid')
            failure_stages[row['error']['type'], invoice['failure']['stage']] += 1
        source_units = sum(invoice['by_stage'].get('common_source', {}).values())
        check(source_units == (430041 if row['request_index'] == 1 else 0),
              'Cap source enrollment fee once per owned session')
        u = primary_row['invoice']['consumer_units']
        fit = u + 1024 <= 2**20
        aggregate['static_bill_fits'] += u <= 2**20
        aggregate['static_bill_plus_reserve_fits'] += fit
        if fit != delivered:
            direction = 'predicted_fit_but_failed' if fit else 'predicted_unfit_but_delivered'
            aggregate[direction] += 1
            discrepancies.append({'stream': row['stream'], 'recipient': row['recipient'], 'method': method,
                                  'request_index': row['request_index'], 'direction': direction,
                                  'primary_consumer_units': u, 'actual_consumer_units': invoice['consumer_units']})
    cap_aggregates[method] = aggregate
    check(aggregate == cap_analysis['aggregate_by_method'][method], 'Independent cap aggregate matches analyzer')
check(sum(v['delivered'] for v in cap_aggregates.values()) == 239, '239 actual capped deliveries')
check(sum(v['failed'] for v in cap_aggregates.values()) == 49, '49 actual capped failures')
check(len(discrepancies) == 12, 'Twelve unique static predicate discrepancies')
cap_prefixes = []
cap_cells = []
for stream, recipient in cells:
    for index in range(1, 7):
        entries = {}
        for method in methods:
            group = cap['groups'][stream, recipient, method][:index]
            entries[method] = {
                'served': sorted(r['request_id'] for r in group if r['status'] == 'DELIVERED'),
                'total_units': sum(r['invoice']['total_units'] for r in group),
                'consumer_units': sum(r['invoice']['consumer_units'] for r in group)}
        ordinary = entries['O-ENUM-RECEIVER']
        nonempty_dominance = bool(ordinary['served']) and all(
            set(ordinary['served']) >= set(row['served']) and ordinary['total_units'] < row['total_units']
            for method, row in entries.items() if method != 'O-ENUM-RECEIVER')
        all_empty = all(not row['served'] for row in entries.values())
        check(nonempty_dominance or all_empty, 'Cap prefix is ordinary coverage/cost winner or all-empty')
        cap_prefixes.append({'stream': stream, 'recipient': recipient, 'prefix': index,
                             'ordinary_nonempty_coverage_cost_dominance': nonempty_dominance,
                             'all_methods_delivered_nothing': all_empty})
        if index == 6:
            check(nonempty_dominance, 'Cap all eight final cells ordinary coverage/cost dominance')
            cap_cells.append({'stream': stream, 'recipient': recipient, 'methods': entries})
check(sum(r['ordinary_nonempty_coverage_cost_dominance'] for r in cap_prefixes) == 46,
      '46 of 48 prefixes have nonempty ordinary coverage/cost dominance')
counter_cell = next(c for c in cap_cells if c['stream'] == 'complementary_k5_n7' and c['recipient'] == 'resident')
warm = counter_cell['methods']['O-ADD-WARM']
enum = counter_cell['methods']['O-ENUM-RECEIVER']
check(warm['served'] == enum['served'] and warm['consumer_units'] < enum['consumer_units'] and
      enum['total_units'] < warm['total_units'], 'Cap total dominance is not consumer-vector dominance')

for relative, binding in list(INPUTS.items()):
    # Captured narrative may later be changed by its owner; this observation
    # binds the saved snapshot. Sealed data and inspected inputs must be stable
    # during this short read-only reconstruction.
    check({'bytes': len((ROOT / relative).read_bytes()), 'sha256': sha((ROOT / relative).read_bytes())} == binding,
          'Input stable during reconstruction: ' + relative)
failed = [c for c in CHECKS if not c['holds']]
observation = {
    'stage': 'DEVELOPMENT', 'review_mode': 'same-model nonblind artifact-only reconstruction',
    'worker_executions': 0, 'proof_checker_executions': 0, 'principal_clock_credit': 0,
    'status': 'PASS' if not failed else 'REVIEW_CHECK_FAILURE',
    'observational_checks': len(CHECKS), 'failures': failed,
    'primary_cells': primary_cells, 'primary_prefixes': primary_prefixes,
    'resident_nonconstant_cold_crossings': cold_crossings,
    'cap_aggregates': cap_aggregates, 'cap_cells': cap_cells,
    'cap_prefixes': cap_prefixes, 'cap_static_discrepancies': discrepancies,
    'cap_failure_stages': [{'type': t, 'stage': s, 'count': n} for (t, s), n in sorted(failure_stages.items())],
    'cap_consumer_vector_counterexample': {'cell': 'complementary_k5_n7/resident', 'warm': warm, 'direct': enum},
    'packet_note': 'This narrow reader does not recheck all blobs; captured-packet validation remains attributed to the named prior source-bound audits.',
    'inputs': INPUTS,
}
write_json(HERE / 'record_reconstruction.json', observation)

duties = []
for draft in draft_data:
    prior_duty = prior_by_id[draft['id']]
    duties.append({
        'id': draft['id'], 'title': prior_duty['title'],
        'prior_status': prior_duty['status'], 'inherited_scope_retained': prior_duty['scope'],
        'disposition': draft['disposition'],
        'proposed_status': draft.get('proposed_status', prior_duty['status']),
        'new_support': draft['new_support'], 'limitations_and_open_obligations': draft['limitations'],
        'evidence': [{'key': key, 'path': EVIDENCE[key], **INPUTS[EVIDENCE[key]]} for key in draft['evidence_keys']],
    })
overlay = {
    'schema': 'value_logic.R-P3-B-B.draft_scientific_overlay.v1',
    'kind': 'Independent review draft only; not an applied checkpoint or new phase gate',
    'stage': 'DEVELOPMENT', 'task': 'R-P3-B-B', 'attempt': 'R-P3-B-B-1',
    'contributor': 'ChatGPT (GPT-6 Astra Pro)',
    'review_mode': 'same-model nonblind, read-only with respect to prior artifacts',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'base_commit': '33c6d6795aac894bd3cf8575e44f1d6f38f6ae56',
    'prior_overlay': {'path': EVIDENCE['prior_overlay'], **INPUTS[EVIDENCE['prior_overlay']]},
    'scientific_disposition': 'No unresolved material scientific blocker identified within the explicitly restricted current receiving service and source-bound DEVELOPMENT comparisons.',
    'contribution': 'Retain P3-N01 SUPPORTED at its previously accepted modest formal-adaptation and implementation-synthesis scope; add the ordinary checked-evidence interface and consequential receiver-relative distinction.',
    'Q3': 'P3-H03 affirmative plurality advantage remains OPEN. The implemented ordinary control displaces a primary-catalogue total advantage; no universal impossibility of plurality follows.',
    'U04': 'Retain the earlier finite owned CNF broker integration closure. The present certificate receiver is a separate interface and has not been composed with the selective-feedback learner.',
    'completion_status': 'DRAFT_SCIENTIFIC_ASSESSMENT_ONLY; principal task scope/floor, stopped-clock actuals, preservation and publication closure are not decided here.',
    'research_minutes_credited': 0, 'worker_executions': 0,
    'duties': duties,
    'primary_observation': '288/288 delivered; direct ordinary uniquely least total in all eight full cells, lower on all 48 matched reuse requests, and pooled-category dominance on all 48 cumulative prefixes. Reuse crosses cold ADD only in resident parity and k3, at prefixes four and five.',
    'actual_cap_observation': '239/288 delivered and 49 paid failures; direct ordinary superset coverage with lower total in all eight full cells and 46 nonempty prefixes, with two all-empty prefixes excluded as successful service. Total dominance is not consumer-vector dominance.',
    'rational_integrity': 'Original 29-row log and inconsistent 30-row summary preserved; complete 30/13/17 scope/failure counts attributed only to the separately declared unchanged retry.',
    'preserve_boundaries': [
        'No total compiler or unrestricted completeness claim over inherited rational inputs.',
        'Parity lower bound is for the exact fresh inherited tree rules; shared ordinary DAG evidence is allowed.',
        'Polynomial complete route is parity-specific, cap-relaxed, and conditional on explicit written-size/arithmetic/map/text/source assumptions.',
        'No physical CPU/heap theorem, free source deployment, uncharged incumbent acquisition or optimal budget policy.',
        'No new probability recovery, calibration, adaptive-policy regret, self-reflection or genuine counterpossible theorem.',
        'No original missing rational row reconstructed from its summary, packets or successful retry.',
        'Post-primary pricing, pruning, rational and actual-cap diagnostics remain separately labeled DEVELOPMENT.',
    ],
    'later_work': {'P3-09': 'unstarted', 'Option C': 'unselected', 'R-P3-N01': 'unselected',
                   'P3-C': 'unattempted', 'P3-D': 'unattempted'},
    'final_challenge_frozen': False, 'final_evaluation_exposed': False,
    'stop_boundary': 'R-P3-B-B only; this draft selects no next task and closes no research floor.',
}
write_json(HERE / 'draft_21_desiderata_overlay.v1.json', overlay)

lines = [
    '# Draft Option B overlay for all 21 desiderata', '',
    'Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 10, 2026 UTC.', '',
    '**DRAFT ONLY — same-model, nonblind DEVELOPMENT review.** This additive',
    'assessment does not edit a checkpoint, close task scope or a research floor,',
    'post time, select another recurrence, freeze a challenge, or expose P3-09.',
    'No worker or proof checker was executed; principal research credit is zero.', '',
    'The [machine-readable draft](draft_21_desiderata_overlay.v1.json) retains',
    'every exact prior status and scope from the latest P3-08 overlay, alongside',
    'the proposed delta and source hashes. A retained duty keeps its prior status.',
    'An extension remains restricted to the named receiving service. The',
    '[review](review.md) gives the scientific disposition and remaining limits.', '',
    '## Scientific disposition', '',
    overlay['scientific_disposition'], '', overlay['contribution'], '', overlay['Q3'], '',
    overlay['U04'], '',
    '## Duty-by-duty proposed overlay', '',
    '| Duty | Disposition | Added support | Retained limitations and open obligations |',
    '|---|---|---|---|',
]
for d in duties:
    lines.append('| **' + d['id'] + ' — ' + d['title'] + '** | ' + d['disposition'].replace('_', ' ') +
                 ' | ' + d['new_support'] + ' | ' + d['limitations_and_open_obligations'] + ' |')
lines += ['', '## Evidence and completion boundary', '',
          'Every duty has exact evidence paths and hashes in the JSON draft. The',
          '[source capture](source_capture.json) binds the inspected current prose,',
          'prior overlay and saved evidence. Captured copies remain as read even if',
          'their owner later revises the canonical documents. The independent',
          '[record reconstruction](record_reconstruction.json) checks the primary',
          'and actual-cap conclusions from saved invoices without rerunning a policy.', '',
          overlay['completion_status'], '', overlay['stop_boundary'], '']
with (HERE / 'draft_21_desiderata_overlay.md').open('x') as handle:
    handle.write('\n'.join(lines))
write_json(HERE / 'source_capture.json', {
    'schema': 'value_logic.R-P3-B-B.final-assessment-capture.v1',
    'stage': 'DEVELOPMENT', 'principal_clock_credit': 0,
    'evidence_keys': {key: {'path': relative, **INPUTS[relative]} for key, relative in EVIDENCE.items()},
    'all_inspected_inputs': INPUTS,
    'captured_paths': sorted(str(p.relative_to(CAPTURE)) for p in CAPTURE.rglob('*') if p.is_file()),
    'record_reconstruction': {'path': 'record_reconstruction.json', 'sha256': sha((HERE / 'record_reconstruction.json').read_bytes())},
})
print(json.dumps({'status': observation['status'], 'observational_checks': len(CHECKS),
                  'failures': failed, 'duties': len(duties),
                  'captured_paths': len(list(CAPTURE.rglob('*'))),
                  'cap_deliveries': sum(a['delivered'] for a in cap_aggregates.values()),
                  'cap_unique_discrepancies': len(discrepancies)}, sort_keys=True))
