"""Reproduce original graph_probe.py input draws, without running its methods."""
import hashlib,json,random,sys,time
from pathlib import Path
out=Path(sys.argv[1]);assert not out.exists();base=Path(__file__).parent
rng=random.Random(64283);cases=[]
for k in range(32):
    n=rng.randrange(2,6 if k<12 else 7);raw=[]
    for v in range(n):raw.append(rng.randrange(0,17))
    raw[0]+=1;total=sum(raw);scale=128*total*(1<<n)
    prizes=[]
    for w in raw:prizes.append(w*64*(1<<n))
    anchors=[]
    for v in range(n):anchors.append(None if rng.randrange(4)==0 else rng.randrange(0,25)*2*total*(1<<n))
    edges=[]
    for v in range(1,n):edges.append([rng.randrange(v),v,rng.randrange(0,17)*total*(1<<n)])
    cases.append(dict(index=k,n=n,raw=raw,scale=scale,prizes=prizes,anchors=anchors,edges=edges))
large=[]
for shape in ('path','star','random'):
    begin=time.perf_counter_ns();n=4096;raw=[]
    for v in range(n):raw.append(rng.randrange(1,33))
    total=sum(raw);scale=65536*2*total;prizes=[]
    for w in raw:prizes.append(w*65536)
    anchors=[]
    for v in range(n):anchors.append(None if rng.randrange(3)==0 else rng.randrange(1,49)*2*total)
    edges=[]
    for v in range(1,n):edges.append([(v-1 if shape=='path' else 0 if shape=='star' else rng.randrange(v)),v,rng.randrange(0,17)*2*total])
    large.append(dict(shape=shape,n=n,scale=scale,prizes=prizes,anchors=anchors,edges=edges,source_ns=time.perf_counter_ns()-begin))
sources={}
for name in ('graph_probe.py','graph_plan.py','graph_inputs.py','graph_node.mjs'):
    sources[name]=hashlib.sha256((base/name).read_bytes()).hexdigest()
out.write_text(json.dumps(dict(seed=64283,python=sys.version,sources=sources,cases=cases,large=large),indent=2)+'\n')
print(json.dumps(dict(cases=len(cases),large=len(large),input_path=str(out))))
