"""DEVELOPMENT screen of local edge/entropy charging, Codex (GPT-6).

Generates legal cap-three invoice maps directly. Float logarithms only screen
the mathematical inequality; they are not an exact all-size proof.
"""
from pathlib import Path
from datetime import datetime, timezone
from itertools import product
from math import log2
import hashlib
import json
import platform
import random
import sys
import time

HERE = Path(__file__).resolve().parent
OUT = HERE/'vector_probe.json'
assert not OUT.exists()
start = time.perf_counter_ns()
started = datetime.now(timezone.utc).isoformat()

def invoice_maps(n):
    """Count 3 uses a distinct last marker, whose answer is discarded."""
    worlds = range(1 << n)
    maps = set()
    for i in range(n):
        options = [tuple([1]*(1 << n))]
        for j in range(n):
            if j == i:
                continue
            for outputs in product((2, 3), repeat=2):
                options.append(tuple(outputs[(x >> j) & 1] for x in worlds))
        options = set(options)
        for left, right in product(options, repeat=2):
            maps.add(tuple((right if (x >> i) & 1 else left)[x] for x in worlds))
    return sorted(maps)

def edges(mask, n):
    return sum(bool(mask & (1 << x)) and bool(mask & (1 << (x ^ (1 << i))))
               for x in range(1 << n) for i in range(n) if not (x >> i) & 1)

rng = random.Random(22014)
results = []
total = 0
for n in (3, 4):
    maps = invoice_maps(n)
    cells = [tuple(sum(1 << x for x, t in enumerate(m) if t == c)
                   for c in (1, 2, 3)) for m in maps]
    sources = list(range(1, 1 << (1 << n))) if n == 3 else sorted({
        (1 << (1 << n))-1, *[rng.randrange(1, 1 << (1 << n)) for _ in range(256)]})
    edge_counts = {w: edges(w, n) for w in range(1 << (1 << n))}
    worst_margin = float('inf')
    for w in sources:
        size = w.bit_count()
        initial_edges = edge_counts[w]
        for masks in cells:
            parts = [w & mask for mask in masks]
            sizes = [p.bit_count() for p in parts]
            crossed = initial_edges-sum(edge_counts[p] for p in parts)
            entropy_mass = size*log2(size)-sum(s*log2(s) for s in sizes if s)
            query_mass = sum(t*s for t, s in enumerate(sizes, 1))
            for f in (0.5, 1, 3, 10, 100):
                a, b = (8+2*f)/3, (2*f-1)/6
                margin = query_mass+f*size-a*crossed-b*entropy_mass
                assert margin >= -1e-9, (n, w, masks, f, margin)
                worst_margin = min(worst_margin, margin)
                total += 1
    results.append(dict(n=n, maps=len(maps), sources=len(sources),
                        minimum_float_margin=worst_margin))

result = dict(status='PASS', label='DEVELOPMENT, same-model finite screen',
              contributor='Codex (GPT-6)', started_utc=started,
              ended_utc=datetime.now(timezone.utc).isoformat(),
              runtime_ns=time.perf_counter_ns()-start,
              python=sys.version, platform=platform.platform(),
              source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              local_comparisons=total, panels=results,
              scope='All nonempty n3 sources; fixed-seed n4 sources; cap3 only; float entropy.')
OUT.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8', newline='\n')
print(json.dumps(result, indent=2))
