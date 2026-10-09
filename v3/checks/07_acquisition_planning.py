"""Bounded ordinary acquisition planning; exact stipulated-law DEVELOPMENT.

A fixed prior on two service completion laws is an explicit assumption. This
program computes, rather than assumes, the value of at most twelve observations.
It charges a declared bounded arithmetic/table tariff; not Python CPU time.
The separate forward enumeration validates results and is audit instrumentation.
"""
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from fractions import Fraction as F
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sp = importlib.util.spec_from_file_location('_p307_acq_plan_adapter', HERE/'07_computation_adapter.py')
A = importlib.util.module_from_spec(sp); sys.modules[sp.name] = A; sp.loader.exec_module(A)
VERSION = 'p307-bounded-two-law-acquisition-planner-v1.1'
LOW, HIGH = F(9,20), F(11,20)
PRIORS = (F(1,2), F(1,2))
CAPS, HORIZONS, PRICES = (1,12), (128,512,4096,16384), (F(0),F(1,10000),F(1,1000))
MAX_BITS = 256


def canonical(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),default=str).encode('ascii')


def bounded(x):
    if isinstance(x,F):
        assert max(abs(x.numerator).bit_length(), x.denominator.bit_length()) <= MAX_BITS
    elif isinstance(x,int):
        assert abs(x).bit_length() <= MAX_BITS
    else:
        raise TypeError('Exact rational/integer required.')
    return x


