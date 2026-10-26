"""Frozen initial development probe described in retention_probe.md.

Codex (GPT-6). No fresh source search; initial s05 receipts only.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import json
import platform
import sys
import time

START = time.monotonic_ns()
HERE = Path(__file__).resolve().parent
OLD = HERE.parent/'s05'
sys.path.insert(0, str(OLD))
import maxsat_repair as source
import maxsat_reprice as raw


def forbidden(*args, **kwargs):
    raise RuntimeError('Fresh provider or exact diagnostic forbidden')


source.budget_provider = forbidden
raw.exact_diagnostic = forbidden


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def packed(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':')).encode()


input_path = OLD/'maxsat_repair_results.json'
data = json.loads(input_path.read_text())
profiles, shared, proof_check = raw.acquire_profiles(data)
assert len(profiles) == 16
old_weights = [s['weight'] for s in data['instances'][0]['soft']]
contexts = raw.recipes(old_weights)
assert len(contexts)*len(profiles) == 80
assert all([s['weight'] for s in inst['soft']] == old_weights
           for inst in data['instances'])


def build(mode):
    meter = source.Meter()
    items, blocks = [], []
    for p, inst in zip(profiles, data['instances']):
        public = next(w for w in p['witnesses']
                      if w['model'] == inst['public_incumbent'])
        baseline, base_work = [], 0
        for _, weights in contexts:
            before = meter.total
            baseline.append(min(6, raw.dot(public['violation_mask'], weights,
                                          meter, 'public_witness')))
            meter.pay('selection', 'baseline_and_price_min', 1)
            base_work += meter.total-before
        ids = []
        for w in p['witnesses']:
            if w['model'] == inst['public_incumbent']:
                continue
            vals, work = [], 0
            for _, weights in contexts:
                before = meter.total
                vals.append(raw.dot(w['violation_mask'], weights,
                                    meter, 'optional_witness'))
                meter.pay('selection', 'upper_min', 1)
                work += meter.total-before
            item = dict(id=len(items), row=p['row'], kind='witness', values=vals,
                        work=work, payload=dict(row=p['row'], model=w['model'],
                                              mask=w['violation_mask']))
            item['bytes'] = len(packed(item['payload']))
            items.append(item)
            ids.append(item['id'])
        for i, t in enumerate(p['trees']):
            vals, work = [], 0
            for _, weights in contexts:
                before = meter.total
                if mode == 'tree':
                    v = min(raw.dot(mask, weights, meter, 'tree_leaf')
                            for mask in t['leaf_masks'])
                    meter.pay('selection', 'leaf_min_and_lower_max',
                              len(t['leaf_masks'])+1)
                else:
                    ell = t['original_budget']+1
                    additive = max(0, ell+sum(min(0,w-a)
                                             for w,a in zip(weights,old_weights)))
                    scaled = ell*min(F(w,a) for w,a in zip(weights,old_weights))
                    v = max(additive, -(-scaled.numerator//scaled.denominator))
                    meter.pay('scalar', 'transport_arithmetic_comparison',
                              5*len(weights)+5)
                vals.append(v)
                work += meter.total-before
            payload = (dict(row=p['row'], leaves=t['leaf_masks']) if mode=='tree'
                       else dict(row=p['row'], lower=t['original_budget']+1,
                                 weights=old_weights))
            item = dict(id=len(items), row=p['row'], kind='lower',
                        archive_tree_index=i, values=vals, work=work,
                        payload=payload, bytes=len(packed(payload)))
            items.append(item)
            ids.append(item['id'])
        assert len(ids) <= 16
        blocks.append(dict(row=p['row'], baseline=baseline, ids=ids,
                           baseline_work=base_work))
    return items, blocks, meter.record()


def analyze(mode):
    items, blocks, table_invoice = build(mode)
    count = Counter()

    def local(block, selected):
        count['local_evaluations'] += 1
        us = block['baseline'].copy()
        ls = [0]*5
        ids = tuple(i for i in block['ids'] if i in selected)
        for i in ids:
            a = items[i]
            for q, v in enumerate(a['values']):
                count['retained_value_comparisons'] += 1
                if a['kind']=='witness':
                    us[q] = min(us[q], v)
                else:
                    ls[q] = max(ls[q], min(6, v))
        assert all(l<=u for l,u in zip(ls,us))
        gaps = [u-l for u,l in zip(us,ls)]
        mask = sum(1<<q for q,g in enumerate(gaps) if g<=1)
        return dict(ids=ids, n=len(ids), hits=mask.bit_count(), mask=mask,
                    gap_reduction=sum(block['baseline'])-sum(gaps),
                    work=block['baseline_work']+sum(items[i]['work'] for i in ids),
                    bytes=sum(items[i]['bytes'] for i in ids))

    def total(selected):
        count['global_evaluations'] += 1
        rows = [local(b, selected) for b in blocks]
        return dict(ids=tuple(sorted(selected)), n=len(selected),
                    hits=sum(r['hits'] for r in rows),
                    masks=[r['mask'] for r in rows],
                    gap_reduction=sum(r['gap_reduction'] for r in rows),
                    work=sum(r['work'] for r in rows),
                    bytes=sum(r['bytes'] for r in rows))

    def preference(r):
        return (r['hits'], -r['work'], -r['bytes'])

    local_best = []
    for block in blocks:
        best = {}
        for n in range(len(block['ids'])+1):
            for ids in combinations(block['ids'], n):
                count['enumerated_local_subsets'] += 1
                r = local(block, set(ids))
                if n not in best or preference(r)>preference(best[n]):
                    best[n] = r
        local_best.append(best)

    dp = {0:dict(ids=(), n=0, hits=0, work=0, bytes=0)}
    for best in local_best:
        nxt = {}
        for old in dp.values():
            for option in best.values():
                count['dp_transitions'] += 1
                n = old['n']+option['n']
                r = dict(ids=old['ids']+option['ids'], n=n,
                         hits=old['hits']+option['hits'],
                         work=old['work']+option['work'],
                         bytes=old['bytes']+option['bytes'])
                if n not in nxt or preference(r)>preference(nxt[n]):
                    nxt[n] = r
        dp = nxt
    exact = []
    for k in range(len(items)+1):
        best = max((r for n,r in dp.items() if n<=k), key=preference)
        checked = total(set(best['ids']))
        assert all(best[key]==checked[key] for key in ('n','hits','work','bytes'))
        exact.append(dict(budget=k, **checked))

    def greedy(k, kind):
        selected = set()
        current = total(selected)
        while len(selected)<k:
            remaining = [i for i in range(len(items)) if i not in selected]
            candidates = [(i,) for i in remaining]
            if kind=='pair' and k-len(selected)>=2:
                candidates += list(combinations(remaining,2))
            best = None
            for new in candidates:
                candidate = total(selected|set(new))
                objective = 'gap_reduction' if kind=='gap' else 'hits'
                delta = candidate[objective]-current[objective]
                rank = (F(delta,len(new)), delta, -len(new),
                        -candidate['work'], -candidate['bytes'])
                if best is None or rank>best[0]:
                    best = (rank,new,candidate)
            if best is None:
                break
            # Preserve zero-marginal single steps; they may unlock complements.
            selected.update(best[1])
            current = best[2]
        assert current['hits']<=exact[k]['hits']
        return dict(budget=k, **current)

    controls = {kind:[greedy(k,kind) for k in range(len(items)+1)]
                for kind in ('single','gap','pair')}
    full = total(set(range(len(items))))
    minimum = next(r for r in exact if r['hits']==full['hits'])
    assert minimum['masks']==full['masks']
    base = total(set())
    complementary = []
    for block in blocks:
        b = local(block,set())
        for i,j in combinations(block['ids'],2):
            a, c = local(block,{i}), local(block,{j})
            joint = local(block,{i,j})
            extra = joint['mask'] & ~(a['mask']|c['mask'])
            if extra:
                complementary.append(dict(row=block['row'], ids=[i,j],
                                          newly_joint_context_bits=extra))
    return dict(mode=mode, optional_count=len(items), items=items,
                baseline=base, full=full, minimum_full_closure=minimum,
                exact=exact, controls=controls,
                complementary_pairs=complementary,
                table_invoice=table_invoice, selection_counts=dict(count),
                local_subset_counts=[sum(1 for _ in range(1<<len(b['ids'])))
                                     for b in blocks])


arms = [analyze(mode) for mode in ('tree','scalar')]
assert [a['optional_count'] for a in arms]==[31,31]
result = dict(status='PASS', evidence='DEVELOPMENT', attribution='Codex (GPT-6)',
              python=platform.python_version(), runtime_ns=time.monotonic_ns()-START,
              source_sha256=sha(Path(__file__)),
              inputs={p.name:sha(p) for p in (input_path,OLD/'maxsat_repair.py',
                                             OLD/'maxsat_reprice.py')},
              archive_bytes=input_path.stat().st_size, contexts=80,
              source_check_invoices=dict(shared=shared.record(),proof=proof_check.record()),
              actual_fresh_source_calls=0, exact_optimum_calls=0, arms=arms,
              limitations=['Exposed fixed contexts; uniform coverage objective, not fees',
                           'Ordinary exact DP is the same method and ties',
                           'Selection comparisons are additional, not source tariff units',
                           'Compact payload bytes omit runtime overhead and archived raw proofs'])
(HERE/'retention_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ('status','runtime_ns','contexts')}))
for a in arms:
    print(json.dumps(dict(mode=a['mode'],baseline=a['baseline']['hits'],
                          full={k:a['full'][k] for k in ('hits','work','bytes')},
                          minimum={k:a['minimum_full_closure'][k]
                                   for k in ('n','hits','work','bytes')},
                          complementary_pairs=len(a['complementary_pairs']),
                          selection_counts=a['selection_counts'])))
