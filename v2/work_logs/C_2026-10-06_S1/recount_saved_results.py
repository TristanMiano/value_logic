"""Read-only Gate C recount of saved evidence; no experiment imports or execution.

Contributor: ChatGPT (GPT-6 Astra Pro). This audits aggregation and chronology,
not the latent ground truth, training, every proof node, or statistical coverage.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import resource
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
RUN = REPO / 'v2/work_logs/F15_v1_run1'
OUT = ROOT / 'saved_results_attempt1'
INPUTS = {}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    data = path.read_bytes()
    INPUTS[path.relative_to(REPO).as_posix()] = {'sha256': sha(data), 'bytes': len(data)}
    return json.loads(data)


def main():
    OUT.mkdir(exist_ok=False)
    started = datetime.now(timezone.utc).isoformat()
    t0, c0 = time.monotonic_ns(), time.process_time_ns()
    (OUT / 'reader.py').write_bytes(Path(__file__).read_bytes())
    (OUT / 'start.json').write_text(json.dumps({'started_utc': started,
        'command': [sys.executable, str(Path(__file__).relative_to(REPO))],
        'python': sys.version, 'source_sha256': sha(Path(__file__).read_bytes())}, indent=2)+'\n')
    try:
        config = read(REPO / 'v2/experiments/config.v1.json')['retention']
        cases = read(REPO / 'v2/work_logs/F15_2026-10-04_S1/retention_results_recovered.json')
        assessment = read(RUN / 'evaluation_attempt_1/retention_assessment.json')
        neural = read(RUN / 'evaluation_attempt_1/neural_assessment.json')
        prep = read(RUN / 'preparation_complete.json')
        validation = read(REPO / 'v2/work_logs/F15_2026-10-04_S1/pre_evaluation_validation.json')
        exposure = read(RUN / 'evaluation_start.json')
        completion = read(RUN / 'evaluation_complete.json')
        assert len(prep['models']) == len(validation['models']) == 5
        assert [m['index'] for m in prep['models']] == list(range(5))
        assert validation['all_five_validated'] and validation['evaluation_marker_absent']
        assert not validation['final_retention_or_neural_population_generated']
        assert not prep['evaluation_started']
        for model, checked in zip(prep['models'], validation['models']):
            path = RUN / model['file']
            artifact = read(path)
            assert sha(path.read_bytes()) == model['sha256'] == checked['sha256']
            assert model['alignment_artifact_hash'] == checked['alignment_artifact_hash'] == artifact['artifact_hash']
            assert checked['index'] == model['index']
            assert checked['configuration_and_budget_valid'] and checked['internal_and_external_hashes_valid']
            assert not checked['evaluation_generated'] and not artifact['evaluation_generated']
        prep_hash = sha((RUN / 'preparation_complete.json').read_bytes())
        assert prep_hash == validation['preparation_manifest_sha256'] == exposure['preparation_manifest_sha256']
        chronology = [prep['completed_utc'], validation['validated_utc'], exposure['started_utc'], completion['completed_utc']]
        assert all(datetime.fromisoformat(a) < datetime.fromisoformat(b) for a,b in zip(chronology, chronology[1:]))
        expected = [(s, v) for s in config['evaluation_seeds'] for v in config['variants']]
        assert [(c['seed'], c['variant']) for c in cases] == expected
        tau, epsilon = Q(config['numeric_tolerance']), Q(config['decision_regret_tolerance'])
        assert tau == epsilon == Q(1, 20)
        qualifying, selective = [], []
        numeric, decisions, native = Counter(), Counter(), Counter()
        method_order = [(a,m) for a in config['access_regimes'] for m in config['methods']]
        direct_edits = {'small_price', 'small_negative_price', 'large_price', 'large_negative_price', 'program_edit'}
        for c in cases:
            unit = RUN / f"evaluation_attempt_1/retention_{c['seed']}_{c['variant']}.json"
            assert read(unit) == c, f'Unit/aggregate mismatch: {unit}'
            assert [(m['access'],m['method']) for m in c['methods']] == method_order
            for m in c['methods']:
                n = m['native']
                numeric.update(a['status'] for a in m['numeric'])
                decisions[m['decision_status']] += 1
                native[n['status']] += 1
                useful = (c['variant'] in direct_edits and m['decision_status'] == 'certified_order'
                    and not m['refused'] and m['executed'] is not None
                    and m['selected'] == m['executed'] == n['candidate_order']
                    and n['certificate_role'] == 'selected_order' and n['status'] == 'received'
                    and n['semantic_valid'] and Q(n['upper_bound']) <= -tau
                    and n['source_premises_used'] >= 2 and Q(m['coherent_worst_regret']) <= epsilon)
                assert useful == n['useful_derivation_candidate']
                if useful:
                    key = {k:c[k] for k in ['seed','variant']}
                    key.update({k:m[k] for k in ['method','access']})
                    qualifying.append(key)
                    if (m['method'] in {'tailored','exact_intervals'} and m['access'] == 'no_reacquisition'
                            and m['resources']['fiber_vertex_count'] > 1
                            and m['numeric'][m['executed_index']]['status'] == 'approximate'):
                        selective.append(key)
        distinct = sorted({(x['seed'],x['variant']) for x in qualifying})
        distinct_selective = sorted({(x['seed'],x['variant']) for x in selective})
        assert len(distinct) == assessment['useful_distinct_cases']
        assert len({s for s,v in distinct}) == assessment['useful_distinct_seeds']
        assert selective == assessment['uncertain_approximate_selective_useful_cases']
        assert dict(numeric) == assessment['numeric_dispositions']
        assert dict(decisions) == assessment['decision_dispositions']
        assert dict(native) == assessment['native_dispositions']
        criterion = (len(distinct) >= 4 and len({s for s,v in distinct}) >= 2
            and any(v == 'program_edit' for s,v in distinct)
            and any(v != 'program_edit' for s,v in distinct) and bool(selective))
        assert criterion == assessment['bounded_application_criterion_met'] == completion['retention_bounded_application_criterion_met']
        control_rows = assessment['equal_information_control_comparisons']
        assert len(control_rows) == len(cases)*len(config['access_regimes'])*3
        assert all(all(r[k] for k in ['ordinary_quality_and_acquisition_equal', 'native_semantic_target_equal',
                                    'native_receipt_status_equal']) for r in control_rows)
        complete = sum(m['disposition'] == 'expected_cost_interchange_supported_at_declared_scope' for m in neural['models'])
        assert complete == neural['supported_prespecified_replicates']
        result = {'status':'pass', 'scope':'Saved-record aggregation and chronology; no scientific rerun.',
            'cases':len(cases), 'method_rows':sum(decisions.values()), 'scalar_rows':sum(numeric.values()),
            'useful_method_rows':len(qualifying), 'useful_distinct_episodes':len(distinct),
            'useful_distinct_seeds':len({s for s,v in distinct}),
            'useful_episodes_by_variant':dict(sorted(Counter(v for s,v in distinct).items())),
            'useful_episode_keys':distinct, 'selective_approximate_rows':len(selective),
            'selective_approximate_distinct_episodes':len(distinct_selective),
            'selective_approximate_distinct_seeds':len({s for s,v in distinct_selective}),
            'selective_approximate_episode_keys':distinct_selective, 'prospective_usefulness_met':criterion,
            'numeric_dispositions':dict(numeric), 'decision_dispositions':dict(decisions),
            'native_dispositions':dict(native), 'saved_equal_information_comparisons_all_agree':len(control_rows),
            'control_scope':'Recount of saved exact-comparison records, not an independent solver execution.',
            'neural_models':len(neural['models']), 'neural_task_ready':sum(m['task_ready'] for m in neural['models']),
            'neural_complete_support':complete, 'preparation_chronology_utc':chronology,
            'all_five_prepared_hashed_validated_before_exposure':True,
            'all_160_units_equal_recovered_aggregate':True,
            'frozen_outcomes_changed':False, 'new_populations_or_models':0}
        result.update({'started_utc':started,'completed_utc':datetime.now(timezone.utc).isoformat(),
            'wall_ns':time.monotonic_ns()-t0, 'process_cpu_ns':time.process_time_ns()-c0,
            'maximum_process_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
        (OUT / 'summary.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
        print(json.dumps({k:result[k] for k in ['status','useful_distinct_episodes','selective_approximate_distinct_episodes','neural_complete_support','wall_ns']}))
    except BaseException:
        (OUT / 'failure.txt').write_text(traceback.format_exc())
        raise
    finally:
        (OUT / 'input_manifest.json').write_text(json.dumps(INPUTS,indent=2,sort_keys=True)+'\n')


if __name__ == '__main__':
    main()
