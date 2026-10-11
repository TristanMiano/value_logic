#!/usr/bin/env python3
"""Additive JSON-only reference/live correction detail; no new truth or rerun."""
from pathlib import Path
from fractions import Fraction as F
from datetime import datetime, timezone
import hashlib
import json
import traceback

ROOT = Path('/workspace/scratch/095cdac579b7/value_logic')
WORK = ROOT/'v3/work_logs/P3_10_2026-10-11_S1'
HERE = Path(__file__).resolve().parent
OUT = HERE/'reference_correction_details_v1'
OUT.mkdir(exist_ok=False)
READS = {}
START = datetime.now(timezone.utc).isoformat()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def enc(x):
    if isinstance(x, F):
        return [x.numerator, x.denominator]
    if isinstance(x, dict):
        return {str(k): enc(v) for k,v in x.items()}
    if isinstance(x, (list, tuple)):
        return [enc(v) for v in x]
    return x


def save(p, x):
    with p.open('x') as f:
        if isinstance(x, str):
            f.write(x)
        else:
            json.dump(enc(x), f, indent=2, sort_keys=True, allow_nan=False)
            f.write('\n')


def read(p, expected=None):
    b = p.read_bytes()
    meta = {'path': str(p.relative_to(ROOT)), 'sha256': sha(b), 'bytes': len(b)}
    if expected is not None:
        assert expected == meta['sha256']
    READS[meta['path']] = meta
    return json.loads(b)


