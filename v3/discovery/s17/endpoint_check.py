"""Exact critical-branch checks for proof.md; DEVELOPMENT, Codex (GPT-6).

For dilation witnesses the source is M=(S^-1-I)^(1/2). Its edited Gram
matrix is evaluated exactly without numerically rounding the square root.
The existence and rank-one edit argument remains a proof duty, not a test.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import platform
from time import perf_counter_ns
from checker_audit import adj_inverse, mm, transpose, plus, eye, det, encode

HERE=Path(__file__).resolve().parent


def scalar(a):
    return a[0][0]


def outer(v,w):
    return mm(v,transpose(w))


def scale(a,z):
    return [[z*x for x in row] for row in a]


def pd(a):
    return a==transpose(a) and all(det([row[:i] for row in a[:i]])>0 for i in range(1,len(a)+1))


def dilation_case(name, lambdas, roots, c, root_tau, side):
    k=len(lambdas); n=2*k
    s_matrix=[[F(0) for _ in range(n)] for _ in range(n)]
    for i,(lam,root) in enumerate(zip(lambdas,roots)):
        assert root*root==lam*(1-lam)
        s_matrix[i][i]=lam
        s_matrix[i+k][i+k]=1-lam
        s_matrix[i][i+k]=s_matrix[i+k][i]=root_tau*root
    assert pd(s_matrix) and pd(plus(eye(n),s_matrix,-1))
    v=[[z] for z in c]+[[F(0)] for _ in range(k)]
    assert scalar(mm(transpose(v),v))==1
    w=mm(s_matrix,v)
    s=scalar(mm(transpose(v),w))
    m=scalar(mm(transpose(w),w)); q=s-m
    h=(2*m-s)/q if side=='lower' else s/m-2
    E=h*h/(1+h)
    assert h>0 and E>0 and q>0
    # These identities ensure exactly the required cap second moment.
    assert m==(s*(1+h)/(2+h) if side=='lower' else s/(2+h))
    gram=plus(adj_inverse(s_matrix),eye(n),-1)
    assert pd(gram)
    mx=plus(v,w,-1)
    cross=plus(outer(mx,w),outer(w,mx))
    coeff=h/m if side=='lower' else h/q
    assert coeff*coeff*m*q==E
    sign=1 if side=='lower' else -1
    edited=plus(plus(gram,cross,sign*coeff),outer(w,w),E/m)
    assert pd(plus(eye(n),edited))
    expected=s/(1+h) if side=='lower' else (1+h)*s
    new_residual=scale(w,1/(1+h) if side=='lower' else 1+h)
    assert mm(plus(eye(n),edited),new_residual)==v
    actual=scalar(mm(transpose(v),mm(adj_inverse(plus(eye(n),edited)),v)))
    assert actual==expected
    return dict(name=name,side=side,shape=[n,n],C=encode([row[:k] for row in s_matrix[:k]]),
                c=[str(z) for z in c],S=encode(s_matrix),source_gram=encode(gram),
                edited_gram=encode(edited),h=str(h),edit_squared=str(E),
                moment=str(m),value=str(actual),normal_equation_exact=True)


def main():
    output=HERE/'endpoint_result.json'
    if output.exists():
        raise SystemExit('Refusing to overwrite an observed result.')
    start=perf_counter_ns()
    records=[]
    # Both interior branches have elementary rational witnesses.
    old=F(1,2); e=F(1,10); C=1/(1+old*old); E=e*e
    for side,new,t in [('lower',old+e,e/old),('upper',old-e,e/(old-e))]:
        d=t-E-E/t
        bound=C/(1+t-d*C) if side=='lower' else (1+t)*C/(1+d*C)
        assert t*t>E*(1+t) and bound==1/(1+new*new)
        residual=1/(1+new*new); x=new*residual
        assert new*(1-new*x)==x
        records.append(dict(name=side+' interior',C=str(C),e=str(e),t=str(t),
                            source=str(old),edited_source=str(new),value=str(bound)))
    # Derivative equality at the cap is allowed, with no dilation needed.
    e=F(5,6); h=F(5,4); E=e*e
    assert h*h==E*(1+h)
    for side,old,new in [('lower',F(2,3),F(3,2)),('upper',F(3,2),F(2,3))]:
        C=1/(1+old*old)
        bound=C/(1+h) if side=='lower' else (1+h)*C
        assert abs(new-old)==e and bound==1/(1+new*new)
        records.append(dict(name=side+' cap equality',C=str(C),e=str(e),t=str(h),
                            source=str(old),edited_source=str(new),value=str(bound)))
    # Upper cancellation, with strictly slack budget and derivative equality.
    for e in (F(1),F(1,2)):
        old=F(1,2)
        assert old*old<=e*e
        records.append(dict(name='upper zero endpoint',source=str(old),edited_source='0',
                            e=str(e),C='4/5',value='1',budget_slack=str(e*e-old*old)))
    # Two non-eigenvector k=2 cases require a genuine hidden-source dilation.
    # Rational Pythagorean pairs make S itself rational; M need not be.
    for side,rt in [('lower',F(3,4)),('upper',F(1,4))]:
        records.append(dilation_case(side+' strict cap dilation',
                                     [F(9,25),F(25,169)],[F(12,25),F(60,169)],
                                     [F(3,5),F(4,5)],rt,side))
    record=dict(status='PASS',cases=records,case_count=len(records),
                elapsed_ns=perf_counter_ns()-start,python=platform.python_version(),
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                arithmetic_helper_sha256=hashlib.sha256((HERE/'checker_audit.py').read_bytes()).hexdigest(),
                scope='Eight exact branch examples. Finite support for the reconstructed algebra, not a proof of universal sharpness or independent confirmation.')
    output.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(dict(status=record['status'],cases=len(records),elapsed_ns=record['elapsed_ns'],
                         dilation_values=[r['value'] for r in records if 'S' in r])))


if __name__=='__main__':
    main()
