"""Narrow reconstruction of the paper's exposed episode and exact threshold.

Not a new confirmation campaign; never writes into historical evidence.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib, importlib.util, json, sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'v3/discovery/s20'))
from decision_service import DecisionService
from cert_audit import source_value

def main():
    inputs=json.loads((ROOT/'v3/discovery/s20/audit_inputs.json').read_text(encoding='utf-8'))
    problem=next(r['problem'] for r in inputs if r['name']=='noisy_envelope')
    service=DecisionService(problem)
    args=(['-5/4','-6/5'],[['0','1'],['10','1'],['10','1'],['10','1'],['0','1']],list(range(5)))
    initial=service.assess(*args,1)
    assert initial['status']=='CONDITIONAL_ON_NONEMPTY_SOURCE'
    assert initial['observation']['sharp_improvement_upper']=='1'
    work=service.propagate(2)
    assert work==dict(row_visits=134,coordinate_updates=28,optimizer_calls=0)
    partial=service.assess(*args,0)
    assert partial['bracket']['outer']==[['-281/200','-11/8'],['-221/200','-43/40']]
    assert not partial['bracket']['exact']
    sources=[[['1/5','1'],['1','4/5']],[['1','1/5'],['4/5','1']]]
    values=[]
    for source in sources:
        service.add_source(source,service.problem_sha256)
        values.append(source_value(problem,[list(map(F,row)) for row in source]))
    final=service.assess(*args,0)
    assert final['status']=='CHECKED_DECISION'
    assert final['computation']['sharp_improvement_bounds'][0]=='0'
    assert values==[F(-7,5),F(-11,10)]
    checker_path=ROOT/'v3/discovery/s17/block_check_v2.py'
    spec=importlib.util.spec_from_file_location('n16_report_checker',checker_path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    saved=json.loads((ROOT/'v3/discovery/s17/cancellation_result.json').read_text(encoding='utf-8'))
    threshold=module.verify(saved['receipt'])
    assert threshold==saved['result']
    assert F(threshold['upper'])<F(3,5)
    # Independent elementary arithmetic for the two possible supports in the text.
    losses=[(9,0),(0,10),(12,13)]
    gaps=[]
    for support in [(0,1),(0,1,2)]:
        worst=[max(losses[j][a] for j in support) for a in (0,1)]
        gaps.append(worst[0]-min(worst))
    assert gaps==[0,0]
    paths={Path(m.__file__).resolve() for m in list(sys.modules.values()) if getattr(m,'__file__',None) and str(ROOT/'v3/discovery') in str(Path(m.__file__).resolve())}
    paths.update([checker_path,ROOT/'v3/discovery/s20/audit_inputs.json',ROOT/'v3/discovery/s17/cancellation_result.json',Path(__file__).resolve()])
    result={'status':'PASS','classification':'P3-12 targeted reconstruction on exposed inputs, not confirmation','contributor':'Codex (GPT-6)','python':sys.version,'propagation':work,'outer':partial['bracket']['outer'],'source_values':list(map(str,values)),'final_status':final['status'],'fast_gap':final['computation']['sharp_improvement_bounds'][0],'N16':threshold,'two_support_gaps':gaps,'source_sha256':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}}
    (HERE/'episode_result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ['status','propagation','source_values','final_status','fast_gap']}))

if __name__=='__main__':main()
