#!/usr/bin/env python3
"""Finite, source-bound obstruction diagnostics; no policy competition or tuning."""
from __future__ import annotations
import argparse
from collections import Counter
from dataclasses import replace
from fractions import Fraction as F
import gzip
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import platform
import sys
import traceback

sys.dont_write_bytecode = True
REVIEW_REL = 'v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/literature_and_obstruction/finite_obstruction_v1'
AUDIT_REL = REVIEW_REL + '/audit.py'
CONTRACT_REL = REVIEW_REL + '/prospective_contract.json'
RUNTIME = tuple('v3/checks/' + name for name in (
    '04_counterfactual_repair.py', '05_counterfactual_transport.py',
    '05_portfolio_transport.py', '05_ordinary_add.py', '05_add_evidence.py',
    '05_add_evidence_check.py', '05_certificate_delivery_cases.py'))


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True,
                      default=lambda value: str(value) if type(value) is F else (_ for _ in ()).throw(TypeError(type(value))))


def scalar(e, x):
    """Independent exact point semantics; no inherited truth routine is called."""
    tag = e[0]
    if tag == 'lit': return F(e[1])
    if tag == 'bit': return F(x[e[1]])
    if tag == 'not': return 1 - scalar(e[1], x)
    if tag == 'scale': return F(e[1]) * scalar(e[2], x)
    a, b = scalar(e[1], x), scalar(e[2], x)
    if tag == 'add': return a + b
    if tag == 'min': return min(a, b)
    if tag == 'max': return max(a, b)
    if tag == 'eq': return F(a == b)
    if tag == 'and': return F(a == 1 and b == 1)
    if tag == 'or': return F(a == 1 or b == 1)
    raise ValueError('Unknown scalar grammar tag.')


def feasible(frame, x):
    return all(scalar(h, x) == 1 for h in frame.request.hard)


def rank(frame, x):
    return sum((F(s.weight) * (1 - scalar(s.formula, x)) for s in frame.request.soft), F(0))


def parity(K, order):
    value = K.bit(order[0])
    for i in order[1:]: value = K.neg(K.eq(value, K.bit(i)))
    return value


def shape(tree):
    if tree[0] == 'split':
        a, b = shape(tree[2]), shape(tree[3])
        leaves = Counter(a['leaf_kinds']) + Counter(b['leaf_kinds'])
        return {'nodes': 1+a['nodes']+b['nodes'], 'leaves': a['leaves']+b['leaves'],
                'splits': 1+a['splits']+b['splits'], 'depth': 1+max(a['depth'], b['depth']),
                'leaf_kinds': dict(leaves)}
    kind = tree[1] if tree[0] == 'leaf' else tree[0]
    return {'nodes': 1, 'leaves': 1, 'splits': 0, 'depth': 0, 'leaf_kinds': {kind: 1}}


