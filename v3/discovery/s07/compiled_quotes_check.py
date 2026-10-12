#!/usr/bin/env python3
"""New finite equivalence and amortization probes; no old workload replay.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. DEVELOPMENT. The asserted finite
logical source is z1 OR z2, with exact nonnegative objective features. The
two covering singleton masks independently justify every supplied lower.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys
import time

import compiled_quotes as compiled
import lattice_quotes as reference

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 's05'))
from maxsat_repair import Meter


def jsonable(value):
    if isinstance(value, F):
        return value.numerator if value.denominator == 1 else str(value)
    if isinstance(value, dict):
        return {k: jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    return value


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def one(prepared, reference_meter, modes, case):
    before_reference, before_compiled = reference_meter.total, prepared.meter.total
    arguments = {k: case[k] for k in ('masks', 'possible', 'lowers', 'price', 'q', 'tolerance')}
    options = case.get('options', {})
    old = reference.closing_query(modes=modes, meter=reference_meter, **arguments, **options)
    new = prepared.closing_query(**arguments, **options)
    if old != new:
        raise AssertionError(dict(case=case, reference=old, prepared=new))
    return dict(reference_units=reference_meter.total - before_reference,
                compiled_units=prepared.meter.total - before_compiled,
                status=old['status'], closes=old['closes'], before=old['before'],
                canonical_budget=old.get('canonical_budget'),
                quoted_bound=None if old.get('quote') is None else old['quote']['worst_bound'])


def equivalence_grid():
    families = [
        dict(name='integer_two_features', modes=[[1, 3], [3, 1], [2, 2]], n=2,
             contexts=[dict(masks=[1], possible=[(0, 1, 2), (0, 1, 2)], factor=1, price=7),
                       dict(masks=[1, 2], possible=[(0,), (0, 1, 2)], factor=F(1, 2), price=5),
                       dict(masks=[1, 1, 3], possible=[(0, 1, 2), (0,)], factor=F(1, 2), price=5),
                       dict(masks=[], possible=[(1, 2), (0, 2)], factor=0, price=3),
                       dict(masks=[3, 1], possible=[(2,), (2,)], factor=1, price=8),
                       dict(masks=[1, 2], possible=[(2, 1, 0), (2, 0)], factor=1, price=0)],
             objectives=[[0, 0], [1, 1], [2, 2], [3, 3], [1, 3], [7, 7]]),
        dict(name='rational_three_features', modes=[[F(1, 2), F(3, 2), 0],
                                                  [F(3, 2), F(1, 2), 2], [1, 1, F(1, 2)]], n=3,
             contexts=[dict(masks=[1, 2, 5], possible=[(0, 1, 2)] * 3, factor=1, price=5),
                       dict(masks=[1], possible=[(0,), (1,), (0, 2)], factor=F(1, 3), price=3),
                       dict(masks=[2, 3], possible=[(2,), (1, 2), (0, 1)], factor=1, price=7)],
             objectives=[[0, 0, 0], [1, 1, 1], [2, 2, 2], [3, 3, 0], [2, 4, 6], [8, 8, 8]]),
    ]
    results = []
    for family in families:
        old_meter, new_meter = Meter(), Meter()
        prepared = compiled.PreparedQuotes(family['modes'], family['n'], new_meter)
        setup = new_meter.total
        exact_lowers = [family['n'] * min(v[0], v[1]) for v in family['modes']]
        records = []
        for context_index, context in enumerate(family['contexts']):
            for q in family['objectives']:
                for tolerance in (0, F(1, 2), 2):
                    case = dict(masks=context['masks'], possible=context['possible'],
                                lowers=[context['factor'] * ell for ell in exact_lowers],
                                price=context['price'], q=q, tolerance=tolerance)
                    record = one(prepared, old_meter, family['modes'], case)
                    records.append(dict(context=context_index, q=q, tolerance=tolerance, **record))
        # Explicit optional semantic branches: unresolved results, exact
        # canonical interval reconstruction, and a genuinely feasible upper.
        for options in (dict(complete=False), dict(exact_interval=True),
                        dict(known_query_upper=2), dict(exact_interval=True, known_query_upper=2)):
            q = [2] * len(family['modes'][0])
            case = dict(masks=[1, 2], possible=[tuple(range(3))] * family['n'],
                        lowers=exact_lowers, price=7, q=q, tolerance=2, options=options)
            # The actually available feasible mask 1 has q-cost exactly 2.
            record = one(prepared, old_meter, family['modes'], case)
            records.append(dict(options=options, **record))
        before_storage_report = new_meter.total
        storage = prepared.storage()
        results.append(dict(family=family, exact_source_lowers=exact_lowers,
                            cases=len(records), compiled_setup_units=setup,
                            reference_units=old_meter.total, compiled_units=before_storage_report,
                            compiled_storage_report_units=new_meter.total - before_storage_report,
                            stats=prepared.stats, storage=storage, records=records,
                            reference_invoice=old_meter.record(), compiled_invoice=new_meter.record()))
    return results


def closing_interval_cases():
    modes = [[1, 3], [3, 1]]
    old_meter, new_meter = Meter(), Meter()
    prepared = compiled.PreparedQuotes(modes, 1, new_meter)
    case = dict(masks=[3], possible=[(0, 1)], lowers=[1, 1], price=8,
                q=[3, 3], tolerance=2)
    records = []
    for options in ({}, dict(exact_interval=True), dict(known_query_upper=6),
                    dict(exact_interval=True, known_query_upper=6), dict(complete=False)):
        actual = case | dict(options=options)
        record = one(prepared, old_meter, modes, actual)
        assert record['closes'] == options.get('complete', True)
        assert record['canonical_budget'] == 3
        records.append(dict(options=options, **record))
    return dict(modes=modes, cohort_size=1, case=case, records=records,
                scope='Actual closing, exact-interval bisection, feasible q-cost upper 6 from mask 3, and unresolved-completion branch',
                reference_invoice=old_meter.record(), compiled_invoice=new_meter.record())


def amortization():
    small_modes = [[1, 3], [3, 1], [2, 2]]
    wide_modes = [[1, 3, 0, 2, 1, 0], [3, 1, 2, 0, 0, 1],
                  [2, 2, 1, 1, 2, 0], [1, 2, 0, 3, 0, 2]]
    small = dict(masks=[1, 2, 3], possible=[(0, 1, 2)] * 2,
                 lowers=[2, 2, 4], price=7, tolerance=2)
    wide = dict(masks=[1, 2, 3, 5], possible=[(0, 1, 2, 3)] * 4,
                lowers=[4, 4, 8, 4], price=12, tolerance=3)
    scenarios = [
        dict(name='trivial_already_closed', modes=[[0]], n=1,
             cases=[dict(masks=[0], possible=[(0,)], lowers=[0], price=0, q=[0], tolerance=0)] * 16,
             purpose='Cold and repeated trivial calls where preparation may never amortize'),
        dict(name='repeated_two_feature_menu', modes=small_modes, n=2,
             cases=[small | dict(q=q) for _ in range(4) for q in
                    ([0, 0], [1, 1], [2, 2], [3, 3], [1, 3], [7, 7])],
             purpose='Shared source/anchor state with six recurring public objectives'),
        dict(name='changing_objectives_and_lowers', modes=small_modes, n=2,
             cases=[small | dict(q=[i + 1, i + 2], lowers=[F(i, 8), F(i, 8), F(i, 4)]) for i in range(16)],
             purpose='Many cold numeric keys; low source-specific lowers are independently valid'),
        dict(name='repeated_six_feature_menu', modes=wide_modes, n=4,
             cases=[wide | dict(q=q) for _ in range(4) for q in
                    ([0] * 6, [1] * 6, [2] * 6, [3] * 6, [4] * 6, [8] * 6)],
             purpose='Larger mode-action arithmetic shared across repeated quotation menus'),
    ]
    result = []
    for scenario in scenarios:
        old_meter, new_meter = Meter(), Meter()
        prepared = compiled.PreparedQuotes(scenario['modes'], scenario['n'], new_meter)
        setup = new_meter.total
        curve, per_call = [], []
        first_cumulative_gain = None
        for index, case in enumerate(scenario['cases'], 1):
            per_call.append(one(prepared, old_meter, scenario['modes'], case))
            if first_cumulative_gain is None and new_meter.total < old_meter.total:
                first_cumulative_gain = index
            if index in (1, 2, 4, 8, 16, len(scenario['cases'])):
                curve.append(dict(calls=index, reference_units=old_meter.total,
                                  compiled_including_setup_units=new_meter.total,
                                  difference=new_meter.total - old_meter.total))
        result.append(dict(name=scenario['name'], purpose=scenario['purpose'],
                           modes=scenario['modes'], cohort_size=scenario['n'], cases=scenario['cases'],
                           calls=len(scenario['cases']), setup_units=setup, curve=curve,
                           first_cumulative_gain_call=first_cumulative_gain,
                           final_reference_units=old_meter.total, final_compiled_units=new_meter.total,
                           difference=new_meter.total - old_meter.total,
                           percent_change=100 * F(new_meter.total - old_meter.total, old_meter.total),
                           per_call=per_call, stats=prepared.stats,
                           reference_invoice=old_meter.record(), compiled_invoice=new_meter.record()))
    return result


def rejections():
    meter = Meter()
    prepared = compiled.PreparedQuotes([[1, 2], [2, 1]], 2, meter)
    good = dict(masks=[1], possible=[(0, 1), (0, 1)], lowers=[2, 2], price=4, q=[2, 2], tolerance=0)
    invalid = [('negative_mode', lambda: compiled.PreparedQuotes([[-1, 2]], 1, meter)),
               ('different_cohort', lambda: prepared.closing_query(**(good | dict(possible=[(0, 1)])))),
               ('empty_source_row', lambda: prepared.closing_query(**(good | dict(possible=[(), (0,)])))),
               ('negative_lower', lambda: prepared.closing_query(**(good | dict(lowers=[-1, 2])))),
               ('wrong_lower_dimension', lambda: prepared.closing_query(**(good | dict(lowers=[2])))),
               ('out_of_range_action', lambda: prepared.closing_query(**(good | dict(masks=[4])))),
               ('fractional_query', lambda: prepared.closing_query(**(good | dict(q=[F(1, 2), 2])))),
               ('negative_query', lambda: prepared.closing_query(**(good | dict(q=[-1, 2]))))]
    records = []
    for name, call in invalid:
        try:
            call()
        except ValueError as exc:
            records.append(dict(case=name, status='rejected', reason=str(exc)))
        else:
            raise AssertionError(f'Invalid compiled quotation accepted: {name}')
    return records


def run(output):
    if output.exists():
        raise FileExistsError('Preserve quotation-compilation evidence')
    wall, cpu = time.perf_counter_ns(), time.process_time_ns()
    grid = equivalence_grid()
    intervals = closing_interval_cases()
    curves = amortization()
    invalid = rejections()
    result = dict(status='passed', evidence='DEVELOPMENT finite exact-correspondence and arithmetic-cost probe',
                  contributor='ChatGPT (GPT-6 Astra Pro)', created_utc=datetime.now(timezone.utc).isoformat(),
                  hashes={p.name: sha(p) for p in [Path(__file__), Path(compiled.__file__), Path(reference.__file__),
                                                 Path(reference.aq.__file__), Path(reference.aq.source_anchor.__file__)]},
                  source_contract='Except the explicitly trivial zero-action source, Boolean z with z1 OR z2 and nonnegative remaining features; singleton masks 1 and 2 cover all feasible repairs and give C*(v)=min(v1,v2). Every tested action has one of the first two bits set; replacement alone is also allowed.',
                  preliminary_screen=dict(cases=1296, exact_output_matches=1296,
                    reference_units=148870, compiled_units=93020,
                    scope='Initial unsaved two-feature arithmetic screen before the saved varied probe; no acquisitions. An initial import-only harness attempt lacked the s05 path and executed no quotation.'),
                  summary=dict(varied_grid_exact_matches=sum(r['cases'] for r in grid),
                               explicit_closing_interval_matches=len(intervals['records']),
                               amortization_exact_matches=sum(r['calls'] for r in curves),
                               admission_rejections=len(invalid)),
                  grids=grid, closing_intervals=intervals, amortization=curves, rejected=invalid,
                  new_LP_SAT_IHS_proof_search_or_audit_calls=0,
                  timing=dict(wall_ns=time.perf_counter_ns() - wall, process_ns=time.process_time_ns() - cpu),
                  accounting='Compiled totals include mode admission, stored numerical words, cache-key work, misses, lookups, arithmetic and output tariffs. Named operation counts use the displayed implementations; they do not establish a CPU, physical-memory or complete-economic advantage. Cold and poor cases are retained.')
    output.write_text(json.dumps(jsonable(result), indent=2) + '\n')
    print(json.dumps(jsonable(dict(status=result['status'], summary=result['summary'],
                     amortization=[{k: s[k] for k in ('name', 'calls', 'final_reference_units', 'final_compiled_units',
                                                      'difference', 'first_cumulative_gain_call')} for s in curves]))))


if __name__ == '__main__':
    run(Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / 'compiled_quotes_results.json')
