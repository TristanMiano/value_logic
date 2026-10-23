"""All 65536 Boolean functions of the seven-bit Hamming quantizer.

Bit-parallel exact decision-depth recursion; Codex (GPT-6), DEVELOPMENT.
"""
from functools import lru_cache
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import time

path=Path(__file__)
out=path.with_suffix('.json')
assert not out.exists()
started=datetime.now(timezone.utc).isoformat()
clock=time.perf_counter_ns()
n=7
def syn(x):
    s=0
    for i in range(n):
        if x>>i&1:s^=i+1
    return s
code=tuple(x for x in range(128) if not syn(x))
indices={c:i for i,c in enumerate(code)}
Q=tuple(indices[x^(1<<(syn(x)-1))] if syn(x) else indices[x] for x in range(128))
assert len(code)==16
ALL=(1<<65536)-1
ONES=tuple(int(('1'*(1<<j)+'0'*(1<<j))*(1<<(15-j)),2) for j in range(16))

@lru_cache(None)
def constants(mask,bits):
    seen=0
    for x in range(128):
        if x&mask==bits:seen|=1<<Q[x]
    zero=one=ALL
    for j in range(16):
        if seen>>j&1:
            one&=ONES[j]
            zero&=ALL^ONES[j]
    return one|zero

@lru_cache(None)
def can(mask,bits,depth):
    if depth>=n-mask.bit_count():return ALL
    result=constants(mask,bits)
    if depth:
        for i in range(n):
            bit=1<<i
            if not(mask&bit):
                result|=can(mask|bit,bits,depth-1)&can(mask|bit,bits|bit,depth-1)
    return result

counts=[can(0,0,d).bit_count() for d in range(8)]
assert counts[0]==2 and counts[-1]==65536
complement_invariant=ALL
for c in code:
    i,j=indices[c],indices[c^127]
    complement_invariant&=(ONES[i]&ONES[j])|((ALL^ONES[i])&(ALL^ONES[j]))
only_complement=(can(0,0,6) & (ALL^complement_invariant))==0
diff=can(0,0,6)^complement_invariant
witness=None if not diff else (diff&-diff).bit_length()-1
def char_mask(w):
    return sum(1<<i for i,c in enumerate(code) if (w&c).bit_count()%2)

def tree(f,mask=0,bits=0,depth=6):
    if constants(mask,bits)>>f&1:
        x=next(x for x in range(128) if x&mask==bits)
        return f>>Q[x]&1
    for i in range(7):
        bit=1<<i
        if not(mask&bit) and (can(mask|bit,bits,depth-1)&can(mask|bit,bits|bit,depth-1))>>f&1:
            return (i,tree(f,mask|bit,bits,depth-1),tree(f,mask|bit,bits|bit,depth-1))
    raise AssertionError('No depth-bounded query tree')

weights=(3,5,9)
trees=[tree(char_mask(w)) for w in weights]
def evaluate(tr,x):
    used=[]
    while isinstance(tr,tuple):
        i,left,right=tr
        assert i not in used
        used.append(i)
        tr=right if x>>i&1 else left
    return tr,used

transcripts={}
query_total=0
for x in range(128):
    counts=[]
    for tr in trees:
        bit,used=evaluate(tr,x)
        assert len(used)<=6
        for i in range(7):
            if i not in used and len(used)<6+bit:used.append(i)
        assert len(used)==6+bit
        counts.append(len(used))
    pair=[c for c in code if all((c&w).bit_count()%2==count-6 for w,count in zip(weights,counts))]
    assert len(pair)==2 and pair[0]^pair[1]==127
    bit=sum((x^pair[0])>>i&1 for i in range(3))>=2
    counts.append(3+int(bit))
    decoded=pair[int(bit)]
    assert decoded==code[Q[x]]
    old=transcripts.setdefault(decoded,tuple(counts))
    assert old==tuple(counts)
    query_total+=sum(counts)
assert len(set(transcripts.values()))==16 and query_total==128*23
assert counts and [can(0,0,d).bit_count() for d in range(6)]==[2]*6
result=dict(status='PASS',attribution='Codex (GPT-6)',started_utc=started,
            ended_utc=datetime.now(timezone.utc).isoformat(),
            elapsed_ns=time.perf_counter_ns()-clock,
            source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            codewords=list(code),boolean_functions=65536,
            number_with_depth_at_most=counts,
            depth6_exactly_complement_invariant=(diff==0),
            depth6_only_complement_invariant=only_complement,
            disagreement_function_if_any=witness,
            recursion_cache=str(can.cache_info()),
            pure_cap7_construction=dict(episodes=4,mean_queries='23',
                worlds_checked=128,distinct_public_transcripts=16,
                first_three_character_representatives=list(weights),
                trees=trees),
            scope='Exact seven-bit finite Boolean depth characterization only; '
                  'not an all-size theorem or an invoice-cost optimum.')
out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
