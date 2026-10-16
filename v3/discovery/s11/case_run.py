"""Bounded per-case execution amendment; preserve every outcome, no input tuning."""
from pathlib import Path
import argparse
import hashlib
import json
import random
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--case', type=int)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    if args.case is not None:
        from potential_probe import fixtures, random_model, evaluate
        rng = random.Random(20261015)
        models = list(fixtures()) + [random_model(rng, i) for i in range(20)]
        start = time.perf_counter_ns()
        result = evaluate(models[args.case], 1000 + args.case)
        result['elapsed_ns'] = time.perf_counter_ns() - start
        result['case_index'] = args.case
        result['source_sha256'] = hashlib.sha256((HERE / 'potential_probe.py').read_bytes()).hexdigest()
        with args.out.open('x', encoding='utf-8', newline='\n') as f:
            f.write(json.dumps(result, indent=2) + '\n')
        return
    args.out.mkdir(exist_ok=False)
    results = []
    for i in range(25):
        passed = False
        for attempt in range(3):
            name = f'c{i:02d}a{attempt}'
            output = args.out / (name + '.json')
            log = args.out / (name + '.log')
            start = time.perf_counter_ns()
            try:
                with log.open('xb') as f:
                    run = subprocess.run([sys.executable, '-X', 'utf8', str(Path(__file__)), '--case', str(i), '--out', str(output)], stdout=f, stderr=f, timeout=15)
                code = run.returncode
            except subprocess.TimeoutExpired:
                code = 'timeout_15_seconds'
            record = {'case': i, 'attempt': attempt, 'returncode': code, 'elapsed_ns': time.perf_counter_ns()-start,
                      'log': log.name, 'output': output.name if output.exists() else None}
            with (args.out / 'attempts.jsonl').open('a', encoding='utf-8', newline='\n') as f:
                f.write(json.dumps(record) + '\n')
            print(json.dumps(record), flush=True)
            if code == 0 and output.exists():
                results.append(json.loads(output.read_text(encoding='utf-8')))
                passed = True
                break
        if not passed:
            print('Case incomplete; continue other declared cases without replacing it.', flush=True)
    summary = {'schema': 's11_pc01_per_case_amendment', 'expected_cases': 25, 'completed_cases': len(results),
               'case_ids': [r['case_index'] for r in results], 'cases': results,
               'exact_recursion_checks': sum(r['exact_recursion_checks'] for r in results),
               'source_sha256': hashlib.sha256((HERE / 'potential_probe.py').read_bytes()).hexdigest()}
    (args.out / 'summary.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8', newline='\n')
    if len(results) != 25:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
