"""Development adapter: decreasing max-min tables via ordinary covering products."""
import math

def covering(f,g,k,counts=None):
    a,b=list(f),list(g); size=1<<k
    for row in (a,b):
        for bit in range(k):
            flag=1<<bit
            for mask in range(size):
                if mask&flag: row[mask]+=row[mask^flag]
    out=[x*y for x,y in zip(a,b)]
    for bit in range(k):
        flag=1<<bit
        for mask in range(size):
            if mask&flag: out[mask]-=out[mask^flag]
    if counts is not None:
        counts['covering_calls']=counts.get('covering_calls',0)+1
        counts['transform_additions']=counts.get('transform_additions',0)+3*k*(size//2)
        counts['transform_products']=counts.get('transform_products',0)+size
    return out

def decreasing(row,k):
    return all(row[mask^1<<bit]>=row[mask] for mask in range(1<<k)
               for bit in range(k) if mask&1<<bit)

def maxmin(f,g,k,counts=None):
    size=1<<k
    if len(f)!=size or len(g)!=size or not decreasing(f,k) or not decreasing(g,k):
        raise ValueError('Expected two decreasing tables on the declared universe')
    if k==0: return [min(f[0],g[0])],[0]
    entries=sorted((-v,mask.bit_count(),side,mask)
                   for side,row in enumerate((f,g)) for mask,v in enumerate(row))
    width=math.isqrt(k*size)
    if width*width<k*size: width+=1
    width=min(width,2*size)
    active=[[0]*size,[0]*size]; answer=[None]*size; split=[None]*size
    for start in range(0,len(entries),width):
        chunk=entries[start:start+width]
        for _,_,side,mask in chunk: active[side][mask]=1
        if not decreasing(active[0],k) or not decreasing(active[1],k):
            raise AssertionError('Tie ordering broke downward closure')
        possible=covering(*active,k,counts)
        if min(possible)<0: raise AssertionError('Negative covering count')
        for mask in range(size):
            if split[mask] is not None or not possible[mask]: continue
            for _,_,side,sub in chunk:
                if counts is not None: counts['tag_scans']=counts.get('tag_scans',0)+1
                if sub&mask!=sub or not active[1-side][mask^sub]: continue
                left=sub if side==0 else mask^sub
                value=min(f[left],g[mask^left])
                if split[mask] is None or value>answer[mask]:
                    answer[mask],split[mask]=value,left
            if split[mask] is None: raise AssertionError('Missing new partition witness')
    if any(s is None for s in split): raise AssertionError('Incomplete convolution')
    return answer,split
