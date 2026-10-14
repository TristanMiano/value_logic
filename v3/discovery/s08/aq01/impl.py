"""Exact receipt-law equivalence and reversed policy ranking. DEVELOPMENT."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sys
import g01

HERE=Path(__file__).resolve().parent
COSTS=(2,7,2)


def trace(bits,policy):
    seen=[]
    def get(i):seen.append((i,bits[i]));return bits[i]
    if policy=='center':
        if get(1):get(0);get(2)
    elif policy=='leaf':
        if get(0):
            if get(1):get(2)
        elif get(2):get(1)
    else:raise ValueError(policy)
    known=dict(seen)
    assert all(known.get(i)==0 or known.get(i+1)==0 or (i in known and i+1 in known) for i in (0,1))
    return tuple(seen)


def run(directory):
    directory.mkdir(exist_ok=False);(directory/'impl.py').write_bytes(Path(__file__).read_bytes())
    worlds=list(product((0,1),repeat=3));laws={'P':{x:F(1,8) for x in worlds},
        'Q':{x:(F(1,8) if x[1] else F(1,2) if x==(1,0,1) else F(0)) for x in worlds}}
    records={};channels={}
    for label,law in laws.items():
        assert sum(law.values())==1;record={};channels[label]={}
        for policy in ('center','leaf'):
            channel=defaultdict(F);fee=F(0)
            for bits,prob in law.items():
                if not prob:continue
                receipts=trace(bits,policy);channel[receipts]+=prob;fee+=prob*sum(COSTS[i] for i,_ in receipts)
            record[policy]=fee;channels[label][policy]=channel
        records[label]=record
    assert channels['P']['center']==channels['Q']['center']
    assert records=={'P':{'center':F(9),'leaf':F(35,4)},'Q':{'center':F(9),'leaf':F(73,8)}}
    for label,law in laws.items():
        mass=sum(prob for x,prob in law.items() if x[1]==1)
        repeats=sum(prob for x,prob in law.items() if x[1]==1 and x[0]==1)
        assert mass==F(1,2) and repeats/mass==F(1,2)
    pilot={label:sum(prob for x,prob in law.items() if x[1]==0 and x[0]==1)/F(1,2) for label,law in laws.items()}
    assert pilot=={'P':F(1,2),'Q':F(1)}
    g01.save(directory/'results.json',dict(status='complete',stage='DEVELOPMENT',contributor='Codex (GPT-6)',
        expected_fees=records,center_receipt_laws_identical=True,
        channels={law:{policy:[dict(receipts=key,probability=value) for key,value in ch.items()] for policy,ch in policies.items()} for law,policies in channels.items()},
        pilot_middle_probabilities=pilot,first_five_type_I_probability=F(1,32),additional_pilot_fee_under_Q=10,
        physical_audits=0,source_sha256=g01.sha(__file__),declaration_sha256=g01.sha(HERE/'adequacy_countermodel.md')))
    print(json.dumps(dict(status='complete',expected_fees=records,identical_center_receipts=True),default=g01.encode))


if __name__=='__main__':run(Path(sys.argv[1]))
