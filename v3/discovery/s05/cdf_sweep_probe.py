"""Source-bound development of the exact CDF sweep; no new truth purchases."""
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform
import random
import sys
import time

import scipy

from cdf_sweep import CDFSweep, verify_minimum
from threshold_queries import CDFValues


def run(destination):
    if destination.exists():
        raise FileExistsError('Choose a new result path; prior evidence is immutable')
    here = Path(__file__).resolve().parent
    previous = here/'threshold_query_results.json'
    bank = json.loads(previous.read_text())
    started = time.perf_counter_ns()
    paid, generated, scaling = [], [], []
    sweep_ns = verification_ns = lp_ns = preparation_ns = 0
    for row in bank['rows']:
        prep = time.perf_counter_ns()
        source = CDFSweep(row['lower_cdf'], row['upper_cdf'])
        preparation_ns += time.perf_counter_ns()-prep
        reference = CDFValues(row['lower_cdf'], row['upper_cdf'])
        for name, g in bank['query_definitions'].items():
            start = time.perf_counter_ns()
            answer = source.interval(g)
            sweep_ns += time.perf_counter_ns()-start
            start = time.perf_counter_ns()
            assert verify_minimum(source, g, answer['lower_certificate'])
            assert verify_minimum(source, [-v for v in g], answer['negative_upper_certificate'])
            verification_ns += time.perf_counter_ns()-start
            start = time.perf_counter_ns()
            check = reference.interval(g)
            lp_ns += time.perf_counter_ns()-start
            assert check['minimum_certificate']['exact_optimality']
            assert check['negative_minimum_certificate']['exact_optimality']
            assert (answer['lower'], answer['upper']) == (check['lower'], check['upper'])
            prior = row['outputs'][name]
            assert (answer['lower'], answer['upper']) == (prior['lower'], prior['upper'])
            paid.append(dict(mode=row['mode'], stage=row['stage'], query=name, answer=answer))

    seed = 261012193
    rng = random.Random(seed)
    for size in (1, 2, 3, 5, 8, 13, 21):
        for variant in range(6):
            if size == 1:
                lo, hi = [], []
            elif variant == 0:
                lo, hi = [F(0)]*(size-1), [F(1)]*(size-1)
            else:
                c1 = sorted(F(rng.randrange(0, 41), 40) for _ in range(size-1))
                c2 = sorted(F(rng.randrange(0, 41), 40) for _ in range(size-1))
                lo = list(map(min, zip(c1, c2)))
                hi = list(map(max, zip(c1, c2)))
                if variant == 1:
                    hi = lo[:]
            g = [F(rng.randrange(-20, 21), rng.choice((1, 2, 3))) for _ in range(size)]
            source = CDFSweep(lo, hi)
            answer = source.interval(g)
            assert verify_minimum(source, g, answer['lower_certificate'])
            assert verify_minimum(source, [-v for v in g], answer['negative_upper_certificate'])
            # The previous LP adapter requires a nonempty cut list. The
            # single-support case has the exact direct reference g[0].
            if size == 1:
                assert answer['lower'] == answer['upper'] == str(g[0])
            else:
                check = CDFValues(lo, hi).interval(g)
                assert check['minimum_certificate']['exact_optimality']
                assert check['negative_minimum_certificate']['exact_optimality']
                assert (answer['lower'], answer['upper']) == (check['lower'], check['upper'])
            generated.append(dict(size=size, variant=variant,
                                  lower=list(map(str, lo)), upper=list(map(str, hi)),
                                  payoff=list(map(str, g)), answer=answer))

    for size in (128, 512, 2048):
        lo = [max(F(0), F(j+1, size)-F(1, 10)) for j in range(size-1)]
        hi = [min(F(1), F(j+1, size)+F(1, 10)) for j in range(size-1)]
        prep = time.perf_counter_ns()
        source = CDFSweep(lo, hi)
        prep_elapsed = time.perf_counter_ns()-prep
        g = [F((j*7919) % 101-50, 7) for j in range(size)]
        start = time.perf_counter_ns()
        answer = source.interval(g, certificate=False)
        elapsed = time.perf_counter_ns()-start
        # Source arrays and deterministic payoff formula fully reconstruct
        # these larger examples; store a digest rather than repeat all masses.
        probs = [answer[k]['probability'] for k in ('lower_certificate','negative_upper_certificate')]
        digest = hashlib.sha256(json.dumps(probs, separators=(',', ':')).encode()).hexdigest()
        scaling.append(dict(size=size, preparation_ns=prep_elapsed, both_values_ns=elapsed,
                            lower=answer['lower'], upper=answer['upper'], probability_sha256=digest,
                            operations=[answer[k]['operations'] for k in ('lower_certificate','negative_upper_certificate')],
                            recipe='CDF bounds clipped((j+1)/size +/- 1/10); payoff=((7919*j)%101-50)/7'))

    result = dict(status='DEVELOPMENT', contributor='ChatGPT (GPT-6 Astra Pro)',
                  generated_utc=datetime.now(timezone.utc).isoformat(), command=sys.argv,
                  seed=seed, new_truth_purchases=0,
                  sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in [Path(__file__), here/'cdf_sweep.py', here/'threshold_queries.py', previous]},
                  environment=dict(python=platform.python_version(), scipy=scipy.__version__),
                  exact_paid_endpoints=2*len(paid), generated_endpoints=2*len(generated),
                  paid_preparation_ns=preparation_ns, paid_sweep_ns=sweep_ns,
                  paid_direct_range_check_ns=verification_ns, paid_lp_and_rational_check_ns=lp_ns,
                  wall_ns=time.perf_counter_ns()-started,
                  scope='Exposed development. The comparison is the existing SciPy plus rational-certificate adapter in this runtime, not an optimized p-box algorithm. Same paid source and exact CDF endpoints; acquisition cost remains inherited.',
                  paid=paid, generated=generated, scaling=scaling)
    destination.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('paid','generated','sources')}))


if __name__ == '__main__':
    run(Path(sys.argv[1]))
