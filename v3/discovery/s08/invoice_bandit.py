"""Ordinary source-free invoice learning; DEVELOPMENT, Codex (GPT-6)."""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json
import sys
import time
import g01
import star_learning as base
import markov_paths as mk
import markov_service as ms
import invoice_completion as ic
import continuum_policy as cp
import action_audits as aa

HERE=Path(__file__).resolve().parent
VERSION='s08-invoice-bandit-v1'
Meter=g01.kernel.Meter


def source(costs):
    data=ms.source(costs);data.pop('identity');data.pop('repeat_numerators')
    data['bit_source']='Fresh independent rows from a fixed unknown joint ternary distribution'
    return g01.seal(data)


def prepare(data,meter):
    bank={};certs={};ranges={};duplicates={}
    for r in mk.MENU:
        proposed=mk.plan(data['audit_costs'],r);roots=proposed['roots']
        meter.pay('preparation','ordinary_policy_proposal',proposed['invoice']['total'])
        duplicate=next((q for q in bank if bank[q]==roots),None)
        meter.pay('preparation','compare_complete_root_maps',len(bank)*len(roots))
        if duplicate is not None:duplicates[r]=duplicate;continue
        bank[r]=roots;cert=ic.produce(data['audit_costs'],roots,{})
        checked=ic.check(data['audit_costs'],roots,{},cert)
        meter.pay('preparation','global_invoice_range_production',cert['invoice']['total'])
        meter.pay('preparation','independent_range_check',checked['total'])
        certs[r]=dict(proof=cert,checking=checked);ranges[r]=(cert['lower'],cert['upper'])
    return bank,ranges,dict(roots=bank,ranges=ranges,certificates=certs,duplicates=duplicates)


def run_arm(directory,case,rows):
    data=source(case['costs']);meter=Meter();cpu=time.process_time_ns();wall=time.perf_counter_ns()
    meter.pay('source','original_source_and_fee_admission',24+data['n']+sum(len(c)+1 for c in data['hard'])+5*len(data['features']))
    bank,ranges,artifact=prepare(data,meter);setup=meter.total
    g01.save(directory/'bank.json',cp.normalize(dict(source=data,**artifact)))
    counts={i:0 for i in bank};sums={i:F(0) for i in bank};intervals=dict(ranges)
    fees=audits=0;selected=Counter();regret=F(0);coverage_failures=0
    # Carried mathematical diagnostics; never used by controller selection.
    old=json.loads((HERE/'cs01'/f"{case['name']}_plugin_bank.json").read_text())
    values={int(i):cp.evaluate(list(map(F,p['proof']['coefficients'])),F(case['r'],10)) for i,p in old['policies'].items()}
    with (directory/'trace.jsonl').open('w') as trace,(directory/'diagnostics.jsonl').open('w') as diag:
        trace.write(json.dumps(dict(kind='header',version=VERSION,source=data['identity'],bank_sha256=g01.sha(directory/'bank.json')))+'\n');trace.flush()
        for t,row in enumerate(rows):
            before=meter.total;chosen=min(bank,key=lambda i:(intervals[i][0],counts[i],i))
            meter.pay('selection','compare_admitted_lower_fee_endpoints',3*len(bank))
            request=f"{case['name']}-ordinary-invoice-{t}"
            trace.write(json.dumps(dict(kind='plan',request=request,policy=chosen,interval=intervals[chosen]),default=g01.encode)+'\n');trace.flush()
            provider=base.Provider(data,row,request,trace,meter)
            receipts=ms.acquire(provider,data['n'],bank[chosen],meter)
            action=base.construct(data,receipts,request,meter);base.check(data,receipts,action,meter)
            paid=sum(r['base_fee'] for r in receipts);fees+=paid;audits+=len(receipts);selected[chosen]+=1
            lower,upper=ranges[chosen];assert lower<=paid<=upper
            counts[chosen]+=1
            if upper>lower:
                sums[chosen]+=F(paid-lower,upper-lower)
                lo,hi=base.confidence(counts[chosen],sums[chosen],len(bank),meter)
                intervals[chosen]=(max(intervals[chosen][0],lower+(upper-lower)*lo),min(intervals[chosen][1],lower+(upper-lower)*hi))
                if intervals[chosen][0]>intervals[chosen][1]:raise ValueError('Empty invoice confidence interval')
            meter.pay('learning','retain_own_complete_invoice_and_interval',12+counts[chosen].bit_length()+sums[chosen].numerator.bit_length()+sums[chosen].denominator.bit_length())
            trace.write(json.dumps(dict(kind='output',request=request,action=action,base_fee=paid,physical_audits=len(receipts),
                named_units=meter.total-before,count=counts[chosen],normalized_sum=sums[chosen],interval=intervals[chosen]),default=g01.encode,separators=(',',':'))+'\n');trace.flush()
            assert aa.direct_regret(data,action['assignment'],row)==0
            excess=values[chosen]-min(values.values());regret+=excess
            covered=all(lo<=values[i]<=hi for i,(lo,hi) in intervals.items());coverage_failures+=not covered
            diag.write(json.dumps(dict(request=t,hidden=row,action_regret=0,mean_intervals_cover=covered,expected_bank_fee_excess=excess),default=g01.encode)+'\n')
    return dict(outputs=len(rows),base_audit_fee=fees,physical_audits=audits,named_units=meter.total,setup_units=setup,
        invoice=meter.record(),selected_policies=selected,counts=counts,normalized_sums=sums,final_intervals=intervals,
        diagnostic_bank_values=values,cumulative_expected_bank_fee_regret=regret,observed_coverage_failures=coverage_failures,
        arm_cpu_ns=time.process_time_ns()-cpu,arm_wall_ns=time.perf_counter_ns()-wall)


if __name__=='__main__':
    directory=Path(sys.argv[1]);name=sys.argv[2];directory.mkdir(exist_ok=False)
    case=next(c for c in json.loads((HERE/'cs01/design.json').read_text())['cases'] if c['name']==name)
    rows=ms.draw(len(case['costs']),case['r'],1024,case['seed'])
    g01.save(directory/'result.json',run_arm(directory,case,rows))
