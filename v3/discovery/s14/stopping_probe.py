"""Bounded lossy readout screen; Codex (GPT-6), DEVELOPMENT."""
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime, timezone
from itertools import product
import hashlib
import json
import math
import time

out = Path(__file__).with_suffix('.json')
assert not out.exists()
started = datetime.now(timezone.utc).isoformat()
clock = time.perf_counter_ns()


def design(T, ratio):
    a, b = ratio.numerator, ratio.denominator
    values = {s: a*abs(s) for s in range(-T, T+1, 2)}
    policy = {}
    for t in range(T-1, 0, -1):
        scale = 2**(T-t)
        current = {}
        for s in range(-t, t+1, 2):
            stop = a*abs(s)*scale
            cont = -b*scale + values[s-1] + values[s+1]
            policy[t, abs(s)] = stop >= cont
            current[s] = max(stop, cont)
        values = current
    value = F(-b*2**T + values[-1] + values[1], b*2**T)
    return policy, value


def evaluate(T, policy):
    paths = {-1: 1, 1: 1}
    q = h = mass = 0
    for t in range(1, T+1):
        nxt = {}
        for s, count in paths.items():
            if t == T or policy[t, abs(s)]:
                worlds = count*2**(T-t)
                mass += worlds
                q += t*worlds
                h += abs(s)*worlds
            else:
                for new in (s-1, s+1):
                    nxt[new] = nxt.get(new, 0)+count
        paths = nxt
    assert mass == 2**T and not paths
    return F(q, 2**T), F(h, 2**T)


def optimize(T, fee):
    terminal_h = F(T*math.comb(T-1, T//2), 2**(T-1))
    terminal_q = T+1-terminal_h
    ratio = (terminal_q+F(1,2)+fee)/terminal_h
    sequence = []
    for iteration in range(100):
        policy, value = design(T, ratio)
        q, h = evaluate(T, policy)
        assert value == ratio*h-q
        new = (q+F(1,2)+fee)/h
        sequence.append(float(new))
        assert new <= ratio
        if new == ratio:
            assert value == fee+F(1,2)
            return policy, q, h, ratio, sequence
        ratio = new
    raise AssertionError('Finite-policy optimization exceeded cheap screen budget')


brute = []
world_checks = 0
for T in (1,3,5):
    states = sorted({(t,abs(s)) for t in range(1,T)
                     for s in range(-t,t+1,2)})
    for fee in (0,1,10):
        best = None
        for flags in product((False,True), repeat=len(states)):
            q,h = evaluate(T, dict(zip(states,flags)))
            candidate = (q+F(1,2)+fee)/h
            best = candidate if best is None else min(best,candidate)
        policy,q,h,ratio,sequence = optimize(T,fee)
        assert ratio == best
        invoices = errors = padding = 0
        for x in range(2**T):
            s = 0
            for t in range(1,T+1):
                s += 1 if (x>>(t-1))&1 else -1
                if t==T or policy[t,abs(s)]:
                    sign = int(s>0) if s else x&1
                    extra = int(t%2 != sign)
                    invoice = t+extra
                    assert 1<=invoice<=T+1 and invoice%2==sign
                    estimate = 2**T-1 if sign else 0
                    invoices += invoice
                    padding += extra
                    errors += (x^estimate).bit_count()
                    world_checks += 1
                    break
        assert F(invoices,2**T)==q+F(1,2)
        assert F(padding,2**T)==F(1,2)
        assert F(errors,2**T)==(T-h)/2
        brute.append({'T':T,'fee':fee,'policies':2**len(states),
                      'ratio':ratio,'iterations':len(sequence)})

panels = []
for H in (16,64,256):
    T = H-1
    terminal_h = F(T*math.comb(T-1,T//2),2**(T-1))
    terminal_q = T+1-terminal_h
    for fee in (10,100,1000,10000):
        policy,q,h,ratio,sequence = optimize(T,fee)
        old_ratio = (terminal_q+F(1,2)+fee)/terminal_h
        affine_ratio = 1+F(fee,H.bit_length()-1)
        assert ratio <= old_ratio
        panels.append({'cap':H,'block_size':T,'reset_fee':fee,
                       'mean_queries':q+F(1,2),'signed_gain':h,
                       'distortion_fraction':(T-h)/(2*T),
                       'ratio':ratio,'old_majority_ratio':old_ratio,
                       'ratio_reduction_fraction':1-ratio/old_ratio,
                       'all_affine_saving_fraction':1-ratio/affine_ratio,
                       'iterations':len(sequence),'ratio_sequence':sequence,
                       'float_summary':{'mean_queries':float(q+F(1,2)),
                         'distortion':float((T-h)/(2*T)),
                         'ratio_reduction_percent':100*float(1-ratio/old_ratio),
                         'all_affine_saving_percent':100*float(1-ratio/affine_ratio)}})

result = {'status':'PASS','contributor':'Codex (GPT-6)',
          'scope':'exact restricted stopping optimization, tiny brute-force comparison',
          'started_utc':started,'ended_utc':datetime.now(timezone.utc).isoformat(),
          'brute':brute,'world_checks':world_checks,'panels':panels,
          'ordinary_equivalent':'identical Bellman stopping and parity readout ties',
          'complete_cost_or_cpu_gain':False,'elapsed_ns':time.perf_counter_ns()-clock,
          'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
out.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'brute_policies':sum(x['policies'] for x in brute),
                  'world_checks':world_checks,'panels':[{'H':p['cap'],'f':p['reset_fee'],
                    'iterations':p['iterations'],**p['float_summary']} for p in panels],
                  'elapsed_ns':result['elapsed_ns'],'source_sha256':result['source_sha256']},indent=2))
