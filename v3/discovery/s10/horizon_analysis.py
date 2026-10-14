from pathlib import Path
import json
root=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
design=read(root/'sf01/design.json');result={'contributor':'Codex (GPT-6)','scope':'Observed prefixes of existing sf01 streams, including full initial setup each time. No extrapolation, new purchases or confirmation.','strata':{}}
for stratum in ['near6','fixed18']:
    data={c['name']:{a:read(root/'sf01'/c['name']/a/'summary.json') for a in design['arms']} for c in design['cases'] if c['stratum']==stratum}
    def cost(s,h):return {'physical_fee':sum(r['physical_fee'] for r in s['rows'][:h]),'named_units':s['setup_units']+sum(r['named_units'] for r in s['rows'][:h])}
    def joint(a,b):return all(a[k]<b[k] for k in a)
    observations=[]
    for h in range(1,129):
        aggregate={a:{'physical_fee':0,'named_units':0} for a in design['arms']};wins=[];losses=[]
        for name,arms in data.items():
            cs={a:cost(s,h) for a,s in arms.items()}
            for a,c in cs.items():
                for k,v in c.items():aggregate[a][k]+=v
            if joint(cs['scalar_prefix'],cs['relevant_audit']):wins.append(name)
            if joint(cs['relevant_audit'],cs['scalar_prefix']):losses.append(name)
        observations.append({'horizon_per_source':h,'outputs_per_arm':h*len(data),'totals':aggregate,'prefix_strictly_improves_both':joint(aggregate['scalar_prefix'],aggregate['relevant_audit']),'sources_improving_both':wins,'sources_worse_on_both':losses})
    persistent=next((h for h in range(1,129) if all(r['prefix_strictly_improves_both'] for r in observations[h-1:])),None)
    result['strata'][stratum]={'first_jointly_better_horizon':next((r['horizon_per_source'] for r in observations if r['prefix_strictly_improves_both']),None),'first_persistently_jointly_better_observed_horizon':persistent,'observations':observations}
(root/'horizon_analysis.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({s:{'first':v['first_jointly_better_horizon'],'persistent':v['first_persistently_jointly_better_observed_horizon'],'source_wins_at128':len(v['observations'][-1]['sources_improving_both']),'source_losses_at128':len(v['observations'][-1]['sources_worse_on_both'])} for s,v in result['strata'].items()}))
