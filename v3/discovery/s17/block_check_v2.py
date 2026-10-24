"""Conditional rational response certificate v2. DEVELOPMENT, Codex (GPT-6).

This checks the finite matrix calculation, not the truth of the supplied
source, compression, orthogonality or edit-norm warrants. No floating inputs.
"""
from fractions import Fraction as F
import json
from pathlib import Path
import re
import sys

MAX_DIM=16
MAX_BITS=4096
MAX_BYTES=1048576
RATIONAL=re.compile(r'-?[0-9]{1,1234}(?:/[1-9][0-9]{0,1233})?\Z')


class InvalidCertificate(ValueError):
    pass


def require(condition,message):
    if not condition:
        raise InvalidCertificate(message)


def rational(value):
    require(type(value) is str and RATIONAL.fullmatch(value) is not None,
            'Use an integer or fraction string, not a float or decimal.')
    z=F(value)
    require(max(abs(z.numerator).bit_length(),z.denominator.bit_length())<=MAX_BITS,
            'Input rational exceeds the declared bit bound.')
    return z


def identity(n):
    return [[F(i==j) for j in range(n)] for i in range(n)]


def add(A,B,scale=F(1)):
    return [[a+scale*b for a,b in zip(row,other)] for row,other in zip(A,B)]


def mul(A,B):
    n=len(A)
    return [[sum((A[i][k]*B[k][j] for k in range(n)),F(0))
             for j in range(n)] for i in range(n)]


def positive(A,strict=False):
    """Exact symmetric Schur elimination, including zero PSD pivots."""
    n=len(A)
    if any(A[i][j]!=A[j][i] for i in range(n) for j in range(n)):
        return False
    B=[row[:] for row in A]
    for i in range(n):
        pivot=B[i][i]
        if pivot<0 or (strict and pivot==0):
            return False
        if pivot==0:
            if any(B[i][j]!=0 for j in range(i+1,n)):
                return False
            continue
        for j in range(i+1,n):
            for k in range(i+1,n):
                B[j][k]-=B[j][i]*B[i][k]/pivot
    return True


def inverse(A):
    n=len(A)
    B=[row[:]+ident for row,ident in zip(A,identity(n))]
    for i in range(n):
        pivot=next((j for j in range(i,n) if B[j][i]),None)
        require(pivot is not None,'Singular denominator.')
        B[i],B[pivot]=B[pivot],B[i]
        z=B[i][i]
        B[i]=[x/z for x in B[i]]
        for j in range(n):
            if j!=i:
                z=B[j][i]
                B[j]=[a-z*b for a,b in zip(B[j],B[i])]
    return [row[n:] for row in B]


def weighted_trace(V,A):
    return sum((V[i][j]*A[j][i] for i in range(len(V)) for j in range(len(V))),F(0))


def matrix(value,n):
    require(type(value) is list and len(value)==n,'Matrix dimension mismatch.')
    require(all(type(row) is list and len(row)==n for row in value),'Matrix is not square.')
    return [[rational(z) for z in row] for row in value]


def integer_text(value):
    """Decimal output without changing Python's process-wide input guard."""
    if value == 0:
        return '0'
    sign='-' if value<0 else ''
    value=abs(value)
    chunks=[]
    while value:
        value,part=divmod(value,10**9)
        chunks.append(part)
    return sign+str(chunks[-1])+''.join(f'{part:09d}' for part in reversed(chunks[:-1]))


def fraction_text(value):
    numerator=integer_text(value.numerator)
    return numerator if value.denominator==1 else numerator+'/'+integer_text(value.denominator)


def verify(data):
    require(type(data) is dict,'Expected a certificate object.')
    require(data.get('schema')=='response-block-v1','Unsupported schema.')
    require(set(data)=={'schema','source_id','dimension','C_minus','C_plus','V',
                        'edit_squared','t_lower','t_upper','threshold'},'Unexpected or missing fields.')
    n=data['dimension']
    require(type(n) is int and 1<=n<=MAX_DIM,'Dimension outside1..16.')
    require(type(data['source_id']) is str and 0<len(data['source_id'])<=256,'Invalid source identifier.')
    lo=matrix(data['C_minus'],n); hi=matrix(data['C_plus'],n); V=matrix(data['V'],n)
    I=identity(n)
    require(positive(lo,True),'This version requires C_minus positive definite.')
    require(positive(add(I,hi,-1),True),'This version requires C_plus strictly below I.')
    require(positive(add(hi,lo,-1)),'Reversed or unordered compression bounds.')
    require(positive(V),'Task weight must be symmetric positive semidefinite.')
    require(sum(V[i][i] for i in range(n))==1,'Task weight must have trace1.')
    E=rational(data['edit_squared']); tl=rational(data['t_lower']); tu=rational(data['t_upper'])
    threshold=rational(data['threshold'])
    require(E>=0,'Negative squared edit budget.')
    if E==0:
        require(tl>=0 and tu>=0,'Negative witness parameter.')
        lower=weighted_trace(V,lo); upper=weighted_trace(V,hi)
    else:
        for t in (tl,tu):
            require(t>0 and t*t>=E*(1+t),'Parameter does not satisfy the exact cap inequality.')
        al=1+tl; dl=tl-E-E/tl
        au=1+tu; du=tu-E-E/tu
        den_l=add([[al*z for z in row] for row in I],lo,-dl)
        den_u=add(I,hi,du)
        require(positive(den_l,True) and positive(den_u,True),'Nonpositive denominator.')
        L=mul(lo,inverse(den_l))
        U=[[au*z for z in row] for row in mul(hi,inverse(den_u))]
        lower=weighted_trace(V,L); upper=weighted_trace(V,U)
    # Intersect the final scalar interval, never clip matrix eigenvalues.
    lower=max(F(0),lower); upper=min(F(1),upper)
    require(0<=lower<=upper<=1,'Derived interval failed its consistency check.')
    verdict='below' if upper<threshold else 'above' if lower>threshold else 'unresolved'
    return dict(schema='response-block-result-v1',source_id=data['source_id'],
                lower=fraction_text(lower),upper=fraction_text(upper),threshold=fraction_text(threshold),verdict=verdict,
                scope='Conditional on truthful compression, task-basis and edit-norm warrants; exact rational calculation only.')


def main():
    require(len(sys.argv)==2,'Usage: block_check.py CERTIFICATE.json')
    path=Path(sys.argv[1])
    require(path.stat().st_size<=MAX_BYTES,'Input exceeds1MiB.')
    data=json.loads(path.read_text(encoding='utf-8-sig'))
    print(json.dumps(verify(data),indent=2))


if __name__=='__main__':
    try:
        main()
    except (InvalidCertificate,OSError,json.JSONDecodeError) as error:
        print(json.dumps(dict(status='INVALID',reason=str(error))),file=sys.stderr)
        raise SystemExit(2)
