"""Exact arithmetic of a restricted-class acquisition separation; Codex (GPT-6)."""
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
import time

out = Path(__file__).with_suffix('.json')
assert not out.exists()
started = datetime.now(timezone.utc).isoformat()
clock = time.perf_counter_ns()
small = []
for g in range(1, 12, 2):
    gain = F(g, 2)*F(math.comb(g-1, (g-1)//2), 2**(g-1))
    direct = sum(F(math.comb(g, k), 2**g)*abs(F(k)-F(g,2))
                 for k in range(g+1))
    assert gain == direct
    error = query_mass = 0
    for x in range(2**g):
        majority = int(x.bit_count() > g//2)
        invoice = g+majority
        estimate = (2**g-1) if invoice == g+1 else 0
        error += (x ^ estimate).bit_count()
        query_mass += invoice
    assert F(error, 2**g) == F(g,2)-gain
    assert F(query_mass, 2**g) == F(2*g+1,2)
    small.append({'g': g, 'gain': gain, 'worlds': 2**g})

panels = []
for power in (6, 7, 8, 10):
    cap = 2**power
    g = cap-1
    gain = F(g, 2)*F(math.comb(g-1, (g-1)//2), 2**(g-1))
    coefficient = 2*gain/power-1
    assert coefficient > 0
    threshold = (F(2*g+1,2)-2*gain)/coefficient
    comparisons = []
    for fee in (100, 1000, 10000):
        candidate = F(2*g+1, 2)+fee
        lower = 2*gain*(1+F(fee,power))
        savings = 1-candidate/lower
        assert (savings > 0) == (fee > threshold)
        comparisons.append({'reset_fee': fee, 'majority_fee_per_block': candidate,
                            'affine_fee_lower_bound': lower,
                            'saving_vs_lower_bound_percent_float': 100*float(savings)})
    panels.append({'cap': cap, 'block': g, 'gain_per_block': gain,
                   'expected_hamming_fraction_float': float(F(1,2)-gain/g),
                   'strict_separation_reset_threshold': threshold,
                   'threshold_float': float(threshold), 'comparisons': comparisons})

result = {'contributor': 'Codex (GPT-6)', 'status': 'PASS',
          'scope': 'exact arithmetic and tiny code maps; affine lower bound is a proposed theorem',
          'started_utc': started, 'ended_utc': datetime.now(timezone.utc).isoformat(),
          'small_panels': small, 'panels': panels,
          'ordinary_comparison': 'identical ordinary majority quantizer ties exactly',
          'complete_cost_or_cpu_gain': False,
          'elapsed_ns': time.perf_counter_ns()-clock,
          'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
out.write_text(json.dumps(result, indent=2, default=str)+'\n', encoding='utf-8')
print(json.dumps({**result, 'panels': [
    {k:v for k,v in panel.items() if k not in ('gain_per_block','strict_separation_reset_threshold','comparisons')}
    | {'comparisons': [{'reset_fee': row['reset_fee'],
                       'saving_percent': row['saving_vs_lower_bound_percent_float']}
                      for row in panel['comparisons']]}
    for panel in panels]}, indent=2, default=str))
