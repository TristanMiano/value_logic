from pathlib import Path
import argparse, hashlib, io, subprocess
from datetime import datetime
from collections import defaultdict
import json,csv
parser=argparse.ArgumentParser(description="Reproduce Gate A's historical timing check without crediting later rows.")
parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[2])
parser.add_argument('--json',type=Path)
args=parser.parse_args()
root=args.repo.resolve()
meta=json.loads((Path(__file__).parent/'A_1_timing_review.json').read_text(encoding='utf-8'))
base=meta['base_commit']
try:
    proc=subprocess.run(['git','-C',str(root),'show',base+':v2/time_ledger.csv'],capture_output=True,check=False)
    raw=proc.stdout if proc.returncode==0 else (root/'v2/time_ledger.csv').read_bytes()[:meta['input_bytes']]
except FileNotFoundError:
    raw=(root/'v2/time_ledger.csv').read_bytes()[:meta['input_bytes']]
if hashlib.sha256(raw).hexdigest()!=meta['input_sha256']:
    raise SystemExit('Historical input hash differs. Use a checkout containing the recorded base commit; nothing changed.')
rows=list(csv.DictReader(io.StringIO(raw.decode('utf-8'))))
bytask=defaultdict(lambda:defaultdict(float)); lanes=defaultdict(lambda:defaultdict(float)); all_int=[]; issues=[]; verified=0; missing=[]; diffs=[]
def dt(s):return datetime.fromisoformat(s.replace('Z','+00:00'))
def stamps(obj,out):
 if isinstance(obj,dict):
  utc=obj.get('utc') or obj.get('start_utc')
  ns=obj.get('monotonic_ns',obj.get('mono_ns'))
  if utc and isinstance(ns,(int,float)):out[utc]=int(ns)
  for k,v in obj.items():
   if isinstance(v,(dict,list)):stamps(v,out)
 elif isinstance(obj,list):
  for v in obj:stamps(v,out)
for index,row in enumerate(rows,2):
 engaged=float(row.get('engaged_seconds') or 0)
 task=row['task_id'];mode=row['mode']
 if engaged>0 and mode in ('D','L','E'):
  bytask[task][mode]+=engaged;lanes[task][row['lane']]+=engaged
  a,b=dt(row['start_utc']),dt(row['end_utc']);elapsed=float(row['elapsed_seconds'])
  if b<a or engaged>elapsed+0.005:issues.append({'row':index,'problem':'negative interval or credit exceeds elapsed'})
  all_int.append((a,b,index,task))
  # Each session prefix may have multiple runtime files. Pair only within one file.
  prefix=f"{task}_{row['session_id'].replace('-S','_S')}"
  matches=list((root/'v2/work_logs').glob(prefix+'*clock.jsonl'))
  found=False
  for p in matches:
   out={}
   for s in p.read_text(encoding='utf-8').splitlines():
    if s.strip():stamps(json.loads(s),out)
   if row['start_utc'] in out and row['end_utc'] in out:
    raw=(out[row['end_utc']]-out[row['start_utc']])/1e9
    if abs(raw-elapsed)>0.005:diffs.append({'row':index,'raw_seconds':raw,'ledger_elapsed':elapsed,'path':str(p.relative_to(root))})
    else:verified+=1
    found=True;break
  if not found and task=='F01' and row['session_id']=='2026-09-21-S2':
   out=json.loads((Path(__file__).parent/'A_1_f01_s2_endpoints.json').read_text(encoding='utf-8'))['endpoints']
   if row['start_utc'] in out and row['end_utc'] in out:
    raw=(out[row['end_utc']]-out[row['start_utc']])/1e9
    if abs(raw-elapsed)>0.005:diffs.append({'row':index,'raw_seconds':raw,'ledger_elapsed':elapsed,'path':'F01 S2 fetched endpoints'})
    else:verified+=1
    found=True
  if not found:missing.append({'row':index,'task':task,'session':row['session_id'],'start':row['start_utc'],'end':row['end_utc']})
all_int.sort()
for prev,nxt in zip(all_int,all_int[1:]):
 if nxt[0]<prev[1]:issues.append({'problem':'overlap','rows':[prev[2],nxt[2]],'seconds':(prev[1]-nxt[0]).total_seconds()})
floors={'F01':('D',60),'F02':('D',60),'F03':('L',60),'F04':('D',60)}
totals=defaultdict(float);ltot=defaultdict(float)
for vals in bytask.values():
 for k,v in vals.items():totals[k]+=v
for vals in lanes.values():
 for k,v in vals.items():ltot[k]+=v
report={'input':'v2/time_ledger.csv','rows':len(rows),'positive_research_rows':len(all_int),'mode_seconds':dict(bytask),'lane_seconds':dict(lanes),'floor_checks':{k:{'mode':m,'recorded_minutes':bytask[k][m]/60,'required_minutes':n,'met':bytask[k][m]>=n*60} for k,(m,n) in floors.items()},'cycle_mode_percent':{k:100*v/sum(totals.values()) for k,v in totals.items()},'cycle_lane_percent':{k:100*v/sum(ltot.values()) for k,v in ltot.items()},'monotonic_elapsed_matches':verified,'raw_mismatches':diffs,'unmatched_rows':missing,'accounting_issues':issues,'limits':'Recorded work-block audit, not independent observation of past cognitive work. Missing raw files are not fabricated. Original exclusions/credits are preserved.'}
report.update({k:meta[k] for k in ('base_commit','input_bytes','input_sha256','input_git_blob','method')})
if args.json:
    args.json.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'rows':len(rows),'verified':verified,'unmatched':len(missing),
                  'issues':len(issues)+len(diffs),'floor_checks':report['floor_checks']},indent=2))
raise SystemExit(0 if not missing and not issues and not diffs and all(x['met'] for x in report['floor_checks'].values()) else 1)
