"""Read-only numerical review of F15 report retention tables.

Contributor: delegated ChatGPT (GPT-6 Astra Pro), F15 retention report review.
No experiment imports, generation, training, or writes to source run/report.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[3]
SESSION = Path(__file__).resolve().parent
REPORT = ROOT/'v2/experiments/results.md'
SOURCE = ROOT/'v2/work_logs/F15_v1_run1/evaluation_attempt_1'
text = REPORT.read_text()
config = json.loads((ROOT/'v2/experiments/config.v1.json').read_text())['retention']
cases = []
hashes = {}
for seed in config['evaluation_seeds']:
    for variant in config['variants']:
        p = SOURCE/f'retention_{seed}_{variant}.json'
        raw = p.read_bytes()
        digest = sha256(raw).hexdigest()
        assert digest == Path(str(p)+'.sha256').read_text().strip()
        hashes[p.name] = digest
        cases.append(json.loads(raw))
groups = defaultdict(list)
for case in cases:
    for row in case['methods']:
        groups[row['access'], row['method']].append(row)
checks = Counter()
errors = []


def check(category, name, observed, expected):
    checks[category] += 1
    if observed != expected:
        errors.append(dict(category=category, name=name, observed=observed, expected=expected))


def rounded(category, name, report_number, exact_value):
    check(category, name, abs(Q(report_number.replace(',', ''))-exact_value) <= Q(1, 2_000_000), True)


def mean(values):
    values = list(values)
    return sum(map(Q, values), Q(0))/len(values)


def part(start, end):
    return text.split(start, 1)[1].split(end, 1)[0]


def tables(section):
    groups, current = [], []
    for line in section.splitlines()+['']:
        if line.startswith('|'):
            current.append([x.strip() for x in line.strip('|').split('|')])
        elif current:
            groups.append(current[2:])
            current = []
    return groups


def access(label):
    return 'no_reacquisition' if label.startswith('No reacquisition') else 'adaptive_reacquisition'


def integers(cell):
    return tuple(int(x.strip()) for x in cell.replace(',', '').split('/'))


for a, method, numeric, decisions, receipts, regret, useful in tables(part('### 3.2 ', '### 3.3 '))[0]:
    rows = groups[access(a), method]
    n = Counter(x['status'] for r in rows for x in r['numeric'])
    d = Counter(r['decision_status'] for r in rows)
    check('outcome_table', a+'/'+method+'/numeric', integers(numeric), tuple(n[k] for k in ('exact','approximate','refused')))
    check('outcome_table', a+'/'+method+'/decisions', integers(decisions), tuple(d[k] for k in ('certified_order','certified_fallback','refusal_to_fallback')))
    check('outcome_table', a+'/'+method+'/receipts', int(receipts), sum(r['native']['status'] == 'received' for r in rows))
    check('outcome_table', a+'/'+method+'/useful', int(useful), sum(r['native']['useful_derivation_candidate'] for r in rows))
    rounded('outcome_table', a+'/'+method+'/regret', regret, mean(r['scoring']['realized_regret'] for r in rows))

variant_names = dict(zip(('Small positive price edit','Small negative price edit','Large positive price edit','Large negative price edit','Program edit'),
                         ('small_price','small_negative_price','large_price','large_negative_price','program_edit')))
for label, count in tables(part('### 3.3 ', '### 3.4 '))[0]:
    observed = sum(c['variant'] == variant_names[label] and any(r['native']['useful_derivation_candidate'] for r in c['methods']) for c in cases)
    check('useful_episode_table', label, int(count), observed)

for method, resident, context, proof, total in tables(part('### 4.1 ', '### 4.2 '))[0]:
    no = groups['no_reacquisition', method]
    yes = groups['adaptive_reacquisition', method]
    for name, cell in [('resident_bytes',resident),('current_source_context_bytes',context),('current_proof_bytes',proof)]:
        check('storage_table', method+'/'+name, Q(cell.replace(',','')), Q(statistics.median(r['resources'][name] for r in no)))
    totals = [Q(x.strip().replace(',','')) for x in total.split('/')]
    check('storage_table', method+'/total_stored', totals,
          [Q(statistics.median(r['resources']['total_stored_serialized_upper_bytes'] for r in rows)) for rows in (no,yes)])

for a, method, initial, arithmetic, native in tables(part('### 4.2 ', '### 4.3 '))[0]:
    rows = groups[access(a),method]
    for name, cell in [('initial_total_ns',initial),('one_update_arithmetic_ns',arithmetic),('one_update_total_ns',native)]:
        rounded('time_table', a+'/'+method+'/'+name, cell, mean(r['resources'][name] for r in rows)/1_000_000)

acq_tables = tables(part('### 4.3 ', '### 4.4 '))
family_names = {
    'fresh / cached_proof / full_joint': ('fresh','cached_proof','full_joint'),
    'tailored / exact_intervals': ('tailored','exact_intervals'),
    'marginal_diagnostic': ('marginal_diagnostic',),
}
for family, counts, decision in acq_tables[0]:
    for method in family_names[family]:
        rows = groups['adaptive_reacquisition',method]
        histogram = Counter(r['resources']['acquisition_scalar_measurements'] for r in rows)
        check('acquisition_table',method+'/histogram', integers(counts), tuple(histogram[i] for i in (0,2,8)))
        rounded('acquisition_table',method+'/decision_cost',decision,mean(r['scoring']['actual_executed_cost'] for r in rows))
for family, free, low, high in acq_tables[1]:
    a = access(family)
    methods = ('fresh','cached_proof','full_joint') if 'full-information' in family else \
              ('tailored','exact_intervals') if 'tailored' in family else ('marginal_diagnostic',)
    for method in methods:
        rows = groups[a,method]
        for fee, cell in zip(('0','1/20','1/2'),(free,low,high)):
            # Compute total independently from current decision + actual scalar
            # acquisition + eight common initial fields + current common facts.
            expected = mean(Q(r['scoring']['actual_executed_cost'])+Q(fee)*(
                8+r['resources']['current_common_scalar_inputs']+
                r['resources']['acquisition_scalar_measurements']) for r in rows)
            rounded('all_source_charge_table',a+'/'+method+'/'+fee,cell,expected)


def successful(row):
    return all(n['status'] != 'refused' for n in row['numeric']) and \
        row['decision_status'] == 'certified_order' and \
        row['native']['certificate_role'] == 'selected_order' and row['native']['status'] == 'received'


def quality(row):
    n, s = row['native'],row['scoring']
    return {'numeric': row['numeric'], 'errors':s['numeric_errors'],
        'decision':{k:row[k] for k in ('decision_status','refused','selected_index','executed_index','coherent_worst_regret')},
        'scores':{k:s[k] for k in ('realized_regret','actual_executed_cost','full_information_oracle_best_cost','full_source_semantic_value','full_source_semantic_valid')},
        'native':{k:n[k] for k in ('status','certificate_role','candidate_order','semantic_valid','upper_bound')}}


horizon_rows=[]
for a, method, eligible, wins in tables(part('### 4.4 ', '## 5.'))[0]:
    pairs = []
    crossings = 0
    for case in cases:
        row = next(r for r in case['methods'] if (r['access'],r['method']) == (access(a),method))
        fresh = next(r for r in case['methods'] if (r['access'],r['method']) == (access(a),'fresh'))
        initial_diff=row['resources']['initial_total_ns']-fresh['resources']['initial_total_ns']
        saving=fresh['resources']['one_update_total_ns']-row['resources']['one_update_total_ns']
        crossings += saving > 0 or (saving == 0 and initial_diff < 0)
        if quality(row) == quality(fresh) and successful(row) and successful(fresh):
            pairs.append((row,fresh))
    check('horizon_table',a+'/'+method+'/eligible',int(eligible),len(pairs))
    actual = tuple(sum(r['resources']['initial_total_ns']+h*r['resources']['one_update_total_ns'] <
                       f['resources']['initial_total_ns']+h*f['resources']['one_update_total_ns'] for r,f in pairs)
                   for h in config['horizons'])
    check('horizon_table',a+'/'+method+'/wins',integers(wins),actual)
    horizon_rows.append(dict(access=access(a),method=method,eligible=len(pairs),wins=actual,eventual_crossings_all= crossings))

flat = [r for c in cases for r in c['methods']]
supporting = {
    'receipts':sum(r['native']['status']=='received' for r in flat),
    'selected_order_receipts':sum(r['native']['status']=='received' and r['native']['certificate_role']=='selected_order' for r in flat),
    'diagnostic_receipts':sum(r['native']['status']=='received' and r['native']['certificate_role']=='diagnostic_option_only' for r in flat),
    'certified_order_without_receipt':sum(r['decision_status']=='certified_order' and r['native']['status']!='received' for r in flat),
    'approximate_selected_with_certified_order':sum(r['decision_status']=='certified_order' and r['numeric'][r['executed_index']]['status']=='approximate' for r in flat),
    'true_full_law_comparison_not_retained_fiber_valid':sum(r['scoring']['full_source_semantic_valid'] and not r['native']['semantic_valid'] for r in flat),
    'regret_above_1_20':sum(Q(r['scoring']['realized_regret'])>Q(1,20) for r in flat),
    'all_above_tolerance_are_refused':all(r['refused'] for r in flat if Q(r['scoring']['realized_regret'])>Q(1,20)),
    'initial_common_production_seconds':sum(c['common_input_accounting']['observed_common_production_ns'] for c in cases)/1e9,
    'method_stage_seconds':sum(r['resources']['initial_total_ns']+r['resources']['one_update_total_ns'] for r in flat)/1e9,
    'median_tailored_saving_vs_intervals':statistics.median(b['resources']['resident_bytes']-a['resources']['resident_bytes'] for a,b in zip(groups['no_reacquisition','tailored'],groups['no_reacquisition','exact_intervals'])),
    'median_tailored_saving_vs_fresh':statistics.median(b['resources']['resident_bytes']-a['resources']['resident_bytes'] for a,b in zip(groups['no_reacquisition','tailored'],groups['no_reacquisition','fresh'])),
}
paired_time=[]
paired_economics=[]
for a in config['access_regimes']:
    for method, baseline in (('cached_proof','fresh'),('tailored','exact_intervals'),('full_joint','fresh')):
        pairs=[(r,b) for r,b in zip(groups[a,method],groups[a,baseline]) if successful(r) and successful(b)]
        delta=[r['resources']['one_case_method_plus_common_ns']-b['resources']['one_case_method_plus_common_ns'] for r,b in pairs]
        paired_time.append(dict(access=a,method=method,baseline=baseline,eligible=len(pairs),strict_wins=sum(v<0 for v in delta),mean_complete_case_difference_ms=float(mean(delta)/1_000_000),mean_arithmetic_difference_ms=float(mean(r['resources']['one_update_arithmetic_ns']-b['resources']['one_update_arithmetic_ns'] for r,b in pairs)/1_000_000)))
for method in config['methods']:
    pairs=[(a,b) for a,b in zip(groups['no_reacquisition',method],groups['adaptive_reacquisition',method]) if b['resources']['acquisition_scalar_measurements']]
    benefit=[Q(a['scoring']['actual_executed_cost'])-Q(b['scoring']['actual_executed_cost']) for a,b in pairs]
    paired_economics.append(dict(method=method,acquiring=len(pairs),zero_benefit=sum(v==0 for v in benefit),already_certified=sum(not a['refused'] for a,b in pairs),net_wins={fee:sum(v>Q(fee)*b['resources']['acquisition_scalar_measurements'] for v,(_,b) in zip(benefit,pairs)) for fee in config['acquisition_costs']}))
result = dict(contributor='delegated ChatGPT (GPT-6 Astra Pro), F15 retention report review',
    report_sha256=sha256(text.encode()).hexdigest(),
    section_3_4_sha256=sha256(text.split('## 3.',1)[1].split('## 5.',1)[0].encode()).hexdigest(),
    passed=not errors,checks=dict(checks),errors=errors,
    supporting_counts=supporting,horizon_reconstruction=horizon_rows,
    paired_time_reconstruction=paired_time,paired_acquisition_reconstruction=paired_economics,
    source_case_sha256=hashes,new_generation=False,original_outputs_modified=False)
with (SESSION/'results_retention_review.json').open('x') as handle:
    json.dump(result,handle,indent=2,sort_keys=True,default=str)
    handle.write('\n')
print(json.dumps({k:v for k,v in result.items() if k != 'source_case_sha256'},indent=2,default=str))
raise SystemExit(0 if result['passed'] else 1)
