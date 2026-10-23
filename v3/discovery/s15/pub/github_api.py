"""Repository-scoped publication helper; never logs or persists credentials."""
import json
from pathlib import Path
import subprocess
import sys
import urllib.error
import urllib.request

ROOT=Path(__file__).resolve().parents[4]
REPO='TristanMiano/value_logic'
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None

def request(method,path,data=None):
    credential=subprocess.run(['git','credential','fill'],input='protocol=https\nhost=github.com\n\n',
        text=True,capture_output=True,cwd=ROOT,check=True)
    fields=dict(line.split('=',1) for line in credential.stdout.splitlines() if '=' in line)
    token=fields['password']
    req=urllib.request.Request('https://api.github.com/repos/'+REPO+'/'+path,
        data=json.dumps(data).encode() if data is not None else None,method=method,
        headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json',
                 'User-Agent':'value-logic-research-publication','Content-Type':'application/json'})
    with urllib.request.build_opener(NoRedirect).open(req,timeout=45) as r:
        return json.load(r)

mode=sys.argv[1]
if mode=='get-pr':
    obj=request('GET','pulls/'+str(int(sys.argv[2])))
    result={k:obj.get(k) for k in ('number','html_url','state','merged','merged_at','merge_commit_sha','draft')}
    result.update(head_sha=obj['head']['sha'],head_ref=obj['head']['ref'],base_ref=obj['base']['ref'])
elif mode=='create-pr':
    body=Path(sys.argv[2]).read_text(encoding='utf-8-sig')
    obj=request('POST','pulls',dict(title='Develop counterfactual bounds and model-correction constructions in s15',
        head='codex/discovery-20261023-s15',base='main',body=body,draft=False))
    result={k:obj.get(k) for k in ('number','html_url','state','draft')}
    result.update(head_sha=obj['head']['sha'],head_ref=obj['head']['ref'],base_ref=obj['base']['ref'])
elif mode=='runs':
    head=sys.argv[2];assert len(head)==40 and all(c in '0123456789abcdef' for c in head)
    obj=request('GET','actions/runs?head_sha='+head+'&per_page=30')
    result=[{k:r.get(k) for k in ('id','name','event','head_sha','status','conclusion','html_url','run_attempt')} for r in obj['workflow_runs']]
elif mode=='jobs':
    obj=request('GET','actions/runs/'+str(int(sys.argv[2]))+'/jobs?per_page=100')
    result=[{k:r.get(k) for k in ('id','name','status','conclusion','html_url','steps')} for r in obj['jobs']]
else: raise ValueError('Unsupported repository operation')
print(json.dumps(result,indent=2))
