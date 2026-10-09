"""Saved-evidence price geometry and source-known finite bound calculation.

ChatGPT (GPT-6 Astra Pro), 2026-10-09. R-P3-B-A DEVELOPMENT.
No new mathematical service executions, random traces or exposed labels.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
RUN = ROOT / 'service_comparison/run_001'


def read(path):
    return json.loads(path.read_text())


def ceil_power(exact_bound):
    exponent = 1
    while F(1 << exponent) < exact_bound:
        exponent += 1
    return exponent


def main():
    result = read(RUN / 'result.json')
    rows = []
    for arm in result['learner_arms']:
        invoice = read(RUN / 'learner_arms' / arm['name'] / 'deployment_invoice.json')
        table = read(RUN / 'controls' / f"quadratic_residue_table_T{arm['horizon']}" / 'deployment_invoice.json')
        keys = sorted(set(invoice['by_category']) | set(table['by_category']))
        delta = {key: invoice['by_category'].get(key, 0)-table['by_category'].get(key, 0) for key in keys}
        assert sum(delta.values()) == invoice['total']-table['total']
        assert invoice['total'] > table['total']
        rows.append({'arm': arm['name'], 'observed_v1_1_delta': delta,
                     'negative_coordinates': {key: value for key,value in delta.items() if value<0},
                     'common_price_delta': sum(delta.values()),
                     'learner_terminal_errors': arm['evaluation']['terminal_sampled_01_loss'],
                     'table_terminal_errors': 0})
    reference = next(row for row in rows if row['arm']=='main_T3968_B8_state16_seed307201')
    # Current core differs only in the setup charge: fresh registry record and
    # observed source registry supply an exact coordinate delta, not a rerun.
    old = read(RUN/'learner_arms/main_T3968_B8_state16_seed307201/source_registry.json')['resources']['by_category']
    current = read(ROOT/'service_comparison/current_registry_reprice_v1.json')['current_registry']['resources']['by_category']
    transfer = {key:current.get(key,0)-old.get(key,0) for key in set(current)|set(old)}
    assert sum(transfer.values()) == 26
    reference['derived_v1_2_delta'] = {key:value+transfer.get(key,0) for key,value in reference['observed_v1_1_delta'].items()}
    reference['price_formula'] = 'J_learner-J_table = c*1702 + sum_j lambda_j*derived_v1_2_delta[j] for these fixed traces.'
    reference['one_coordinate_separator'] = {'prices': {'cache':1,'all_other_primitive_categories':0,'terminal_error':0},
        'learner_minus_table':reference['derived_v1_2_delta']['cache'],
        'meaning':'Refutes categorywise table dominance; not a claimed favorable application or superiority to other ordinary controls.'}
    precision = []
    # ln(4)=4*sum_{k>=0}(1/3)^(2k+1)/(2k+1); an explicit positive tail.
    z=F(1,3); count=24
    log_lower=4*sum((z**(2*k+1)/F(2*k+1) for k in range(count)), F(0))
    log_upper=log_lower + 4*z**(2*count+1)/F(2*count+1)/(1-z*z)
    for t in (2,8,64,992,3968,8192):
        for b in (2,4,8,16,32,64,128,256,512,1024):
            if t%b:
                continue
            m=t//b
            for mode in ('uniform','adaptive_tickets'):
                k=max(2,b-1) if mode=='uniform' else 2*b-1
                a=(b-1)*m*k if mode=='uniform' else m*k*k
                state=ceil_power(F(1+a)); action=ceil_power(F(t-m))
                assert F(a,(1<<state)-1)<=1 and F(t-m,1<<action)<=1
                assert state<=32 and action<=32
                alpha=F(b-1,b)*(1+F(1,k)) if mode=='uniform' else F(1)
                log_coefficient=(b-1)*k if mode=='uniform' else k*k
                certificate=min(F(t-m), alpha*F(t,2)+log_coefficient*log_upper+F(a,65535)+F(t-m,65536))
                row={'T':t,'B':b,'mode':mode,'s_for_state_allowance_1':state,'h_for_action_allowance_1':action,
                     'source_known_L_star_upper':str(F(t,2)),
                     's16_h16_terminal_expectation_upper':str(certificate),
                     's16_h16_terminal_expectation_upper_decimal':float(certificate),
                     'trivial_cap_active':certificate==t-m}
                # Representation checks for the prospectively declared precisions.
                checks=[]
                for s in (1,2,8,16,32):
                    for h in (1,2,8,16,32):
                        mass=4*(1<<s)
                        assert mass==(1<<(s+2))
                        checks.append({'s':s,'h':h,'state_allowance':str(F(a,(1<<s)-1)),
                                       'action_allowance':str(F(t-m,1<<h)),
                                       'all_weight_probabilities_exactly_dyadic':h>=s+2})
                row['precision_grid']=checks
                precision.append(row)
    files=[RUN/'result.json',ROOT/'price_scope_plan_v1.json',ROOT/'deployment_bound_design.md',Path(__file__)]
    output={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','stage':'DEVELOPMENT',
        'no_scientific_rerun':True,'source_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        'price_rows':rows,'reference':reference,'registry_transfer_by_category':transfer,
        'log4_enclosure':[str(log_lower),str(log_upper)],'parameter_rows':precision,
        'precision_grid_count':len(precision)*25,
        'scope':'All-category price tests concern retained coordinates and fixed trajectories; expected certificates use source-known T/2, not evaluator losses.'}
    destination=ROOT/'price_and_precision_audit.json'
    with destination.open('x') as stream:
        json.dump(output,stream,indent=2);stream.write('\n')
    print(json.dumps({'status':output['status'],'rows':len(rows),'precision_grid_count':output['precision_grid_count'],
        'negative_coordinates':sorted({k for r in rows for k in r['negative_coordinates']}),
        'reference_delta':reference['derived_v1_2_delta'],
        'reference_precision':[r for r in precision if r['T']==3968 and r['B']==8][0]['s16_h16_terminal_expectation_upper_decimal']}))


if __name__=='__main__':
    main()
