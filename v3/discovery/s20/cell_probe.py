"""Exhaustive finite support check of decision_cells; no optimizer."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import gzip
import hashlib
import json
import sys
import time
import traceback
from decision_cells import assess, cell_witness

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REPS = ['-1', '0', '1/2', '1', '2']
MATRICES = [
    [['0','1'], ['2','1'], ['0','1'], ['2','1'], ['0','1']],
    [['0','4','2'], ['3','1','2'], ['2','2','0'], ['4','0','2'], ['1','3','2']],
    [['100','101'], ['101','101'], ['101','101'], ['101','101'], ['101','101']],
    [['-2'], ['-1'], ['0'], ['1'], ['2']],
]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def point_union(indices):
    return [[REPS[j], REPS[j]] for j in indices]


def worst(matrix, indices):
    return [max(matrix[j][a] for j in indices) for a in range(len(matrix[0]))]


def main():
    destination = HERE/'cell_runs'/sys.argv[1]
    destination.mkdir(parents=True, exist_ok=False)
    freeze_path = HERE/'cell_freeze.json'
    freeze = json.loads(freeze_path.read_text())
    for name, expected in freeze['sha256'].items():
        assert sha(ROOT/name) == expected, name
    (destination/'freeze.json').write_bytes(freeze_path.read_bytes())
    started = time.perf_counter_ns()
    counts = dict(brackets=0, action_bounds=0, optimal_certificates=0,
                  discarded_cells=0, relevance_witnesses=0)
    try:
        for costs in MATRICES:
            for criterion in ('loss','regret'):
                matrix = [list(map(F, row)) for row in costs]
                if criterion == 'regret':
                    matrix = [[v-min(row) for v in row] for row in matrix]
                for states in product(range(4), repeat=5):
                    inner = [j for j, s in enumerate(states) if s == 3]
                    actual = [j for j, s in enumerate(states) if s >= 2]
                    outer = [j for j, s in enumerate(states) if s >= 1]
                    if not actual:
                        continue
                    result = assess(dict(inner=point_union(inner), outer=point_union(outer)),
                                    ['0','1'], costs, criterion)
                    assert result['known_cells'] == inner and result['possible_cells'] == outer
                    true = worst(matrix, actual)
                    lo, hi, eta = [list(map(F, result[key])) for key in
                                   ('lower','upper','improvement_bounds')]
                    for a, value in enumerate(true):
                        assert lo[a] <= value <= hi[a]
                        assert 0 <= value-min(true) <= eta[a]
                        counts['action_bounds'] += 1
                    assert result['conservative_action'] == min(range(len(hi)), key=lambda a:(hi[a],a))
                    assert result['smallest_gap_action'] == min(range(len(eta)), key=lambda a:(eta[a],a))
                    for a in result['certified_optimal_actions']:
                        assert true[a] == min(true)
                        counts['optimal_certificates'] += 1
                    discarded = result['irrelevant_unknown_cells']
                    if discarded:
                        reduced = [j for j in actual if j not in discarded]
                        assert reduced and worst(matrix,reduced) == true
                        counts['discarded_cells'] += len(discarded)
                    if inner:
                        old = worst(matrix,inner)
                        for j in set(outer)-set(inner)-set(discarded):
                            assert worst(matrix,inner+[j]) != old
                            counts['relevance_witnesses'] += 1
                    counts['brackets'] += 1
        # Boundary truth is independent of midpoint selection in the implementation.
        cuts = [F(0),F(1)]
        examples = [([(F(0),F(0))], {1}), ([(F(1),F(1))],{3}),
                    ([(F(0),F(1))],{1,2,3}), ([(F(-1),F(2))],set(range(5))),
                    ([(F(1,3),F(1,3))],{2}), ([],set())]
        for ranges, expected in examples:
            got = {j for j in range(5) if cell_witness(ranges,cuts,j) is not None}
            assert got == expected
            for j in got:
                q = cell_witness(ranges,cuts,j)
                assert any(a <= q <= b for a,b in ranges)
                assert (j == 0 and q < 0) or (j == 1 and q == 0) or (j == 2 and 0 < q < 1) or (j == 3 and q == 1) or (j == 4 and q > 1)
        valid = dict(inner=[],outer=[['0','1']])
        bad_calls = [
            lambda: assess(valid,['1','0'],MATRICES[0]),
            lambda: assess(valid,['0','0'],MATRICES[0]),
            lambda: assess(valid,['0','1'],MATRICES[0],'unspecified'),
            lambda: assess(valid,['0','1'],[['0']]),
            lambda: assess(valid,['0','1'],[[],[],[],[],[]]),
            lambda: assess(dict(inner=[['-1','-1']],outer=[['0','1']]),['0','1'],MATRICES[0]),
            lambda: assess(dict(inner=[],outer=[['1','0']]),['0','1'],MATRICES[0]),
            lambda: assess(dict(inner=[],outer=[['0','1'],['1','2']]),['0','1'],MATRICES[0]),
        ]
        rejections = []
        for operation in bad_calls:
            try: operation()
            except ValueError as e: rejections.append(str(e))
            else: raise AssertionError('invalid input accepted')
        assert assess(dict(inner=[],outer=[]),['0','1'],MATRICES[0])['status'] == 'INCONSISTENT_BRACKET'
        # Load already exposed partial-service evidence. No new service or LP run.
        with gzip.open(HERE/'partial_runs/a01/records.jsonl.gz','rt',encoding='utf-8') as f:
            rows = [json.loads(line) for line in f]
        box = [r for r in rows if r.get('name') == 'noisy_envelope' and r.get('step') == 'box'][-1]
        # Closed hazardous band includes its singleton endpoints.
        costs = [['0','1'],['10','1'],['10','1'],['10','1'],['0','1']]
        example = assess(box['bracket'],['-5/4','-6/5'],costs)
        assert example['certified_optimal_actions'] == [0]
        assert example['improvement_bounds'][0] == '0'
        result = dict(status='PASS', label='DEVELOPMENT; finite supports; no statistical calibration',
                      counts=counts, endpoint_controls=len(examples), rejections=rejections,
                      noisy_example=example, new_optimizer_calls=0,
                      elapsed_ns=time.perf_counter_ns()-started,freeze_sha256=sha(freeze_path))
        (destination/'result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(result))
    except BaseException:
        (destination/'failure.txt').write_text(traceback.format_exc(),encoding='utf-8')
        raise


if __name__ == '__main__':
    main()
