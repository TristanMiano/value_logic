"""Independent corner-based review of saved F15 rectangular-regret analysis.

Contributor: delegated ChatGPT (GPT-6 Astra Pro), F15 saved-data review.
No project imports, population generation, or experimental-stage execution.
"""
from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

SESSION = Path(__file__).resolve().parent
ROOT = SESSION.parents[2]
inputs = {}


def checked(path):
    raw = path.read_bytes()
    digest = sha256(raw).hexdigest()
    assert digest == Path(str(path)+'.sha256').read_text().strip()
    inputs[str(path.relative_to(ROOT))] = digest
    return json.loads(raw)


@lru_cache(maxsize=None)
def corner_regrets(intervals):
    # Deterministic algebra on the saved interval box, not a source-law or
    # experimental-population generator. For each box corner compute actual
    # action cost minus the cheapest action in that same corner. Self regret
    # is therefore exactly zero without a separate b!=a formula.
    maximum = [Q(0)]*len(intervals)
    axes = tuple((lo,) if lo == hi else (lo,hi) for lo,hi in intervals)
    for costs in product(*axes):
        best = min(costs)
        for a, cost in enumerate(costs):
            maximum[a] = max(maximum[a],cost-best)
    return tuple(maximum)


analysis_path = SESSION/'decision_information_analysis.json'
analysis = checked(analysis_path)
config_path = ROOT/'v2/experiments/config.v1.json'
raw_config = config_path.read_bytes()
inputs[str(config_path.relative_to(ROOT))] = sha256(raw_config).hexdigest()
config = json.loads(raw_config)['retention']
fallback, epsilon = Q(config['fallback_cost']),Q(config['decision_regret_tolerance'])
saved = {(r['seed'],r['variant'],r['access'],r['method']):r for r in analysis['rows']}
assert len(saved) == len(analysis['rows']) == 1920
count = Counter()
by_method = Counter()
useful_episodes = set()
all_gap_episodes = set()
first_program = None
for seed in config['evaluation_seeds']:
    for variant in config['variants']:
        case = checked(ROOT/f'v2/work_logs/F15_v1_run1/evaluation_attempt_1/retention_{seed}_{variant}.json')
        for row in case['methods']:
            key = (seed,variant,row['access'],row['method'])
            observed = saved[key]
            intervals = tuple((Q(n['lower']),Q(n['upper'])) for n in row['numeric'])+((fallback,fallback),)
            rect = corner_regrets(intervals)
            selected, executed = row['selected_index'],row['executed_index']
            coherent = Q(row['coherent_worst_regret'])
            certified = not row['refused']
            assert tuple(map(Q,observed['rectangular_regrets_by_action'])) == rect
            assert tuple(tuple(map(Q,p)) for p in observed['numeric_intervals']) == intervals
            assert Q(observed['selected_rectangular_regret']) == rect[selected]
            assert Q(observed['best_rectangular_regret']) == min(rect)
            assert Q(observed['selected_coherent_regret']) == coherent
            assert (observed['selected_index'],observed['executed_index']) == (selected,executed)
            assert Q(0) <= coherent <= rect[selected]
            assert certified == (coherent <= epsilon) == observed['decision_certified']
            assert observed['selected_rectangular_certifiable'] == (rect[selected] <= epsilon)
            assert observed['any_rectangular_action_certifiable'] == (min(rect) <= epsilon)
            assert observed['actual_executed_regret'] == row['scoring']['realized_regret']
            assert observed['useful_native'] == row['native']['useful_derivation_candidate']
            admitted = sum(n['status'] != 'refused' for n in row['numeric'])
            assert observed['admitted_numeric_count'] == admitted
            count['rows_checked'] += 1
            count['action_regrets_checked'] += len(rect)
            count['refused_rows_with_selected_not_executed'] += (not certified and selected != executed)
            if certified:
                assert selected == executed
                count['certified_with_some_numeric_refused'] += admitted < 6
                count['certified_with_all_six_numeric_refused'] += admitted == 0
                count['certified_order_selected_cost_refused'] += (row['decision_status']=='certified_order' and row['numeric'][selected]['status']=='refused')
            if certified and min(rect) > epsilon:
                count['certified_without_rectangle_certifiable_action'] += 1
                by_method[(row['access'],row['method'])] += 1
                all_gap_episodes.add((seed,variant))
            if row['native']['useful_derivation_candidate'] and min(rect) > epsilon:
                count['useful_without_rectangle_certifiable_action'] += 1
                useful_episodes.add((seed,variant))
                if first_program is None and variant=='program_edit' and row['method']=='tailored' and row['access']=='no_reacquisition' and admitted==0:
                    first_program = dict(seed=seed,variant=variant,selected_index=selected,
                        coherent_regret=str(coherent),best_rectangular_regret=str(min(rect)))
assert count['rows_checked']==1920 and count['action_regrets_checked']==13440
assert count['certified_without_rectangle_certifiable_action']==22
assert by_method==Counter({('no_reacquisition','tailored'):11,('no_reacquisition','exact_intervals'):11})
assert count['useful_without_rectangle_certifiable_action']==16 and len(useful_episodes)==8
assert count['certified_with_some_numeric_refused']==80
assert count['certified_with_all_six_numeric_refused']==32
assert count['certified_order_selected_cost_refused']==24
assert first_program==dict(seed=15105,variant='program_edit',selected_index=5,
    coherent_regret='0',best_rectangular_regret='155/231')
for name, value in {
    'certified_decision_but_no_rectangular_action_certifiable':22,
    'useful_native_but_no_rectangular_action_certifiable':16,
    'decision_certified_with_some_numeric_refused':80,
    'decision_certified_with_all_six_numeric_refused':32,
    'certified_order_selected_numeric_refused':24,
}.items():
    assert analysis['summary'][name]==value
assert analysis['useful_no_rectangular_action_distinct_episodes']==8
result = dict(contributor='delegated ChatGPT (GPT-6 Astra Pro), F15 saved-data review',
    passed=True,counts=dict(count),
    no_rectangle_certified_by_method=[dict(access=a,method=m,rows=n) for (a,m),n in sorted(by_method.items())],
    useful_distinct_episodes=len(useful_episodes),all_certified_gap_distinct_episodes=len(all_gap_episodes),
    first_program_example=first_program,
    independent_method='Enumerate deterministic corners of each saved marginal-cost rectangle; maximize cost[a]-min(costs) at common corners, including exact fallback.',
    unique_interval_boxes_checked=corner_regrets.cache_info().currsize,
    input_sha256=inputs,script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
    new_population_generation=False,original_outputs_modified=False,
    new_registered_control=False,new_novelty_claim=False,credited_E_minutes=0)
with (SESSION/'decision_information_review.json').open('x') as handle:
    json.dump(result,handle,indent=2,sort_keys=True)
    handle.write('\n')
print(json.dumps({k:v for k,v in result.items() if k!='input_sha256'},indent=2))
