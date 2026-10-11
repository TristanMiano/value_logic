#!/usr/bin/env python3
"""Independent saved-JSON geometry audit. No project imports or truth evaluator.

The public reconstruction uses incremental Minkowski sums and exact monotone
chain hulls, distinct from the reviewed angular edge-walk implementation.
Existing numeric truth records are parsed only after this run's public
reconstruction is saved. The reviewer is unblinded; no new coverage claim.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
import time
import traceback

ROOT = Path('/workspace/scratch/095cdac579b7/value_logic')
WORK = ROOT / 'v3/work_logs/P3_10_2026-10-11_S1'
HERE = Path(__file__).resolve().parent
OUT = HERE / 'independent_observation_v1'
OUT.mkdir(exist_ok=False)
READS, OFFICIAL = {}, {}
CHECKS, COUNTS = Counter(), Counter()
DIFFERENCES = []


def stamp():
    return {'utc': datetime.now(timezone.utc).isoformat(),
            'monotonic_ns': time.monotonic_ns()}


def digest(b):
    return hashlib.sha256(b).hexdigest()


def require(condition, name, detail=None):
    CHECKS[name] += 1
    if not condition:
        raise AssertionError(f'{name}: {detail}')


def loads(b):
    def pairs(items):
        result = {}
        for k, v in items:
            if k in result:
                raise AssertionError('Duplicate JSON key: ' + k)
            result[k] = v
        return result
    return json.loads(b, object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def read(path, parse=True):
    p = Path(path)
    b = p.read_bytes()
    k = str(p.relative_to(ROOT))
    meta = {'path': k, 'bytes': len(b), 'sha256': digest(b)}
    require(k not in READS or READS[k] == meta, 'read_stability', k)
    READS[k] = meta
    if k.startswith(('v3/experiments/final_v1/',
                     'v3/experiments/final_v1_amended_A1/',
                     'v3/experiments/frozen_v1/')):
        require(OFFICIAL.get(k) == meta, 'prior_independent_lineage_hash', k)
    return loads(b) if parse else b


def rat(x):
    return F(*x) if isinstance(x, list) else F(x)


def encode(x):
    if isinstance(x, F):
        return [x.numerator, x.denominator]
    if isinstance(x, dict):
        return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [encode(v) for v in x]
    return x


def canonical(x):
    return (json.dumps(encode(x), sort_keys=True, separators=(',', ':'),
                       ensure_ascii=True, allow_nan=False) + '\n').encode()


def save(path, x):
    with Path(path).open('x') as f:
        json.dump(encode(x), f, sort_keys=True, indent=2, allow_nan=False)
        f.write('\n')


def same(actual, expected, where):
    CHECKS['exact_reconstructed_field'] += 1
    if actual != encode(expected):
        DIFFERENCES.append({'where': where, 'actual': actual,
                            'expected': encode(expected)})


def verified_result(path):
    path = Path(path)
    seal, start, result = (read(path.parent / 'seal.json'),
                           read(path.parent / 'start.json'), read(path))
    require(digest(path.read_bytes()) == seal['result_sha256'], 'seal_result_hash')
    require(result['identity'] == start['identity'] == seal['identity']
            and result['unit'] == start['unit']
            and result['attempt'] == start['attempt'] == seal['attempt'],
            'sealed_result_identity')
    return result


def full_key(x):
    require(isinstance(x, list) and len(x) == 4, 'complete_key_shape')
    return json.dumps(x, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False)


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def minus(a, b):
    return (a[0] - b[0], a[1] - b[1])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def convex_hull(points):
    """Lexicographically sorted exact hull; no angle sorting or generator flips."""
    points = sorted(set(points))
    if len(points) <= 1:
        return points
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(minus(lower[-1], lower[-2]),
                                        minus(p, lower[-1])) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(minus(upper[-1], upper[-2]),
                                        minus(p, upper[-1])) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def minkowski_hull(origin, vectors):
    hull = [origin]
    for v in vectors:
        hull = convex_hull(hull + [(p[0] + v[0], p[1] + v[1]) for p in hull])
        COUNTS['incremental_hull_steps'] += 1
    return hull


def cyclic_origin(vertices):
    index = min(range(len(vertices)), key=vertices.__getitem__)
    return vertices[index:] + vertices[:index]


def contained(hull, point):
    # A point is in a convex hull iff adjoining it does not enlarge the hull.
    return convex_hull(hull + [point]) == hull


def support(origin, vectors, direction):
    projected = [dot(v, direction) for v in vectors]
    constant = dot(origin, direction)
    return (constant + sum((min(F(0), z) for z in projected), F(0)),
            constant + sum((max(F(0), z) for z in projected), F(0)))


START = stamp()
try:
    lineage_path = WORK / 'reviews/certificate_reconstruction/final_observation_v4/source_hashes.json'
    lineage_bytes = lineage_path.read_bytes()
    require(digest(lineage_bytes) == '58b51d1f1379ddf41ed34f8949fdc315de524aa5e61a3f38fe5d2aba7e0c75fb',
            'prior_independent_lineage_manifest')
    OFFICIAL = {x['path']: x for x in loads(lineage_bytes)['consumed_files']}
    read(lineage_path)
    snapshots = read(HERE / 'initial_snapshot_manifest.json')
    for s in snapshots['files']:
        b = read(ROOT / s['review_snapshot'], False)
        require(digest(b) == s['sha256'] and len(b) == s['bytes'], 'snapshot_integrity')
    snap = HERE / 'source_and_data'
    principal = read(snap / 'joint_report_geometry_observation_A1/public_geometry.json')
    prior = read(snap / 'retrospective_report_observation_A1/public_bounds.json')
    require(principal['status'] == prior['status'] == 'PASS', 'public_observer_status')
    for name, path in [('source_sha256', 'joint_report_geometry_observer.py'),
                       ('derivation_sha256', 'joint_report_geometry.md'),
                       ('derivation_addendum_sha256', 'joint_report_geometry_addendum.md'),
                       ('earlier_public_bounds_sha256', 'retrospective_report_observation_A1/public_bounds.json')]:
        require(principal[name] == digest(read(snap / path, False)), 'principal_binding', name)
    require(principal['private_truth_reads_before_public_geometry_saved'] == 0
            and prior['private_truth_reads_before_bounds_saved'] == 0,
            'public_phase_declarations')
    require(principal['amendment_lineage'] == prior['amendment_lineage'], 'same_lineage_receipt')
    require(principal['amendment_lineage']['reader_source_sha256'] ==
            digest(read(snap / 'amended_lineage_reader.py', False)), 'lineage_reader_pin')
    require(principal['amendment_lineage']['original_failed_prefix_cost'] == 'unknown',
            'unknown_prefix_preserved')

    schedule = read(ROOT / 'v3/experiments/frozen_v1/schedule.json')
    group_map = {g['id']: g for g in schedule['groups']}
    units = [u for u in schedule['units'] if u['arm'] == 'broker' and u['engine'] in ('broker', 'mirror')]
    ids = [u['id'] for u in units]
    require(len(ids) == len(set(ids)) == 126, '126_distinct_scheduled_parents')
    require([r['unit_id'] for r in principal['records']] == ids
            and [r['unit_id'] for r in prior['records']] == ids, 'complete_public_rosters')
    require(principal['scheduled_reports'] == principal['available_reports'] == 126,
            'complete_report_denominators')
    by_principal = {r['unit_id']: r for r in principal['records']}
    by_prior = {r['unit_id']: r for r in prior['records']}
    composite = read(ROOT / 'v3/experiments/final_v1_amended_A1/composite_public.json')
    require(composite['expected_units'] == composite['completed_units'] == 500
            and composite['original_units'] == 440 and composite['amended_units'] == 60,
            'completed_composite')
    refs = {r['unit_id']: r for r in composite['seals']}
    input_refs = read(ROOT / 'v3/experiments/final_v1_amended_A1/input_reference.json')
    inputs = {r['unit_id']: verified_result(ROOT / r['origin_root'] / r['result_path'])
              for r in input_refs['seals'] if group_map[r['unit_id']]['arm'] == 'broker'}
    for stage, expected in [('public', 60), ('evaluation', 500), ('analysis', 1)]:
        complete = read(ROOT / 'v3/experiments/final_v1_amended_A1/stages' / stage / 'complete.json')
        require(complete['expected_units'] == complete['completed_units'] == expected,
                'completion_barrier', stage)

    records, cache = [], {}
    for unit in units:
        uid = unit['id']
        ref, observed, earlier = refs[uid], by_principal[uid], by_prior[uid]
        raw = verified_result(ROOT / ref['origin_root'] / ref['result_path'])
        paid = raw['value']['paid_result']
        require(paid['unit'] == raw['unit'] == unit, 'scheduled_paid_identity', uid)
        episode, report = paid['episode'], paid['optional_reporting']['report']
        require(episode['status'] == report['status'] == 'success'
                and observed['status'] == earlier['status'] == 'available', 'complete_parent_report', uid)
        rows = episode['trace']
        queries = inputs[unit['group_id']]['value']['queries']
        horizon = episode['contract']['horizon']
        whole = [x for x in unit['segments'] if x['name'] == 'whole']
        require(len(whole) == 1 and whole[0]['start'] == 0
                and whole[0]['stop'] == horizon == len(rows) == len(queries)
                and [x['index'] for x in rows] == list(range(horizon)), 'full_ordered_horizon', uid)
        expected_scope = [queries[0]['semantics_version'], queries[0]['source_version'], 'p309-' + unit['group_id']]
        require(episode['scope'] == episode['hard_state']['scope'] == expected_scope
                and all(episode['hard_state'][k] == 0 for k in ('generation', 'conflicts', 'withdrawals')),
                'full_scope_unchanged_epoch', uid)
        require(episode['hard_enabled'] == unit['parameters']['hard'], 'scheduled_hard_mode', uid)
        invoices = episode['invoices']
        invoice_ids = [x['query_id'] for x in invoices]
        selected_ids = [x['query_id'] for x in rows if x['selected']]
        require(invoice_ids == selected_ids and len(set(invoice_ids)) == len(invoices) == horizon // 4,
                'exact_ordered_selected_invoice_roster', uid)
        by_invoice, known = {}, {}
        provider = ('bounded_cnf_checked', 'p308-bounded-cnf-services-v1.1') if unit['parameters']['provider'] == 'cold' else (
                   'owned_cached_cnf_receipt', 'p308-selected-receipt-cache-v1.1')
        for inv in invoices:
            require(inv['status'] == 'success' and inv['checked'] is True
                    and type(inv['answer']) is int and inv['answer'] in (0, 1)
                    and (inv['provider'], inv['provider_version']) == provider,
                    'current_checked_provider', uid)
            key = full_key(inv['claim_key'])
            require(key not in known or known[key] == inv['answer'], 'consistent_paid_key', uid)
            known[key] = inv['answer']
            by_invoice[inv['query_id']] = inv
        constant = {'F': F(0), 'V': F(0), 'Z': F(0)}
        coefficients = defaultdict(lambda: [F(0), F(0), F(0)])
        all_keys, rowkeys, shift = set(), [], F(0)
        for row, query in zip(rows, queries):
            claim = [query['semantics_version'], query['source_version'], query['variables'], query['clauses']]
            require(row['claim_key'] == claim and row['scope'] == expected_scope
                    and row['query_id'] == query['query_id'], 'row_input_full_identity', [uid, row['index']])
            key = full_key(claim)
            all_keys.add(key)
            rowkeys.append(key)
            q, a, selected = rat(row['emitted_q']), row['terminal_action'], row['selected']
            require(0 <= q <= 1 and type(a) is int and a in (0, 1)
                    and type(selected) is bool, 'binary_record_domain', [uid, row['index']])
            if selected:
                inv = by_invoice[row['query_id']]
                require(inv['claim_key'] == claim and inv['answer'] == row['purchased_label'] == a,
                        'selected_label_binding', [uid, row['index']])
                shift += (q - inv['answer']) ** 2
            else:
                require(row['purchased_label'] is None, 'unselected_no_current_label')
                shift -= q * (1 - q)
            terms = ((q*q, 1-2*q), (F(0), F(0)) if selected else (q, 1-2*q), (F(a), F(1-2*a)))
            for j, name in enumerate(('F', 'V', 'Z')):
                c, b = terms[j]
                constant[name] += c + (b * known[key] if key in known else 0)
                if key not in known:
                    coefficients[key][j] += b
        unknown = sorted(all_keys - known.keys())
        vectors = [(coefficients[k][0], coefficients[k][2]) for k in unknown]
        origin = (constant['F'], constant['Z'])
        require(all(coefficients[k][0] == coefficients[k][1] for k in unknown)
                and constant['F'] - constant['V'] == shift, 'public_affine_identity', uid)
        same(observed['unresolved_full_keys'], unknown, [uid, 'unknown_keys'])
        same(observed['unresolved_key_vectors'], vectors, [uid, 'vectors'])
        same(observed['public_origin'], origin, [uid, 'origin'])
        same(observed['F_minus_V_public_shift'], shift, [uid, 'shift'])
        same(observed['paid_known_keys'], len(known), [uid, 'known_keys'])
        same(observed['horizon'], horizon, [uid, 'horizon'])
        require(len(unknown) == earlier['unresolved_distinct_keys'], 'prior_key_denominator', uid)

        hull = minkowski_hull(origin, vectors)
        actual_vertices = [tuple(map(rat, p)) for p in observed['polygon']['vertices']]
        require(len(actual_vertices) == len(set(actual_vertices)), 'distinct_saved_vertices', uid)
        same(encode(cyclic_origin(actual_vertices)), hull, [uid, 'independent_monotone_chain_hull'])
        nonzero = [b for b in vectors if b != (0, 0)]
        directions_unoriented = {(1, b[1] / b[0]) if b[0] else (0, F(1)) for b in nonzero}
        m = len(directions_unoriented)
        dimension = 0 if len(hull) == 1 else 1 if len(hull) == 2 else 2
        require(dimension == (0 if m == 0 else 1 if m == 1 else 2), 'independent_dimension', uid)
        require(len(hull) == max(1, 2*m), 'independent_vertex_count', uid)
        # The planar zonotope area is the sum of absolute pairwise generator determinants.
        area = sum((abs(cross(a, b)) for i, a in enumerate(vectors) for b in vectors[:i]), F(0))
        hull_area = sum((cross(p, hull[(i+1) % len(hull)]) for i, p in enumerate(hull)), F(0))/2
        require(area == hull_area, 'pairwise_determinant_area', uid)
        for field, value in [('dimension', dimension), ('nonparallel_directions', m), ('area', area)]:
            same(observed['polygon'][field], value, [uid, field])
        masks = observed['polygon']['binary_witness_masks']
        require(len(masks) == len(actual_vertices), 'witness_roster', uid)
        for p, mask in zip(actual_vertices, masks):
            bits = int(mask, 16)
            require(0 <= bits < (1 << len(vectors)), 'witness_index_domain', uid)
            represented = (origin[0] + sum((v[0] for i, v in enumerate(vectors) if (bits >> i) & 1), F(0)),
                           origin[1] + sum((v[1] for i, v in enumerate(vectors) if (bits >> i) & 1), F(0)))
            require(represented == p, 'independent_binary_vertex_witness', uid)
        diagnostics = {(F(a), F(b)) for a in range(-2, 3) for b in range(-2, 3) if a or b}
        for i, point in enumerate(hull):
            edge = minus(hull[(i+1) % len(hull)], point)
            if edge != (0, 0):
                diagnostics |= {(-edge[1], edge[0]), (edge[1], -edge[0])}
        for direction in diagnostics:
            projected = [dot(p, direction) for p in hull]
            require(support(origin, vectors, direction) == (min(projected), max(projected)),
                    'independent_support_value', [uid, encode(direction)])
        same(observed['nonaxis_support_checks'], len(diagnostics), [uid, 'misnamed_total_diagnostic_directions'])
        axis_count = sum(d[0] == 0 or d[1] == 0 for d in diagnostics)
        f_bounds, z_bounds = support(origin, vectors, (1, 0)), support(origin, vectors, (0, 1))
        bounds = {'F': f_bounds, 'V': tuple(x-shift for x in f_bounds), 'Z': z_bounds}
        same(observed['marginals'], bounds, [uid, 'marginals'])
        for name, bound in bounds.items():
            same([earlier['endpoints'][name]['public_only_lower'], earlier['endpoints'][name]['public_only_upper']],
                 bound, [uid, 'earlier_' + name + '_bounds'])
        corners = []
        for fi, flabel in enumerate(('lower', 'upper')):
            for zi, zlabel in enumerate(('lower', 'upper')):
                conflicts = []
                for index, (bf, bz) in enumerate(vectors):
                    allowed = {0, 1}
                    for coefficient, maximize in [(bf, bool(fi)), (bz, bool(zi))]:
                        if coefficient:
                            endpoint = int((coefficient > 0) == maximize)
                            allowed &= {endpoint}
                    if not allowed:
                        conflicts.append(index)
                point = (f_bounds[fi], z_bounds[zi])
                compatible = not conflicts
                require(contained(hull, point) == compatible, 'hull_extension_corner_membership', uid)
                corners.append({'F': flabel, 'Z': zlabel, 'point': point,
                                'jointly_attainable_on_key_cube': compatible,
                                'conflicting_unknown_key_indices': conflicts})
        same(observed['rectangle_corners'], corners, [uid, 'corners'])
        rectangle = (f_bounds[1]-f_bounds[0]) * (z_bounds[1]-z_bounds[0])
        ratio = area / rectangle if rectangle else None
        require(0 <= area <= rectangle, 'rectangle_area_domination', uid)
        same(observed['rectangle_area'], rectangle, [uid, 'rectangle_area'])
        same(observed['convex_hull_area_fraction_of_rectangle'], ratio, [uid, 'area_fraction'])

        original = {}
        original['live_center_shift'] = rat(report['live_centers']['F'])-rat(report['live_centers']['V'])
        original['reference_center_shift'] = rat(report['reference_centers']['F'])-rat(report['reference_centers']['V'])
        original['reference_correction_shift'] = rat(report['reference_corrections']['F'])-rat(report['reference_corrections']['V'])
        original['deterministic_endpoint_shifts'] = [rat(report['deterministic_envelopes']['F'][i])-rat(report['deterministic_envelopes']['V'][i]) for i in range(2)]
        original['delivered_endpoint_shifts'] = [rat(report['intervals']['F'][end])-rat(report['intervals']['V'][end]) for end in ('lower', 'upper')]
        require(original['live_center_shift'] == shift, 'original_live_centers_translate_by_C', uid)
        require(original['reference_center_shift'] == shift+original['reference_correction_shift'],
                'original_reference_center_correction_identity', uid)
        require(original['deterministic_endpoint_shifts'] == [shift, shift], 'original_deterministic_envelopes_translate_by_C', uid)
        require(original['delivered_endpoint_shifts'] == [shift, shift], 'original_delivered_F_V_intervals_translate_by_C', uid)
        require(report['intervals']['F']['confidence_conflict'] == report['intervals']['V']['confidence_conflict'],
                'original_F_V_conflict_status_agrees', uid)
        fwidth = rat(report['intervals']['F']['upper'])-rat(report['intervals']['F']['lower'])
        vwidth = rat(report['intervals']['V']['upper'])-rat(report['intervals']['V']['lower'])
        require(fwidth == vwidth, 'original_F_V_delivered_widths_equal', uid)
        if original['reference_center_shift'] == shift:
            COUNTS['reference_center_shift_also_equals_C'] += 1
        else:
            COUNTS['reference_center_shift_differs_from_C_by_recorded_correction'] += 1

        r = {'unit_id': uid, 'group_id': unit['group_id'], 'family': group_map[unit['group_id']]['recipe']['family'],
             'configuration_id': unit['configuration_id'], 'selector': unit['parameters']['selector'], 'seed': unit['seed'],
             'status': 'available', 'horizon': horizon, 'paid_known_keys': len(known), 'unresolved_distinct_keys': len(unknown),
             'nonzero_generators': len(nonzero), 'dimension': dimension, 'nonparallel_directions': m,
             'vertices': len(hull), 'canonical_hull_sha256': digest(canonical(hull)),
             'unknown_key_and_vector_sha256': digest(canonical([unknown, vectors])),
             'public_origin': origin, 'F_minus_V_public_shift': shift, 'marginals': bounds,
             'polygon_area': area, 'rectangle_area': rectangle, 'convex_hull_area_fraction_of_rectangle': ratio,
             'rectangle_corners': corners, 'total_diagnostic_direction_vectors': len(diagnostics),
             'axis_diagnostic_direction_vectors': axis_count,
             'nonaxis_diagnostic_direction_vectors': len(diagnostics)-axis_count,
             'original_F_V_report_translation': original}
        records.append(r)
        cache[uid] = {'rows': rows, 'keys': rowkeys, 'known': known, 'unknown': unknown, 'vectors': vectors,
                      'origin': origin, 'hull': hull, 'public_ref': ref}
        COUNTS.update(parents=1, positions=horizon, selected_receipts=len(invoices),
                      unresolved_key_instances=len(unknown), retained_polygon_vertices=len(hull),
                      diagnostic_direction_vectors=len(diagnostics), axis_direction_vectors=axis_count,
                      nonaxis_direction_vectors=len(diagnostics)-axis_count,
                      incompatible_rectangle_corners=sum(not x['jointly_attainable_on_key_cube'] for x in corners))

    groups = defaultdict(list)
    for r in records:
        groups[(r['family'], r['configuration_id'])].append(r)
    reconstructed_summaries = []
    for (family, config), rs in sorted(groups.items()):
        pops = defaultdict(list)
        for r in rs:
            pops[r['group_id']].append(r)
        require(len(rs) == 6 and len(pops) == 2 and all(len(x) == 3 and len({r['seed'] for r in x}) == 3 for x in pops.values()),
                'six_parent_hierarchical_cell', [family, config])
        def mean(field):
            return sum((sum((r[field] for r in pop), F(0))/len(pop) for pop in pops.values()), F(0))/len(pops)
        reconstructed_summaries.append({'family': family, 'configuration_id': config,
            'scheduled_reports': len(rs), 'available_reports': len(rs),
            'dimensions': dict(Counter(str(r['dimension']) for r in rs)),
            'reports_with_incompatible_rectangle_corners': sum(any(not c['jointly_attainable_on_key_cube'] for c in r['rectangle_corners']) for r in rs),
            'incompatible_corner_counts': dict(Counter(str(sum(not c['jointly_attainable_on_key_cube'] for c in r['rectangle_corners'])) for r in rs)),
            'mean_convex_hull_area_fraction_of_rectangle': mean('convex_hull_area_fraction_of_rectangle'),
            'mean_F_minus_V_shift': mean('F_minus_V_public_shift'),
            'weighting': 'equal scheduled seeds within population, then equal populations',
            'unit_ids': [r['unit_id'] for r in rs]})
    require(len(reconstructed_summaries) == 21, '21_family_configuration_cells')
    same(principal['summaries'], reconstructed_summaries, 'all_hierarchical_summaries')

    coupled = defaultdict(list)
    for r in records:
        coupled[(r['group_id'], r['seed'], r['selector'])].append(r)
    coupled_summary = []
    for k, rs in sorted(coupled.items()):
        expected = 4 if k[2] == 'uniform' else 3
        require(len(rs) == expected and len({r['unknown_key_and_vector_sha256'] for r in rs}) == 1,
                'same_unknown_geometry_across_coupled_configurations', k)
        require(len({r['convex_hull_area_fraction_of_rectangle'] for r in rs}) == 1,
                'coupled_geometry_ratio_identity', k)
        coupled_summary.append({'group_id': k[0], 'seed': k[1], 'selector': k[2],
            'configuration_count': len(rs), 'area_fraction': rs[0]['convex_hull_area_fraction_of_rectangle'],
            'unit_ids': [r['unit_id'] for r in rs]})
    require(len(coupled_summary) == 36, '36_coupled_geometry_classes')
    public_result = {'status': 'PASS' if not DIFFERENCES else 'MISMATCH', 'reviewer': 'ChatGPT (GPT-6 Astra Pro), /root/certificate_reconstruction',
        'start': START, 'public_reconstruction_complete': stamp(), 'records': records,
        'summaries': reconstructed_summaries, 'coupled_geometry_classes': coupled_summary,
        'counts': dict(COUNTS), 'checks_by_kind': dict(CHECKS), 'mismatch_count': len(DIFFERENCES),
        'mismatches': list(DIFFERENCES), 'source_sha256': digest(Path(__file__).read_bytes()),
        'private_numeric_or_validation_payloads_parsed_before_this_save': 0,
        'investigator_unblinded': True, 'new_truth_generation': False, 'paid_or_frozen_execution': False,
        'principal_research_credit_seconds': 0}
    save(OUT/'public_reconstruction.json', public_result)
    public_hash = digest((OUT/'public_reconstruction.json').read_bytes())

    private_start = stamp()
    validation = read(snap/'joint_report_geometry_observation_A1/validation.json')
    numeric_path = WORK/'reviews/certificate_reconstruction/forecast_mechanism_review_v1/source_and_data/numeric_observation_A1/results.json'
    numeric = read(numeric_path)
    prior_review = read(WORK/'reviews/certificate_reconstruction/forecast_mechanism_review_v1/independent_observation_v1/results.json')
    require(validation['status'] == numeric['status'] == prior_review['status'] == 'PASS', 'existing_private_validation_status')
    require(validation['numeric_source_sha256'] == digest(numeric_path.read_bytes()) ==
            '8f7e34aef5060b43bccb2447f87238c3b3c864c5a2e375d317472827567da82f', 'previously_independently_checked_numeric_pin')
    require(validation['public_geometry_sha256'] == digest((snap/'joint_report_geometry_observation_A1/public_geometry.json').read_bytes()),
            'principal_public_geometry_validation_binding')
    require([r['unit_id'] for r in numeric['per_episode']] == [r['unit_id'] for r in validation['checks']] == ids,
            'complete_private_validation_rosters')
    require(numeric['amendment_lineage'] == principal['amendment_lineage'], 'numeric_lineage_binding')
    require(principal['start']['boot_id'] == principal['public_completion']['boot_id'] == validation['private_start']['boot_id'] == validation['end']['boot_id']
            and principal['start']['monotonic_ns'] < principal['public_completion']['monotonic_ns'] < validation['private_start']['monotonic_ns'] < validation['end']['monotonic_ns'],
            'principal_saved_phase_order')
    num_map = {r['unit_id']: r for r in numeric['per_episode']}
    val_map = {r['unit_id']: r for r in validation['checks']}
    private_checks = []
    for record in records:
        uid = record['unit_id']
        old = cache[uid]
        nrows = [x for b in num_map[uid]['blocks'] for x in b['rows']]
        require(len(nrows) == len(old['rows']) == record['horizon'] and [x['index'] for x in nrows] == list(range(record['horizon'])),
                'existing_numeric_ordered_horizon', uid)
        ys = {}
        f_total, v_total, z_total = F(0), F(0), 0
        for row, nrow, key in zip(old['rows'], nrows, old['keys']):
            y = nrow['truth']
            require(type(y) is int and y in (0, 1) and (key not in ys or ys[key] == y), 'existing_truth_key_consistency', uid)
            ys[key] = y
            if key in old['known']:
                require(y == old['known'][key], 'existing_truth_paid_label_agreement', uid)
            q = rat(row['emitted_q'])
            brier = (q-y)**2
            err = int(row['terminal_action'] != y)
            require(brier == rat(nrow['live_brier']) and err == nrow['live_terminal_error'], 'existing_numeric_row_targets', uid)
            f_total += brier
            z_total += err
            if not row['selected']:
                v_total += q+(1-2*q)*y
        point = (f_total, F(z_total))
        mask = sum(ys[k] << i for i, k in enumerate(old['unknown']))
        represented = (old['origin'][0]+sum((v[0]*ys[k] for k,v in zip(old['unknown'],old['vectors'])),F(0)),
                       old['origin'][1]+sum((v[1]*ys[k] for k,v in zip(old['unknown'],old['vectors'])),F(0)))
        require(represented == point and contained(old['hull'], point), 'actual_saved_truth_binary_image_and_hull_containment', uid)
        require(f_total-v_total == record['F_minus_V_public_shift'], 'actual_saved_truth_affine_identity', uid)
        targets = {'F': f_total, 'V': v_total, 'Z': F(z_total)}
        same(val_map[uid]['targets'], targets, [uid, 'validation_targets'])
        require(val_map[uid]['affine_identity'] is True and val_map[uid]['joint_containment'] is True, 'principal_validation_flags', uid)
        score_path = ROOT/'v3/experiments/final_v1_amended_A1/stages/evaluation/units'/('score-'+uid)/'attempt_01/result.json'
        outer = verified_result(score_path)
        score = outer['value']['score']
        require(outer['value']['public_result_sha256'] == old['public_ref']['result_sha256'], 'score_public_binding', uid)
        require(score['status'] == 'success' and score['validity_pass'] is True and score['full_horizon'] is True,
                'frozen_score_complete', uid)
        require(rat(score['issued_brier_sum']) == f_total and score['terminal_errors'] == z_total, 'frozen_F_Z_targets_agree', uid)
        private_checks.append({'unit_id': uid, 'targets': targets, 'unknown_truth_mask': hex(mask),
                               'binary_relaxed_image': True, 'hull_containment': True, 'F_minus_V_identity': True})
    require(digest((OUT/'public_reconstruction.json').read_bytes()) == public_hash, 'independent_public_artifact_unchanged')
    result = {'status': 'PASS' if not DIFFERENCES else 'MISMATCH', 'start': START, 'end': stamp(),
              'source_sha256': digest(Path(__file__).read_bytes()), 'public_reconstruction_sha256': public_hash,
              'private_validation_start': private_start, 'mismatch_count': len(DIFFERENCES), 'mismatches': DIFFERENCES,
              'records_reconstructed': len(records), 'hierarchical_cells': len(reconstructed_summaries),
              'saved_truth_validations': len(private_checks), 'private_checks': private_checks,
              'counts': dict(COUNTS), 'checks_by_kind': dict(CHECKS),
              'new_truth_generation': False, 'paid_or_frozen_execution': False,
              'principal_research_credit_seconds': 0}
    save(OUT/'results.json', result)
    save(OUT/'source_hashes.json', {'consumed_files': [READS[k] for k in sorted(READS)],
                                   'observer_source': {'path': str(Path(__file__).relative_to(ROOT)),
                                                       'sha256': digest(Path(__file__).read_bytes())}})
    save(OUT/'signature.json', {'reviewer': 'ChatGPT (GPT-6 Astra Pro), /root/certificate_reconstruction',
                               'signed_utc': stamp()['utc'], 'status': result['status'],
                               'output_hashes': {p.name: digest(p.read_bytes()) for p in sorted(OUT.iterdir()) if p.is_file()},
                               'principal_research_credit_seconds': 0})
    print(json.dumps({'status': result['status'], 'records': len(records), 'cells': len(reconstructed_summaries),
                      'mismatches': len(DIFFERENCES), 'counts': dict(COUNTS),
                      'results_sha256': digest((OUT/'results.json').read_bytes())}, sort_keys=True))
except BaseException as error:
    save(OUT/'observer_failure.json', {'status': 'OBSERVER_FAILURE', 'start': START, 'end': stamp(),
         'source_sha256': digest(Path(__file__).read_bytes()), 'error_type': type(error).__name__,
         'error': str(error), 'traceback': traceback.format_exc(), 'checks_completed': dict(CHECKS),
         'mismatches': DIFFERENCES, 'scientific_stage_failure': False,
         'principal_research_credit_seconds': 0})
    save(OUT/'failure_source_hashes.json', {'consumed_files': [READS[k] for k in sorted(READS)]})
    raise