@dataclass(frozen=True)
class Plan:
    cap: int
    horizon: int
    unit_price: F
    rows: tuple
    construction_resources: tuple
    source_hashes: tuple
    identity: str
    core_bytes: int

    def row(self,n,s):
        # Exact triangular indexing. This method is used by external auditing;
        # deployed access has the explicitly priced eight-unit lookup contract.
        return self.rows[n*(n+1)//2+s]


def build(cap,horizon,unit_price,meter):
    if type(meter) is not A.Meter:
        raise TypeError('Exact bounded operation meter required.')
    # The admission bundle precedes all supplied model-value inspection.
    meter.pay('admission','fixed_planner_model_admission',96)
    if type(cap) is not int or cap not in CAPS or type(horizon) is not int or horizon not in HORIZONS:
        raise ValueError('Fixed development cap and horizon required.')
    if type(unit_price) is not F:
        raise ValueError('Exact rational resource price required.')
    if max(unit_price.numerator.bit_length(),unit_price.denominator.bit_length())>MAX_BITS:
        raise ValueError('Resource price exceeds bounded comparison domain.')
    if unit_price not in PRICES:
        raise ValueError('Fixed rational resource price required.')
    count=(cap+1)*(cap+2)//2
    words=1024+64*count
    names=('07_computation_adapter.py',Path(__file__).name)
    meter.pay('profile','bounded_registry_file_stat',len(names))
    sizes=[(HERE/n).stat().st_size for n in names]
    assert sum(sizes)<=512000
    meter.pay('profile','planner_source_read_hash_words',2*sum((s+7)//8 for s in sizes))
    hashes=tuple((n,hashlib.sha256((HERE/n).read_bytes()).hexdigest()) for n in names)
    rows=[None]*count
    for n in range(cap,-1,-1):
        for s in range(n+1):
            # Funds all bounded posterior, two-continuation and argmax work
            # before inspecting child values or computing the new state.
            meter.pay_many((('assessment','bounded_bellman_state_bundle',128),
                            ('storage','bounded_state_child_read_and_retention',64)))
            high_weight=11**s*9**(n-s)
            low_weight=9**s*11**(n-s)
            posterior=bounded(F(high_weight,high_weight+low_weight))
            predict=bounded(LOW+(HIGH-LOW)*posterior)
            commit=bounded(horizon*(2*posterior-1)/20)
            stop=max(F(0),commit)
            action='compute' if commit>0 else 'fallback'
            continuation=None
            if n<cap:
                a=rows[(n+1)*(n+2)//2+s+1][3]
                b=rows[(n+1)*(n+2)//2+s][3]
                continuation=bounded(-F(1,2)-16*unit_price+predict*a+(1-predict)*b)
                if continuation>stop:
                    action='acquire';stop=continuation
            rows[n*(n+1)//2+s]=(n,s,action,bounded(stop),posterior,predict,commit,continuation)
    meter.pay_many((('profile','bounded_planner_freeze_validate_hash',2*words),
                    ('storage','bounded_planner_core_retention',words)))
    resources=tuple(meter.by_category[c] for c in A.CATEGORIES)
    core={'version':VERSION,'hypotheses':(LOW,HIGH),'prior':PRIORS,
          'cap':cap,'horizon':horizon,'unit_price':unit_price,
          'attempt_loss_cost':F(1,2),'lookup_units':8,'acquisition_control_units':8,
          'rows':tuple(rows),'source_hashes':hashes,'construction_resources':resources,
          'numeric_cap_bits':MAX_BITS,'word_envelope':words}
    encoded=canonical(core)
    assert len(encoded)<=8*words
    return Plan(cap,horizon,unit_price,tuple(rows),resources,hashes,
                hashlib.sha256(encoded).hexdigest(),len(encoded)),core


def forward_audit(plan,theta):
    """Independent path propagation under one supplied law; no Bellman values.

    It charges no deployed meter because these are exact external validation
    calculations, not observations supplied to the controller.
    """
    frontier={(0,0):F(1)}; terminal=F(0); buy=F(0); attempts=F(0); nodes=0
    for n in range(plan.cap+1):
        next_level=defaultdict(F)
        for (depth,s),mass in frontier.items():
            assert depth==n
            row=plan.row(depth,s);action=row[2];nodes+=1
            if action=='acquire':
                assert n<plan.cap
                attempts+=mass
                next_level[(n+1,s+1)]+=mass*theta
                next_level[(n+1,s)]+=mass*(1-theta)
            else:
                terminal+=mass
                if action=='compute':buy+=mass
                else:assert action=='fallback'
        frontier=dict(next_level)
    assert not frontier and terminal==1 and 0<=attempts<=plan.cap and 0<=buy<=1
    # One initial lookup; each acquired observation adds its attempt cost,
    # eight control units, and the next state's eight-unit lookup.
    control_units=8+16*attempts
    gain=bounded(plan.horizon*(theta-F(1,2))*buy-F(1,2)*attempts-plan.unit_price*control_units)
    return {'theta':theta,'buy_probability':buy,'expected_profile_attempts':attempts,
            'expected_online_control_units':control_units,'gain_excluding_construction':gain,
            'reachable_state_count':nodes}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=False);(out/'sources').mkdir()
    for name in ('07_computation_adapter.py',Path(__file__).name):
        (out/'sources'/name).write_bytes((HERE/name).read_bytes())
    results=[];construction_total=0
    for cap in CAPS:
        for horizon in HORIZONS:
            for price in PRICES:
                meter=A.Meter(1000000)
                plan,core=build(cap,horizon,price,meter)
                # This exact table is frozen before independent forward audit.
                stem=f'cap{cap}_h{horizon}_price{price.numerator}_{price.denominator}'
                (out/(stem+'_plan.json')).write_bytes(canonical({'identity':plan.identity,'core':core})+b'\n')
                conditional=tuple(forward_audit(plan,t) for t in (LOW,HIGH))
                prior_gain=sum((p*r['gain_excluding_construction'] for p,r in zip(PRIORS,conditional)),F(0))
                assert prior_gain==plan.rows[0][3]-8*price
                setup=price*sum(plan.construction_resources)
                row={'cap':cap,'horizon':horizon,'unit_price':price,'root_action':plan.rows[0][2],
                     'bellman_value_after_initial_lookup':plan.rows[0][3],
                     'prior_gain_excluding_construction':prior_gain,
                     'construction_units':sum(plan.construction_resources),'construction_cost':setup,
                     'all_in_prior_gain':prior_gain-setup,'conditional_laws':conditional,
                     'core_bytes':plan.core_bytes,'plan_id':plan.identity,'meter':meter.snapshot()}
                construction_total+=sum(plan.construction_resources);results.append(row)
    result={'status':'PASS','version':VERSION,'stage':'EXACT_STIPULATED_LAW_DEVELOPMENT',
            'rows':results,'plans':len(results),'total_24_plan_construction_units':construction_total,
            'source_hashes':dict(plan.source_hashes),'finished_utc':datetime.now(timezone.utc).isoformat(),
            'boundary':'Known two-point prior and conditional independence are assumptions. Exact forward-law audit is external. State bundles are a declared bounded arithmetic tariff, not measured CPU; human model and program development are unquantified. Root planning costs are sunk once incurred; all-in values retain them. No claim of choosing optimally whether to acquire this model or compute the table.'}
    (out/'result.json').write_text(json.dumps(result,indent=2,default=str)+'\n')
    print(json.dumps({'status':'PASS','plans':len(results),'source_hashes':dict(plan.source_hashes),
        'priced_cap12':[{k:r[k] for k in ('horizon','root_action','prior_gain_excluding_construction','construction_cost','all_in_prior_gain')} for r in results if r['cap']==12 and r['unit_price']==F(1,1000)]},indent=2,default=str))


if __name__=='__main__':main()
