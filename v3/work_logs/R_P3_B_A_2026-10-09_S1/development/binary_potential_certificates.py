"""Tighter certificates for the already executed uniform binary-loss service.

ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC. R-P3-B-A DEVELOPMENT.
Read-only mathematical calculation; output is refused if already present.
"""
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

ROOT=Path(__file__).resolve().parent


def log_ratio(numerator, denominator, terms=24):
    assert numerator>denominator>0
    z=F(numerator-denominator,numerator+denominator)
    lower=2*sum((z**(2*j+1)/F(2*j+1) for j in range(terms)),F(0))
    upper=lower+2*z**(2*terms+1)/F(2*terms+1)/(1-z*z)
    return lower,upper


def main():
    input_path=ROOT/'service_comparison/run_001/result.json'
    inputs=json.loads(input_path.read_text())
    ln2_lower,ln2_upper=log_ratio(2,1)
    ln4_upper=2*ln2_upper
    rows=[]
    for arm in inputs['learner_arms']:
        t,b=arm['horizon'],arm['block_size'];m=t//b;k=max(2,b-1)
        ell=min(arm['evaluation']['fixed_expert_all_issued_losses'].values())
        beta_lower,beta_upper=log_ratio(k,k-1)
        beta_lower*=k;beta_upper*=k
        alpha_lower=F(b-1,b)*beta_lower;alpha_upper=F(b-1,b)*beta_upper
        old_alpha=F(b-1,b)*(1+F(1,k))
        assert alpha_upper<old_alpha<=1
        state=F(0) if arm['state_bits'] is None else F((b-1)*m*k,(1<<arm['state_bits'])-1)
        brier_state=F(0) if arm['state_bits'] is None else F(b*m*k,(1<<arm['state_bits'])-1)
        action=F(t-m,1<<arm['contract']['action_bits'])
        brier_round=F(2*t,1<<arm['contract']['action_bits'])
        common=(b-1)*k*ln4_upper+state+action
        retrospective=min(F(t-m),alpha_upper*ell+common)
        source_known=min(F(t-m),alpha_upper*F(t,2)+common)
        brier=min(F(t),beta_upper*ell+b*k*ln4_upper+brier_state+brier_round)
        old=F(arm['evaluation']['theorem_bounds']['terminal_expectation_upper_clipped'])
        assert retrospective<=old
        rows.append({'arm':arm['name'],'policy_change':False,'observed_source_version':arm['contract']['version'],
            'alpha_enclosure':[str(alpha_lower),str(alpha_upper)],'conservative_original_alpha':str(old_alpha),
            'retrospective_L_star':ell,'source_known_L_star_upper':str(F(t,2)),
            'refined_terminal_upper':str(retrospective),'refined_terminal_upper_decimal':float(retrospective),
            'original_terminal_upper':str(old),'bound_reduction':str(old-retrospective),
            'source_known_terminal_upper':str(source_known),'source_known_terminal_upper_decimal':float(source_known),
            'refined_brier_upper':str(brier),'state_allowance':str(state),'action_allowance':str(action)})
    rate_rows=[]
    for b in (2,4,8,16,32,64,128,256,512,1024):
        eta=F(2,b+1)
        scalar_ratio_cap=1+eta/(2*(1-eta))
        alpha_cap=F(b-1,b)*scalar_ratio_cap
        assert alpha_cap==1
        penalty=F(b-1)/eta
        assert penalty==F(b*b-1,2)
        rate_rows.append({'B':b,'unexecuted_eta':str(eta),'alpha_cap':str(alpha_cap),
                          'log_N_coefficient':str(penalty),'integer_correct_factor':b+1,'integer_wrong_factor':b-1,
                          'status':'Mathematical rate option only; not a selected or executed policy.'})
    out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','task':'R-P3-B-A','stage':'DEVELOPMENT',
        'kind':'Rational-certificate refinement, no new scientific execution',
        'input_sha256':hashlib.sha256(input_path.read_bytes()).hexdigest(),
        'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'log2_enclosure':[str(ln2_lower),str(ln2_upper)],'executed_uniform_rows':rows,'unexecuted_rate_candidates':rate_rows}
    with (ROOT/'binary_potential_certificates.json').open('x') as stream:
        json.dump(out,stream,indent=2);stream.write('\n')
    print(json.dumps({'status':'PASS','uniform_rows':len(rows),'unexecuted_rate_rows':len(rate_rows),
        'T3968_B8_fixed':[r for r in rows if r['arm']=='main_T3968_B8_state16_seed307201'][0]}))


if __name__=='__main__':
    main()