def reachable(manager, root):
    seen, todo = set(), [root]
    while todo:
        i = todo.pop()
        if i in seen: continue
        seen.add(i)
        node = manager.nodes[i]
        if node[0] == 'node': todo.extend(node[2:])
    terminals = sum(manager.nodes[i][0] == 'terminal' for i in seen)
    return {'nodes': len(seen), 'terminals': terminals, 'decisions': len(seen)-terminals,
            'ids': sorted(seen)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source-root', required=True, type=Path)
    ap.add_argument('--out', required=True, type=Path)
    args = ap.parse_args()
    root, out = args.source_root.resolve(), args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    artifacts, failures = [], []
    counted_checks = 0
    source_paths = RUNTIME + (AUDIT_REL, CONTRACT_REL)
    before = {p: digest((root/p).read_bytes()) for p in source_paths}

    def save(name, value, raw=None):
        target = out/name
        target.parent.mkdir(parents=True, exist_ok=True)
        body = (encoded(value)+'\n').encode() if raw is None else raw
        target.write_bytes(body)
        row = {'path': name, 'sha256': digest(body), 'bytes': len(body)}
        artifacts.append(row)
        return row

    def check(condition, label, detail=None):
        nonlocal counted_checks
        counted_checks += 1
        if not condition: failures.append({'check': label, 'detail': detail})

    E = load('_rp3bb_obstruction_producer', root/'v3/checks/05_add_evidence.py')
    C = load('_rp3bb_obstruction_cases', root/'v3/checks/05_certificate_delivery_cases.py')
    R = E.receiver_module()
    M, K, P, A = E.M, E.K, E.P, E.A
    check(C.M is M and C.K is K and R.M is M, 'shared_module_identity')
    source_record = E.make_source_record(RUNTIME + (AUDIT_REL,), repo_root=root)
    save('source_record.json', None, raw=source_record.encode())
    save('prospective_contract.json', json.loads((root/CONTRACT_REL).read_text()))

    def frame(n, difference, name, hard=(), soft=()):
        metadata = encoded({'stage':'DEVELOPMENT','task':'R-P3-B-B','diagnostic':name,
                            'source':'fixed finite obstruction audit v1'})
        request = K.Request(n, tuple(hard), tuple(soft), (('D', difference),),
                            'rp3bb-obstruction-v1/'+name, metadata)
        return M.Frame(request, 'D', 'declared-loss-unit')

    def tree_record(name, proof):
        return save(name, None, raw=M.canonical(proof.record()).encode())

    def reject(name, cache, proof, current):
        record = tree_record(name+'/submitted_proof.json', proof)
        try:
            report = cache.verify(proof, current, current.record())
        except M.Rejected as exc:
            return {'status':'EXPECTED_REJECTION','exception':type(exc).__name__,
                    'detail':str(exc),'proof':record}
        check(False, name+'/must_reject', report)
        return {'status':'UNEXPECTED_ACCEPTANCE','report':report,'proof':record}

    parity_rows, complement_rows, old_rows, null_rows = [], [], [], []
    full_cube_frames = {}
    try:
        cells_path = out/'all_parity_cells.jsonl.gz'
        with cells_path.open('wb') as raw_cells:
            with gzip.GzipFile(filename='', fileobj=raw_cells, mode='wb', mtime=0) as cells:
                for n in range(2, 9):
                    pn = parity(K, tuple(range(n)))
                    qn = parity(K, tuple(reversed(range(n))))
                    d = K.sub(pn, qn)
                    f = frame(n, d, f'parity_n{n}')
                    x = (0,)*n
                    full_cube_frames[n] = f
                    target_vec, target_atoms = P.form(d)
                    target_keys = set(target_vec)
                    check(len(target_keys) == 2 and all(target_atoms[k][0] == 'eq' for k in target_keys),
                          f'n{n}/two_distinct_opaque_equality_features')
                    proper_count = complete_count = 0
                    hist = Counter()
                    for cell in product((None,0,1), repeat=n):
                        a, b = K.interval(pn, cell), K.interval(qn, cell)
                        enclosure = M.enclosure(d, cell)
                        rows = P.context_rows(f, cell, F(0))
                        upper0 = P.conditional_upper(d, (), rows, cell)
                        # This fixed positive tuple is a finite consistency check only.
                        # The arbitrary-multiplier proof is supplied by row support below.
                        weights = tuple((i, F(i+1, i+2)) for i in range(len(rows.expressions)))
                        upperw = P.conditional_upper(d, weights, rows, cell)
                        assigned_keys = {M._key(K.bit(i)) for i,v in enumerate(cell) if v is not None}
                        supports_ok = True
                        for row in rows.expressions:
                            rv, _ = P.form(row)
                            support = set(rv)-{P._CON}
                            supports_ok &= support <= assigned_keys and not (support & target_keys)
                            supports_ok &= M.enclosure(row, cell) == (F(0),F(0))
                        check(supports_ok, f'n{n}/premise_support/{cell}')
                        proper = None in cell
                        if proper:
                            proper_count += 1
                            check(a == b == (F(0),F(1)) and enclosure == (F(-1),F(1))
                                  and upper0 == upperw == 1,
                                  f'n{n}/proper_box/{cell}', [a,b,enclosure,upper0,upperw])
                        else:
                            complete_count += 1
                            exact = F(sum(cell)%2)
                            check(a == b == (exact,exact) and enclosure == (F(0),F(0))
                                  and upper0 == upperw == 0 and scalar(d,cell) == 0,
                                  f'n{n}/singleton/{cell}')
                        hist[(str(enclosure[0]),str(enclosure[1]),str(upper0))] += 1
                        cells.write((encoded({'n':n,'cell':cell,'proper':proper,
                                              'forward_interval':a,'reverse_interval':b,
                                              'band_enclosure':enclosure,'portfolio_upper_empty':upper0,
                                              'portfolio_upper_fixed_positive_weights':upperw,
                                              'premise_count':len(rows.expressions),
                                              'premise_support_assigned_bits_only_and_exact_zero':supports_ok})+'\n').encode())
                    check(proper_count == 3**n-2**n and complete_count == 2**n, f'n{n}/cell_counts')
                    bw, bv = {}, {}
                    band = M.build_band(f, 0, 0, bw)
                    M.verify_band(band, f.record(), bv)
                    band_artifact = tree_record(f'parity/n{n}/band.json', band)
                    empty = P.PortfolioCache()
                    pw, pv = {}, {}
                    fresh = empty.build(f, (), x, 0, symbolic=True, work=pw)
                    fresh_report = empty.verify(fresh, f, f.record(), pv)
                    fresh_artifact = tree_record(f'parity/n{n}/fresh_portfolio.json', fresh)
                    lw, lv = {}, {}
                    lm = A.Manager(n)
                    legacy = E.export_tree(lm, f, x, 0, f.record(), symbolic=True, work=lw)
                    legacy_report = empty.verify(legacy, f, f.record(), lv)
                    legacy_artifact = tree_record(f'parity/n{n}/ordinary_exported_tree.json', legacy)
                    expected = {'nodes':2**(n+1)-1,'leaves':2**n,'splits':2**n-1,'depth':n}
                    for label, proof, checked in [('band',band,bv.get('verified_proof_nodes')),
                                                   ('fresh_portfolio',fresh,pv.get('verified_cover_nodes')),
                                                   ('ordinary_exported_tree',legacy,lv.get('verified_cover_nodes'))]:
                        s = shape(proof.tree)
                        check(all(s[k] == v for k,v in expected.items()) and checked == expected['nodes'],
                              f'n{n}/{label}/tree_size', {'shape':s,'checked':checked})
                    dw, dv = {}, {}
                    epoch = f'finite-obstruction-parity-{n}'
                    dm = E.RecordingManager(n, source_record=source_record, epoch=epoch, work=dw)
                    evidence = E.export_dag(dm, f, x, 0, f.record(), work=dw)
                    wire = E.to_wire(evidence, dw)
                    receiver = R.Receiver(source_record, epoch, n, work=dv)
                    dag_report = receiver.receive(wire, f, f.record(), x, 0, work=dv, request_id=f'n{n}')
                    root_p, root_q = dm.expressions[pn], dm.expressions[qn]
                    reachable_p, reachable_q = reachable(dm, root_p), reachable(dm, root_q)
                    reachable_d, reachable_bad = reachable(dm,evidence.roots[2]), reachable(dm,evidence.roots[3])
                    check(root_p == root_q and reachable_p['nodes'] == 2*n+1
                          and reachable_p['decisions'] == 2*n-1 and reachable_p['terminals'] == 2,
                          f'n{n}/parity_root_size', reachable_p)
                    check(reachable_d['nodes'] == reachable_bad['nodes'] == 1
                          and dm.nodes[evidence.roots[2]] == ('terminal',F(0)),
                          f'n{n}/difference_and_bad_zero_roots')
                    wire_artifact = save(f'parity/n{n}/dag_wire.json', None, raw=wire)
                    producer_artifact = save(f'parity/n{n}/producer_retained.json', None, raw=dm.state_bytes())
                    receiver_artifact = save(f'parity/n{n}/receiver_retained.json', None,
                                              raw=M.canonical(receiver.state_record()).encode())
                    save(f'parity/n{n}/dag_report.json', dag_report)
                    row = {'n':n,'current_record':f.record(),'proper_boxes':proper_count,'singletons':complete_count,
                           'interval_histogram':[{'band_lower':a,'band_upper':b,'portfolio_upper':c,'count':v}
                                                 for (a,b,c),v in sorted(hist.items())],
                           'predicted_tree':expected,
                           'band':{'shape':shape(band.tree),'checker_nodes':bv['verified_proof_nodes'],
                                   'record':band_artifact,'producer_work':bw,'checker_work':bv},
                           'fresh_portfolio':{'shape':shape(fresh.tree),'checker_nodes':pv['verified_cover_nodes'],
                                              'record':fresh_artifact,'report':fresh_report,'producer_work':pw,'checker_work':pv},
                           'ordinary_exported_tree':{'shape':shape(legacy.tree),'checker_nodes':lv['verified_cover_nodes'],
                                                      'record':legacy_artifact,'report':legacy_report,
                                                      'producer_work':lw,'checker_work':lv,'manager_storage':lm.storage()},
                           'dag':{'forward_root':root_p,'reverse_root':root_q,'roots':evidence.roots,
                                  'reachable_forward':reachable_p,'reachable_reverse':reachable_q,
                                  'reachable_difference':reachable_d,'reachable_bad':reachable_bad,
                                  'all_constructed_nodes':len(dm.nodes),'all_apply_facts':len(dm.apply_log),
                                  'all_expression_facts':len(dm.expression_log),
                                  'all_expression_key_bytes':sum(len(key.encode()) for key,_ in evidence.expressions),
                                  'node_fact_encoding_bytes':len(E.canonical(evidence.nodes).encode()),
                                  'apply_fact_encoding_bytes':len(E.canonical(evidence.applies).encode()),
                                  'expression_fact_encoding_bytes':len(E.canonical(evidence.expressions).encode()),
                                  'terminal_values':sorted({str(node[1]) for node in dm.nodes if node[0] == 'terminal'}),
                                  'wire':wire_artifact,
                                  'producer_retained':producer_artifact,'receiver_retained':receiver_artifact,
                                  'receiver_counts':receiver.state_counts(),'producer_work':dw,'checker_work':dv}}
                    parity_rows.append(row)
                    save(f'parity/n{n}/row.json', row)
                    print(encoded({'progress':'parity','n':n,'proper_boxes':proper_count,
                                   'tree_nodes':expected['nodes'],'dag_all_nodes':len(dm.nodes)}), flush=True)
        cells_raw = cells_path.read_bytes()
        artifacts.append({'path':'all_parity_cells.jsonl.gz','sha256':digest(cells_raw),'bytes':len(cells_raw)})

        caches = {}
        five_tree = ('split',0,('reuse',0,((),),(),()),
                     ('split',1,('hard',0),('reuse',1,((),),(),())))
        for stream in C.streams():
            if not stream.name.startswith('complementary_'): continue
            cache = P.PortfolioCache()
            choices = []
            for old_index, old in enumerate(stream.old):
                domain_points = []
                for point in product((0,1), repeat=stream.nbits):
                    included = feasible(old.frame, point) and rank(old.frame, point) <= 0
                    expected_predicate = point[0] == 0 if old_index == 0 else point[1] == 1
                    check(included == expected_predicate, old.name+'/predicate/'+str(point))
                    check(rank(old.frame, point) == 0, old.name+'/rank_zero/'+str(point))
                    check(scalar(old.frame.difference,point) == point[0]-point[1], old.name+'/difference/'+str(point))
                    if included:
                        domain_points.append(point)
                        check(scalar(old.frame.difference,point) <= old.bound, old.name+'/bound/'+str(point))
                check(feasible(old.frame,old.witness) and rank(old.frame,old.witness) == 0,
                      old.name+'/old_incumbent')
                work, verification = {}, {}
                proof = M.build_band(old.frame, 0, old.bound, work)
                cache.admit_band(old.handle, proof, old.frame.record(), verification)
                old_row = {'case':old.name,'frame_record':old.frame.record(),'domain_points':domain_points,
                           'predicate':'p=0' if old_index == 0 else 'q=1','rank':'0','bound':old.bound,
                           'certificate_shape':shape(proof.tree),'certificate':tree_record(f'complement/{stream.name}/old{old_index}.json',proof),
                           'producer_work':work,'admission_work':verification}
                old_rows.append(old_row)
                choices.append(P.Choice(old.handle, old.frame.record(), stream.identity_replacements, F(1)))
            choices = tuple(choices)
            caches[stream.name] = (cache,choices,stream)
            for j, case in enumerate(stream.edits):
                f, witness = case.frame, case.witness
                cutoff = rank(f,witness)
                check(feasible(f,witness), case.name+'/incumbent_feasible')
                named = []
                for name, point in case.named_witnesses:
                    old_membership = [feasible(old.frame,point) and rank(old.frame,point) <= 0 for old in stream.old]
                    current_ok = feasible(f,point) and rank(f,point) <= cutoff
                    expected_membership = [True,False] if name.startswith('left_') else [False,True] if name.startswith('right_') else [True,True]
                    check(current_ok and rank(f,point) == cutoff and old_membership == expected_membership,
                          case.name+'/'+name, {'point':point,'old':old_membership,'rank':str(rank(f,point)),'cutoff':str(cutoff)})
                    named.append({'name':name,'assignment':point,'current_hard':feasible(f,point),
                                  'current_rank':rank(f,point),'cutoff':cutoff,'in_current_sublevel':current_ok,
                                  'old_membership':old_membership,'difference':scalar(f.difference,point)})
                all_points = []
                hard_points = [x for x in product((0,1), repeat=stream.nbits) if feasible(f,x)]
                minrank = min(rank(f,x) for x in hard_points)
                hist = Counter()
                for point in product((0,1), repeat=stream.nbits):
                    r = rank(f,point)
                    current_ok = feasible(f,point) and r <= cutoff
                    old_membership = [feasible(old.frame,point) and rank(old.frame,point) <= 0 for old in stream.old]
                    d = scalar(f.difference,point)
                    if current_ok:
                        hist[(tuple(old_membership), str(d))] += 1
                        check(any(old_membership) and d <= case.bound, case.name+'/whole_sublevel/'+str(point))
                    all_points.append({'assignment':point,'hard':feasible(f,point),'rank':r,'cutoff':cutoff,
                                       'in_current_sublevel':current_ok,'is_minimizer':feasible(f,point) and r == minrank,
                                       'old_membership':old_membership,'difference':d})
                values = {F(value) for (_,value),count in hist.items() if count}
                shift = F(1,2) if j == 5 else F(0)
                check(values == {shift-1,shift}, case.name+'/nonconstant_values',sorted(map(str,values)))
                proof = P.PortfolioProof(f.record(), choices, witness, case.bound, five_tree)
                verify_work = {}
                report = cache.verify(proof, f, f.record(), verify_work)
                check(report['counts'] == {'reuse_leaves':2,'direct_leaves':0,'hard_exclusions':1,'rank_exclusions':0,'splits':2}
                      and verify_work['verified_cover_nodes'] == 5, case.name+'/five_node_checker',report['counts'])
                single_failures = []
                for index in (0,1):
                    one_tree = ('split',0,('reuse',0,((),),(),()),
                                ('split',1,('hard',0),('reuse',0,((),),(),())))
                    wrong = P.PortfolioProof(f.record(), (choices[index],), witness, case.bound, one_tree)
                    single_failures.append(reject(f'complement/{stream.name}/edit{j}/only_old{index}',cache,wrong,f))
                row = {'stream':stream.name,'edit':j,'current_record':f.record(),'witness':witness,
                       'requested_bound':case.bound,'cutoff':cutoff,'minimum_rank':minrank,
                       'named_witnesses':named,'hard_count':len(hard_points),
                       'sublevel_count':sum(h['in_current_sublevel'] for h in all_points),
                       'membership_and_difference_counts':[{'old_membership':membership,'difference':d,'count':count}
                                                            for (membership,d),count in sorted(hist.items())],
                       'proof':tree_record(f'complement/{stream.name}/edit{j}/five_node_proof.json',proof),
                       'checker_report':report,'checker_work':verify_work,
                       'single_old_partition_rejections':single_failures}
                save(f'complement/{stream.name}/edit{j}/all_points.json',all_points)
                save(f'complement/{stream.name}/edit{j}/row.json',row)
                complement_rows.append(row)
                print(encoded({'progress':'complement','stream':stream.name,'edit':j,
                               'sublevel':row['sublevel_count'],'cutoff':str(cutoff)}),flush=True)

        # Prespecified null cases: scope qualifications, not alternative policy search.
        null_configs = []
        p1 = parity(K,(0,))
        null_configs.append(('one_bit_identical',frame(1,K.sub(p1,p1),'null_n1'),F(0)))
        p3 = parity(K,(0,1,2))
        null_configs.append(('identical_syntax',frame(3,K.sub(p3,p3),'null_same_fold'),F(0)))
        null_configs.append(('loosen_bound_one',full_cube_frames[3],F(1)))
        for name, f, bound in null_configs:
            bp = M.build_band(f,0,bound)
            M.verify_band(bp,f.record())
            pc = P.PortfolioCache()
            pp = pc.build(f,(),(0,)*f.request.nbits,bound)
            report = pc.verify(pp,f,f.record())
            check(shape(bp.tree)['nodes'] == shape(pp.tree)['nodes'] == 1, 'null/'+name)
            null_rows.append({'case':name,'conclusion':'Strict exponential-tree claim does not apply.',
                              'band_shape':shape(bp.tree),'portfolio_shape':shape(pp.tree),'report':report,
                              'band':tree_record('null/'+name+'/band.json',bp),
                              'portfolio':tree_record('null/'+name+'/portfolio.json',pp)})
        f = full_cube_frames[3]
        cached = P.PortfolioCache()
        cached.admit_band('full_old',M.build_band(f,0,0),f.record())
        choice = P.Choice('full_old',f.record(),tuple(K.bit(i) for i in range(3)))
        pp = P.PortfolioProof(f.record(),(choice,),(0,)*3,F(0),('reuse',0,(),(),()))
        report = cached.verify(pp,f,f.record())
        check(report['counts']['reuse_leaves'] == 1,'null/admitted_history_one_leaf')
        null_rows.append({'case':'admitted_same_full_domain','conclusion':'Useful admitted history removes the empty-history obstruction.',
                          'shape':shape(pp.tree),'report':report,'proof':tree_record('null/admitted_history.json',pp)})

        cache, choices, stream = caches['complementary_k3_n5']
        initial = stream.edits[0]
        rank_soft = (K.Soft('prefer_not_p',K.neg(K.bit(0)),F(1),0),K.Soft('prefer_q',K.bit(1),F(1),0))
        narrowed = frame(stream.nbits,initial.frame.difference,'null_rank_depends_on_pq',
                         (initial.frame.request.hard[0],),rank_soft)
        cutoff = rank(narrowed,initial.witness)
        survivors = [x for x in product((0,1),repeat=stream.nbits) if feasible(narrowed,x) and rank(narrowed,x) <= cutoff]
        check(cutoff == 0 and survivors and all(x[0] == 0 and x[1] == 1 for x in survivors),
              'null/pq_rank_destroys_exclusive_points')
        one_reports=[]
        for index in (0,1):
            multiplier = ((0,F(1)),)
            pp = P.PortfolioProof(narrowed.record(),(choices[index],),initial.witness,F(0),
                                  ('reuse',0,(multiplier,),(),()))
            report=cache.verify(pp,narrowed,narrowed.record())
            check(report['counts']['reuse_leaves'] == 1,'null/pq_rank_one_old/'+str(index))
            one_reports.append({'old_index':index,'report':report,
                                'proof':tree_record('null/pq_rank/only_old'+str(index)+'.json',pp)})
        null_rows.append({'case':'rank_rows_on_pq','conclusion':'Positive weights and a free parity coordinate alone do not imply two-domain necessity.',
                          'current_record':narrowed.record(),'cutoff':cutoff,'sublevel_points':survivors,'one_leaf_reports':one_reports})
        withdrawn = frame(stream.nbits,initial.frame.difference,'null_withdraw_H',
                          initial.frame.request.hard[1:],initial.frame.request.soft)
        violating = (1,0)+initial.witness[2:]
        check(feasible(withdrawn,violating) and rank(withdrawn,violating) <= rank(withdrawn,initial.witness)
              and scalar(withdrawn.difference,violating) == 1,'null/withdraw_H_counterexample')
        pp = P.PortfolioProof(withdrawn.record(),choices,initial.witness,F(0),five_tree)
        null_rows.append({'case':'withdraw_H','current_record':withdrawn.record(),'violating_point':violating,
                          'difference':scalar(withdrawn.difference,violating),
                          'rejection':reject('null/withdraw_H',cache,pp,withdrawn)})
        last = stream.edits[5]
        violating = dict(last.named_witnesses)['left_exclusive_parity_one']
        check(feasible(last.frame,violating) and rank(last.frame,violating) <= rank(last.frame,last.witness)
              and scalar(last.frame.difference,violating) == F(1,2),'null/missing_half_drift_counterexample')
        pp = P.PortfolioProof(last.frame.record(),choices,last.witness,F(0),five_tree)
        null_rows.append({'case':'missing_half_drift','current_record':last.frame.record(),'incorrect_requested_bound':'0',
                          'violating_point':violating,'difference':'1/2','rejection':reject('null/missing_half_drift',cache,pp,last.frame)})
        save('parity_rows.json',parity_rows)
        save('old_domain_rows.json',old_rows)
        save('complementary_rows.json',complement_rows)
        save('null_rows.json',null_rows)
    except BaseException as exc:
        failures.append({'check':'unhandled_execution_exception','detail':type(exc).__name__+': '+str(exc)})
        save('execution_failure.json',{'type':type(exc).__name__,'detail':str(exc),'traceback':traceback.format_exc(),
                                       'completed_parity':len(parity_rows),'completed_complement':len(complement_rows)})
        raise
    finally:
        after = {p:digest((root/p).read_bytes()) for p in source_paths}
        check(before == after,'captured_source_preservation')
        summary={'stage':'DEVELOPMENT','task':'R-P3-B-B','principal_clock_credit_minutes':0,
                 'policy_competition_or_tuning':False,'python':sys.version,'platform':platform.platform(),
                 'checks':counted_checks,'failures':failures,'pass':not failures,
                 'parity_dimensions_completed':[r['n'] for r in parity_rows],
                 'proper_boxes_completed':sum(r['proper_boxes'] for r in parity_rows),
                 'complete_boxes_completed':sum(r['singletons'] for r in parity_rows),
                 'complementary_edits_completed':len(complement_rows),'old_domains_completed':len(old_rows),
                 'null_groups_completed':len(null_rows),'source_hashes_before':before,'source_hashes_after':after,
                 'artifacts':artifacts,'cost_scope':'Raw diagnostic counts/serialized sizes only; no common tariff or policy frontier claim.'}
        save('summary.json',summary)
        print(encoded({k:summary[k] for k in ('checks','failures','pass','parity_dimensions_completed',
                                             'proper_boxes_completed','complementary_edits_completed','null_groups_completed')}),flush=True)
    if failures: raise SystemExit(1)


if __name__ == '__main__': main()
