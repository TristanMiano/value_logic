"""Exact early-stop and count-coloring screen; Codex (GPT-6), DEVELOPMENT."""
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
small, colorings = [], 0
for g in range(1, 12, 2):
    h, m = g+1, g//2
    gain = F(g,2)*F(math.comb(g-1,m),2**(g-1))
    expected = F(2*g+3,2)-2*gain
    counts = errors = padding = 0
    for x in range(2**g):
        votes = [0,0]
        for j in range(g):
            b = (x >> j) & 1
            votes[b] += 1
            if votes[b] == m+1:
                tau, majority = j+1, b
                break
        extra = int(tau % 2 != majority)
        invoice = tau+extra
        assert invoice <= h and invoice % 2 == int(x.bit_count()>m)
        estimate = 2**g-1 if invoice % 2 else 0
        errors += (x^estimate).bit_count()
        counts += invoice
        padding += extra
    assert F(counts,2**g) == expected
    assert F(padding,2**g) == F(1,2)
    assert F(errors,2**g) == F(g,2)-gain
    # Independent enumeration of all public majority labels on count values.
    best = None
    feasible = 0
    for labels in range(2**h):
        cost = F(0)
        valid = True
        for t in range(m+1,g+1):
            one_sign_mass = F(math.comb(t-1,m),2**t)
            for b in (0,1):
                legal = [q for q in range(t,h+1) if (labels>>(q-1))&1 == b]
                if not legal:
                    valid = False
                    break
                cost += one_sign_mass*min(legal)
            if not valid:
                break
        colorings += 1
        if valid:
            feasible += 1
            best = cost if best is None else min(best,cost)
    assert best == expected
    small.append({'g':g, 'worlds':2**g, 'feasible_colorings':feasible,
                  'optimal_mean_queries':expected})

panels=[]
for power in (6,7,8,10):
    h=2**power
    g=h-1
    gain=F(g,2)*F(math.comb(g-1,g//2),2**(g-1))
    q=F(2*g+3,2)-2*gain
    threshold=(q-2*gain)/(2*gain/power-1)
    rows=[]
    for fee in (100,1000,10000):
        candidate=q+fee
        lower=2*gain*(1+F(fee,power))
        saving=1-candidate/lower
        assert (saving>0)==(fee>threshold)
        rows.append({'reset_fee':fee, 'candidate_fee_per_block':candidate,
                     'affine_fee_lower_bound':lower, 'saving_fraction':saving,
                     'saving_percent_float':100*float(saving)})
    panels.append({'cap':h,'g':g,'mean_queries':q,'mean_queries_float':float(q),
                   'distortion_fraction':F(1,2)-gain/g,
                   'distortion_float':float(F(1,2)-gain/g),
                   'threshold':threshold,'threshold_float':float(threshold),
                   'comparisons':rows})
result={'status':'PASS','contributor':'Codex (GPT-6)',
        'scope':'tiny exact majority/count-coloring screen and exact formula evaluation',
        'started_utc':started,'ended_utc':datetime.now(timezone.utc).isoformat(),
        'small':small,'count_colorings_examined':colorings,'panels':panels,
        'ordinary_equivalent':'identical ordinary early-majority decoder ties',
        'complete_cost_or_cpu_gain':False,'elapsed_ns':time.perf_counter_ns()-clock,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
out.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'count_colorings':colorings,'small':small,
                  'panels':[{'cap':p['cap'],'mean_queries':p['mean_queries_float'],
                             'distortion':p['distortion_float'],'threshold':p['threshold_float'],
                             'comparisons':[{'reset':r['reset_fee'],'saving_percent':r['saving_percent_float']}
                                            for r in p['comparisons']]}
                            for p in panels], 'elapsed_ns':result['elapsed_ns'],
                  'source_sha256':result['source_sha256']},indent=2,default=str))