try:
    index = read(WORK/'reviews/certificate_reconstruction/final_observation_v4/source_hashes.json',
                 '58b51d1f1379ddf41ed34f8949fdc315de524aa5e61a3f38fe5d2aba7e0c75fb')
    hashes = {x['path']: x['sha256'] for x in index['consumed_files']}
    summary = read(HERE/'summary.json', 'b493e80a82abc27ed149f2dba835c84a25439b56b3737186211cd9b8f3881b47')
    details = []
    for expected in summary['reference_center_exceptions']:
        uid = expected['unit_id']
        p = ROOT/'v3/experiments/final_v1/stages/public/units'/uid/'attempt_01/result.json'
        raw = read(p, hashes[str(p.relative_to(ROOT))])
        paid = raw['value']['paid_result']
        episode, report = paid['episode'], paid['optional_reporting']['report']
        known, changes = {}, []
        for row in episode['trace']:
            key = json.dumps(row['claim_key'], separators=(',', ':'), sort_keys=True)
            prior = known.get(key)
            if row['hard_before'] == 'checked' and prior and prior['block'] == row['block']:
                base, issued = F(*row['base_q']), F(*row['emitted_q'])
                y = prior['answer']
                assert issued == y and row['selected'] is False
                changes.append({'index': row['index'], 'block': row['block'],
                    'receipt_index': prior['index'], 'receipt_query_id': prior['query_id'],
                    'query_id': row['query_id'], 'claim_key': row['claim_key'],
                    'base_q': base, 'issued_q': issued, 'paid_answer': y,
                    'reference_delta_F': (base-y)**2,
                    'reference_delta_V': base+(1-2*base)*y,
                    'source_of_label': 'Earlier selected checked receipt in this same block'})
            if row['selected'] and key not in known:
                known[key] = {'answer': row['purchased_label'], 'block': row['block'],
                              'index': row['index'], 'query_id': row['query_id']}
        delta_f, delta_v = (F(*report['reference_corrections'][name]) for name in ('F','V'))
        assert delta_f == sum((x['reference_delta_F'] for x in changes), F(0))
        assert delta_v == sum((x['reference_delta_V'] for x in changes), F(0))
        shift, ref_shift = F(*expected['C']), F(*expected['reference_center_shift'])
        assert ref_shift == shift + delta_f-delta_v
        assert len(changes) == 1 and changes[0]['index'] == 15 and changes[0]['block'] == 3
        details.append({'unit_id': uid, 'source_result': READS[str(p.relative_to(ROOT))],
            'reference_delta_F': delta_f, 'reference_delta_V': delta_v,
            'reference_delta_F_minus_V': delta_f-delta_v,
            'saved_reference_correction_encoding': report['reference_corrections'],
            'saved_full_live_correction_encoding': report['corrections'],
            'public_C': shift, 'reference_center_F_minus_V': ref_shift,
            'within_block_changes': changes})
    assert len(details) == 6
    result = {'status': 'PASS', 'reviewer': 'ChatGPT (GPT-6 Astra Pro), /root/certificate_reconstruction',
        'start': START, 'signed_utc': datetime.now(timezone.utc).isoformat(),
        'source_sha256': sha(Path(__file__).read_bytes()), 'records': details,
        'reports': 6, 'distinct_seed_paths': 2, 'within_block_changed_positions_per_report': 1,
        'identity': 'reference_center_F - reference_center_V = C + reference_delta_F - reference_delta_V',
        'new_truth_generation': False, 'official_or_observer_rerun': False, 'principal_research_credit_seconds': 0}
    save(OUT/'results.json', result)
    table = '\n'.join(f"| `{x['unit_id']}` | {x['reference_delta_F']} | {x['reference_delta_V']} | {x['reference_delta_F_minus_V']} |" for x in details)
    receipt_indices = sorted({z['receipt_index'] for x in details for z in x['within_block_changes']})
    body = f'''# Addendum: exact snapshot-to-live reference corrections

Signed: **ChatGPT (GPT-6 Astra Pro), `/root/certificate_reconstruction`**  
UTC: {result['signed_utc']}  
Disposition: **PASS, all six reference-center exceptions explained exactly.**

This additive detail accompanies the signed geometry review SHA-256
`76841babb5faa4851f9ca0cab7375d15b6b554da52af365a600fd1678b6f525b`.
It preserves the existing review, observer and results. Delta F and Delta V
below are specifically the reporter's **reference corrections** from its
predictable block-start snapshot to the live issued path. They are not the
larger full base-to-live correction totals, whose raw encodings are separately
retained in the accompanying JSON.

| Unit ID | Reference Delta F | Reference Delta V | Delta F minus Delta V |
|---|---:|---:|---:|
{table}

Every row has exactly one within-block change: zero-based position **15** in
block **3**, after a matching selected receipt at position(s) **{', '.join(map(str, receipt_indices))}**.
The changed position is unselected. The receipt says y=1, and the live issued
forecast is exactly 1. The block-start snapshot did not yet possess this
receipt, so its reference forecast still uses the base dyadic. For seed
3091002 that base is `53118/65536`; for seed 3091003 it is `54613/65536`.
Consequently `Delta F=(1-base)^2` and `Delta V=1-base` at this position.

The corresponding reference-center difference is exactly
`C + Delta F - Delta V`; the corrected live centers and both delivered
interval endpoints still differ by C. These are two coupled seed-path cases
represented in three configurations each, not six independent mechanisms.
Full claim keys, paid receipt/query identities, the original unreduced
encodings, reduced exact fractions and input hashes remain in `results.json`
and `source_hashes.json`.

This is read-only JSON arithmetic using already paid labels. No new truth,
paid method, principal observer, scorer or analysis was executed. Principal
research-clock credit is zero.
'''
    save(OUT/'review.md', body)
    save(OUT/'source_hashes.json', {'consumed_files': list(READS.values())})
    save(OUT/'signature.json', {'reviewer': result['reviewer'], 'signed_utc': result['signed_utc'],
        'source_sha256': result['source_sha256'],
        'outputs': {p.name: sha(p.read_bytes()) for p in sorted(OUT.iterdir()) if p.is_file()},
        'principal_research_credit_seconds': 0})
    print(json.dumps({'status': 'PASS', 'reports': 6, 'receipt_indices': receipt_indices,
                      'results_sha256': sha((OUT/'results.json').read_bytes()),
                      'review_sha256': sha((OUT/'review.md').read_bytes())}))
except BaseException as error:
    save(OUT/'observer_failure.json', {'status': 'OBSERVER_FAILURE', 'start': START,
        'error_type': type(error).__name__, 'error': str(error), 'traceback': traceback.format_exc(),
        'consumed_files': list(READS.values()), 'scientific_stage_failure': False,
        'principal_research_credit_seconds': 0})
    raise
