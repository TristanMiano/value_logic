"""Versioned feature-enumerator repair; replay old exposed cases explicitly."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import hashlib,json,sys,time
import moment_probe as previous
import moment_v2 as revised
from moment_values import masks as original_masks
previous.acquire_from_table=revised.acquire_from_table
previous.plan=revised.plan


def main(out):
    assert not out.exists();start=time.perf_counter_ns();small=0
    for m in range(1,11):
        for d in range(m+1):assert revised.masks(m,d)==original_masks(m,d);small+=1
    path=Path(__file__).with_name('moment01.json');prior=json.loads(path.read_text());replays=[]
    for old in prior['random_cases']+prior['pair']+prior['parity']+[prior['point_mass']]:
        row=previous.compare(old['m'],old['counts'],tuple(tuple(map(F,r)) for r in old['terminal']),tuple(map(F,old['prices'])),old['horizon'],old['available_mask'])
        assert row['value']==old['value'] and row['first_choices']==old['first_choices'];replays.append(row)
    scaling=[]
    for m in (64,128,256):
        begin=time.perf_counter_ns();masks=revised.masks(m,2);elapsed=time.perf_counter_ns()-begin
        assert len(masks)==sum(comb(m,k) for k in range(3)) and len(set(masks))==len(masks)
        assert all(k.bit_count()<=2 and 0<=k<1<<m for k in masks)
        scaling.append({'variables':m,'degree':2,'features':len(masks),'enumeration_ns':elapsed})
    sources={p:hashlib.sha256(Path(__file__).with_name(p).read_bytes()).hexdigest() for p in ('moment_v2.py','moment_v2_probe.py','moment_probe.py','continuation.py')}
    sources['../moment_values.py']=hashlib.sha256(Path(__file__).parent.parent.joinpath('moment_values.py').read_bytes()).hexdigest()
    result={'status':'complete','evidence':'DEVELOPMENT','contributor':'Codex (GPT-6)','python':sys.version,'sources':sources,
            'amendment':'Version 1 scanned 2^m masks. Version 2 enumerates coordinate combinations; all prior exposures are retained and reused explicitly, not confirmation.',
            'prior_record_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'small_enumerator_checks':small,'replayed_cases':replays,'enumerator_scaling':scaling,
            'elapsed_ns':time.perf_counter_ns()-start}
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:result[k] for k in ('status','small_enumerator_checks','enumerator_scaling','elapsed_ns')}))


if __name__=='__main__':main(Path(sys.argv[1]))
