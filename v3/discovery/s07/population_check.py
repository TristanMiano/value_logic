#!/usr/bin/env python3
"""Read-only reconstruction of the common-CDF repair acquisition records.

ChatGPT (GPT-6 Astra Pro), DEVELOPMENT. Rechecks raw proof and CDF support
certificates; derives a strong deterministic-cohort prefix alternative from
the *same* paid observations. Prefix alternative is replay, not a new arm.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import sys
from datetime import datetime,timezone
import population_service as service


def reconstruct(path):
    raw=json.loads(path.read_text())
    data=raw['source']; instance=data['logical_source']
    assert raw['status']=='complete'
    assert service.native.kernel.digest({k:v for k,v in data.items() if k!='source_identity'})==data['source_identity']
    public={k:v for k,v in data.items() if k!='hidden_population'}
    results=[]
    for arm in raw['arms']:
        meter=service.native.kernel.Meter()
        costs=service.PopulationCosts(public,meter)
        proof=arm['events'][0]['response']
        leaves=service.check_common_proof(instance,proof,meter)
        witnesses=[service.native.profile_kernel.compile_witness(instance,model,meter)
                   for model in data['initial_checked_models']]
        assert [w['violation_mask'] for w in witnesses]==[1,2]
        profile=dict(source_identity=instance['identity'],witnesses=witnesses,
                     trees=[dict(leaf_masks=leaves,receipt_id=proof['receipt_id'])])
        # This outer state targets the fixed cohort mean, with every unvisited
        # identity represented. It needs no sampling event or mode frequencies.
        all_intervals={i:[0,3] for i in range(data['population_size'])}
        prefix=[dict(audits=0,deterministic_cohort_bound=4)]
        cursor=1
        stages_checked=0
        for stage in arm['stages']:
            while cursor<len(arm['events']) and cursor<=stage['observations']:
                event=arm['events'][cursor]
                assert event['kind']=='cut_audit'
                receipt=event['receipt']; i,j=receipt['row'],receipt['cut']
                assert receipt['provider_call']==cursor-1
                assert receipt['at_or_below']==(data['hidden_population'][i]<=j)
                costs.observe(receipt)
                l,u=all_intervals[i]
                all_intervals[i]=[l,j] if receipt['at_or_below'] else [j+1,u]
                low=F(sum(u<=1 for l,u in all_intervals.values()),data['population_size'])
                high=F(sum(l<=1 for l,u in all_intervals.values()),data['population_size'])
                bound=min(max(F(0),4-8*low),max(F(0),8*high-4))
                prefix.append(dict(audits=cursor,deterministic_cohort_bound=bound,
                                   complete_cohort_cut_probability_interval=[low,high]))
                cursor+=1
            got=service.joint.certificate(profile,costs,data['price'])
            assert got['bound']==F(stage['answer']['bound'])
            assert got['model']==stage['answer']['model']
            assert costs.snapshot()['physical_intervals']==stage['cost_state']['physical_intervals']
            assert tuple(costs.sweep.lower)==tuple(map(F,stage['cost_state']['lower_cdf']))
            assert tuple(costs.sweep.upper)==tuple(map(F,stage['cost_state']['upper_cdf']))
            stages_checked+=1
        assert cursor==len(arm['events'])
        support_checks=0
        for record in arm['support_records']:
            sweep=service.cdf_sweep.CDFSweep(record['band']['lower'],record['band']['upper'])
            payoff=list(map(F,record['payoff']))
            assert service.cdf_sweep.verify_minimum(sweep,[-v for v in payoff],record['negative_minimum'])
            assert -F(record['negative_minimum']['value'])==F(record['value'])
            support_checks+=1
        first=next((p for p in prefix if p['deterministic_cohort_bound']<=data['tolerance']),None)
        classified=sum(costs.multiplicity[i] for i,(l,u) in costs.intervals.items() if u<=1 or l>=2)
        results.append(dict(policy=arm['policy'],checked_stages=stages_checked,
            independently_checked_support_certificates=support_checks,
            all_actual_audits_reconstructed=cursor-1,fully_identified_latent_rows=sum(l==u for l,u in costs.intervals.values()),
            draw_occurrences_with_relevant_cost_class=classified,
            deterministic_cohort_prefix=prefix,first_qualifying_deterministic_prefix=first,
            reconstruction_invoice=meter.record()))
    if raw['version'].endswith('v2'):
        relevant,full,direct=raw['arms']
        assert relevant['invoice']['named_units']==direct['invoice']['named_units']
        assert relevant['summary']==direct['summary']
        assert full['summary']['external_cut_audits']==2*relevant['summary']['external_cut_audits']
    return dict(path=path.name,source_sha256=service.native.sha(path),arms=results)


def main(output,paths):
    if output.exists():
        raise FileExistsError('Preserve reconstruction evidence')
    results=[reconstruct(path) for path in paths]
    record=dict(status='passed',created_utc=datetime.now(timezone.utc).isoformat(),
        contributor='ChatGPT (GPT-6 Astra Pro)',evidence='DEVELOPMENT reconstruction',
        checker_sha256=service.native.sha(__file__),runs=results,actual_new_acquisitions=0,
        limitations='One declared synthetic source, no empirical calibration claim. The deterministic-cohort prefix uses same already purchased receipts; no hypothetical saved calls are counted as executed savings.')
    output.write_text(json.dumps(record,indent=2,default=service.encode)+'\n')
    print(json.dumps(dict(status='passed',runs=len(results),arms=sum(len(r['arms']) for r in results),
                         stages=sum(a['checked_stages'] for r in results for a in r['arms']),
                         support_checks=sum(a['independently_checked_support_certificates'] for r in results for a in r['arms']))))
    for r in results:
        for a in r['arms']:
            print(json.dumps(dict(run=r['path'],policy=a['policy'],first_deterministic=a['first_qualifying_deterministic_prefix']),default=service.encode))


if __name__=='__main__':
    main(Path(sys.argv[1]),list(map(Path,sys.argv[2:])))
