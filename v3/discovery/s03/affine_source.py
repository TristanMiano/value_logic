"""Finite GF(2) source compilation with replayed invertible row operations."""
def parity(x):return x.bit_count()&1

def eliminate(matrix,n):
    rows=list(matrix);steps=[];pivot=0
    for j in range(n):
        found=next((i for i in range(pivot,len(rows)) if rows[i]>>j&1),None)
        if found is None:continue
        if found!=pivot:
            rows[pivot],rows[found]=rows[found],rows[pivot];steps.append(('swap',pivot,found))
        for i in range(len(rows)):
            if i!=pivot and rows[i]>>j&1:
                rows[i]^=rows[pivot];steps.append(('xor',i,pivot))
        pivot+=1
    return dict(rows=rows,steps=steps)

def compile_source(matrix,n,targets,available,certificate):
    """Check equivalence by operation replay, then capture immutable relation maps."""
    assert type(n) is int and n>=0
    assert all(type(row) is int and 0<=row<1<<n for row in matrix)
    assert all(type(row) is int and 0<=row<1<<n for row in targets)
    rows=list(matrix);transforms=[1<<i for i in range(len(rows))]
    for op,i,j in certificate['steps']:
        assert type(i) is int and type(j) is int and 0<=i<len(rows) and 0<=j<len(rows)
        if op=='swap':
            rows[i],rows[j]=rows[j],rows[i];transforms[i],transforms[j]=transforms[j],transforms[i]
        elif op=='xor':
            assert i!=j;rows[i]^=rows[j];transforms[i]^=transforms[j]
        else:raise AssertionError('invalid operation')
    assert rows==certificate['rows']
    nonzero=[r for r in rows if r];rank=len(nonzero)
    assert rows==nonzero+[0]*(len(rows)-rank)
    pivots=[(r&-r).bit_length()-1 for r in nonzero]
    assert pivots==sorted(set(pivots))
    assert all(sum((r>>j)&1 for r in rows)==1 for j in pivots)
    free=[j for j in range(n) if j not in pivots]
    assert all(j in available for j in free),'Compiler must not invent query access to latent coordinates.'
    support=[0]*n;rhs_map=[0]*n
    for k,j in enumerate(free):support[j]=1<<k
    for i,j in enumerate(pivots):
        support[j]=sum(1<<k for k,f in enumerate(free) if rows[i]>>f&1)
        rhs_map[j]=transforms[i]
    target_support=[];target_rhs=[]
    for target in targets:
        mask=offset=0
        while target:
            bit=target&-target;j=bit.bit_length()-1;target^=bit
            mask^=support[j];offset^=rhs_map[j]
        target_support.append(mask);target_rhs.append(offset)
    zero_tests=tuple(transforms[rank:]);phase_maps=tuple(target_rhs);size=len(matrix)
    def revise(b):
        assert type(b) is int and 0<=b<1<<size
        if any(parity(test&b) for test in zero_tests):return None
        return tuple(parity(row&b) for row in phase_maps)
    return dict(n=n,rank=rank,free=tuple(free),fact_support=tuple(support),fact_rhs=tuple(rhs_map),
        target_support=tuple(target_support),target_rhs=phase_maps,zero_tests=zero_tests,revise=revise)
