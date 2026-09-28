from dataclasses import replace
from fractions import Fraction as F
from pathlib import Path
import json
from v2.checks import f06_inference_rules as R
from v2.checks import f06_derived_cases as D
ctx=R.context((),(),{})
g=R.num(0); old=R.num(2); new=R.num(1)
b=R.Builder(ctx,'h'); b.constant(new,R.add(old,D.rho(g,ctx)))
a=D.GuardAllowance(b.proof(),F(-1),F(1),g,new,old)
u=R.Builder(ctx,'h'); u.constant(g,R.num(0)); guard=u.proof()
results={}
for label,record in [('honest',a),('forged_baseline',replace(a,baseline=F(-100))),('forged_new',replace(a,new=R.num(3))),('forged_both',replace(a,baseline=F(-100),new=R.num(3)))]:
    p=D.almost_exclusion(ctx,record,guard); root=R.check(ctx,p)
    results[label]={'actual_root':R.serial(root),'advertised_difference':str(R.evaluate(record.new,ctx.signature,{})-R.evaluate(record.old,ctx.signature,{})), 'advertised_baseline':str(record.baseline),'literal_requested_pair_matches':(root.new,root.old)==(record.new,record.old),'actual_difference':str(R.evaluate(root.new,ctx.signature,{})-R.evaluate(root.old,ctx.signature,{}))}
Path('/mnt/data/f07_public_session/metadata_probe.json').write_text(json.dumps(results,indent=2)+'\n')
for k,v in results.items(): print(k,{key:val for key,val in v.items() if key!='actual_root'})
