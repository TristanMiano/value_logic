"""Continuous replacement-price and reasoning-price profiles from paid repairs.

ChatGPT (GPT-6 Astra Pro), 2026-10-12. DEVELOPMENT. No new proof calls.
All uncertainty statements concern the retained finite cohort.
"""
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys
import time

from maxsat_repair import Meter, checked_objective


def regret_profile(intervals):
    """Exact sum_i(min(U_i,p)-min(L_i,p)) for every real price p>=0."""
    events = {F(0): 0}
    for lower, upper in intervals:
        lower, upper = F(lower), F(upper)
        if not 0 <= lower <= upper:
            raise ValueError('Invalid nonnegative objective interval')
        events[lower] = events.get(lower, 0)+1
        events[upper] = events.get(upper, 0)-1
    slope, value, previous = 0, F(0), F(0)
    pieces = []
    ordered = sorted(events)
    for j, point in enumerate(ordered):
        value += slope*(point-previous)
        slope += events[point]
        pieces.append(dict(left=str(point), right=str(ordered[j+1]) if j+1<len(ordered) else None,
                           value_at_left=str(value), slope=slope))
        previous=point
    assert slope==0
    return pieces


def evaluate(pieces, price):
    price=F(price)
    if price<0:
        raise ValueError('Replacement price must be nonnegative')
    piece=next(p for p in reversed(pieces) if F(p['left'])<=price)
    return F(piece['value_at_left'])+piece['slope']*(price-F(piece['left']))


def tariff_regions(lines):
    """Exact lower envelope of known action cost + lambda * service bill."""
    crossings={F(0)}
    for i, first in enumerate(lines):
        for second in lines[i+1:]:
            if first['work'] != second['work']:
                x=F(second['action_cost']-first['action_cost'], first['work']-second['work'])
                if x>0:
                    crossings.add(x)
    points=sorted(crossings)
    regions=[]
    for i,left in enumerate(points):
        right=points[i+1] if i+1<len(points) else None
        at=(left+right)/2 if right is not None else left+1
        chosen=min(lines,key=lambda x:(F(x['action_cost'])+at*x['work'],x['work'],x['name']))
        if regions and regions[-1]['winner']==chosen['name']:
            regions[-1]['right']=str(right) if right is not None else None
        else:
            regions.append(dict(left=str(left),right=str(right) if right is not None else None,
                                winner=chosen['name']))
    return regions


def run(destination):
    if destination.exists():
        raise FileExistsError('Choose a new result path')
    here=Path(__file__).resolve().parent
    evidence=here/'maxsat_repair_results.json'
    raw=json.loads(evidence.read_text())
    meter=Meter()
    initial=[checked_objective(instance,instance['public_incumbent'],meter)
             for instance in raw['instances']]
    started=time.perf_counter_ns()
    rows=[]
    for arm in raw['arms']:
        for stage in arm['stages']:
            intervals=stage['optimum_intervals']
            pieces=regret_profile(intervals)
            # Breakpoints and one point per affine interval reconstruct the
            # entire function; these are not random-price coverage trials.
            for piece in pieces:
                p=F(piece['left'])
                end=F(piece['right']) if piece['right'] is not None else p+2
                for price in (p,(p+end)/2):
                    assert evaluate(pieces,price)==sum(min(F(u),price)-min(F(l),price) for l,u in intervals)
            price=stage['price']
            action=sum(min(u,price) for l,u in intervals)
            upper_regret=evaluate(pieces,price)
            exact=sum(min(v,price) for v in raw['post_run_exact_optima'])
            assert 0<=action-exact<=upper_regret
            rows.append(dict(mode=arm['mode'],stage_price=price,profile=pieces,
                             total_action_cost=action,total_regret_certificate=str(upper_regret),
                             exact_reference_action_cost=exact,
                             realized_regret=action-exact,
                             largest_any_price_row_regret=max(u-l for l,u in intervals),
                             service_units=stage['snapshot']['total_units']))
    economic=[]
    for price in (3,6,9):
        # Favor the supplied-repair control by charging zero incremental
        # service work. Candidate bills include their whole recorded lifecycle.
        # This is a conservative comparison, not a free-certification claim.
        lines=[dict(name='public_repairs_favored_zero_incremental_bill',
                    action_cost=sum(min(u,price) for u in initial),work=0)]
        lines += [dict(name=row['mode'],action_cost=row['total_action_cost'],work=row['service_units'])
                  for row in rows if row['stage_price']==price]
        economic.append(dict(price=price,lines=lines,regions=tariff_regions(lines)))
    result=dict(status='DEVELOPMENT',contributor='ChatGPT (GPT-6 Astra Pro)',
                generated_utc=datetime.now(timezone.utc).isoformat(),command=sys.argv,
                sources={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                         (Path(__file__),evidence,here/'maxsat_repair.py')},
                new_solver_purchases=0,initial_witness_recheck_invoice=meter.record(),
                profile_and_analysis_ns=time.perf_counter_ns()-started,
                profiles=rows,economic_profiles=economic,
                scope='Exact deterministic profiles of the saved finite cohort. All real nonnegative replacement prices are covered by the piecewise formulas. Reasoning-price regions are retrospective and depend on these observed invoices; no forecast of new solver cost or currency equivalence is supplied.')
    destination.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(profile_and_analysis_ns=result['profile_and_analysis_ns'],
                          economic_profiles=economic)))


if __name__=='__main__':
    run(Path(sys.argv[1]))
