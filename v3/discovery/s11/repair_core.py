"""DEVELOPMENT chain-constrained output repair primitives, Codex (GPT-6)."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product

SIGNS=(-1,1)
ALL=set(product(SIGNS,repeat=2))


def compatible(x,h):
    return all(not v or x[i]==v for i,v in enumerate(h))


def admissible(x,relations):
    return all((x[i],x[i+1]) in relation for i,relation in enumerate(relations))


def compile_menu(source,target,h):
    m=len(source)+1
    assert len(target)==m-1 and len(h)<=m
    allowed=[{h[i]} if i<len(h) and h[i] else set(SIGNS) for i in range(m)]
    left=[set() for _ in range(m)];right=[set() for _ in range(m)]
    left[0]=allowed[0];right[-1]=allowed[-1]
    for i in range(1,m):
        left[i]={x for x in allowed[i] if any((y,x) in source[i-1] for y in left[i-1])}
    if not left[-1]:return None
    for i in range(m-2,-1,-1):
        right[i]={x for x in allowed[i] if any((x,y) in source[i] for y in right[i+1])}
    menus=[]
    for i,relation in enumerate(source):
        projection={(x,y) for x,y in relation if x in left[i] and y in right[i+1]}
        menus.append({(a,b) for a,b in product((0,1),repeat=2)
                      if all((x*(1-2*a),y*(1-2*b)) in target[i] for x,y in projection)})
    return menus


def mask_network(m,menu,cap):
    if menu is None or cap<0:return None
    @lru_cache(None)
    def can(i,previous,count):
        if i==m:return True
        return any(count+b<=cap and (not i or (previous,b) in menu[i-1])
                   and can(i+1,b,count+b) for b in (0,1))
    root=(0,0,0)
    if not can(*root):return None
    nodes=[root];known={root};out={};edges=[]
    for key in nodes:
        i,previous,count=key;out[key]=[]
        if i==m:continue
        for b in (0,1):
            child=(i+1,b,count+b)
            if count+b>cap or (i and (previous,b) not in menu[i-1]) or not can(*child):continue
            edge=len(edges);edges.append((key,child,i,b));out[key].append(edge)
            if child not in known:known.add(child);nodes.append(child)
    return {'root':root,'nodes':nodes,'edges':edges,'out':out}


def joint_network(source,menu,z,cap,mode):
    m=len(source)+1
    @lru_cache(None)
    def can(i,previous,oldflip,count):
        if i==m:return True
        for x in SIGNS:
            if (i<len(z) and x!=z[i]) or (i and (previous,x) not in source[i-1]):continue
            for b in ((0,1) if mode else (0,)):
                if count+b>cap or (mode and i and (oldflip,b) not in menu[i-1]):continue
                if can(i+1,x,b,count+b):return True
        return False
    root=(0,0,0,0)
    if (mode and menu is None) or not can(*root):return None
    nodes=[root];known={root};out={};edges=[]
    for key in nodes:
        i,previous,oldflip,count=key;out[key]=[]
        if i==m:continue
        for x in SIGNS:
            if (i<len(z) and x!=z[i]) or (i and (previous,x) not in source[i-1]):continue
            for b in ((0,1) if mode else (0,)):
                child=(i+1,x,b,count+b)
                if count+b>cap or (mode and i and (oldflip,b) not in menu[i-1]) or not can(*child):continue
                edge=len(edges);edges.append((key,child,i,x,b));out[key].append(edge)
                if child not in known:known.add(child);nodes.append(child)
    return {'root':root,'nodes':nodes,'edges':edges,'out':out}


def point_comparator(x,w,f,q,H,menus,networks):
    best=F(0);witness=('stop0',)
    for h,network in networks.items():
        if network is None or not compatible(x,h):continue
        values={};choice={}
        for key in reversed(network['nodes']):
            outgoing=network['out'][key]
            if not outgoing:values[key]=F(0);continue
            options=[]
            for e in outgoing:
                _,child,i,b=network['edges'][e]
                options.append((w[i]*x[i]*(1-2*b)+f[i]*b+values[child],e))
            values[key],choice[key]=min(options)
        cost=values[network['root']]+sum((q[j] for j,v in enumerate(h) if v),F(0))
        if cost<best:
            best=cost;key=network['root'];mask=0
            while network['out'][key]:
                _,child,i,b=network['edges'][choice[key]];mask|=b<<i;key=child
            witness=('stop1',h,mask)
    return best,witness


def separator(rows,w,f,q,H,source,menus):
    best=None;witness=None;counts={'networks':0,'states':0,'edges':0}
    for z,(fee,coeff) in rows.items():
        choices=[(None,None,0,0,F(0))]
        choices += [(h,menu,1,H-sum(v!=0 for v in h),sum((q[j] for j,v in enumerate(h) if v),F(0)))
                    for h,menu in menus.items() if menu is not None and compatible(z,h) and sum(v!=0 for v in h)<=H]
        for h,menu,mode,cap,query_fee in choices:
            network=joint_network(source,menu,z,cap,mode)
            if network is None:continue
            counts['networks']+=1;counts['states']+=len(network['nodes']);counts['edges']+=len(network['edges'])
            values={};chosen={}
            for key in reversed(network['nodes']):
                outgoing=network['out'][key]
                if not outgoing:values[key]=F(0);continue
                options=[]
                for e in outgoing:
                    _,child,i,x,b=network['edges'][e]
                    score=w[i]*(coeff[i]-mode+2*b)*x-f[i]*b
                    options.append((score+values[child],e))
                values[key],chosen[key]=max(options)
            value=fee-query_fee+values[network['root']]
            if best is None or value>best:
                best=value;truth=[];mask=0;key=network['root']
                while network['out'][key]:
                    _,child,i,x,b=network['edges'][chosen[key]];truth.append(x);mask|=b<<i;key=child
                witness={'truth':truth,'comparator_history':h,'comparator_mask':mask,'mode':mode}
    assert best is not None
    return best,witness,counts


def integer_distribution(raw,total):
    clipped=[max(F(0),F(float(v))) for v in raw]
    mass=sum(clipped,F(0))
    if not mass:return [total]+[0]*(len(raw)-1)
    quotas=[v*total/mass for v in clipped]
    units=[v.numerator//v.denominator for v in quotas]
    remaining=total-sum(units)
    order=sorted(range(len(units)),key=lambda i:(quotas[i]-units[i],-i),reverse=True)
    for i in order[:remaining]:units[i]+=1
    assert all(v>=0 for v in units) and sum(units)==total
    return units
