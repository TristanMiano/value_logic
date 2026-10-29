"""Extract paper tables from preserved evidence; never rerun historical experiments."""
from pathlib import Path
from fractions import Fraction
import hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=HERE/'tables'
OUT.mkdir(exist_ok=True)
sources={}
def read(name):
    p=ROOT/name
    sources[name]=hashlib.sha256(p.read_bytes()).hexdigest()
    return json.loads(p.read_text(encoding='utf-8'))
def table(name,headers,rows):
    text='| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'
    text+=''.join('| '+' | '.join(map(str,r))+' |\n' for r in rows)
    (OUT/(name+'.md')).write_text(text,encoding='utf-8')
audit=read('v3/discovery/s20/audit_results.json')
partial=read('v3/discovery/s20/partial_runs/a01/result.json')
refine=read('v3/discovery/s20/refine_runs/a01/result.json')
inc=read('v3/discovery/s20/incumbent_runs/a01/result.json')
feature=read('v3/discovery/s15/feature_probe.json')
great=read('v3/discovery/s20/greatest_runs/a01/result.json')
integ=read('v3/discovery/s20/integration_runs/a01/result.json')
rows=[
 ['Range certificate audit',f"{audit['case_count']} problems; {sum(x['bounded'] for x in audit['cases'])} bounded and {sum(x['empty'] for x in audit['cases'])} empty slices",f"{sum(x['source_witnesses'] for x in audit['cases'])} source witnesses; {sum(x['mutations'] for x in audit['cases'])} rejected mutations",'Development; local checker, not end-to-end proof'],
 ['Partial range service',f"{len(partial['cases'])} problems; {sum(x['query_answers'] for x in partial['cases'])} answers",f"{sum(x['source_answers'] for x in partial['cases'])} checked attainable answers",'Development; exposed examples'],
 ['Sharp stopping gap',f"{refine['brackets']:,} brackets; {refine['supports']:,} support uses",f"{refine['strict_improvements']} tighter bounds; {refine['newly_certified_actions']} new optimality certificates",'Development; exhaustive finite controls'],
 ['Incumbent observation bound',f"{inc['brackets']:,} brackets; {inc['support_controls']} distinct support controls",f"{inc['strict_decomposition_improvements']:,} tighter bounds than sum of separate maxima",'Development; finite controls'],
 ['Structured model correction',f"{feature['coefficient_maps']} maps over the three-element field",f"{feature['repaired_vectors_checked']:,} repaired vectors",'Development; exact finite-field scope'],
 ['Greatest-point shortcut',f"{len(great['cases'])} restricted cases",f"{great['shortcut_optimizer_calls']} versus {great['full_optimizer_calls']} LP calls",'Structural shortcut; not general speedup'],
 ['Bound source-to-action service',f"{integ['source_checks']} source checks; {len(integ['invalid_rejections'])} invalid inputs rejected",f"{integ['optimizer_calls']} optimizer calls",'Implemented composition on exposed example']]
table('results',['Service','Unit and denominator','Recorded result','Evidence scope'],rows)
bc=read('v3/discovery/s08/progress_results.json')
# Reconstruct aggregate directly from the four saved stream results.
for arm in ['budget','ordinary_budget','cover','anchor']:
    records=[read(f'v3/discovery/s08/bc02/c{i}_{arm}/result.json') for i in range(4)]
    for key in ['outputs','base_audit_fee','named_units','setup_units']:
        assert sum(r[key] for r in records)==bc['totals'][arm][key]
cost=[]
for arm,label in [('budget','Selective controller'),('ordinary_budget','Same controller, ordinary label'),('cover','Distinct greedy-cover control'),('anchor','Always-fallback control')]:
    d=bc['totals'][arm];cost.append([label,d['outputs'],f"{d['base_audit_fee']:,}",f"{d['named_units']:,}"])
table('cost',['Method','Outputs','Audit fees','Counted work'],cost)
base=bc['totals']['anchor'];chosen=bc['totals']['budget']
fee=Fraction(base['base_audit_fee']-chosen['base_audit_fee'],base['base_audit_fee'])
work=Fraction(base['named_units']-chosen['named_units'],base['named_units'])
assert round(100*float(fee),2)==37.37 and round(100*float(work),2)==9.68
data={'schema':'p3_report_tables_v1','contributor':'Codex (GPT-6)','source_sha256':sources,'results':rows,'cost':cost,'saving_vs_fallback':{'audit_fraction':str(fee),'counted_work_fraction':str(work)},'analytic_coordinate_example':{'n':128,'M':35,'d':4,'initial_feature_rank':7,'repaired':128*7+4*(35-7),'full':128*35,'saving_fraction':str(1-Fraction(128*7+4*(35-7),128*35))},'no_reacquisition':True}
(OUT/'data.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print('Extracted 7 development rows and 4 matched cost rows; 16 raw cost records verified.')
