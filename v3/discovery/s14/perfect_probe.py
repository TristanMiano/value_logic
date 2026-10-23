"""Classical perfect-code invoice adapter; Codex (GPT-6), DEVELOPMENT."""
from fractions import Fraction as F
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
import time

out=Path(__file__).with_suffix('.json')
assert not out.exists()
started=datetime.now(timezone.utc).isoformat()
clock=time.perf_counter_ns()
panels=[]
parity_checks=0
for r in (2,3,4):
    g=2**r-1
    k=g-r
    H=g+2**k-1
    data=[i for i in range(1,g+1) if i&(i-1)]
    assert len(data)==k
    def syndrome(x):
        s=0
        for i in range(1,g+1):
            if x>>(i-1)&1:
                s^=i
        return s
    def decode(j):
        c=sum(((j>>b)&1)<<(i-1) for b,i in enumerate(data))
        s=syndrome(c)
        for b in range(r):
            c^=((s>>b)&1)<<((1<<b)-1)
        assert syndrome(c)==0
        return c
    cells={}
    counts=errors=0
    for x in range(2**g):
        s=syndrome(x)
        c=x^(1<<(s-1) if s else 0)
        assert syndrome(c)==0
        j=sum(((c>>(i-1))&1)<<b for b,i in enumerate(data))
        assert decode(j)==c
        invoice=g+j
        assert g<=invoice<=H
        counts+=invoice
        errors+=(x^c).bit_count()
        cells.setdefault(c,[]).append(x)
    assert len(cells)==2**k
    assert F(counts,2**g)==g+F(2**k-1,2)
    assert F(errors,2**g)==F(g,g+1)
    for c,cell in cells.items():
        assert {x^c for x in cell}=={0}|{1<<i for i in range(g)}
        assert len(cell)==g+1
        if g<=7:
            for support in range(2**g):
                wrong=sum(((x^c)&support).bit_count()%2 for x in cell)
                assert wrong==support.bit_count()
                parity_checks+=1
    q=g+F(2**k-1,2)
    gain=g-F(2*g,g+1)
    logH=math.log2(H)
    comparisons=[]
    for fee in (10,100,1000,10000):
        candidate=q+fee
        lower=float(gain)*(1+fee/logH)
        item={'f':fee,'candidate_fee':candidate,
              'affine_lower_float':lower,'saving_percent_float':100*(1-float(candidate)/lower)}
        if r==3:
            assert H**2<2**9
            exact_lower=F(21,4)+F(7*fee,6)
            exact_saving=1-candidate/exact_lower
            assert (candidate<exact_lower)==(fee>F(111,2))
            item.update({'conservative_exact_lower':exact_lower,
                         'conservative_exact_saving':exact_saving,
                         'conservative_saving_percent_float':100*float(exact_saving)})
        comparisons.append(item)
    panels.append({'r':r,'block':g,'cap':H,'worlds':2**g,'cells':len(cells),
                   'queries':q,'error_fraction':F(1,g+1),'comparisons':comparisons})
result={'status':'PASS','contributor':'Codex (GPT-6)',
        'scope':'exact 3-, 7- and 15-bit quantizer and count checks; exact 7-bit fee inequality',
        'started_utc':started,'ended_utc':datetime.now(timezone.utc).isoformat(),
        'panels':panels,'parity_checks':parity_checks,
        'ordinary_equivalent':'identical Hamming quantizer and invoice adapter ties',
        'complete_cost_or_cpu_gain':False,'elapsed_ns':time.perf_counter_ns()-clock,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
out.write_text(json.dumps(result,indent=2,default=str)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2,default=str))
